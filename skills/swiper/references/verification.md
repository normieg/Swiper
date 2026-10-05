# Browser verification and completion

Use [evidence-contract](evidence-contract.md) for IDs, statuses, provenance, immutable captures, and discrepancy records; [browser-inspection](browser-inspection.md) for discovered capabilities; [animation-inspection](animation-inspection.md) for timing evidence. Instructions here are checks to execute, not claims of live validation.

**Do not implement multiple unverified batches and defer browser verification until the end.**

## Establish an actual comparison

1. Run the replica in a browser at its recorded local origin. Discover current browser capabilities and confirm session ownership. Keep source and replica sessions distinct when supported (configurable examples: `swiper-src` and `swiper-rep`). Record side/session/origin mapping; confirm current URL and asserted state before every replay/capture so source checks cannot accidentally run on the replica or vice versa.
2. Create a fresh run with actual time, environment, code revision/changed files, intended checks, and results. Preserve failed runs and original artifacts. Action success or a goal's `DONE` narrative requires actual successful verify/assert results.
3. Pair SRC/REP captures only for the same route, state, profile and actual CSS dimensions, phase, equivalent fixture conditions, scroll position, and trigger-relative timing. Match browser/version, zoom, device pixel ratio, fonts/readiness, locale, color scheme, reduced-motion preference, and other relevant environment conditions. Record mismatches; do not infer comparability from filenames.
4. Set tolerance policy in scope.md before scoring. Repeat source captures under matching conditions to establish natural variation; define a reasoned metric, numeric threshold when using numeric scoring, and baseline for this project/state. There is no universal acceptable percentage. Prioritize geometry, behavior, typography/assets, and meaningful motion over antialiasing noise.
5. If masks are needed, record exact regions and reasons before comparing and preserve unmasked originals. Masks must never conceal wrong controls, layout geometry, or motion. Aggregate pixel similarity never excuses a material layout defect.

Browser unavailability blocks the current batch and stops further implementation batches; independent evidence inspection can continue. Build output, code inspection, and unit tests cannot substitute for testing the running replica. Unsupported viewport/timing/semantic inspection leaves those checks transparently blocked, not passed.

## Required batch exit checks

| Check | Required evidence |
| --- | --- |
| State graph | Replay every included batch transition from its asserted fixture/source state to the destination; verify URL, result, persistence, loading/error/validation behavior when observed. Replay reversal/reset and confirm initial assertions. |
| Keyboard/semantics | Exercise keyboard activation, tab order, labels/names, disabled controls, focus entry/trap/restoration and relevant ARIA. Screenshots alone cannot prove nonvisual semantics. |
| Presentation | Register paired SRC/REP screenshots for affected states with matched metadata; inspect geometry, typography, assets, crop, spacing, and controls in addition to any metric. |
| Motion | Recheck changed motion at before, intermediate, and endpoint phases, with actual timing/uncertainty; compare sequence/easing and meaningful interruption/reversal/repeat/reduced-motion outcomes. Endpoint images cannot prove motion fidelity. |
| Responsive | Test the actual required desktop/mobile dimensions and affected breakpoints, including transitions between layouts and profile-specific interactions. A named profile without confirmed dimensions proves nothing. |
| Shared components | Recheck affected consumer routes and variant states after shared changes; propagate stale/failed/blocked status rather than relying on an earlier unrelated run. |
| Differences | Fix critical/major differences and actually recheck, or obtain explicit user acceptance of a documented scope exclusion. Give every minor difference a recorded disposition/reason. |
| Records | Update run results, item verification, component evidence, batch verification runs/discrepancy IDs, mappings, inventories, and session cursor. References must resolve; no pending run counts as evidence. |

A batch can become `verified` only when its required checks pass for the remaining approved scope. An explicitly accepted critical/major exclusion adjusts scope and remains reported as an accepted difference, never equivalence. Open critical/major differences keep failed checks `failed`; unavailable required checks keep them `blocked`. Do not proceed to the next batch on an unverified gate.

## Classify and resolve differences

Severity describes impact; disposition describes resolution. Keep them separate.

| Severity | Examples |
| --- | --- |
| `critical` | Broken required flow, unreachable required state, inaccessible required control. |
| `major` | Material layout, font/asset, semantics, behavior, or motion mismatch. |
| `minor` | Isolated rendering/rasterization noise with demonstrated lack of material effect. |

| Disposition | Rule |
| --- | --- |
| `open` | Record expected/actual, evidence, severity, and next action; it remains unresolved. |
| `fixed` | Requires successful fresh browser recheck of the affected state/transition/profile and shared consumers. An edit alone is not a fix. |
| `accepted` | Requires reason and evidence; means documented difference, not equivalent behavior/design. Demonstrated minor rasterization variance may be accepted routinely without user approval (record why approvalReference is null). Behavior/design omissions, scope exclusions, or accepted unresolved critical/major differences require explicit user acceptance and a real approval reference. |

Do not relabel a material defect minor to pass the gate. Retain failed runs after repair. Fresh meaningful code changes invalidate mapped affected verification and require another run; preserved historical passes do not establish the new revision.

## Final cross-batch check and report

Final verification supplements the per-batch gates. Replay connected flows across batch boundaries, shared navigation and persistence/reset, required desktop/mobile transitions, motion, semantics, and asset/font loading. Confirm:

- Inventories and implementation mappings are nonempty for actual work and traced to valid IDs, files, fixtures, runs, and registered evidence.
- Scoped route families/significant states are covered with reproducible entry/reset steps, or explicitly blocked/excluded; assumed or unvisited variants are not observed coverage.
- Every meaningful batch has actual browser evidence and every required graph transition, affected consumer/variant, profile, and motion check is passed or transparently blocked/excluded.
- Critical/major differences are fixed with fresh evidence or explicitly excluded by the user; minor dispositions and any outstanding discrepancies are reported. Statuses agree with current code and evidence.

Never claim unqualified full fidelity with blockers, unverified checks, unresolved differences, or accepted omissions. Choose final status against the current user scope: for a full replication task, incomplete required browser gates, unverified in-scope checks, or blockers preventing completion mean `BLOCKED`; completed scoped work with disclosed accepted differences/exclusions means `DONE_WITH_CONCERNS`; completed, verified scoped work with no remaining differences means `DONE`. An inspection-only request can finish its inspection deliverable without claiming replica completion; unrelated notes do not automatically block that deliverable. Report actual results using this compact format:

| Report item | Include |
| --- | --- |
| Coverage | Inspected/implemented/verified route families and states; representative fixture limits and remaining variants. |
| Verified checks | Browser-tested behaviors, graph replay/reversal, motion phases/timing, semantics, desktop/mobile dimensions and breakpoint transitions. |
| Accepted minor differences | Evidence-backed reasons and dispositions. |
| User exclusions | Explicitly accepted behavior/design omissions or critical/major scope exclusions with approval references. |
| Blocked/unverified | Exact checks, reasons, affected IDs, and next steps; no inferred passes. |
| Discrepancies | Remaining differences and severity/disposition; changed files and relevant checks. |
| Evidence | Destination `.replica-evidence/` path and run/capture references. |
