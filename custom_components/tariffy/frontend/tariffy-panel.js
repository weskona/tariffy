/* Tariffy panel (beta).
 *
 * Read-only overview of all contracts, fed by the integration's websocket API
 * (tariffy/subscribe). Plain web component, no build step, system font.
 *
 * Security: text that comes from the user (contract names, providers, tariffs)
 * is only ever written with textContent / text nodes, never as HTML.
 */

const I18N = {
  en: {
    overview: "Overview", costs: "Costs", contracts: "Contracts",
    beta: "Beta",
    loading: "Loading contracts …",
    error: "The panel could not load the contracts.",
    emptyTitle: "No contracts yet",
    emptyText: "Add a contract under Settings → Devices & services → Tariffy.",
    emptyLink: "Add a contract",
    monthlyTotal: "Instalments per month",
    forecastTotal: "Forecast at contract end",
    forecastSub: "{n} of {m} contracts with metering",
    nextDeadline: "Next date",
    nothingPlanned: "Nothing planned",
    inDays: "in {n} days", today: "today", tomorrow: "tomorrow",
    credit: "Credit", balanceDue: "Balance due",
    cancelDue: "Cancel now", warning: "Balance due likely",
    switchOn: "Switch on {d}",
    endForecast: "Credit / balance due at contract end",
    endTotal: "Instalments over the contract term",
    term: "Term",
    costSoFar: "Cost so far", balanceSoFar: "Credit / balance due so far",
    consumption: "Consumption", projected: "projected {v}",
    remaining: "Remaining", daysLeft: "{n} days", until: "until {d}",
    instalment: "Instalment / month", contractEnd: "Contract end",
    reminder: "Reminder", reminderOff: "Off",
    paid: "Instalments paid", cost: "Cost",
    noteWarning: "At the current usage a balance due of about {v} is expected. Adjust the instalment to about {a} per month.",
    noteWarningShort: "At the current usage a balance due of about {v} is expected.",
    noteCancel: "The cancellation period is running, the contract ends on {d}.",
    noteNext: "Next contract from {d}: {name}",
    colContract: "Contract", colCost: "Cost so far", colBalance: "Balance so far",
    colForecast: "At contract end", colInstalment: "Instalment", colRecommended: "Recommended",
    total: "Total", highTariff: "High tariff", lowTariff: "Low tariff",
    costsHint: "Positive = credit, negative = balance due. “At contract end” is projected from the consumption so far.",
    secContract: "Contract", secPrices: "Prices", secConsumption: "Consumption",
    secAdvice: "Recommendations", secNext: "Next contract",
    provider: "Provider", tariff: "Tariff", start: "Start", end: "End",
    unitPrice: "Unit price", unitPriceLow: "Unit price low tariff", unitPriceNight: "Unit price night",
    unitPriceEff: "Unit price effective", unitPriceWater: "Water price incl. wastewater",
    basePrice: "Base price", perMonth: "/ month",
    soFar: "So far", soFarHigh: "So far, high tariff", soFarLow: "So far, low tariff",
    projectedTerm: "Projected for the term", lastPeriod: "Last period",
    recommended: "Recommended instalment", adjustment: "Instalment adjustment",
    reminderDate: "Reminder from", reminderActive: "Active", reminderDone: "Acknowledged",
    nextStart: "Start", nextEnd: "End", nextProvider: "Provider", nextTariff: "Tariff",
    nextPrice: "Unit price", nextInstalment: "Instalment",
    months: "{n} months", yes: "yes", no: "no",
    actConfirmWarning: "Acknowledge warning", actConfirmCancel: "Acknowledge cancellation",
    actYesAck: "Yes, acknowledge", actCancel: "Cancel",
    actAskWarning: "Acknowledge the instalment warning? It will not be shown again for this contract unless the forecast recovers first.",
    actAskCancel: "Acknowledge the cancellation reminder? The reminder is dismissed for this contract.", actFailed: "Action failed: {m}",
    actNextPlan: "Plan next contract", actNextEdit: "Edit next contract", actEdit: "Edit contract", actNew: "New contract",
    dlgTitleCreate: "New contract", dlgCreated: "The contract was created.",
    dlgDelete: "Delete contract", dlgDeleteYes: "Delete for good", dlgDeleted: "The contract was deleted.",
    dlgDeleteAsk: "Delete the contract \"{name}\" for good? This cannot be undone. Type its name to confirm.",
    dlgDeleteNote: "Its sensors and buttons are removed. The long-term statistics Home Assistant already recorded stay in its database.",
    dlgDeleteFailed: "Deleting failed: {m}",
    dlgTitleEdit: "Edit contract · {name}", dlgContinue: "Next",
    dlgSaveAsk: "Save the changes? The contract data is replaced with what the form shows.", dlgSaveYes: "Yes, save",
    dlgTitle: "Next contract · {name}", dlgLoading: "Loading the form …", dlgSave: "Save", dlgClose: "Close",
    dlgSaving: "Saving …", dlgSaved: "Saved. Home Assistant reloads the contract.",
    dlgMarkDone: "Mark the cancellation as done",
    dlgMarkDoneFailed: "Saved, but the cancellation could not be marked as done. Please use \"Acknowledge cancellation\".",
    dlgRemove: "Remove planned contract", dlgRemoveAsk: "Remove the planned next contract? The current contract stays as it is.",
    dlgRemoveYes: "Yes, remove", dlgRemoved: "The planned contract was removed.",
    dlgInvalidNumber: "Not a valid number (zero or more, decimal comma or point).", dlgRequired: "Required",
    dlgLoadFailed: "The form could not be loaded: {m}", dlgSaveFailed: "Saving failed: {m}",
    dlgAborted: "Home Assistant ended the form: {m}",
    dlgUnsupported: "This form has fields the panel cannot show yet. Please use the setup of Home Assistant.",
    coveredHint: "Credit covers the costs",
    sparte: {
      electricity: "Electricity", electricity_ht_nt: "Electricity HT/NT", gas: "Gas",
      water: "Water", internet: "Internet", mobile: "Mobile", insurance: "Insurance", other: "Other",
    },
  },
  de: {
    overview: "Übersicht", costs: "Kosten", contracts: "Verträge",
    beta: "Beta",
    loading: "Verträge werden geladen …",
    error: "Das Panel konnte die Verträge nicht laden.",
    emptyTitle: "Noch keine Verträge",
    emptyText: "Lege einen Vertrag unter Einstellungen → Geräte & Dienste → Tariffy an.",
    emptyLink: "Vertrag anlegen",
    monthlyTotal: "Abschläge pro Monat",
    forecastTotal: "Prognose zum Vertragsende",
    forecastSub: "{n} von {m} Verträgen mit Verbrauchsmessung",
    nextDeadline: "Nächster Termin",
    nothingPlanned: "Nichts geplant",
    inDays: "in {n} Tagen", today: "heute", tomorrow: "morgen",
    credit: "Guthaben", balanceDue: "Nachzahlung",
    cancelDue: "Jetzt kündigen", warning: "Nachzahlung droht",
    switchOn: "Wechsel am {d}",
    endForecast: "Guthaben / Nachzahlung zum Vertragsende",
    endTotal: "Abschläge über die Laufzeit",
    term: "Laufzeit",
    costSoFar: "Kosten bisher", balanceSoFar: "Guthaben / Nachzahlung bisher",
    consumption: "Verbrauch", projected: "hochgerechnet {v}",
    remaining: "Restlaufzeit", daysLeft: "{n} Tage", until: "bis {d}",
    instalment: "Abschlag / Monat", contractEnd: "Vertragsende",
    reminder: "Erinnerung", reminderOff: "Aus",
    paid: "Abschläge gezahlt", cost: "Kosten",
    noteWarning: "Beim aktuellen Verbrauch ist eine Nachzahlung von etwa {v} zu erwarten. Abschlag auf etwa {a} pro Monat anpassen.",
    noteWarningShort: "Beim aktuellen Verbrauch ist eine Nachzahlung von etwa {v} zu erwarten.",
    noteCancel: "Die Kündigungsfrist läuft, der Vertrag endet am {d}.",
    noteNext: "Folgevertrag ab {d}: {name}",
    colContract: "Vertrag", colCost: "Kosten bisher", colBalance: "Saldo bisher",
    colForecast: "Zum Vertragsende", colInstalment: "Abschlag", colRecommended: "Empfohlen",
    total: "Summe", highTariff: "Hochtarif", lowTariff: "Niedertarif",
    costsHint: "Positiv = Guthaben, negativ = Nachzahlung. „Zum Vertragsende“ ist aus dem bisherigen Verbrauch hochgerechnet.",
    secContract: "Vertrag", secPrices: "Preise", secConsumption: "Verbrauch",
    secAdvice: "Empfehlungen", secNext: "Folgevertrag",
    provider: "Anbieter", tariff: "Tarif", start: "Beginn", end: "Ende",
    unitPrice: "Arbeitspreis", unitPriceLow: "Arbeitspreis Niedertarif", unitPriceNight: "Arbeitspreis Nacht",
    unitPriceEff: "Arbeitspreis effektiv", unitPriceWater: "Wasserpreis inkl. Abwasser",
    basePrice: "Grundpreis", perMonth: "/ Monat",
    soFar: "Bisher", soFarHigh: "Bisher, Hochtarif", soFarLow: "Bisher, Niedertarif",
    projectedTerm: "Hochgerechnet auf die Laufzeit", lastPeriod: "Letzte Laufzeit",
    recommended: "Empfohlener Abschlag", adjustment: "Abschlag-Anpassung",
    reminderDate: "Erinnerung ab", reminderActive: "Aktiv", reminderDone: "Bestätigt",
    nextStart: "Beginn", nextEnd: "Ende", nextProvider: "Anbieter", nextTariff: "Tarif",
    nextPrice: "Arbeitspreis", nextInstalment: "Abschlag",
    months: "{n} Monate", yes: "ja", no: "nein",
    actConfirmWarning: "Warnung bestätigen", actConfirmCancel: "Kündigung bestätigen",
   
    actYesAck: "Ja, bestätigen", actCancel: "Abbrechen",
    actAskWarning: "Abschlag-Warnung bestätigen? Sie wird für diesen Vertrag erst wieder gemeldet, wenn sich die Prognose zwischendurch erholt hat.",
    actAskCancel: "Kündigungs-Erinnerung bestätigen? Die Erinnerung wird für diesen Vertrag ausgeblendet.", actFailed: "Aktion fehlgeschlagen: {m}",
    actNextPlan: "Folgevertrag planen", actNextEdit: "Folgevertrag bearbeiten", actEdit: "Vertrag bearbeiten", actNew: "Neuer Vertrag",
    dlgTitleCreate: "Neuer Vertrag", dlgCreated: "Der Vertrag wurde angelegt.",
    dlgDelete: "Vertrag löschen", dlgDeleteYes: "Endgültig löschen", dlgDeleted: "Der Vertrag wurde gelöscht.",
    dlgDeleteAsk: "Den Vertrag \"{name}\" endgültig löschen? Das lässt sich nicht rückgängig machen. Zur Bestätigung den Namen eintippen.",
    dlgDeleteNote: "Seine Sensoren und Buttons werden entfernt. Die Langzeit-Statistiken, die Home Assistant schon aufgezeichnet hat, bleiben in der Datenbank.",
    dlgDeleteFailed: "Löschen fehlgeschlagen: {m}",
    dlgTitleEdit: "Vertrag bearbeiten · {name}", dlgContinue: "Weiter",
    dlgSaveAsk: "Änderungen speichern? Die Vertragsdaten werden durch das ersetzt, was das Formular zeigt.", dlgSaveYes: "Ja, speichern",
    dlgTitle: "Folgevertrag · {name}", dlgLoading: "Formular wird geladen …", dlgSave: "Speichern", dlgClose: "Schließen",
    dlgSaving: "Wird gespeichert …", dlgSaved: "Gespeichert. Home Assistant lädt den Vertrag neu.",
    dlgMarkDone: "Kündigung als erledigt markieren",
    dlgMarkDoneFailed: "Gespeichert, aber die Kündigung konnte nicht als erledigt markiert werden. Bitte \"Kündigung bestätigen\" benutzen.",
    dlgRemove: "Geplanten Vertrag entfernen", dlgRemoveAsk: "Den geplanten Folgevertrag entfernen? Der aktuelle Vertrag bleibt unverändert.",
    dlgRemoveYes: "Ja, entfernen", dlgRemoved: "Der geplante Vertrag wurde entfernt.",
    dlgInvalidNumber: "Keine gültige Zahl (null oder größer, Komma oder Punkt).", dlgRequired: "Pflichtfeld",
    dlgLoadFailed: "Das Formular konnte nicht geladen werden: {m}", dlgSaveFailed: "Speichern fehlgeschlagen: {m}",
    dlgAborted: "Home Assistant hat das Formular beendet: {m}",
    dlgUnsupported: "Dieses Formular enthält Felder, die das Panel noch nicht anzeigen kann. Bitte die Einrichtung von Home Assistant benutzen.",
    coveredHint: "Guthaben deckt die Kosten",
    sparte: {
      electricity: "Strom", electricity_ht_nt: "Strom HT/NT", gas: "Gas",
      water: "Wasser", internet: "Internet", mobile: "Mobilfunk", insurance: "Versicherung", other: "Sonstiges",
    },
  },
};

const SVG_NS = "http://www.w3.org/2000/svg";
const TABS = ["overview", "costs", "contracts"];
const TAB_KEY = "tariffy-panel-tab";

/* Simple outline icons per contract type (24x24, stroke). */
const ICONS = {
  electricity: [["path", { d: "M13 2 4 14h7l-1 8 9-12h-7z" }]],
  electricity_ht_nt: [["path", { d: "M13 2 4 14h7l-1 8 9-12h-7z" }]],
  gas: [["path", { d: "M12 2c.5 4 5 6 5 11a5 5 0 0 1-10 0c0-2 1-3.500 2-4.500.2 2 1 3 2 3 .5-3-1-5 1-9.500z" }]],
  water: [["path", { d: "M12 2s6.500 7 6.500 12a6.500 6.500 0 0 1-13 0C5.500 9 12 2 12 2z" }]],
  internet: [
    ["path", { d: "M2.500 9a14 14 0 0 1 19 0" }],
    ["path", { d: "M5.500 12.500a9.500 9.500 0 0 1 13 0" }],
    ["path", { d: "M8.600 16a5 5 0 0 1 6.800 0" }],
    ["circle", { cx: "12", cy: "19.500", r: "1", fill: "currentColor" }],
  ],
  mobile: [
    ["rect", { x: "7", y: "2.500", width: "10", height: "19", rx: "2.500" }],
    ["path", { d: "M11 18.500h2" }],
  ],
  insurance: [["path", { d: "M12 2.500 20 5.500v6c0 5-3.500 8.500-8 10.500-4.500-2-8-5.500-8-10.500v-6z" }]],
  other: [
    ["circle", { cx: "6", cy: "12", r: "1.600", fill: "currentColor" }],
    ["circle", { cx: "12", cy: "12", r: "1.600", fill: "currentColor" }],
    ["circle", { cx: "18", cy: "12", r: "1.600", fill: "currentColor" }],
  ],
};

const STYLE = `
:host {
  --bg: #0b0d12; --panel: #14171e; --panel2: #11141a;
  --tile: rgba(255,255,255,.032); --tile-line: rgba(255,255,255,.07); --line: rgba(255,255,255,.065);
  --text: #f3f5f9; --muted: #8b91a1; --dim: #5d6373;
  --green: #34d399; --red: #f87171; --orange: #fb923c; --blue: #60a5fa; --gold: #f7b733;
  display: block; min-height: 100%; box-sizing: border-box;
  background: var(--bg); color: var(--text);
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  container-type: inline-size;
}
* { box-sizing: border-box; }
.wrap { max-width: 1280px; margin: 0 auto; padding: 16px 20px 40px; }
.top { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 18px; }
.brand { display: flex; align-items: center; gap: 10px; font-size: 20px; font-weight: 700; letter-spacing: .02em; }
.pill { font-size: 10px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--gold);
  border: 1px solid rgba(247,183,51,.4); border-radius: 999px; padding: 2px 8px; }
.tabs { display: flex; gap: 2px; margin: 0 auto; padding: 4px; background: var(--panel2);
  border: 1px solid var(--line); border-radius: 12px; }
.tab { appearance: none; border: 0; background: transparent; color: var(--muted); font: inherit;
  font-size: 14px; font-weight: 600; padding: 8px 18px; border-radius: 9px; cursor: pointer; }
.tab:hover { color: var(--text); }
.tab[aria-selected="true"] { background: rgba(255,255,255,.09); color: var(--text); }
.tab:focus-visible, summary:focus-visible, a:focus-visible { outline: 2px solid var(--blue); outline-offset: 2px; }
.spacer { width: 90px; }

.summary { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 18px; }
.sum { background: var(--panel); border: 1px solid var(--line); border-radius: 16px; padding: 14px 18px; }
.label { font-size: 11px; font-weight: 600; letter-spacing: .09em; text-transform: uppercase; color: var(--muted); }
.sum .value { font-size: 26px; font-weight: 700; margin-top: 6px; font-variant-numeric: tabular-nums; }
.sum .sub { font-size: 12px; color: var(--muted); margin-top: 2px; }

.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 16px; align-items: start; }
.card { background: var(--panel); border: 1px solid var(--line); border-radius: 16px; padding: 18px; }
.card.alert { border-color: rgba(248,113,113,.35); background: linear-gradient(180deg, rgba(248,113,113,.06), var(--panel) 40%); }
.head { display: flex; align-items: flex-start; gap: 12px; }
.badge { flex: none; width: 40px; height: 40px; border-radius: 12px; display: grid; place-items: center;
  background: var(--tile); border: 1px solid var(--tile-line); color: var(--blue); }
.badge svg { width: 22px; height: 22px; fill: none; stroke: currentColor; stroke-width: 1.7; stroke-linecap: round; stroke-linejoin: round; }
.badge.gas { color: var(--orange); } .badge.water { color: #38bdf8; } .badge.electricity,
.badge.electricity_ht_nt { color: var(--gold); } .badge.internet { color: #a78bfa; } .badge.mobile { color: var(--green); }
.title { font-size: 17px; font-weight: 700; line-height: 1.2; }
.meta { font-size: 13px; color: var(--muted); margin-top: 2px; }
.who { min-width: 0; flex: 1; }
.chips { display: flex; flex-wrap: wrap; gap: 6px; justify-content: flex-end; }
.chip { font-size: 12px; font-weight: 700; padding: 4px 10px; border-radius: 999px; white-space: nowrap;
  background: rgba(255,255,255,.06); color: var(--muted); }
.chip.green { background: rgba(52,211,153,.14); color: var(--green); }
.chip.red { background: rgba(248,113,113,.14); color: var(--red); }
.chip.orange { background: rgba(251,146,60,.15); color: var(--orange); }
.chip.blue { background: rgba(96,165,250,.15); color: var(--blue); }

.hero { display: flex; align-items: center; gap: 18px; margin: 18px 0 14px; }
.ring { position: relative; flex: none; width: 96px; height: 96px; }
.ring svg { width: 96px; height: 96px; transform: rotate(-90deg); }
.ring .track { stroke: rgba(255,255,255,.08); } .ring .arc { stroke: var(--blue); stroke-linecap: round; }
.ring .center { position: absolute; inset: 0; display: grid; place-content: center; text-align: center; }
.ring .pct { font-size: 20px; font-weight: 700; font-variant-numeric: tabular-nums; }
.ring .pcap { font-size: 9px; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); }
.big { font-size: 34px; font-weight: 700; font-variant-numeric: tabular-nums; line-height: 1.1; margin-top: 4px; }
.green-t { color: var(--green); } .red-t { color: var(--red); } .muted-t { color: var(--muted); }
.note { font-size: 13px; color: var(--muted); margin-top: 6px; }
.actions { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
.btn { appearance: none; font: inherit; font-size: 13px; font-weight: 700; padding: 8px 14px; border-radius: 10px;
  border: 1px solid var(--tile-line); background: var(--tile); color: var(--text); cursor: pointer; }
.btn:hover { background: rgba(255,255,255,.08); }
.btn[disabled] { opacity: .5; cursor: default; }
.btn:focus-visible { outline: 2px solid var(--blue); outline-offset: 2px; }
.btn.red { color: var(--red); border-color: rgba(248,113,113,.4); }
.btn.orange { color: var(--orange); border-color: rgba(251,146,60,.4); }
.btn.blue { color: var(--blue); border-color: rgba(96,165,250,.4); }
.btn.go { background: rgba(96,165,250,.18); color: var(--blue); border-color: rgba(96,165,250,.5); }
.overlay { position: fixed; inset: 0; z-index: 30; background: rgba(0,0,0,.62); display: flex; align-items: center; justify-content: center; padding: 16px; }
.dialog { background: var(--panel); border: 1px solid var(--line); border-radius: 16px; width: 100%; max-width: 620px; max-height: calc(100vh - 32px); overflow: auto; padding: 18px 20px; box-sizing: border-box; }
.dialog h2 { margin: 0 0 6px; font-size: 18px; }
.dialog .hint { color: var(--muted); font-size: 13px; margin: 0 0 8px; }
.fields { display: grid; grid-template-columns: 1fr 1fr; gap: 0 14px; }
.fld { display: block; margin: 8px 0; }
.fld .lbl { display: block; font-size: 12px; color: var(--muted); margin-bottom: 4px; }
.fld input, .fld select { width: 100%; box-sizing: border-box; font: inherit; font-size: 14px; color: var(--text); background: var(--tile); border: 1px solid var(--tile-line); border-radius: 8px; padding: 8px 10px; color-scheme: dark; }
.fld input:focus-visible, .fld select:focus-visible { outline: 2px solid var(--blue); outline-offset: 1px; }
.confirm-name { width: 100%; font: inherit; font-size: 14px; color: var(--text); background: var(--tile); border: 1px solid var(--tile-line); border-radius: 8px; padding: 8px 10px; color-scheme: dark; }
.confirm-name:focus-visible { outline: 2px solid var(--red); outline-offset: 1px; }
.fld.bool { display: flex; gap: 8px; align-items: center; }
.fld.bool .lbl { margin: 0; font-size: 13px; color: var(--text); }
.fld.bool input { width: auto; }
.fld.bad input, .fld.bad select { border-color: var(--red); }
.ferr { color: var(--red); font-size: 12px; margin-top: 4px; }
.check { display: flex; gap: 8px; align-items: center; margin: 12px 0 0; font-size: 13px; }
.dialog .actions { margin-top: 16px; }
@media (max-width: 560px) { .fields { grid-template-columns: 1fr; } }
.ask { width: 100%; display: flex; flex-wrap: wrap; gap: 8px; align-items: center; font-size: 13px; color: var(--muted); }
.ask span { flex-basis: 100%; }
.err { width: 100%; font-size: 13px; color: var(--red); }

.tiles { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.tile { background: var(--tile); border: 1px solid var(--tile-line); border-radius: 12px; padding: 10px 12px; min-width: 0; }
.tile .label { overflow-wrap: anywhere; }
.tile .v { font-size: 18px; font-weight: 700; margin-top: 4px; font-variant-numeric: tabular-nums; }
.tile .s { font-size: 12px; color: var(--muted); margin-top: 1px; }
.tile .v small, .big small { font-size: 12px; font-weight: 500; color: var(--muted); margin-left: 3px; }

.bars { margin-top: 14px; display: grid; gap: 6px; }
.bar { display: grid; grid-template-columns: 1fr auto; gap: 2px 10px; align-items: center; font-size: 12px; color: var(--muted); }
.bar .tr { grid-column: 1 / -1; height: 7px; border-radius: 4px; background: rgba(255,255,255,.07); overflow: hidden; }
.bar .fl { display: block; height: 100%; border-radius: 4px; }
.bar b { color: var(--text); font-variant-numeric: tabular-nums; }

.notes { margin-top: 14px; display: grid; gap: 8px; }
.callout { font-size: 13px; line-height: 1.4; border-radius: 12px; padding: 10px 12px; background: var(--tile); border: 1px solid var(--tile-line); color: var(--muted); }
.callout.red { border-color: rgba(248,113,113,.35); background: rgba(248,113,113,.07); color: #fecaca; }
.callout.orange { border-color: rgba(251,146,60,.35); background: rgba(251,146,60,.07); color: #fed7aa; }
.callout.blue { border-color: rgba(96,165,250,.3); background: rgba(96,165,250,.06); color: #bfdbfe; }

table { width: 100%; border-collapse: collapse; background: var(--panel); border: 1px solid var(--line); border-radius: 16px; overflow: hidden; }
th, td { padding: 12px 14px; text-align: right; font-variant-numeric: tabular-nums; border-bottom: 1px solid var(--line); }
th:first-child, td:first-child { text-align: left; }
th { font-size: 11px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); background: var(--panel2); }
tr.sub td { font-size: 13px; color: var(--muted); padding-top: 6px; padding-bottom: 6px; }
tr.sub td:first-child { padding-left: 32px; }
tr.total td { font-weight: 700; border-bottom: 0; background: var(--panel2); }
td .t2 { display: block; font-size: 12px; color: var(--muted); font-weight: 400; }
.hint { font-size: 12px; color: var(--muted); margin-top: 10px; }

details { background: var(--panel); border: 1px solid var(--line); border-radius: 16px; margin-bottom: 12px; overflow: hidden; }
summary { list-style: none; cursor: pointer; display: flex; align-items: center; gap: 12px; padding: 14px 18px; }
summary::-webkit-details-marker { display: none; }
summary .who { flex: 1; }
summary .end { text-align: right; font-weight: 700; font-variant-numeric: tabular-nums; white-space: nowrap; }
summary .caret { color: var(--muted); transition: transform .15s; }
summary .chips:empty { display: none; }
/* cards (overview): the chips get a line of their own below */
details.card > summary .chips { flex-basis: 100%; justify-content: flex-start; order: 5; }
/* rows of the contract list: name, chips, amount on one line, wrapping on narrow screens */
details:not(.card) > summary { flex-wrap: wrap; }
details:not(.card) > summary .who { flex: 1 1 220px; }
details:not(.card) > summary .chips { flex: 0 1 auto; justify-content: flex-end; }
details.card { padding: 0; }
details.card > summary { padding: 14px 16px; flex-wrap: wrap; }
details.card .body { padding: 0 16px 16px; }
details.card.alert { border-color: rgba(248,113,113,.35); }
details[open] summary .caret { transform: rotate(90deg); }
.detail { padding: 4px 18px 18px; display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 18px; }
.sec h4 { margin: 8px 0 6px; font-size: 11px; font-weight: 600; letter-spacing: .09em; text-transform: uppercase; color: var(--muted); }
.row { display: flex; justify-content: space-between; gap: 12px; padding: 7px 0; border-bottom: 1px solid var(--line); font-size: 14px; }
.row span:first-child { color: var(--muted); } .row span:last-child { text-align: right; font-variant-numeric: tabular-nums; }

.state { text-align: center; padding: 64px 16px; color: var(--muted); }
.state h2 { color: var(--text); margin: 0 0 6px; }
.state a { color: var(--blue); font-weight: 600; }

@container (max-width: 760px) {
  .wrap { padding: 12px 12px 32px; }
  .top { gap: 10px; }
  .tabs { order: 3; width: 100%; margin: 0; }
  .tab { flex: 1; padding: 9px 6px; }
  .spacer { display: none; }
  .summary { grid-template-columns: 1fr; gap: 10px; }
  .sum { display: grid; grid-template-columns: 1fr auto; align-items: center; padding: 12px 14px; }
  .sum .value { font-size: 20px; margin: 0; grid-column: 2; grid-row: 1 / span 2; }
  .sum .sub { grid-column: 1; }
  .grid { grid-template-columns: 1fr; gap: 12px; }
  .card { padding: 14px; }
  .big { font-size: 28px; }
  .ring, .ring svg { width: 84px; height: 84px; }
  table, thead, tbody, tr, td { display: block; }
  thead { display: none; }
  table { background: transparent; border: 0; border-radius: 0; }
  tr { background: var(--panel); border: 1px solid var(--line); border-radius: 14px; margin-bottom: 10px; padding: 8px 14px; }
  tr.sub { margin: -6px 0 10px 14px; background: var(--panel2); padding: 6px 14px; }
  td { display: flex; justify-content: space-between; text-align: right; padding: 5px 0; border: 0; }
  td::before { content: attr(data-label); color: var(--muted); font-size: 12px; text-align: left; margin-right: 12px; }
  td:first-child { font-weight: 700; padding-bottom: 6px; }
  td:first-child::before { content: none; }
  tr.sub td:first-child { padding: 0 0 2px; font-weight: 600; color: var(--muted); }
  tr.total td:first-child { display: none; }
  td.empty { display: none; }
  td.rec { flex-wrap: wrap; }
  td.rec .t2 { flex-basis: 100%; text-align: right; margin-top: 2px; }
  .detail { grid-template-columns: 1fr; gap: 6px; padding: 0 14px 14px; }
  summary { padding: 12px 14px; }
}
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
`;

/* ---------- DOM helpers (text only, never HTML) ---------- */

function h(tag, props, ...children) {
  const el = document.createElement(tag);
  for (const [key, value] of Object.entries(props || {})) {
    if (value === null || value === undefined || value === false) continue;
    if (key === "class") el.className = value;
    else if (key === "text") el.textContent = value;
    else if (key.startsWith("on")) el.addEventListener(key.slice(2), value);
    else el.setAttribute(key, value);
  }
  for (const child of children.flat(Infinity)) {
    if (child === null || child === undefined || child === false) continue;
    el.appendChild(typeof child === "string" ? document.createTextNode(child) : child);
  }
  return el;
}

function svg(tag, attrs, ...children) {
  const el = document.createElementNS(SVG_NS, tag);
  for (const [key, value] of Object.entries(attrs || {})) el.setAttribute(key, value);
  for (const child of children.flat()) if (child) el.appendChild(child);
  return el;
}

function icon(sparte) {
  const parts = ICONS[sparte] || ICONS.other;
  return svg(
    "svg", { viewBox: "0 0 24 24", "aria-hidden": "true" },
    parts.map(([tag, attrs]) => svg(tag, attrs))
  );
}

const FLOWS = {
  // the integration's "Configure" dialog (next contract) and its "Reconfigure" dialog (the contract itself)
  next: { api: "config/config_entries/options/flow", body: (c) => ({ handler: c.entry_id }), category: "options" },
  edit: { api: "config/config_entries/flow", body: (c) => ({ handler: "tariffy", entry_id: c.entry_id }), category: "config" },
  // the integration's "Add entry" dialog
  create: { api: "config/config_entries/flow", body: () => ({ handler: "tariffy" }), category: "config" },
};

const isNum = (v) => typeof v === "number" && Number.isFinite(v);

/* ---------- the panel ---------- */

class TariffyPanel extends HTMLElement {
  constructor() {
    super();
    this._hass = null;
    this._unsub = null;
    this._contracts = null; // null = loading
    this._error = null;
    this._narrow = false;
    this._tab = this._loadTab();
    this._open = new Set();
    this._compact = false;
    this._confirming = null;
    this._busy = null;
    this._actionError = null;
    this.attachShadow({ mode: "open" });
  }

  set hass(hass) {
    const first = !this._hass;
    const languageChanged = this._hass && this._hass.language !== hass.language;
    this._hass = hass;
    if (first) {
      this._subscribe();
      this._render();
    } else if (languageChanged) {
      this._render();
    }
  }

  set narrow(value) {
    this._narrow = Boolean(value);
    if (this._hass) this._render();
  }

  set panel(value) {
    this._panel = value;
  }

  connectedCallback() {
    if (this._hass && !this._unsub) this._subscribe();
    if (typeof ResizeObserver === "function" && !this._observer) {
      this._observer = new ResizeObserver((entries) => {
        const width = entries[entries.length - 1].contentRect.width;
        const compact = width > 0 && width <= 760;
        if (compact !== this._compact) {
          this._compact = compact;
          if (this._hass) this._render();
        }
      });
    }
    if (this._observer) this._observer.observe(this);
  }

  disconnectedCallback() {
    if (this._observer) this._observer.disconnect();
    this._closeFlow();
    if (this._unsub) {
      this._unsub();
      this._unsub = null;
    }
  }

  async _subscribe() {
    try {
      this._unsub = await this._hass.connection.subscribeMessage(
        (event) => {
          this._contracts = Array.isArray(event.contracts) ? event.contracts : [];
          this._error = null;
          this._render();
        },
        { type: "tariffy/subscribe" }
      );
    } catch (err) {
      this._error = String((err && err.message) || err);
      this._render();
    }
  }

  _loadTab() {
    try {
      const tab = window.localStorage.getItem(TAB_KEY);
      return TABS.includes(tab) ? tab : "overview";
    } catch (_err) {
      return "overview";
    }
  }

  _saveTab(tab) {
    try {
      window.localStorage.setItem(TAB_KEY, tab);
    } catch (_err) { /* private mode */ }
  }

  /* ----- language, numbers, dates ----- */

  get _lang() {
    const code = String((this._hass && this._hass.language) || "en").toLowerCase();
    return code.startsWith("de") ? "de" : "en";
  }

  _t(key, vars) {
    let text = I18N[this._lang][key] ?? I18N.en[key] ?? key;
    for (const [name, value] of Object.entries(vars || {})) text = text.replace(`{${name}}`, value);
    return text;
  }

  get _locale() {
    return (this._hass && this._hass.locale && this._hass.locale.language) ||
      (this._hass && this._hass.language) || "en";
  }

  _money(value, currency, { sign = false, digits = 0 } = {}) {
    if (!isNum(value)) return "–";
    let text;
    try {
      text = new Intl.NumberFormat(this._locale, {
        style: "currency", currency: currency || "EUR",
        minimumFractionDigits: digits, maximumFractionDigits: digits,
      }).format(Math.abs(value));
    } catch (_err) {
      text = `${Math.abs(value).toFixed(digits)} ${currency || ""}`;
    }
    if (value < 0) return `−${text}`;
    return sign && value > 0 ? `+${text}` : text;
  }

  _num(value, digits = 0) {
    if (!isNum(value)) return "–";
    return new Intl.NumberFormat(this._locale, {
      minimumFractionDigits: digits, maximumFractionDigits: digits,
    }).format(value);
  }

  _price(value, currency, unit) {
    if (!isNum(value)) return "–";
    return `${this._money(value, currency, { digits: 4 })} / ${unit}`;
  }

  /* A negative recommended instalment means the credit already covers the costs
   * until the end of the contract: show 0 instead of a negative instalment. */
  _instalment(value, currency) {
    return isNum(value) ? this._money(Math.max(0, value), currency, { digits: 2 }) : "–";
  }

  _covered(value) {
    return isNum(value) && value < 0;
  }

  _parse(iso) {
    if (typeof iso !== "string") return null;
    const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso);
    return m ? new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3])) : null;
  }

  _date(iso) {
    const d = this._parse(iso);
    return d
      ? new Intl.DateTimeFormat(this._locale, { day: "2-digit", month: "2-digit", year: "numeric" }).format(d)
      : "–";
  }

  _today() {
    const n = new Date();
    return new Date(n.getFullYear(), n.getMonth(), n.getDate());
  }

  _days(iso) {
    const d = this._parse(iso);
    return d ? Math.round((d - this._today()) / 86400000) : null;
  }

  _unit(contract) {
    if (contract.verbrauch_einheit) return contract.verbrauch_einheit;
    return contract.sparte === "gas" || contract.sparte === "water" ? "m³" : "kWh";
  }

  _priceUnit(contract) {
    return contract.sparte === "water" ? this._unit(contract) : "kWh";
  }

  /* ----- derived values per contract ----- */

  _derive(c) {
    const begin = this._parse(c.beginn);
    const end = this._parse(c.ende);
    let elapsed = null;
    if (begin && end && end > begin) {
      elapsed = Math.min(1, Math.max(0, (this._today() - begin) / (end - begin)));
    }
    const paid = isNum(c.kosten_bisher) && isNum(c.guthaben_bisher) ? c.kosten_bisher + c.guthaben_bisher : null;
    const hasMetering = isNum(c.prognose_real);
    const chips = [];
    if (c.erinnerung_aktiv) chips.push({ text: this._t("cancelDue"), tone: "orange" });
    if (c.abschlag_warnung_aktiv) chips.push({ text: this._t("warning"), tone: "red" });
    else if (hasMetering) {
      chips.push(c.prognose_real >= 0
        ? { text: this._t("credit"), tone: "green" }
        : { text: this._t("balanceDue"), tone: "red" });
    }
    if (c.wechsel) chips.push({ text: this._t("switchOn", { d: this._date(c.wechsel) }), tone: "blue" });
    return { elapsed, paid, hasMetering, chips };
  }

  /* ----- rendering ----- */

  _render() {
    const root = this.shadowRoot;
    root.replaceChildren(h("style", { text: STYLE }));
    const wrap = h("div", { class: "wrap" });
    wrap.appendChild(this._top());

    if (this._error) {
      wrap.appendChild(h("div", { class: "state" }, h("h2", { text: this._t("error" ) }), h("div", { text: this._error })));
    } else if (this._contracts === null) {
      wrap.appendChild(h("div", { class: "state", text: this._t("loading") }));
    } else if (this._contracts.length === 0) {
      wrap.appendChild(this._empty());
    } else if (this._tab === "costs") {
      wrap.appendChild(this._costs());
    } else if (this._tab === "contracts") {
      wrap.appendChild(this._contractList());
    } else {
      wrap.appendChild(this._summary());
      wrap.appendChild(h("div", { class: "grid" }, this._contracts.map((c) => this._card(c))));
    }
    root.appendChild(wrap);
    if (this._dlgEl) root.appendChild(this._dlgEl);
  }

  _top() {
    const menu = this._narrow && customElements.get("ha-menu-button")
      ? Object.assign(document.createElement("ha-menu-button"), { hass: this._hass, narrow: this._narrow })
      : null;
    const tabs = h(
      "div", { class: "tabs", role: "tablist" },
      TABS.map((tab) => h("button", {
        class: "tab", role: "tab", "aria-selected": String(this._tab === tab), text: this._t(tab),
        onclick: () => { this._tab = tab; this._saveTab(tab); this._render(); },
      }))
    );
    return h(
      "div", { class: "top" },
      menu,
      h("div", { class: "brand" }, "Tariffy", h("span", { class: "pill", text: this._t("beta") })),
      tabs,
      this._isAdmin
        ? h("button", { class: "btn blue", type: "button", text: this._t("actNew"), onclick: () => this._openFlow(null, "create") })
        : h("div", { class: "spacer" })
    );
  }

  _empty() {
    return h(
      "div", { class: "state" },
      h("h2", { text: this._t("emptyTitle") }),
      h("p", { text: this._t("emptyText") }),
      h("a", { href: "/config/integrations/dashboard/add?domain=tariffy", text: this._t("emptyLink") })
    );
  }

  _summary() {
    const contracts = this._contracts;
    const currency = contracts[0].currency || "EUR";
    const monthly = contracts.reduce((sum, c) => sum + (isNum(c.abschlag) ? c.abschlag : 0), 0);
    const withMetering = contracts.filter((c) => isNum(c.prognose_real));
    const forecast = withMetering.reduce((sum, c) => sum + c.prognose_real, 0);

    const candidates = [];
    for (const c of contracts) {
      const endDays = this._days(c.ende);
      if (c.erinnerung_aktiv && endDays !== null && endDays >= 0) {
        candidates.push({ days: endDays, rank: 0, text: `${this._t("cancelDue")} · ${c.title}`, date: c.ende });
      }
      const switchDays = this._days(c.wechsel);
      if (switchDays !== null && switchDays >= 0) {
        candidates.push({ days: switchDays, rank: 1, text: this._t("switchOn", { d: this._date(c.wechsel) }) + ` · ${c.title}`, date: c.wechsel });
      }
      if (endDays !== null && endDays >= 0) {
        candidates.push({ days: endDays, rank: 2, text: `${this._t("contractEnd")} · ${c.title}`, date: c.ende });
      }
    }
    candidates.sort((a, b) => a.rank - b.rank || a.days - b.days);
    const urgent = candidates.find((x) => x.rank === 0);
    const next = urgent || candidates.sort((a, b) => a.days - b.days)[0];

    const rel = (days) => (days === 0 ? this._t("today") : days === 1 ? this._t("tomorrow") : this._t("inDays", { n: days }));
    const tone = (value) => (value < 0 ? "red-t" : value > 0 ? "green-t" : "");

    return h(
      "div", { class: "summary" },
      h("div", { class: "sum" },
        h("div", { class: "label", text: this._t("monthlyTotal") }),
        h("div", { class: "value", text: this._money(monthly, currency, { digits: 2 }) })),
      h("div", { class: "sum" },
        h("div", { class: "label", text: this._t("forecastTotal") }),
        h("div", { class: `value ${withMetering.length ? tone(forecast) : "muted-t"}`,
          text: withMetering.length ? this._money(forecast, currency, { sign: true }) : "–" }),
        h("div", { class: "sub", text: this._t("forecastSub", { n: withMetering.length, m: contracts.length }) })),
      h("div", { class: "sum" },
        h("div", { class: "label", text: this._t("nextDeadline") }),
        h("div", { class: "value", text: next ? this._date(next.date) : "–" }),
        h("div", { class: "sub", text: next ? `${next.text} · ${rel(next.days)}` : this._t("nothingPlanned") }))
    );
  }

  _chips(chips) {
    return h("div", { class: "chips" }, chips.map((chip) => h("span", { class: `chip ${chip.tone}`, text: chip.text })));
  }

  _who(c) {
    return h(
      "div", { class: "who" },
      h("div", { class: "title", text: c.title }),
      h("div", { class: "meta", text: [this._t("sparte")[c.sparte] || c.sparte, c.anbieter, c.tarif].filter(Boolean).join(" · ") })
    );
  }

  _tile(label, value, sub, tone) {
    return h(
      "div", { class: "tile" },
      h("div", { class: "label", text: label }),
      h("div", { class: `v ${tone || ""}`, text: value }),
      sub ? h("div", { class: "s", text: sub }) : null
    );
  }

  _ring(elapsed) {
    const radius = 38;
    const circumference = 2 * Math.PI * radius;
    const pct = elapsed === null ? null : Math.round(elapsed * 100);
    return h(
      "div", { class: "ring", role: "img", "aria-label": `${this._t("term")}: ${pct === null ? "–" : pct + " %"}` },
      svg("svg", { viewBox: "0 0 96 96" },
        svg("circle", { class: "track", cx: 48, cy: 48, r: radius, fill: "none", "stroke-width": 8 }),
        pct === null ? null : svg("circle", {
          class: "arc", cx: 48, cy: 48, r: radius, fill: "none", "stroke-width": 8,
          "stroke-dasharray": `${(circumference * elapsed).toFixed(2)} ${circumference.toFixed(2)}`,
        })),
      h("div", { class: "center" },
        h("div", { class: "pct", text: pct === null ? "–" : `${pct} %` }),
        h("div", { class: "pcap", text: this._t("term") }))
    );
  }

  _bars(c, d) {
    if (d.paid === null || !isNum(c.kosten_bisher)) return null;
    const max = Math.max(d.paid, c.kosten_bisher, 1);
    const over = c.kosten_bisher > d.paid;
    const bar = (label, value, color) => h(
      "div", { class: "bar" },
      h("span", { text: label }),
      h("b", { text: this._money(value, c.currency) }),
      h("span", { class: "tr" }, h("span", { class: "fl", style: `width:${Math.max(2, (value / max) * 100).toFixed(1)}%;background:${color}` }))
    );
    return h("div", { class: "bars" },
      bar(this._t("paid"), d.paid, "var(--blue)"),
      bar(this._t("cost"), c.kosten_bisher, over ? "var(--red)" : "var(--green)"));
  }

  _card(c) {
    const d = this._derive(c);
    const unit = this._unit(c);
    const alert = c.abschlag_warnung_aktiv;

    const heroValue = d.hasMetering ? c.prognose_real : c.jahreskosten;
    const heroLabel = d.hasMetering ? this._t("endForecast") : this._t("endTotal");
    const heroTone = d.hasMetering ? (heroValue < 0 ? "red-t" : "green-t") : "";
    const heroSub = isNum(c.abschlag)
      ? `${this._t("instalment")}: ${this._money(c.abschlag, c.currency, { digits: 2 })}` +
        (isNum(c.abschlag_anpassung_empfohlen)
          ? ` · ${this._t("recommended")}: ${this._instalment(c.abschlag_anpassung_empfohlen, c.currency)}` +
            (this._covered(c.abschlag_anpassung_empfohlen) ? ` (${this._t("coveredHint")})` : "")
          : "")
      : null;

    const tiles = d.hasMetering
      ? [
        this._tile(this._t("costSoFar"), this._money(c.kosten_bisher, c.currency, { digits: 2 })),
        this._tile(this._t("balanceSoFar"), this._money(c.guthaben_bisher, c.currency, { sign: true, digits: 2 }), null,
          isNum(c.guthaben_bisher) ? (c.guthaben_bisher < 0 ? "red-t" : "green-t") : ""),
        this._tile(this._t("consumption"), `${this._num(c.verbrauch_bisher, 0)} ${unit}`,
          isNum(c.verbrauch_hochgerechnet) ? this._t("projected", { v: `${this._num(c.verbrauch_hochgerechnet, 0)} ${unit}` }) : null),
        this._tile(this._t("remaining"), isNum(c.restlaufzeit) ? this._t("daysLeft", { n: c.restlaufzeit }) : "–",
          c.ende ? this._t("until", { d: this._date(c.ende) }) : null),
      ]
      : [
        this._tile(this._t("instalment"), this._money(c.abschlag, c.currency, { digits: 2 })),
        this._tile(this._t("contractEnd"), this._date(c.ende)),
        this._tile(this._t("remaining"), isNum(c.restlaufzeit) ? this._t("daysLeft", { n: c.restlaufzeit }) : "–"),
        this._tile(this._t("reminder"), c.erinnerung_datum ? this._date(c.erinnerung_datum) : this._t("reminderOff"),
          c.erinnerung_monate ? this._t("months", { n: c.erinnerung_monate }) : null),
      ];

    const notes = [];
    if (c.abschlag_warnung_zu_bestaetigen) {
      const value = this._money(Math.abs(c.prognose_real), c.currency);
      notes.push(h("div", { class: "callout red", text: isNum(c.abschlag_anpassung_empfohlen) && c.abschlag_anpassung_empfohlen > 0
        ? this._t("noteWarning", { v: value, a: this._money(c.abschlag_anpassung_empfohlen, c.currency) })
        : this._t("noteWarningShort", { v: value }) }));
    }
    if (c.erinnerung_aktiv) {
      notes.push(h("div", { class: "callout orange", text: this._t("noteCancel", { d: this._date(c.ende) }) }));
    }
    if (c.next && c.next.beginn) {
      const name = [c.next.anbieter, c.next.tarif].filter(Boolean).join(" · ") || "–";
      notes.push(h("div", { class: "callout blue", text: this._t("noteNext", { d: this._date(c.next.beginn), name }) }));
    }

    const hero = h("div", { class: "hero" },
      this._ring(d.elapsed),
      h("div", {},
        h("div", { class: "label", text: heroLabel }),
        h("div", { class: `big ${heroTone}`, text: this._money(heroValue, c.currency, { sign: d.hasMetering }) }),
        heroSub ? h("div", { class: "note", text: heroSub }) : null));
    const body = [hero, h("div", { class: "tiles" }, tiles), this._bars(c, d),
      notes.length ? h("div", { class: "notes" }, notes) : null, this._actions(c)];

    if (this._compact) {
      const card = h(
        "details", { class: `card compact${alert ? " alert" : ""}`, "data-id": c.entry_id },
        h("summary", {},
          h("div", { class: `badge ${c.sparte}` }, icon(c.sparte)),
          this._who(c),
          h("div", { class: `end ${heroTone}`, text: this._money(heroValue, c.currency, { sign: d.hasMetering }) }),
          h("span", { class: "caret", "aria-hidden": "true", text: "›" }),
          this._chips(d.chips)),
        h("div", { class: "body" }, body));
      if (this._open.has(c.entry_id)) card.setAttribute("open", "");
      card.addEventListener("toggle", () => {
        if (card.open) this._open.add(c.entry_id);
        else this._open.delete(c.entry_id);
      });
      return card;
    }
    return h(
      "section", { class: `card${alert ? " alert" : ""}` },
      h("div", { class: "head" },
        h("div", { class: `badge ${c.sparte}` }, icon(c.sparte)),
        this._who(c),
        this._chips(d.chips)),
      body
    );
  }

  get _isAdmin() {
    return Boolean(this._hass && this._hass.user && this._hass.user.is_admin);
  }

  /* Actions are only offered to administrators; the backend checks it again. */
  _actions(c) {
    if (!this._isAdmin) return null;
    const list = [];
    if (c.abschlag_warnung_zu_bestaetigen) {
      list.push({ key: "confirm_abschlag_warning", label: this._t("actConfirmWarning"), tone: "red", ask: "actAskWarning", yes: "actYesAck" });
    }
    if (c.erinnerung_aktiv) {
      list.push({ key: "confirm_cancellation", label: this._t("actConfirmCancel"), tone: "orange", ask: "actAskCancel", yes: "actYesAck" });
    }
    list.push({
      key: "plan_next", open: "next", tone: "blue",
      label: this._t(c.next && c.next.beginn ? "actNextEdit" : "actNextPlan"),
    });
    list.push({ key: "edit_contract", open: "edit", tone: "blue", label: this._t("actEdit") });

    const id = c.entry_id;
    const busy = this._busy === id;
    const children = [];
    const pending = this._confirming && this._confirming.id === id
      ? list.find((a) => a.key === this._confirming.key) : null;
    if (pending) {
      children.push(h("div", { class: "ask" },
        h("span", { text: this._t(pending.ask) }),
        h("button", { class: "btn go", type: "button", disabled: busy ? "" : null, text: this._t(pending.yes),
          onclick: () => this._run(c, pending.key) }),
        h("button", { class: "btn", type: "button", text: this._t("actCancel"),
          onclick: () => { this._confirming = null; this._render(); } })));
    } else {
      for (const action of list) {
        children.push(h("button", {
          class: `btn ${action.tone}`, type: "button", disabled: busy ? "" : null, text: action.label,
          onclick: () => {
            if (action.open) { this._openFlow(c, action.open); return; }
            this._confirming = { id, key: action.key };
            this._actionError = null;
            this._render();
          },
        }));
      }
    }
    if (this._actionError && this._actionError.id === id) {
      children.push(h("div", { class: "err", role: "alert", text: this._t("actFailed", { m: this._actionError.message }) }));
    }
    return h("div", { class: "actions" }, children);
  }

  async _run(c, action) {
    this._busy = c.entry_id;
    this._confirming = null;
    this._actionError = null;
    this._render();
    try {
      await this._hass.callWS({ type: "tariffy/action", entry_id: c.entry_id, action });
    } catch (err) {
      this._actionError = { id: c.entry_id, message: String((err && err.message) || err) };
    } finally {
      this._busy = null;
      this._render();
    }
  }

  /* ---------- forms of the integration: next contract and contract data ----------
     Renders the flows of Home Assistant from its REST API (the "Configure" dialog for the
     next contract, the "Reconfigure" dialog for the contract itself), so validation and
     storage stay in the integration. Empty optional fields are left out, exactly as Home
     Assistant's own form does. */

  _errorText(err) {
    return String((err && ((err.body && err.body.message) || err.message || err.error)) || err);
  }

  _fieldSpec(raw, dlg, step) {
    const kind = ["date", "text", "number", "select", "entity", "boolean"].find((k) => raw.selector && k in raw.selector) || null;
    const sel = kind === "select" ? raw.selector.select : {};
    const suggested = raw.description && raw.description.suggested_value;
    const initial = suggested !== undefined && suggested !== null ? suggested : raw.default;
    const label = dlg.localize(`component.tariffy.${dlg.category}.step.${step}.data.${raw.name}`) ||
      raw.name.replace(/^next_/, "").replace(/_/g, " ");
    const optionLabel = (value, fallback) => (sel.translation_key
      ? dlg.localize(`component.tariffy.selector.${sel.translation_key}.options.${value}`) : "") || fallback;
    return {
      name: raw.name, kind, label, required: Boolean(raw.required),
      min: kind === "number" && isNum(raw.selector.number.min) ? raw.selector.number.min : null,
      domains: kind === "entity" ? [].concat(raw.selector.entity.domain || []) : [],
      custom: Boolean(sel.custom_value),
      options: (sel.options || []).map((o) => {
        const value = typeof o === "string" ? o : o.value;
        return { value, label: optionLabel(value, typeof o === "string" ? o : o.label || o.value) };
      }),
      initial: kind === "boolean" ? Boolean(initial) : (initial === undefined || initial === null ? "" : String(initial)),
    };
  }

  async _flowLocalize(category) {
    try {
      if (typeof this._hass.loadBackendTranslation === "function") {
        await this._hass.loadBackendTranslation("selector", "tariffy"); // labels of the drop-downs
        const localize = await this._hass.loadBackendTranslation(category, "tariffy");
        if (typeof localize === "function") return localize;
      }
    } catch (_err) { /* fall back to the field names */ }
    return typeof this._hass.localize === "function" ? this._hass.localize : () => "";
  }

  _applyForm(dlg, form) {
    if (form.type === "create_entry" || (form.type === "abort" && form.reason === "reconfigure_successful")) {
      dlg.stage = "saved";
      return;
    }
    if (form.type === "abort") {
      dlg.stage = "error";
      dlg.message = this._t("dlgAborted", { m: form.reason || "" });
      return;
    }
    dlg.flowId = form.flow_id;
    dlg.stage = "form";
    if (dlg.step !== form.step_id) { // a new step starts with its own values
      dlg.step = form.step_id;
      dlg.values = {};
      dlg.refocus = true;
    }
    dlg.final = dlg.mode === "next" || form.step_id !== (dlg.mode === "create" ? "user" : "reconfigure");
    dlg.fields = (form.data_schema || []).map((f) => this._fieldSpec(f, dlg, form.step_id));
    dlg.unsupported = dlg.fields.some((f) => !f.kind);
    dlg.hint = dlg.localize(`component.tariffy.${dlg.category}.step.${form.step_id}.description`) || "";
    dlg.fieldErrors = {};
    dlg.message = null;
    for (const [name, code] of Object.entries(form.errors || {})) {
      const text = dlg.localize(`component.tariffy.${dlg.category}.error.${code}`) || String(code);
      if (name === "base") dlg.message = text;
      else dlg.fieldErrors[name] = text;
    }
    for (const f of dlg.fields) if (!(f.name in dlg.values)) dlg.values[f.name] = f.initial;
  }

  async _openFlow(c, mode) {
    this._closeFlow();
    const flow = FLOWS[mode];
    const dlg = {
      mode, api: flow.api, category: flow.category, id: c ? c.entry_id : null, name: c ? c.title : "", stage: "loading", flowId: null,
      step: null, final: true, fields: [], values: {}, fieldErrors: {}, message: null, hint: "", unsupported: false,
      asking: null, localize: () => "", refocus: false,
      hasNext: mode === "next" && Boolean(c.next && c.next.beginn),
      reminder: mode === "next" && Boolean(c.erinnerung_aktiv), markDone: true, note: null, info: null, doneKey: "dlgSaved",
    };
    this._dlg = dlg;
    this._renderDialog();
    try {
      const [form, localize] = await Promise.all([
        this._hass.callApi("POST", flow.api, flow.body(c)),
        this._flowLocalize(flow.category),
      ]);
      if (this._dlg !== dlg) {
        if (form && form.flow_id) this._abortFlow(flow.api, form.flow_id);
        return;
      }
      dlg.localize = localize;
      this._applyForm(dlg, form);
    } catch (err) {
      dlg.stage = "error";
      dlg.message = this._t("dlgLoadFailed", { m: this._errorText(err) });
    }
    if (this._dlg === dlg) this._renderDialog();
  }

  _abortFlow(api, flowId) {
    try {
      Promise.resolve(this._hass.callApi("DELETE", `${api}/${flowId}`)).catch(() => {});
    } catch (_err) { /* the flow expires by itself */ }
  }

  _closeFlow() {
    const dlg = this._dlg;
    this._dlg = null;
    if (dlg && dlg.flowId && dlg.stage !== "saved") this._abortFlow(dlg.api, dlg.flowId);
    if (this._dlgEl) {
      this._dlgEl.remove();
      this._dlgEl = null;
    }
  }

  _collectFlow(dlg) {
    const values = {};
    const errors = {};
    for (const f of dlg.fields) {
      if (f.kind === "boolean") {
        values[f.name] = Boolean(dlg.values[f.name]);
        continue;
      }
      const raw = String(dlg.values[f.name] ?? "").trim();
      if (raw === "") {
        if (f.required) errors[f.name] = this._t("dlgRequired");
        continue;
      }
      if (f.kind === "number") {
        const n = Number(raw.replace(",", "."));
        if (!Number.isFinite(n) || (f.min !== null && n < f.min)) errors[f.name] = this._t("dlgInvalidNumber");
        else values[f.name] = n;
      } else {
        values[f.name] = raw;
      }
    }
    return { values, errors };
  }

  async _sendFlow(dlg, values, removed) {
    dlg.stage = "saving";
    dlg.message = null;
    this._renderDialog();
    let result;
    try {
      result = await this._hass.callApi("POST", `${dlg.api}/${dlg.flowId}`, values);
    } catch (err) {
      if (this._dlg !== dlg) return;
      dlg.stage = "form";
      dlg.asking = null;
      dlg.message = this._t("dlgSaveFailed", { m: this._errorText(err) });
      this._renderDialog();
      return;
    }
    if (this._dlg !== dlg) return;
    dlg.asking = null;
    this._applyForm(dlg, result);
    if (dlg.stage !== "saved") {
      this._renderDialog();
      return;
    }
    dlg.doneKey = removed ? "dlgRemoved" : dlg.mode === "create" ? "dlgCreated" : "dlgSaved";
    dlg.note = null;
    this._renderDialog();
    if (!removed && dlg.reminder && dlg.markDone) {
      const done = await this._markCancellationDone(dlg.id);
      if (this._dlg !== dlg) return;
      if (!done) dlg.note = this._t("dlgMarkDoneFailed");
      this._renderDialog();
    }
  }

  /* Saving reloads the contract, so the action may answer "not_found" for a moment. */
  async _markCancellationDone(entryId) {
    for (let attempt = 0; attempt < 12; attempt++) {
      await new Promise((resolve) => setTimeout(resolve, attempt === 0 ? 700 : 600));
      try {
        await this._hass.callWS({ type: "tariffy/action", entry_id: entryId, action: "confirm_cancellation" });
        return true;
      } catch (err) {
        if (err && err.code === "not_available") return true; // nothing left to acknowledge
        if (!err || err.code !== "not_found") return false;
      }
    }
    return false;
  }

  /* Deleting is Home Assistant's own "remove entry"; the open form is closed first. */
  async _deleteContract(dlg) {
    dlg.stage = "saving";
    dlg.message = null;
    this._renderDialog();
    if (dlg.flowId) this._abortFlow(dlg.api, dlg.flowId);
    dlg.flowId = null;
    try {
      await this._hass.callApi("DELETE", `config/config_entries/entry/${dlg.id}`);
    } catch (err) {
      if (this._dlg !== dlg) return;
      dlg.stage = "error";
      dlg.message = this._t("dlgDeleteFailed", { m: this._errorText(err) });
      this._renderDialog();
      return;
    }
    if (this._dlg !== dlg) return;
    dlg.stage = "saved";
    dlg.doneKey = "dlgDeleted";
    dlg.info = this._t("dlgDeleteNote");
    this._renderDialog();
  }

  /* Validates the form; the last step of editing a contract asks once more before it is sent. */
  _submitFlow(confirmed) {
    const dlg = this._dlg;
    if (!dlg || dlg.stage !== "form") return;
    const { values, errors } = this._collectFlow(dlg);
    dlg.fieldErrors = errors;
    if (Object.keys(errors).length) {
      dlg.message = null;
      dlg.asking = null;
      this._renderDialog();
      return;
    }
    if (dlg.mode === "edit" && dlg.final && !confirmed) {
      dlg.asking = "save";
      this._renderDialog();
      return;
    }
    this._sendFlow(dlg, values, false);
  }

  _fieldInput(dlg, f) {
    const forget = (target) => { // an error message is outdated as soon as its field is edited
      if (!dlg.fieldErrors[f.name]) return;
      delete dlg.fieldErrors[f.name];
      const label = target.closest("label");
      if (label) {
        label.classList.remove("bad");
        const note = label.querySelector(".ferr");
        if (note) note.remove();
      }
      target.removeAttribute("aria-invalid");
    };
    const common = {
      id: `f-${f.name}`, name: f.name, "aria-invalid": dlg.fieldErrors[f.name] ? "true" : null,
      oninput: (ev) => { dlg.values[f.name] = ev.target.value; forget(ev.target); },
    };
    if (f.kind === "boolean") {
      return [h("input", { id: common.id, name: f.name, type: "checkbox",
        onchange: (ev) => { dlg.values[f.name] = ev.target.checked; } })];
    }
    if (f.kind === "select" && !f.custom) {
      return [h("select", { ...common, onchange: (ev) => { dlg.values[f.name] = ev.target.value; } },
        f.options.map((o) => h("option", { value: o.value, text: o.label })))];
    }
    if (f.kind === "entity" || f.kind === "select") { // free text with suggestions
      const list = `dl-${f.name}`;
      const ids = f.kind === "select" ? f.options.map((o) => o.value)
        : Object.keys((this._hass && this._hass.states) || {})
          .filter((id) => !f.domains.length || f.domains.includes(id.split(".")[0])).sort();
      return [
        h("input", { ...common, type: "text", list, autocomplete: "off", spellcheck: "false" }),
        h("datalist", { id: list }, ids.map((id) => h("option", { value: id }))),
      ];
    }
    const type = f.kind === "date" ? "date" : "text";
    return [h("input", { ...common, type, inputmode: f.kind === "number" ? "decimal" : null, autocomplete: "off" })];
  }

  _renderDialog() {
    const dlg = this._dlg;
    if (!dlg) return;
    const busy = dlg.stage === "saving";
    const body = [h("h2", { id: "dlg-title", text: this._t({ edit: "dlgTitleEdit", create: "dlgTitleCreate", next: "dlgTitle" }[dlg.mode], { name: dlg.name }) })];
    const buttons = [];
    const ask = (text, yes, tone, onYes) => h("div", { class: "ask" },
      h("span", { text }),
      h("button", { class: `btn ${tone}`, type: "button", disabled: busy ? "" : null, text: yes, onclick: onYes }),
      h("button", { class: "btn", type: "button", text: this._t("actCancel"),
        onclick: () => { dlg.asking = null; this._renderDialog(); } }));

    if (dlg.stage === "loading") {
      body.push(h("p", { class: "hint", text: this._t("dlgLoading") }));
    } else if (dlg.stage === "error") {
      body.push(h("div", { class: "err", role: "alert", text: dlg.message }));
      buttons.push(h("button", { class: "btn", type: "button", text: this._t("dlgClose"), onclick: () => this._closeFlow() }));
    } else if (dlg.stage === "saved") {
      body.push(h("p", { class: "hint", text: this._t(dlg.doneKey) }));
      if (dlg.info) body.push(h("p", { class: "hint", text: dlg.info }));
      if (dlg.note) body.push(h("div", { class: "err", role: "alert", text: dlg.note }));
      buttons.push(h("button", { class: "btn go", type: "button", text: this._t("dlgClose"), onclick: () => this._closeFlow() }));
    } else {
      if (dlg.hint) body.push(h("p", { class: "hint", text: dlg.hint }));
      if (dlg.unsupported) {
        body.push(h("div", { class: "err", role: "alert", text: this._t("dlgUnsupported") }));
      } else {
        body.push(h("div", { class: "fields" }, dlg.fields.map((f) => {
          const error = dlg.fieldErrors[f.name];
          const input = this._fieldInput(dlg, f);
          const text = h("span", { class: "lbl", text: f.label });
          return h("label", { class: `fld${f.kind === "boolean" ? " bool" : ""}${error ? " bad" : ""}`, for: `f-${f.name}` },
            f.kind === "boolean" ? [input, text] : [text, input],
            error ? h("div", { class: "ferr", text: error }) : null);
        })));
      }
      if (dlg.message) body.push(h("div", { class: "err", role: "alert", text: dlg.message }));
      if (dlg.reminder && !dlg.unsupported) {
        body.push(h("label", { class: "check" },
          h("input", { type: "checkbox", checked: dlg.markDone ? "" : null, onchange: (ev) => { dlg.markDone = ev.target.checked; } }),
          h("span", { text: this._t("dlgMarkDone") })));
      }
      if (dlg.asking === "remove") {
        buttons.push(ask(this._t("dlgRemoveAsk"), this._t("dlgRemoveYes"), "red", () => this._sendFlow(dlg, {}, true)));
      } else if (dlg.asking === "delete") {
        const go = h("button", { class: "btn red", type: "button", disabled: "", text: this._t("dlgDeleteYes"),
          onclick: () => this._deleteContract(dlg) });
        buttons.push(h("div", { class: "ask" },
          h("span", { text: this._t("dlgDeleteAsk", { name: dlg.name }) }),
          h("input", { class: "confirm-name", type: "text", autocomplete: "off", spellcheck: "false", placeholder: dlg.name,
            "aria-label": this._t("dlgDeleteAsk", { name: dlg.name }),
            oninput: (ev) => { go.disabled = ev.target.value.trim() !== dlg.name; } }),
          go,
          h("button", { class: "btn", type: "button", text: this._t("actCancel"),
            onclick: () => { dlg.asking = null; this._renderDialog(); } })));
      } else if (dlg.asking === "save") {
        buttons.push(ask(this._t("dlgSaveAsk"), this._t("dlgSaveYes"), "go", () => this._submitFlow(true)));
      } else {
        if (!dlg.unsupported) {
          buttons.push(h("button", { class: "btn go", type: "button", disabled: busy ? "" : null,
            text: this._t(busy ? "dlgSaving" : dlg.final ? "dlgSave" : "dlgContinue"), onclick: () => this._submitFlow(false) }));
        }
        buttons.push(h("button", { class: "btn", type: "button", disabled: busy ? "" : null, text: this._t("actCancel"),
          onclick: () => this._closeFlow() }));
        if (dlg.mode === "edit") {
          buttons.push(h("button", { class: "btn red", type: "button", disabled: busy ? "" : null, text: this._t("dlgDelete"),
            onclick: () => { dlg.asking = "delete"; this._renderDialog(); } }));
        }
        if (dlg.hasNext && !dlg.unsupported) {
          buttons.push(h("button", { class: "btn red", type: "button", disabled: busy ? "" : null, text: this._t("dlgRemove"),
            onclick: () => { dlg.asking = "remove"; this._renderDialog(); } }));
        }
      }
    }
    body.push(h("div", { class: "actions" }, buttons));

    const el = this._dlgEl || (this._dlgEl = h("div", { class: "overlay" }));
    el.onkeydown = (ev) => { if (ev.key === "Escape" && !busy) this._closeFlow(); };
    el.replaceChildren(h("div", { class: "dialog", role: "dialog", "aria-modal": "true", "aria-labelledby": "dlg-title" }, body));
    if (!el.isConnected) this.shadowRoot.appendChild(el);

    // the inputs are filled through properties, attributes would not follow later changes
    for (const f of dlg.fields) {
      const input = el.querySelector(`[name="${f.name}"]`);
      if (!input) continue;
      if (f.kind === "boolean") input.checked = Boolean(dlg.values[f.name]);
      else input.value = dlg.values[f.name] ?? "";
    }
    const confirmName = el.querySelector(".confirm-name");
    if (confirmName) confirmName.focus();
    if (dlg.refocus && dlg.stage === "form") {
      dlg.refocus = false;
      const first = el.querySelector("input, select");
      if (first) first.focus();
    }
  }

  _recommendedCell(c) {
    const raw = c.empfohlener_abschlag ?? c.abschlag_anpassung_empfohlen;
    return h("td", {
      "data-label": this._t("colRecommended"), class: isNum(raw) ? "rec" : "rec empty",
    }, this._instalment(raw, c.currency),
    this._covered(raw) ? h("span", { class: "t2", text: this._t("coveredHint") }) : null);
  }

  _costs() {
    const contracts = this._contracts;
    const currency = contracts[0].currency || "EUR";
    const tone = (v) => (isNum(v) ? (v < 0 ? "red-t" : v > 0 ? "green-t" : "") : "muted-t");
    const cell = (label, value, cls) => h("td", { "data-label": label, class: [cls, value === "–" ? "empty" : ""].filter(Boolean).join(" ") || null, text: value });
    const sum = (key) => contracts.reduce((s, c) => s + (isNum(c[key]) ? c[key] : 0), 0);

    const rows = [];
    for (const c of contracts) {
      rows.push(h("tr", {},
        h("td", {}, c.title, h("span", { class: "t2", text: c.anbieter || this._t("sparte")[c.sparte] || c.sparte })),
        cell(this._t("colCost"), this._money(c.kosten_bisher, c.currency, { digits: 2 })),
        cell(this._t("colBalance"), this._money(c.guthaben_bisher, c.currency, { sign: true, digits: 2 }), tone(c.guthaben_bisher)),
        cell(this._t("colForecast"), this._money(c.prognose_real, c.currency, { sign: true }), tone(c.prognose_real)),
        cell(this._t("colInstalment"), this._money(c.abschlag, c.currency, { digits: 2 })),
        this._recommendedCell(c)));
      if (isNum(c.kosten_ht_bisher) || isNum(c.kosten_nt_bisher)) {
        for (const [label, key, vkey] of [["highTariff", "kosten_ht_bisher", "verbrauch_bisher_ht"], ["lowTariff", "kosten_nt_bisher", "verbrauch_bisher_nt"]]) {
          rows.push(h("tr", { class: "sub" },
            h("td", { text: `${this._t(label)} · ${this._num(c[vkey], 0)} ${this._unit(c)}` }),
            cell(this._t("colCost"), this._money(c[key], c.currency, { digits: 2 }))));
        }
      }
    }
    rows.push(h("tr", { class: "total" },
      h("td", { text: this._t("total") }),
      cell(this._t("colCost"), this._money(sum("kosten_bisher"), currency, { digits: 2 })),
      cell(this._t("colBalance"), this._money(sum("guthaben_bisher"), currency, { sign: true, digits: 2 }), tone(sum("guthaben_bisher"))),
      cell(this._t("colForecast"), this._money(sum("prognose_real"), currency, { sign: true }), tone(sum("prognose_real"))),
      cell(this._t("colInstalment"), this._money(sum("abschlag"), currency, { digits: 2 })),
      h("td", { text: "" })));

    return h(
      "div", {},
      h("table", {},
        h("thead", {}, h("tr", {}, [
          this._t("colContract"), this._t("colCost"), this._t("colBalance"),
          this._t("colForecast"), this._t("colInstalment"), this._t("colRecommended"),
        ].map((label) => h("th", { text: label })))),
        h("tbody", {}, rows)),
      h("div", { class: "hint", text: this._t("costsHint") })
    );
  }

  _contractList() {
    return h("div", {}, this._contracts.map((c) => this._detail(c)));
  }

  _detail(c) {
    const d = this._derive(c);
    const unit = this._unit(c);
    const pu = this._priceUnit(c);
    const row = (label, value) => (value === null || value === undefined || value === "–" ? null
      : h("div", { class: "row" }, h("span", { text: label }), h("span", { text: value })));
    const section = (title, rows) => {
      const filled = rows.filter(Boolean);
      return filled.length ? h("div", { class: "sec" }, h("h4", { text: title }), filled) : null;
    };
    const money = (v, digits = 2) => (isNum(v) ? this._money(v, c.currency, { digits }) : null);
    const amount = (v) => (isNum(v) ? `${this._num(v, 0)} ${unit}` : null);
    const nxt = c.next || {};

    const sections = [
      section(this._t("secContract"), [
        row(this._t("provider"), c.anbieter), row(this._t("tariff"), c.tarif),
        row(this._t("start"), c.beginn ? this._date(c.beginn) : null),
        row(this._t("end"), c.ende ? this._date(c.ende) : null),
        row(this._t("remaining"), isNum(c.restlaufzeit) ? this._t("daysLeft", { n: c.restlaufzeit }) : null),
        row(this._t("reminderDate"), c.erinnerung_datum
          ? `${this._date(c.erinnerung_datum)} · ${c.erinnerung_bestaetigt ? this._t("reminderDone") : c.erinnerung_aktiv ? this._t("reminderActive") : this._t("months", { n: c.erinnerung_monate })}`
          : null),
      ]),
      section(this._t("secPrices"), [
        row(this._t("unitPrice"), isNum(c.arbeitspreis) ? this._price(c.arbeitspreis, c.currency, pu) : null),
        row(this._t("unitPriceLow"), isNum(c.arbeitspreis_nt) ? this._price(c.arbeitspreis_nt, c.currency, pu) : null),
        row(this._t("unitPriceNight"), isNum(c.arbeitspreis_nacht) ? this._price(c.arbeitspreis_nacht, c.currency, pu) : null),
        row(this._t("unitPriceEff"), isNum(c.effektiver_arbeitspreis) ? this._price(c.effektiver_arbeitspreis, c.currency, pu) : null),
        row(this._t("unitPriceWater"), isNum(c.arbeitspreis_gesamt_wasser) ? this._price(c.arbeitspreis_gesamt_wasser, c.currency, pu) : null),
        row(this._t("basePrice"), isNum(c.grundpreis) ? `${money(c.grundpreis)} ${this._t("perMonth")}` : null),
        row(this._t("instalment"), isNum(c.abschlag) ? `${money(c.abschlag)} ${this._t("perMonth")}` : null),
      ]),
      d.hasMetering || isNum(c.verbrauch_letzte_laufzeit) ? section(this._t("secConsumption"), [
        row(this._t("soFar"), amount(c.verbrauch_bisher)),
        row(this._t("soFarHigh"), amount(c.verbrauch_bisher_ht)),
        row(this._t("soFarLow"), amount(c.verbrauch_bisher_nt)),
        row(this._t("projectedTerm"), amount(c.verbrauch_hochgerechnet)),
        row(this._t("lastPeriod"), amount(c.verbrauch_letzte_laufzeit)),
        row(this._t("costSoFar"), money(c.kosten_bisher)),
        row(this._t("balanceSoFar"), isNum(c.guthaben_bisher) ? this._money(c.guthaben_bisher, c.currency, { sign: true, digits: 2 }) : null),
        row(this._t("endForecast"), isNum(c.prognose_real) ? this._money(c.prognose_real, c.currency, { sign: true, digits: 2 }) : null),
      ]) : null,
      section(this._t("secAdvice"), [
        row(this._t("recommended"), isNum(c.empfohlener_abschlag) ? `${money(c.empfohlener_abschlag)} ${this._t("perMonth")}` : null),
        row(this._t("adjustment"), isNum(c.abschlag_anpassung_empfohlen)
          ? `${this._instalment(c.abschlag_anpassung_empfohlen, c.currency)} ${this._t("perMonth")}` +
            (this._covered(c.abschlag_anpassung_empfohlen) ? ` · ${this._t("coveredHint")}` : "")
          : null),
      ]),
      c.next ? section(this._t("secNext"), [
        row(this._t("nextStart"), nxt.beginn ? this._date(nxt.beginn) : null),
        row(this._t("nextEnd"), nxt.ende ? this._date(nxt.ende) : null),
        row(this._t("nextProvider"), nxt.anbieter), row(this._t("nextTariff"), nxt.tarif),
        row(this._t("nextPrice"), isNum(nxt.arbeitspreis) ? this._price(nxt.arbeitspreis, c.currency, pu) : null),
        row(this._t("nextInstalment"), isNum(nxt.abschlag) ? `${money(nxt.abschlag)} ${this._t("perMonth")}` : null),
      ]) : null,
    ];

    const endValue = d.hasMetering ? this._money(c.prognose_real, c.currency, { sign: true }) : this._money(c.jahreskosten, c.currency);
    const details = h(
      "details", { "data-id": c.entry_id },
      h("summary", {},
        h("div", { class: `badge ${c.sparte}` }, icon(c.sparte)),
        this._who(c),
        this._chips(d.chips),
        h("div", { class: `end ${d.hasMetering ? (c.prognose_real < 0 ? "red-t" : "green-t") : ""}`, text: endValue }),
        h("span", { class: "caret", "aria-hidden": "true", text: "›" })),
      h("div", { class: "detail" }, sections)
    );
    if (this._open.has(c.entry_id)) details.setAttribute("open", "");
    details.addEventListener("toggle", () => {
      if (details.open) this._open.add(c.entry_id);
      else this._open.delete(c.entry_id);
    });
    return details;
  }
}

if (!customElements.get("tariffy-panel")) {
  customElements.define("tariffy-panel", TariffyPanel);
}
