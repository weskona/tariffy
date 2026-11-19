// Renders the main panel screenshots in the light design (files named *-light.png next to the dark ones).
// Usage: node tests/frontend/screenshots-light.mjs [outDir]
// Not part of CI: it needs Playwright with a Chromium browser. The dark set comes from screenshots.mjs.
import { createServer } from "node:http";
import { readFile, mkdir } from "node:fs/promises";
import { extname, join, normalize, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const root = resolve(fileURLToPath(new URL("../..", import.meta.url)));
const outDir = resolve(process.argv[2] || join(root, "docs", "panel-preview"));
const TYPES = { ".html": "text/html", ".js": "text/javascript", ".json": "application/json" };

const server = createServer(async (req, res) => {
  const path = normalize(join(root, decodeURIComponent(new URL(req.url, "http://x").pathname)));
  if (!path.startsWith(root)) { res.writeHead(403).end(); return; }
  try {
    res.writeHead(200, { "content-type": TYPES[extname(path)] || "application/octet-stream" });
    res.end(await readFile(path));
  } catch { res.writeHead(404).end(); }
});
await new Promise((ok) => server.listen(0, "127.0.0.1", ok));
const base = `http://127.0.0.1:${server.address().port}/tests/frontend/preview.html`;

await mkdir(outDir, { recursive: true });
const browser = await chromium.launch();
const tabs = [["overview", 0], ["costs", 1], ["contracts", 2], ["history", 3], ["backup", 4]];
const errors = [];
// the same sets as screenshots.mjs: German desktop and phone, English at 960 px (for the README)
const sets = [
  { prefix: "desktop", lang: "de", viewport: { width: 1280, height: 900 }, scale: 1, narrow: false },
  { prefix: "mobile", lang: "de", viewport: { width: 390, height: 844 }, scale: 2, narrow: true },
  { prefix: "english", lang: "en", viewport: { width: 960, height: 900 }, scale: 1, narrow: false },
];

for (const set of sets) {
  for (const [tab, index] of tabs) {
    const context = await browser.newContext({ viewport: set.viewport, deviceScaleFactor: set.scale, colorScheme: "light" });
    const page = await context.newPage();
    page.on("pageerror", (e) => errors.push(`${set.prefix}/${tab}: ${e.message}`));
    page.on("console", (m) => { if (m.type() === "error") errors.push(`${set.prefix}/${tab}: ${m.text()}`); });
    await page.clock.setFixedTime("2026-07-12T12:00:00Z");
    await page.goto(`${base}?lang=${set.lang}&theme=light${set.narrow ? "&narrow=1" : ""}`);
    await page.waitForFunction(() => window.__panel && window.__panel.shadowRoot.querySelector(".tabs"));
    if (set.narrow) await page.waitForFunction(() => window.__panel._compact === true);
    await page.evaluate((i) => window.__panel.shadowRoot.querySelectorAll(".tab")[i].click(), index);
    if (tab === "contracts") {
      await page.evaluate(() => window.__panel.shadowRoot.querySelectorAll("details").forEach((d, i) => { if (i < 2) d.open = true; }));
    }
    await page.waitForTimeout(300);
    const isLight = await page.evaluate(() => window.__panel.classList.contains("light"));
    if (!isLight) errors.push(`${set.prefix}/${tab}: the panel is not in the light design`);
    await page.screenshot({ path: join(outDir, `${set.prefix}-${tab}-light.png`), fullPage: true });
    await context.close();
  }
}
await browser.close();
server.close();
if (errors.length) { console.error("Browser errors:\n" + errors.join("\n")); process.exit(1); }
console.log("light screenshots written to", outDir);
