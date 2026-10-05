# Browser capabilities and inspection

Use Jev first. At every new session, discover actual MCP names, schemas, operation descriptions, and assertion checks through tool metadata (`ALL_TOOLS` or tool search). Record discovery date/version and exact supported schemas in `.replica-evidence/capabilities.md`; remembered examples are not discovery. Run the discovered `browser_doctor` when availability or policy is uncertain. Do not enable configuration, bypass approvals, or invent unsupported operations.

## Capability checklist

Record each capability as available, disabled, unsupported, or not checked, with its evidence and fallback. The table describes the metadata discovered while authoring this guide, not a permanent API guarantee.

| Capability | Discovered Jev surface / limitation |
| --- | --- |
| Navigation | `browser_open`; `browser_act` ops `nav`, `back`, `forward`, `reload`, `tab` |
| Screenshots | `screenshot` op: optional `path`, `full` (default false), `format` (default jpeg); inspect returned artifact |
| Viewport | No resize/emulation op exposed; record actual CSS dimensions if inspection permits; named desktop/mobile profiles remain blocked until reproducibly set and measured |
| Hover / keyboard / scrolling | `hover {ref}`; `keys {key}` or `{keys:[]}`; `scroll {dir,amount,ref?}` |
| Known text / selection | `type {ref,text,clear?,submit?}`, `select {ref,value}`, `toggle {ref,state?}` |
| Assertions | `browser_assert`; identical checks supported by goal `verify` |
| Evaluation / DOM | `eval {js}` only when checked enabled (`JEVMCP_ALLOW_JS=1`); observations expose actionable element tables, not complete DOM |
| Computed styles / assets | Conditional page JS can inspect styles, image URLs, fonts, stylesheets; no dedicated style inspector exposed |
| Accessibility | Element roles/names/states plus observable keyboard behavior; not a complete accessibility audit/tree |
| Network | No CDP network interception/HAR surface exposed; conditional Resource Timing is partial, not headers, bodies, or a complete request log |
| Timing / animations | Conditional Web Animations API/computed styles; captures and measured elapsed times otherwise; `wait` is not a precise frame scheduler |

At authoring, doctor reported `js_eval:false`, `text_model:false`, `typesafe_turbo:true`. The TypeSafe key does not supply the text-generation helper required for autonomous `TYPE_TEXT`. Use grouped direct actions for known text. Prefer supported autonomous goals for other browser tasks; if `turbo_unavailable`, record it and use direct control. Recheck capabilities in your session.

## Current-schema syntax examples

**All examples below are syntax examples, never executed or passed browser checks.** Replace URLs and semantic expectations with your scoped fixture. Derive `searchRef`, `sortRef`, and `detailsRef` from the actual current observation; never copy an illustrative `e` ID. Reobserve after navigation, replacement, stale/covered references, or unexpected changes. Preserve semantic actions in evidence, not tool handles.

```js
await tools.mcp__jev_ultrafast_mcp__browser_open({
  url: "https://example.invalid/products", session: "swiper", hint: "Inspect product listing"
});
await tools.mcp__jev_ultrafast_mcp__browser_observe({
  session: "swiper", mode: "full", include_text: true, include_json: true
});
// Bind these variables ONLY from the observation of the actual page.
await tools.mcp__jev_ultrafast_mcp__browser_act({
  session: "swiper", observe_after: true, stop_on_error: true,
  // Edit controls only; this example does not submit a search.
  ops: [{op: "type", ref: searchRef, text: "linen", clear: true, submit: false},
        {op: "select", ref: sortRef, value: "Price: low to high"}]
});
await tools.mcp__jev_ultrafast_mcp__browser_assert({session: "swiper", checks: [
  {type: "value_equals", ref: searchRef, value: "linen"}
]});
```

Supported op names are `click`, `type`, `select`, `toggle`, `hover`, `upload`, `keys`, `scroll`, `nav`, `back`, `forward`, `reload`, `wait`, `wait_for_ref`, `wait_for_text`, `wait_for_load`, `screenshot`, `tab`, and conditional `eval`. Check fresh descriptions for fields/defaults before using them. Uploads and consequential actions must remain within authorization; honor `needs_confirmation` rather than automatically adding `confirm:true`.

```js
// Non-destructive autonomous task with deterministic final-page verification.
// Derive this destination URL and unique heading from prior source-fixture inspection.
await tools.mcp__jev_ultrafast_mcp__browser_goal({
  session: "swiper", url: "https://example.invalid/products", max_steps: 8,
  goal: "Open the first product's details without buying, submitting, or changing account data.",
  verify: [{type: "url_matches", pattern: "https://example.invalid/products/42"},
           {type: "element_exists", role: "heading", name: "Linen shirt — product 42"}]
});
// DONE is a claim: require returned successful verify results, or assert explicitly.
await tools.mcp__jev_ultrafast_mcp__browser_assert({session: "swiper", checks: [
  {type: "url_matches", pattern: "https://example.invalid/products/42"},
  {type: "element_exists", role: "heading", name: "Linen shirt — product 42"},
  {type: "text_absent", text: "Page not found"}
]});
await tools.mcp__jev_ultrafast_mcp__browser_observe({session: "swiper", mode: "full"});
// Rebind detailsRef from this destination observation; never reuse the listing's ref.
await tools.mcp__jev_ultrafast_mcp__browser_act({session: "swiper", ops: [
  {op: "hover", ref: detailsRef}, {op: "scroll", dir: "down", amount: 400},
  {op: "screenshot", path: "SRC-R001-S001-V-VP_DESKTOP-after-01.png", full: false, format: "png"}
]});
```

Other discovered checks: `url_matches {pattern}`, `title_matches {pattern}`, `element_gone {ref}`, `checked {ref,state}`, `count_at_least {role,min}`, and conditional `js {expr}`. Verify check availability and evaluation policy first. Screenshot `path` names a file in Jev's shots directory, not automatically `.replica-evidence/`. Locate the actual artifact from the returned result, confirm its format, and copy it to the registered source/replica evidence path without overwriting prior captures; preserve the original and register provenance according to [evidence-contract](evidence-contract.md). Do not label default JPEG bytes `.png`; request `format:"png"` as above. Record exact viewport, scroll, fixture, state, phase, elapsed time, URL, and observation time; no passed result follows from a file name or action success alone.

## DevTools-equivalent evidence

Inspect layout boxes, spacing, breakpoints, colors, borders, shadows, typography, image sizing/cropping, and pseudo-elements. Capture semantic DOM/ARIA and focus behavior where supported. Record actual asset/font URLs and availability, not guessed filenames. Observe states before and after the trigger; inspect animation keyframes, duration, delay, easing, iterations, sequence, interruption, scroll coupling, and reduced-motion behavior. Active animation snapshots alone do not establish every behavior or completed animation.

The following read-only evaluation is **conditional syntax only**. Use it solely after doctor/policy confirms JS evaluation enabled and a fresh inspection establishes the selector. It samples computed styles, pseudo-elements, assets/fonts, animation keyframes/timing, and partial resource timing without claiming CDP access.

```js
await tools.mcp__jev_ultrafast_mcp__browser_act({session: "swiper", ops: [{op: "eval", js: `
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
})()`}]});
```

FontFace entries do not expose font source URLs: inspect accessible stylesheet/font-face rules or actual network evidence when supported; cross-origin rules may be inaccessible. Resource Timing can be buffered, incomplete, or restricted. Do not infer response bodies, headers, font rendering, complete accessibility, or network absence from this output. Store unknowns and limitations explicitly. If evaluation is disabled, use captures/visible behavior plus a discovered supported alternative; do not enable JS just to run this example.

## Accessible fallback and recovery

`mcp__cua_repl.js` is a discovered alternative. Its first call must be exactly `await cua.getState();` (or another documented entry-point call), then read returned documentation. Native Chrome inspection supports `cua.getApp("Google Chrome")`, `getAXState()`, `getScreenshot()`, and `getAXStateAndScreenshot()`: use the target window only, fresh AX indexes, and read-only visible DevTools inspection where exposed. Browser-specific methods require their own returned documentation; do not assume Playwright/eval/network/viewport APIs. No `agent-browser` CLI was found in this environment, so it is not an installed fallback.

The CUA discovery during authoring returned native apps but browser inventory failed with `failed to start codex app-server: No such file or directory (os error 2)`. This establishes a concrete native AX/screenshot fallback surface, not working browser-tab or DevTools validation. Rediscover availability; record failures honestly. Do not attach to an unrelated browser session or alter its configuration.

| Failure | Recovery |
| --- | --- |
| Stale reference | Reobserve; bind fresh references to the intended semantic target. |
| Occluded / out of viewport | Inspect covering element; appropriately dismiss an authorized overlay or scroll target into view, then reobserve. |
| `= no change` | Inspect/assert actual state; change strategy rather than repeat the same reference. |
| Disabled eval | Record limitation; use discovered capture/AX/visible-inspection fallback, retaining unknown measurements. |
| Unsupported schema/check | Rediscover exact metadata; correct arguments without inventing fields. |
| Browser startup/profile conflict | Use doctor and ownership evidence. A live Chrome using the launch profile plus locks suggests conflict; startup exit 21 alone does not prove it. Do not kill unrelated Chrome, delete live locks, or change configuration automatically. |
| Browser unavailable | Mark verification blocked and stop further implementation batches; independent evidence inspection may continue. Resume the existing batch's verification first. |
| Login/access-required/security/approval state | Record inaccessible state as blocked; use only authorized access and honor required handoff/confirmation. |

Never report successful browser verification from examples, tool discovery, doctor health, or a goal's narrative alone.
