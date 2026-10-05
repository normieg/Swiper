---
name: website-frontend-replication
description: Use when the user asks to clone, copy, recreate, or reverse engineer a website frontend, including its interactions, responsive layouts, assets, and animations, using Jev browser inspection.
---

# Website Frontend Replication

Recreate the observed frontend with local mocks. User instructions take priority; this workflow adds no approval requirements for unrelated actions.

## Establish the evidence

Inputs: source URL, destination project, optional page/flow scope, framework and viewport constraints. Default to the whole website reachable through ordinary navigation; explicit page/flow scope overrides that default. Infer optional preferences from the destination and record them alongside exclusions and required desktop/mobile viewports.

Read [evidence-contract](references/evidence-contract.md). On first use, copy [assets/evidence-template](assets/evidence-template/) into the destination's `.replica-evidence/`; never replace existing evidence. Maintain `session.md`, scope, capabilities, route/state graph, route and resource inventories, interaction/motion records, presentation/semantic observations, implementation map, verification evidence, and discrepancies there. Link observations to URL, state, viewport, action, capture, and observation time; distinguish observed, inferred, unknown, blocked, and accepted differences.

Inspect before inferring. Never fabricate measurements, timing, screenshots, successful checks, or coverage. Do not permanently assume a Jev API or capability: discover available tools and probe current browser, evaluation, text-entry, and capture support. Read [browser-inspection](references/browser-inspection.md) before browsing; choose supported fallbacks and record limitations.

## Ordered checklist

Each phase consumes the previous evidence and updates it before its exit condition is met. Read the linked reference when entering that phase.

| Phase | Inputs → outputs | Exit condition |
| --- | --- | --- |
| 1. Establish scope/capabilities | Request/project/tools → scope and capability record | Boundaries, viewports, supported inspection methods recorded |
| 2. Discover routes/states | Scope/navigation → route/state graph and inventory; [discovery-and-state](references/discovery-and-state.md) | Scoped route families and meaningful variants identified or explicitly blocked |
| 3. Dissect interactions/motion | Graph/actions → triggers, transitions, intermediate frames, timing; [animation-inspection](references/animation-inspection.md) | Batch behavior observed with reproducible actions |
| 4. Inspect presentation/resources/semantics | States/captures → layout, responsive behavior, assets, semantic evidence; [browser-inspection](references/browser-inspection.md) | Batch has sufficient evidence to implement |
| 5. Implement one bounded batch | Evidence/project → mapped local implementation; [implementation](references/implementation.md) | Only the evidenced batch implemented using mocks |
| 6. Browser verify that batch | Implementation/source evidence → comparisons and discrepancies; [verification](references/verification.md) | Batch verified, repaired and rechecked, or explicitly blocked |
| 7. Repeat 2–6 | Verified batch/remaining graph → next bounded batch | No unverified batch stacking |
| 8. Cross-batch verification | Completed graph/map → final route, state, responsive and motion checks | Completion criteria below met |

Preserve meaningful states such as disabled, unavailable, out-of-stock, empty, error, overlay, and selected variants; do not collapse them into mere data differences. Never merge meaningful route/state variants solely because they look similar; merge only after observed behavior and structure agree. Check button/link names, labels, tab order, disabled behavior, focus trapping/restoration, and relevant ARIA.

**A blocked browser stops additional implementation batches.** Independent evidence inspection may continue. Record the blocker and resume verification of the existing batch when available.

## Resume and finish

On resumption read `session.md`, scope/capabilities, inventories, state graph, implementation map, and discrepancies. Reconcile actual files, reverify stale evidence, then take the next incomplete item.

Completion requires observed coverage of scoped route families/states, required desktop/mobile checks, animation intermediate/timing evidence, and final cross-batch verification. Self-review coverage and evidence consistency. Report `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED`, changed files, checks, blockers, and accepted differences honestly. Never claim full fidelity or browser validation when blocked.
