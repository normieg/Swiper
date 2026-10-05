# Route discovery and significant states

Use [evidence-contract](evidence-contract.md) for record fields, IDs, confidence, and provenance; use [browser-inspection](browser-inspection.md) for supported actions. This guide supplies the discovery procedure, not an alternate schema.

## Account for the bounded route queue

Default scope is the whole website reachable through ordinary navigation. An explicit page/flow request overrides it. Define same-site boundaries, exclusions, fixture limits, and viewport profiles in scope.md before crawling; do not silently turn a whole-site request into one page.

1. Seed a queue with the requested URL and known scoped entry points. Keep each discovered URL, referring page/action, proposed family, and queue disposition in a linked scope/session supplement.
2. Visit queued entries through navigation and inspect links, menus, footer, pagination, and observed flow destinations. Enqueue same-site routes within scope. Record external destinations without recursing; document approved exclusions. Preserve inaccessible and unvisited entries with their reason and next action.
3. Compare observed structure **and behavior** before assigning canonical families. Keep actual URLs in `observedUrls`, representative fixture IDs in `fixtures`, and significant states in `stateIds`. Unknown variants remain explicitly uninspected; a pattern is not evidence that every matching URL was visited.
4. Bound data-driven lists and combinations with representative fixtures and documented selection rationale. Discover route templates rather than endlessly traversing IDs, pagination, filters, or calendars. Account for deferred URLs as represented but unvisited, excluded with rationale, or blocked; no arbitrary page limit implies coverage.
5. Stop only when every queue entry is accounted for and every scoped family/meaningful variant is inspected or explicitly blocked. Report remaining unvisited variants; do not claim full inspection from inferred equivalence.

| Canonicalization decision | Required evidence |
| --- | --- |
| `/products/123` and `/products/456` → family `PRODUCT_DETAIL`, pattern `/products/:id` | Observe both structures and interactions agreeing before merging. |
| Out-of-stock, selected variants, long titles, layout exceptions | Keep meaningful fixture variants and distinct states even inside the shared family; split families if structure/behavior differs. |
| Query, hash, case, trailing slash | Retain when meaningful or unknown; remove only parameters/segments proven to be tracking or no-ops. Record the proof and original URLs. |
| Unvisited matching URL | Record as unknown/uninspected; never add it to `observedUrls` or call it inspected. |

Route `scopeStatus` uses `included`, `excluded`, or `blocked`; `inspectionStatus` uses `uninspected`, `partial`, `inspected`, or `blocked`. Queue bookkeeping can supplement these fields but must not invent inventory status values.

## Build a reproducible state graph

A significant state is a route plus fixture conditions and observable behavior, not merely a screenshot. Allocate globally unique `S001` IDs across all routes. Include validation, loading/submitting, success/error, overlays, unavailable/disabled, selected variants, empty/populated cart, and transient feedback when observed. Avoid the unbounded Cartesian product of unrelated controls; document representative combinations and unresolved exceptions.

1. Define the initial fixture and local mock mapping. Enter a state using repeatable `entrySteps`; establish `conditions`, visible/semantic `assertions`, `viewportProfiles`, and `resetSteps`.
2. Perform one meaningful action from that asserted source state. Observe the actual destination, URL, focus, persistence, and transient effects; allocate a destination state if behavior/conditions differ.
3. Add a first-class `I001` record joining `sourceStateId` and `destinationStateId`; add `{interactionId, destinationStateId}` to the source state's `transitions`. Record ordered semantic `actions`, `expectedResult`, `navigation`, `persistence`, and reset evidence. Self-transitions are valid for repeat actions that preserve a state.
4. Verify reverse action or reset against the initial assertions, then inspect the next significant branch. A reset instruction is not proof that reset works. Share viewport coverage only after observed equivalence; otherwise preserve profile-specific behavior and assertions.
5. Attach registered captures or inspection output with URL, state, viewport, action, and time. Use `confidence` `observed`, `estimated`, `assumed`, or `blocked`; record unknowns explicitly. `verificationStatus` remains `unverified` until actual checks pass, or becomes `failed`/`blocked` from evidence.

## Inspect control behavior and semantics

| Control check | Observe and record |
| --- | --- |
| Hover, focus, click, keyboard activation | Visible changes; button versus link semantics; accessible name; tab order; disabled behavior. |
| Input, selection, submit | Labels, required/error descriptions, validation timing, pending controls, result and persistence. |
| Scroll and navigation | Sticky/revealed elements, destination URL/hash, scroll position and restoration. |
| Open/close and Escape | Dialog/menu role and relevant ARIA; initial focus, trapping where applicable, closing and restoration. |
| Repeat and interruption | Double activation, changed selection mid-request, closing during opening, repeated feedback; eventual state. |

Use supported DOM/accessibility observations and keyboard checks; a screenshot cannot establish labels, tab order, focus trapping, or ARIA. Mark unavailable inspection explicitly. Record source defects and deliberate corrections as discrepancies with expected/actual behavior; never silently claim equivalence after improving the source.

Inspect safely: do not make real payments, send real messages, or perform destructive changes to discover a state. Use authorized harmless source actions; otherwise record the branch blocked/unknown and model it locally with mocks, retaining the distinction from observed behavior.

## Hypothetical application example

**Not executed; all proposed states/interactions remain assumed and unverified until observed.** On R003, fixture F001 starts at S001 (product available, modal closed). I004 opens S002; closing must restore the trigger focus. A variant change may require S003 if availability or controls change. A locally mocked cart action could enter S004 and a transient toast S005. A form branch could be S006 validation error → S007 submitting → S008 success, with separate interactions for each observed transition. Do not create these as source observations merely because they are common UI patterns; replace, omit, or block them according to evidence.
