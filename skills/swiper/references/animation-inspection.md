# Animation inspection and capture

Use [evidence-contract](evidence-contract.md) for `A001` records, provenance, statuses, and capture registration; use [browser-inspection](browser-inspection.md) to discover supported timing/evaluation methods. No live source inspection is implied by this guide.

## Inspect one reproducible sequence

1. Enter the asserted fixture/state at a defined viewport and scroll position. Stabilize fonts, images, layout, and prior motion; record readiness evidence and any assets that remain unresolved. Establish the trigger and all animated elements, including relevant descendants/pseudo-elements.
2. Inspect available computed styles, keyframes, and animation timing before/during/after the trigger. Read-only JS is conditional on freshly confirmed evaluation support and observed selectors, using the documented browser guide; do not invent an inspector API or enable disabled evaluation. Visible inspection/captures are fallbacks with explicit limits.
3. Record `properties`, `startValues`, `endValues`, `delayMs`, `durationMs`, `easing`, `sequence` (including stagger offsets), `repeat`, and `scrollCoupling`. Include concurrent versus sequential motion, iterations/direction, trigger thresholds, and scroll-linked progress when observed. Link `trigger` to the `I001` interaction and `stateIds` to the source/destination states.
4. Reset and replay. Capture before, trigger-relative intermediate frames, and the settled endpoint. Record actual frame timestamps or animation `currentTime` where supported, plus how the trigger origin was established. Sample enough phases to distinguish the observed curve/sequence, not only endpoints.
5. Test reverse motion, interruption at meaningful progress, repeat activation, and the reduced-motion preference where reproducibly supported. Record outcomes in `interruption`, `repeat`, and `reducedMotion`; unavailable preference control remains unknown/blocked.
6. Inspect transient loading, toasts, canvas/video behavior, and motion assets **when observed and relevant**. Register assets as `AS001` with provenance. Do not add speculative animations or mandatory media work where none was observed.

| Evidence quality | Recording rule |
| --- | --- |
| Measured timing/style | Numeric milliseconds and exact inspected values, with `measurementMethod` and supporting output. |
| Visually estimated timing | `confidence: estimated`, method, uncertainty/range in notes; numeric values must be explicitly estimates, never reported as measured. |
| Unknown easing/timing | Explicit unknown note and blocker; do not invent a cubic-bezier curve. Unknown required values may be null with keyed `nullReasons` explaining unavailable measurement, never a silent placeholder. |
| Unsupported inspection | `confidence: blocked` for blocked measurements and `verificationStatus: blocked` for blocked checks; preserve any separately observed facts. No full motion-fidelity claim. |

Tool round trips and `wait` are not precise millisecond clocks. A requested 150 ms wait followed by a screenshot does not prove a t150 frame: scheduling and capture latency intervene. Use the actual measured elapsed time in metadata/phase, or explicitly label its uncertainty and leave precise comparison blocked. An active animation snapshot alone cannot prove its completed endpoint, repeat behavior, or interruption behavior.

## Register immutable PNG captures

Use exactly:

```text
<SIDE>-<ROUTE_ID>-<STATE_ID>-V-<VIEWPORT>-<PHASE>[-<CAPTURE>].png
```

`SIDE` is `SRC` or `REP`; store them under `screenshots/source/` and `screenshots/replica/`. Define named profiles such as `MOBILE` in scope.md with exact CSS dimensions and scope; the filename token must identify the registered `viewportProfile`. Profiles are not evidence that resize/emulation worked. Use actual confirmed dimensions.

The optional suffix distinguishes immutable retries: `01`, `02`, … as in the contract, or capture labels such as `C001`, `C002` within the capture registry. A suffix `C001` is a capture label, not a component reference; component IDs still resolve only in their own inventory. Never overwrite a prior artifact. Request PNG and verify actual format; JPEG bytes renamed `.png` are invalid evidence.

Register every capture with the contract's complete capture fields: fixture, profile/dimensions, scroll, state, phase, elapsed time, interaction/animation IDs, observation time, provenance and run association. The run records environment and checks/results. Use null only with keyed reasons; bare filenames are not proof. Preserve originals and tool outputs.

Pair source and replica only at matching route, state, fixture, viewport/dimensions, scroll, environment, phase, and trigger-relative elapsed conditions. Set tolerance/baseline and any justified masks in scope.md before comparison. After a transition, use the destination state ID, including its entry-animation frames; the preceding frame uses the source state ID.

## Hypothetical capture example

**Naming/application example only; not captured, measured, or verified.** Suppose R003/S002 is an observed open modal and `MOBILE` is a defined profile. `SRC-R003-S002-V-MOBILE-before.png` plus `REP-R003-S002-V-MOBILE-after.png` is **not a valid comparison pair**: phases differ. A valid pair would be `SRC-R003-S002-V-MOBILE-after.png` and `REP-R003-S002-V-MOBILE-after.png`, once their registered metadata also matches.

For an S001 → S002 opening transition, use S001 for the before capture and S002 for `t150` and after captures. A measured 150 ms pair could be `SRC-R003-S002-V-MOBILE-t150-01.png` and `REP-R003-S002-V-MOBILE-t150-01.png`; a retry can use `-C001.png` instead, registered separately. An estimated frame must retain its estimate/uncertainty rather than claiming the filename proves 150 ms. All example confidence stays `assumed` and verification `unverified` until actual inspection supplies evidence.
