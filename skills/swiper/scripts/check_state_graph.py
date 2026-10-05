#!/usr/bin/env python3
"""Read-only structural graph check; deliberately not a coverage validator."""
import json
from pathlib import Path
import sys

DISCLAIMER = 'Structural consistency only; not coverage, browser verification, or fidelity.'


def check_graph(root):
    errors, warnings, indexes = [], [], {}
    for kind, prefix in (('routes', 'R'), ('states', 'S'), ('interactions', 'I')):
        index = indexes[kind] = {}
        try:
            data = json.loads((root / (kind + '.json')).read_text())
        except (OSError, ValueError) as exc:
            errors.append(f'{kind}.json: {exc}')
            continue
        if (not isinstance(data, dict) or type(data.get('schemaVersion')) is not int
                or data.get('schemaVersion') != 1 or not isinstance(data.get(kind), list)):
            errors.append(f'{kind}.json: require schemaVersion 1 and {kind} array')
            continue
        for position, record in enumerate(data[kind]):
            ident = record.get('id') if isinstance(record, dict) else None
            if (not isinstance(ident, str) or not ident.startswith(prefix)
                    or len(ident) < 4 or not ident[1:].isdigit()):
                errors.append(f'{kind}[{position}]: invalid typed id {ident!r}')
            elif ident in index:
                errors.append(f'{kind}: duplicate id {ident}')
            else:
                index[ident] = record

    def resolve(record, field, kind, owner):
        value = record.get(field)
        if value is None:
            reasons = record.get('nullReasons', {})
            reason = reasons.get(field) if isinstance(reasons, dict) else None
            if not isinstance(reason, str) or not reason.strip():
                errors.append(f'{owner}.{field}: null/missing requires explicit nullReasons')
            else:
                warnings.append(f'{owner}.{field}: not checked ({reason})')
            return None
        if not isinstance(value, str) or value not in indexes[kind]:
            errors.append(f'{owner}.{field}: unresolved {value!r}')
            return None
        return value

    for ident, interaction in indexes['interactions'].items():
        resolve(interaction, 'sourceStateId', 'states', ident)
        resolve(interaction, 'destinationStateId', 'states', ident)
    for ident, state in indexes['states'].items():
        resolve(state, 'routeId', 'routes', ident)
        transitions = state.get('transitions')
        if not isinstance(transitions, list):
            errors.append(f'{ident}.transitions: require array')
            continue
        for position, edge in enumerate(transitions):
            owner = f'{ident}.transitions[{position}]'
            if not isinstance(edge, dict):
                errors.append(f'{owner}: require object')
                continue
            interaction_id = resolve(edge, 'interactionId', 'interactions', owner)
            destination = resolve(edge, 'destinationStateId', 'states', owner)
            if interaction_id is None or destination is None:
                continue
            interaction = indexes['interactions'][interaction_id]
            source = interaction.get('sourceStateId')
            target = interaction.get('destinationStateId')
            if source is None or target is None:
                warnings.append(f'{owner}: {interaction_id} edge consistency unknown')
            elif source != ident or target != destination:
                errors.append(f'{owner}: {ident} + {interaction_id} -> {destination} '
                              f'does not match interaction {source} -> {target}')
    return errors, warnings, (len(indexes['states']), len(indexes['interactions']))


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print('Usage: python3 check_state_graph.py <project>/.replica-evidence', file=sys.stderr)
        return 1
    errors, warnings, counts = check_graph(Path(args[0]))
    for warning in warnings:
        print('WARNING: ' + warning)
    for error in errors:
        print('ERROR: ' + error, file=sys.stderr)
    print(f'{"INVALID" if errors else "Structurally valid"}: '
          f'{counts[0]} states, {counts[1]} interactions. {DISCLAIMER}')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
