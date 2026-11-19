[🇩🇪 Deutsch](Vertrag-Strom) · 🇬🇧 English

# Contract electricity

This page explains all fields of an electricity contract (categories **Electricity** and **Electricity (dual tariff, HT/NT)**), how Tariffy works out cost, balance and forecast from them, and what applies to the dual tariff, night rate, dynamic tariff, feed-in tariff and tiered prices.

**Contents:**

- [How Tariffy calculates](#how-tariffy-calculates)
- [The form fields](#the-form-fields)
- [Meter sensor and units](#meter-sensor-and-units)
- [Dual tariff HT/NT](#dual-tariff-htnt)
- [Day and night tariff](#day-and-night-tariff)
- [Dynamic tariff](#dynamic-tariff)
- [Feed-in tariff](#feed-in-tariff)
- [Tiered prices](#tiered-prices)
- [Worked example](#worked-example)
- [Typical mistakes](#typical-mistakes)

## How Tariffy calculates

With a **Consumption sensor** Tariffy measures the consumption since contract start and works out (a month counts as 30.44 days):

```
Consumption (so far)          = current meter value − meter value at contract start
Cost (so far)                 = consumption so far × unit price + base price × months elapsed
Refund/balance due (so far)   = instalments due until today − Cost (so far)
Consumption projected         = consumption so far ÷ days elapsed × days of the contract term
```

The contract term is contract end minus contract start in days (365 days if no contract end is entered). The forecast at contract end sets the projected cost against the instalments of the whole term. **Plus is credit, minus is balance due.** The four cost sensors are explained in the [Sensor reference](EN-Sensor-Reference), the measuring itself in [Measuring consumption](EN-Measuring-Consumption), the instalment in [Payments and costs](EN-Payments-and-Costs).

## The form fields

The second form is called **Electricity details** ("Prices, usage and meter data."). For the dual tariff it is called **Electricity details (dual tariff, HT/NT)**.

| Field | Required | Description |
|---|---|---|
| Unit price (€/kWh) | yes | Price per kWh consumed, found on your bill. Also used as a fallback while no statistics exist yet for the price sensor. For the dual tariff the field is called **Unit price, high tariff / HT (€/kWh)**. |
| Dynamic tariff price sensor (optional) | no | Sensor with the spot-market price, see [Dynamic tariff](#dynamic-tariff). |
| Dynamic tariff markup (€/kWh) | no | Fixed markup on the price of the price sensor. |
| Base price (€/month) | yes | Fixed monthly charge regardless of consumption. |
| Monthly instalment (€/month) | yes | Monthly advance payment to the provider. |
| Estimated annual usage (kWh) | no | Estimate in kWh. It serves as input for the display with tiered prices and night rate and appears as an attribute of the sensor **Unit price**. Cost so far and forecast use the measured consumption, not this estimate. |
| Consumption sensor (optional) | no | Sensor of your electricity meter; enables real consumption tracking. For the dual tariff this is the high-tariff register. |
| Meter reading at contract start (optional) | no | Your exact meter reading on the contract start date, if you know it (for example from your bill). Takes priority over automatic detection. Helps if the statistics of the sensor do not reach back to the contract start. |
| Warn if instalment is too low | no | Off by default. If the option is on and the forecast at contract end is below zero by more than the threshold, Tariffy reports it as a Home Assistant notification (and through the notification target, if one is entered) until you acknowledge it with **Confirm low-instalment warning**. |
| Warning threshold (€ balance due) | no | Default 50. |
| Take PV self-sufficiency into account | no | Optional, for the remaining term only. Together with **Total consumption of the house (sensor)**, **Self-sufficiency sensor (%)** or **Self-sufficiency, own values (%)**. For the dual tariff additionally **Total consumption, low-tariff period (sensor)**. All of it at [PV self-sufficiency](EN-PV-Self-Sufficiency). |
| Feed-in tariff (per kWh, optional) | no | See [Feed-in tariff](#feed-in-tariff). |
| Sign-up bonus (€) | no | One-time bonus from the provider. The value is stored and shown as the attribute `bonus` of the sensor **Unit price**, but it does not enter the cost. For a bonus that should change the balance, use a one-off item, see [Payment history and one-off items](EN-Payment-History-and-One-off-Items). |
| Green energy | yes | Yes or no, for documentation only (attribute `oekostrom`). |
| Meter number | no | For documentation. For the dual tariff this is the high-tariff register. |
| Market location (MaLo) / metering point | no | For documentation. |
| Price guarantee until | no | Date until which the unit price is guaranteed (attribute `preisgarantie_bis`). |

Only for the dual tariff these fields are added (see below): **Unit price, low tariff / NT (€/kWh)**, **Consumption sensor, low tariff / NT (optional)**, **Meter reading at contract start, NT (optional)** and **Meter number, low tariff / NT**.

Depending on the country set in Home Assistant the form also shows **Enable tiered/block pricing** with the blocks and, for electricity (not for the dual tariff), the **night rate**. Both are described in their own sections below.

> **Good to know:** Prices, instalment and base price are number fields. The unit of the prices is the currency of your Home Assistant installation per kWh.

## Meter sensor and units

- The **Consumption sensor** must be a sensor with a long-term statistic that keeps the cumulative sum (a meter sensor like the one the Energy dashboard uses). Tariffy reads the value at contract start and the current value from it.
- If the sensor reports in **Wh** or **MWh**, Tariffy converts the consumption to **kWh** (Wh × 0.001, MWh × 1000). Other units stay unchanged. A manual **Meter reading at contract start** is entered in the unit of the meter.
- The sensor **Consumption (so far)** always shows kWh for electricity.
- If the sensor is briefly unavailable, Tariffy uses the last recorded statistic value with a manual meter reading, so that the sensors do not fall to "unknown".

More on the meter reading methods and meter resets is at [Measuring consumption](EN-Measuring-Consumption).

## Dual tariff HT/NT

The category **Electricity (dual tariff, HT/NT)** is for a meter with two registers: high tariff (HT) and low tariff (NT). Each register has its own unit price, its own consumption sensor, its own manual start value and its own meter number.

- Tariffy calculates both registers separately: **Consumption, high tariff (so far)** and **Consumption, low tariff (so far)** in kWh, plus **Cost, high tariff (so far)** and **Cost, low tariff (so far)** (without a base price share).
- For the other sensors (cost, balance, forecast, recommended instalment) Tariffy uses a **weighted average price** of both registers, weighted with the measured consumption. **Consumption (so far)** is the sum of both registers.
- If the low-tariff sensor is missing or has no value yet, Tariffy only uses the high-tariff price.
- Additional sensors exist only for this category: **Unit price (low tariff / NT)**, **Meter number (low tariff / NT)** and the four high-tariff/low-tariff sensors for consumption and cost.
- The night rate (Economy 7) belongs to **Electricity**, not to the dual tariff.

## Day and night tariff

For countries with day/night tariffs (Economy 7, time of use) the form shows three fields: **Night rate (e.g. Economy 7, TOU off-peak)**, **Annual daytime usage** and **Annual night-time usage**. They appear when one of these countries is set in Home Assistant: GB, US, CA, AU, NZ, IE. The **Unit price** is then the day price.

If all three fields are filled in, the sensor **Unit price (night)** exists. Its attributes show the annual usages and `tou_jahreskosten`, which is day usage × unit price + night usage × night price. This number is a display. **Cost (so far)** keeps using the measured consumption and the one unit price.

If you have a meter with two registers, use the [dual tariff](#dual-tariff-htnt).

## Dynamic tariff

With a dynamic tariff (Tibber, aWATTar, Nordpool and similar) you enter a price sensor instead of a fixed price:

1. In the field **Dynamic tariff price sensor (optional)** choose the sensor with the current spot-market price.
2. In **Dynamic tariff markup (€/kWh)** enter your fixed markup (for example the margin of the provider).
3. Leave the **Unit price** as a fallback value.

Tariffy then replaces the unit price with the **average of the price sensor since contract start** (from the long-term statistics, hourly means) **plus the markup**. If no statistics exist yet, the entered unit price stays. The sensor **Unit price** shows this average price, gets the icon `mdi:chart-line` and has two attributes: `arbeitspreis_aktuell` (current live price plus markup) and `dynamischer_tarif`.

> **Good to know:** The average is a simple mean of the hourly values, not weighted by your consumption. Tariffy does not convert the sensor value; it has to deliver the price in the currency per kWh, like the markup.

## Feed-in tariff

The field **Feed-in tariff (per kWh, optional)** stores the remuneration for electricity fed into the grid (for example with photovoltaics). It is available everywhere and shown as the sensor **Feed-in tariff**. Tariffy calculates **nothing** with it: there is no revenue calculation and the cost does not change.

## Tiered prices

Tiered prices (blocks with a rising price) exist only for the countries US, CA, AU, NZ, ES, PT, IT, GR, IL, IN, BR, MX, ZA, CN, JP, KR. There **Enable tiered/block pricing** and up to five blocks appear, with **Block 1 limit** and **Block 1 price** up to **Block 5 limit** and **Block 5 price**. If you leave the limit of a block empty, that block applies to all the rest. A block without a price ends the list.

Tariffy uses them to work out the annual cost for your **Estimated annual usage (kWh)** and shows it with the average price in the sensor **Unit price (effective)**. Example from the tests: block 1 up to 1,000 kWh at 0.10 €, block 2 above at 0.20 €, annual usage 1,500 kWh. That gives 1,000 × 0.10 + 500 × 0.20 = 200 €, so 0.1333 €/kWh effective. This is a display too; **Cost (so far)** and the forecast stay with the unit price.

## Worked example

The example contract "Strom Haus": instalment 40 €/month, unit price 0.2977 €/kWh, base price 11.51 €/month, term 01.01. to 31.12.2026 (364 days, 11.958 months). Today is 12 July 2026, so day 192 (6.3075 months). The meter read 1,000 kWh at contract start and reads 2,481.17 kWh now. The numbers are those of the test case in `tests/test_coordinator.py`; they are mock data.

```
Consumption (so far)                   = 2,481.17 − 1,000                      = 1,481.17 kWh
Cost (so far)                          = 1,481.17 × 0.2977 + 11.51 × 6.3075    =   513.54 €
Instalments due so far                 = 40 × 6.3075                           =   252.30 €
→ Refund/balance due (so far)          = 252.30 − 513.54                       =  −261.24 €  (balance due)

Consumption projected                  = 1,481.17 ÷ 192 × 364                  = 2,808.1 kWh
Installment total (contract term)      = 40 × 11.958                           =   478.32 €
Estimated cost at contract end         = 2,808.1 × 0.2977 + 11.51 × 11.958     =   973.61 €
→ Refund/balance due (contract end)    = 478.32 − 973.61                       =  −495.29 €  (balance due, forecast)
```

(The months are days ÷ 30.44: 192 ÷ 30.44 = 6.3075 and 364 ÷ 30.44 = 11.958.)

The consumption is well above what the instalment covers: the balance due grows from −261 € today to a forecast −495 € at contract end. The panel shows the same values on the card "Strom Haus".

### Example dual tariff

A contract with high tariff at 0.30 €/kWh and low tariff at 0.20 €/kWh, base price 11.51 €/month, instalment 40 €/month, same term and same day as above. Since the start 300 kWh were measured in the high tariff and 300 kWh in the low tariff (numbers from the tests):

```
Cost, high tariff (so far)  = 300 × 0.30                                  =  90.00 €
Cost, low tariff (so far)   = 300 × 0.20                                  =  60.00 €
Consumption (so far)        = 300 + 300                                   = 600 kWh
Weighted unit price         = (300 × 0.30 + 300 × 0.20) ÷ 600             = 0.25 €/kWh
Cost (so far)               = 600 × 0.25 + 11.51 × 6.3075                 = 222.60 €
```

The instalments so far (252.30 €) give a credit of about +29.70 € here.

## Typical mistakes

| Problem | Cause and solution |
|---|---|
| **Cost (so far)**, balance and forecast stay empty | The consumption sensor or the contract start is missing. See [Troubleshooting](EN-Troubleshooting). |
| Consumption is unknown | The statistics of the sensor do not reach back to the contract start. Enter the **Meter reading at contract start (optional)**. |
| Consumption is off by a factor of 1,000 | Tariffy only converts Wh and MWh to kWh. If the sensor reports in another unit, the value is taken unchanged. |
| The cost does not match the bill | Check unit price, base price, contract start and instalment. Tariffy counts months by the day (a month is 30.44 days), the bill of the supplier may draw the lines differently. |
| Night rate or tiered prices are missing in the form | They only appear if one of the countries named above is set in Home Assistant. |
| Sensor **Unit price (night)** or **Unit price (effective)** is missing | **Unit price (night)** only exists if unit price, night rate and both annual usages are entered. **Unit price (effective)** only exists with tiered pricing switched on and has a value with a block price and an annual usage. |
| Dynamic tariff: the price looks far too high | The price sensor delivers for example ct/kWh instead of €/kWh. Tariffy does not convert. |

## See also

- [Creating contracts](EN-Creating-Contracts)
- [Measuring consumption](EN-Measuring-Consumption)
- [PV self-sufficiency](EN-PV-Self-Sufficiency)
- [Payments and costs](EN-Payments-and-Costs)
- [Sensor reference](EN-Sensor-Reference)
- [Next contract or renew](EN-Next-Contract-or-Renew)
- [Troubleshooting](EN-Troubleshooting)
