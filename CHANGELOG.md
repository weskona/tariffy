# Changelog

Format angelehnt an [Keep a Changelog](https://keepachangelog.com/).

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
