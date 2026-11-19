[🇩🇪 Deutsch](Vertrag-Internet-und-Mobilfunk) · 🇬🇧 English

# Contract: Internet and Mobile

Internet and mobile contracts are **flat-rate contracts**: you pay a fixed amount, there is no meter and no consumption. This page shows which fields Tariffy asks for, how the costs are counted and what to keep in mind for price changes and cancellation.

**Contents:**
- [What Tariffy calculates for flat-rate contracts](#what-tariffy-calculates-for-flat-rate-contracts)
- [Step by step](#step-by-step)
- [Fields at a glance](#fields-at-a-glance)
- [Term, minimum term and cancellation](#term-minimum-term-and-cancellation)
- [Price change and introductory price](#price-change-and-introductory-price)
- [Worked example](#worked-example)
- [Typical mistakes](#typical-mistakes)
- [See also](#see-also)

## What Tariffy calculates for flat-rate contracts

The categories **Internet** and **Mobile** belong (like Streaming, Insurance and Other) to the flat-rate contracts. You choose the **payment interval** (monthly, quarterly, half-yearly, yearly) and enter the **amount per payment**. Internally Tariffy works with the amount per month (600 € a year is 50 € a month).

The **cost so far** is the **instalments booked**; there is no forecast from consumption:

- **Monthly payment:** the instalment of a month counts **from the first day of that month**, whatever day it is debited.
- **Quarterly, half-yearly, yearly:** every debit counts on the day of the payment. With the field **Date of the first debit** you set its day; the following ones come at the interval of the payment.
- Debits after the contract end already belong to the next term.

More on [Payments and Costs](EN-Payments-and-Costs).

## Step by step

1. In the panel, click **New contract** in the **Contracts** tab (or add an integration in Home Assistant under Settings → Integrations → Tariffy). The general steps are described on [Creating Contracts](EN-Creating-Contracts).
2. **Step 1, general data:** enter label, **category** (Internet or Mobile), provider, contract start, contract end, minimum term, notice period and reminder.
3. **Step 2, cost:** choose the **payment interval**, enter the **amount per payment** and, if you do not pay monthly, set **Date of the first debit**.
4. Save. The contract appears in the panel by itself.

Later you change everything with **Edit contract**: the panel shows the same two forms and asks once more before saving.

## Fields at a glance

**Step 1, general data** (the same for all categories):

| Field | Required | Meaning | Default |
|-------|----------|---------|---------|
| Label (e.g. Electricity House) | yes | Display name, shown in the device name (for example "Internet Home") | – |
| Category | yes | **Internet** or **Mobile** | Electricity |
| Provider | yes | Name of the provider | – |
| Customer number | no | Your customer number; counts as personal and is only visible to administrators in the panel | – |
| Tariff name | no | Name of the tariff | – |
| Icon | no | Own icon, for example `mdi:router-wireless`; empty = the icon of the category | empty |
| Contract start | no | The day the contract starts; Tariffy assumes the first instalment on this day | – |
| Contract end / valid until | no | Last day of the contract term | – |
| Minimum term (months) | no | The panel shows until when the contract runs at least (start plus minimum term) | – |
| Notice period (months) | no | Months before the contract end by which the cancellation must be received | – |
| Cancellation reminder | yes | "No reminder" or 1 to 4 months before | 3 months before |
| Notification target (notify service) | no | Service for the reminder, for example `mobile_app_iphone`; the field only appears if there are notify services | – |

**Step 2, cost:**

| Field | Required | Meaning | Default |
|-------|----------|---------|---------|
| Payment interval | yes | Monthly, Quarterly, Half-yearly or Yearly | Monthly |
| Amount per payment (€) | yes | The amount of one payment in the chosen interval | 0 |
| Date of the first debit | no | The day of the first debit; empty = the contract start. The following ones come at the interval of the payment | empty |

The former field **Base price (€/month)** no longer exists for new flat-rate contracts. It only appears when you edit a contract that already has a base price; there the value can be cleared.

## Term, minimum term and cancellation

- **Minimum term** is only a display in the panel ("until …"). It triggers no reminder.
- **Notice period:** if you enter it, the reminder refers to the **last day to cancel** (contract end minus notice period) instead of the contract end.
- **Cancellation reminder** sets how many months before that date Tariffy notifies you: a persistent notification in Home Assistant and, if set, a push message through the **notification target**. With the button "Confirm cancellation" you acknowledge the reminder.
- Example: contract end 31 Dec, notice period 3 months, reminder "3 months before". The cancellation must be received by 30 Sep, the message comes on 30 Jun.

All details are on [Contract End and Switching](EN-Contract-End-and-Switching).

## Price change and introductory price

For flat-rate contracts Tariffy has **no price phases** (for example "cheaper for the first 12 months"). There is one amount per payment. This is what you can do when the price changes:

- **The amount rises or falls in the middle of the term:** enter the new amount in the contract. It applies from the day you save; before that Tariffy calculates with the old one. Changing only the payment interval does not count as a price change.
- **The term ends and the price changes:** use the icon **Renew contract** (two arrows in a circle, administrators only) in the **Contracts** tab. The current term goes to the history, the contract runs on with the new start, end and amount. The panel shows at once by how many percent the contract gets dearer or cheaper (compared per month). The dialog is described on [Next Contract or Renew](EN-Next-Contract-or-Renew).
- **You already know the date of the change:** plan a next contract (icon **Plan next contract**); on the switch date Home Assistant takes it over automatically. The form asks for the amount per month ("Instalment new (€/month)"), not per payment.
- **You want to correct amounts from the past:** in the block **Instalments paid** of the contract details (dialog **Edit instalments**) you enter what was really paid. See [Payment History and One-off Items](EN-Payment-History-and-One-off-Items).
- **Switching bonus or connection fees:** the field "New customer bonus" exists for electricity only. For internet and mobile you enter a **one-time item**: a positive amount is a credit, a negative one is a bill.

## Worked example

Example values (not from a real contract): mobile contract "Phone Anna", start 1 April, monthly payment of 17.99 €, debited on the 27th each month.

On 13 November eight instalments are counted (April to November), although the November instalment is only debited on the 27th:

```
8 instalments × 17.99 € = 143.92 €   (cost so far)
```

Later the contract is renewed at the end of the term. In the renew dialog of an internet contract that has cost 39.99 € a month so far, the payment interval is "yearly" and the amount 432 € per payment. Below it the dialog shows:

```
432 € / 12 = 36.00 € a month  →  10.0 % cheaper (36.00 € instead of 39.99 € per month)
```

![Renew contract dialog for an internet contract with payment interval yearly, amount 432 and the note 10.0 % cheaper](https://raw.githubusercontent.com/wiki/weskona/tariffy/images/renew-dialog.png)

*Figure: The dialog "Renew contract" for an internet contract (sample data, German interface). Below the amount is the comparison per month.*

With **Renew** the old term goes to the history and the contract runs on with the new amount.

## Typical mistakes

- **Yearly amount entered with "Monthly".** The amount is per payment. If you pay 432 € a year, choose the payment interval **Yearly** and enter 432, not 36.
- **No contract start.** Tariffy assumes the first instalment on the contract start, so enter it.
- **The first debit differs from the contract start.** For a payment that is not monthly, set **Date of the first debit**, otherwise Tariffy counts the debits from the contract start.
- **Price raised, but only the contract end changed.** Enter the new amount or renew the contract, otherwise Tariffy keeps calculating with the old price.
- **No reminder.** "Cancellation reminder" is set to "No reminder", or no contract end is entered.
- **Forgot to confirm the cancellation.** The persistent notification stays until you press "Confirm cancellation".

> **Good to know:** the name of the contract can be changed in the first field when you edit it; sensors and entity IDs stay as they are.

## See also

- [Creating Contracts](EN-Creating-Contracts)
- [Payments and Costs](EN-Payments-and-Costs)
- [Payment History and One-off Items](EN-Payment-History-and-One-off-Items)
- [Contract End and Switching](EN-Contract-End-and-Switching)
- [Next Contract or Renew](EN-Next-Contract-or-Renew)
- [Contract: Streaming](EN-Contract-Streaming)
- [Sensor Reference](EN-Sensor-Reference)
