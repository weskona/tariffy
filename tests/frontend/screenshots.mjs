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
const tabs = [["overview", 0], ["costs", 1], ["contracts", 2], ["history", 3], ["backup", 4]];
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
    await page.waitForTimeout(300); // let the arrow finish turning
    await page.screenshot({ path: join(outDir, `${shot.name}-${tab}.png`), fullPage: true });
    if (shot.narrow && tab === "overview") {
      await page.evaluate(() => window.__panel.shadowRoot.querySelectorAll("details.card").forEach((d, i) => { if ([0, 3, 4].includes(i)) d.open = true; }));
      await page.waitForTimeout(300);
      await page.screenshot({ path: join(outDir, `${shot.name}-${tab}-open.png`), fullPage: true });
    }
    await context.close();
  }
}

// states and English
for (const [name, query] of [["state-empty", "state=empty"], ["state-error", "state=error"]]) {
  const context = await browser.newContext({ viewport: { width: 1280, height: 700 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  page.on("pageerror", (e) => errors.push(`${name}: ${e.message}`));
  await page.clock.setFixedTime("2026-07-12T12:00:00Z");
  await page.goto(`${base}?${query}`);
  await page.waitForFunction(() => window.__panel && window.__panel.shadowRoot.querySelector(".brand"));
  await page.screenshot({ path: join(outDir, `${name}.png`), fullPage: false });
  await context.close();
}

// English, full page, for the README (960 px wide: two cards per row, so no label breaks inside a word)
for (const [tab, index] of tabs) {
  const context = await browser.newContext({ viewport: { width: 960, height: 900 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  page.on("pageerror", (e) => errors.push(`english/${tab}: ${e.message}`));
  await page.clock.setFixedTime("2026-07-12T12:00:00Z");
  await page.goto(`${base}?lang=en`);
  await page.waitForFunction(() => window.__panel && window.__panel.shadowRoot.querySelector(".tabs"));
  await page.evaluate((i) => window.__panel.shadowRoot.querySelectorAll(".tab")[i].click(), index);
  if (tab === "contracts") {
    await page.evaluate(() => window.__panel.shadowRoot.querySelectorAll("details").forEach((d, i) => { if (i < 2) d.open = true; }));
  }
  await page.waitForTimeout(300);
  await page.screenshot({ path: join(outDir, `english-${tab}.png`), fullPage: true });
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

  const listRow = (name) => page.locator("details:not(.card)", { hasText: name }).first();
  const openRow = async (name) => { if (!(await listRow(name).evaluate((el) => el.open))) await listRow(name).locator("summary").click(); };
  check((await page.locator(".actions").count()) === 0 && (await page.locator(".btn").count()) === 0, "the overview has no buttons at all, also no acknowledgements");
  const editing = /Vertrag bearbeiten|Folgevertrag|Neuer Vertrag|Vertrag löschen/;
  check((await page.getByRole("button", { name: editing }).count()) === 0, "the overview has no editing actions at all");
  check((await page.locator(".callout").count()) >= 2, "the notes with the reason stay on the cards");
  // the list of contracts: icons per row, a button for a new contract, the acknowledgements in the details
  await page.getByRole("tab", { name: "Verträge" }).click();
  await openRow("Strom Haus");
  await openRow("Internet");
  check((await page.locator(".actions").count()) === 2, "only the two contracts with something to acknowledge show buttons in the list");
  check((await listRow("Strom Haus").getByRole("button", { name: "Warnung bestätigen" }).count()) === 1, "warning button on Strom Haus");
  check((await listRow("Internet").getByRole("button", { name: "Kündigung bestätigen" }).count()) === 1, "cancellation button on Internet");
  const named = (name) => page.getByRole("button", { name, exact: true });
  check((await named("Vertrag bearbeiten").count()) === 6, "every row has an icon to edit the contract");
  check((await page.getByRole("button", { name: /^Folgevertrag (planen|bearbeiten)$/ }).count()) === 6, "and one to plan or edit the next contract");
  check((await named("Neuer Vertrag").count()) === 1, "the list has the button for a new contract");
  const row = (name) => page.locator("details", { hasText: name }).first();
  check((await row("Mobilfunk").getByRole("button", { name: "Folgevertrag bearbeiten", exact: true }).count()) === 1, "Mobilfunk can edit its planned contract");
  check((await row("Gas Heizung").getByRole("button", { name: "Folgevertrag planen", exact: true }).count()) === 1, "Gas can plan a next contract");
  check((await row("Gas Heizung").locator(".icon-btn").first().getAttribute("title")) === "Folgevertrag planen", "the icons have a tooltip");
  await row("Wasser").getByRole("button", { name: "Vertrag bearbeiten", exact: true }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".dialog input"));
  check(!(await row("Wasser").evaluate((el) => el.open)), "an icon does not open or close the row");
  await page.locator(".dialog").getByRole("button", { name: "Abbrechen" }).click();
  await page.getByRole("tab", { name: "Übersicht" }).click();

  // a negative recommended instalment is shown as 0 with a hint, never as a negative amount
  const gasText = await card(page, "Gas Heizung").innerText();
  check(gasText.includes("Kein Abschlag nötig: Das Guthaben deckt die Kosten bis Vertragsende"),
    "gas card says no instalment is needed instead of showing a negative recommendation");
  check(!/Abschlag auf [−-]|[−-]\d+,\d\d €[^\n]*pro Monat/.test(gasText), "no negative recommended instalment on the gas card");
  check((await card(page, "Strom Haus").innerText()).replace(/\u00a0/g, " ").includes("Abschlag auf 127,66 € pro Monat erhöhen"),
    "a needed increase is worded as an increase");
  // credit at the end: the recommendation is lower than the current instalment and says so
  await page.evaluate(() => {
    window.__panel._contracts = window.__panel._contracts.map((c) => (c.title === "Wasser" ? { ...c, abschlag_anpassung_empfohlen: 20, abschlag: 28 } : c));
    window.__panel._render();
  });
  check((await card(page, "Wasser").innerText()).replace(/\u00a0/g, " ").includes("Abschlag könnte auf 20,00 € pro Monat sinken"),
    "a lower recommendation is worded as a possible reduction");
  await page.getByRole("tab", { name: "Kosten" }).click();
  const gasRow = page.locator("tr", { hasText: "Gas Heizung" }).first();
  check((await gasRow.innerText()).includes("Guthaben deckt die Kosten") && !(await gasRow.innerText()).includes("−179"),
    "cost table: hint instead of the negative amount");
  check((await page.locator("tr", { hasText: "Strom Haus" }).first().innerText()).includes("127,66"), "cost table: positive recommendation unchanged");
  await page.getByRole("tab", { name: "Verträge" }).click();
  await page.locator("details", { hasText: "Gas Heizung" }).locator("summary").click();
  const gasDetails = (await page.locator("details", { hasText: "Gas Heizung" }).innerText()).replace(/\u00a0/g, " ");
  check(gasDetails.includes("Kein Abschlag nötig: Das Guthaben deckt die Kosten bis Vertragsende"),
    "contract details: the adjustment says no instalment is needed");
  await page.getByRole("tab", { name: "Übersicht" }).click();

  // switching is not offered in the panel (the contract switches itself on its start date)
  check((await page.getByRole("button", { name: "Jetzt wechseln" }).count()) === 0, "no switch button in the panel");

  // acknowledgements ask first as well, and cancel does nothing
  await page.getByRole("tab", { name: "Verträge" }).click();
  await openRow("Strom Haus");
  await openRow("Internet");
  const before = (await calls(page)).length;
  await listRow("Internet").getByRole("button", { name: "Kündigung bestätigen" }).click();
  check((await listRow("Internet").locator(".ask").count()) === 1, "cancellation acknowledgement asks first");
  check((await calls(page)).length === before, "no call before the acknowledgement is confirmed");
  await listRow("Internet").getByRole("button", { name: "Abbrechen" }).click();
  check((await calls(page)).length === before, "cancelling the acknowledgement does nothing");
  await listRow("Internet").getByRole("button", { name: "Kündigung bestätigen" }).click();
  await listRow("Internet").getByRole("button", { name: "Ja, bestätigen" }).click();
  await listRow("Strom Haus").getByRole("button", { name: "Warnung bestätigen" }).click();
  check((await calls(page)).length === before + 1, "warning acknowledgement also waits for confirmation");
  await listRow("Strom Haus").getByRole("button", { name: "Ja, bestätigen" }).click();
  const sent = (await calls(page)).map((c) => `${c.entry_id}:${c.action}`);
  check(sent.join(",") === "contract-5:confirm_cancellation,contract-1:confirm_abschlag_warning", `acknowledgements sent: ${sent}`);
  await context.close();
}

// ---- plan the next contract: the options flow of Home Assistant rendered in a dialog ----
const flowPath = "config/config_entries/options/flow";
const api = (page) => page.evaluate(() => window.__api);
const dialog = (page) => page.locator(".dialog");
// everything that changes a contract is an icon in its row of the "Contracts" tab
async function openDialog(page, name, button) {
  if (await page.locator(".tab[aria-selected=true]").innerText() !== "Verträge" && await page.locator(".tab[aria-selected=true]").innerText() !== "Contracts") {
    await page.getByRole("tab", { name: /Verträge|Contracts/ }).click();
  }
  const row = page.locator("details", { hasText: name }).first();
  if (/^Warnung|^Kündigung|^Acknowledge/.test(button)) {
    await page.getByRole("tab", { name: /Übersicht|Overview/ }).click();
    await card(page, name).getByRole("button", { name: button }).click();
  } else {
    await row.getByRole("button", { name: button, exact: true }).click();
  }
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".dialog input, .dialog .err"));
}
async function openPage(browser, query) {
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  page.on("pageerror", (e) => errors.push(`${query}: ${e.message}`));
  await page.clock.setFixedTime("2026-07-12T12:00:00Z");
  await page.goto(`${base}?${query}`);
  await page.waitForFunction(() => window.__panel && window.__panel.shadowRoot.querySelector(".card"));
  return { context, page };
}

{ // plan, validate, save, and mark the cancellation as done in the same step
  const { context, page } = await openPage(browser, "lang=de&reload=2");
  await openDialog(page, "Internet", "Folgevertrag planen");
  check((await dialog(page).innerText()).includes("Folgevertrag · Internet"), "dialog title names the contract");
  check(JSON.stringify((await api(page))[0]) === JSON.stringify({ method: "POST", path: flowPath, body: { handler: "contract-5" } }),
    "opening starts the options flow of the contract");
  check((await dialog(page).innerText()).includes("Wechseldatum (Beginn neuer Vertrag)"), "labels come from the integration's translations");
  check(await page.locator(".dialog .check input").isChecked(), "cancellation is marked as done by default");

  await page.locator(".dialog [name=next_beginn]").fill("2027-10-01");
  await page.locator(".dialog [name=next_anbieter]").fill("Neuer Anbieter");
  await page.locator(".dialog [name=next_abschlag]").fill("abc");
  await dialog(page).getByRole("button", { name: "Speichern" }).click();
  check((await dialog(page).innerText()).includes("Keine gültige Zahl"), "an invalid number is refused in the panel");
  check((await api(page)).length === 1, "nothing is sent while a field is invalid");

  await page.locator(".dialog [name=next_abschlag]").fill("44,98");
  check((await page.locator(".dialog .ferr").count()) === 0, "the error disappears once the field is edited");
  await dialog(page).screenshot({ path: join(outDir, "next-contract-dialog.png") });
  await dialog(page).getByRole("button", { name: "Speichern" }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".dialog")?.innerText.includes("Gespeichert"));
  check(JSON.stringify((await api(page))[1].body) === JSON.stringify({ next_beginn: "2027-10-01", next_anbieter: "Neuer Anbieter", next_abschlag: 44.98 }),
    "only the filled fields are sent, the decimal comma becomes a number");
  await page.waitForFunction(() => window.__calls.filter((c) => c.action === "confirm_cancellation").length === 3, null, { timeout: 8000 });
  check((await calls(page)).every((c) => c.entry_id === "contract-5" && c.action === "confirm_cancellation"),
    "the cancellation is acknowledged for this contract once it is loaded again (retried while it reloads)");
  check(!(await dialog(page).innerText()).includes("konnte nicht"), "no warning when the cancellation could be marked");
  await dialog(page).getByRole("button", { name: "Schließen" }).click();
  check((await page.locator(".dialog").count()) === 0, "the dialog closes");
  await context.close();
}

{ // cancelling aborts the flow, unticking the box leaves the cancellation alone
  const { context, page } = await openPage(browser, "lang=de");
  await openDialog(page, "Internet", "Folgevertrag planen");
  await dialog(page).getByRole("button", { name: "Abbrechen" }).click();
  const sent = await api(page);
  check(sent.length === 2 && sent[1].method === "DELETE" && sent[1].path === `${flowPath}/flow-5`, "cancel aborts the flow");
  await openDialog(page, "Internet", "Folgevertrag planen");
  await page.locator(".dialog [name=next_beginn]").fill("2027-10-01");
  await page.locator(".dialog .check input").uncheck();
  await dialog(page).getByRole("button", { name: "Speichern" }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".dialog")?.innerText.includes("Gespeichert"));
  await page.waitForTimeout(1500);
  check((await calls(page)).length === 0, "an unticked box leaves the cancellation reminder alone");
  await context.close();
}

{ // an existing plan is shown, can be removed after a second question
  const { context, page } = await openPage(browser, "lang=de");
  await openDialog(page, "Mobilfunk", "Folgevertrag bearbeiten");
  check((await page.locator(".dialog [name=next_beginn]").inputValue()) === "2027-01-01", "the planned start date is filled in");
  check((await page.locator(".dialog [name=next_anbieter]").inputValue()) === "Mobil Plus", "the planned provider is filled in");
  check((await page.locator(".dialog .check").count()) === 0, "no cancellation box where no reminder is due");
  await dialog(page).getByRole("button", { name: "Geplanten Vertrag entfernen" }).click();
  check((await api(page)).length === 1, "removing asks first");
  await dialog(page).getByRole("button", { name: "Abbrechen" }).first().click();
  check((await dialog(page).getByRole("button", { name: "Speichern" }).count()) === 1, "the question can be dismissed");
  await dialog(page).getByRole("button", { name: "Geplanten Vertrag entfernen" }).click();
  await dialog(page).getByRole("button", { name: "Ja, entfernen" }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".dialog")?.innerText.includes("entfernt"));
  const post = (await api(page)).at(-1);
  check(post.method === "POST" && JSON.stringify(post.body) === "{}", "removing sends an empty form, which the integration reads as 'no next contract'");
  await context.close();
}

{ // the integration's own validation errors are shown at the field and the input is kept
  const { context, page } = await openPage(browser, "lang=de&flowfail=1");
  await openDialog(page, "Strom Haus", "Folgevertrag planen");
  await page.locator(".dialog [name=next_beginn]").fill("2027-01-01");
  await page.locator(".dialog [name=next_abschlag]").fill("40");
  await dialog(page).getByRole("button", { name: "Speichern" }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".dialog .ferr"));
  check((await page.locator(".dialog .fld.bad .ferr").innerText()).includes("Keine gültige Zahl"), "backend error is shown at the field");
  check((await page.locator(".dialog [name=next_abschlag]").inputValue()) === "40", "typed values survive a rejected save");
  await context.close();
}

{ // REST failures are reported, not swallowed
  const { context, page } = await openPage(browser, "lang=de&flowerr=1");
  await openDialog(page, "Strom Haus", "Folgevertrag planen");
  check((await dialog(page).innerText()).includes("konnte nicht geladen werden"), "load failure is shown");
  await dialog(page).getByRole("button", { name: "Schließen" }).click();
  check((await page.locator(".dialog").count()) === 0, "and can be closed");
  await context.close();
}

// ---- edit a contract: the two steps of the integration's "Reconfigure" dialog ----
const configFlow = "config/config_entries/flow";

{ // step 1 (general data), step 2 (data of the sparte), a question before the contract data is replaced
  const { context, page } = await openPage(browser, "lang=de");
  await openDialog(page, "Strom Haus", "Vertrag bearbeiten");
  check((await dialog(page).innerText()).includes("Vertrag bearbeiten · Strom Haus"), "edit dialog names the contract");
  check(JSON.stringify((await api(page))[0]) === JSON.stringify({ method: "POST", path: configFlow, body: { handler: "tariffy", entry_id: "contract-1" } }),
    "editing starts the reconfigure flow of the contract");
  check((await page.locator(".dialog [name=sparte] option:checked").innerText()) === "Strom", "the sparte drop-down shows translated names");
  check((await page.locator(".dialog [name=name]").inputValue()) === "Strom Haus", "the name of the contract can be changed: it is the first field and filled in");
  check((await page.locator(".dialog .lbl").first().innerText()) === "Name", "and labelled");
  check((await page.locator(".dialog [name=anbieter]").inputValue()) === "Stadtwerke Nord", "stored provider is filled in");
  check((await page.locator(".dialog [name=erinnerung_monate] option:checked").innerText()) === "3 Monate vorher", "the reminder lead time is readable, not a bare number");
  check((await page.locator(".dialog [name=ende]").inputValue()) === "2026-12-31", "stored end date is filled in");
  check((await page.locator(".dialog [name=notify_target]").count()) === 1, "the notification target field is offered");
  check((await page.locator(".dialog .check").count()) === 0, "no cancellation box when editing the contract itself");

  await page.locator(".dialog [name=anbieter]").fill("");
  await dialog(page).getByRole("button", { name: "Weiter" }).click();
  check((await dialog(page).innerText()).includes("Pflichtfeld") && (await api(page)).length === 1, "a required field is checked in the panel");
  await page.locator(".dialog [name=anbieter]").fill("Neuer Versorger");
  await dialog(page).getByRole("button", { name: "Weiter" }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".dialog [name=arbeitspreis]"));
  const first = (await api(page))[1];
  check(first.path === `${configFlow}/rflow-1` && first.body.anbieter === "Neuer Versorger" && first.body.sparte === "electricity",
    "step 1 sends the general data");
  check(Object.values(first.body).every((v) => v !== "" && v !== null), "empty optional fields are left out");
  check(first.body.beginn === "2026-01-01" && first.body.erinnerung_monate === "3", "unchanged values are sent as they are stored");
  check((await api(page)).length === 2, "going to step 2 asks nothing");

  check((await page.locator(".dialog [name=arbeitspreis]").inputValue()) === "0.2977", "step 2 shows the stored price");
  check(await page.locator(".dialog [name=abschlag_warnung]").isChecked(), "a stored yes/no setting is shown as ticked");
  check(!(await page.locator(".dialog [name=oekostrom]").isChecked()), "and an unticked one as unticked");
  await page.locator(".dialog [name=abschlag]").fill("100,5");
  await dialog(page).screenshot({ path: join(outDir, "edit-contract-dialog.png") });
  await dialog(page).getByRole("button", { name: "Speichern" }).click();
  check((await dialog(page).innerText()).includes("Änderungen speichern?") && (await api(page)).length === 2, "saving asks first");
  await dialog(page).getByRole("button", { name: "Abbrechen" }).first().click();
  check((await dialog(page).getByRole("button", { name: "Speichern" }).count()) === 1 && (await api(page)).length === 2, "the question can be dismissed");
  await dialog(page).getByRole("button", { name: "Speichern" }).click();
  await dialog(page).getByRole("button", { name: "Ja, speichern" }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".dialog")?.innerText.includes("Gespeichert"));
  const second = (await api(page))[2];
  check(second.body.abschlag === 100.5 && second.body.arbeitspreis === 0.2977, "numbers are sent as numbers, the decimal comma is understood");
  check(second.body.oekostrom === false && second.body.abschlag_warnung === true, "yes/no settings are always sent");
  check((await calls(page)).length === 0, "editing never touches the cancellation reminder");
  await context.close();
}

{ // closing in step 2 aborts the flow; gas keeps its text fields as typed
  const { context, page } = await openPage(browser, "lang=de");
  await openDialog(page, "Gas Heizung", "Vertrag bearbeiten");
  await dialog(page).getByRole("button", { name: "Weiter" }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".dialog [name=brennwert]"));
  check((await page.locator(".dialog [name=gas_einheit]").inputValue()) === "m³", "gas unit is selected");
  check((await page.locator(".dialog [name=brennwert]").inputValue()) === "11.2", "stored calorific value is filled in");
  await page.locator(".dialog [name=brennwert]").fill("11,5");
  await dialog(page).getByRole("button", { name: "Abbrechen" }).click();
  const sent = await api(page);
  check(sent.at(-1).method === "DELETE" && sent.at(-1).path === `${configFlow}/rflow-2`, "cancel in step 2 aborts the flow");
  check(!sent.some((c) => c.method === "POST" && c.path.endsWith("rflow-2") && c.body.brennwert === "11,5"), "nothing typed is sent without saving");
  await openDialog(page, "Gas Heizung", "Vertrag bearbeiten");
  await dialog(page).getByRole("button", { name: "Weiter" }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".dialog [name=brennwert]"));
  await page.locator(".dialog [name=brennwert]").fill("11,5");
  await dialog(page).getByRole("button", { name: "Speichern" }).click();
  await dialog(page).getByRole("button", { name: "Ja, speichern" }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".dialog")?.innerText.includes("Gespeichert"));
  check((await api(page)).at(-1).body.brennwert === "11,5", "the text field is sent as typed, the integration parses it");
  await context.close();
}

{ // an error of the integration is shown at the field in step 2 and the input is kept
  const { context, page } = await openPage(browser, "lang=de&flowfail=1");
  await openDialog(page, "Internet", "Vertrag bearbeiten");
  await dialog(page).getByRole("button", { name: "Weiter" }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".dialog [name=abschlag]"));
  await page.locator(".dialog [name=abschlag]").fill("12");
  await dialog(page).getByRole("button", { name: "Speichern" }).click();
  await dialog(page).getByRole("button", { name: "Ja, speichern" }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".dialog .ferr"));
  check((await page.locator(".dialog [name=abschlag]").inputValue()) === "12", "typed values survive a rejected save");
  check(await dialog(page).getByRole("button", { name: "Speichern" }).isVisible(), "and the form can be saved again");
  await context.close();
}

// ---- create and delete contracts ----
const entryApi = "config/config_entries/entry";

{ // a new contract: the integration's setup flow, name and sparte first
  const { context, page } = await openPage(browser, "lang=de");
  await page.getByRole("tab", { name: "Verträge" }).click();
  await page.getByRole("button", { name: "Neuer Vertrag" }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".dialog [name=name]"));
  check((await dialog(page).innerText()).includes("Neuer Vertrag"), "the dialog is titled as a new contract");
  check(JSON.stringify((await api(page))[0]) === JSON.stringify({ method: "POST", path: configFlow, body: { handler: "tariffy" } }),
    "creating starts the setup flow without a contract");
  check((await page.locator(".dialog [name=sparte] option:checked").innerText()) === "Strom", "the sparte drop-down shows translated names");
  await dialog(page).getByRole("button", { name: "Weiter" }).click();
  check((await dialog(page).innerText()).includes("Pflichtfeld") && (await api(page)).length === 1, "name and provider are required");

  await page.locator(".dialog [name=name]").fill("Gas Ferienhaus");
  await page.locator(".dialog [name=sparte]").selectOption("gas");
  await page.locator(".dialog [name=anbieter]").fill("Nordgas");
  await dialog(page).getByRole("button", { name: "Weiter" }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".dialog [name=brennwert]"));
  const first = (await api(page))[1];
  check(first.path === `${configFlow}/cflow-1` && first.body.name === "Gas Ferienhaus" && first.body.sparte === "gas" && first.body.anbieter === "Nordgas",
    "step 1 sends name, sparte and provider");
  check(Object.values(first.body).every((v) => v !== "" && v !== null), "empty optional fields are left out");
  check((await page.locator(".dialog [name=gas_einheit]").inputValue()) === "m³", "the step of the sparte offers its defaults");

  await page.locator(".dialog [name=arbeitspreis]").fill("0,105");
  await page.locator(".dialog [name=abschlag]").fill("80");
  await page.locator(".dialog [name=brennwert]").fill("11,2");
  await dialog(page).screenshot({ path: join(outDir, "new-contract-dialog.png") });
  await dialog(page).getByRole("button", { name: "Speichern" }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".dialog")?.innerText.includes("angelegt"));
  const second = (await api(page))[2];
  check(second.body.arbeitspreis === 0.105 && second.body.abschlag === 80 && second.body.brennwert === "11,2", "the values of the sparte are sent");
  check(typeof second.body.oekostrom === "boolean", "yes/no settings are always sent");
  check((await calls(page)).length === 0, "creating never touches a reminder");
  await context.close();
}

{ // cancelling a new contract aborts the setup flow
  const { context, page } = await openPage(browser, "lang=de");
  await page.getByRole("tab", { name: "Verträge" }).click();
  await page.getByRole("button", { name: "Neuer Vertrag" }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".dialog [name=name]"));
  await dialog(page).getByRole("button", { name: "Abbrechen" }).click();
  const sent = await api(page);
  check(sent.at(-1).method === "DELETE" && sent.at(-1).path === `${configFlow}/cflow-1`, "cancel aborts the setup flow");
  await context.close();
}

{ // deleting: a long way round on purpose, the name has to be typed
  const { context, page } = await openPage(browser, "lang=de");
  await openDialog(page, "Strom Haus", "Vertrag bearbeiten");
  await dialog(page).getByRole("button", { name: "Vertrag löschen" }).click();
  check((await dialog(page).innerText()).includes("endgültig löschen"), "deleting asks first");
  const confirm = dialog(page).getByRole("button", { name: "Endgültig löschen" });
  check(await confirm.isDisabled(), "the delete button is disabled until the name is typed");
  await page.locator(".dialog .confirm-name").fill("Strom");
  check(await confirm.isDisabled(), "a part of the name is not enough");
  await dialog(page).screenshot({ path: join(outDir, "delete-contract-dialog.png") });
  await dialog(page).getByRole("button", { name: "Abbrechen" }).first().click();
  check((await api(page)).every((c) => !c.path.startsWith(entryApi)), "cancelling deletes nothing");
  await dialog(page).getByRole("button", { name: "Vertrag löschen" }).click();
  await page.locator(".dialog .confirm-name").fill("Strom Haus");
  check(await confirm.isEnabled(), "the full name enables the button");
  await confirm.click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".dialog")?.innerText.includes("gelöscht"));
  const sent = await api(page);
  const removal = sent.filter((c) => c.method === "DELETE");
  check(removal.length === 2 && removal[0].path === `${configFlow}/rflow-1` && removal[1].path === `${entryApi}/contract-1`,
    "the open form is aborted, then exactly this contract is removed");
  check((await dialog(page).innerText()).includes("Langzeit-Statistiken"), "the dialog says that the statistics stay");
  await context.close();
}

{ // a failing removal is reported
  const { context, page } = await openPage(browser, "lang=de&deletefail=1");
  await openDialog(page, "Internet", "Vertrag bearbeiten");
  await dialog(page).getByRole("button", { name: "Vertrag löschen" }).click();
  await page.locator(".dialog .confirm-name").fill("Internet");
  await dialog(page).getByRole("button", { name: "Endgültig löschen" }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".dialog .err"));
  check((await dialog(page).innerText()).includes("Löschen fehlgeschlagen"), "the failure is shown");
  await context.close();
}

// ---- the rows of the contract list stay readable at every width (name never squeezed, nothing overlaps) ----
for (const width of [1280, 900, 600, 390]) {
  const context = await browser.newContext({ viewport: { width, height: 900 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  page.on("pageerror", (e) => errors.push(`list ${width}: ${e.message}`));
  await page.clock.setFixedTime("2026-07-12T12:00:00Z");
  await page.goto(`${base}?lang=de`);
  await page.waitForFunction(() => window.__panel && window.__panel.shadowRoot.querySelector(".card"));
  await page.getByRole("tab", { name: "Verträge" }).click();
  const rows = await page.evaluate(() => [...window.__panel.shadowRoot.querySelectorAll("details > summary")].map((summary) => {
    const box = (sel) => { const el = summary.querySelector(sel); if (!el) return null; const r = el.getBoundingClientRect(); return { x: r.x, y: r.y, w: r.width, h: r.height, r: r.right, b: r.bottom }; };
    return { who: box(".who"), meta: box(".meta"), end: box(".end"), chips: box(".chips"), row: summary.getBoundingClientRect().width };
  }));
  check(rows.length === 6, `list ${width}: six rows`);
  const overlap = (a, b) => a && b && a.x < b.r - 1 && b.x < a.r - 1 && a.y < b.b - 1 && b.y < a.b - 1;
  for (const [i, row] of rows.entries()) {
    check(row.who.w >= 150, `list ${width}, row ${i + 1}: the name keeps a readable width (${Math.round(row.who.w)}px)`);
    check(row.meta.h <= 40, `list ${width}, row ${i + 1}: the subtitle is not broken word by word (${Math.round(row.meta.h)}px high)`);
    check(!overlap(row.who, row.end) && !overlap(row.who, row.chips) && !overlap(row.chips, row.end), `list ${width}, row ${i + 1}: nothing overlaps`);
  }
  if (width === 1280 || width === 390) await page.screenshot({ path: join(outDir, `list-${width}.png`), fullPage: false });
  await context.close();
}

// ---- the redesigned cards ----
{
  const { context, page } = await openPage(browser, "lang=de");
  const tones = await page.evaluate(() => Object.fromEntries([...window.__panel.shadowRoot.querySelectorAll("section.card")]
    .map((el) => [el.querySelector(".title").textContent, [...el.classList].filter((c) => c.startsWith("tone-"))[0] || "none"])));
  check(tones["Strom Haus"] === "tone-red" && tones["Gas Heizung"] === "tone-green" && tones["Internet"] === "tone-orange" && tones["Mobilfunk"] === "none",
    `the top of a card is tinted by its state: ${JSON.stringify(tones)}`);

  // a contract without start and end date has nothing to show in a ring
  await page.evaluate(() => {
    const panel = window.__panel;
    panel._contracts = panel._contracts.map((c) => (c.title === "Mobilfunk" ? { ...c, beginn: null, ende: null } : c));
    panel._render();
  });
  check((await card(page, "Mobilfunk").locator(".ring").count()) === 0, "no empty ring when start or end date is missing");
  check((await card(page, "Strom Haus").locator(".ring").count()) === 1, "the ring stays where it has a value");

  // the balance today and the forecast point in different directions: the card says why
  await page.evaluate(() => {
    const panel = window.__panel;
    panel._tab = "overview";
    panel._contracts = panel._contracts.map((c) => (c.title === "Strom Haus" ? { ...c, guthaben_bisher: -84.36, prognose_real: 54 }
      : c.title === "Wasser" ? { ...c, guthaben_bisher: 40, prognose_real: -25 } : c));
    panel._render();
  });
  const catchUp = (await card(page, "Strom Haus").innerText()).replace(/\u00a0/g, " ");
  check(catchUp.includes("Heute 84,36 € im Rückstand") && /saldo heute/i.test(catchUp), "balance behind today but credit at the end: the card explains it");
  check((await card(page, "Wasser").innerText()).replace(/\u00a0/g, " ").includes("Heute 40,00 € im Plus"), "balance ahead today but balance due at the end: the card explains it");
  check(!(await card(page, "Gas Heizung").innerText()).includes("Heute"), "no explanation where both point the same way");

  // the state badge is the last one, so it sits at the far right; other badges stand to its left
  await page.evaluate(() => {
    window.__panel._contracts = window.__panel._contracts.map((c) => (c.title === "Gas Heizung" ? { ...c, wechsel: "2027-01-01" } : c));
    window.__panel._render();
  });
  const chipTexts = await card(page, "Gas Heizung").locator(".chip").allInnerTexts();
  check(chipTexts.length === 2 && /guthaben|nachzahlung/i.test(chipTexts[chipTexts.length - 1]), `the state badge comes last (${chipTexts})`);
  check(!/wechsel|kündigen/i.test(chipTexts[chipTexts.length - 1]), "switch and cancel badges stand left of the state badge");

  // cards of one row line up: the tiles, the bars and the footer start at the same height in every card of the row
  const rowTops = await page.evaluate(() => {
    const root = window.__panel.shadowRoot;
    const tops = (sel) => ["Strom Haus", "Gas Heizung", "Wasser"].map((name) => {
      const card = [...root.querySelectorAll("section.card")].find((el) => el.querySelector(".title")?.textContent === name);
      const el = card && card.querySelector(sel);
      return el ? Math.round(el.getBoundingClientRect().top - card.getBoundingClientRect().top) : null;
    });
    return { hero: tops(".hero .label"), ring: tops(".ring"), big: tops(".big"), tiles: tops(".tiles"), bars: tops(".bars"), foot: tops(".foot") };
  });
  for (const [part, tops] of Object.entries(rowTops)) {
    check(tops.every((v) => v !== null) && new Set(tops).size === 1, `${part} starts at the same height in all cards of the row (${tops})`);
  }

  // the second line of a card does not repeat the kind of contract: the icon shows it
  check((await card(page, "Gas Heizung").locator(".meta").innerText()).trim() === "Energie Süd · Gas Basis", "the second line has provider and tariff, not the kind of contract again");

  // the first day of a contract with a sensor: costs and consumption exist, the forecast does not yet
  await page.evaluate(() => {
    const panel = window.__panel;
    panel._contracts = panel._contracts.map((c) => (c.title === "Strom Haus" ? { ...c, prognose_real: null, hochgerechnet: null, verbrauch_hochgerechnet: null } : c));
    panel._tab = "contracts";
    panel._render();
  });
  await page.locator("details", { hasText: "Strom Haus" }).locator("summary").click();
  const details = (await page.locator("details", { hasText: "Strom Haus" }).innerText()).replace(/ /g, " ");
  check(/Verbrauch/i.test(details) && details.includes("Kosten bisher"), "the consumption block shows on day one although there is no forecast yet");
  check(!details.includes("Prognose zum Vertragsende"), "and the forecast row stays out");
  await context.close();
}

{ // metered and flat-rate contracts are told apart
  const { context, page } = await openPage(browser, "lang=de");
  const groups = await page.evaluate(() => [...window.__panel.shadowRoot.querySelectorAll(".group")].map((g) => ({
    title: g.querySelector(".group-title span").textContent, count: g.querySelector(".count").textContent,
    cards: [...g.querySelectorAll("section.card")].map((c) => c.querySelector(".title").textContent),
  })));
  check(JSON.stringify(groups.map((g) => [g.title, g.count])) === JSON.stringify([["Verbrauchsverträge", "4"], ["Pauschalverträge", "2"]]), `two groups with their counts: ${JSON.stringify(groups.map((g) => [g.title, g.count]))}`);
  check(groups[1].cards.join() === "Internet,Mobilfunk", "internet and mobile are flat-rate contracts");
  for (const name of ["Internet", "Mobilfunk"]) {
    const text = await card(page, name).innerText();
    check(await card(page, name).locator(".ring").count() === 0, `${name}: no ring`);
    check((await card(page, name).locator(".tile .label").allInnerTexts()).join().toLowerCase().startsWith("kosten bisher"), `${name}: the cost so far (instalments due until today) is shown`);
    check(/ABSCHLAG \/ MONAT/i.test(text), `${name}: leads with the monthly amount`);
  }
  check((await card(page, "Internet").locator(".bar").count()) === 1, "a flat-rate contract with both dates shows how far its term has come");
  check((await card(page, "Strom Haus").locator(".tile").count()) === 3, "a metered contract keeps its three figures");

  // a flat-rate contract without an end date (a typical internet contract)
  await page.evaluate(() => {
    const panel = window.__panel;
    panel._contracts = panel._contracts.map((c) => (c.title === "Internet"
      ? { ...c, ende: null, restlaufzeit: null, jahreskosten: null, erinnerung_datum: null, erinnerung_aktiv: false } : c));
    panel._render();
  });
  const open = (await card(page, "Internet").innerText()).replace(/ /g, " ");
  check(open.includes("39,99 €") && open.includes("Kein Vertragsende"), "without an end date: the monthly amount and \"no contract end\"");
  check(!open.includes("über die Laufzeit"), "and no total \"over the contract term\" that would assume a term");
  check(!open.includes("–") && (await card(page, "Internet").locator(".bar").count()) === 0, "and no dash or empty bar");

  // three contracts per row on a wide screen, in both groups; the cards of a row are equally high
  const cols = await page.evaluate(() => [...window.__panel.shadowRoot.querySelectorAll(".grid")].map((g) => getComputedStyle(g).gridTemplateColumns.split(" ").length));
  check(cols.length === 2 && cols.every((n) => n === 3), `three columns in both groups (${cols})`);
  const rows = await page.evaluate(() => {
    const byTop = {};
    for (const el of window.__panel.shadowRoot.querySelectorAll(".grid > section.card")) {
      const r = el.getBoundingClientRect();
      (byTop[Math.round(r.top)] ||= []).push(Math.round(r.height));
    }
    return Object.values(byTop);
  });
  check(rows.length === 3 && rows[0].length === 3 && rows[1].length === 1 && rows[2].length === 2 && rows.every((row) => row.every((h) => h === row[0])),
    `4 + 2 contracts make rows of 3, 1 and 2 cards, each row equally high: ${JSON.stringify(rows)}`);
  await context.close();
}

{ // the cost table and the contract list are split like the overview
  const { context, page } = await openPage(browser, "lang=de");
  const groupsOf = () => page.evaluate(() => [...window.__panel.shadowRoot.querySelectorAll(".group")].map((g) => [
    g.querySelector(".group-title span").textContent, g.querySelector(".count").textContent]));
  await page.getByRole("tab", { name: "Verträge" }).click();
  check(JSON.stringify(await groupsOf()) === JSON.stringify([["Verbrauchsverträge", "4"], ["Pauschalverträge", "2"]]), "the contract list has the two groups");
  const listGroups = await page.evaluate(() => [...window.__panel.shadowRoot.querySelectorAll(".group")].map((g) => [...g.querySelectorAll("details .title")].map((t) => t.textContent).join()));
  check(listGroups[1] === "Internet,Mobilfunk", `internet and mobile are in the flat-rate group of the list: ${listGroups}`);

  await page.getByRole("tab", { name: "Kosten" }).click();
  check(JSON.stringify(await groupsOf()) === JSON.stringify([["Verbrauchsverträge", "4"], ["Pauschalverträge", "2"]]), "the cost table has the two groups");
  const heads = await page.evaluate(() => [...window.__panel.shadowRoot.querySelectorAll(".group table")].map((t) => [...t.querySelectorAll("th")].map((h) => h.textContent)));
  check(heads.length === 2 && heads[0].includes("Saldo heute") && heads[0].includes("Empfohlen"), "the metered table has balance, forecast and recommendation");
  check(!heads[1].includes("Saldo heute") && !heads[1].includes("Zum Vertragsende") && heads[1].includes("Vertragsende") && heads[1].includes("Restlaufzeit"),
    `the flat-rate table has no balance but the term: ${heads[1]}`);

  const cells = async (name) => (await page.locator("tr", { hasText: name }).first().locator("td").allInnerTexts()).map((t) => t.replace(/ /g, " ").trim());
  const internet = await cells("Internet");
  const expected = await page.evaluate(() => window.__panel._contracts.find((c) => c.title === "Internet").abschlag_bisher_gezahlt);
  check(expected > 300, `the backend delivers the instalments due so far (${expected})`);
  check(internet[1].includes("373"), `Internet: the cost so far is filled in (${internet[1]})`);
  check(internet[2] === "80 Tage" && internet[3] === "30.09.2026" && internet[4].startsWith("39,99 €"), `Internet: remaining term, end and instalment (${internet})`);
  check(internet[4].includes("480 € / Jahr"), "Internet: the yearly instalment stands under the monthly one");
  // both tables share one column grid: cost so far and instalment sit exactly below each other
  const edges = await page.evaluate(() => [...window.__panel.shadowRoot.querySelectorAll(".group table")].map((t) => [...t.querySelectorAll("th")].map((th) => Math.round(th.getBoundingClientRect().right))));
  check(edges.length === 2 && edges[0][1] === edges[1][1] && edges[0][4] === edges[1][4] && edges[0].length === edges[1].length,
    `the two cost tables line up (cost so far ${edges.map((e) => e[1])}, instalment ${edges.map((e) => e[4])})`);

  // group totals and the grand total
  const number = (text) => Number(text.replace(/[^\d,]/g, "").replace(",", "."));
  const expectedCosts = await page.evaluate(() => {
    const metered = ["electricity", "electricity_ht_nt", "gas", "water"];
    const cost = (c) => c.kosten_bisher ?? (metered.includes(c.sparte) ? 0 : c.abschlag_bisher_gezahlt ?? 0);
    const all = window.__panel._contracts;
    return { metered: all.filter((c) => metered.includes(c.sparte)).reduce((s, c) => s + cost(c), 0),
      flat: all.filter((c) => !metered.includes(c.sparte)).reduce((s, c) => s + cost(c), 0) };
  });
  const totals = await page.evaluate(() => [...window.__panel.shadowRoot.querySelectorAll("tr.total")].map((r) => r.querySelector("td:nth-child(2)").textContent));
  check(Math.abs(number(totals[0]) - expectedCosts.metered) <= 1 && Math.abs(number(totals[1]) - expectedCosts.flat) <= 1,
    `each group has its own total (${totals} for ${JSON.stringify(expectedCosts)})`);
  // the overall total is a row of the same column grid: right below the costs and the instalments above
  const grand = await page.evaluate(() => {
    const root = window.__panel.shadowRoot;
    const right = (el) => Math.round(el.getBoundingClientRect().right);
    const cells = [...root.querySelectorAll(".grand-table td")];
    const heads = [...root.querySelector(".group table").querySelectorAll("th")];
    const sums = [...root.querySelectorAll("tr.total")].map((r) => [...r.querySelectorAll("td")].map(right));
    return { cost: cells[1].textContent, instalment: cells[4].textContent, costX: right(cells[1]), instalmentX: right(cells[4]),
      headCostX: right(heads[1]), headInstalmentX: right(heads[4]), sumCostX: sums[0][1], sumInstalmentX: sums[0][4] };
  });
  check(Math.abs(number(grand.cost) - (expectedCosts.metered + expectedCosts.flat)) <= 1, `the grand total adds both groups (${grand.cost})`);
  check(grand.costX === grand.headCostX && grand.costX === grand.sumCostX, `overall cost sits below the costs above (${grand.costX} / ${grand.sumCostX} / ${grand.headCostX})`);
  check(grand.instalmentX === grand.headInstalmentX && grand.instalmentX === grand.sumInstalmentX, `overall instalment sits below the instalments above (${grand.instalmentX} / ${grand.sumInstalmentX} / ${grand.headInstalmentX})`);
  await context.close();
}

{ // the whole width of the window is used; very wide windows get a fourth column
  for (const [width, columns] of [[1280, 3], [1600, 3], [1920, 4]]) {
    const context = await browser.newContext({ viewport: { width, height: 900 }, deviceScaleFactor: 1 });
    const page = await context.newPage();
    await page.clock.setFixedTime("2026-07-12T12:00:00Z");
    await page.goto(`${base}?lang=de`);
    await page.waitForFunction(() => window.__panel && window.__panel.shadowRoot.querySelector(".card"));
    const m = await page.evaluate(() => {
      const root = window.__panel.shadowRoot;
      return { wrap: Math.round(root.querySelector(".wrap").getBoundingClientRect().width),
        cols: getComputedStyle(root.querySelector(".grid.metered")).gridTemplateColumns.split(" ").length };
    });
    check(m.wrap >= width - 60, `${width}px: the content uses the width of the window (${m.wrap}px)`);
    check(m.cols === columns, `${width}px: ${columns} columns (${m.cols})`);
    if (width === 1920) await page.screenshot({ path: join(outDir, "wide-overview.png"), fullPage: false });
    await context.close();
  }
}

{ // the header of the overview: four tiles with details
  const { context, page } = await openPage(browser, "lang=de");
  const tiles = await page.evaluate(() => [...window.__panel.shadowRoot.querySelectorAll(".summary .sum")].map((t) => ({
    text: t.innerText.replace(/ /g, " "),
    rows: [...t.querySelectorAll(".mrow")].map((r) => r.innerText.replace(/ /g, " ").replace(/\n/g, " ")),
    segments: [...t.querySelectorAll(".split span")].map((x) => parseFloat(x.style.width)),
  })));
  check(tiles.length === 4, `four tiles in the header (${tiles.length})`);
  check(tiles[0].text.includes("322,98 €") && tiles[0].text.includes("≈ 3.876 € / Jahr"), "instalments per month and per year");
  check(tiles[0].text.includes("Verbrauch 263,00 €") && tiles[0].text.includes("Pauschal 59,98 €"), "split into metered and flat-rate contracts");
  check(tiles[0].segments.length === 2 && Math.abs(tiles[0].segments[0] - 81.4) < 0.3 && Math.abs(tiles[0].segments[1] - 18.6) < 0.3, `the bar is proportional (${tiles[0].segments})`);
  check(tiles[1].text.toLowerCase().includes("kosten bisher") && tiles[1].text.includes("2.772,18 €") && tiles[1].text.includes("Fällige Abschläge bisher"), "cost so far with the instalments due");
  check(tiles[1].rows.length === 1 && tiles[1].rows[0].includes("Saldo heute") && tiles[1].rows[0].includes("−8,56 €"), `balance so far (${tiles[1].rows})`);
  check(tiles[2].rows.length === 4 && tiles[2].rows[0].startsWith("Strom Haus") && tiles[2].rows[3].startsWith("Gas Heizung"), `forecast per contract, worst first (${tiles[2].rows})`);
  check(tiles[3].text.toLowerCase().includes("nächste termine") && tiles[3].rows.length === 2, `the next dates (${tiles[3].rows.length} more rows)`);
  const dateRows = tiles[3].rows.map((r) => r.match(/^(\d\d)\.(\d\d)\.(\d{4})/)).filter(Boolean).map((m) => `${m[3]}${m[2]}${m[1]}`);
  check(dateRows.length === 2 && dateRows[0] <= dateRows[1], `dates are in order (${dateRows})`);
  check(new Set(tiles[3].rows.map((r) => r.replace(/ in \d+ Tagen$/, ""))).size === tiles[3].rows.length, "no contract appears twice for the same date");
  await context.close();
}

{ // nothing sticks out sideways on a phone, in any view
  const context = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  await page.clock.setFixedTime("2026-07-12T12:00:00Z");
  await page.goto(`${base}?lang=de&narrow=1`);
  await page.waitForFunction(() => window.__panel && window.__panel._compact === true);
  for (const tab of ["Übersicht", "Kosten", "Verträge"]) {
    await page.getByRole("tab", { name: tab }).click();
    const width = await page.evaluate(() => document.scrollingElement.scrollWidth);
    check(width <= 391, `${tab} on a phone fits the width (${width}px)`);
  }
  await context.close();
}

{ // the figures of a card stay readable on a phone
  const context = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  await page.clock.setFixedTime("2026-07-12T12:00:00Z");
  await page.goto(`${base}?lang=de&narrow=1`);
  await page.waitForFunction(() => window.__panel && window.__panel._compact === true);
  await page.locator("details.card", { hasText: "Strom Haus" }).locator("summary").click();
  const tiles = await page.evaluate(() => [...window.__panel.shadowRoot.querySelectorAll("details.card[open] .tile")].map((el) => {
    const r = el.getBoundingClientRect();
    return { w: Math.round(r.width), v: el.querySelector(".v").getBoundingClientRect().height };
  }));
  check(tiles.length === 3 && tiles.every((t) => t.v <= 24), `no figure breaks into several lines on a phone: ${JSON.stringify(tiles)}`);
  await context.close();
}

{ // English and the phone layout
  const { context, page } = await openPage(browser, "lang=en");
  await openDialog(page, "Gas Heizung", "Plan next contract");
  check((await dialog(page).innerText()).includes("Next contract · Gas Heizung"), "English dialog title");
  check((await page.locator(".dialog select").count()) === 1, "the gas unit is a drop-down");
  check((await page.locator(".dialog select").inputValue()) === "m³", "its default is selected");
  await context.close();
}

{ // a failing action shows its error and re-enables the button
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  await page.clock.setFixedTime("2026-07-12T12:00:00Z");
  await page.goto(`${base}?lang=de&fail=1`);
  await page.waitForFunction(() => window.__panel && window.__panel.shadowRoot.querySelector(".card"));
  await page.getByRole("tab", { name: "Verträge" }).click();
  const strom = page.locator("details:not(.card)", { hasText: "Strom Haus" }).first();
  await strom.locator("summary").click();
  await strom.getByRole("button", { name: "Warnung bestätigen" }).click();
  await strom.getByRole("button", { name: "Ja, bestätigen" }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".err"));
  check((await strom.locator(".err").innerText()).includes("fehlgeschlagen"), "error text is shown");
  check(await strom.getByRole("button", { name: "Warnung bestätigen" }).isEnabled(), "button is usable again after an error");
  await strom.screenshot({ path: join(outDir, "actions-error.png") });
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
  await page.getByRole("tab", { name: "Verträge" }).click();
  check((await page.getByRole("button", { name: /Neuer Vertrag|bearbeiten|Folgevertrag/ }).count()) === 0 && (await page.locator(".icon-btn").count()) === 0,
    "and no icons and no button for a new contract in the list");
  await context.close();
}

{ // phone: buttons are inside the expanded card
  const context = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  const page = await context.newPage();
  await page.clock.setFixedTime("2026-07-12T12:00:00Z");
  await page.goto(`${base}?lang=de&narrow=1`);
  await page.waitForFunction(() => window.__panel && window.__panel._compact === true);
  check((await page.locator(".btn").count()) === 0, "phone: the cards of the overview have no buttons");
  await page.getByRole("tab", { name: "Verträge" }).click();
  const acks = page.locator(".actions .btn");
  check((await acks.count()) === 2, "phone: the two acknowledgements are buttons in the list");
  check(!(await acks.first().isVisible()), "phone: buttons stay hidden until the row is expanded");
  await page.locator("details", { hasText: "Internet" }).first().locator("summary").click();
  check(await page.locator("details", { hasText: "Internet" }).first().getByRole("button", { name: "Kündigung bestätigen" }).isVisible(), "phone: button visible after expanding");
  await context.close();
}

{ // history and archive: archived contracts only show in the History tab, expired ones can be archived
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  page.on("pageerror", (e) => errors.push(`history: ${e.message}`));
  await page.clock.setFixedTime("2026-07-12T12:00:00Z");
  await page.goto(`${base}?lang=de`);
  await page.waitForFunction(() => window.__panel && window.__panel.shadowRoot.querySelector(".card"));
  const wrapText = () => page.evaluate(() => window.__panel.shadowRoot.querySelector(".wrap").innerText.replace(/\u00a0/g, " "));
  const tab = (name) => page.getByRole("tab", { name, exact: true }).click();

  check((await page.locator("section.card").count()) === 6 && !(await wrapText()).includes("Altvertrag"), "an archived contract is not on the overview");
  await tab("Kosten");
  check(!(await wrapText()).includes("Altvertrag"), "an archived contract is not in the costs");
  await tab("Verträge");
  check((await page.locator("details").count()) === 6 && !(await wrapText()).includes("Altvertrag"), "an archived contract is not in the contract list");

  await tab("Historie");
  const history = await wrapText();
  check(/archivierte verträge/i.test(history) && history.includes("Strom Altvertrag"), "the History tab lists the archived contract");
  check(/frühere laufzeiten/i.test(history), "and the earlier terms of the other contracts");
  check((await page.locator(".hist[data-id=contract-1] tbody tr").count()) === 2, "Strom Haus shows its two earlier terms");
  check((await page.locator(".hist[data-id=contract-1] tbody tr").first().innerText()).replace(/\u00a0/g, " ").includes("01.01.2025 – 31.12.2025"), "the newest term comes first");
  check((await page.locator(".hist[data-id=contract-7] tbody tr").count()) === 2, "the archived contract shows its terms");
  check(history.includes("Archiviert"), "the archived contract is marked");
  check(!history.includes("Warnung bestätigen") && !history.includes("Kündigung bestätigen"), "the History tab offers no acknowledgements, only archive and restore");
  await page.screenshot({ path: join(outDir, "desktop-history-actions.png"), fullPage: true });

  // restore asks first
  const before = (await calls(page)).length;
  await page.getByRole("button", { name: "Zurückholen" }).click();
  check((await page.locator(".hist .ask").count()) === 1 && (await calls(page)).length === before, "restoring asks first");
  await page.getByRole("button", { name: "Abbrechen" }).click();
  check((await calls(page)).length === before, "cancelling does nothing");
  await page.getByRole("button", { name: "Zurückholen" }).click();
  await page.getByRole("button", { name: "Ja, zurückholen" }).click();
  check((await calls(page)).some((c) => c.entry_id === "contract-7" && c.action === "restore_contract"), "restore is sent for the archived contract");

  // an expired contract can be archived (in the Contracts tab, after asking)
  await page.evaluate(() => {
    const panel = window.__panel;
    panel._contracts = panel._contracts.map((c) => (c.title === "Internet" ? { ...c, archivierbar: true } : c));
    panel._tab = "overview";
    panel._render();
  });
  const internet = (await card(page, "Internet").innerText()).replace(/\u00a0/g, " ");
  check(/abgelaufen/i.test(internet) && internet.includes("Im Tab Verträge kannst du ihn archivieren"), "an expired contract is marked and says where to archive it");
  check((await page.getByRole("button", { name: "Archivieren" }).count()) === 0, "the overview has no archive button");
  await tab("Verträge");
  await page.locator("details", { hasText: "Internet" }).first().locator("summary").click();
  await page.getByRole("button", { name: "Archivieren" }).click();
  check((await page.locator("details .ask").count()) === 1, "archiving asks first");
  await page.getByRole("button", { name: "Ja, archivieren" }).click();
  check((await calls(page)).some((c) => c.entry_id === "contract-5" && c.action === "archive_contract"), "archive is sent for the expired contract");

  // everything archived: the other tabs say so instead of breaking
  await page.evaluate(() => {
    const panel = window.__panel;
    panel._contracts = panel._contracts.map((c) => ({ ...c, archiviert: true }));
    panel._tab = "overview";
    panel._render();
  });
  check((await wrapText()).includes("Alle Verträge sind archiviert"), "all archived: the overview says so");
  await tab("Kosten");
  check((await wrapText()).includes("Alle Verträge sind archiviert"), "all archived: the costs say so");
  await tab("Historie");
  check((await page.locator(".hist").count()) >= 1, "all archived: the History tab still works");
  await context.close();
}

{ // history for everyone who can see the panel, but only administrators get buttons
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  page.on("pageerror", (e) => errors.push(`history/non-admin: ${e.message}`));
  await page.clock.setFixedTime("2026-07-12T12:00:00Z");
  await page.goto(`${base}?lang=de&admin=0`);
  await page.waitForFunction(() => window.__panel && window.__panel.shadowRoot.querySelector(".card"));
  await page.getByRole("tab", { name: "Historie", exact: true }).click();
  check((await page.locator(".hist").count()) >= 2 && (await page.locator(".hist .btn").count()) === 0, "non-administrators see the history without buttons");
  check((await page.getByRole("button", { name: /Alten Vertrag hinzufügen|Laufzeit bearbeiten/ }).count()) === 0, "and without the buttons for old contracts");
  await context.close();
}

{ // an empty history says what it is for
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  page.on("pageerror", (e) => errors.push(`history/empty: ${e.message}`));
  await page.clock.setFixedTime("2026-07-12T12:00:00Z");
  await page.goto(`${base}?lang=de`);
  await page.waitForFunction(() => window.__panel && window.__panel.shadowRoot.querySelector(".card"));
  await page.evaluate(() => {
    const panel = window.__panel;
    panel._contracts = panel._contracts.filter((c) => !c.archiviert).map((c) => ({ ...c, historie: [] }));
    panel._tab = "history";
    panel._render();
  });
  const text = await page.evaluate(() => window.__panel.shadowRoot.querySelector(".wrap").innerText);
  check(text.includes("Noch keine Historie") && text.includes("früheren Laufzeiten"), "an empty history explains itself");
  await context.close();
}

{ // old contracts: a term entered by hand, worked out automatically where possible
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  page.on("pageerror", (e) => errors.push(`term: ${e.message}`));
  await page.clock.setFixedTime("2026-07-12T12:00:00Z");
  await page.goto(`${base}?lang=de`);
  await page.waitForFunction(() => window.__panel && window.__panel.shadowRoot.querySelector(".card"));
  await page.getByRole("tab", { name: "Historie", exact: true }).click();
  const dialogText = async () => (await page.locator(".dialog").innerText()).replace(/\u00a0/g, " ");
  const field = (name) => page.locator(`.dialog [name=${name}]`);
  const enter = async (name, value) => { await field(name).fill(value); await field(name).blur(); };
  const termCalls = async () => (await calls(page)).filter((c) => String(c.type).startsWith("tariffy/history_") && c.type !== "tariffy/history_calc");

  await page.getByRole("button", { name: "Alten Vertrag hinzufügen" }).click();
  check((await dialogText()).includes("Alten Vertrag hinzufügen"), "the dialog for an old contract opens");
  check((await field("entry_id").inputValue()) === "contract-1", "the first contract is preselected");
  // the list of a drop-down must be readable in the dark layout: dark background, light text (not the browser's white list)
  const option = await field("entry_id").locator("option").first().evaluate((el) => {
    const style = getComputedStyle(el);
    return { background: style.backgroundColor, color: style.color, scheme: getComputedStyle(el.parentElement).colorScheme };
  });
  check(option.background === "rgb(26, 29, 37)" && option.color === "rgb(243, 245, 249)" && option.scheme === "dark",
    `the options of a drop-down have dark colours (${JSON.stringify(option)})`);

  // nothing can be worked out without the term
  await page.getByRole("button", { name: "Speichern" }).click();
  check((await dialogText()).includes("Pflichtfeld") && (await termCalls()).length === 0, "start and end are required, nothing is sent");

  await enter("beginn", "2024-01-01");
  await enter("ende", "2024-12-31");
  check((await field("verbrauch").getAttribute("placeholder")) === "3.200,00", `the consumption is worked out from the statistics (${await field("verbrauch").getAttribute("placeholder")})`);
  check((await dialogText()).includes("Automatisch aus den Statistiken von sensor.strom_haus"), "and the dialog says where it comes from");
  check((await field("kosten").getAttribute("placeholder")) === "", "the cost needs prices first");

  await enter("arbeitspreis", "0,30");
  await enter("grundpreis", "10");
  await enter("abschlag", "90");
  check((await field("kosten").getAttribute("placeholder")) === "1.079,90", `the cost follows from the prices (${await field("kosten").getAttribute("placeholder")})`);
  check((await field("abschlag_gezahlt").getAttribute("placeholder")) === "1.079,10", "and the instalments paid from the instalment");
  check((await field("saldo").getAttribute("placeholder")) === "−0,80" || (await field("saldo").getAttribute("placeholder")) === "-0,80", "and the balance from both");

  // a value typed by hand wins and the rest follows from it
  await enter("verbrauch", "3000");
  check((await dialogText()).includes("Von dir eingetragen"), "a typed value is marked as the user's own");
  check((await field("kosten").getAttribute("placeholder")) === "1.019,90", `the cost follows the typed consumption (${await field("kosten").getAttribute("placeholder")})`);
  await dialog(page).screenshot({ path: join(outDir, "term-dialog.png") });

  await page.getByRole("button", { name: "Speichern" }).click();
  await page.waitForFunction(() => !window.__panel.shadowRoot.querySelector(".dialog"));
  const saved = (await termCalls()).at(-1);
  check(saved.type === "tariffy/history_save" && saved.entry_id === "contract-1" && saved.index === undefined, "a new term is saved for the contract");
  check(JSON.stringify(saved.values) === JSON.stringify({ beginn: "2024-01-01", ende: "2024-12-31", arbeitspreis: 0.3, grundpreis: 10, abschlag: 90, verbrauch: 3000 }),
    `only what was entered is sent, the rest is left to the backend (${JSON.stringify(saved.values)})`);

  // editing: the newest term is the first row; the stored list is oldest first, so it is index 1
  await page.locator(".hist[data-id=contract-1] tbody tr").first().getByRole("button", { name: "Laufzeit bearbeiten" }).click();
  check((await dialogText()).includes("Laufzeit bearbeiten") && (await field("beginn").inputValue()) === "2025-01-01", "editing opens the term with its values");
  check(await field("entry_id").isDisabled(), "a term stays with its contract");
  await enter("tarif", "Neu");
  await page.getByRole("button", { name: "Speichern" }).click();
  await page.waitForFunction(() => !window.__panel.shadowRoot.querySelector(".dialog"));
  const edited = (await termCalls()).at(-1);
  check(edited.type === "tariffy/history_save" && edited.index === 1 && edited.values.tarif === "Neu", "an edited term is saved at its position");

  // deleting asks first
  await page.locator(".hist[data-id=contract-1] tbody tr").first().getByRole("button", { name: "Laufzeit bearbeiten" }).click();
  const before = (await termCalls()).length;
  await page.getByRole("button", { name: "Laufzeit löschen" }).click();
  check((await dialogText()).includes("Diese Laufzeit aus der Historie löschen?") && (await termCalls()).length === before, "deleting a term asks first");
  await page.getByRole("button", { name: "Ja, löschen" }).click();
  await page.waitForFunction(() => !window.__panel.shadowRoot.querySelector(".dialog"));
  const deleted = (await termCalls()).at(-1);
  check(deleted.type === "tariffy/history_delete" && deleted.entry_id === "contract-1" && deleted.index === 1, "the term is deleted");

  // escape closes the dialog without saving
  await page.getByRole("button", { name: "Alten Vertrag hinzufügen" }).click();
  const callsBefore = (await termCalls()).length;
  await page.keyboard.press("Escape");
  check((await page.locator(".dialog").count()) === 0 && (await termCalls()).length === callsBefore, "escape closes the dialog and sends nothing");
  await context.close();
}

{ // a refused term shows why and keeps the dialog open
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  page.on("pageerror", (e) => errors.push(`term/error: ${e.message}`));
  await page.clock.setFixedTime("2026-07-12T12:00:00Z");
  await page.goto(`${base}?lang=de&histerr=1`);
  await page.waitForFunction(() => window.__panel && window.__panel.shadowRoot.querySelector(".card"));
  await page.getByRole("tab", { name: "Historie", exact: true }).click();
  await page.getByRole("button", { name: "Alten Vertrag hinzufügen" }).click();
  await page.locator(".dialog [name=beginn]").fill("2024-12-31");
  await page.locator(".dialog [name=ende]").fill("2024-01-01");
  await page.getByRole("button", { name: "Speichern" }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".dialog .err"));
  check((await page.locator(".dialog .err").innerText()).includes("Das Ende darf nicht vor dem Beginn liegen."), "the reason is shown");
  check(await page.getByRole("button", { name: "Speichern" }).isEnabled(), "and the dialog can be corrected and saved again");
  await context.close();
}

{ // backup: export, restore from a file, deleted contracts
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1, acceptDownloads: true });
  const page = await context.newPage();
  page.on("pageerror", (e) => errors.push(`backup: ${e.message}`));
  await page.clock.setFixedTime("2026-07-12T12:00:00Z");
  await page.goto(`${base}?lang=de`);
  await page.waitForFunction(() => window.__panel && window.__panel.shadowRoot.querySelector(".card"));
  const wrapText = () => page.evaluate(() => window.__panel.shadowRoot.querySelector(".wrap").innerText.replace(/\u00a0/g, " "));
  const bkCalls = async () => (await calls(page)).filter((c) => /backup_|deleted_/.test(String(c.type)) && c.type !== "tariffy/deleted_list" && c.type !== "tariffy/backup_preview");
  await page.getByRole("tab", { name: "Sicherung", exact: true }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".bk-row"));
  let text = await wrapText();
  check(/sicherung erstellen/i.test(text) && text.includes("persönliche Daten"), "the backup tab explains that the file has personal data");
  check(text.includes("Strom 2023") && text.includes("gelöscht am 01.07.2026"), "a deleted contract is listed with its date");

  // export: a file download with all contracts
  const [download] = await Promise.all([page.waitForEvent("download"), page.getByRole("button", { name: "Sicherung herunterladen" }).click()]);
  check(/^tariffy-backup-\d{4}-\d{2}-\d{2}\.json$/.test(download.suggestedFilename()), `the file has a dated name (${download.suggestedFilename()})`);
  const { readFile } = await import("node:fs/promises");
  const saved = JSON.parse(await readFile(await download.path(), "utf8"));
  check(saved.tariffy_backup === 1 && saved.contracts.length === 1, "the downloaded file is the backup");
  check((await wrapText()).includes("Sicherung heruntergeladen: 1 Verträge."), "and the panel says so");
  const exported = (await bkCalls()).length; // the export itself is a call; what follows must not add any until confirmed

  // restore: a preview first, then asking, then only the missing contracts are created
  const file = { tariffy_backup: 1, contracts: [
    { title: "Strom Alt", data: { sparte: "electricity" }, options: {} }, { title: "Gas Alt", data: { sparte: "gas" }, options: {} } ] };
  await page.locator(".bk .file").setInputFiles({ name: "backup.json", mimeType: "application/json", buffer: Buffer.from(JSON.stringify(file)) });
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".bk table"));
  text = await wrapText();
  check(text.includes("Strom Alt") && text.includes("wird angelegt") && text.includes("übersprungen: gibt es schon"), "the preview says what is created and what is skipped");
  check((await bkCalls()).length === exported, "a preview creates nothing");
  await page.getByRole("button", { name: "Wiederherstellen (1)" }).click();
  check((await page.locator(".bk .ask").count()) === 1 && (await bkCalls()).length === exported, "restoring asks first");
  await page.getByRole("button", { name: "Abbrechen" }).click();
  check((await bkCalls()).length === exported, "cancelling does nothing");
  await page.getByRole("button", { name: "Wiederherstellen (1)" }).click();
  await page.getByRole("button", { name: "Ja, wiederherstellen" }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".bk-msg"));
  const restoreCall = (await bkCalls()).at(-1);
  check(restoreCall.type === "tariffy/backup_restore" && restoreCall.backup.contracts.length === 2, "the whole file is sent for restoring");
  check((await wrapText()).includes("Wiederhergestellt: 1 angelegt, 1 übersprungen."), "the result is shown");
  check((await page.locator(".bk table").count()) === 0, "and the preview is gone");

  // a file that is not a backup
  await page.locator(".bk .file").setInputFiles({ name: "x.json", mimeType: "application/json", buffer: Buffer.from("das ist kein json") });
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".err"));
  check((await page.locator(".err").innerText()).includes("keine gültige Tariffy-Sicherung"), "a file that is no backup is refused with a reason");

  // forgetting a deleted contract asks first, too
  const beforeDiscard = (await bkCalls()).length;
  await page.getByRole("button", { name: "Jetzt vergessen" }).click();
  check((await page.locator(".bk-row .ask").count()) === 1 && (await bkCalls()).length === beforeDiscard, "forgetting a deleted contract asks first");
  await page.getByRole("button", { name: "Ja, vergessen" }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".bk-msg")?.innerText.includes("vergessen"));
  const discarded = (await bkCalls()).at(-1);
  check(discarded.type === "tariffy/deleted_discard" && discarded.item_id === "d1", "it is forgotten for good");

  // deleted contracts: asks first
  const before = (await bkCalls()).length;
  await page.getByRole("button", { name: "Zurückholen" }).click();
  check((await page.locator(".bk-row .ask").count()) === 1 && (await bkCalls()).length === before, "bringing a contract back asks first");
  await page.getByRole("button", { name: "Ja, zurückholen" }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".bk-msg"));
  const restoreOne = (await bkCalls()).at(-1);
  check(restoreOne.type === "tariffy/deleted_restore" && restoreOne.item_id === "d1", "the deleted contract is brought back");
  check((await wrapText()).includes("„Strom 2023“ ist wieder da."), "and the panel says so");
  await page.screenshot({ path: join(outDir, "desktop-backup-actions.png"), fullPage: true });
  await context.close();
}

{ // the backup tab belongs to administrators
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  page.on("pageerror", (e) => errors.push(`backup/non-admin: ${e.message}`));
  await page.clock.setFixedTime("2026-07-12T12:00:00Z");
  await page.addInitScript(() => window.localStorage.setItem("tariffy-panel-tab", "backup"));
  await page.goto(`${base}?lang=de&admin=0`);
  await page.waitForFunction(() => window.__panel && window.__panel.shadowRoot.querySelector(".tabs"));
  check((await page.getByRole("tab", { name: "Sicherung", exact: true }).count()) === 0, "non-administrators have no backup tab");
  check((await page.locator(".bk").count()) === 0 && (await page.locator(".card").count()) > 0, "and a saved backup tab does not trap them: they get the overview");
  await context.close();
}

{ // a refused restore says why
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  page.on("pageerror", (e) => errors.push(`backup/error: ${e.message}`));
  await page.clock.setFixedTime("2026-07-12T12:00:00Z");
  await page.goto(`${base}?lang=de&bkerr=1`);
  await page.waitForFunction(() => window.__panel && window.__panel.shadowRoot.querySelector(".card"));
  await page.getByRole("tab", { name: "Sicherung", exact: true }).click();
  const file = { tariffy_backup: 1, contracts: [{ title: "Strom Alt", data: { sparte: "electricity" }, options: {} }] };
  await page.locator(".bk .file").setInputFiles({ name: "backup.json", mimeType: "application/json", buffer: Buffer.from(JSON.stringify(file)) });
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".bk table"));
  await page.getByRole("button", { name: "Wiederherstellen (1)" }).click();
  await page.getByRole("button", { name: "Ja, wiederherstellen" }).click();
  await page.waitForFunction(() => window.__panel.shadowRoot.querySelector(".err"));
  check((await page.locator(".err").innerText()).includes("Das Wiederherstellen ist fehlgeschlagen."), "a failed restore shows its reason");
  await context.close();
}

{ // flat-rate contracts show yearly values; the payment interval shows when it is not monthly
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  page.on("pageerror", (e) => errors.push(`yearly: ${e.message}`));
  await page.clock.setFixedTime("2026-07-12T12:00:00Z");
  await page.goto(`${base}?lang=de`);
  await page.waitForFunction(() => window.__panel && window.__panel.shadowRoot.querySelector(".card"));
  const text = async (sel) => (await page.locator(sel).first().innerText()).replace(/\u00a0/g, " ");
  const internet = await text("section.card:has-text('Internet')");
  check(internet.includes("480 € / Jahr") && !internet.includes("jährlich"), `a monthly flat-rate card shows the yearly instalment (${internet.replace(/\n/g, " | ")})`);

  // a yearly premium: 600 a year is 50 a month
  await page.evaluate(() => {
    const panel = window.__panel;
    panel._contracts = panel._contracts.map((c) => (c.title === "Internet"
      ? { ...c, abschlag: 50, zahlweise: "yearly", abschlag_je_zahlung: 600, abschlag_jahr: 600, kosten_jahr: 600 } : c));
    panel._render();
  });
  const yearly = await text("section.card:has-text('Internet')");
  check(yearly.includes("600,00 € jährlich"), `the card says how it is paid (${yearly.replace(/\n/g, " | ")})`);
  check(!yearly.includes("600 € / Jahr"), "and does not repeat the yearly figure");
  await page.getByRole("tab", { name: "Verträge", exact: true }).click();
  await page.locator("details", { hasText: "Internet" }).first().locator("summary").click();
  const details = await text("details:has-text('Internet')");
  check(details.includes("Abschlag / Jahr") && details.includes("Kosten / Jahr") && details.includes("Zahlung"), "the details show the yearly instalment, the yearly cost and the payment");
  check(/Zahlung\s*600,00 € jährlich/.test(details), `the payment row says the amount and the interval (${details.replace(/\n/g, " | ")})`);
  await page.getByRole("tab", { name: "Kosten", exact: true }).click();
  check((await text("tr:has-text('Internet')")).includes("600 € / Jahr"), "the cost table shows the yearly instalment");

  // the base price counts for the yearly cost, not for the yearly instalment
  await page.evaluate(() => {
    const panel = window.__panel;
    panel._contracts = panel._contracts.map((c) => (c.title === "Mobilfunk" ? { ...c, grundpreis: 5, kosten_jahr: 299.88 } : c));
    panel._tab = "contracts";
    panel._render();
  });
  await page.locator("details", { hasText: "Mobilfunk" }).first().locator("summary").click();
  const mobile = await text("details:has-text('Mobilfunk')");
  check(/Abschlag \/ Jahr\s*239,88 €/.test(mobile) && /Kosten \/ Jahr\s*299,88 €/.test(mobile), `yearly cost includes the base price, the yearly instalment does not (${mobile.replace(/\n/g, " | ")})`);
  await context.close();
}

await browser.close();
server.close();
if (errors.length) { console.error("Browser errors:\n" + errors.join("\n")); process.exit(1); }
console.log("screenshots written to", outDir);
