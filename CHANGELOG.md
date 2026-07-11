# Changelog

Format angelehnt an [Keep a Changelog](https://keepachangelog.com/).

## [1.18.0] - 2026-07-12

### Fixed

- **Wrong unit on "Consumption (so far)"/"Consumption (contract term projected)" for gas/water**: these sensors displayed the unit from the `gas unit`/`water unit` setting (which actually only describes the unit of the manually entered annual consumption estimate), even though the displayed value is the raw meter delta of the real consumption sensor — with an m³ meter and `gas unit: kWh`, it incorrectly showed "kWh" over an m³ value (off by a factor of ~18x in one observed case). Now shows the actual unit of the configured consumption sensor, falling back to the config field if the sensor is unavailable.

### Changed

- README substantially reworked: every sensor explanation now includes a worked example from real live contracts (electricity, gas) instead of only abstract formulas; water/TOU/tiered sections use clearly labeled illustrative numbers (no live contracts of those types available).

## [1.17.0] - 2026-07-12

### Changed

- **Renamed two cost sensors** to clarify how the four balance/cost sensors relate (display name only, `entity_id`/`unique_id` unchanged):
  - "Cost (contract term)" → "Installment total (contract term)" (`jahreskosten`) — makes clear this is just the payment plan, not a cost forecast based on real consumption.
  - "Cost (refund/balance due)" → "Refund/balance due (contract end)" (`prognose_real`) — parallel naming with "Refund/balance due (so far)".
- README substantially reworked: a 2×2 grid (so-far/contract-end × raw amount/balance) plus a fully worked numeric example for all four sensors.

## [1.16.0] - 2026-07-12

### Fixed

- **Manual "Switch now" button didn't freeze the ending period's consumption**: the button called `_switch_now()` without the actually measured consumption, unlike the automatic date-based switch — `verbrauch_letzte_laufzeit` stayed empty or stale, which would have skewed `empfohlener_abschlag` at the next switch. Both paths now share the same calculation (`_verbrauch_letzte_laufzeit_jetzt()`).

## [1.15.0] - 2026-07-12

### Changed

- **Tariff switch now triggers exactly on date change**: previously the switch date was only checked on the next regular 6-hour poll, so the switch could take effect up to almost 6 hours late. Added a daily trigger at 00:00:01 (`async_track_time_change`) that checks and performs the switch exactly when the date changes. The existing 6h poll and HA-start refresh remain as fallback.

## [1.14.0] - 2026-07-11

### Added

- **New sensor "Refund/balance due (so far)"** (`guthaben_bisher`): `abschlag × vergangene_monate − kosten_bisher`. Answers "am I currently ahead or behind on my installment payments?" — unlike `prognose_real`, no projection onto the full contract term, just today's exact standing. Same dynamic thumb-up/thumb-down icon as `prognose_real`. Energy contracts only, requires a configured `verbrauch_sensor`.

## [1.13.0] - 2026-07-11

### Changed

- **Sensor renamed**: "Cost (forecast real)" → "Cost (refund/balance due)" / German: "Kosten (Prognose Real)" → "Kosten (Guthaben/Nachzahlung)" — clearer about what the sensor actually answers. `entity_id`/`unique_id` unchanged.
- **Dynamic icon for `prognose_real`**: now shows `mdi:thumb-up` when in credit (value ≥ 0), `mdi:thumb-down` when a balance is due (value < 0), falling back to `mdi:calculator-variant` when the value is unknown (e.g. no `verbrauch_sensor` configured).
- README updated with an overview table comparing the three cost sensors (`jahreskosten`, `kosten_bisher`, `prognose_real`).

## [1.12.0] - 2026-07-09

### Changed

- **Consumption projection now uses the actual contract term, not a fixed calendar year**: `verbrauch_hochgerechnet` used to always project onto 365 days regardless of the real contract duration. Now projects onto `(contract end − contract start)` days — important for contracts that switch mid-year. Falls back to 365 for contracts without an end date.
- **Recommended monthly payment** now uses the actual duration of the expiring contract period (frozen at tariff switch) instead of assuming a flat 12 months.
- **Sensor renamed**: "Annual consumption (projected)" → "Consumption (contract term projected)" / German: "Jahresverbrauch (Hochgerechnet)" → "Verbrauch (Vertragslaufzeit hochgerechnet)".
- **Sensor renamed**: "Billing forecast (real)" → "Cost (forecast real)" / German: "Prognose (Real)" → "Kosten (Prognose Real)".
- **Consumption tracking switched to the recorder's cumulative `sum` statistic** instead of the raw sensor state, for both the contract-start offset and the current value. Required for sensors with `state_class: total_increasing` that legitimately reset periodically (some smart-meter integrations reset their raw counter on every reading cycle) — the previous state-based subtraction could produce negative "consumption so far" values for such sensors.

### Fixed

- **Crash (500 Internal Server Error) when creating/editing a gas contract**: an initial attempt to accept decimal-comma input (`11,2`) for calorific value / state number used a schema validator that `voluptuous_serialize` could not convert to JSON for the frontend. Calorific value and state number are now plain text fields in the schema; comma/dot normalization happens after form submission, with a clean validation error instead of a crash on invalid input.
- **Calorific value / state number now accept decimal commas** (`11,2` as well as `11.2`) — the native HTML5 number field didn't reliably handle commas depending on browser/locale.

### Recommended

- For meters that reset periodically, configure a true never-resetting cumulative sensor as the consumption sensor where available (e.g. a separate utility meter with `cycle: none`), rather than relying solely on the `sum` statistic.

## Before 1.12.0

No structured changelog prior to this version.
