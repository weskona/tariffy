[🇩🇪 Deutsch](Panel-Historie) · 🇬🇧 English

# Panel: History

The **History** tab shows what used to be: the **earlier terms** of every contract and the **archived contracts**. Here, as an administrator, you also add an old contract by hand. All users may look at the tab.

**Contents:**
- [What the tab shows](#what-the-tab-shows)
- [Earlier terms](#earlier-terms)
- [Archived contracts](#archived-contracts)
- [Add an old contract](#add-an-old-contract)
- [Total cost](#total-cost)
- [Example: Strom Haus](#example-strom-haus)
- [When the history is empty](#when-the-history-is-empty)
- [On a phone](#on-a-phone)
- [See also](#see-also)

## What the tab shows

At the top right administrators see the button **Add an old contract**. Below it are two groups: **Archived contracts** and **Earlier terms**. Each group has one table per contract with the columns **Term** (with provider and tariff below), **Instalment**, **Cost**, **Consumption** and **Balance**. Administrators see a pencil at the end of the row to edit it.

<table align="center"><tr><td align="center" width="50%"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/english-history.png" alt="History tab: at the top right the button Add an old contract, below it the archived contract Strom Altvertrag with two terms and the button Restore, then the earlier terms of Strom Haus (dark design)" width="100%"><br><sub>Dark</sub></td><td align="center" width="50%"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/english-history-light.png" alt="History tab: at the top right the button Add an old contract, below it the archived contract Strom Altvertrag with two terms and the button Restore, then the earlier terms of Strom Haus (light design)" width="100%"><br><sub>Light</sub></td></tr></table>

*Figure: The History tab (mock data of 12 July 2026).*

## Earlier terms

When the next contract takes over on its planned date, Tariffy replaces the contract data. The old term is saved first, with its term, provider, tariff, prices, instalment, cost, consumption and balance at the end, and then shown here under the contract. **Renew contract** for flat-rate contracts also creates one entry per renewal (term, provider, tariff, instalment, instalments paid), so you see how the premium rises.

- There are no entries for terms that are already over; the history starts with the first switch after the update.
- At most 50 terms per contract are kept.
- Customer and meter numbers are not part of them.
- The colour of the **Balance** shows the direction: green is credit (+37.50 €), red is balance due (−146.20 €).

## Archived contracts

A contract whose end has passed and that has no next contract gets the badge **Expired** in the overview. In the tab [Panel contracts](EN-Panel-Contracts) you archive it with the button **Archive** (administrators, asks first). Then it appears here under **Archived contracts** with the badge **Archived**; its last term is already in the table and is not counted twice.

- It leaves the overview, the costs, the contracts and the totals; its reminders and warnings are off.
- Nothing is deleted: the sensors and their statistics stay.
- With **Restore** (administrators, asks "Bring this contract back to the overview?" with **Yes, restore**) the contract is back in the overview.
- Nothing is archived automatically. If all contracts are archived, the overview says: "All contracts are archived. You find them in the History tab."

Background in [Archive and history](EN-Archive-and-History).

## Add an old contract

With the button **Add an old contract** (administrators only) you create an earlier term, for example a contract from two years ago. The pencil in its row edits it; it can be deleted there too ("Delete this term from the history?" with **Yes, delete**).

You pick the **contract** the term belongs to (meter and category come from it) and enter **Start** and **End**, and optionally **Provider**, **Tariff**, **Price per unit (€)**, **Base price per month (€)** and **Instalment per month (€)**. **Consumption, cost, instalments paid and balance are worked out automatically** where possible:

| Value | Where it comes from |
|---|---|
| **Consumption** | From the long-term statistics of the meter in Home Assistant, between start and end. If there are no statistics for that time you enter it yourself. |
| **Cost (€)** | From consumption, price and base price (gas with the calorific value and state number of the contract). For flat-rate contracts the cost is what was paid. |
| **Instalments paid (€)** | From the instalment and the duration. |
| **Balance (€)** | From instalments paid and cost. |

The grey fields show the calculated value and where it comes from ("Automatic, from the statistics of ...", "Calculated", "Entered by you", "No statistics for this term, please enter it"). **You can type your own value into any field**, it then takes precedence and the rest follows from it. When you edit a term, the values you did not type are calculated again. Nothing is saved until you click **Save**.

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/term-dialog.png" alt="Dialog Add an old contract for Strom Haus: start 01.01.2024, end 31.12.2024, unit price 0,30, base price 10, instalment 90, consumption 3000 entered by hand, cost 1.019,90, instalments paid 1.079,10 and balance 59,20 as calculated grey fields" width="520"></p>

*Figure: The dialog "Add an old contract" (German labels in this screenshot). The consumption (3000) is entered by hand, cost, instalments paid and balance are calculated.*

- If the old contract had another tariff name or other prices, just enter them.
- Tiered prices, dynamic prices and separate prices for high and low tariff are not calculated; enter the cost yourself.
- Below the fields is the area **Instalments by payment (optional)** with one field per payment of the term (from start, end and the payment interval of the contract). If you enter something there, **Paid** and the **balance** of the term are calculated from it (for metered contracts pro rata by days, for flat-rate contracts payment by payment); a value you typed yourself under "Instalments paid" takes precedence. The amounts stay stored and appear again when you edit the term. If the area stays empty, the term uses the single instalment. More in [Payment history and one-off items](EN-Payment-History-and-One-off-Items).
- Possible messages: "The end must not be before the start.", "The history is full (50 terms).", "This term does not exist any more.", "One of the numbers is not valid."

## Total cost

If a contract has a history (because you renewed it, the next contract took over or you entered old terms), Tariffy shows the **total cost** over all terms: the earlier terms plus the running one. In the History tab the line stands under the table, each with "since <date> · n terms"; it is also in the overview and in the contract details.

- For an earlier term its cost counts if there is one, otherwise the instalments paid.
- If a term has neither, it says "at least ...", because the sum is not complete.
- For an archived contract the last term is already in the history and is not counted twice.
- One-off items (bonus, bill) go into the total cost.
- Without a history and without one-off items there is no extra display.

## Example: Strom Haus

In the mock data **Strom Haus** has two earlier terms. The table shows:

| Term | Instalment | Cost | Consumption | Balance |
|---|---|---|---|---|
| 01.01.2025 – 31.12.2025 | 85.00 € | 1,166.20 € | 3,340 kWh | −146.20 € |
| 01.01.2024 – 31.12.2024 | 90.00 € | 1,042.50 € | 3,210 kWh | +37.50 € |

The balance is instalments paid minus cost: 12 × 85.00 € = 1,020.00 € paid against 1,166.20 € cost gives −146.20 €; 12 × 90.00 € = 1,080.00 € against 1,042.50 € gives +37.50 €. Under the table it says "Total cost 2,667.24 € · since 01.01.2024 · 3 terms". That is the two earlier terms (1,166.20 € + 1,042.50 €) plus the running one (513.54 €), less the one-off items of this contract (net +55.00 €, so a credit): 2,208.70 € + 513.54 € − 55.00 € = 2,667.24 €.

The archived contract **Strom Altvertrag** (Stadtwerke Süd) also has two terms, together 1,725.40 € ("since 01.01.2022 · 2 terms"), and the button **Restore**.

## When the history is empty

If you have had no next contract and have not archived a contract, you see "No history yet" with the text "The earlier terms of a contract appear here once the next contract takes over. Archived contracts appear here too." Administrators can still add terms with **Add an old contract**.

## On a phone

On a phone the rows of the tables stand as cards one below the other, the buttons stay in place.

<table align="center"><tr><td align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-history.png" alt="History tab on a phone: archived contract and earlier terms one below the other (dark design)" width="300"><br><sub>Dark</sub></td><td align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-history-light.png" alt="History tab on a phone: archived contract and earlier terms one below the other (light design)" width="300"><br><sub>Light</sub></td></tr></table>

*Figure: The History tab on a phone (German labels in this screenshot).*

## See also

- [Panel contracts](EN-Panel-Contracts): archive, renew and plan the next contract.
- [Archive and history](EN-Archive-and-History): archive and history in context.
- [Next contract or renew](EN-Next-Contract-or-Renew): when a term goes into the history.
- [Payment history and one-off items](EN-Payment-History-and-One-off-Items): instalments by payment and one-off items.
- [Panel backup](EN-Panel-Backup): the history is part of the backup too.
