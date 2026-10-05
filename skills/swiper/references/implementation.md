# Implement one evidenced batch

Use [evidence-contract](evidence-contract.md) for records/statuses, [discovery-and-state](discovery-and-state.md) for the graph, and [animation-inspection](animation-inspection.md) for motion. This guide defines implementation gates, not another schema.

**Do not implement multiple unverified batches and defer browser verification until the end.**

## Prepare and bound

1. Read destination instructions, package/configuration files, routing, styling, asset conventions, and existing component patterns. Preserve the project's framework and conventions; if the destination is empty, select a suitable framework using the request and constraints and record the choice. This skill forces no framework.
2. Inspect evidence for the next route/state graph slice. Identify shared components first and list their consumer routes and variant states. Implement shared structure before route-specific composition; preserve observed exceptions rather than forcing variants into one layout.
3. Register one bounded batch with explicit route, state, interaction, animation, asset, and component IDs as applicable; each ID must resolve. Define files, deterministic fixture IDs, and observable acceptance checks before coding. Include affected shared consumers in the batch's checks.
4. Require enough source evidence for its presentation, semantics, transitions, responsive behavior, and motion. Unknown outcomes remain assumptions or blockers with reasons; they never become observed coverage merely because local code implements them.

## Implement and map

| Area | Action/check |
| --- | --- |
| Presentation | Reproduce evidenced geometry, typography, colors, surfaces, image crop, responsive changes, and significant variants. Link changes to inventory items. |
| Assets/fonts | Match actual inspected source URLs and metadata to local files and usage IDs. Confirm local loading and font family/weight coverage. Record inaccessible assets, substitutions, and differences; do not guess asset URLs or claim fallback fonts equivalent. |
| Navigation | Map observed source destinations to local routes, preserving meaningful query/hash, browser back/forward, and scroll behavior. Preserve external/out-of-scope destination mappings with their scope disposition; do not silently invent replacement pages or reroute every link home. |
| Semantics | Use evidenced buttons/links, names, labels, disabled states, focus behavior, and relevant ARIA. Any deliberate correction to source behavior is a documented difference. |
| Mock state | Use deterministic local fixtures, controlled loading/error outcomes and reset steps. Reproduce observed validation, cart/search/login, persistence, and transient transitions where in scope. Define reload/storage/session behavior explicitly; resets must restore the asserted fixture. |
| Isolation | Do not call live target APIs for local flows, authentication, carts, payments, search, or mutations. Use local mock handlers/state and locally mapped assets. Distinguish mock implementation from proof of source backend behavior. |
| Motion | Implement observed triggers, properties, timing, easing, sequences, interruption/reversal, repeats, scroll coupling, and reduced-motion behavior. Keep estimates and unavailable measurements explicit. |

Keep fixtures reproducible without personal accounts or uncontrolled live data. Mock an unobserved branch only as a labeled assumption with a discrepancy/blocker; do not fabricate source success or error evidence. Record reset and persistence controls in scope/session evidence.

Update the implementation map with actual files, item-to-batch mappings, shared consumers/variants, and fixture IDs. Mark implementation progress with contract values; code written is not verification. A meaningful change to presentation, navigation, interaction, semantics, mock state, or motion requires browser verification. Fresh changes invalidate affected prior verification, including shared consumers: preserve old runs, set affected items unverified, and record the changed files/revision and recheck scope.

## Hand off this batch

1. Start the replica using the destination's documented command and record its actual local origin. Build/type/unit checks may assist debugging but cannot replace browser verification.
2. Enter batch status `verifying`; run [verification](verification.md) against the running replica before implementing the next batch.
3. If required browser execution or inspection is unavailable, mark the batch/checks `blocked`, retain existing evidence and the resume cursor, and stop further implementation batches. Independent source/evidence inspection may continue. Resume verification of this batch first when the blocker clears.

Only a batch that satisfies verification exit checks may advance to the next implementation batch. Do not count future intended runs, screenshots alone, or successful compilation as a passed gate.
