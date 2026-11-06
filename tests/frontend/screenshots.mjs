// Renders the panel preview in headless Chromium and writes screenshots.
// Usage: node tests/frontend/screenshots.mjs [outDir]
// Not part of CI: it needs Playwright with a Chromium browser.
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
const shots = [
  { name: "desktop", viewport: { width: 1280, height: 900 }, scale: 1, narrow: false },
  { name: "mobile", viewport: { width: 390, height: 844 }, scale: 2, narrow: true },
];
const tabs = [["overview", 0], ["costs", 1], ["contracts", 2]];
const errors = [];

for (const shot of shots) {
  for (const [tab, index] of tabs) {
    const context = await browser.newContext({ viewport: shot.viewport, deviceScaleFactor: shot.scale });
    const page = await context.newPage();
    page.on("pageerror", (e) => errors.push(`${shot.name}/${tab}: ${e.message}`));
    page.on("console", (m) => { if (m.type() === "error") errors.push(`${shot.name}/${tab}: ${m.text()}`); });
    await page.clock.setFixedTime("2026-07-12T12:00:00Z");
    await page.goto(`${base}?lang=de${shot.narrow ? "&narrow=1" : ""}`);
    await page.waitForFunction(() => window.__panel && window.__panel.shadowRoot.querySelector(".tabs"));
    await page.waitForFunction((narrow) => window.__panel._compact === narrow, shot.narrow);
    await page.evaluate((i) => window.__panel.shadowRoot.querySelectorAll(".tab")[i].click(), index);
    if (tab === "contracts") {
      await page.evaluate(() => window.__panel.shadowRoot.querySelectorAll("details").forEach((d, i) => { if (i < 2) d.open = true; }));
    }
    await page.screenshot({ path: join(outDir, `${shot.name}-${tab}.png`), fullPage: true });
    if (shot.narrow && tab === "overview") {
      await page.evaluate(() => window.__panel.shadowRoot.querySelectorAll("details.card").forEach((d, i) => { if ([0, 3, 4].includes(i)) d.open = true; }));
      await page.screenshot({ path: join(outDir, `${shot.name}-${tab}-open.png`), fullPage: true });
    }
    await context.close();
  }
}

// states and English
for (const [name, query] of [["state-empty", "state=empty"], ["state-error", "state=error"], ["english-overview", "lang=en"]]) {
  const context = await browser.newContext({ viewport: { width: 1280, height: 700 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  page.on("pageerror", (e) => errors.push(`${name}: ${e.message}`));
  await page.clock.setFixedTime("2026-07-12T12:00:00Z");
  await page.goto(`${base}?${query}`);
  await page.waitForFunction(() => window.__panel && window.__panel.shadowRoot.querySelector(".brand"));
  await page.screenshot({ path: join(outDir, `${name}.png`), fullPage: false });
  await context.close();
}

// ---- interactions: the action buttons (administrators only) ----
const check = (ok, message) => { if (!ok) errors.push(`check failed: ${message}`); };
const calls = (page) => page.evaluate(() => window.__calls);
const card = (page, name) => page.locator(".card", { hasText: name }).first();

{
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  page.on("pageerror", (e) => errors.push(`actions: ${e.message}`));
  await page.clock.setFixedTime("2026-07-12T12:00:00Z");
  await page.goto(`${base}?lang=de`);
  await page.waitForFunction(() => window.__panel && window.__panel.shadowRoot.querySelector(".card"));

  check((await page.locator(".actions").count()) === 3, "three contracts offer actions (warning, cancellation, switch)");
  check((await card(page, "Strom Haus").getByRole("button", { name: "Warnung bestätigen" }).count()) === 1, "warning button on Strom Haus");
  check((await card(page, "Internet").getByRole("button", { name: "Kündigung bestätigen" }).count()) === 1, "cancellation button on Internet");
  check((await card(page, "Mobilfunk").getByRole("button", { name: "Jetzt wechseln" }).count()) === 1, "switch button on Mobilfunk");
  check((await card(page, "Gas Heizung").locator(".btn").count()) === 0, "no buttons where nothing is possible");

  // a negative recommended instalment is shown as 0 with a hint, never as a negative amount
  const gasText = await card(page, "Gas Heizung").innerText();
  check(gasText.includes("Empfohlener Abschlag: 0,00") && gasText.includes("Guthaben deckt die Kosten"),
    "gas card shows 0,00 and the hint instead of a negative recommendation");
  check(!/Empfohlener Abschlag: [−-]/.test(gasText), "no negative recommended instalment on the gas card");
  check((await card(page, "Strom Haus").innerText()).includes("Empfohlener Abschlag: 127,66"),
    "a positive recommendation is shown unchanged");
  await page.getByRole("tab", { name: "Kosten" }).click();
  const gasRow = page.locator("tr", { hasText: "Gas Heizung" }).first();
  check((await gasRow.innerText()).includes("Guthaben deckt die Kosten") && !(await gasRow.innerText()).includes("−179"),
    "cost table: hint instead of the negative amount");
  check((await page.locator("tr", { hasText: "Strom Haus" }).first().innerText()).includes("127,66"), "cost table: positive recommendation unchanged");
  await page.getByRole("tab", { name: "Verträge" }).click();
  await page.locator("details", { hasText: "Gas Heizung" }).locator("summary").click();
  const gasDetails = (await page.locator("details", { hasText: "Gas Heizung" }).innerText()).replace(/\u00a0/g, " ");
  check(gasDetails.includes("0,00 € / Monat · Guthaben deckt die Kosten"),
    "contract details: adjustment shown as 0 with the hint");
  await page.getByRole("tab", { name: "Übersicht" }).click();

  // switching asks first and does nothing until confirmed
  await card(page, "Mobilfunk").getByRole("button", { name: "Jetzt wechseln" }).click();
  check((await calls(page)).length === 0, "no call before the switch is confirmed");
  check((await card(page, "Mobilfunk").locator(".ask").count()) === 1, "confirmation question is shown");
  await card(page, "Mobilfunk").screenshot({ path: join(outDir, "actions-confirm.png") });
  await card(page, "Mobilfunk").getByRole("button", { name: "Abbrechen" }).click();
  check((await calls(page)).length === 0, "cancel does nothing");
  check((await card(page, "Mobilfunk").locator(".ask").count()) === 0, "question is gone after cancel");
  await card(page, "Mobilfunk").getByRole("button", { name: "Jetzt wechseln" }).click();
  await card(page, "Mobilfunk").getByRole("button", { name: "Ja, wechseln" }).click();
  check(JSON.stringify(await calls(page)) === JSON.stringify([{ type: "tariffy/action", entry_id: "contract-6", action: "switch_now" }]),
    "confirmed switch sends exactly one switch_now for contract-6");

  // acknowledgements ask first as well, and cancel does nothing
  const before = (await calls(page)).length;
  await card(page, "Internet").getByRole("button", { name: "Kündigung bestätigen" }).click();
  check((await card(page, "Internet").locator(".ask").count()) === 1, "cancellation acknowledgement asks first");
  check((await calls(page)).length === before, "no call before the acknowledgement is confirmed");
  await card(page, "Internet").getByRole("button", { name: "Abbrechen" }).click();
  check((await calls(page)).length === before, "cancelling the acknowledgement does nothing");
  await card(page, "Internet").getByRole("button", { name: "Kündigung bestätigen" }).click();
  await card(page, "Internet").getByRole("button", { name: "Ja, bestätigen" }).click();
  await card(page, "Strom Haus").getByRole("button", { name: "Warnung bestätigen" }).click();
  check((await calls(page)).length === before + 1, "warning acknowledgement also waits for confirmation");
  await card(page, "Strom Haus").getByRole("button", { name: "Ja, bestätigen" }).click();
  const sent = (await calls(page)).slice(1).map((c) => `${c.entry_id}:${c.action}`);
  check(sent.join(",") === "contract-5:confirm_cancellation,contract-1:confirm_abschlag_warning", `acknowledgements sent: ${sent}`);
  await context.close();
}

{ // a failing action shows its error and re-enables the button
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  await page.clock.setFixedTime("2026-07-12T12:00:00Z");
  await page.goto(`${base}?lang=de&fail=1`);
  await page.waitForFunction(() => window.__panel && window.__panel.shadowRoot.querySelector(".card"));
  await card(page, "Strom Haus").getByRole("button", { name: "Warnung bestätigen" }).click();
  await card(page, "Strom Haus").getByRole("button", { name: "Ja, bestätigen" }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".err"));
  check((await card(page, "Strom Haus").locator(".err").innerText()).includes("fehlgeschlagen"), "error text is shown");
  check(await card(page, "Strom Haus").getByRole("button", { name: "Warnung bestätigen" }).isEnabled(), "button is usable again after an error");
  await card(page, "Strom Haus").screenshot({ path: join(outDir, "actions-error.png") });
  await context.close();
}

{ // no buttons at all for non-administrators
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  await page.clock.setFixedTime("2026-07-12T12:00:00Z");
  await page.goto(`${base}?lang=de&admin=0`);
  await page.waitForFunction(() => window.__panel && window.__panel.shadowRoot.querySelector(".card"));
  check((await page.locator(".actions").count()) === 0 && (await page.locator(".btn").count()) === 0, "non-administrators see no action buttons");
  check((await page.locator(".card").count()) === 6, "non-administrators still see all contracts");
  await context.close();
}

{ // phone: buttons are inside the expanded card
  const context = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  const page = await context.newPage();
  await page.clock.setFixedTime("2026-07-12T12:00:00Z");
  await page.goto(`${base}?lang=de&narrow=1`);
  await page.waitForFunction(() => window.__panel && window.__panel._compact === true);
  check((await page.locator(".btn").count()) === 3, "phone: all three buttons are in the page");
  check(!(await page.locator(".btn").first().isVisible()), "phone: buttons stay hidden until the row is expanded");
  await page.locator("details.card", { hasText: "Internet" }).locator("summary").click();
  check(await page.locator("details.card", { hasText: "Internet" }).getByRole("button", { name: "Kündigung bestätigen" }).isVisible(), "phone: button visible after expanding");
  await context.close();
}

await browser.close();
server.close();
if (errors.length) { console.error("Browser errors:\n" + errors.join("\n")); process.exit(1); }
console.log("screenshots written to", outDir);
