[🇩🇪 Deutsch](Vertrag-Streaming) · 🇬🇧 English

# Contract: Streaming

The category **Streaming** is for subscriptions such as video, music or game services. It is a **flat-rate contract** with one price per payment and has a short form of its own for the **next contract**.

**Contents:**
- [What is different from other flat-rate contracts](#what-is-different-from-other-flat-rate-contracts)
- [Step by step](#step-by-step)
- [Fields at a glance](#fields-at-a-glance)
- [The next contract in the short form](#the-next-contract-in-the-short-form)
- [Worked example](#worked-example)
- [Typical mistakes](#typical-mistakes)
- [See also](#see-also)

## What is different from other flat-rate contracts

The costs are counted as for [Internet and Mobile](EN-Contract-Internet-and-Mobile): payment interval, amount per payment, cost so far as the instalments booked. Streaming has three differences:

- **The amount is called "Price" in the panel** instead of "Instalment" (for example **Price / month**). The dialog to correct past payments is called **Edit amounts**, the block **Amounts paid**.
- **The block "One-time items" is missing** as long as the contract has none; a subscription rarely needs it. If a streaming contract already has one-time items, the block stays visible with them.
- **The row "Instalment / year" is not shown twice.**

The next contract has a shorter form, see [below](#the-next-contract-in-the-short-form).

## Step by step

1. In the panel, click **New contract** in the **Contracts** tab. The general steps are on [Creating Contracts](EN-Creating-Contracts).
2. **Step 1:** enter label, category **Streaming**, provider, tariff name (for example "Standard"), contract start and, if the subscription has a fixed term, the contract end.
3. **Step 2, cost:** choose the **payment interval** and enter the **amount per payment (€)**. If you do not pay monthly, set **Date of the first debit**.
4. Save.
5. Optional, later: in the **Contracts** tab choose the icon **Plan next contract** when the price or the payment interval changes on a known date.

## Fields at a glance

Step 1 (general data) is the same for all categories and described on [Contract: Internet and Mobile](EN-Contract-Internet-and-Mobile#fields-at-a-glance). Step 2:

| Field | Required | Meaning | Default |
|-------|----------|---------|---------|
| Payment interval | yes | Monthly, Quarterly, Half-yearly or Yearly | Monthly |
| Amount per payment (€) | yes | The amount of one payment in the chosen interval | 0 |
| Date of the first debit | no | The day of the first debit; empty = the contract start | empty |

Tariffy stores the amount per month (120 € a year is stored as 10 € a month) and shows the amount per payment again when you edit.

## The next contract in the short form

For streaming the icon **Plan next contract** opens the form **Plan next contract** with only five fields. On the start date Home Assistant takes the new term over automatically (checked daily at 00:00:01, plus the regular refresh and at Home Assistant start).

| Field | Required | Meaning |
|-------|----------|---------|
| Start of the new term | no | The **day after the contract end** is suggested, also over the turn of the year. Without a contract end there is no suggestion. A start that is already planned is not replaced by the suggestion. **Leaving it empty removes a planned contract.** |
| Tariff name (new) | no | New tariff name |
| Payment interval (new) | no | Defaults to the current interval; this is how you change, for example, from yearly to monthly |
| Amount per payment (new, €) | no | Amount per payment in the chosen interval; the amount per month is stored |
| End of the new term / valid until | no | End of the new term |

Three more fields only appear if the planned contract already has them: **Provider (new)**, **Customer number (new)** and **Base price new (€/month)**.

This is how the switch behaves:

- **Fields you leave empty keep the current value**, the payment interval too (it does not fall back to "monthly").
- **The first debit of the new term is its start.** An old entry in "Date of the first debit" is dropped.
- All other categories keep their previous form. Electricity, gas, water, internet, mobile, insurance, leasing and other still ask for provider, customer number, base price and so on.
- The planned next contract is also part of the Tariffy backup.

The form for electricity, gas, water and the other categories is described on [Next Contract or Renew](EN-Next-Contract-or-Renew).

## Worked example

Example values from the tests: streaming subscription "Standard" from Netflix, start 1 April 2026, end 31 March 2027, payment interval **Yearly**, 10 € a month, so **120 € per payment**.

You plan the change to a monthly subscription: in the form **Plan next contract** the start **2027-04-01** (day after the end) is already filled in. You enter:

| Field | Input |
|-------|-------|
| Payment interval (new) | Monthly |
| Amount per payment (new, €) | 12.99 |
| Tariff name (new) | Monatsabo |

On 1 April 2027 the new contract applies with payment interval monthly, 12.99 € and the tariff name "Monatsabo". The provider ("Netflix") stays because you did not change it.

The conversion works both ways: if you choose **Yearly** at "Payment interval (new)" and enter 120, Tariffy stores 10 € a month and shows 120 again the next time you open the form.

## Typical mistakes

- **Start left empty.** Without **Start of the new term** nothing is planned, and an existing plan is removed. The start is required for the plan.
- **Monthly amount instead of the amount per payment.** With payment interval "Yearly" you enter the yearly amount.
- **No contract end, no suggested start.** Then you have to enter the start yourself.
- **Wanting to change provider or customer number.** The short form only shows these fields if the plan already has them. If the provider or customer number changes, edit the contract after the switch with **Edit contract**.
- **Reminder forgotten.** Even a subscription needs a contract end for a cancellation reminder, see [Contract End and Switching](EN-Contract-End-and-Switching).

> **Good to know:** for a subscription without a fixed end, when the price rises use the icon **Renew contract** with an empty end or enter the new amount directly in the contract; it applies from the day you save.

## See also

- [Contract: Internet and Mobile](EN-Contract-Internet-and-Mobile)
- [Next Contract or Renew](EN-Next-Contract-or-Renew)
- [Contract End and Switching](EN-Contract-End-and-Switching)
- [Payment History and One-off Items](EN-Payment-History-and-One-off-Items)
- [Payments and Costs](EN-Payments-and-Costs)
