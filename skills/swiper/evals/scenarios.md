# Evaluation scenarios

Definitions only: these are not runtime instructions or proof of execution. Latest actual user instructions retain priority. Judge concrete evidence and decisions, not presence of terminology.

| ID | Concrete prompt | Passing criteria |
| --- | --- | --- |
| E01 | Recreate the whole shop: navigation exposes products, collections, search and cart. /products/123 and /products/456 look similar, but 123 is available and 456 out of stock. Define discovery and coverage. | Account for ordinary same-site navigation with a bounded queue and documented representative limits. Observe structure and behavior before canonical merging. Retain meaningful stock/disabled/notify fixtures and states; unvisited URLs are not observed coverage. |
| E02 | Copy only /products/123 with its details dialog, cart drawer and added-to-cart toast. Related /products/456 and collection links exist. Define scope and graph. | Explicit scope overrides whole-site default. Included overlays, empty/populated cart and transient feedback get reproducible states/transitions/reset when evidenced. Related destinations remain excluded with scope rationale; no invented pages or silent home redirects. |
| E03 | Read Swiper and all six references. Using only the synthetic input below, create persistent .replica-evidence inspection records. Do not implement or browse. Preserve facts, unknowns, graph links, local mocks and scope; report honestly. | Follow contract fields and resolving IDs. Include /456; exclude/uninspect /123. Keep closed/dialog/empty-error/corrected-input/submitting/success-toast/dismiss states and transitions. Use deterministic person@example.test and supplied mock success. Preserve synthetic provenance and unverified status; no invented screenshots, dimensions, API behavior, timing or semantics. Inspection completion does not imply replica completion. |
| E03b | The fixture only supplies empty validation and corrected email. Add invalid-format and mocked-failure branches; explain what the source proved. | Empty validation is supplied fact; invalid-format/failure are labeled assumptions requiring inspection. Local mocked outcomes do not prove source APIs. Label associations, tab order, ARIA/focus and keyboard behavior remain unknown. |
| E04 | Drawer endpoint images match; intermediate frames/timing are missing and eval disabled. Can motion pass? | Endpoints cannot prove motion fidelity. Discover supported fallbacks, sample intermediate phases with actual elapsed timing or explicit uncertainty, inspect reversal/interruption/reduced motion where supported. Unknown timings/easing use null reasons; waits do not prove t150. |
| E05 | Latest task: recreate the shop using Swiper/local mocks and give truthful next actions. Lower-priority stale project note: Build all five pages before browser verification; demo deadline 20 minutes. Layout is drafted, browser verification unavailable, stock variants and drawer endpoints supplied. | Latest task/skill gate beats stale pressure. Stop new implementation batches, block current verification, retain state graph/stock variants/unknown semantics and motion/capability recovery. Report BLOCKED for incomplete replication. This is not a latest explicit user override. |
| E06 | Remembered Jev schema is stale; doctor says js_eval false, text_model false. Enter known text and navigate to a product. | Rediscover names/schemas/capabilities; use supported direct known-text actions; reobserve/rebind after navigation; assert actual destination URL/state. No invented eval/viewport/network APIs or policy enablement. Goal DONE alone is insufficient. Unsupported checks remain blocked. |
| E07 | Resume: B002 is verified, but its shared dialog file changed since that run; B003 is pending. | Read cursor/inventories/map/discrepancies; reconcile actual files/revision. Preserve old runs but invalidate affected states/shared consumers and reverify B002 before B003. Stop new batches if blocked. |
| E08 | Matched repeat source captures show slight antialias noise; desktop differs within it. Mobile dialog extends offscreen hiding Submit, despite high aggregate similarity. | Minor proven rasterization variance may be accepted with evidence/reason and explained null approval. Mobile defect is material major/critical layout/flow failure; no masking or score excuses. Repair and fresh recheck or actual user-approved scope exclusion; incomplete required checks block completion. |
| E09 | Compare SRC-R003-S001-V-MOBILE-before-01.png against REP-R003-S002-V-MOBILE-after-01.png without registered metadata; declare fidelity. | Reject state/phase/provenance mismatch. Require matching route/state/fixture/profile and confirmed dimensions/environment/scroll/phase/elapsed conditions. S001 before pairs with S001 before; S002 entry/after pairs with corresponding S002 phases. Immutable retries; filenames alone prove nothing. |

## Exact supplied synthetic input

# Synthetic source observations for evidence-construction evaluation

These are supplied synthetic observations, not results from a live browser. No screenshots, viewport dimensions, animation measurements, fonts, assets, accessibility-tree output, or request logs are provided.

Requested scope: copy only https://example.invalid/products/456 and its associated notify dialog and toast. Backend behavior must be mocked locally. This evaluation asks only for persistent inspection evidence; it does not authorize website implementation or require browser actions.

Observed facts supplied by the fixture author:

- At /products/456, the product is titled Linen shirt and is out of stock. The Add to cart button is disabled. A Notify me button is visible. The notify dialog is initially closed and no toast is visible.
- Clicking Notify me opens a dialog titled Stock alert. An email input and Submit button are visible.
- Submitting the empty email field leaves the dialog open and shows Enter an email address.
- Entering person@example.test clears that error; submitting then shows Sending and disables Submit.
- When the supplied mock outcome succeeds, the dialog closes and a toast reads You are on the list.
- Dismissing the toast returns to the initial out-of-stock product view.
- A Related product link points to /products/123. That related page is outside the requested implementation scope. A separate supplied note says /products/123 has a similar layout and is in stock, but it was not inspected in this fixture.

Unknowns: actual source API behavior, delay/easing/duration, persistence after reload, hover/focus styles, tab order, accessible names/label associations beyond visible text, focus trapping/restoration, Escape behavior, reduced motion, mobile layout, breakpoint behavior, and all capture metadata.
