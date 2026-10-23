#!/usr/bin/env node
// Deterministic capture of one registered state in an isolated, fresh-profile Playwright browser.
// Run the identical command for SRC and REP; it prints capture-record metadata as JSON.
//
//   node capture_state.mjs --url <url> --out <file.png> --viewport <W>x<H> [options]
//
//   --steps <file.mjs>     module whose default export `async (page) => {}` performs the entry steps
//   --freeze-ms <N>        trigger-relative frame: animations started by the steps pause at N ms
//   --freeze-from <steps|load>  start the --freeze-ms trigger at the steps (default) or at page load
//   --loop-ms <N>          phase for endless animations (default 0)
//   --media-s <N>          time every <video>/<audio> is paused at (default 0)
//   --clock <ISO>          fake Date/timers/requestAnimationFrame, paused at ISO time before load
//   --run-ms <N>           with --clock: advance scripted time by exactly N ms after the steps
//   --scroll-y <N>         scroll position applied after the steps
//   --dpr <N> --locale <tag> --color-scheme <light|dark> --reduced-motion <reduce|no-preference>
//   --wait-until <networkidle|load|domcontentloaded>  navigation readiness (default networkidle;
//                          use load when streaming media keeps the network busy)
//   --wait-ms <N>          real-time wait after load for lazy content (default 0)
//   --full-page
//
// Playwright must resolve from the working directory (`npm i -D playwright`).
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { parseArgs } from 'node:util';

const { values: o } = parseArgs({ options: Object.fromEntries([
  ...['url', 'out', 'viewport', 'steps', 'freeze-ms', 'freeze-from', 'loop-ms', 'media-s', 'clock', 'run-ms',
    'scroll-y', 'dpr', 'locale', 'color-scheme', 'reduced-motion', 'wait-until', 'wait-ms']
    .map((k) => [k, { type: 'string' }]),
  ['full-page', { type: 'boolean' }]]) });
const fail = (message) => { console.error(`ERROR: ${message}`); process.exit(2); };
const num = (key, fallback = null) => {
  if (o[key] === undefined) return fallback;
  const value = Number(o[key]);
  return Number.isFinite(value) ? value : fail(`--${key} must be a number`);
};
if (!o.url || !o.out || !/^\d+x\d+$/.test(o.viewport ?? '')) fail('need --url, --out and --viewport WxH');
if (o['run-ms'] !== undefined && !o.clock) fail('--run-ms requires --clock');
const freezeFrom = o['freeze-from'] ?? 'steps', waitUntil = o['wait-until'] ?? 'networkidle';
if (!['steps', 'load'].includes(freezeFrom)) fail('--freeze-from must be steps or load');
if (freezeFrom === 'load' && o['freeze-ms'] === undefined) fail('--freeze-from load requires --freeze-ms');
if (!['networkidle', 'load', 'domcontentloaded'].includes(waitUntil)) fail('--wait-until must be networkidle, load or domcontentloaded');
const [width, height] = o.viewport.split('x').map(Number);
const freezeAt = num('freeze-ms'), loopAt = num('loop-ms', 0), mediaAt = num('media-s', 0);
const runMs = num('run-ms', 0), scrollY = num('scroll-y'), waitMs = num('wait-ms', 0);
let chromium;
try { ({ chromium } = createRequire(join(process.cwd(), 'noop.js'))('playwright')); } catch {
  fail(`playwright does not resolve from ${process.cwd()}; run where it is installed (npm i -D playwright)`);
}

const browser = await chromium.launch(); // fresh profile: never the user's cookies or logins
const context = await browser.newContext({
  viewport: { width, height }, deviceScaleFactor: num('dpr', 1), locale: o.locale ?? 'en-US',
  colorScheme: o['color-scheme'] ?? 'light', reducedMotion: o['reduced-motion'] ?? 'no-preference',
});
await context.addInitScript((loadFreezeAt) => { // catch animations the moment the trigger creates them
  window.__swiperTriggered = new Set();
  window.__swiperFreezeAt = loadFreezeAt; // set from document start only with --freeze-from load
  window.__swiperSetTimeout = setTimeout; // runs before the fake clock's init script
  const grab = (e) => {
    if (window.__swiperFreezeAt == null) return;
    for (const a of e.target.getAnimations()) {
      window.__swiperTriggered.add(a); a.pause(); a.currentTime = window.__swiperFreezeAt;
    }
  };
  addEventListener('transitionrun', grab, true);
  addEventListener('animationstart', grab, true);
}, freezeFrom === 'load' ? freezeAt : null);
const page = await context.newPage();
const clockStart = o.clock ? new Date(o.clock) : null;
if (clockStart) {
  if (Number.isNaN(clockStart.getTime())) fail('--clock must be an ISO date');
  // Install 1 s early, then pause exactly at the start: pausing at "now" drifts by real install latency.
  await page.clock.install({ time: new Date(clockStart.getTime() - 1000) });
  await page.clock.pauseAt(clockStart);
}
const PAINT_MS = 34; // with --clock: one fixed scripted step so paused painters draw the seeked media frame
const settle = () => (clockStart ? page.waitForTimeout(50)
  : page.evaluate(() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)))));

try {
  await page.goto(o.url, { waitUntil });
} catch (error) {
  fail(`navigation (${waitUntil}) failed: ${error.message.split('\n')[0]}`
    + (waitUntil === 'networkidle' ? '; retry with --wait-until load if media keeps streaming' : ''));
}
await page.evaluate(() => document.fonts.ready);
if (waitMs) await page.waitForTimeout(waitMs);
await page.evaluate(({ t, fromLoad }) => {
  window.__swiperBefore = new Set(fromLoad ? [] : document.getAnimations());
  window.__swiperFreezeAt = t;
}, { t: freezeAt, fromLoad: freezeFrom === 'load' });
if (o.steps) await (await import(pathToFileURL(resolve(o.steps)).href)).default(page);
if (runMs) await page.clock.runFor(runMs);
// After --run-ms so load-time scroll resets cannot undo it; scroll inside --steps when timed motion must follow it.
if (scrollY !== null) await page.evaluate((y) => window.scrollTo({ top: y, behavior: 'instant' }), scrollY);

const media = await page.evaluate(async (at) => Promise.all([...document.querySelectorAll('video, audio')]
  .map(async (m) => {
    m.pause();
    if (m.readyState > 0 && Math.abs(m.currentTime - at) > 1e-3) {
      await new Promise((r) => {
        m.addEventListener('seeked', r, { once: true }); m.currentTime = at;
        window.__swiperSetTimeout(r, 5000); // real timer: page timers are paused under --clock
      });
    }
    return { t: m.currentTime, readyState: m.readyState };
  })), mediaAt);
const frozen = { triggered: 0, finished: 0, loops: 0 };
for (let pass = 0; pass < 5; pass += 1) { // finishing can start chained animations; repeat until stable
  const counts = await page.evaluate(({ t, loop }) => {
    const c = { triggered: 0, finished: 0, loops: 0, running: 0 };
    for (const a of document.getAnimations()) {
      const endless = a.effect?.getComputedTiming().endTime === Infinity;
      if (t != null && (window.__swiperTriggered.has(a) || !window.__swiperBefore.has(a))) {
        a.pause(); a.currentTime = t; c.triggered += 1;
      } else if (endless) {
        a.pause(); a.currentTime = loop; c.loops += 1;
      } else if (a.playState !== 'finished') {
        try { a.finish(); c.finished += 1; c.running += 1; } catch { a.pause(); }
      }
    }
    return c;
  }, { t: freezeAt, loop: loopAt });
  frozen.triggered = counts.triggered; frozen.loops = counts.loops; frozen.finished += counts.finished;
  await settle();
  if (!counts.running) break;
}
if (clockStart) await page.clock.runFor(PAINT_MS);
const measured = await page.evaluate(() => ({ url: location.href, width: innerWidth, height: innerHeight,
  scrollX, scrollY, deviceScaleFactor: devicePixelRatio, observedAt: new Date().toISOString(),
  scriptedMs: performance.now() }));
await page.screenshot({ path: o.out, fullPage: Boolean(o['full-page']) });
console.log(JSON.stringify({
  out: o.out, sha256: createHash('sha256').update(readFileSync(o.out)).digest('hex'),
  tool: `playwright chromium ${browser.version()}`, ...measured,
  observedAt: clockStart ? new Date().toISOString() : measured.observedAt,
  elapsedMs: freezeAt, freezeFrom: freezeAt === null ? null : freezeFrom, waitUntil,
  loopAtMs: loopAt, mediaAtS: mediaAt, media,
  clock: clockStart ? { start: clockStart.toISOString(), runMs, paintMs: PAINT_MS, scriptedMs: measured.scriptedMs } : null,
  frozen, steps: o.steps ?? null,
}));
await browser.close();
