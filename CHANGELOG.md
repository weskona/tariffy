# Changelog

All notable changes to Tariffy are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.27.0-rc.2] - 2026-11-06

Second release candidate for testing the sidebar panel. The panel uses the whole width of the window, the header of the overview has more details and the cost tables line up. Please report problems with the bug report form and mention this exact version.

### Changed

- The header of the overview has four tiles with details: the instalments per month (with the yearly figure and a bar that splits metered and flat-rate contracts), the cost so far (with the instalments due until today and the balance), the forecast at contract end (per contract, worst first) and the next three dates.
- The two tables of the "Costs" view share one column grid: "cost so far" and "instalment" sit exactly below each other (flat-rate table: cost so far, remaining term, contract end, instalment).
- The panel uses the whole width of the window instead of being capped at 1280 px and centred (the cap is now 2400 px, only for ultra-wide monitors). The overview keeps three contracts per row and gets a fourth column on a very wide window (1750 px and more).

## [1.27.0-rc.1] - 2026-11-06

Same content as 1.27.0-beta.10, released again under a new name: GitHub lists `beta.10` between `beta.2` and `beta.1`, so HACS did not offer it. Please install this version (see "Beta releases" in the documentation; the numbering now continues with `rc.2`, `rc.3`, ...). Please report problems with the bug report form and mention this exact version.

### Changed

- The "Costs" view has two tables like the overview: **metered contracts** (cost so far, balance so far, balance at contract end, instalment, recommended instalment) and **flat-rate contracts** (cost so far, instalment, contract end, remaining term), each with its own total row and the overall total below. The "Contracts" view lists the contracts in the same two groups.
- On a wide screen the overview shows three contracts per row, in both groups. The small arrow that opens a row or card is an icon in the style of the other icons and turns when it opens.
- Release process: version numbers of pre-releases stop at 9 per series (`beta.1` ... `beta.9`, `rc.1` ... `rc.9`), because GitHub sorts release tags as text and HACS would not offer `beta.10`. A test guards this.

## [1.27.0-beta.10] - 2026-11-06

Tenth beta for testing the sidebar panel. The "Costs" and "Contracts" views are now split like the overview. Please report problems with the bug report form and mention this exact version.

### Changed

- Beta: the "Costs" view has two tables like the overview: **metered contracts** (cost so far, balance so far, balance at contract end, instalment, recommended instalment) and **flat-rate contracts** (cost so far, instalment, contract end, remaining term). Each table has its own total row, and the overall total sits below. Flat-rate contracts no longer show rows of dashes for balance and forecast.
- Beta: the "Contracts" view lists the contracts in the same two groups.
- Beta: the small arrow that opens a row or card is an icon in the style of the other icons and turns when it opens.
- Beta: on a wide screen the overview shows three contracts per row, in both groups (before: two columns for four metered contracts).

## [1.27.0-beta.9] - 2026-11-06

Ninth beta for testing the sidebar panel. The overview is sorted by kind of contract, flat-rate contracts get their own cards, and everything that changes a contract moved to the "Contracts" tab. Please report problems with the bug report form and mention this exact version.

### Changed

- Beta: the overview has two groups: **metered contracts** (electricity, gas, water) in big cards and **flat-rate contracts** (internet, mobile, insurance, other) in slim cards. Cards sit in rows of equal height; four metered contracts make 2 x 2 instead of leaving one card alone in a row.
- Beta: a flat-rate card leads with the monthly instalment and shows the cost so far, the contract end and a term bar. It has no ring, no consumption and no empty figures; a contract without an end date shows "No contract end" instead of a dash or an assumed 12-month total.
- Beta: the cost table treats flat-rate contracts: the cost so far is the instalments due until today (also in the total and in the contract details). Balance and forecast stay empty because there is no consumption.
- Beta: the overview has no editing actions any more. Everything that changes a contract is in the "Contracts" tab: icons in each row (plan or edit the next contract, edit the contract) and the button "New contract" at the top. Deleting stays in the edit dialog. "Acknowledge warning" and "Acknowledge cancellation" remain on the card next to their note.

### Added

- The contract data now contains the instalments due until today (`abschlag_bisher_gezahlt`, stops at the contract end and respects an instalment change). It is only a value for the panel: no new sensor, so existing installations get no new entities.

## [1.27.0-beta.8] - 2026-11-06

Eighth beta for testing the sidebar panel. New: a redesigned overview. Please report problems with the bug report form and mention this exact version.

### Changed

- Beta: redesigned overview, closer to the style of the reference dashboard. The cards now flow into columns without gaps instead of a grid with holes, the top of a card is tinted by its state (green credit, red balance due, orange cancellation due), titles are set in small capitals and the key figure sits next to a smaller progress ring. A card shows at most three figures (costs so far, balance so far, consumption) plus a footer line with the remaining term; the balance so far, the consumption and the instalments remain in the "Costs" and "Contracts" views.
- Beta: "Plan next contract" and "Edit contract" moved into a "..." menu in the card header (administrators only). Acknowledge warning and acknowledge cancellation stay on the card, next to the note they belong to. On phones the buttons stay in the opened card.
- Beta: contracts without start or end date no longer show an empty progress ring, and empty figure tiles are left out.

### Fixed

- Beta: on the first day of a contract with a consumption sensor the "Consumption" block of the contract details is shown (costs and consumption so far exist, only the forecast is still missing). It used to stay hidden until the next day.
- Beta: a menu on a card stayed open behind the dialog after choosing an entry.

## [1.27.0-beta.7] - 2026-11-06

Seventh beta for testing the sidebar panel. It fixes the layout of the contract list. Please report problems with the bug report form and mention this exact version.

### Fixed

- Beta: in the "Contracts" view the rows were squeezed: the name and the subtitle broke word by word and the amount was drawn over the text. The rows now show name, status and amount on one line and wrap on narrow screens. The overview cards are unchanged.

## [1.27.0-beta.6] - 2026-11-06

Sixth beta for testing the sidebar panel. New: create and delete contracts directly in the panel (administrators only). Please report problems with the bug report form and mention this exact version.

### Added

- Beta: the panel can now create contracts ("New contract" in the top bar, administrators only). It runs the integration's own setup dialog (name and sparte first, then the data of the sparte), so validation and storage are unchanged, and the new contract appears in the panel by itself.
- Beta: the panel can now delete a contract ("Delete contract" in the edit dialog, administrators only). Because it cannot be undone, the name of the contract has to be typed before the button works. The sensors and buttons of the contract are removed; the long-term statistics Home Assistant already recorded stay in its database (the dialog says so).

### Fixed

- Deleting a contract (in the panel or in Home Assistant) now also dismisses its open cancellation and low-instalment notifications. Until now they stayed in the notification list for good.

## [1.27.0-beta.5] - 2026-11-06

Fifth beta for testing the sidebar panel. New: edit a contract directly in the panel (administrators only). Please report problems with the bug report form and mention this exact version.

### Added

- Beta: the panel can now edit a contract ("Edit contract" on the contract card, administrators only). It shows the same two forms as the integration's "Reconfigure" dialog (general data, then the data of the sparte) and stores them through that dialog, so validation and storage are unchanged. The last step asks once more before the contract data is replaced. Yes/no settings, drop-downs with translated names and free-text suggestions (notification target) are supported.

### Fixed

- Reconfiguring a contract no longer loses the state the integration keeps itself. Until now the "Reconfigure" dialog replaced the stored data with what the forms contain, so an acknowledged cancellation reminder or low-instalment warning came back, a push notification that was already sent could be sent again, and the consumption of the last contract term (used for the recommended instalment) was lost. It is now kept. The cancellation reminder starts over only when the contract end or the reminder lead time changes.
- The "Cancellation reminder" drop-down shows "3 months before" instead of a bare "3" (the texts already existed but were not connected). The stored values are unchanged.

## [1.27.0-beta.4] - 2026-11-06

Fourth beta for testing the sidebar panel. New: plan, edit and remove the next contract directly in the panel (administrators only). The two action buttons now ask a second question, and "Switch now" is gone from the panel because it would have replaced the current contract before the new one starts. Please report problems with the bug report form and mention this exact version.

### Added

- Beta: the panel can now plan, edit and remove the next contract ("Plan next contract" on the contract card, administrators only). It shows the same form as the integration's "Configure" dialog and stores it through that dialog, so validation and storage are unchanged. When the cancellation reminder is due, a box (ticked by default) marks the cancellation as done in the same step.

### Changed

- Beta: the two remaining action buttons in the panel (acknowledge warning, acknowledge cancellation) now ask for a second confirmation, so nothing can be triggered by an accidental click.
- Beta: the panel no longer offers "Switch now". It would have replaced the current contract at once while the new one still starts on its planned date. The contract switches itself on that date; the button entity in Home Assistant is unchanged. The unused websocket action `switch_now` was removed with it.

## [1.27.0-beta.3] - 2026-11-06

Third beta for testing the sidebar panel. New: acknowledging the warning and the cancellation reminder and switching to a planned next contract directly in the panel (administrators only), and a clearer display when a negative instalment is recommended. Please report problems with the bug report form and mention this exact version.

### Added

- Beta: the panel can now acknowledge the low-instalment warning, acknowledge the cancellation reminder and switch to a planned next contract directly from the contract card, with a confirmation question before the switch. The same actions as the three buttons, available to administrators only (new websocket command `tariffy/action`, which checks the same conditions as the buttons). Everyone else keeps the read-only view.

### Changed

- Beta: when the credit already covers the costs until the end of the contract, the panel no longer shows a negative recommended instalment. It shows 0.00 € with the note "Credit covers the costs". The sensor "Instalment adjustment (recommended)" itself is unchanged.

## [1.27.0-beta.2] - 2026-11-06

Second beta for testing the sidebar panel. It contains the forecast fix from 1.26.6, so the panel shows the corrected "Credit / balance due (contract end)" after an instalment change. The panel itself is unchanged and read only. Please report problems with the bug report form and mention this exact version.

### Fixed

- "Refund/balance due (contract end)" (and with it the low-instalment warning) was too optimistic after an instalment change during the contract. The forecast now uses the instalments actually paid so far plus the current instalment for the remaining term, see 1.26.6. Contracts whose instalment was never changed keep exactly the same value.

## [1.27.0-beta.1] - 2026-11-05

Beta release for testing the new sidebar panel. The panel only reads, everything else works as in 1.26.5. Please report problems with the bug report form and mention this exact version. HACS offers this version only if "Show beta versions" is enabled.

### Added

- Beta: the panel now shows the contracts in a dark, card based design (overview with summary, cost table, contract details), in German and English, with a compact expandable layout on phones. Read only. The page is delivered by the integration, uses the system font and needs no build step.
- Beta: backend for a Tariffy sidebar panel. It registers the "Tariffy" panel (visible to all users) and two read-only websocket commands, `tariffy/contracts` and `tariffy/subscribe`, that deliver the calculated values of all contracts, without customer number, meter numbers, MaLo-ID and notification target. If the panel cannot be set up, a warning is logged and the integration works as before. `manifest.json` lists `frontend`, `http`, `panel_custom` and `websocket_api` in `after_dependencies`.

### Changed

- CI: the release workflow now also runs on the `beta` branch and publishes versions like `1.27.0-beta.1` as GitHub pre-releases (never marked as latest), so HACS only offers them to users who enabled beta versions. Stable releases from `main` work as before. See `docs/beta-releases.md`.

## [1.26.6] - 2026-11-05

### Fixed

- **"Refund/balance due (contract end)" (and with it the low-instalment warning) was too optimistic after an instalment change during the contract.** The forecast assumed the current instalment for the whole term, although "Refund/balance due (so far)" and the instalment recommendation correctly counted the older, different instalment up to the change date. Example: instalment raised from 40 € to 100 € in July, the sensor showed a credit at contract end while the balance so far was negative. The forecast now uses the instalments actually paid so far plus the current instalment for the remaining term. For contracts whose instalment was never changed the value is exactly the same as before. "Installment total (contract term)" stays the plain payment plan (instalment × term).

### Changed

- CI: the release workflow now also runs on the `beta` branch and publishes versions like `1.27.0-beta.1` as GitHub pre-releases (never marked as latest), so HACS only offers them to users who enabled beta versions. Stable releases from `main` work as before. See `docs/beta-releases.md`.

## [1.26.5] - 2026-11-05

### Fixed

- If a tariff switch fell into the very first refresh after a Home Assistant start, the consumption of the ended contract period was not frozen, so the new contract had no "Consumption (last period)" and no recommended monthly payment. The contract-start meter value is now read in that case too. Contracts with a manually entered start value are unchanged.
- After a tariff switch (automatic on the switch date or via the "Switch now" button) the integration reloads again, as it did before 1.26.3. Since 1.26.3 the sensor set (night rate, tiered pricing) was no longer rebuilt after a switch, so a next contract with different features did not get its sensors until Home Assistant was restarted.

### Changed

- Added automated tests for the cost and forecast calculation, tariff switch, cancellation reminder and instalment warning, including a regression test for the missing sensors after a tariff switch. CI runs them on every push and pull request.

## [1.26.4] - 2026-11-05

### Changed

- `manifest.json` now declares `recorder` in `after_dependencies`, since the integration reads Long-Term Statistics.
- The coordinator now passes its config entry to `DataUpdateCoordinator` (`config_entry=`), as newer Home Assistant versions expect.
- Removed an unused variable and two unused imports.
- CI: added `ruff` (correctness rules only) and the official `hassfest` check.

## [1.26.3] - 2026-11-05

### Fixed

- **HA Core warning "custom integration 'tariffy' has an update listener and should use it for scheduling a reload"** (will stop working in Home Assistant 2026.12.0, [#2](https://github.com/weskona/tariffy/issues/2)): the manual update listener was replaced by `OptionsFlowWithReload`, so saving the options flow still reloads the entry. Internal data changes (manual switch, confirming cancellation/instalment warning) now trigger a coordinator refresh instead of a full reload. Minimum Home Assistant version raised to 2025.8.0 in `hacs.json`.

## [1.26.2] - 2026-08-25

### Fixed

- **Price fields silently ignored their configured step size**: the internal `_preis()` helper used by roughly two dozen config-flow price fields (unit prices, base price, instalment, low-instalment warning threshold) accepted a `step` argument but never actually passed it to the underlying number selector — every price field always used the generic `step="any"` regardless of what precision it was meant to have (e.g. 0.0001 for unit prices, 0.01 for base price/instalment, 1.0 for the warning threshold). Fixed to use the given step — except for the eight unit-price fields requesting 0.0001: Home Assistant's `NumberSelector` hard-rejects any step below 0.001 (throws when the form is built, it doesn't just round), so those keep `"any"` since no valid finer step exists; the base price/instalment/warning-threshold fields (0.01/1.0) now correctly get a real spinner step.
- **"Plan next contract" was missing the low-tariff (NT) fields for dual-tariff (HT/NT) contracts**: the options flow for scheduling an upcoming tariff switch only exposed a single "Unit price new" field, even for the dual-tariff meter category which tracks high and low tariff independently — there was no way to plan a rate change for the NT register alongside the HT one. Added "Unit price new, low tariff / NT", "Consumption sensor new, low tariff / NT", and "Meter number new, low tariff / NT", shown only for HT/NT contracts, right after the existing unit price field.
- **English translations were massively incomplete — 311 of 470 keys missing**: `translations/en.json` was never kept in sync with `strings.json` (the German file, `translations/de.json`, had full parity). Missing entirely: the whole "Water" and "Electricity (dual tariff, HT/NT)" setup steps, most config-flow field labels for tiered/block pricing and day/night rates, every single field-hint description (`data_description`) across all steps, and two dropdown option labels (the HT/NT category itself, and all three wastewater-pricing-model options) — all of these showed their raw internal key instead of readable English text. Filled from `strings.json` (the authoritative English source) without touching any of the 159 keys that were already correct; both files now have identical structure and matching key sets. Also removed two orphaned translation keys (`prognose`, `geschaetzte_jahreskosten`) from `strings.json` — no sensor in the code references them anymore.

## [1.26.1] - 2026-08-07

### Added

- **Dual-tariff meter category (HT/NT — high tariff / low tariff)**: a new "Electricity (dual tariff, HT/NT)" category for a real two-register electricity meter. Adds a second unit price, second consumption sensor, second manual meter-reading override and second meter number for the low-tariff register, tracked completely independently from the high-tariff one (its own Long-Term Statistics offset, its own manual-override fallback). The existing combined sensors (Cost/Refund/Forecast so far, etc.) keep working exactly as for any other electricity contract — the two registers' consumption is summed, and the unit price used by all downstream formulas becomes an automatically weighted average of both tariffs' prices. Four new dedicated sensors expose the per-register breakdown: Consumption (high/low tariff, so far) and Cost (high/low tariff, so far) — the latter is the pure usage-based cost of that register, without a base-fee share.

## [1.25.1] - 2026-07-30

### Fixed

- **"Consumption (so far)" could suddenly show an implausibly high value due to an anomaly in
  Home Assistant's own recorder `sum` long-term statistic**, even though the sensor's raw meter
  reading stayed perfectly continuous and correct (observed: after a Home Assistant restart, the
  `sum` statistic jumped to roughly double within a single hour, while the actual meter reading
  changed by only 0.1 kWh in that same hour). The calculation now also reads the sensor's raw
  `state` value alongside the `sum` statistic and cross-checks both: if the current reading
  hasn't dropped below the value at contract start (the normal case — no real meter reset), it
  uses the simpler, more robust state difference instead of the potentially glitched `sum`
  statistic. A genuine meter reset (common for some gas meters) is still correctly handled via
  the reset-safe `sum` statistic. This automatically resolves the issue reported in #1 without
  needing the manual meter-reading override added in 1.25.0 — that option remains available for
  the rarer case where a sensor's statistics history genuinely doesn't reach back to the contract
  start date.

## [1.25.0] - 2026-07-26

### Added

- **Optional manual meter reading at contract start** (Electricity/Gas/Water): a new "Meter
  reading at contract start" field overrides the automatically detected reference value from
  Home Assistant's recorder long-term statistics as soon as it is set. Covers the case where the
  consumption sensor's statistics history does not reach back to the contract start date (e.g.
  because the sensor was renamed or recreated at some point, even if the plain state history
  looks continuous) — previously this led to an incorrect calculation ("Consumption (so far)"
  showed the full meter reading instead of the delta since contract start).

## [1.24.4] - 2026-07-26

### Fixed

- **"Unable to remove unknown job listener" error on every reload after Home Assistant startup**:
  the one-time `EVENT_HOMEASSISTANT_STARTED` listener was tracked via `entry.async_on_unload()`
  even though it already removes itself once it fires — any reload happening after that point
  tried to remove it a second time. Now checks `hass.is_running`: if HA is already running, the
  refresh happens immediately instead of waiting for an event that will never fire again, and the
  listener is no longer redundantly tracked for removal.

## [1.24.3] - 2026-07-14

### Fixed

- **1.24.2's `zip_release` broke HACS's ability to see/install the release entirely**: the release zip wrapped everything under `custom_components/tariffy/` (plus `hacs.json`/`README.md`/`LICENSE` at the root), but HACS's `zip_release` mode expects the integration's files directly at the zip root (verified byte-for-byte against HACS's own `hacs.zip` release asset, which has `manifest.json` etc. at the top level, no `custom_components/hacs/` wrapper). The release workflow now zips the *contents* of `custom_components/tariffy/` directly.

## [1.24.2] - 2026-07-14

### Fixed

- **HACS download counter always showed 0**: `hacs.json` didn't set `zip_release`/`filename`, so HACS silently fell back to GitHub's auto-generated source archive for each release instead of the `tariffy.zip` asset our release workflow uploads — and GitHub only tracks download counts for actual uploaded release assets, not auto-generated source archives. Added `"zip_release": true, "filename": "tariffy.zip"` so HACS fetches the tracked asset.

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
- For meters that reset periodically, configure a true never-resetting cumulative sensor as the consumption sensor where available (e.g. a separate utility meter with `cycle: none`), rather than relying solely on the `sum` statistic.

### Fixed

- **Crash (500 Internal Server Error) when creating/editing a gas contract**: an initial attempt to accept decimal-comma input (`11,2`) for calorific value / state number used a schema validator that `voluptuous_serialize` could not convert to JSON for the frontend. Calorific value and state number are now plain text fields in the schema; comma/dot normalization happens after form submission, with a clean validation error instead of a crash on invalid input.
- **Calorific value / state number now accept decimal commas** (`11,2` as well as `11.2`) — the native HTML5 number field didn't reliably handle commas depending on browser/locale.

## Before 1.12.0

No structured changelog prior to this version.

[Unreleased]: https://github.com/weskona/tariffy/compare/v1.27.0-beta.3...HEAD
[1.27.0-beta.3]: https://github.com/weskona/tariffy/compare/v1.27.0-beta.2...v1.27.0-beta.3
[1.27.0-beta.2]: https://github.com/weskona/tariffy/compare/v1.27.0-beta.1...v1.27.0-beta.2
[1.27.0-beta.1]: https://github.com/weskona/tariffy/compare/v1.26.5...v1.27.0-beta.1
[1.26.6]: https://github.com/weskona/tariffy/compare/v1.26.5...v1.26.6
[1.26.5]: https://github.com/weskona/tariffy/compare/v1.26.4...v1.26.5
[1.26.4]: https://github.com/weskona/tariffy/compare/v1.26.3...v1.26.4
[1.26.3]: https://github.com/weskona/tariffy/compare/v1.26.2...v1.26.3
[1.26.2]: https://github.com/weskona/tariffy/compare/v1.26.1...v1.26.2
[1.26.1]: https://github.com/weskona/tariffy/compare/v1.25.1...v1.26.1
[1.25.1]: https://github.com/weskona/tariffy/compare/v1.25.0...v1.25.1
[1.25.0]: https://github.com/weskona/tariffy/compare/v1.24.4...v1.25.0
[1.24.4]: https://github.com/weskona/tariffy/compare/v1.24.3...v1.24.4
[1.24.3]: https://github.com/weskona/tariffy/compare/v1.24.2...v1.24.3
[1.24.2]: https://github.com/weskona/tariffy/compare/v1.24.1...v1.24.2
[1.24.1]: https://github.com/weskona/tariffy/compare/v1.24.0...v1.24.1
[1.24.0]: https://github.com/weskona/tariffy/compare/v1.23.0...v1.24.0
[1.23.0]: https://github.com/weskona/tariffy/compare/v1.22.0...v1.23.0
[1.22.0]: https://github.com/weskona/tariffy/compare/v1.21.0...v1.22.0
[1.21.0]: https://github.com/weskona/tariffy/compare/v1.20.0...v1.21.0
[1.20.0]: https://github.com/weskona/tariffy/compare/v1.19.0...v1.20.0
[1.19.0]: https://github.com/weskona/tariffy/compare/v1.18.0...v1.19.0
[1.18.0]: https://github.com/weskona/tariffy/compare/v1.17.0...v1.18.0
[1.17.0]: https://github.com/weskona/tariffy/compare/v1.16.0...v1.17.0
[1.16.0]: https://github.com/weskona/tariffy/compare/v1.15.0...v1.16.0
[1.15.0]: https://github.com/weskona/tariffy/compare/v1.14.0...v1.15.0
[1.14.0]: https://github.com/weskona/tariffy/compare/v1.13.0...v1.14.0
[1.13.0]: https://github.com/weskona/tariffy/compare/v1.12.0...v1.13.0
[1.12.0]: https://github.com/weskona/tariffy/releases/tag/v1.12.0
