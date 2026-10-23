# Browser capabilities and inspection

Use Jev first for semantic navigation, interaction, and assertions. At every new session, discover actual tool names, schemas, operation descriptions, and assertion checks through tool metadata (`ALL_TOOLS`, tool search, or the harness's tool docs). Record discovery date/version and exact supported schemas in `.replica-evidence/capabilities.md`; remembered examples are not discovery. Run the discovered `browser_doctor` when availability or policy is uncertain. Never enable a tool's disabled policy (for example Jev's `JEVMCP_ALLOW_JS`), bypass approvals, or invent unsupported operations.

## Route each capability

Record every needed capability as available, disabled, unsupported, or not checked, with the tool that serves it, its evidence, and its fallback. A capability is blocked only after every route below has failed or been ruled out with a recorded reason. The Jev column describes the last discovered surface, not a permanent API guarantee.

| Capability | Jev surface (rediscover) | Alternative route |
| --- | --- | --- |
| Navigation / interaction | `browser_open`; `browser_act` ops `nav`, `back`, `forward`, `reload`, `tab`, `click`, `hover`, `keys`, `scroll`, `type`, `select`, `toggle` | Isolated browser locators by role, label, or text |
| Assertions | `browser_assert`; identical checks in goal `verify` | Isolated browser checks of URL, role/name, text, value |
| Exact viewport / device scale | None exposed | Isolated browser context `viewport` and `deviceScaleFactor`; Playwright CLI `--viewport-size=W,H` |
| Screenshots | `screenshot` op: `path`, `full` (default false), `format` (default jpeg; request png) | Isolated browser PNG screenshot |
| Computed styles, boxes, fonts, keyframes | `eval` only when its policy is already enabled | Isolated browser `page.evaluate` of the read-only snippet below |
| Source HTML/CSS/fonts/assets | None | HTTP fetch of public in-scope URLs; see Static source |
| Network log | None exposed | Isolated browser HAR (Playwright CLI `--save-har=file.har`) or request events |
| Animation timing / intermediate frames | `eval`-only Web Animations API; `wait` is not a frame clock | [capture_state](../scripts/capture_state.mjs) `--freeze-ms` and `--clock`; see Deterministic capture |
| Reduced motion, color scheme, locale | None exposed | Isolated browser context options |
| Accessibility | Element roles/names/states plus observable keyboard behavior; not a full tree or audit | Isolated browser accessibility snapshot, role locators, real keyboard events |

When Jev's text model is unavailable, enter known text with grouped direct `type` actions. Prefer supported autonomous goals for other tasks; if a goal returns `turbo_unavailable`, record it and use direct control.

### Isolated automation browser

An isolated automation browser is one you launch yourself with a fresh profile: Playwright, Puppeteer, or a harness browser tool with CDP access. Prefer one already available (harness tool, installed package, cached browser binaries). Otherwise add Playwright as a destination dev dependency or in a scratch tool directory when user and project rules permit (`npm i -D playwright && npx playwright install chromium`), and record the version in capabilities.md.

- Never attach it to the user's browser profile, cookies, or logins. It is a separate capability, not a way around another tool's disabled policy; login-, paywall-, or approval-gated states stay blocked. This rule governs browsers you launch; use Jev's sessions as the user configured them and never change that configuration.
- Capture both SRC and REP with [capture_state](../scripts/capture_state.mjs) using identical flags, and record its output in the run environment. Pairs from different tools or settings are not comparable.

## Static source

Fetch the in-scope page HTML, every linked stylesheet (following `@import`), and referenced fonts and assets over HTTP, without credentials and without bypassing bot protection. Runtime-injected CSS (CSS-in-JS, framework style tags) exists only after scripts run: read it from `document.styleSheets` in the isolated browser. Save unmodified copies under `.replica-evidence/static/`, recording source URL, fetch time, HTTP status, and SHA-256 as provenance.

From the source, extract custom properties/design tokens, `@font-face` family/weight/style/`src`, `@media` breakpoints, `@keyframes`, `transition`/`animation` declarations, and the typography, color, and spacing rules for classes seen in the rendered DOM.

Record a declared value as `confidence: "estimated"` with `measurementMethod: "declared: <stylesheet URL> <selector>"`. Promote it to `observed` only when computed styles or frozen frames of the rendered element at the registered profile confirm it, and cite both. Motion with no matching CSS or Web Animations entry is script-driven and stays unknown until frames are inspected.

## Current-schema syntax examples

**All examples below are syntax examples, never executed or passed browser checks.** Call each tool through its discovered name (often a namespaced MCP route). Replace URLs and semantic expectations with your scoped fixture. Derive `searchRef`, `sortRef`, and `detailsRef` from the actual current observation; never copy an illustrative `e` ID. Reobserve after navigation, replacement, stale/covered references, or unexpected changes. Preserve semantic actions in evidence, not tool handles.

```js
await browser_open({url: "https://example.invalid/products", session: "swiper", hint: "Inspect product listing"});
await browser_observe({session: "swiper", mode: "full", include_text: true, include_json: true});
// Bind these variables ONLY from the observation of the actual page.
await browser_act({
  session: "swiper", observe_after: true, stop_on_error: true,
  // Edit controls only; this example does not submit a search.
  ops: [{op: "type", ref: searchRef, text: "linen", clear: true, submit: false},
        {op: "select", ref: sortRef, value: "Price: low to high"}]
});
await browser_assert({session: "swiper", checks: [{type: "value_equals", ref: searchRef, value: "linen"}]});
```

Supported op names are `click`, `type`, `select`, `toggle`, `hover`, `upload`, `keys`, `scroll`, `nav`, `back`, `forward`, `reload`, `wait`, `wait_for_ref`, `wait_for_text`, `wait_for_load`, `screenshot`, `tab`, and conditional `eval`. Check fresh descriptions for fields/defaults before using them. Uploads and consequential actions must remain within authorization; honor `needs_confirmation` rather than automatically adding `confirm:true`.

```js
// Non-destructive autonomous task with deterministic final-page verification.
// Derive this destination URL and unique heading from prior source-fixture inspection.
await browser_goal({
  session: "swiper", url: "https://example.invalid/products", max_steps: 8,
  goal: "Open the first product's details without buying, submitting, or changing account data.",
  verify: [{type: "url_matches", pattern: "https://example.invalid/products/42"},
           {type: "element_exists", role: "heading", name: "Linen shirt — product 42"}]
});
// DONE is a claim: require returned successful verify results, or assert explicitly.
await browser_assert({session: "swiper", checks: [
  {type: "url_matches", pattern: "https://example.invalid/products/42"},
  {type: "element_exists", role: "heading", name: "Linen shirt — product 42"},
  {type: "text_absent", text: "Page not found"}
]});
await browser_observe({session: "swiper", mode: "full"});
// Rebind detailsRef from this destination observation; never reuse the listing's ref.
await browser_act({session: "swiper", ops: [
  {op: "hover", ref: detailsRef}, {op: "scroll", dir: "down", amount: 400},
  {op: "screenshot", path: "SRC-R001-S001-V-VP_DESKTOP-after-01.png", full: false, format: "png"}
]});
```

Other discovered checks: `url_matches {pattern}`, `url_contains {text}`, `title_matches {pattern}`, `text_contains {text}`, `element_gone {ref}`, `checked {ref,state}`, `count_at_least {role,min}`, and conditional `js {expr}`. Verify check availability and evaluation policy first. Screenshot `path` names a file in Jev's shots directory, not automatically `.replica-evidence/`. Locate the actual artifact from the returned result, confirm its format, and copy it to the registered source/replica evidence path without overwriting prior captures; preserve the original and register provenance according to [evidence-contract](evidence-contract.md). Do not label default JPEG bytes `.png`; request `format:"png"` as above. Jev cannot set the viewport, so its screenshots count as a registered profile only when their measured dimensions match it. Record exact viewport, scroll, fixture, state, phase, elapsed time, URL, and observation time; no passed result follows from a file name or action success alone.

## Deterministic capture

Capture every registered SRC and REP state with the bundled [capture_state](../scripts/capture_state.mjs), using identical flags for both sides. Run it from a directory where `playwright` resolves. It launches a fresh-profile Chromium at the exact viewport, runs the state's entry steps, makes the frame reproducible, saves the PNG, and prints capture-record metadata: measured viewport, scroll, device scale, SHA-256, tool version, frozen-animation counts, media times, and clock.

```sh
node "<skill-directory>/scripts/capture_state.mjs" --url "<origin>/products/42" --viewport 390x844 \
  --steps steps/open-cart.mjs --freeze-ms 150 --out "<screenshots/source/SRC-R003-S002-V-VP_MOBILE-t150-01.png>"
```

```js
// steps/open-cart.mjs: entry steps for the registered state, by role, label, or text.
export default async (page) => { await page.getByRole('button', { name: 'Open cart' }).click(); };
```

| Motion source | Default handling | Flag |
| --- | --- | --- |
| CSS transitions/animations and Web Animations started by the steps | Finished: settled endpoint | `--freeze-ms N` pauses them N ms after the trigger |
| Finite animations already running (load reveals) | Finished | `--freeze-from load --freeze-ms N` pauses animations started during load at N ms after document start |
| Endless animations (spinners, floats, pulses) | Paused at a fixed phase | `--loop-ms N` (default 0) |
| `<video>` / `<audio>` | Paused and seeked to a fixed time | `--media-s N` (default 0) |
| Scripted timers, `requestAnimationFrame`, `Date` | Run in real time: not reproducible | `--clock <ISO>` pauses a fake clock before load; `--run-ms N` advances it exactly N ms after the steps, plus a fixed 34 ms paint step |
| Scroll position | Top | `--scroll-y N`, applied after `--run-ms`; scroll inside `--steps` when timed motion must follow the scroll |

Limits to record when they apply: the fake `performance.now` origin can drift 1–2 ms between runs, so script-driven elements may shift by a sub-pixel edge; canvas or WebGL painters that ignore seeked media stay nondeterministic and need a reasoned mask or a blocked check; `preload="none"` media shows its poster (`readyState` 0 in the output); smooth-scroll libraries can override `--scroll-y`, so check the reported `scrollY`; the default `--wait-until networkidle` never settles while media keeps streaming, so use `--wait-until load` on both sides when navigation times out. Prove determinism on each target by capturing the source twice and comparing (verification step 4). `npx playwright screenshot --viewport-size=W,H` freezes nothing; use it only for states with no motion or media.

## DevTools-equivalent evidence

Inspect layout boxes, spacing, breakpoints, colors, borders, shadows, typography, image sizing/cropping, and pseudo-elements. Capture semantic DOM/ARIA and focus behavior where supported. Record actual asset/font URLs and availability, not guessed filenames. Observe states before and after the trigger; inspect animation keyframes, duration, delay, easing, iterations, sequence, interruption, scroll coupling, and reduced-motion behavior. Active animation snapshots alone do not establish every behavior or completed animation.

The following read-only evaluation is **syntax only**. Run it with `page.evaluate` in the isolated browser, or with Jev `eval` only when doctor/policy already reports evaluation enabled, after a fresh inspection establishes the selector. It samples computed styles, pseudo-elements, assets/fonts, animation keyframes/timing, and partial resource timing.

```js
(() => {
  const el = document.querySelector('[data-inspected-target]'); // replace observed selector
  if (!el) return {error: 'Target absent; reobserve'};
  const props = ['display','position','gap','padding','margin','color','backgroundImage',
    'border','boxShadow','fontFamily','fontSize','fontWeight','lineHeight','letterSpacing',
    'opacity','transform','transitionDuration','transitionDelay','transitionTimingFunction'];
  const styles = pseudo => { const s = getComputedStyle(el, pseudo);
    return Object.fromEntries(props.map(p => [p, s[p]])); };
  const r = el.getBoundingClientRect();
  return {url: location.href, sampledAt: performance.now(),
    viewport: {width: innerWidth,height: innerHeight,scrollX,scrollY},
    dom: {tag: el.tagName,role: el.getAttribute('role'),label: el.getAttribute('aria-label')},
    box: {x:r.x,y:r.y,width:r.width,height:r.height}, styles: styles(null),
    before: styles('::before'), after: styles('::after'),
    images: [...el.querySelectorAll('img')].map(i => ({url:i.currentSrc,width:i.naturalWidth,height:i.naturalHeight})),
    fonts: [...document.fonts].map(f => ({family:f.family,weight:f.weight,status:f.status})),
    stylesheets: [...document.styleSheets].map(s => s.href),
    animations: el.getAnimations({subtree:true}).map(a => ({name:a.animationName || null,
      playState:a.playState,currentTime:a.currentTime,timing:a.effect?.getTiming(),
      computedTiming:a.effect?.getComputedTiming(),keyframes:a.effect?.getKeyframes()})),
    resources: performance.getEntriesByType('resource').map(e => ({url:e.name,
      initiator:e.initiatorType,start:e.startTime,duration:e.duration}))};
})()
```

FontFace entries do not expose font source URLs: read `@font-face` rules from fetched stylesheets or the HAR; cross-origin rules may be inaccessible to page scripts. Resource Timing can be buffered, incomplete, or restricted. Do not infer response bodies, headers, font rendering, complete accessibility, or network absence from this output. Store unknowns and limitations explicitly.

## Fallback and recovery

Discovered computer-use or accessibility tools can supply native screenshots and AX state: follow their returned documentation, target only the intended window with fresh element indexes, and never attach to or reconfigure an unrelated browser session.

| Failure | Recovery |
| --- | --- |
| Stale reference | Reobserve; bind fresh references to the intended semantic target. |
| Occluded / out of viewport | Inspect covering element; appropriately dismiss an authorized overlay or scroll target into view, then reobserve. |
| `= no change` | Inspect/assert actual state; change strategy rather than repeat the same reference. |
| Disabled eval / no viewport op | Route the check to the isolated browser; if no route works, record the limitation and keep the measurement unknown. |
| Unsupported schema/check | Rediscover exact metadata; correct arguments without inventing fields. |
| Browser startup/profile conflict | Use doctor and ownership evidence. A live Chrome using the launch profile plus locks suggests conflict; a startup exit code alone does not prove it. Do not kill unrelated Chrome, delete live locks, or change configuration automatically. |
| Every browser route unavailable | Mark verification blocked and stop further implementation batches; independent evidence inspection may continue. Resume the existing batch's verification first. |
| Login/access-required/security/approval state | Record inaccessible state as blocked; use only authorized access and honor required handoff/confirmation. |

Never report successful browser verification from examples, tool discovery, doctor health, or a goal's narrative alone.
