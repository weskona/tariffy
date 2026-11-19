[🇩🇪 Deutsch](Vertrag-Sonstiges) · 🇬🇧 English

# Contract: Other

The category **Other** is for everything that fits no other category and costs a fixed amount, for example a gym, a club fee, a newspaper or a maintenance contract. It is a plain **flat-rate contract** without special fields.

**Contents:**
- [What Other can do](#what-other-can-do)
- [Step by step](#step-by-step)
- [Fields at a glance](#fields-at-a-glance)
- [Price change and next contract](#price-change-and-next-contract)
- [Worked example](#worked-example)
- [Typical mistakes](#typical-mistakes)
- [See also](#see-also)

## What Other can do

- **Cost:** as for [Internet and Mobile](EN-Contract-Internet-and-Mobile): payment interval, amount per payment, cost so far as the instalments booked.
- **Cancellation:** contract end, notice period, minimum term and reminder as for every category.
- **Renew:** the icon **Renew contract** exists for Other too. You can also use it for a contract **without a contract end**, for example for a price adjustment (leave the end in the dialog empty).
- **Own icon:** with the field **Icon** (for example `mdi:dumbbell`) the contract gets a symbol of its own in the panel and on the sensors; empty = the icon of the category.
- **What is missing:** there are no insurance, kilometre or loan fields. If you need them, choose [Insurance](EN-Contract-Insurance), [Leasing](EN-Contract-Leasing) or [Loan](EN-Contract-Loan).

## Step by step

1. In the panel, click **New contract** in the **Contracts** tab. The general steps are on [Creating Contracts](EN-Creating-Contracts).
2. **Step 1:** enter label, category **Other**, provider, contract start and, if there is one, contract end, notice period and reminder.
3. **Step 2, cost:** choose the **payment interval**, enter the **amount per payment (€)** and, for a payment that is not monthly, set **Date of the first debit**.
4. Save.

## Fields at a glance

Step 1 is described on [Contract: Internet and Mobile](EN-Contract-Internet-and-Mobile#fields-at-a-glance). Step 2:

| Field | Required | Meaning | Default |
|-------|----------|---------|---------|
| Payment interval | yes | Monthly, Quarterly, Half-yearly or Yearly | Monthly |
| Amount per payment (€) | yes | The amount of one payment in the chosen interval (for example the yearly fee) | 0 |
| Date of the first debit | no | The day of the first debit; empty = the contract start | empty |

The field **Base price (€/month)** only appears when you edit a contract that already has one.

## Price change and next contract

- **The amount changes in the middle of the term:** enter the new amount in the contract; it applies from the day you save.
- **At the end of the term:** **Renew contract** (history with one entry per term, see [Next Contract or Renew](EN-Next-Contract-or-Renew)).
- **Known change:** **Plan next contract** opens a form that asks for: **Switch date (start of new contract)**, **Provider (new)**, **Customer number (new)**, **Tariff name (new)**, **Instalment new (€/month)**, **Base price new (€/month)** and **Contract end new / valid until**. Unlike [Streaming](EN-Contract-Streaming) the form has no payment interval, and the amount is the **amount per month**. Fields you leave empty keep the current value; an empty **Switch date** removes the planned switch.

## Worked example

Example values (not from a real contract): contract "Gym" with category **Other**, start 15 March 2026, payment interval **Yearly**, **249 €** per payment, first debit on 15 March 2026.

```
The monthly amount is stored:   249 € / 12 = 20.75 € a month
Cost so far on 20 Nov 2026:     249.00 €   (one debit)
Cost so far from 15 Mar 2027:   498.00 €   (two debits, if the contract still runs then)
```

If the contract had an end on 14 March 2027, the debit of 15 March 2027 would already belong to the next term.

## Typical mistakes

- **Amount per month instead of per payment.** With payment interval "Yearly" the yearly amount belongs in the field, not the monthly one.
- **Chose Other although a special category fits.** Electricity, gas and water (with a meter), streaming, insurance, leasing and loan have categories of their own with fitting fields.
- **Contract start missing.** Tariffy assumes the first instalment on the contract start.
- **Looking for a payment interval in the next-contract form.** It exists only for streaming; for Other you plan the amount per month.

> **Good to know:** the category can be changed when you edit. Check the fields of the new step afterwards, because every category has fields of its own.

## See also

- [Contract: Internet and Mobile](EN-Contract-Internet-and-Mobile)
- [Contract: Streaming](EN-Contract-Streaming)
- [Next Contract or Renew](EN-Next-Contract-or-Renew)
- [Payments and Costs](EN-Payments-and-Costs)
- [Creating Contracts](EN-Creating-Contracts)
