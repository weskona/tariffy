[🇩🇪 Deutsch](Vertrag-Kredit) · 🇬🇧 English

# Contract: Loan and Financing

The category **Loan / financing** is for annuity loans (mortgages), instalment loans and car financing. From amount, interest, term and payment interval Tariffy builds a repayment plan and shows you the remaining debt, the interest paid and the next rate.

**Contents:**
- [Loans are kept apart](#loans-are-kept-apart)
- [Step by step](#step-by-step)
- [Fields at a glance](#fields-at-a-glance)
- [How Tariffy calculates](#how-tariffy-calculates)
- [What Tariffy shows](#what-tariffy-shows)
- [Follow-up financing: renew the loan](#follow-up-financing-renew-the-loan)
- [Worked example](#worked-example)
- [Typical mistakes](#typical-mistakes)
- [See also](#see-also)

## Loans are kept apart

The loan has a **group of its own** in the panel (**Loans / financing**) and does **not** count in the totals of the contracts (instalments per month, cost so far, cost split). The panel says so: "Loans are kept apart: they do not count in the totals of the contracts." A leasing contract stands in the same group but does count in the totals, see [Contract: Leasing](EN-Contract-Leasing).

## Step by step

1. In the panel, click **New contract** in the **Contracts** tab. The general steps are on [Creating Contracts](EN-Creating-Contracts).
2. **Step 1, general data:** label (for example "Mortgage"), category **Loan / financing**, provider and **contract start**. You do not have to enter the contract end here: it follows from the start and the term.
3. **Step "Loan / financing":** enter the data the way the loan contract states it (see the table below). The rate is optional.
4. Save. There is no further cost step.

Later you change everything with **Edit contract**.

## Fields at a glance

Step 1 is described on [Contract: Internet and Mobile](EN-Contract-Internet-and-Mobile#fields-at-a-glance). The step **Loan / financing**:

| Field | Required | Meaning | Default |
|-------|----------|---------|---------|
| Loan amount (€) | yes | The amount borrowed, as stated in the contract. Must be above zero | 0 |
| Nominal interest rate (% a year) | no | Nominal rate per year. The banks calculate the rate with this one. If you leave it empty, the effective rate is used | empty |
| Effective annual interest rate (%) | no | For information and as a fallback if there is no nominal rate. **One of the two rates is needed** | empty |
| Term (months) | yes | Months from the contract start to its end; 1 to 600 | 12 |
| Payment interval | yes | Monthly, Quarterly, Half-yearly or Yearly | Monthly |
| Rate per payment (€) | no | The rate from your contract. **Empty = Tariffy calculates the annuity** | empty |
| Final payment / residual value (€) | no | An amount still open at the end and paid with the last rate (car financing) | empty |
| Date of the first payment | no | Empty = one payment interval after the start (a monthly loan: the end of the first month) | empty |

## How Tariffy calculates

- **Interest per payment** = nominal rate divided by the payments per year (monthly: 5 % gives 5 / 12 % per rate). Without a nominal rate the rate is derived from the effective annual rate.
- **Number of rates** = term divided by the payment interval in months (24 months quarterly are 8 rates).
- **Every rate** consists of interest on the remaining debt and principal; the interest share falls from rate to rate.
- **Annuity:** without an entered rate Tariffy calculates the constant rate that repays the amount down to the final payment. With an interest of 0 the repayment is in equal parts.
- **Entered rate:** it takes precedence over the calculated one. If it is **more than 1 %** away from the rate the interest gives, Tariffy reports it and shows the calculated rate.
- **Final payment / residual value:** paid with the **last rate**. If an entered rate is too low, a rest remains at the end, which is also paid with the last rate.
- **A rate counts from its date**, the rate of today counts too.
- **Not included:** special repayments and an interest rate that changes during the term.

If the amount, the term, the start or a rate of interest is missing, the loan cannot be calculated yet.

## What Tariffy shows

- **In the panel**, block **Loan**: **Remaining debt**, **Paid so far** (interest and principal), **Remaining payments** (still to pay until the end), the **Next payment** split as "interest … · principal …", the progress **Repaid** and the **Payments made**. The details add: Loan amount, Nominal interest rate, Effective interest rate, Term, Rate, Rate by the interest, Final payment at the end, Interest paid so far, Principal repaid so far, Interest over the term, Total of all payments and First payment.
- **Notes:** "The loan cannot be calculated yet: amount, term, start and an interest rate are needed." and, if your rate differs: "Your rate differs by … % from the one the interest gives (…)."
- **Sensors:** every loan has four: **Remaining debt**, **Paid so far**, **Remaining payments** and **Interest paid so far**. Attributes and entity IDs are in the [Sensor Reference](EN-Sensor-Reference).

## Follow-up financing: renew the loan

When the fixed-interest period or the loan runs out, a new loan follows. For this the loan has the icon **Renew contract** (administrators only) in the **Contracts** tab. It opens the dialog **Follow-up financing**. A loan has **no** icon for a next contract.

![Follow-up financing dialog for the loan Baufinanzierung with start, new loan amount, nominal interest rate, effective interest rate, term, payment interval, rate, final payment and first debit](https://raw.githubusercontent.com/wiki/weskona/tariffy/images/loan-renew-dialog.png)

*Figure: The dialog "Follow-up financing" for a mortgage (sample data, German interface).*

The dialog suggests:

| Field | Suggestion |
|-------|------------|
| Start | the current contract end |
| New loan amount (€) | the **remaining debt** |
| Nominal interest rate (% a year), Effective interest rate (%) | the current values |
| Term (months) | the current term |
| Payment interval | the current payment interval |
| Rate per payment (optional), Final payment (optional), First debit (optional) | empty |

You adjust amount, interest and term to the new conditions. With **Renew** the current term goes to the **history** (with amount, interest and cost) and the loan runs on with the new values. Tariffy does not take over rate, final payment and effective rate of the old term; what you leave empty counts as not set for the new loan.

## Worked example

Values from the tests: a loan of **10,000 €**, **5 % nominal rate**, **12 months**, monthly, start **15 January 2026**, no rate entered. Reference date **20 June 2026**.

```
Rate (annuity):           856.07 €
First rate:               15 Feb 2026   →  by 20 June 5 rates are due (Feb to June)
Interest of the 1st rate: 10,000 × 5 % / 12 = 41.67 €  (principal 814.40 €)

Interest so far:          174.26 €
Repaid so far:            4,106.12 €
Paid so far:              4,280.37 €   (interest plus principal)
Remaining debt:           10,000 − 4,106.12 = 5,893.88 €
Remaining payments:       5,992.52 €     (still to pay until 15 Jan 2027)
Interest over the term:   272.90 €
Total of all payments:    10,272.90 €
Next payment:             15 Jul 2026, 856.07 € (24.56 € interest · 831.52 € principal)
Progress:                 41.1 % repaid
```

Paid so far plus remaining payments give (apart from rounding to the cent) the total of all payments. If you enter 900 € instead of the calculated rate, Tariffy shows the deviation of 5.13 % and points it out because it is above 1 %.

## Typical mistakes

- **Loan amount 0.** The form refuses it: "Enter a loan amount above zero."
- **No interest rate.** The form refuses it: "Enter the nominal or the effective interest rate." Enter at least one of the two.
- **No contract start.** Without a start Tariffy cannot calculate a plan; enter it in step 1.
- **Expecting the effective rate to give the bank's rate.** The bank calculates the rate with the nominal rate. If you enter only the effective rate, Tariffy derives a rate from it. So enter the nominal rate if you can, or the rate from the contract.
- **Rate and interest do not fit.** If your rate is more than 1 % off, Tariffy shows both values. Check interest, payment interval and final payment.
- **Expecting special repayments.** Tariffy does not include special repayments, so the remaining debt can differ from the bank's.
- **Wrong payment interval.** With quarterly payment the rate per payment is the quarterly amount, not the monthly one.
- **Follow-up financing with the old rate.** In the dialog rate and final payment stay empty; leave them empty if Tariffy should calculate the new rate.

> **Good to know:** the block "Instalments paid" does not exist for the loan, its payments come from the repayment plan. One-time items can be entered for every kind of contract.

## See also

- [Contract: Leasing](EN-Contract-Leasing)
- [Contract: Other](EN-Contract-Other)
- [Next Contract or Renew](EN-Next-Contract-or-Renew)
- [Archive and History](EN-Archive-and-History)
- [Sensor Reference](EN-Sensor-Reference)
