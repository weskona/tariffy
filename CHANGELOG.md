# Changelog

Format angelehnt an [Keep a Changelog](https://keepachangelog.com/).

## [1.24.1] - 2026-07-14

### Fixed

- **Units showed "€/kWh" instead of "EUR/kWh"**: the 1.23.0 code-to-symbol fix (`hass.config.currency` → "€") was a misinterpretation and exactly backwards — the raw ISO 4217 code (e.g. "EUR/kWh") was wanted throughout, not the symbol. The symbol conversion has been removed entirely; all cost sensors show the unit as the plain currency code again.

## [1.24.0] - 2026-07-14

### Added

- **Dynamic tariff for electricity (spot price)**: new optional fields "Dynamic tariff price sensor" and "Dynamic tariff markup" on electricity contracts. Instead of a fixed unit price, you can now reference an existing HA sensor providing a live spot-market price (e.g. from Tibber, aWATTar, Nordpool) — the unit price is then calculated as that sensor's statistical average over the contract-to-date (+ fixed markup) and automatically feeds into all existing calculations (cost so far, refund/balance due, instalment adjustment recommendation, real billing forecast). The manually entered unit price remains as a fallback while no sufficient statistics history exists yet for the sensor. The current live price (sensor + markup) is additionally exposed as the `arbeitspreis_aktuell` attribute on the "Unit price" sensor, which also gets its own icon while a dynamic tariff is active.

## [1.23.0] - 2026-07-14

### Added

- **New sensor "Instalment adjustment (recommended)"**: continuously calculates what the instalment should be from now until contract end to break even exactly — unlike "Monthly payment (recommended)" (only available after a tariff switch, based on the frozen last-period consumption). The low-instalment warning notification now also states this concrete recommendation instead of just "consider raising your instalment".

### Fixed

- **Units showed "EUR" instead of "€"**: `hass.config.currency` returns the ISO 4217 code ("EUR"), not a symbol. All cost sensors (unit price, base price, instalment, costs, refund/balance due, ...) showed e.g. "EUR/kWh" instead of "€/kWh". Now converted to the proper symbol for common currencies (EUR, USD, GBP, JPY, CNY, KRW, INR, RUB, BRL, TRY, ILS, MYR, NGN, PHP, THB, TWD, VND); unknown codes still fall back to the raw code.
- **Instalment changes were applied retroactively to the entire elapsed contract period**: raising or lowering the instalment mid-contract made "Refund/balance due (so far)" and "Instalment adjustment (recommended)" incorrectly calculate as if the NEW instalment had applied since day one. Tariffy now automatically remembers the date and previous value on every instalment change and applies the old instalment correctly only up to that date, the new one from then on. Multiple corrections on the same day count as a single change (no retroactive intermediate state).

## [1.22.0] - 2026-07-14

### Added

- **Optional low-instalment warning** (per contract, electricity/gas/water with a consumption sensor): warns via persistent notification (+ optional push notification) when the contract-end forecast (`prognose_real`) projects a balance due beyond a configurable threshold (default 50 €). New "Confirm low-instalment warning" button to dismiss — if the forecast worsens again afterwards, it fires again automatically (no permanent mute). Raw state also exposed as the `abschlag_warnung_aktiv` attribute on the "Refund/balance due (contract end)" sensor.

## [1.21.0] - 2026-07-14

### Fixed

- **"Expected str" error on calorific value/state number when editing an existing gas contract**: the schema default for these fields was a `float` (the stored value), but `TextSelector` strictly requires a string. Submitting the pre-filled form unchanged sent a raw float instead of a string, so validation failed with "expected str" — before the comma/dot normalization logic even ran. Only actively editing the value (e.g. to a comma) produced a genuine string, which then worked. Schema defaults for these fields are now always declared as strings.
- **Calorific value/state number/gas unit were missing entirely when planning a successor gas contract**: an automatic tariff switch would silently carry over the old contract's values with no way to correct them for the new provider. These fields are now available in the options flow for gas contracts.

## [1.20.0] - 2026-07-12

### Fixed

- **README.md was missing the "four cost sensors" explanation entirely**: the detailed 2×2 grid and worked numeric example for `jahreskosten`/`kosten_bisher`/`guthaben_bisher`/`prognose_real` had only been added to a separate documentation copy, never to this repo's actual README.md (the one HACS/GitHub display). Added to both the English and German sections now.

## [1.19.0] - 2026-07-12

### Fixed

- **README.md/CHANGELOG.md kept getting deleted from installations by HACS**: both files previously lived only at the repo root, not inside `custom_components/tariffy/`. HACS syncs that folder 1:1 from the repo, so any local file not part of the official package got removed on every update. Both files now also live inside `custom_components/tariffy/` so they're retained as part of the package.

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
