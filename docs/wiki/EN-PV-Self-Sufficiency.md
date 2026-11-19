[🇩🇪 Deutsch](PV-Autarkie) · 🇬🇧 English

# PV self-sufficiency

With a photovoltaic system (also with a battery) the electricity you draw from the grid varies strongly with the season. PV self-sufficiency makes the forecast at the contract end take that into account. This page is for everyone with an electricity contract and a PV system.

**Contents:**
- [What PV self-sufficiency is for](#what-pv-self-sufficiency-is-for)
- [Switching it on](#switching-it-on)
- [The three sources](#the-three-sources)
- [How Tariffy calculates](#how-tariffy-calculates)
- [Total consumption and Covered by PV](#total-consumption-and-covered-by-pv)
- [How self-sufficiency enters the forecast](#how-self-sufficiency-enters-the-forecast)
- [What you see on the sensor and in the panel](#what-you-see-on-the-sensor-and-in-the-panel)
- [Example](#example)
- [When nothing happens](#when-nothing-happens)
- [See also](#see-also)

## What PV self-sufficiency is for

The consumption sensor of your contract measures the **grid draw**. Whoever looks at the forecast in winter has measured a lot of grid draw and uses it for the whole year: the forecast is too high. Whoever looks in summer has measured little: it is too low.

The **self-sufficiency** of a month is the share of the house consumption that the system covers:

```
Self-sufficiency = 1 − grid draw ÷ total consumption      (limited to 0 to 100 %)
```

With the option Tariffy compares, for every remaining month of the term, the self-sufficiency of the **same month last year** with the self-sufficiency of the period measured so far and adjusts the expected grid draw accordingly.

- The option applies **to the remaining term only**. The consumption measured so far and the cost so far stay as they are.
- It exists only for **electricity** and **electricity (dual tariff)**. Gas and water do not offer it.
- It is **off by default**. Without the option nothing changes.

## Switching it on

1. Open the electricity contract for editing (in the panel **Edit contract**, see [Contract-Electricity](EN-Contract-Electricity)).
2. Switch on **Take PV self-sufficiency into account**.
3. Give the source of the self-sufficiency, at least one of the three under [The three sources](#the-three-sources).
4. The **consumption sensor** of the contract must measure the **grid draw**. Without a consumption sensor there is no forecast that could be changed. How it works is explained in [Measuring-Consumption](EN-Measuring-Consumption).
5. Save. After the reload Tariffy calculates the forecast with the self-sufficiency.

## The three sources

The sources apply in this order: if source 1 is given it determines the self-sufficiency, otherwise source 2, otherwise source 3. If the value of source 1 or 2 is missing for a month, source 3 applies for that month (if entered), otherwise there is no adjustment for that month.

| No. | Field in the form | What you enter | What Tariffy makes of it |
|---|---|---|---|
| 1 | **Total consumption of the house (sensor)** | Sensor in kWh with a long-term statistic (`total_increasing`), for example the house consumption of the Energy dashboard | Self-sufficiency per month from the energy sums of last year: `1 − grid draw ÷ total consumption`. The most exact source, also works with a battery |
| 2 | **Self-sufficiency sensor (%)** | Sensor with the degree of self-sufficiency in % and a statistic (`state_class` measurement), for example the autonomy of the Fronius integration | Monthly mean of this sensor last year. Not used if source 1 is given |
| 3 | **Self-sufficiency, own values (%)** | Twelve values for January to December, separated by spaces or semicolons, for example `10 10 25 50 70 80 85 80 60 35 15 10`, or one value for all months | The value of the month. Applies to months without data and is enough on its own, for example in the first year of a PV system without history |

Rules for your own values:

- One value or twelve values between 0 and 100 are allowed, with a comma or a point as decimal separator. The form rejects anything else.
- **A single value for all months changes nothing on its own.** The forecast compares the self-sufficiency of each remaining month with that of the measured period, and a single value is the same in every month. That is why, without a sensor, the form asks for twelve **different** monthly values. One value for all months only makes sense as a fallback for months without data **next to a sensor**.

**Dual-tariff meter:** For source 1 there is a second field **Total consumption, low-tariff period (sensor)**. If it is filled, Tariffy calculates per tariff. Without the second field the self-sufficiency is calculated over both tariffs together and applied to both. That is an approximation and is shown in the attribute `autarkie_naeherung`. Sources 2 and 3 apply to both tariffs alike.

## How Tariffy calculates

For every calendar month of the remaining term, with the days from today on:

1. **Self-sufficiency of the month** `a_month`: for source 1 from the long-term statistics of the **same month last year** (grid draw and total consumption of that month), for source 2 the monthly mean of last year, for source 3 your value. Always limited to 0 to 100 %.
2. **Self-sufficiency so far** `a_sofar`: from the same source for the period since the contract start. For source 3 these are your values of the months already measured, weighted by days.
3. **Factor** of the month: `(1 − a_month) ÷ (1 − a_sofar)`.
4. **Grid draw of the month**: `grid draw per day so far × days of the month × factor`.

The consumption so far plus these monthly values is the projected grid draw for the whole term.

The factor has limits:

| Case | Factor |
|---|---|
| no value for the month or for the measured period | 1 (linear projection as without the option) |
| self-sufficiency so far almost 100 % (grid share below 5 %) | 1, because the calculation would not be reliable |
| month fully self-sufficient (self-sufficiency 100 %) | 0 (no grid draw) |
| month much darker than the measured period | at most 4 |

A dual-tariff meter is calculated per tariff. The mixed price of high and low tariff then also shifts with the season.

> **Good to know:** For source 1 Tariffy needs statistics of **last year** for the total consumption **and** for the consumption sensor of the contract. If they are missing for a month, that month stays with the linear projection. If there is no history at all, nothing changes and there is no error.

## Total consumption and Covered by PV

With source 1 Tariffy also knows the **total consumption** of your house. The panel then shows, in the block **Consumption** of the contract details (tab **Contracts**), a small grid with the columns **So far** and **Projected**:

| Row in the panel | Meaning |
|---|---|
| **Total consumption** | total consumption of the house in kWh |
| **Covered by PV** | total consumption minus grid draw, never negative |
| **Grid draw (billed)** | the consumption your provider bills, that is the consumption sensor of the contract |

- The total consumption is extended **linearly**: the season only sits in the grid draw.
- For a dual-tariff meter both tariffs are added. If there is only one total-consumption sensor, it counts once.
- With a self-sufficiency sensor in % (source 2) or own values (source 3) there is no total consumption, so the grid is not shown.
- The grid draw and all costs stay as they are. The grid only shows additional figures.

## How self-sufficiency enters the forecast

The adjusted grid draw replaces the linear projection in the forecast:

- **Consumption (contract term projected)** shows the adjusted value.
- **Refund/balance due (contract end)** calculates with the estimated cost from this consumption. For a dual-tariff meter the weighted mixed price of the season applies.
- **Instalment adjustment (recommended)** follows the same estimated cost sum.
- The **low-instalment warning** follows the forecast and therefore also the self-sufficiency.
- **Unchanged** stay **Consumption (so far)**, **Cost (so far)** and **Refund/balance due (so far)**.

The calculation path of the forecast is shown in [Payments-and-Costs](EN-Payments-and-Costs).

## What you see on the sensor and in the panel

The sensor **Refund/balance due (contract end)** gets additional attributes, **only if the self-sufficiency really determines the forecast**. If the option is off or the history is missing, the attributes look as always.

| Attribute | Content |
|---|---|
| `autarkie_variante` | the source: `gesamtverbrauch`, `entitaet` or `manuell` |
| `autarkie_monatswerte` | one row per remaining month: `monat`, `tage`, `autarkie` (in %), `faktor`, `quelle` (`statistik` or `manuell`); for a dual-tariff meter also `autarkie_nt` and `faktor_nt` |
| `autarkie_bisher` | self-sufficiency in the measured period in % |
| `autarkie_bisher_nt` | the same for the low tariff (dual-tariff meter only) |
| `autarkie_naeherung` | `true` if, with two tariffs, only one total-consumption sensor determines the self-sufficiency for both |
| `prognose_ohne_autarkie` | the forecast at the contract end with the linear projection |

Only with a total-consumption sensor (source 1) these are added: `verbrauch_gesamt_bisher`, `verbrauch_gesamt_hochgerechnet`, `verbrauch_pv_gedeckt_bisher` and `verbrauch_pv_gedeckt_hochgerechnet`.

In the panel the contract details show in the block **Consumption** in addition **Forecast at contract end without PV self-sufficiency**, **PV self-sufficiency so far** (with the low-tariff value for a dual-tariff meter) and **Source of the self-sufficiency** (**Total consumption of the house**, **Self-sufficiency sensor** or **Own values**). With the approximation there is also the row **Self-sufficiency over both tariffs (approximation)**.

## Example

The example comes from the Tariffy tests (sample data, not your contract).

- Contract 1 Jan to 31 Dec 2026 (364 days), unit price 0.30 €/kWh, base price 10 €/month, instalment 100 €/month.
- Reference date 1 July 2026, after **181 days**: grid draw so far **1,800 kWh**, total consumption of the house so far **3,600 kWh**. The self-sufficiency so far is `1 − 1,800 ÷ 3,600 = 50 %`.
- Last year the total consumption was 300 kWh every month. The grid draw last year from July to December was 50, 50, 100, 150, 200 and 250 kWh.

| Month | Days | Self-sufficiency last year | Factor `(1 − a) ÷ 0.5` |
|---|---|---|---|
| July | 31 | 83.3 % | 0.333 |
| August | 31 | 83.3 % | 0.333 |
| September | 30 | 66.7 % | 0.667 |
| October | 31 | 50.0 % | 1.000 |
| November | 30 | 33.3 % | 1.333 |
| December | 30 | 16.7 % | 1.667 |

```
Grid draw per day so far     = 1,800 kWh ÷ 181 days                        = 9.945 kWh
Grid draw of the rest        = 9.945 × (31×0.333 + 31×0.333 + 30×0.667 + 31×1 + 30×1.333 + 30×1.667)
                             = 9.945 × 161.67                               = 1,607.7 kWh
Projected with self-suff.    = 1,800 + 1,607.7                              = 3,407.7 kWh
Projected linearly           = 1,800 ÷ 181 × 364                            = 3,619.9 kWh
```

The factors below 1 (July to September) lower the expected grid draw, those above 1 (November and December) raise it. Overall the adjusted projection is below the linear one.

```
Instalments over the term    = 100 € × 11.958 months                       = 1,195.80 €
Cost with self-sufficiency   = 3,407.7 kWh × 0.30 € + 10 € × 11.958         = 1,141.90 €
Cost linear                  = 3,619.9 kWh × 0.30 € + 10 € × 11.958         = 1,205.55 €

Refund/balance due (contract end)  with self-sufficiency = 1,195.80 € − 1,141.90 € = +53.90 €
prognose_ohne_autarkie                                   = 1,195.80 € − 1,205.55 € =  −9.75 €
```

The linear calculation would have predicted a small balance due, with the self-sufficiency it is a credit. The total consumption of the house would be linearly `3,600 ÷ 181 × 364 = 7,239.8 kWh`; **Covered by PV** is 1,800 kWh so far and projected `7,239.8 − 3,407.7 = 3,832.0 kWh`.

## When nothing happens

The option stays without effect, without an error message, when:

- there is no consumption sensor in the contract or no consumption above zero has been measured yet,
- none of the three sources is given (option on, but everything empty),
- the statistics of last year for the total consumption or the grid draw are missing and there are no own values,
- the self-sufficiency so far cannot be calculated, for example because the total consumption is zero,
- the contract is not electricity or electricity (dual tariff).

A consumption sensor that measures the **total consumption** instead of the grid draw does not fit this option.

## See also

- [Measuring-Consumption](EN-Measuring-Consumption): how the consumption so far comes about
- [Payments-and-Costs](EN-Payments-and-Costs): forecast and recommended instalment
- [Contract-Electricity](EN-Contract-Electricity): the electricity form with the self-sufficiency fields
- [Sensor-Reference](EN-Sensor-Reference): attributes of the sensor Refund/balance due (contract end)
- [Dashboard-Examples](EN-Dashboard-Examples): the self-sufficiency values on the dashboard
