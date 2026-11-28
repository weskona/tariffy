[🇩🇪 Deutsch](Vertrag-Wasser) · 🇬🇧 English

# Contract water

Here you find all fields of a water contract, the three ways to bill wastewater and the outdoor meters for garden, pool and irrigation. Like electricity and gas, water is a metered contract: with a meter sensor Tariffy works out real cost, balance and forecast.

**Contents:**

- [How Tariffy calculates water](#how-tariffy-calculates-water)
- [The form fields](#the-form-fields)
- [Fresh water and wastewater](#fresh-water-and-wastewater)
- [Outdoor meters](#outdoor-meters)
- [Worked example](#worked-example)
- [Typical mistakes](#typical-mistakes)

## How Tariffy calculates water

```
Consumption (so far)      = current meter value − meter value at contract start
Water price (combined)    = fresh water price + wastewater price (depending on the wastewater type)
Cost (so far)             = consumption so far × water price (combined) + base price × months elapsed
```

A month counts as 30.44 days. Balance and forecast are calculated like for electricity, the formulas are at [Contract electricity](EN-Contract-Electricity#how-tariffy-calculates). The consumption sensors show the unit of the meter sensor (for example m³); if it has none, the chosen **Water unit** applies. There is no conversion to kWh.

## The form fields

The second form is called **Water contract details**.

| Field | Required | Description |
|---|---|---|
| Water unit | yes | Unit used on your water bill: `m³`, `L`, `gal`, `ft³` or `CCF` (default `m³`). |
| Fresh water price (per unit) | yes | Price per unit of fresh water. |
| Base price (per month) | yes | Fixed monthly charge regardless of consumption. |
| Monthly instalment | yes | Monthly advance payment to the provider. |
| Wastewater billing type | yes | How wastewater is billed, see [Fresh water and wastewater](#fresh-water-and-wastewater). |
| Wastewater charge | no | Price per unit, percentage or flat monthly rate, depending on the chosen type. |
| Annual usage | no | Estimated annual consumption. Cost so far and forecast use the measured consumption. |
| Consumption sensor (optional) | no | Sensor of your water meter; enables real consumption tracking. |
| Meter reading at contract start (optional) | no | Your exact meter reading on the contract start date, if you know it. Takes priority over automatic detection. |
| Warn if instalment is too low | no | Off by default. Works as described at [Contract electricity](EN-Contract-Electricity#the-form-fields). |
| Warning threshold (€ balance due) | no | Default 50. |
| Meter number | no | For documentation. |

Depending on the country set in Home Assistant, **Enable tiered/block pricing** and the blocks are added; they work as at [Contract electricity](EN-Contract-Electricity#tiered-prices). You do not enter the outdoor meters in the form but in the panel (see below).

## Fresh water and wastewater

With **Wastewater billing type** you choose one of three ways. Which one is preselected depends on the country in Home Assistant (percentage in US, CA, AU, NZ, GB, IE; flat monthly rate in FR, BE, LU; otherwise fixed price).

| Type | Meaning of **Wastewater charge** | Effect on the water price (combined) |
|---|---|---|
| Fixed price per unit (e.g. DE, AT, CH) | Price per unit | fresh water price + wastewater charge |
| Percentage of fresh water price (e.g. US, UK, AU) | Percent, for example 80 for 80 % | fresh water price + fresh water price × percent ÷ 100 |
| Flat monthly rate (e.g. FR, BE) | Currency per month | fresh water price unchanged |

This creates the sensors **Unit price (wastewater)** and **Water price (combined)** in "currency per water unit". With the percentage, **Unit price (wastewater)** shows the calculated price; its attribute `typ` names the wastewater type.

> **Good to know:** The **flat monthly rate** is only shown as the attribute `pauschal_monat` of the sensor **Unit price (wastewater)**. Tariffy does **not** include it in the cost. If it should appear in the balance, add it to the **Base price (per month)**.

## Outdoor meters

Water for the garden, the pool or irrigation does not run into the sewer and is therefore not billed as wastewater. For this there are outdoor meters: sub-meters whose consumption is **already included in the main meter**. You enter them in the panel, in the **Contracts** tab in the details of the water contract, in the block **Outdoor meters**. This only works as an administrator and for at most ten meters.

![The details of a water contract in the Contracts tab: blocks Contract, Prices, One-off items and Consumption with outdoor water and wastewater cost, below it the block Outdoor meters with ten meters](https://raw.githubusercontent.com/wiki/weskona/tariffy/images/outdoor-meters-layout.png)

*Figure: The block "Outdoor meters" below the details of the water contract, here with ten meters (mock data, date 12 July 2026, German panel). The block "Verbrauch" (Consumption) shows "Gartenwasser" (outdoor water), "Abwasserpflichtiger Verbrauch" (wastewater-liable consumption), "Gartenwasser-Kosten" and "Abwasserkosten" (wastewater cost).*

### Adding an outdoor meter

1. In the panel open the **Contracts** tab and expand the water contract.
2. In the block **Outdoor meters** click **Add outdoor meter**. To change one, use the pencil at the meter.
3. Fill in the dialog and click **Save**.

![The Add outdoor meter dialog with the fields Name, Consumption sensor, Start value and Own price per unit](https://raw.githubusercontent.com/wiki/weskona/tariffy/images/aussen-dialog.png)

*Figure: The dialog "Add outdoor meter" with the example "Pool" (German panel).*

| Field | Required | Description |
|---|---|---|
| Name | yes | Name of the meter, for example "Pool". |
| Consumption sensor | yes | Sensor of the outdoor meter. It must not be the main meter of the contract. |
| Start value (optional) | no | Meter reading at contract start, in the unit of the meter. Without a start value Tariffy reads the value from the long-term statistics. |
| Own price per unit, without wastewater (optional) | no | Price used for the water of this meter, **fresh water only, without wastewater** (garden water does not go into the sewer). The field is **prefilled with the fresh-water price of the contract**; change it if this water costs something else. If you leave it as it is, the meter follows the price of the contract (for example after a tariff switch). |

You can delete a meter in the edit dialog with **Delete meter** (with the question "Delete this outdoor meter?" and **Yes, delete**). When you add the first outdoor meter, Home Assistant reloads the contract because it gets additional sensors.

### How Tariffy calculates the outdoor meters

- **Wastewater-liable consumption = main meter − sum of the outdoor meters** (never below 0). If the outdoor meters together count more than the main meter, their share is capped at the main meter.
- The outdoor water costs the **fresh water price** or the own price of the meter, the remaining water costs the full **Water price (combined)** of fresh water and wastewater.
- **Cost (so far)**, the forecast and the recommended instalment use the **weighted price** of the main meter that follows from this, like the dual tariff for electricity.
- In the panel the block **Prices** then shows two rows: **Water price incl. wastewater** is the **full price** (fresh water plus wastewater, for example 5.51 €/m³), **Mixed price (with garden water)** is the **weighted price** of the main meter that the costs are worked out with. The sensor **Water price (combined)** holds the weighted price.
- A meter in litres is converted to the unit of the main meter (m³). A start value applies in the unit of the meter.
- With a **flat monthly rate** for wastewater outdoor meters change nothing in the cost; **Wastewater cost** is then 0.
- A contract with outdoor meters gets four additional sensors: **Outdoor water (consumption)**, **Outdoor water (cost)**, **Wastewater-liable consumption** and **Wastewater cost**. The total cost is in **Cost (so far)** as always. Without outdoor meters nothing changes.

> **Good to know:** At an automatic switch to the next contract the outdoor meters stay connected; their start values are dropped because they belonged to the old term. Outdoor meters are part of the [backup](EN-Panel-Backup) too.

## Worked example

A water contract with fresh water price 2.00 €/m³, wastewater as a fixed price of 3.00 €/m³ (so water price (combined) 5.00 €/m³), base price 5.00 €/month, instalment 30 €/month. Term 01.01. to 31.12.2026, today is 12 July 2026 (6.3075 months). The main meter shows 150 m³ consumption since the start. The numbers come from the tests (`tests/test_coordinator.py` and `tests/test_aussen.py`); they are example values.

**Without an outdoor meter:**

```
Cost (so far)                   = 150 × 5.00 + 5.00 × 6.3075            =   781.54 €
Instalments due so far          = 30 × 6.3075                           =   189.22 €
→ Refund/balance due (so far)   = 189.22 − 781.54                       =  −592.32 €  (balance due)
```

### With one outdoor meter

The garden meter shows 40 m³ since the start (no own price):

```
Outdoor water (consumption)     = 40 m³
Wastewater-liable consumption   = 150 − 40                              = 110 m³
Outdoor water (cost)            = 40 × 2.00                             =    80.00 €
Wastewater cost                 = 110 × 3.00                            =   330.00 €
Cost (so far)                   = 110 × 5.00 + 40 × 2.00 + 5.00 × 6.3075 =  661.54 €
Weighted price of the main meter = (110 × 5.00 + 80) ÷ 150             =     4.20 €/m³
→ Refund/balance due (so far)   = 189.22 − 661.54                       =  −472.32 €  (balance due)
```

Compared with the calculation without an outdoor meter, the outdoor meter saves 120 € of wastewater here (40 m³ × 3.00 €). The forecast at contract end follows the weighted price and therefore turns out better than without an outdoor meter.

If the percentage is chosen as the wastewater type (fresh water 2.00 €/m³, wastewater charge 80), the result is a wastewater price of 1.60 €/m³ and a water price (combined) of 3.60 €/m³.

## Typical mistakes

| Problem | Cause and solution |
|---|---|
| The wastewater flat rate does not show in the cost | The **flat monthly rate** does not enter the calculation. Add it to the **Base price (per month)**. |
| Wrong wastewater price | The **Wastewater billing type** does not match your bill. With "percentage" enter the percent value in **Wastewater charge** (80 for 80 %), not the price. |
| The four outdoor meter sensors are missing | They only appear with the first outdoor meter; the contract then reloads. An outdoor meter can only be added to a water contract. |
| The outdoor meter is refused | Enter a name, choose a sensor and do not use the main meter of the contract ("This is the main meter of the contract."). The price must not be negative. |
| There is no outdoor meter cost | The split needs the consumption of the main meter: without a consumption sensor on the water contract the values stay empty. |
| The outdoor meter counts in litres, the main meter in m³ | That works: Tariffy converts litres to m³ (only these two units). |
| Consumption unknown | The statistics of the sensor do not reach back to the contract start. Enter the **Meter reading at contract start (optional)**. |

## See also

- [Creating contracts](EN-Creating-Contracts)
- [Contract electricity](EN-Contract-Electricity)
- [Measuring consumption](EN-Measuring-Consumption)
- [Panel contracts](EN-Panel-Contracts)
- [Payments and costs](EN-Payments-and-Costs)
- [Sensor reference](EN-Sensor-Reference)
- [Troubleshooting](EN-Troubleshooting)
