[🇩🇪 Deutsch](Vertrag-Hauskosten) · 🇬🇧 English

# Contract: House costs

The category **House costs** is for the running costs around the house that have no meter and come in fixed amounts: waste fees, street cleaning, rainwater (stormwater fee), property tax, chimney sweep, winter service and the like. It is a **flat-rate contract** with an additional **type** that you choose from a list or type freely.

**Contents:**
- [What house costs can do](#what-house-costs-can-do)
- [Step by step](#step-by-step)
- [Fields at a glance](#fields-at-a-glance)
- [What it looks like in the panel](#what-it-looks-like-in-the-panel)
- [The amount changes and the next contract](#the-amount-changes-and-the-next-contract)
- [Worked example](#worked-example)
- [Typical mistakes](#typical-mistakes)
- [See also](#see-also)

## What house costs can do

- **Type:** choose from the list **Waste fees**, **Street cleaning**, **Rainwater (stormwater fee)**, **Property tax**, **Chimney sweep**, **Winter service** or **Caretaker / building services**, or type your own (for example "Garden waste"). The type is optional and only for the overview.
- **Cost:** as for [Other](EN-Contract-Other) and [Internet and Mobile](EN-Contract-Internet-and-Mobile): payment interval (monthly, quarterly, half-yearly, yearly), amount per payment and cost so far as the instalments booked.
- **In the totals:** house costs **count**, in the instalments per month, in the cost so far and in the yearly sums, like any flat-rate contract. In the cost split they appear as a category of their own, **House costs**.
- **Group of their own:** in the panel house costs stand in a group **House costs** (after the flat-rate contracts and before the loans).
- **Wording:** for house costs the panel says **amount**, not "instalment" ("Amount / month", "Amounts paid").
- **Cancellation and renewing:** contract end (also empty), notice period and reminder as for every category. **Renew contract** also works without a contract end, for example when a fee changes (leave the end in the dialog empty).
- **Own icon:** with the field **Icon** the contract gets a symbol of its own; empty = the house symbol of the category.
- **What is missing:** there is no meter and no forecast. For water with a meter use [Water](EN-Contract-Water), for the building insurance [Insurance](EN-Contract-Insurance).

## Step by step

1. In the panel, click **New contract** in the **Contracts** tab. The general steps are on [Creating Contracts](EN-Creating-Contracts).
2. **Step 1:** enter label (for example "Waste fees"), category **House costs**, provider (for example the city or municipality), contract start and, if there is one, contract end and reminder.
3. **Step 2, type:** choose the **type of house costs** from the list or type one. You can leave it empty.
4. **Step 3, cost:** choose the **payment interval**, enter the **amount per payment (€)** and, for a payment that is not monthly, set **Date of the first debit**.
5. Save.

## Fields at a glance

Step 1 is described on [Contract: Internet and Mobile](EN-Contract-Internet-and-Mobile#fields-at-a-glance). The further steps:

| Field | Step | Required | Meaning | Default |
|-------|------|----------|---------|---------|
| Type of house costs | 2 | no | Chosen from the list or typed freely | empty |
| Payment interval | 3 | yes | Monthly, Quarterly, Half-yearly or Yearly | Monthly |
| Amount per payment (€) | 3 | yes | The amount of one payment in the chosen interval (for example a quarterly instalment) | 0 |
| Date of the first debit | 3 | no | The day of the first debit; empty = the contract start | empty |

The field **Base price (€/month)** only appears when you edit a contract that already has one.

## What it looks like in the panel

The card in the group **House costs** shows the type first, then provider and tariff, below it **Amount / month**, the payment per instalment and **Cost so far**.

<table align="center"><tr><td align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/house-costs-card.png" alt="Card Waste fees in the group House costs: amount per month 31 euro, 93 euro quarterly, cost so far 279 euro (dark design)" width="380"><br><sub>Dark</sub></td><td align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/house-costs-card-light.png" alt="Card Waste fees in the group House costs: amount per month 31 euro, 93 euro quarterly, cost so far 279 euro (light design)" width="380"><br><sub>Light</sub></td></tr></table>

*Figure: card in the overview (mock data, date 12 July 2026; the panel shows the texts in the language of Home Assistant).*

The details are in the **Contracts** tab: the type under **Contract**, the payment and the next payment under **Prices**, and on the right the **Amounts paid**.

<table align="center"><tr><td align="center" width="50%"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/house-costs-details.png" alt="Details of the contract Waste fees with type of house costs, prices, one-time items and amounts paid (dark design)" width="100%"><br><sub>Dark</sub></td><td align="center" width="50%"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/house-costs-details-light.png" alt="Details of the contract Waste fees with type of house costs, prices, one-time items and amounts paid (light design)" width="100%"><br><sub>Light</sub></td></tr></table>

*Figure: details in the Contracts tab (mock data, German texts).*

## The amount changes and the next contract

Fees often change at the turn of the year. You have three ways, as for [Other](EN-Contract-Other#price-change-and-next-contract):

- **In the middle of the term:** enter the new amount in the contract; it applies from the day you save. If the supplier debited other amounts in the past, correct them under **Enter amounts paid** ([Payment History and One-off Items](EN-Payment-History-and-One-off-Items)).
- **At the end of the term:** **Renew contract**, also without a contract end ([Next Contract or Renew](EN-Next-Contract-or-Renew)).
- **Known change:** **Plan next contract** with the form of the flat-rate contracts (switch date, provider, tariff name, amount per month and so on).

## Worked example

Example values (not from a real contract): "Waste fees" with category **House costs**, type **Waste fees**, start 1 January 2026, payment interval **Quarterly**, **93 €** per payment.

```
The monthly amount is stored:   93 € / 3 = 31.00 € a month
Cost per year:                  31.00 € × 12 = 372.00 €
Cost so far on 12 Jul 2026:     279.00 €   (three debits: 1 Jan, 1 Apr, 1 Jul)
Next payment:                   1 Oct 2026
```

## Typical mistakes

- **Monthly amount instead of the amount per payment.** With the payment interval "Quarterly" the quarterly instalment (93 €) belongs in the field, not the monthly amount (31 €).
- **House costs chosen although a meter is involved.** Water with a meter belongs in [Water](EN-Contract-Water); there Tariffy works with the consumption.
- **First debit not set.** Without it Tariffy assumes the first instalment at the contract start; if the first real debit is later, enter its date.
- **The type does not have to be "right".** It is only for the overview and changes nothing in the calculation. A type of your own is shown exactly as you typed it.

> **Good to know:** the category can be changed when editing. Check the fields of the new step afterwards, because every category has fields of its own.

## See also

- [Contract: Other](EN-Contract-Other)
- [Contract: Internet and Mobile](EN-Contract-Internet-and-Mobile)
- [Payments and Costs](EN-Payments-and-Costs)
- [Next Contract or Renew](EN-Next-Contract-or-Renew)
- [Creating Contracts](EN-Creating-Contracts)
