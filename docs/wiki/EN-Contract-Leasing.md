[🇩🇪 Deutsch](Vertrag-Leasing) · 🇬🇧 English

# Contract: Leasing

The category **Leasing** is for a car lease. The rate works like a flat-rate contract and counts in the totals. On top of that Tariffy keeps an eye on the **kilometres**: you see how much you have driven, whether you are on target and what the return will probably cost or bring.

**Contents:**
- [How leasing is set up in Tariffy](#how-leasing-is-set-up-in-tariffy)
- [Step by step](#step-by-step)
- [Fields at a glance](#fields-at-a-glance)
- [How Tariffy calculates the kilometres](#how-tariffy-calculates-the-kilometres)
- [What Tariffy shows](#what-tariffy-shows)
- [Worked example](#worked-example)
- [Typical mistakes](#typical-mistakes)
- [See also](#see-also)

## How leasing is set up in Tariffy

The form has three steps:

1. **General data** (as for all categories): **Contract start** is the start of the lease, **Contract end / valid until** is the **return date**.
2. **Leasing:** the kilometres of the contract. Everything is optional.
3. **Cost:** the rate, as for any flat-rate contract (payment interval, amount per payment, date of the first debit).

In the panel a leasing contract stands in the group **Loans / financing**. The **kilometre costs do not count** in the totals of the contract: they are an estimate for the return, not an amount paid.

## Step by step

1. In the panel, click **New contract** in the **Contracts** tab. The general steps are on [Creating Contracts](EN-Creating-Contracts).
2. **Step 1:** enter label, category **Leasing**, provider (for example the leasing bank), **contract start** and **contract end / valid until** (return date). Without these two dates Tariffy cannot spread the kilometres over the term.
3. **Step Leasing:** either choose an **Odometer sensor** or enter the **Current odometer (km)** by hand; also **Odometer at contract start (km)**, the allowed kilometres, the tolerances and the prices per kilometre.
4. **Cost:** enter the **payment interval** and the **amount per payment (€)** of the lease rate.
5. Save. Without a sensor you update the odometer from time to time with **Edit contract**.

## Fields at a glance

Step 1 and the cost step are described on [Contract: Internet and Mobile](EN-Contract-Internet-and-Mobile#fields-at-a-glance). The step **Leasing**:

| Field | Required | Meaning | Default |
|-------|----------|---------|---------|
| Licence plate | no | Counts as personal: not shown in the side panel | empty |
| Odometer sensor | no | Sensor of the car with the odometer in km (miles are converted). It takes precedence over the value entered by hand. If it is missing or not available, the entered value applies | empty |
| Current odometer (km) | no | Only if you have no sensor: enter it by hand and update it from time to time (edit the contract) | empty |
| Odometer at contract start (km) | no | Odometer reading at the start of the lease | empty = 0 |
| Allowed kilometres per year (km) | no | Kilometres per year agreed in the contract | empty |
| Allowed kilometres over the whole term (km) | no | The total of the whole term. The value takes precedence over "per year" | empty = kilometres per year times the term |
| Tolerance upwards (km) | no | Extra kilometres up to this value are not charged | empty = 0 |
| Tolerance downwards (km) | no | Kilometres not driven up to this value are not credited | empty = 0 |
| Price per extra kilometre (€) | no | Charged for each extra kilometre beyond the tolerance | empty |
| Credit per kilometre not driven (€) | no | Credited for each kilometre not driven beyond the tolerance | empty |

## How Tariffy calculates the kilometres

1. **Driven** = odometer minus the reading at contract start. The odometer comes from the sensor, otherwise from the entered value.
2. **Allowed in total** = the total value, otherwise kilometres per year times the term in days divided by 365.25.
3. **Target by now** = the allowed kilometres spread evenly over the term, counted up to today.
4. **Kilometres left** = allowed minus driven; **Allowed per day from now** = the rest divided by the days left.
5. **Projection at return** = the average per day so far, extended to the return date. It exists **only from 14 days of driving on**; before that only the plain figures are shown.
6. **Deviation** = projection minus allowed. **Extra kilometres** are what the deviation exceeds beyond the tolerance upwards. **Kilometres not driven** are what exceeds the tolerance downwards.
7. **Expected extra payment** = extra kilometres times the price per extra kilometre; **expected credit** = kilometres not driven times the credit per kilometre not driven. The **balance** is extra payment minus credit, so a credit is negative. Without prices there is no money figure.
8. **After the return date** the kilometres driven are the result.

Without a usable odometer (no sensor, no value, or a reading below the start value) Tariffy shows no kilometre figures.

## What Tariffy shows

- **In the contract card** there is a line with the kilometres driven and what the pace means at return.
- **In the details** there is the block **Leasing kilometres**: Odometer, Driven so far, Allowed in total, Target by now, Against the target, Kilometres left, Allowed per day from now, Your average per day, Projected at return, Against the allowance at return, tolerances, extra kilometres and kilometres not driven, the prices and the money figure (**Expected extra payment**, **Expected credit**, **Expected balance at return**).
- **Notes in the block:**
  - "No odometer yet: choose a sensor or enter the odometer in the contract."
  - "The projection needs at least two weeks of driving."
  - "At this pace you will be about … km over the allowance at return.", "… under the allowance at return." or "At this pace you stay within the allowance at return."
- **Sensors:** **Kilometres driven** (in km, with the attributes `km_stand`, `km_erlaubt`, `km_soll`, `abweichung_soll`, `km_rest`, `km_rest_je_tag`, `km_je_tag`, `prozent_der_erlaubten`), **Projected kilometres at return** and **Expected extra/shortfall kilometre cost**. Plus the car sensors of the insurance: **Licence plate**, **Odometer at contract start**, **Allowed kilometres per year**. The sensors exist for leasing only; their names and entity IDs are in the [Sensor Reference](EN-Sensor-Reference).

## Worked example

Values from the tests: lease at "Autobank", rate 299 € a month, start **1 January 2026**, return **1 January 2027** (365 days), odometer at contract start **20,000 km**, allowed over the whole term **12,000 km**, no tolerance, **0.10 €** per extra kilometre, **0.05 €** credit per kilometre not driven. The odometer sensor reads **26,000 km** on **1 July 2026** (day 181).

```
Driven:                  26,000 − 20,000 = 6,000 km
Target by now:           12,000 × 181 / 365 ≈ 5,951 km   → 49 km above the target
Kilometres left:         12,000 − 6,000 = 6,000 km  (about 32.6 km per day with 184 days left)
Your average:            6,000 / 181 ≈ 33.1 km per day
Projection:              6,000 / 181 × 365 ≈ 12,099 km
Extra kilometres:        12,099 − 12,000 ≈ 99 km
Expected extra payment:  99.45 km × 0.10 € ≈ 9.94 €
```

With a **tolerance upwards** of 500 km these 99 km would not be charged: extra kilometres 0, extra payment 0 €.

For kilometres not driven: if the odometer reads only 22,000 km on 1 July (2,000 km driven), the projection is about 4,033 km, that is just under 7,967 km below the allowance. With **1,000 km tolerance downwards** about 6,967 kilometres not driven count, the credit is about 348 € and the balance at return is about −348 € (negative = credit).

## Typical mistakes

- **Odometer at contract start left empty.** Then Tariffy counts from 0, and the "driven" kilometres are the whole odometer of the car. Enter the reading from when you took over the car.
- **No return date or no start.** Without both, target, projection and days left are missing. Only the kilometres driven appear, if there is an odometer reading.
- **Odometer below the start value.** Then Tariffy shows no kilometre figures at all. This happens, for example, when a sensor delivers another vehicle or a trip counter.
- **The projection is missing.** It does not exist in the first 14 days, that is intended.
- **No money figure.** Neither a price per extra kilometre nor a credit per kilometre not driven is entered.
- **Sensor and manual value at the same time.** The sensor takes precedence. If it is "unavailable", Tariffy takes the value entered by hand; hopefully you kept that one up to date.
- **Mixing up the tolerance.** "Upwards" relieves extra kilometres, "downwards" only the credit for kilometres not driven.

> **Good to know:** a **tariff switch** or a planned next contract keeps the car, the sensor and the kilometre rules; the odometer at the start and the value entered by hand belong to the old term and are dropped. With **Renew contract** the figures stay as they are: check the start odometer and the allowance in **Edit contract** if the new lease is another car.

## See also

- [Contract: Loan](EN-Contract-Loan)
- [Contract: Insurance](EN-Contract-Insurance)
- [Contract: Internet and Mobile](EN-Contract-Internet-and-Mobile)
- [Next Contract or Renew](EN-Next-Contract-or-Renew)
- [Sensor Reference](EN-Sensor-Reference)
- [Panel: Contracts](EN-Panel-Contracts)
