[🇩🇪 Deutsch](Panel-Uebersicht) · 🇬🇧 English

# Panel: Overview

The **Tariffy panel** is a page of its own in the Home Assistant sidebar. This page explains how the panel is built and what the **Overview** tab shows: four tiles with the totals and, below them, one card per contract. It is for everyone who opens the panel for the first time.

**Contents:**
- [Open the panel](#open-the-panel)
- [The five tabs](#the-five-tabs)
- [The four tiles on top](#the-four-tiles-on-top)
- [The contract cards](#the-contract-cards)
- [Signs and colours](#signs-and-colours)
- [Example: the Strom Haus card](#example-the-strom-haus-card)
- [On a phone](#on-a-phone)
- [When something is wrong](#when-something-is-wrong)
- [See also](#see-also)

## Open the panel

The **Tariffy** entry (icon `mdi:cash-multiple`) appears in the sidebar as soon as at least one contract is loaded. There is nothing to install or set up: the panel has been part of the integration since version `1.27.0`. If you do not want the entry in the sidebar, you can hide it in your own profile.

After an update, restart Home Assistant and **hard-reload** the browser page once (Ctrl+F5; on a phone: reload the page or clear the app cache). Otherwise the browser still shows the old panel file.

The panel follows the **language** of Home Assistant (German, otherwise English) and its **theme** (light or dark, see [Panel permissions and design](EN-Panel-Permissions-and-Design)). The panel remembers in the browser which tab you had open last.

All examples on the panel pages come from mock data dated 12 July 2026. The numbers in your panel look different.

## The five tabs

The tab bar is at the top, in the middle. The **Backup** tab only appears for administrators.

| Tab | What it is for | Page |
|---|---|---|
| **Overview** | Four tiles with the totals, below them one card per contract. View only, without editing actions. | this page |
| **Costs** | Cost split as a ring chart and one table each for metered and flat-rate contracts. | [Panel costs](EN-Panel-Costs) |
| **Contracts** | Expandable details per contract and every action that changes a contract. | [Panel contracts](EN-Panel-Contracts) |
| **History** | Earlier terms and archived contracts. | [Panel history](EN-Panel-History) |
| **Backup** | Download a backup, restore from a file, bring back deleted contracts (administrators only). | [Panel backup](EN-Panel-Backup) |

<table align="center"><tr><td align="center" width="50%"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/english-overview.png" alt="Overview tab on the desktop: the tab bar with Overview, Costs, Contracts, History and Backup on top, below it four tiles, then the groups of metered contracts, flat-rate contracts and loans with one card per contract (dark design)" width="100%"><br><sub>Dark</sub></td><td align="center" width="50%"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/english-overview-light.png" alt="Overview tab on the desktop: the tab bar with Overview, Costs, Contracts, History and Backup on top, below it four tiles, then the groups of metered contracts, flat-rate contracts and loans with one card per contract (light design)" width="100%"><br><sub>Light</sub></td></tr></table>

*Figure: The Overview tab on the desktop (mock data of 12 July 2026).*

## The four tiles on top

The tiles sum up all contracts. Loans do not count (see below).

| Tile | What it shows |
|---|---|
| **Instalments per month** | The sum of all monthly instalments, below it the yearly figure ("≈ x / year") and a bar that splits **Metered** and **Flat rate**. |
| **Cost so far** | The cost of all contracts until today, plus "Instalments due so far" and the **Balance today**. |
| **Forecast at contract end** | The sum of the forecasts and, per contract, the forecast, the worst first. Only contracts with consumption metering count; the line below says so ("n of m contracts with metering"). |
| **Next dates** | The next date big, below it the further ones: cancellation deadline ("Cancel now"), switch and contract end. Without dates it says "Nothing planned". |

> **Good to know:** All values are the same as those of the sensors (see [Sensor reference](EN-Sensor-Reference)) and update by themselves. The panel does not calculate anything itself.

## The contract cards

Below the tiles the contracts stand in groups, one card per contract:

- **Metered contracts** (electricity, gas, water),
- **Flat-rate contracts** (internet, mobile, insurance, streaming, other),
- **House costs** (waste fees, street cleaning and the like; they count in the totals),
- **Loans / financing** (kept apart: their amounts do not count in the totals of the contracts).

The cards are tinted by their state: green for credit, red for balance due, orange when the cancellation is due. At the top right of a card there is a badge, for example **Credit**, **Balance due**, **Balance due likely** (the forecast is below the warning threshold), **Cancel now**, **Switch on 01.01.2027** (a next contract is planned) or **Expired** (the contract end has passed, see [Panel history](EN-Panel-History)).

**Metered card** (electricity, gas, water):

- The **forecast at contract end** as the big figure, next to the **term ring** (percent of the term that is over).
- Below it the instalment per month and the note about the instalment: "Raise the instalment to x per month", "Instalment could drop to x per month" or "No instalment needed: the credit covers the costs until the contract ends".
- At most three figures: **Cost so far**, **Balance today** and **Consumption** (with the projection for the term).
- Two bars: **Instalments paid** against **Cost**.
- The **remaining term** and, if the contract has a history, the **total cost** over all terms ("since 01.01.2024 · 3 terms").
- A note box, for example about a balance due or a running cancellation period. If **Balance today** and the forecast point in different directions (behind today, credit at the end, or the other way round), a line says why.

**Flat-rate card** (internet, mobile, ...): the **instalment per month** big, below it the yearly figure and the amount over the term, plus the tiles **Cost so far** and **Contract end**, a **term bar**, the remaining term and the **reminder**. There is no ring, no consumption and no balance. If the contract has a history, a tile **Total cost** is added.

**Loan card:** the **remaining debt** big, below it the monthly rate, nominal and effective interest rate, the tiles **Paid so far**, **Remaining payments** and **Next payment**, a bar **Repaid**, the remaining term, payments made and the split of the next payment into interest and principal. More in [Loan contract](EN-Contract-Loan).

> **Good to know:** For flat-rate contracts the **Cost so far** are the payments booked until today, not a daily share. How Tariffy counts them is in [Payments and costs](EN-Payments-and-Costs). A **Total cost** line only appears when there is a history or one-off items ([Payment history and one-off items](EN-Payment-History-and-One-off-Items)).

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/wide-overview.png" alt="Overview on a wide screen: the four tiles side by side, below them four metered cards in one row" width="100%"></p>

*Figure: On a wide screen more cards stand side by side (German labels in this screenshot).*

## Signs and colours

- **Plus** is credit, **minus** is balance due.
- "At contract end" is projected from the consumption so far.
- If a credit already covers the costs until contract end, the recommended instalment shows "0.00 €" with the note "Credit covers the costs", never a negative amount.

Green stands for credit, red for balance due, orange for a due cancellation and blue for a planned switch.

## Example: the Strom Haus card

In the mock data the contract **Strom Haus** (Stadtwerke Nord, tariff Öko Fix 12, instalment 40.00 € a month) shows these values:

| Display | Value | Meaning |
|---|---|---|
| Forecast at contract end | −495 € | A balance due of about 495 € is expected by 31.12.2026. |
| Balance today | −206.24 € | Today the cost (513.54 €) is above what was paid by this amount. |
| Instalments paid | 307 € | 252.30 € of instalments plus 55.00 € from the one-off items (switching bonus +80.00 €, broker's fee −25.00 €). |
| Instalment note | "Raise the instalment to 127.66 € per month" | With this instalment the forecast would be balanced by the contract end. |
| Term ring | 53 % | 172 days remaining until 31.12.2026. |

The card is tinted red and carries the badge **Balance due likely**. Check: the **Balance today** is 252.30 € + 55.00 € − 513.54 € = −206.24 €. Next to it, **Gas Heizung** shows **Credit** (+524 € at contract end): its note says "No instalment needed: the credit covers the costs until the contract ends".

The overview has no buttons. How you change the instalment or acknowledge the warning is described in [Panel contracts](EN-Panel-Contracts).

## On a phone

When the panel is narrow (up to about 760 pixels wide), the tiles stand one below the other and every card is an **expandable row**: name, provider and tariff, the forecast as a figure and the badge. The arrow on the right expands the card and shows the same details as on the desktop. When Home Assistant itself is narrow, the menu button appears at the top left.

<table align="center"><tr><td align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-overview.png" alt="Overview on a phone: four tiles one below the other, below them the contracts as collapsed rows with forecast and badge (dark design)" width="300"><br><sub>Dark</sub></td><td align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-overview-light.png" alt="Overview on a phone: four tiles one below the other, below them the contracts as collapsed rows with forecast and badge (light design)" width="300"><br><sub>Light</sub></td></tr></table>

*Figure: The overview on a phone, all cards collapsed (German labels in this screenshot).*

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-overview-open.png" alt="Overview on a phone with expanded cards for Strom Haus, Strom Wohnung and Internet" width="300"></p>

*Figure: Cards expanded with the arrow show all details, just stacked (German labels in this screenshot).*

## When something is wrong

| Problem | Solution |
|---|---|
| No "Tariffy" entry in the sidebar | Check the version in HACS (the panel exists from 1.27.0), restart Home Assistant, hard-reload the page. Check in your profile whether the entry is hidden. Look in the log for "Tariffy: panel": the panel can fail without disturbing the contracts. |
| The panel shows the old interface or buttons are missing | Hard-reload the page (Ctrl+F5), the browser cached the old file. |
| Page black or empty | Hard-reload the page. If that does not help, restart Home Assistant and look in the log for "Tariffy: panel". See also [Panel permissions and design](EN-Panel-Permissions-and-Design) about the messages "No contracts yet" and "The panel could not load the contracts." |
| No buttons visible | The actions are for administrators only. |

More help: [Troubleshooting](EN-Troubleshooting). Report a problem with the [bug report form](https://github.com/weskona/tariffy/issues/new/choose) and the exact version.

## See also

- [Panel costs](EN-Panel-Costs): the cost split and the tables.
- [Panel contracts](EN-Panel-Contracts): contract details and every action.
- [Panel history](EN-Panel-History): earlier terms and archive.
- [Panel backup](EN-Panel-Backup): backup and deleted contracts.
- [Panel permissions and design](EN-Panel-Permissions-and-Design): administrators, light and dark theme.
- [Sensor reference](EN-Sensor-Reference): the same values as sensors.
