[🇩🇪 Deutsch](Panel-Kosten) · 🇬🇧 English

# Panel: Costs

The **Costs** tab shows at the top how your costs split between categories and contracts, and below it one table each for metered and flat-rate contracts with totals. It is view only: you edit in the tab [Panel contracts](EN-Panel-Contracts).

**Contents:**
- [Cost split](#cost-split)
- [The tables](#the-tables)
- [Loans](#loans)
- [Example: the share of gas](#example-the-share-of-gas)
- [On a phone](#on-a-phone)
- [See also](#see-also)

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/english-costs.png"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/english-costs-light.png" alt="Costs tab: the cost split with ring chart and legend on top, below it the tables for metered contracts, flat-rate contracts and loans" width="100%"></picture></p>

*Figure: The Costs tab on the desktop (mock data of 12 July 2026).*

## Cost split

At the top is the **cost split**: a **ring chart** with the total in the middle and a legend next to it with amount and share per entry. Below it a bar shows the split between **consumption contracts** and **flat-rate contracts**. Three switches control the chart:

| Switch | Choice | Effect |
|---|---|---|
| Period | **Cost so far** / **Per year** | "Cost so far" counts what has accrued until today. "Per year" projects the instalment to one year (for example Gas Heizung 140.00 € × 12 = 1,680.00 €). |
| **Year** | **Current** or a calendar year | Shows the cost of a calendar year, for every year with data, also from the history and from archived contracts. A term spanning several years counts for its days in each year. A note says "The cost of this calendar year; earlier terms count for their days in it." |
| Grouping | **By category** / **By contract** | "By category" adds up contracts of one category (two internet contracts become "Internet (2)"). "By contract" shows each on its own. |

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/cost-chart-sparte.png" alt="Cost split by category for cost so far: gas, Internet (2), electricity, electricity HT/NT, mobile and water with amount and percent" width="100%"></p>

*Figure: "By category" and "Cost so far": contracts of the same category are added up, here Internet (2). Other mock data with a second internet contract; the labels are German in this screenshot.*

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/cost-chart.png" alt="Cost split by contract for per year: Gas Heizung 1,680 euro, Strom Wohnung 660 euro, Strom Haus 480 euro and more contracts" width="100%"></p>

*Figure: "By contract" and "Per year": each contract on its own, projected to one year; the labels are German in this screenshot.*

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/cost-chart-year.png" alt="Cost split by contract for the year 2025 with the note that earlier terms count for their days" width="100%"></p>

*Figure: The year selection shows the cost of a calendar year, here 2025, also from earlier terms and from the archived contract Strom Altvertrag; the labels are German in this screenshot.*

If there are no values yet, it says "Nothing to show yet."

## The tables

Below the chart are two tables like in the overview. Both share one column grid, so "Cost so far" and "Instalment" sit exactly below each other.

**Metered contracts:**

| Column | Meaning |
|---|---|
| **Contract** | Name and provider. |
| **Cost so far** | The cost until today, from the measured consumption. |
| **Balance today** | Credit (plus) or balance due (minus) until today. |
| **At contract end** | The forecast at contract end, projected from the consumption so far. |
| **Instalment** | The current instalment per month. |
| **Recommended** | The recommended instalment. If a credit already covers the costs it shows "0.00 €" with "Credit covers the costs". |

With a dual-tariff meter (electricity HT/NT) two rows appear below the contract, **High tariff** and **Low tariff**, with consumption and cost (900 kWh = 288.00 € and 600 kWh = 126.00 €).

**Flat-rate contracts:** **Cost so far** (the payments booked until today), **Remaining**, **Contract end** and **Instalment** (with the yearly figure below, for example "480 € / year"). There is no balance or forecast.

Each table has a **Total** row; below them the row **Overall** shows the overall total. A note under the tables reminds you of the signs: "Positive = credit, negative = balance due. "At contract end" is projected from the consumption so far. For flat-rate contracts the cost so far is the instalments due until today."

> **Good to know:** How the cost is counted for flat-rate contracts paid in advance (quarterly, half-yearly, yearly) is in [Payments and costs](EN-Payments-and-Costs). One-off items go into the total cost, not into the forecast ([Payment history and one-off items](EN-Payment-History-and-One-off-Items)).

## Loans

Loans have a **table of their own**, "Loans / financing", with the columns **Paid so far**, **Remaining debt**, **Remaining payments**, **Instalment** and **Interest over the term**. The note below says: "Loans are kept apart: they do not count in the totals of the contracts." More about loans in [Loan contract](EN-Contract-Loan).

## Example: the share of gas

In the mock data the sum of **Cost so far** is 2,791.24 € (metered contracts 2,151.46 € plus flat-rate contracts 639.78 €). The gas contract **Gas Heizung** has 991.76 € cost so far:

1. You open the tab **Costs**.
2. You keep **Cost so far** and **By category** selected.
3. The legend reads "Gas 991.76 € 35.5 %". That is 991.76 € ÷ 2,791.24 € = 35.5 %.

With **By contract** and **Per year** you see the instalment projected to a year instead: at 140.00 € a month Gas Heizung costs 1,680.00 € a year.

## On a phone

On narrow screens the legend sits below the ring, and each contract of the tables becomes a card with one row per column (Cost so far, Balance today, At contract end, Instalment, Recommended). The totals are cards of their own below.

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-costs.png"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-costs-light.png" alt="Costs tab on a phone: cost split and tables one below the other" width="300"></picture></p>

*Figure: The Costs tab on a phone; the labels are German in this screenshot.*

## See also

- [Panel overview](EN-Panel-Overview): the tiles and cards.
- [Panel contracts](EN-Panel-Contracts): details and actions.
- [Payments and costs](EN-Payments-and-Costs): how the cost is counted.
- [Sensor reference](EN-Sensor-Reference): the same values as sensors.
