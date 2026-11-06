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

  check((await page.locator(".actions").count()) === 2, "only the two contracts with something to acknowledge show buttons on the card");
  check((await page.getByRole("button", { name: "Weitere Aktionen" }).count()) === 6, "every card has a menu for the less frequent actions");
  check((await card(page, "Strom Haus").getByRole("button", { name: "Warnung bestätigen" }).count()) === 1, "warning button on Strom Haus");
  check((await card(page, "Internet").getByRole("button", { name: "Kündigung bestätigen" }).count()) === 1, "cancellation button on Internet");
  const menuItems = async (name) => {
    await card(page, name).getByRole("button", { name: "Weitere Aktionen" }).click();
    const items = await card(page, name).getByRole("menuitem").allInnerTexts();
    await page.keyboard.press("Escape");
    return items.join();
  };
  check((await menuItems("Mobilfunk")) === "Folgevertrag bearbeiten,Vertrag bearbeiten", "Mobilfunk can edit its planned contract");
  check((await menuItems("Gas Heizung")) === "Folgevertrag planen,Vertrag bearbeiten", "Gas offers to plan the next contract and to edit itself");
  check((await page.getByRole("menuitem").count()) === 0, "Escape closes the menu");
  await card(page, "Internet").getByRole("button", { name: "Weitere Aktionen" }).click();
  check((await page.getByRole("menuitem").count()) === 2, "the menu opens");
  await page.locator(".top .brand").click();
  check((await page.getByRole("menuitem").count()) === 0, "a click outside closes the menu");

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

  // switching is not offered in the panel (the contract switches itself on its start date)
  check((await page.getByRole("button", { name: "Jetzt wechseln" }).count()) === 0, "no switch button in the panel");

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
  const sent = (await calls(page)).map((c) => `${c.entry_id}:${c.action}`);
  check(sent.join(",") === "contract-5:confirm_cancellation,contract-1:confirm_abschlag_warning", `acknowledgements sent: ${sent}`);
  await context.close();
}

// ---- plan the next contract: the options flow of Home Assistant rendered in a dialog ----
const flowPath = "config/config_entries/options/flow";
const api = (page) => page.evaluate(() => window.__api);
const dialog = (page) => page.locator(".dialog");
// plan/edit live behind the "..." menu of a card on wide screens
const MENU_ITEMS = new Set(["Folgevertrag planen", "Folgevertrag bearbeiten", "Vertrag bearbeiten", "Plan next contract", "Edit next contract", "Edit contract"]);
async function openDialog(page, name, button) {
  if (MENU_ITEMS.has(button)) {
    await card(page, name).getByRole("button", { name: /Weitere Aktionen|More actions/ }).click();
    await card(page, name).getByRole("menuitem", { name: button }).click();
  } else {
    await card(page, name).getByRole("button", { name: button }).click();
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
  check((await page.getByRole("button", { name: "Neuer Vertrag" }).count()) === 0, "and get no button for a new contract");
  await context.close();
}

{ // phone: buttons are inside the expanded card
  const context = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  const page = await context.newPage();
  await page.clock.setFixedTime("2026-07-12T12:00:00Z");
  await page.goto(`${base}?lang=de&narrow=1`);
  await page.waitForFunction(() => window.__panel && window.__panel._compact === true);
  check((await page.locator(".btn").count()) === 15, "phone: all buttons are in the page");
  check((await page.getByRole("button", { name: "Neuer Vertrag" }).isVisible()), "phone: the button for a new contract is in the top bar");
  check(!(await page.locator(".card .btn").first().isVisible()), "phone: buttons stay hidden until the row is expanded");
  await page.locator("details.card", { hasText: "Internet" }).locator("summary").click();
  check(await page.locator("details.card", { hasText: "Internet" }).getByRole("button", { name: "Kündigung bestätigen" }).isVisible(), "phone: button visible after expanding");
  await context.close();
}

await browser.close();
server.close();
if (errors.length) { console.error("Browser errors:\n" + errors.join("\n")); process.exit(1); }
console.log("screenshots written to", outDir);
