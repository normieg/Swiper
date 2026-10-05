import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).parents[1] / 'scripts' / 'check_state_graph.py'
spec = importlib.util.spec_from_file_location('check_state_graph', SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class StateGraphTests(unittest.TestCase):
    def graph(self):
        return ([{'id': 'R001'}],
                [{'id': 'S001', 'routeId': 'R001', 'transitions': [
                    {'interactionId': 'I001', 'destinationStateId': 'S002'}]},
                 {'id': 'S002', 'routeId': 'R001', 'transitions': []}],
                [{'id': 'I001', 'sourceStateId': 'S001', 'destinationStateId': 'S002'}])

    def check(self, records):
        with tempfile.TemporaryDirectory() as root:
            for kind, items in zip(('routes', 'states', 'interactions'), records):
                Path(root, kind + '.json').write_text(json.dumps(
                    {'schemaVersion': 1, kind: items}))
            return checker.check_graph(Path(root))

    def test_consistent_graph(self):
        errors, warnings, counts = self.check(self.graph())
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual(counts, (2, 1))

    def test_actual_reused_interaction_failures(self):
        routes = [{'id': 'R001'}]
        states = [{'id': f'S00{i}', 'routeId': 'R001', 'transitions': []}
                  for i in range(1, 7)]
        states[0]['transitions'] = [{'interactionId': 'I006', 'destinationStateId': 'S001'}]
        states[1]['transitions'] = [{'interactionId': 'I003', 'destinationStateId': 'S004'}]
        interactions = [
            {'id': 'I006', 'sourceStateId': 'S006', 'destinationStateId': 'S001'},
            {'id': 'I003', 'sourceStateId': 'S003', 'destinationStateId': 'S004'}]
        errors, _, _ = self.check((routes, states, interactions))
        self.assertEqual(len(errors), 2)
        self.assertTrue(any('S001' in e and 'I006' in e for e in errors))
        self.assertTrue(any('S002' in e and 'I003' in e for e in errors))

    def test_duplicate_and_unresolved_ids(self):
        routes, states, interactions = self.graph()
        states.append(dict(states[0]))
        states[1]['routeId'] = 'R999'
        interactions[0]['destinationStateId'] = 'S999'
        errors, _, _ = self.check((routes, states, interactions))
        self.assertTrue(any('duplicate' in e for e in errors))
        self.assertTrue(any('R999' in e for e in errors))
        self.assertTrue(any('S999' in e for e in errors))

    def test_empty_templates_are_structural_only(self):
        errors, warnings, counts = self.check(([], [], []))
        self.assertEqual((errors, warnings, counts), ([], [], (0, 0)))
        self.assertIn('not coverage', checker.DISCLAIMER)

    def test_null_requires_reason_and_warns(self):
        routes, states, interactions = self.graph()
        interactions[0]['sourceStateId'] = None
        errors, _, _ = self.check((routes, states, interactions))
        self.assertTrue(any('nullReasons' in e for e in errors))
        interactions[0]['nullReasons'] = {'sourceStateId': 'Unknown source; inspection pending'}
        errors, warnings, _ = self.check((routes, states, interactions))
        self.assertEqual(errors, [])
        self.assertTrue(warnings)

    def test_malformed_json(self):
        with tempfile.TemporaryDirectory() as root:
            for kind in ('routes', 'states', 'interactions'):
                Path(root, kind + '.json').write_text('{')
            errors, _, _ = checker.check_graph(Path(root))
            self.assertEqual(len(errors), 3)


if __name__ == '__main__':
    unittest.main()
