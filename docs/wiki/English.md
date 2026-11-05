# English documentation

## Features

- **Categories:** Electricity, Gas, Water, Internet, Mobile, Insurance, Other
- **Real consumption tracking** – connect any HA sensor as your meter; Tariffy reads the meter value at contract start from Long-Term Statistics and calculates consumption since contract start and projected annual usage
- **Real billing forecast** – forecast based on actual measured consumption (credit or surcharge)
- **Last contract period consumption** – frozen at tariff switch; used to calculate the recommended monthly payment for the new period
- **Recommended monthly payment** – based on last period's real consumption × current rates
- **Automatic tariff switch** – store the next tariff, HA promotes it automatically on the switch date
- **Cancellation reminder** – 1–4 months before contract end, persistent notification + optional notify service
- **Gas conversion** – annual consumption in m³ is automatically converted to kWh via calorific value & state number
- **Water** – fresh water + wastewater (fixed price, % or flat rate)
- **Tiered pricing** – country-specific (US, AU, ES, …)
- **Time-of-Use / Night rate** – Economy 7, TOU (GB, US, AU, …)
- **Dual-tariff meter (HT/NT)** – separate category for a real two-register electricity meter (high tariff / low tariff): a second unit price, second consumption sensor and second meter number, tracked independently from the high-tariff register. All the usual sensors (Cost/Refund/Forecast so far) stay combined across both registers via an automatically weighted average price; dedicated Consumption/Cost sensors per register are also available
- **Dynamic tariff (spot price)** – reference an external HA sensor (Tibber, aWATTar, Nordpool, …) instead of a fixed unit price; the effective price is calculated as the sensor's statistical average over the contract-to-date plus a fixed markup, with automatic fallback to the manual price while no statistics history exists yet
- **Feed-in tariff** – per kWh fed into the grid (solar)
- **Auto-refresh after HA startup** – sensors update automatically once Long-Term Statistics are ready after a restart
- **Check interval** – every 6 hours


## Sensors per contract

| Sensor | Unit | Category | Description |
|--------|------|----------|-------------|
| Unit price | €/kWh | Energy | Consumption-based price. For a dynamic tariff (spot-price sensor configured), this is the statistical average over the contract-to-date + markup; attribute `arbeitspreis_aktuell` shows the live current price, `dynamischer_tarif` whether a price sensor is set |
| Unit price (night) | €/kWh | Energy | Night rate (TOU/Economy 7) |
| Unit price (low tariff / NT) | €/kWh | Electricity (dual meter) | Low-tariff register price, as entered in the config flow |
| Unit price (effective) | €/kWh | Energy | Effective average price (tiered) |
| Unit price (wastewater) | €/m³ | Water | Wastewater charge |
| Water price (combined) | €/m³ | Water | Fresh water + wastewater |
| Base price | €/month | Energy | Monthly base fee |
| Monthly payment | €/month | All | Monthly instalment |
| Monthly payment (recommended) | €/month | Energy | Based on last period consumption × current rates |
| Instalment adjustment (recommended) | €/month | Energy+Water | What the instalment should be from now until contract end to break even exactly — unlike "Monthly payment (recommended)" (only after a tariff switch), this updates continuously during the current contract |
| Installment total (contract term) | € | All | Instalment × contract duration in months — a payment plan total, **not** a cost forecast |
| Cost (so far) | € | Energy+Water | Actual costs incurred since contract start (real consumption) |
| Refund/balance due (so far) | € | Energy | Instalments paid so far − Cost (so far), as of today (no projection). Icon shows 👍/👎 depending on sign |
| Feed-in tariff | €/kWh | Electricity | Configured feed-in rate |
| Annual consumption (kWh) | kWh | Gas | Manually entered annual estimate, converted via calorific value & state number |
| Consumption (so far) | unit of the consumption sensor (usually m³) | Energy+Water | Measured consumption since contract start — raw meter delta, **not** automatically converted to kWh |
| Consumption (contract term projected) | unit of the consumption sensor | Energy+Water | Current consumption extrapolated to the full contract term (not a fixed calendar year) |
| Consumption (last period) | unit of the consumption sensor | Energy | Frozen at tariff switch — basis for recommended payment |
| Consumption, high/low tariff (so far) | kWh | Electricity (dual meter) | Measured consumption of each register since contract start |
| Cost, high/low tariff (so far) | € | Electricity (dual meter) | Usage-based cost of each register (no base fee share) since contract start |
| Refund/balance due (contract end) | € | Energy+Water | Forecast based on real consumption, projected to contract end. Icon shows 👍/👎 depending on sign |
| Remaining term | Days | All | Days until contract end |
| Contract start | Date | All | Start date of contract |
| Contract end | Date | All | End of current contract |
| Next switch | Date | All | Date of planned tariff switch |
| Cancellation reminder | Date | All | Date from which the reminder is active |
| Provider | – | All | Provider name (diagnostic) |
| Tariff | – | All | Tariff name (diagnostic) |
| Customer number | – | All | Customer number (diagnostic) |
| Meter number | – | Energy | Meter number (diagnostic) |
| Meter number (low tariff / NT) | – | Electricity (dual meter) | Meter number of the low-tariff register (diagnostic) |

> **Night rate**, **tiered pricing** and **dual-tariff (HT/NT)** sensors only appear when the corresponding category/option is used.


## The four cost sensors at a glance

Tariffy has four sensors with a currency unit. Behind them are two independent questions:

- **When?** – the standing **so far** (actual) or the forecast for **contract end** (projected)?
- **What?** – a **raw amount** (instalment total or actual cost) or the **balance** between them (instalments minus cost = refund/balance due)?

|  | **raw amount** | **balance (instalments − cost)** |
|---|---|---|
| **so far** | Cost (so far) `kosten_bisher` | Refund/balance due (so far) `guthaben_bisher` |
| **contract end** (projected) | Installment total (contract term) `jahreskosten` | Refund/balance due (contract end) `prognose_real` |

Important: **Installment total (contract term)** is *not* a cost forecast — it's simply `instalment × months`, just the payment plan, independent of actual consumption. Both balance sensors (`guthaben_bisher`, `prognose_real`) are positive when in credit, negative when a balance is due (see the `tendenz` attribute and the 👍/👎 icon).

**Real example** (electricity contract: instalment 40 €/month, unit price 0.2977 €/kWh, base price 11.51 €/month, term 01.01.–31.12.2026 ≈ 11.96 months; today, after 6.31 months: 1,481.17 kWh consumed):

```
Cost (so far)                       = 1,481.17 kWh × 0.2977 €  + 11.51 € × 6.31 months  =    513.54 €
Instalments paid so far (internal)  = 40 € × 6.31 months                               =    252.40 €
→ Refund/balance due (so far)       = 252.40 € − 513.54 €                              =   −261.24 €  (balance due)

Projected onto the full term: 1,481.17 kWh / 192 days × 364 days ≈ 2,808.1 kWh

Installment total (contract term)   = 40 € × 11.96 months                              =    478.32 €
Projected real cost (internal)      = 2,808.1 kWh × 0.2977 € + 11.51 € × 11.96 months   =    973.61 €
→ Refund/balance due (contract end)  = 478.32 € − 973.61 €                              =   −495.29 €  (balance due, projected)
```

All four values match this contract's live sensors exactly. Consumption is well above what the instalment covers — the balance due grows from −261 € (today) to a projected −495 € (contract end), roughly in step with elapsed time (6.31 → 11.96 months, nearly 2×). That's the difference between the two balance sensors: one is the **current** standing, the other the **forecast** for contract end, assuming consumption continues at the same rate.

All four require `unit price`; `Cost (so far)`, `Refund/balance due (so far)` and `Refund/balance due (contract end)` additionally require a configured consumption sensor.


## Real consumption tracking

When a **consumption sensor** is configured, Tariffy reads the historical meter value at contract start from **Long-Term Statistics** and calculates:

Tariffy also reads the sensor's raw `state` alongside the `sum` statistic: if the current reading
hasn't dropped below the value at contract start (the normal case — no real meter reset), it uses
the simpler state difference instead of the `sum` statistic. This makes the calculation robust
against rare anomalies in the `sum` statistic itself (observed once after a Home Assistant
restart: the statistic suddenly jumped to an implausible value while the meter reading stayed
perfectly continuous). If the sensor's statistics history still doesn't reach back to the
contract start date (e.g. because it was renamed or recreated at some point), you can optionally
enter a **"Meter reading at contract start"** — this manual value takes priority over both
automatic methods.

```
Consumption so far                    = current meter value − meter value at contract start   (in the sensor's own unit, e.g. m³)
Consumption (contract term projected) = consumption so far ÷ days elapsed × contract term (days)
Cost (so far)                         = consumption so far (in kWh) × unit price + base price × months elapsed
Refund/balance due (so far)           = instalments paid so far − Cost (so far)                (today's exact standing, no projection)
Refund/balance due (contract end)     = instalment total − projected cost over contract period (projected to contract end)
```

**Positive** = credit · **Negative** = surcharge

⚠️ **Unit note (gas/water):** "Consumption (so far)" and "Consumption (contract term projected)" show the raw meter delta in whatever unit your actual consumption sensor reports (usually m³) — they are **not** automatically converted to kWh, even though the `gas unit`/`water unit` setting might say "kWh". That setting only describes the unit of your manually entered annual consumption *estimate*, not your real meter. For all cost calculations (Cost so far, both refund/balance due sensors), the consumption **is** converted to kWh internally via calorific value × state number — just not for the raw "Consumption" sensors themselves.

The contract term used for the projection is `contract end − contract start` in days (falls back to 365 if no end date is set) — a contract that runs for e.g. 6 months is projected onto those 6 months, not a full calendar year.

Both the current meter value and the historical value at contract start are read from the recorder's **cumulative `sum` statistic**, not the sensor's raw state. This makes the calculation robust against sensors with `state_class: total_increasing` that legitimately reset periodically (some smart-meter integrations reset their raw counter on every reading cycle) — the recorder's `sum` already accounts for such resets. A meter that never resets at all is still preferable where available.

> The sensor must have Long-Term Statistics enabled and must have existed since at least the contract start date.


## Last contract period & recommended payment

When a tariff switch occurs — automatic (date reached) or manual ("Switch now" button, identical calculation either way) — Tariffy freezes the total consumption of the expiring contract period:

```
Consumption (last period)          = meter at switch date − meter at contract start
Monthly payment (recommended)      = (last period consumption × new unit price + new base price × months) / months
```

`months` is the **actual duration of the expiring contract period** in months (frozen at the moment of switching), not a fixed 12 — relevant if the previous contract ran shorter or longer than a year. Falls back to 12 for periods frozen before this was tracked.

This gives a data-driven recommendation for the monthly instalment in the new contract.


## Buttons per contract

| Button | Description |
|--------|-------------|
| Switch now | Promotes the stored next tariff immediately (without waiting for the switch date) — freezes the ending period's consumption exactly like the automatic switch |
| Confirm cancellation | Acknowledges the reminder and removes the persistent notification |
| Confirm low-instalment warning | Acknowledges the low-instalment warning and removes the persistent notification (re-arms automatically if the forecast worsens again later) |


## Tariff switch

Under **Settings → Integrations → Tariffy → [Contract] → Options** you can store a successor tariff:

- Switch date, new provider, customer number, tariff name
- New prices and consumption values

On the switch date HA promotes the new tariff automatically — checked exactly at midnight (00:00:01) plus the regular 6-hour poll and HA-start refresh as fallback. Fields left blank keep their current value.


## Cancellation reminder

When contract end is set and the reminder period is reached:

1. **Persistent notification** in the HA notification centre
2. One-time **push notification** via the configured notify service
3. **"Confirm cancellation"** button to acknowledge


## Low-instalment warning (optional)

Opt-in per contract (electricity/gas/water with a configured consumption sensor): warns via persistent notification (+ optional push notification) when the contract-end forecast (`prognose_real`, see "Refund/balance due (contract end)" above) projects a balance due beyond a configurable threshold.

- **Enable**: "Warn if instalment is too low" checkbox in the contract's config/reconfigure flow. Off by default.
- **Threshold** (€ balance due, default 50 €): fires when `prognose_real < -threshold`.
- **Acknowledge**: "Confirm low-instalment warning" button removes the notification for the current episode. If the forecast recovers above the threshold and later worsens again, the warning fires again automatically — acknowledging isn't a permanent mute, just a dismissal of the current episode.
- The raw state (independent of acknowledgement) is exposed as the `abschlag_warnung_aktiv` attribute on the "Refund/balance due (contract end)" sensor.
- The notification message includes a concrete recommendation ("adjust your instalment to about X €/month") from the "Instalment adjustment (recommended)" sensor, if computable.

> **No retroactive recalculation on instalment changes.** If you raise or lower your instalment mid-contract, Tariffy remembers the date and the previous value and applies the old instalment correctly only up to that date, the new one from then on — "Refund/balance due (so far)" and "Instalment adjustment (recommended)" won't suddenly jump as if the new instalment had applied since day one. Multiple corrections on the same day count as a single change.


## Installation via HACS

1. HACS → Integrations → ⋮ → **Custom repositories**
2. URL: `https://github.com/weskona/tariffy` – Category: **Integration**
3. Install Tariffy → restart HA
4. Settings → Integrations → **Tariffy** → Add

## Manual installation

```bash
cp -r custom_components/tariffy /config/custom_components/
```
Restart HA.

## Requirements

- Home Assistant 2026.6 or newer

