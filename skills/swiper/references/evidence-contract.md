# Evidence contract

Initialize `.replica-evidence/` from `../assets/evidence-template/` once. On resume preserve every existing record and capture, reconcile actual implementation files, and update status only from fresh evidence. Never overwrite evidence with empty templates or silently discard failed runs.

## Files and identifiers

```text
.replica-evidence/
  scope.md
  capabilities.md
  session.md
  routes.json
  states.json
  interactions.json
  animations.json
  assets.json
  discrepancies.json
  implementation-map.json
  screenshots/source/
  screenshots/replica/
```

The six inventory files contain `{"schemaVersion":1,"<collection>":[]}`, with collection names `routes`, `states`, `interactions`, `animations`, `assets`, and `discrepancies`. The implementation map contains `schemaVersion: 1` and arrays `components`, `batches`, `mappings`. Markdown records define scope, fixtures, profiles, capabilities, runs, and the resume cursor. Keep run/capture registries in session.md or a linked JSON supplement if needed; their IDs and paths must resolve.

Allocate monotonic IDs: `R001` route, `S001` state, `I001` interaction, `A001` animation, `AS001` asset, `D001` discrepancy, `B001` batch, `C001` component, `RUN001` run. State IDs are globally unique, not per route. Pad to at least three digits and expand naturally (for example `S1000`); never reuse an ID, even after retirement. Define fixture IDs (for example `F001`) and viewport profile IDs (for example `VP_DESKTOP`) before referring to them.

Each reference must resolve to an existing record. Paths are relative to `.replica-evidence/` for evidence, and to the destination project for implementation/assets. Ordered entry/action/reset steps use plain language and semantic targets; refresh tool references at runtime instead of preserving stale DOM handles.

## Record fields

Use camelCase fields. These are the complete baseline fields; optional provenance/notes may supplement them without replacing them.

| Record | Fields |
| --- | --- |
| Route | `id, family, urlPattern, observedUrls, fixtures, scopeStatus, entrySteps, componentIds, stateIds, inspectionStatus, implementationStatus, verificationStatus, blockers` |
| State | `id, name, routeId, fixtureId, conditions, viewportProfiles, assertions, entrySteps, resetSteps, semantics, transitions, evidence, confidence, verificationStatus` |
| Interaction | `id, routeId, componentId, sourceStateId, destinationStateId, viewportProfiles, actions, expectedResult, navigation, resetSteps, persistence, mockMapping, evidence, verificationStatus` |
| Animation | `id, routeId, componentId, stateIds, trigger, properties, startValues, endValues, durationMs, delayMs, easing, sequence, repeat, scrollCoupling, interruption, reducedMotion, measurementMethod, confidence, evidence, verificationStatus` |
| Asset | `id, sourceUrl, type, usageIds, metadata, localPath, differences, evidence` |
| Discrepancy | `id, routeId, stateId, viewportProfile, category, severity, disposition, expected, actual, evidence, nextAction, acceptanceReason, approvalReference` |
| Component | `id, name, consumerRouteIds, variantStateIds, files, verificationEvidence` |
| Batch | `id, itemIds, acceptanceChecks, files, fixtureIds, status, verificationRuns, discrepancyIds` |
| Mapping | `itemId, batchId, files, fixtureIds, verificationEvidence` |

Identifiers and paths are strings; reference sets, ordered steps, assertions, evidence, files, blockers, and transitions are arrays. Timing fields are numeric milliseconds when measured; estimated numeric timings must be explicitly marked as estimates with confidence and method. Unknown or unmeasured timings use null with the reasons described below. Descriptive nested objects (semantics, navigation, persistence, mockMapping, metadata, repeat, scrollCoupling, interruption, reducedMotion) record reproducible facts, not tool-specific assumptions. `startValues` and `endValues` map named properties to their values. `transitions` contains objects `{interactionId, destinationStateId}`. Assertions and acceptanceChecks must be observable, reproducible checks, such as visibility, accessible name, focus destination, navigation URL, or a measured comparison threshold.

Use `null` for an inapplicable, unknown, or unmeasured field with a recorded reason in `nullReasons` keyed by field name. Each reason must distinguish inapplicability from unknown/unmeasured information. Unknown observations also require an explicit unknown note and appropriate confidence/blocker; do not substitute invented values. Null never proves zero, absence, or inapplicability. An empty array means no recorded entries, not proven absence. Record the actual reason when inspection cannot establish absence. Scope status is `included`, `excluded`, or `blocked`; exclusions link their rationale/approval in scope.md.

| Field | Values |
| --- | --- |
| inspectionStatus | `uninspected, partial, inspected, blocked` |
| implementationStatus | `pending, in_progress, implemented, blocked` |
| verificationStatus | `unverified, verified, failed, blocked` |
| Batch status | `pending, implementing, verifying, verified, blocked` |
| confidence | `observed, estimated, assumed, blocked` |
| severity | `critical, major, minor` |
| disposition | `open, fixed, accepted` |

`observed` requires direct evidence; `estimated` labels an inference/estimate and its method; `assumed` marks an unverified working assumption. Unknown/blocked facts remain explicit and cannot count as observed coverage. `fixed` requires successful rechecking. `accepted` requires an acceptanceReason and supporting evidence. Evidence-backed minor browser rasterization variance may be accepted without user approval; use approvalReference null with a nullReasons entry explaining why approval is unnecessary. Design or behavior omissions, scope exclusions, and unresolved critical or major differences accepted as exclusions require a real user approvalReference. A capture or declared check alone does not make a record verified.

## Capture and provenance

Each evidence capture record contains:

`path, side, runId, routeId, stateId, viewportProfile, width, height, scrollX, scrollY, fixtureId, phase, elapsedMs, interactionId, animationId, observedAt, provenance`.

Use `side` `SRC` or `REP`, exact viewport dimensions in CSS pixels, numeric scroll offsets, an ISO-8601 observation time, and the named fixture. Record interactionId/animationId when applicable; otherwise null with a reason. Stable captures can use elapsedMs null with a reason; motion captures record elapsed time relative to the documented trigger. `provenance` describes the method/tool, originating URL or local source, and facts supported by that capture. Add provenance to nonvisual observations too: URL, state, viewport, action, time, and supporting capture or inspection output. Preserve distinctions between observed facts, inferred/estimated facts, assumptions, unknowns, blockers, and accepted differences.

`evidence` and `verificationEvidence` may contain complete capture objects or path references to a fully defined capture registry. Never use a bare unregistered path as proof. Each run defines its ID, observation time, environment, checks/results, status, and evidence. Actual runs record actual results and tool output; pending runs contain intended checks and remain unverified.

Name captures:

```text
<SIDE>-<ROUTE_ID>-<STATE_ID>-V-<VIEWPORT>-<PHASE>[-<CAPTURE>].png
SRC-R003-S002-V-VP_DESKTOP-t150-01.png
REP-R003-S002-V-VP_DESKTOP-t150-01.png
```

Use phases such as `before`, `after`, or `t150`. Store SRC under `screenshots/source/` and REP under `screenshots/replica/`. A retry creates a new immutable suffix (01, 02, ...), capture record, and run association; never overwrite a previous capture. Pair only the same route, state, fixture, named viewport/dimensions, environment, phase, elapsed time, and scroll position. Record tolerance metric/baseline and masks with reasons in scope.md before evaluating comparisons. Following a transition, captures use the destination state ID, including intermediate frames of its entry animation; the preceding capture uses the source state ID.

## Scope, capabilities, and resume notes

scope.md establishes source URL, scope, exclusions/approvals, destination conventions, route boundaries, representative fixtures and local mock mappings, named viewport dimensions, comparison environment, tolerance metric/baseline, and masks/reasons. Fresh entries say **Not established**.

capabilities.md records discovery date/version, exact current tool names/schemas, supported operations, inspection access, text-entry restrictions, unsupported features, and fallback mappings. Fresh entries say **Not checked**. Do not treat a remembered API as discovery.

session.md tracks current phase, current batch, last successfully verified item, next item, known blockers, and outstanding critical discrepancies. Maintain this cursor after meaningful progress; preserve history and run evidence on resume. Do not advance past an unverified batch when browser verification is blocked.

## Connected illustrative example

**The entire example below is illustrative and was never executed.** Its times, assets, component paths, semantics, and captures are specifications only, not observations or passed checks. All confidence remains assumed and verification unverified. R003 is the PRODUCT_DETAIL `/products/:id` family; F001 is a representative product. I004 opens S002 from S001, A001 describes its entry animation, C001 is its component, B001 is the intended implementation batch, and RUN001 is the intended verification run. The combined envelope shows records that belong in their respective inventory files; fixtures/profiles/runs/captures belong in scope/session records or linked supplements. A real inspection must replace assumptions before implementation and verification.

```json
{
  "schemaVersion": 1,
  "exampleOnly": true,
  "fixtures": [
    {"id":"F001","name":"Available product 42","sourceSetup":"Open /products/42 with the product available and details modal closed.","mockMapping":{"productId":"42","available":true,"title":"Sample product"},"reset":"Close modal and reload /products/42."}
  ],
  "viewportProfiles": [
    {"id":"VP_DESKTOP","width":1440,"height":900,"deviceScaleFactor":1}
  ],
  "runs": [
    {"id":"RUN001","status":"unverified","observedAt":null,"nullReasons":{"observedAt":"Illustrative run never executed"},"comparisonEnvironment":{"browser":"Illustrative Chromium","zoom":1,"locale":"en-US","colorScheme":"light","reducedMotion":"no-preference"},"checks":["Compare paired before, t150, and after captures at identical dimensions.","Open with keyboard; confirm focus trapping and Escape restoration."],"evidence":["screenshots/source/SRC-R003-S001-V-VP_DESKTOP-before-01.png","screenshots/source/SRC-R003-S002-V-VP_DESKTOP-t150-01.png","screenshots/source/SRC-R003-S002-V-VP_DESKTOP-after-01.png","screenshots/replica/REP-R003-S001-V-VP_DESKTOP-before-01.png","screenshots/replica/REP-R003-S002-V-VP_DESKTOP-t150-01.png","screenshots/replica/REP-R003-S002-V-VP_DESKTOP-after-01.png"]}
  ],
  "captures": [
    {"path":"screenshots/source/SRC-R003-S001-V-VP_DESKTOP-before-01.png","side":"SRC","runId":"RUN001","routeId":"R003","stateId":"S001","viewportProfile":"VP_DESKTOP","width":1440,"height":900,"scrollX":0,"scrollY":0,"fixtureId":"F001","phase":"before","elapsedMs":0,"interactionId":"I004","animationId":null,"observedAt":null,"provenance":{"method":"illustrative capture specification","facts":["Capture belongs to the named state and phase."],"source":"https://example.invalid/products/42"},"nullReasons":{"observedAt":"Never executed","animationId":"Stable endpoint capture"}},
    {"path":"screenshots/source/SRC-R003-S002-V-VP_DESKTOP-t150-01.png","side":"SRC","runId":"RUN001","routeId":"R003","stateId":"S002","viewportProfile":"VP_DESKTOP","width":1440,"height":900,"scrollX":0,"scrollY":0,"fixtureId":"F001","phase":"t150","elapsedMs":150,"interactionId":"I004","animationId":"A001","observedAt":null,"provenance":{"method":"illustrative capture specification","facts":["Capture belongs to the named state and phase."],"source":"https://example.invalid/products/42"},"nullReasons":{"observedAt":"Never executed"}},
    {"path":"screenshots/source/SRC-R003-S002-V-VP_DESKTOP-after-01.png","side":"SRC","runId":"RUN001","routeId":"R003","stateId":"S002","viewportProfile":"VP_DESKTOP","width":1440,"height":900,"scrollX":0,"scrollY":0,"fixtureId":"F001","phase":"after","elapsedMs":300,"interactionId":"I004","animationId":null,"observedAt":null,"provenance":{"method":"illustrative capture specification","facts":["Capture belongs to the named state and phase."],"source":"https://example.invalid/products/42"},"nullReasons":{"observedAt":"Never executed","animationId":"Stable endpoint capture"}},
    {"path":"screenshots/replica/REP-R003-S001-V-VP_DESKTOP-before-01.png","side":"REP","runId":"RUN001","routeId":"R003","stateId":"S001","viewportProfile":"VP_DESKTOP","width":1440,"height":900,"scrollX":0,"scrollY":0,"fixtureId":"F001","phase":"before","elapsedMs":0,"interactionId":"I004","animationId":null,"observedAt":null,"provenance":{"method":"illustrative capture specification","facts":["Capture belongs to the named state and phase."],"source":"http://localhost:3000/products/42"},"nullReasons":{"observedAt":"Never executed","animationId":"Stable endpoint capture"}},
    {"path":"screenshots/replica/REP-R003-S002-V-VP_DESKTOP-t150-01.png","side":"REP","runId":"RUN001","routeId":"R003","stateId":"S002","viewportProfile":"VP_DESKTOP","width":1440,"height":900,"scrollX":0,"scrollY":0,"fixtureId":"F001","phase":"t150","elapsedMs":150,"interactionId":"I004","animationId":"A001","observedAt":null,"provenance":{"method":"illustrative capture specification","facts":["Capture belongs to the named state and phase."],"source":"http://localhost:3000/products/42"},"nullReasons":{"observedAt":"Never executed"}},
    {"path":"screenshots/replica/REP-R003-S002-V-VP_DESKTOP-after-01.png","side":"REP","runId":"RUN001","routeId":"R003","stateId":"S002","viewportProfile":"VP_DESKTOP","width":1440,"height":900,"scrollX":0,"scrollY":0,"fixtureId":"F001","phase":"after","elapsedMs":300,"interactionId":"I004","animationId":null,"observedAt":null,"provenance":{"method":"illustrative capture specification","facts":["Capture belongs to the named state and phase."],"source":"http://localhost:3000/products/42"},"nullReasons":{"observedAt":"Never executed","animationId":"Stable endpoint capture"}}
  ],
  "routes": [
    {"id":"R003","family":"PRODUCT_DETAIL","urlPattern":"/products/:id","observedUrls":[],"fixtures":["F001"],"scopeStatus":"included","entrySteps":["Load fixture F001 at /products/42."],"componentIds":["C001"],"stateIds":["S001","S002"],"inspectionStatus":"uninspected","implementationStatus":"pending","verificationStatus":"unverified","blockers":[]}
  ],
  "states": [
    {"id":"S001","name":"Modal closed","routeId":"R003","fixtureId":"F001","conditions":["F001 available; details modal closed"],"viewportProfiles":["VP_DESKTOP"],"assertions":["Details button is visible; dialog is absent."],"entrySteps":["Load /products/42 with F001."],"resetSteps":["Close the dialog or reload F001."],"semantics":{"buttonName":"View details","focus":"Details button is reachable by Tab."},"transitions":[{"interactionId":"I004","destinationStateId":"S002"}],"evidence":["screenshots/source/SRC-R003-S001-V-VP_DESKTOP-before-01.png","screenshots/replica/REP-R003-S001-V-VP_DESKTOP-before-01.png"],"confidence":"assumed","verificationStatus":"unverified"},
    {"id":"S002","name":"Modal open","routeId":"R003","fixtureId":"F001","conditions":["I004 activated; dialog present, including opening phase"],"viewportProfiles":["VP_DESKTOP"],"assertions":["A dialog named Product details is visible.","Tab cycles within the dialog; Escape closes it and restores focus to View details."],"entrySteps":["Enter S001.","Activate View details as specified by I004."],"resetSteps":["Press Escape; reload F001 if necessary."],"semantics":{"role":"dialog","accessibleName":"Product details","ariaModal":true,"focus":"Move focus inside on open; trap until closed; restore to trigger."},"transitions":[],"evidence":["screenshots/source/SRC-R003-S002-V-VP_DESKTOP-t150-01.png","screenshots/replica/REP-R003-S002-V-VP_DESKTOP-t150-01.png","screenshots/source/SRC-R003-S002-V-VP_DESKTOP-after-01.png","screenshots/replica/REP-R003-S002-V-VP_DESKTOP-after-01.png"],"confidence":"assumed","verificationStatus":"unverified"}
  ],
  "interactions": [
    {"id":"I004","routeId":"R003","componentId":"C001","sourceStateId":"S001","destinationStateId":"S002","viewportProfiles":["VP_DESKTOP"],"actions":["Enter S001 using F001.","Refresh runtime browser references.","Activate the button named View details."],"expectedResult":["Enter S002; dialog appears and takes focus."],"navigation":{"type":"none","url":"/products/42"},"resetSteps":["Press Escape and confirm focus returns to View details."],"persistence":{"reload":"Modal resets to closed","storage":"None"},"mockMapping":{"fixtureId":"F001","effect":"Set local modalOpen to true; no network mutation."},"evidence":["screenshots/source/SRC-R003-S001-V-VP_DESKTOP-before-01.png","screenshots/replica/REP-R003-S001-V-VP_DESKTOP-before-01.png","screenshots/source/SRC-R003-S002-V-VP_DESKTOP-after-01.png","screenshots/replica/REP-R003-S002-V-VP_DESKTOP-after-01.png"],"verificationStatus":"unverified"}
  ],
  "animations": [
    {"id":"A001","routeId":"R003","componentId":"C001","stateIds":["S001","S002"],"trigger":"I004 opens the dialog","properties":["opacity","transform"],"startValues":{"opacity":0,"transform":"translateY(8px)"},"endValues":{"opacity":1,"transform":"translateY(0px)"},"durationMs":300,"delayMs":0,"easing":"ease-out","sequence":["Fade and translate concurrently."],"repeat":{"count":1},"scrollCoupling":{"type":"none"},"interruption":{"closeDuringOpen":"Reverse toward closed; inspect before implementation."},"reducedMotion":{"behavior":"Show endpoint immediately","verificationStatus":"unverified"},"measurementMethod":"Illustrative timestamps; actual measurements must replace these values.","confidence":"assumed","evidence":["screenshots/source/SRC-R003-S001-V-VP_DESKTOP-before-01.png","screenshots/replica/REP-R003-S001-V-VP_DESKTOP-before-01.png","screenshots/source/SRC-R003-S002-V-VP_DESKTOP-t150-01.png","screenshots/replica/REP-R003-S002-V-VP_DESKTOP-t150-01.png","screenshots/source/SRC-R003-S002-V-VP_DESKTOP-after-01.png","screenshots/replica/REP-R003-S002-V-VP_DESKTOP-after-01.png"],"verificationStatus":"unverified"}
  ],
  "assets": [
    {"id":"AS001","sourceUrl":"https://example.invalid/product-42.png","type":"image","usageIds":["R003","S001","C001"],"metadata":{"width":800,"height":800,"mimeType":"image/png","provenance":"Illustrative fixture asset; not downloaded"},"localPath":"public/mocks/product-42.png","differences":["Placeholder only; real asset inspection pending."],"evidence":["screenshots/source/SRC-R003-S001-V-VP_DESKTOP-before-01.png","screenshots/replica/REP-R003-S001-V-VP_DESKTOP-before-01.png"]}
  ],
  "discrepancies": [
    {"id":"D001","routeId":"R003","stateId":"S002","viewportProfile":"VP_DESKTOP","category":"motion","severity":"minor","disposition":"open","expected":"Source and replica match at t150.","actual":"Illustrative potential mismatch; no comparison performed.","evidence":["screenshots/source/SRC-R003-S002-V-VP_DESKTOP-t150-01.png","screenshots/replica/REP-R003-S002-V-VP_DESKTOP-t150-01.png"],"nextAction":"Measure source, implement B001, and compare paired t150 captures.","acceptanceReason":null,"approvalReference":null,"nullReasons":{"acceptanceReason":"Open difference, not accepted","approvalReference":"No approval requested or recorded"}}
  ],
  "components": [
    {"id":"C001","name":"ProductDetailsDialog","consumerRouteIds":["R003"],"variantStateIds":["S001","S002"],"files":["src/components/ProductDetailsDialog.tsx"],"verificationEvidence":["screenshots/source/SRC-R003-S002-V-VP_DESKTOP-after-01.png","screenshots/replica/REP-R003-S002-V-VP_DESKTOP-after-01.png"]}
  ],
  "batches": [
    {"id":"B001","itemIds":["R003","S001","S002","I004","A001","AS001","C001"],"acceptanceChecks":["Dialog opening matches before/t150/after source phases.","Keyboard focus enters, traps, and restores on Escape."],"files":["src/components/ProductDetailsDialog.tsx"],"fixtureIds":["F001"],"status":"pending","verificationRuns":["RUN001"],"discrepancyIds":["D001"]}
  ],
  "mappings": [
    {"itemId":"S001","batchId":"B001","files":["src/components/ProductDetailsDialog.tsx"],"fixtureIds":["F001"],"verificationEvidence":["screenshots/source/SRC-R003-S001-V-VP_DESKTOP-before-01.png","screenshots/replica/REP-R003-S001-V-VP_DESKTOP-before-01.png"]},
    {"itemId":"S002","batchId":"B001","files":["src/components/ProductDetailsDialog.tsx"],"fixtureIds":["F001"],"verificationEvidence":["screenshots/source/SRC-R003-S002-V-VP_DESKTOP-after-01.png","screenshots/replica/REP-R003-S002-V-VP_DESKTOP-after-01.png"]},
    {"itemId":"I004","batchId":"B001","files":["src/components/ProductDetailsDialog.tsx"],"fixtureIds":["F001"],"verificationEvidence":["screenshots/source/SRC-R003-S002-V-VP_DESKTOP-after-01.png","screenshots/replica/REP-R003-S002-V-VP_DESKTOP-after-01.png"]},
    {"itemId":"A001","batchId":"B001","files":["src/components/ProductDetailsDialog.tsx"],"fixtureIds":["F001"],"verificationEvidence":["screenshots/source/SRC-R003-S001-V-VP_DESKTOP-before-01.png","screenshots/replica/REP-R003-S001-V-VP_DESKTOP-before-01.png","screenshots/source/SRC-R003-S002-V-VP_DESKTOP-t150-01.png","screenshots/replica/REP-R003-S002-V-VP_DESKTOP-t150-01.png","screenshots/source/SRC-R003-S002-V-VP_DESKTOP-after-01.png","screenshots/replica/REP-R003-S002-V-VP_DESKTOP-after-01.png"]},
    {"itemId":"AS001","batchId":"B001","files":["src/components/ProductDetailsDialog.tsx"],"fixtureIds":["F001"],"verificationEvidence":["screenshots/source/SRC-R003-S002-V-VP_DESKTOP-after-01.png","screenshots/replica/REP-R003-S002-V-VP_DESKTOP-after-01.png"]}
  ],
  "scope": {"sourceUrl":"https://example.invalid","replicaUrl":"http://localhost:3000","fixtureIds":["F001"],"viewportProfiles":["VP_DESKTOP"],"tolerance":{"metric":"Illustrative pixel mismatch fraction","threshold":0.01,"baseline":["screenshots/source/SRC-R003-S001-V-VP_DESKTOP-before-01.png","screenshots/source/SRC-R003-S002-V-VP_DESKTOP-t150-01.png","screenshots/source/SRC-R003-S002-V-VP_DESKTOP-after-01.png"]},"masks":[]}
}
```
