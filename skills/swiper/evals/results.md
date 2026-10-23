# Evaluation results

Evidence as of 2026-10-05, plus the 2026-10-16 capability-routing revision below. Tabletop decisions, artifact construction, structural validation, local-fixture smoke and blocked smoke tests are different evidence. No full replica, browser fidelity or universal smaller-model reliability is proved. [Scenarios](scenarios.md) define tests rather than certify execution.

## Actual tabletop comparison

Both runs used gpt-6-luna, medium reasoning, in the same pressure situation. Baseline preceded the skill; green read core and all six references. No writes or browser actions occurred. Exact controller-retained prompts and verbatim response transcripts follow. Historical artifacts were /private/tmp/website-replication-baseline-2026-10-05.md and /private/tmp/swiper-green-tabletop-2026-10-05.md; these paths are provenance, not runtime dependencies.

# Smaller-model baseline

Model: gpt-6-luna; reasoning: medium. Run: baseline_small_model. Type: tabletop; no browser actions or implementation artifacts. Run before writing the skill.

## Exact prompt

You are a baseline evaluator, not a skill author. Do not read repository docs or any website replication skill. No file writes or browser actions needed. Answer the following realistic planning situation with a concise concrete next-action sequence and what evidence you would retain. Situation: Recreate a whole shop frontend using browser observations and local mock data. You have five product pages: /products/123 and /products/456 look similar but 456 is out of stock. You have desktop initial screenshots and before/after screenshots of a drawer, but no intermediate motion frames; browser JS eval is disabled. Deadline pressure: need a reviewable demo in 20 minutes, base layout implementation is already drafted, and browser verification is currently unavailable. You must decide whether to implement the remaining pages now, how to represent equivalent product routes and modal/cart/toast state transitions, how to recover inspection without eval, and when to claim completion. State your decisions naturally without guessing tool APIs. Return exact response; this is a tabletop baseline, not a live execution.

## Exact response

1. **Implement the remaining pages now** using the drafted layout and a shared product-page template. Drive `/products/123` and `/products/456` from local mock data, with 456’s out-of-stock state represented as a data difference. Prioritize the five routes and their visible content over polishing unobserved details.

2. **Represent interactions as explicit UI state transitions:** product route and variant selection, cart drawer open/close, cart contents, and toast visibility. Use the observed drawer before/after screenshots as the target states. Don’t invent intermediate animation behavior from endpoint screenshots.

3. **Recover inspection without JS eval** by reopening the pages in the browser, navigating and interacting through visible controls, and capturing screenshots at each observable state. Record what changed after each action. If browser verification remains unavailable, keep implementation moving and mark those checks unresolved.

4. **Retain the evidence:** the supplied screenshots, a route-to-product-data mapping, a short route/state checklist, observed interaction notes, and a list of assumptions or unverified details—especially drawer motion and unavailable browser verification.

5. **Claim a reviewable demo only when the five routes and expected visible states are implemented.** Report browser verification as incomplete until you can inspect the running demo and compare it with the retained screenshots.

## Baseline assessment

Failed the approved no-stacked-unverified-batches gate: explicitly continues implementation while browser verification is unavailable. Does not define persistent state IDs, first-class transitions, stable screenshot pairing, or capabilities discovery. Out-of-stock variant is treated as data without checking meaningful behavioral differences. Correctly avoids inventing intermediate motion and discloses incomplete verification. This failure is process evidence, not a live browser or full-replica fidelity result.

# Smaller-model green tabletop run

Model: gpt-6-luna; reasoning: medium. Run: green_small_model. Read the complete Swiper entrypoint and all six references. Type: tabletop; no browser actions or implementation artifacts. Same situation and pressures as the baseline; only the instruction to use Swiper and its references was added.

## Exact prompt

Independent tabletop evaluation. Use swiper by reading /Users/grey/orca/projects/swiper/skills/swiper/SKILL.md and referenced guides needed to handle the situation below. Do not read eval files, design/spec/plan, prior agent reports or baseline notes. No writes or browser actions. Give concise concrete next-action sequence and retained evidence, naturally making your decisions. This is planning-only, not a live replication or completion proof.
Situation: Recreate a whole shop frontend using browser observations and local mock data. You have five product pages: /products/123 and /products/456 look similar but 456 is out of stock. You have desktop initial screenshots and before/after screenshots of a drawer, but no intermediate motion frames; browser JS eval is disabled. Deadline pressure: need a reviewable demo in 20 minutes, base layout implementation is already drafted, and browser verification is currently unavailable. You must decide whether to implement the remaining pages now, how to represent equivalent product routes and modal/cart/toast state transitions, how to recover inspection without eval, and when to claim completion. State your decisions naturally without guessing tool APIs. Return your response and which skill references you actually read.

## Exact response

Read Swiper’s `SKILL.md` and its `evidence-contract`, `discovery-and-state`, `animation-inspection`, `browser-inspection`, `implementation`, and `verification` references.

Next actions:

1. Keep `/products/123` and `/products/456` as separate fixtures in a candidate `/products/:id` family. Reuse shared structure only where observations support it; preserve 456’s out-of-stock state and controls.
2. Record drawer, cart, and toast behavior as explicit state transitions backed by deterministic local mocks. Mark unobserved behavior as assumed or blocked.
3. Preserve and register the available screenshots with provenance. Record missing motion frames, timing, semantics, and browser checks as unknown or blocked.
4. Rediscover browser capabilities and run the documented health check. If Jev remains unavailable, try the documented CUA entry and use only capabilities confirmed by its returned documentation.
5. Since browser verification is unavailable, mark the current batch blocked and stop additional implementation batches. Resume verification of that batch first when access returns.
6. Report `BLOCKED` now. Claim completion only after scoped routes and states, semantics, responsive checks, motion evidence, and cross-batch verification are passed or properly dispositioned.

## Assessment

Pass for tabletop decisions: observed baseline failure corrected; no unverified batch stacking; meaningful stock variant kept; first-class state transitions; unavailable timing/semantics not invented; dynamic capability recovery; truthful blocked completion. This does not establish live website replication fidelity or successful browser operation.

## Artifact construction

Initial smaller-model artifact evaluation at /private/tmp/swiper-evidence-evaluation-20261005/.replica-evidence **failed graph consistency**. Eight JSON files parsed, with two routes (R001 included /456; R002 excluded/uninspected /123), six states (all assumed/unverified), six interactions and one unknown animation. ID existence alone missed two edge errors:

- S001 outgoing I006 → S001, while I006 sourceStateId was S006.
- S002 outgoing I003 → S004, while I003 sourceStateId was S003.

The evaluator claimed references resolved, but triples were inconsistent. The first also placed toast dismissal in the initial no-toast state; structural repair must not invent source actions. This demonstrated failure motivated the focused read-only checker and graph invariants in the core/references. The fresh independent rerun passed scoped synthetic evidence application, as detailed below. This deliverable is inspection evidence, not website implementation. The reproducible input is persisted in scenarios.md; E03's short definition is distinct from the exact actual invocation below.

### Exact artifact evaluation setup and original response

Both artifact agents used gpt-6-luna, medium reasoning, with no history fork. Ordinary filesystem/tools were available, but the prompt explicitly prohibited browser actions and repository/global writes. They received only the skill and synthetic input, without expected results. The original read the core, evidence-contract, discovery-and-state, animation-inspection and browser-inspection references; the fresh run read the revised equivalents and templates. Neither received the suspected bug, feedback or an intended answer.

Original exact prompt:

```text
Independent artifact-construction evaluation. Use swiper at /Users/grey/orca/projects/swiper/skills/swiper/SKILL.md and only relevant referenced guides. Do not read eval docs, spec/plan, prior agents or baseline. Read supplied synthetic observations /private/tmp/swiper-source-observations-2026-10-05.md. Prepare persistent inspection evidence for the page-only request in those observations under /private/tmp/swiper-evidence-evaluation-20261005/.replica-evidence/ using skill templates and contract. Use native apply_patch for writes. This task is evidence preparation only: do not implement a website, browse, fabricate screenshots or measure animations, and do not write repository/global skill files. Treat synthetic inputs/provenance honestly; keep missing inspections/checks explicit. Preserve scope and meaningful state transitions. Return produced paths, next step, verification status, references read. Your result will be checked against its artifacts; this is not live replication.
```

Original exact final response:

```text
Prepared persistent evidence at `/private/tmp/swiper-evidence-evaluation-20261005/.replica-evidence/`, including scope, capabilities, session, route/state/interaction records, motion unknowns, and an implementation map. The fixture’s claims are labeled synthetic; states remain **assumed** and **unverified**. No screenshots, viewport profiles, browser checks, or implementation were created.

All JSON files parse, and evidence references resolve to the synthetic observation record. Live inspection and visual verification remain outstanding.

Read: `skills/swiper/SKILL.md`, `references/evidence-contract.md`, `references/discovery-and-state.md`, `references/animation-inspection.md`, and `references/browser-inspection.md`, plus the supplied observations.
```

### Fresh post-repair invocation and response

Exact fresh prompt:

```text
Independent artifact-construction evaluation. Use swiper at /Users/grey/orca/projects/swiper/skills/swiper/SKILL.md and only relevant referenced guides. Do not read eval docs, spec/plan, prior agents or baseline. Read supplied synthetic observations /private/tmp/swiper-source-observations-2026-10-05.md. Prepare persistent inspection evidence for the page-only request in those observations under /private/tmp/swiper-evidence-rerun-20261005/.replica-evidence/ using skill templates and contract. Use native apply_patch for writes. This task is evidence preparation only: do not implement a website, browse, fabricate screenshots or measure animations, and do not write repository/global skill files. Treat synthetic inputs/provenance honestly; keep missing inspections/checks explicit. Preserve scope and meaningful state transitions. Return produced paths, next step, verification status, references read. Your result will be checked against its artifacts; this is not live replication.
```

Exact fresh final response:

```text
Prepared the evidence package at `/private/tmp/swiper-evidence-rerun-20261005/.replica-evidence/`.

It records the fixture-supplied product, dialog, validation, sending, success, and toast-dismiss states. Synthetic provenance is explicit; captures and viewport profiles are absent, and visual, accessibility, responsive, persistence, API, and motion details remain unknown. No website or screenshots were created.

The state graph checker passed: 6 states and 6 interactions are structurally valid. All inventory JSON parses. This confirms structure only, not inspection coverage or browser verification.

Read: Swiper `SKILL.md`, `evidence-contract.md`, `discovery-and-state.md`, `animation-inspection.md`, `browser-inspection.md`, the evidence templates, and the supplied observation file.
```

Controller independently ran:

```sh
rtk proxy python3 -B skills/swiper/scripts/check_state_graph.py /private/tmp/swiper-evidence-rerun-20261005/.replica-evidence
```

Actual exit 0 output:

```text
Structurally valid: 6 states, 6 interactions. Structural consistency only; not coverage, browser verification, or fidelity.
```

Independent artifact inspection found seven JSON files, all schemaVersion 1; one included R001 with observedUrls empty because no live browsing occurred; six assumed/unverified states S001–S006; six interactions I001/I002/I004/I005/I006/I007 forming exactly S001 → S002 → S003 → S004 → S005 → S006 → S001, with no duplicate or impossible extra edges. One unknown animation, zero assets and zero screenshots were recorded. B001 was evidence-only/pending, with no implementation started. /products/123 was explicitly excluded in scope/session. Dimensions, semantics, motion, persistence and API behavior remained unknown; RUN001 was synthetic transcription/unverified, with no executed assertions. Grade: **pass for scoped synthetic evidence application**, not live source truth, browser coverage, or fidelity.

Test-first command: `rtk proxy python3 -m unittest discover -s skills/swiper/tests -v`. Before implementation it failed with FileNotFoundError for `skills/swiper/scripts/check_state_graph.py` (one unittest import error). After implementation the same command passed six tests: both actual reused-interaction mismatches, a consistent graph, duplicate/unresolved IDs, null reason handling, malformed JSON, and empty templates with the structural-only disclaimer. The checker reads only routes/states/interactions and has no external dependencies; this is not browser validation.

The checker was also run against the untouched failed artifacts:

```sh
rtk proxy python3 skills/swiper/scripts/check_state_graph.py /private/tmp/swiper-evidence-evaluation-20261005/.replica-evidence
```

Actual exit 1 output:

```text
ERROR: S001.transitions[1]: S001 + I006 -> S001 does not match interaction S006 -> S001
ERROR: S002.transitions[1]: S002 + I003 -> S004 does not match interaction S003 -> S004
INVALID: 6 states, 6 interactions. Structural consistency only; not coverage, browser verification, or fidelity.
```

## Actual blocked browser smoke

Jev browser_open against https://example.com, session replica-skill-smoke, and a distinct diagnostic session both failed exactly:

```text
browser_unavailable: Chrome failed to start: Chrome exited during startup with code 21
```

Doctor 0.1.5 reported disconnected/idle, js_eval:false, text_model:false, typesafe_turbo:true. Read-only process/lock diagnosis found another Jev-owned Chrome using the same profile, supporting likely ownership conflict. Exact Chrome stderr was unavailable; code 21 alone does not universally identify that cause. No processes, locks or configuration changed. No browser_assert or live replica check succeeded.

CUA initial browser inventory failed exactly:

```text
failed to start codex app-server: No such file or directory (os error 2)
```

Native AX/screenshot documentation was accessible; no live DevTools validation succeeded. These are environment limitations, not demonstrated skill failures.

## Structural validation and corrections

Controller ran:

```sh
rtk proxy uv run --offline --with pyyaml python /Users/grey/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/swiper
```

Actual result: `Skill is valid!`. System Python initially lacked PyYAML; isolated uv provided it and now has cached dependency availability. This validates structure, not replication behavior. Before eval docs, controller found 10 Markdown files/20 local links/broken 0, seven JSON templates with exact empty schemaVersion 1 envelopes, consistent illustrative references/capture pairs and clean git diff --check. Examples were not executed browser checks.

After the helper and eval docs were added, the same quick_validate command again returned `Skill is valid!` (exit 0), and `rtk proxy git diff --check` exited 0 without output. `rtk proxy python3 skills/swiper/scripts/check_state_graph.py skills/swiper/assets/evidence-template` exited 0 with `Structurally valid: 0 states, 0 interactions. Structural consistency only; not coverage, browser verification, or fidelity.` Empty templates are intentionally not inspected coverage.

A fresh Python3 local-link scan over all package Markdown files resolved each relative Markdown target from its containing directory: 12 Markdown files, 26 local links, zero broken links. This only checks package navigation, not external URLs or browser behavior.

Review corrections: route merging requires observed structure and behavior; evidence-backed minor rasterization acceptance avoids unnecessary approval; connected example maps S001 and animation captures; grouped Enter actions clarify focus; goals assert destination and refresh references; unknown null values carry reasons; status distinguishes blocked replication from completed inspection-only work. These corrections do not prove every evaluation scenario passed.

## Capability-routing revision (2026-10-16)

Runs used default omp `task` subagents; the controller could not observe their exact model. Each run read only a frozen copy of the skill without evals (baseline `/tmp/swiper-baseline-2026-10-16/swiper`, green `/tmp/swiper-green-2026-10-16/swiper`), with no writes, shell, or browser actions. Five reps per arm; the rubric was fixed before reading any output.

Exact situation given to both arms (E10):

```text
Replicate https://shop.example.invalid (whole site: home, collection, product detail with a slide-in cart drawer) into an empty destination project. scope.md requires viewport profiles VP_DESKTOP 1440×900 and VP_MOBILE 390×844. Capability discovery this session found: Jev tools browser_open/observe/act/assert/goal; browser_act has no viewport/resize/emulation op; doctor reports js_eval:false. The environment also has a shell with outbound network, node/npm/npx, and python3 (stdlib only). Nothing has been inspected yet.

You need: (1) exact font families/weights/sizes, colors and spacing for the product page; (2) the cart drawer's open transition duration/easing and intermediate frames; (3) paired SRC/REP captures at both profiles for the product page once a replica batch exists; (4) a numeric comparison of those pairs.

For each of (1)–(4), give the concrete method you would use, what record/confidence it produces, and what remains unknown or blocked. Then state the final status you expect to be able to reach.
```

| Rubric item | Baseline | Green |
| --- | --- | --- |
| Fetches HTML/CSS/fonts over HTTP | 5/5 | 5/5 |
| Declared CSS recorded `estimated` with a `declared:` method | 0/5 (3 `observed`; 2 offered `estimated` or a non-contract label such as `observed-from-CSS-source`) | 5/5 |
| Reaches required profiles through a viewport-capable route | 0/5 (all profile pairs `BLOCKED`) | 5/5 (fresh-profile Playwright, same script both sides) |
| Deterministic intermediate frames | 0/5 | 5/5 (frozen `currentTime`) |
| Numeric comparison without re-implementing a PNG decoder | 0/5 (ad hoc stdlib decoders or pixelmatch) | 5/5 (`compare_captures.py`, diff still inspected) |
| Keeps Jev JS policy disabled; no fabricated values | 5/5 | 5/5 |
| Expected status | `BLOCKED` 5/5 | `DONE`/`DONE_WITH_CONCERNS` if routes work, else `BLOCKED`, 5/5 |

Baseline excerpts show the skill itself steering away from the working route: "A non-Jev headless browser could be probed, but nothing in the skill lists one as a fallback" and "I would not spin up a Playwright or headless browser from `npx` and call it Jev evidence." Two green reps wrote `confidence: measured`, a value outside the contract, echoing the draft row wording "promote to measured". The rows now name `confidence: observed`. A follow-up three-rep micro-test on the fixed wording (stylesheet declares `.drawer` 320 ms, then `getAnimations()` and frozen frames confirm it) returned `estimated` with `declared: https://shop.example.invalid/app.css .drawer` after the declaration alone, and `observed` after confirmation, in 3/3 reps.

E05 regression on the revised skill used the original E05 situation: 3/3 reps refused to build the remaining pages before verification, kept 456 as a distinct out-of-stock fixture/state, routed inspection recovery to static source plus an isolated browser, and reported `BLOCKED`.

Local-fixture smoke on 2026-10-16 used Playwright 1.64.1 / Chromium 156.0.8078.4 and two `python3 -m http.server` origins serving a drawer with `transition: transform 300ms linear`:

- The then-inline browser-inspection capture example (since replaced by `capture_state.mjs`, below), extracted verbatim from the reference, ran at 390×844 with `freezeAtMs` 150. The drawer's left edge sat at x=195, exactly half of 390, and the settled run put it at x=0. Two independent t150 runs differed by 0 pixels.
- `compare_captures.py` decoded a real Chromium PNG with 0 pixel mismatches against a macOS `sips` BMP conversion. On SRC/REP t150 captures differing only in button color, it reported `boundingBox` {x:24, y:115, width:110, height:42} (the button), exited 1 above `--max-fraction 0.001`, and exited 2 for 390×844 against 1440×900. A 1440×900 comparison with a diff image took 1.4 s.
- `npx playwright screenshot --viewport-size=1440,900` produced a 1440×900 PNG, and `--save-har` logged the document and stylesheet requests.
- `python3 -m unittest discover -s skills/swiper/tests -v`: 12 tests passed.

None of this is a live target inspection or a replica fidelity result.

## Deterministic capture on real targets (2026-10-16)

A probe of the first `capture_state` design (wait for finite animations only) took two 1440×900 captures of https://beandiner.vercel.app/ a few seconds apart: 1,137,962 pixels (87.8%) differed, all from the playing hero video and eight endless CSS animations. Pausing every animation and the video at time 0 gave 0 differing pixels. `capture_state.mjs` now finishes finite animations, pauses endless ones at `--loop-ms`, pauses and seeks media to `--media-s`, freezes step-triggered animations at `--freeze-ms`, and optionally pauses a fake clock (`--clock`, `--run-ms`).

Repeat-capture results, two runs per row, Playwright 1.64.1 / Chromium 156.0.8078.4, live sites:

| Target and flags | Differing pixels |
| --- | --- |
| beandiner, 1440×900, top | 0 |
| beandiner, 390×844, top | 0 |
| beandiner, 1440×900, `--scroll-y 1800` | 0 |
| beandiner, 1440×900, `--clock … --run-ms 500` | 0 |
| beandiner, 1440×900, `--clock … --run-ms 500 --scroll-y 1800` | 0 (first build: 1,022,876 and `scrollY` 0, because the site reset scroll during `--run-ms`; scroll now applies after it) |
| beandiner, 390×844, steps open "Open navigation" | 0 |
| do-smoothie, 1440×900, initial (coupon dialog) | 0 |
| do-smoothie, 1440×900, steps Escape + "次のフレーバーへ", settled | 0 |
| do-smoothie, same steps, `--freeze-ms 300` | 0 |

Local fixture (300 ms linear drawer, endless spinner, fill-forwards load reveal, `requestAnimationFrame` progress bar): `--freeze-ms 150` put the drawer edge at x=195 of 390 without rewinding the finished reveal; settled put it at x=0. Without `--clock` the scripted bar moved between runs (20 pixels). With `--clock` and `--run-ms 500`, fake `Date` was exact, but the fake `performance.now` origin varied by 0–1 ms (scripted 184–186 ms in a 150 ms + 34 ms run), shifting the bar's antialiased edge: up to 153 pixels differed with max channel delta about 20, and 1 of 3 reruns still differed by 20 pixels at `--channel-tolerance 24`. Pausing the clock at "now" instead of a future instant added drift and was replaced.

## Live bounded trial: beandiner header and hero (2026-10-16)

One fresh default omp `task` subagent (model not observable by the controller) used the skill as written, with no access to evals. Scope: https://beandiner.vercel.app/ header and hero at scroll 0, VP_DESKTOP 1440×900 and VP_MOBILE 390×844, plus the mobile "Open navigation" state. The destination was plain static HTML/CSS/JS under `/tmp/swiper-trial/replica/`. The controller's asset policy forbade copying the site's images, logo, video, illustrations, self-hosted fonts, or source files; placeholders were used, and every pair was compared with `video, img, picture, svg image` hidden on both sides through a shared `--steps` module. The agent ran 32 minutes, with three or fewer repair iterations, and reported `DONE_WITH_CONCERNS`.

The controller re-ran every scored pair independently with the repository's `capture_state.mjs` and `compare_captures.py --max-fraction 0.002`, and got the agent's numbers exactly:

| Pair | Differing pixels | mismatchFraction | Where |
| --- | --- | --- | --- |
| Desktop, settled | 217 | 0.000167 | Logo placeholder ring, Facebook icon placeholder, scroll-cue arrow |
| Mobile, settled | 5 | 0.000015 | Scroll-cue arrow |
| Mobile, menu open, settled | 0 | 0 | — |
| Mobile, menu open, `--freeze-ms 150` | 2 | 0.000006 | Scroll-cue arrow |
| Desktop, `--freeze-from load --freeze-ms 150` (controller, after the fix below) | 23 | 0.000018 | Logo badge edge; source repeat variance there was 18 |

The agent also reported keyboard parity for the menu dialog (Enter open, Tab/Shift+Tab trap, Escape, Close, and backdrop all restore focus to "Open navigation") and element boxes within 0.05 px of the source. A check of the replica against the saved source HTML found 6 of 183 60-character CSS windows and 4 of 126 HTML windows verbatim (short declarations and UI labels), and none in its JavaScript. The replica totalled 9 KB HTML, 13 KB CSS and 1.4 KB JS.

These numbers exclude the hidden media and cover only this batch. Open minor discrepancies: dialog interruption/reversal untested, reduced motion compared only on mobile settled, hover/focus beyond the menu button not compared. One run first captured another project's server on port 8765; the skill's URL confirmation caught it and the captures were quarantined.

Skill problems the trial exposed, and the fixes:

- Load-time animations could be sampled only through a reload workaround. Fixed: `--freeze-from load`. On the source it froze 32 load animations at 150 ms; repeat variance was 18 pixels, and the frame differed from settled by 3.65%.
- `waitUntil: networkidle` was hard-coded and timed out on the source under `--reduced-motion reduce`, because the 4K video kept streaming. Fixed: `--wait-until`. The timeout now fails with a hint, and `--wait-until load` captured the same state.
- The fresh-profile rule read as forbidding Jev. Fixed: it governs only browsers the agent launches.
- A shorter partial-page replica made the sticky-header shadow rasterize differently (about 2% on mobile) until a spacer matched the source's scroll height. Added as implementation step 5.
- Not changed: the agent found the evidence bookkeeping heavy for one batch, with no automation for capture registration.

## Coverage

| Scenario | Actual coverage |
| --- | --- |
| E01 | Stock variant tabletop decisions only; no whole-shop crawl |
| E02 | Defined, not separately executed |
| E03 | Initial artifact evaluation failed edge consistency; helper tests and independent fresh synthetic application passed; E03b not executed |
| E04 | Tabletop missing-motion decisions; local-fixture frozen-frame smoke (exact t150); live repeat captures of CSS/video motion at 0 differing pixels; no live SRC/REP motion comparison |
| E05 | Baseline fail, green tabletop pass (2026-10-05); revised-skill regression 3/3 pass (2026-10-16); no live batch-gate execution |
| E06 | Tabletop recovery and blocked smoke; changed-schema/text/destination workflow unexecuted |
| E07 | Defined, not executed |
| E08 | Defined, not executed |
| E09 | Specification review only; no actual capture comparison |
| E10 | Baseline 0/5 reachable profiles, green 5/5; local-fixture capture/compare smoke; no live target |
| Live trial | beandiner header/hero/mobile menu, media hidden: `DONE_WITH_CONCERNS`, all scored pairs ≤0.000167 mismatch, independently reproduced; whole site, media fidelity and other states untested |

Beyond the bounded trial above, live follow-up requires whole-site route/state discovery, media and canvas fidelity under the asset policy, interruption/reversal and hover/focus checks, and final cross-batch verification. No whole-site live success is claimed.
