[🇩🇪 Deutsch](Abschlagsverlauf-und-Einmalposten) · 🇬🇧 English

# Payment history and one-off items

This page explains two tools in the panel with which you adjust the numbers of a contract to reality: the **payment history** ("Edit instalments") when your provider changed the instalment in the middle of the term, and **one-time items**, for example a switching bonus or a broker's bill. Both are in the tab **Contracts** and only for administrators.

**Contents:**
- [When you need the payment history](#when-you-need-the-payment-history)
- [Entering the instalments paid](#entering-the-instalments-paid)
- [How Tariffy calculates the history](#how-tariffy-calculates-the-history)
- [Earlier terms](#earlier-terms)
- [One-time items](#one-time-items)
- [Example](#example)
- [See also](#see-also)

## When you need the payment history

By default Tariffy calculates **Paid so far** with the current instalment for the whole term so far. If your provider has changed the instalment in the meantime, that is wrong: balance and forecast would be too optimistic or too pessimistic.

- If you change the instalment in the contract form, Tariffy remembers the date and the old value and uses the old amount only until then. Several changes on the same day count as one.
- If the provider changed the instalment more than once, or you no longer know the exact date, you enter in the **payment history** **what you really paid for each payment**. It then replaces the single change.

Without an entry everything stays as before. Loans have no payment history.

## Entering the instalments paid

1. In the tab **Contracts** open the details of the contract (arrow in the row).
2. The block **Instalments paid** shows what is recorded, each with **From** and the date. The last entry carries the word **current**. Without an entry it says **No history yet: the current instalment counts for the whole term.**
3. Click **Enter instalments paid** (no history yet) or **Edit instalments** (there is one already).
4. The dialog **Instalments paid** opens with **one field per payment**:
   - for monthly payment one field per month (columns **Month** and **Instalment (€)**),
   - for quarterly payment four fields a year, for half-yearly two, for yearly one (columns **Payment** and **Amount per payment (€)**), each on the day of the debit.
5. Enter in each field what was paid for that payment. **A change also applies to the following payments that still have the same amount.** So only change the fields that differ. A comma or a point works as the decimal separator.
6. **Payments that have not been due yet** are locked and show the current instalment. **The last payment that is due is the current instalment** of the contract.
7. Click **Save**.

An empty field takes the amount of the payment before it, only the first field has to be filled. Otherwise the dialog says **Enter an amount for the first month.**

Error messages of the dialog:

| Message | Cause |
|---|---|
| **A date is not valid (not in the future, each month once).** | a date in the future or twice |
| **Each month needs an amount above zero.** | an amount is zero, negative or not a number |
| **Too many changes (60 at most).** | more than 60 changes in the history |
| **This contract has no instalments.** | the contract is a loan |
| **The contract needs a start date before the instalments can be entered by month.** | the start is missing in the contract |

Only the payments where the amount changes are stored. Each entry consists of the date (**From**) and the amount **per month**. For quarterly payment Tariffy divides the entered amount by 3, for half-yearly by 6, for yearly by 12. An empty history deletes it, the instalment of the contract stays.

> **Good to know:** If the instalment is changed later in the contract form and there is a history already, Tariffy appends a new entry with today's date. For a change on the same day it replaces the last entry.

## How Tariffy calculates the history

- **Metered contracts:** Each amount applies for the months between its date and the next entry (days ÷ 30.44). Before the first entry its amount applies. From the last entry on the current instalment applies. Entries that have not been reached yet do not count.
- **Flat-rate contracts:** Each debit counts with the amount that applied on its day.
- What changes is **Paid so far** and with it **Refund/balance due (so far)**, the forecast **Refund/balance due (contract end)** and **Instalment adjustment (recommended)**. **Cost (so far)** does not depend on the instalment.
- The history **replaces** the single change with date and old value.
- The calculation path is in [Payments-and-Costs](EN-Payments-and-Costs).

## Earlier terms

The same input exists when you enter an old contract in the tab **History** (button **Add an old contract**). In the dialog, below the fields, there is the collapsible area **Instalments by payment (optional)** with the same grid, not visible in the screenshot. From the payments Tariffy calculates the grey field **Instalments paid (€)** and the **Balance (€)**. If the area stays empty, the single **Instalment per month** applies.

![Dialog Alten Vertrag hinzufügen (German interface) with the contract Strom Haus, term 2024 and the grey calculated fields cost, instalments paid and balance](https://raw.githubusercontent.com/wiki/weskona/tariffy/images/term-dialog.png)

*Figure: The dialog for an old contract (German interface; in English it is titled "Add an old contract"). The grey fields show the calculated value with the note "Berechnet" ("Calculated"). Sample data.*

More about the history is in [Archive-and-History](EN-Archive-and-History) and [Panel-History](EN-Panel-History).

## One-time items

A **one-time item** is an amount that does not belong to the monthly instalment: a **switching bonus** or **new-customer bonus** (positive) or, for example, a **broker's fee** (negative).

1. In the tab **Contracts** open the details of the contract.
2. In the block **One-time items** click **Add item**.
3. In the dialog **Add a one-time item** fill in:
   - **Description** (at most 100 characters),
   - **Amount (+ credit, − bill)**: positive for a credit, negative for a bill, not zero,
   - **Date** (optional).
4. Click **Save**.

With the pencil in the row (**Edit item**) you change an item, and the dialog also has **Delete item** with the question **Delete this item?** and **Yes, delete**. Up to 50 items are possible per contract.

![Dialog Einmalposten hinzufügen (German interface) with the description Gebühr and the amount minus 12.5](https://raw.githubusercontent.com/wiki/weskona/tariffy/images/once-dialog.png)

*Figure: The dialog for a one-time item (German interface), here with a bill (negative amount). Sample data.*

The **date** decides from when an item counts:

- **With a date in the past or today:** It counts at once.
- **With a date in the future:** It counts only from that day.
- **Without a date:** It counts at once and belongs to the running term.
- An item dated before the contract start no longer belongs to the running term, but counts in the **Total cost**.

What a one-time item changes:

| Value | Effect |
|---|---|
| **Refund/balance due (so far)** (balance today) | plus the sum of the items of the running term |
| **Total cost** (in the panel) | minus the sum of all items: a bonus lowers, a bill raises the total cost |
| **Cost (so far)** | unchanged |
| **Refund/balance due (contract end)** and the low-instalment warning | unchanged: they stay a pure consumption calculation |

One-time items belong to the **contract**, not to a term. They stay at a tariff switch. With more than one item the block shows a row **Net** with the sum. A streaming contract only shows the block once it has items.

## Example

The contract Strom Haus from the sample data of the panel (reference date 12 July 2026) has two one-time items.

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/english-contracts.png"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/english-contracts-light.png" alt="Contracts tab with the contract Strom Haus: the block One-time items shows Wechselbonus plus 80 euros and Honorar Makler minus 25 euros, net plus 55 euros" width="100%"></picture></p>

*Figure: Contracts tab with the details of Strom Haus. The block One-time items shows the two items and their net sum.*

| Item | Date | Amount |
|---|---|---|
| Wechselbonus | 15 Jan 2026 | +80.00 € |
| Honorar Makler | 20 Jan 2026 | −25.00 € |
| **Net** | | **+55.00 €** |

```
Paid so far                               =  252.30 €
Cost (so far)                             =  513.54 €     (unchanged)
Balance without items                     = 252.30 € − 513.54 € = −261.24 €
Refund/balance due (so far)               = −261.24 € + 55.00 €  = −206.24 €
Total cost                                = 1,042.50 € + 1,166.20 € + 513.54 € − 55.00 € = 2,667.24 €
Refund/balance due (contract end)         = −495.29 €     (unchanged)
```

For the payment history the example comes from the Tariffy tests: A gas contract has run since 1 Jan 2026, today is 18 Nov 2026 (321 days). The instalment was **178 €** from January to July, **174.41 €** in August, **215 €** since September (the current one). So the dialog holds three changes: **178** in January, **174.41** in August, **215** in September.

```
Paid so far with history    = 178 € × 6.96 months + 174.41 € × 1.02 months + 215 € × 2.56 months ≈ 1,968.20 €
Paid so far without history = 215 € × 321 ÷ 30.44                                                ≈ 2,267.25 €
```

Without the history Tariffy would assume about 299 € more paid than you really paid. With the history **Refund/balance due (so far)** and the forecast **Refund/balance due (contract end)** come out correspondingly lower, and the recommendation **Instalment adjustment (recommended)** goes up.

## See also

- [Payments-and-Costs](EN-Payments-and-Costs): how cost, balance and forecast come about
- [Panel-Contracts](EN-Panel-Contracts): the Contracts tab in the panel
- [Panel-History](EN-Panel-History): earlier terms and entering old contracts by hand
- [Archive-and-History](EN-Archive-and-History)
- [Sensor-Reference](EN-Sensor-Reference)
