[🇩🇪 Deutsch](Vertrag-Gas) · 🇬🇧 English

# Contract gas

Here you find all fields of a gas contract and the conversion from cubic metres to kilowatt hours through the calorific value and the state number. You need both values from your gas bill.

**Contents:**

- [How Tariffy calculates gas](#how-tariffy-calculates-gas)
- [The form fields](#the-form-fields)
- [Converting cubic metres to kWh](#converting-cubic-metres-to-kwh)
- [Meter sensor and units](#meter-sensor-and-units)
- [Worked example](#worked-example)
- [Typical mistakes](#typical-mistakes)

## How Tariffy calculates gas

The **Unit price** of a gas contract is per **kWh**, but your meter usually counts in **m³**. Tariffy measures the consumption in the unit of the meter and converts to kWh only for the cost:

```
Consumption (so far)      = current meter value − meter value at contract start   (in m³)
Consumption in kWh        = Consumption (so far) × calorific value × state number
Cost (so far)             = consumption in kWh × unit price + base price × months elapsed
```

Balance and forecast are calculated like for electricity (a month counts as 30.44 days); the formulas are at [Contract electricity](EN-Contract-Electricity#how-tariffy-calculates). The sensor **Consumption (so far)** still shows the meter difference in m³, not in kWh.

## The form fields

The second form is called **Gas details** ("Prices, usage (m³) and conversion to kWh via calorific value and state number.").

| Field | Required | Description |
|---|---|---|
| Gas unit | yes | Unit used on your gas bill: `m³`, `CCF`, `therm`, `ft³`, `MBtu` or `kWh` (default `m³`). |
| Unit price (€/kWh) | yes | Price per kWh of gas, found on your gas bill. |
| Base price (€/month) | yes | Fixed monthly charge regardless of consumption. |
| Monthly instalment (€/month) | yes | Monthly advance payment to the provider. |
| Estimated annual usage (m³) | no | Estimate in the chosen unit. It becomes the sensor **Annual usage (kWh)**. Cost so far and forecast use the measured consumption. |
| Consumption sensor (optional) | no | Sensor of your gas meter; enables real consumption tracking. |
| Meter reading at contract start (optional) | no | Your exact meter reading on the contract start date, if you know it. Takes priority over automatic detection. |
| Calorific value (kWh/m³) | yes | Calorific value Hs in kWh per unit, printed on your gas bill (default 11.0). |
| State number (Z) | yes | Conversion factor Z for gas volume, printed on your gas bill (usually 0.9 to 1.0; default 0.95). |
| Warn if instalment is too low | no | Off by default. Works as described at [Contract electricity](EN-Contract-Electricity#the-form-fields). |
| Warning threshold (€ balance due) | no | Default 50. |
| Sign-up bonus (€) | no | Stored, but does not enter the cost. For a bonus in the balance use a one-off item. |
| Green energy | yes | Yes or no, for documentation only (the field has this name for gas too). |
| Meter number | no | For documentation. |
| Market location (MaLo) / metering point | no | For documentation. |
| Price guarantee until | no | Date until which the unit price is guaranteed. |

Depending on the country set in Home Assistant the fields for **tiered prices** and the **night rate** are added. They work as for electricity and are described at [Contract electricity](EN-Contract-Electricity#tiered-prices). Dynamic tariff, feed-in tariff, PV self-sufficiency and the dual tariff do not exist for gas.

> **Good to know:** **Calorific value** and **State number** are text fields. You can enter them with a decimal point (`11.2`) or a decimal comma (`11,2`). Anything else reports "Not a valid number. Use a dot or comma as the decimal separator (e.g. 11.2 or 11,2)."

## Converting cubic metres to kWh

For the units `m³`, `CCF` and `ft³`:

```
kWh = quantity × calorific value × state number
```

- The **calorific value** (Hs) says how much energy one unit of gas holds (about 10 to 12 kWh per m³).
- The **state number** (Z) converts the gas volume to the standard state (about 0.95).

For `therm`, `MBtu` and `kWh` Tariffy converts the **annual usage estimate** with fixed factors and needs no calorific value for that: 1 therm = 29.3071 kWh, 1 MBtu = 293.071 kWh, 1 kWh = 1 kWh.

The conversion of the estimate is shown by the sensor **Annual usage (kWh)** (icon `mdi:fire`). Its attributes name the estimate in m³, the calorific value and the state number.

> **Good to know:** The cost calculation from the metered consumption (**Cost (so far)**, forecast, recommended instalment) always multiplies by **calorific value × state number** as soon as both are entered, also for `therm`, `MBtu` and `kWh`. Both fields are required in the form. If your meter already reports in kWh, enter a calorific value of 1 and a state number of 1 so that the conversion changes nothing.

## Meter sensor and units

- The **Consumption sensor** delivers the meter reading, for example in m³. Tariffy reads the value at contract start and the current value from it, as described at [Measuring consumption](EN-Measuring-Consumption). Gas meters that jump back now and then are handled as well.
- The sensors **Consumption (so far)**, **Consumption (contract term projected)** and **Consumption (last period)** show the unit of the meter sensor if it has one, otherwise the chosen **Gas unit**. If the meter reports in Wh or MWh, kWh is shown there.
- The **Unit price** has the unit "currency per kWh".

## Worked example

A gas contract with unit price 0.10 €/kWh, base price 10.00 €/month, instalment 80 €/month, gas unit m³, calorific value 11.2, state number 0.95. Term 01.01. to 31.12.2026, today is 12 July 2026 (day 192, so 6.3075 months). The meter read 1,000 m³ at contract start and reads 1,100 m³ now. The numbers come from the tests (`tests/test_coordinator.py`); they are example values.

```
Consumption (so far)            = 1,100 − 1,000                         = 100 m³
Consumption in kWh              = 100 × 11.2 × 0.95                     = 1,064 kWh
Cost (so far)                   = 1,064 × 0.10 + 10.00 × 6.3075         =   169.47 €
Instalments due so far          = 80 × 6.3075                           =   504.60 €
→ Refund/balance due (so far)   ≈ 504.60 − 169.47                       =  +335.12 €  (credit)
```

And the projection onto the term (364 days, 11.958 months):

```
Consumption projected           = 100 ÷ 192 × 364                       = 189.6 m³
Consumption projected in kWh    = 189.6 × 11.2 × 0.95                   = 2,017.3 kWh
Estimated cost at the end       = 2,017.3 × 0.10 + 10.00 × 11.958       =   321.31 €
Instalments of the whole term   = 80 × 11.958                           =   956.64 €
→ Refund/balance due (contract end) ≈ 956.64 − 321.31                   =  +635.32 €
```

So the instalment in the example is clearly too high. The test checks the cost so far; the forecast follows the same formula as for electricity.

The estimate in the form is converted the same way: 1,000 m³ annual usage × 11.2 × 0.95 gives 10,640 kWh in the sensor **Annual usage (kWh)**.

## Typical mistakes

| Problem | Cause and solution |
|---|---|
| The consumption is in m³, the cost is calculated in kWh | This is intended: **Consumption (so far)** shows the meter difference, only the cost goes through calorific value × state number. |
| "Not a valid number." when saving | Calorific value or state number contain something other than digits with a dot or comma. |
| The cost is about ten times too high with a kWh meter | Calorific value and state number multiply in that case too. For a meter in kWh enter both values as 1. |
| The cost does not match the bill | Calorific value and state number change at the supplier over time. Enter the values of your current bill. For a new contract with other values create a [next contract](EN-Next-Contract-or-Renew) with **Calorific value new** and **State number new**. |
| Consumption is unknown | The statistics of the sensor do not reach back to the contract start. Enter the **Meter reading at contract start (optional)**. |
| No sensor **Annual usage (kWh)** with a value | It needs the **Estimated annual usage (m³)** and, for m³, CCF and ft³, the calorific value. |

## See also

- [Creating contracts](EN-Creating-Contracts)
- [Contract electricity](EN-Contract-Electricity)
- [Measuring consumption](EN-Measuring-Consumption)
- [Payments and costs](EN-Payments-and-Costs)
- [Next contract or renew](EN-Next-Contract-or-Renew)
- [Sensor reference](EN-Sensor-Reference)
- [Troubleshooting](EN-Troubleshooting)
