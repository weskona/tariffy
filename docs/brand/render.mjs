// Renders the brand images from the SVG sources (transparent PNGs) into custom_components/tariffy/brand/.
// Usage: node docs/brand/render.mjs   (needs Playwright with Chromium; not part of CI)
import { readFile, writeFile, mkdir } from "node:fs/promises";
import { resolve, join } from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const here = resolve(fileURLToPath(new URL(".", import.meta.url)));
const out = resolve(here, "..", "..", "custom_components", "tariffy", "brand");
await mkdir(out, { recursive: true });

// file in the integration, SVG source, size of the SVG in px, scale for the PNG
const jobs = [
  ["icon.png", "icon.svg", 256, 1],
  ["icon@2x.png", "icon.svg", 256, 2],
  ["logo.png", "logo.svg", [700, 256], 1],
  ["logo@2x.png", "logo.svg", [700, 256], 2],
  ["dark_logo.png", "logo-dark.svg", [700, 256], 1],
  ["dark_logo@2x.png", "logo-dark.svg", [700, 256], 2],
];
const browser = await chromium.launch();
for (const [name, source, size, scale] of jobs) {
  const [w, h] = Array.isArray(size) ? size : [size, size];
  const svg = await readFile(join(here, source), "utf8");
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: scale });
  await page.setContent(`<!doctype html><body style="margin:0;background:transparent">${svg}</body>`);
  await writeFile(join(out, name), await page.screenshot({ omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } }));
  await page.close();
}
await browser.close();
console.log("brand images written to", out);
