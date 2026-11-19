[🇩🇪 Deutsch](Archiv-und-Historie) · 🇬🇧 English

# Archive and history

This page explains what happens to a contract after its end: you can **archive** it without deleting anything, you see all **earlier terms** in the **History** tab, and you can **add** old contracts you never entered. It is for everyone who wants to keep an eye on their costs over several years.

**Contents:**

- [Archiving expired contracts](#archiving-expired-contracts)
- [The History tab](#the-history-tab)
- [Earlier terms](#earlier-terms)
- [Example with numbers](#example-with-numbers)

## Archiving expired contracts

Archiving clears an ended contract out of everyday view without deleting it. Archiving never happens by itself.

### When a contract can be archived

A contract can be archived when all three points are true:

- The **contract end has passed** (the day of the contract end itself does not count yet).
- **No next contract is planned**.
- It is not archived yet.

A contract without a contract end never expires and therefore cannot be archived. An expired contract gets the badge **Expired** in the overview and, in the contract details, a note that you can archive it.

### Archiving and restoring

1. In the panel open the **Contracts** tab and expand the details of the expired contract.
2. Click **Archive**. A confirmation question follows ("Archive this contract? …") which you confirm with **Yes, archive**. Only administrators see the button.
3. The contract disappears from the overview, the costs, the contracts and the totals and appears in the **History** tab in the group **Archived contracts**.
4. To bring it back, click **Restore** there and confirm with **Yes, restore**.

This is what archiving does:

- The **last term** is added to the contract's history (marked "archived").
- Reminder and instalment warning are off, open persistent notifications are removed.
- **Nothing is deleted.** The sensors, buttons and their statistics stay.

**Restoring** removes exactly that one entry again, all earlier terms stay. The contract is then back as normal, and a reminder that was active before reports again.

> **Good to know:** Archiving and deleting are different things. A deleted contract loses its sensors and can be brought back for only 30 days (see [Backup-and-Migration](EN-Backup-and-Migration)). An archived one is kept without a time limit.

## The History tab

The **History** tab shows two groups, each with one block per contract:

- **Archived contracts** with the badge "Archived" and the button **Restore**.
- **Earlier terms** of the contracts that are still running.

Every row is a term with **Term** (period, below it provider and tariff), **Instalment**, **Cost**, **Consumption** and **Balance**; the newest is on top. Below the block is the **Total cost** over all terms with "since <date>" and the number of terms. For an earlier term its cost counts, and if none is entered, the instalments paid. If both are missing it says "at least …", because the sum is then incomplete. For an archived contract the last term is already in the history and is not counted twice.

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/english-history.png"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/english-history-light.png" alt="The History tab with the group Archived contracts (an old electricity contract, two terms, button Restore) and the group Earlier terms (Strom Haus, two terms), at the top right the button Add an old contract" width="100%"></picture></p>

*Figure: The "History" tab with mock data dated 12 Jul 2026: an archived contract and the earlier terms of a running contract.*

All users see the history, only administrators see **Add an old contract**, the pencils for editing and the actions. More about the layout of the tab is on [Panel-History](EN-Panel-History).

## Earlier terms

### How they come about

A term gets into the history in three ways:

- **Automatically** when a next contract takes over or when you renew a flat-rate contract (see [Contract-End-and-Switching](EN-Contract-End-and-Switching)).
- **When archiving**, as the last term of the contract.
- **By hand**, when you add an older contract (see below).

Only what the panel shows anyway is stored: period, provider, tariff, unit price, base price, instalment, cost, instalments paid, balance and consumption, for a loan also loan amount, interest and remaining debt. **Customer, meter and market location numbers are not included.** At most **50 terms** are kept per contract; if the history is full, an automatic entry pushes the oldest one out, and adding by hand gives the message "The history is full (50 terms)." The history has no entity of its own in Home Assistant; it is in the panel and in the backup.

### Adding an earlier term

Do you have a contract from before Tariffy? Add it, then the total cost is right too.

1. Open the **History** tab and click **Add an old contract** (administrators only).
2. At **Contract** choose which contract the term belongs to. Meter and kind come from it.
3. Enter **Start** and **End**. The end must not be before the start.
4. Enter, as far as known, **Provider**, **Tariff**, **Price per unit (€)**, **Base price per month (€)** and **Instalment per month (€)**.
5. Leave the grey fields **Consumption**, **Cost (€)**, **Instalments paid (€)** and **Balance (€)** empty. They are calculated; below each one it says where the value comes from.
6. Click **Save**. Nothing is saved before that.

![The Add an old contract dialog for the contract Strom Haus, period 2024, with consumption 3000 entered and the fields cost, instalments paid and balance calculated](https://raw.githubusercontent.com/wiki/weskona/tariffy/images/term-dialog.png)

*Figure: The dialog "Add an old contract" with mock data (German interface). The consumption is entered by hand ("Von dir eingetragen", entered by you), the other three values are calculated ("Berechnet").*

### What is calculated automatically

You can type your own value into any field; it then takes precedence and the rest follows from it. The calculation:

| Value | Calculation |
|-------|-------------|
| Consumption | From the long-term statistics of the meter between start and end; for a dual-tariff contract both registers are added. If there are no statistics for that time, you enter it yourself. Flat-rate contracts have no consumption. |
| Instalments paid | Instalment per month times the duration in months (days divided by 30.44). If you entered the real payments under **Instalments by payment (optional)**, those count. |
| Cost | Consumption times unit price plus base price times months; for gas the consumption is converted to kWh with the contract's calorific value and state number. For flat-rate contracts the cost is what was paid. |
| Balance | Instalments paid minus cost (only for contracts with consumption). Positive is a credit, negative a balance due. |

> **Good to know:** Tiered prices, dynamic prices and separate prices for high and low tariff are not calculated here. In that case enter the cost yourself.

### Editing and deleting

The pencil in the row opens **Edit term**. Values you entered yourself stay; calculated ones are calculated again. Terms entered by hand are marked "entered by hand". With **Delete term** (question "Delete this term from the history?") you remove a row. If you edit the term that archiving created, its archive marker is kept, so that **Restore** still finds it.

## Example with numbers

Example (the values from the screenshot above): for the contract "Strom Haus" you add the term 1 Jan 2024 to 31 Dec 2024, unit price 0.30 €/kWh, base price 10 €/month, instalment 90 €/month and a consumption of 3000 kWh.

1. Duration: 365 days / 30.44 = 11.99 months.
2. **Instalments paid** = 90 € × 11.99 = 1,079.10 €.
3. **Cost** = 3000 × 0.30 € + 10 € × 11.99 = 1,019.90 €.
4. **Balance** = 1,079.10 € − 1,019.90 € = +59.20 €, so a credit.

Had you left the consumption empty, Tariffy would fetch it from the meter's statistics and calculate everything from that. In the tests, meter readings of 1000 and 4200 kWh at the start and on the day after the end give a consumption of 3200 kWh.

## See also

- [Panel-History](EN-Panel-History): the History tab in the panel
- [Contract-End-and-Switching](EN-Contract-End-and-Switching): when terms get into the history automatically
- [Next-Contract-or-Renew](EN-Next-Contract-or-Renew): next contract or renew
- [Backup-and-Migration](EN-Backup-and-Migration): history and archive are part of the backup
- [Payments-and-Costs](EN-Payments-and-Costs): total cost over all terms
