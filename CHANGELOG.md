# Changelog

All notable changes to Tariffy are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.33.0-beta.1] - 2026-11-20

First beta of 1.33.0. Please report problems with the bug report form and mention this exact version.

### Added

- **New category "House costs"** (requested in #121) for the running costs around the house that have no meter: waste fees, street cleaning, rainwater (stormwater fee), property tax, chimney sweep, winter service and the like. It is a normal **flat-rate contract** (payment interval, amount per payment, start, end, reminder, one-time items, renew, plan next contract) with an additional, optional **type**: choose it from a list (waste fees, street cleaning, rainwater, property tax, chimney sweep, winter service, caretaker / building services) **or type your own**. House costs **count in the totals** (instalments per month, cost so far, the cost split, the yearly sums) and have a group of their own in the panel, **House costs**; the panel says "amount" instead of "instalment" for them. Other contracts are not changed.

### Changed

- **New brand icon.** Tariffy has a new icon (a contract with a euro coin on a blue-violet gradient) and a logo with the name, also for the dark design. They are shown by Home Assistant in the list of integrations and by HACS. Only images change; nothing else is affected.

## [1.32.0] - 2026-11-19

This release brings together everything that was tested in the betas `1.32.0-beta.1` to `1.32.0-beta.9` and the release candidates `1.32.0-rc.1` to `1.32.0-rc.3`. **Existing contracts keep working without any change.** All new functions are optional or only add something.

### Added

- **New category "Leasing"** (requested in #90) for a car lease. The rate is a normal **flat-rate contract**; on top of that Tariffy watches the **kilometres**: an **odometer sensor** (miles are converted) or the odometer entered by hand, the odometer at the start, the **allowed kilometres per year** and/or over the whole term, a **tolerance upwards and downwards** and a **price per extra kilometre / credit per kilometre not driven**. Tariffy shows the kilometres driven, the target by now, what is left, your average per day and the **projection at the return date** with the **expected extra payment or credit**. Three more sensors (**Kilometres driven**, **Projected kilometres at return**, **Expected extra/shortfall kilometre cost**); the kilometre cost is an estimate and not part of the totals. Leasing contracts stand in the group **"Loans / financing"** of the overview and the list and count in the totals like any flat-rate contract.
- **Own icon for every contract** (requested in #93). Optional field **Icon** (for example `mdi:car`) in the contract form; used in the panel and for the sensors of the contract. Empty = the icon of the category.
- **Light design.** The panel follows the design of Home Assistant (light, dark or automatic, no setting of its own); the dark design is unchanged.
- **Customer number, meter number(s) and MaLo ID in the contract details** of the panel, for administrators only, each with a symbol to copy the value.
- **Total consumption and "covered by PV"** (requested in #86): with PV self-sufficiency and a total-consumption sensor the block **Consumption** shows total consumption, share covered by PV and grid draw (billed), so far and projected. Also attributes of the sensor "Refund/balance due (contract end)".
- **Instalments paid: correct what was really charged.** In the **Contracts** tab the dialog **Edit instalments** has a field per payment of the term (monthly one per month, quarterly four a year, half-yearly two, yearly one); payments that were not due yet stay locked. **Paid so far**, the balance, the forecast at contract end and the recommended instalment use the amounts that really applied. Without entries nothing changes.
- **Earlier terms: instalments by payment.** The dialog for an earlier term (tab **History**) has an optional section with a field for every payment of the term; **Paid** and the balance are worked out from it.
- **Renew a contract without an end date** (requested in #103): the icon **Renew contract** is also shown for flat-rate contracts without a contract end; the end in the dialog is optional.

### Changed

- **Flat-rate contracts: one amount is enough.** The cost form no longer has the second field **Base price (€/month)**; it stays only for contracts that already have one. Existing contracts keep their figures.
- **Plan next contract (category Streaming): a shorter form** with start (suggested as the day after the current end), tariff name, payment interval, amount per payment and end. Streaming contracts say **Price** instead of "Instalment", have no empty "One-time items" block and no duplicate "Instalment / year" row. All other categories keep their form.
- The panel is split into several files (internal); after the update reload the browser page once (Ctrl+F5).

### Fixed

- **The panel stayed empty after a contract was created or changed** (reported in #102): a contract that is being set up is now part of the list sent to the panel.
- **The panel stayed black when it was opened** until another dashboard was opened and back: the panel now defines itself at once, takes back values that were set earlier and draws itself when its parts have arrived; if a part cannot be loaded, an error is shown.
- **A flat-rate contract with a yearly, half-yearly or quarterly payment fell back to monthly at an automatic switch.** The payment interval is now taken over into the new term.

## [1.31.0] - 2026-11-17

This release brings together everything that was tested in the betas `1.31.0-beta.1` and `1.31.0-beta.2`. **Existing contracts keep working without any change.** The new option is off by default.

### Added

- **PV self-sufficiency in the forecast of the final cost** (requested in #86), for electricity contracts (also dual-tariff meters). Optional and **off by default: without it nothing changes**. In the contract form you switch it on and give the source of the self-sufficiency, in this order: **(1) the total consumption of the house** as a sensor (for a dual-tariff meter optionally a second one for the low-tariff period; the most exact source, it works with a battery), **(2) a self-sufficiency sensor in %** (monthly mean of last year, for example Fronius; it is an instantaneous value, so it can deviate a few percent from the Energy dashboard) or **(3) own values in %** (**twelve values**, January to December; they also fill months without data and are enough on their own, for example in the first year of a PV system. Without a sensor the values must differ between months: one value for all months changes nothing, because the forecast compares every month with the measured period, and the form says so). For every month of the **remaining term** Tariffy takes the **same month of last year** and works out the self-sufficiency (for (1) `1 − grid draw / total consumption`, limited to 0–100 %). Because the consumption sensor of the contract measures the grid draw, the daily grid draw so far is **normalised for the season** (self-sufficiency of the month against the self-sufficiency in the measured period). The consumption so far stays as it is; the forecast at contract end, the recommended instalment and the projected consumption follow the remaining months. A dual-tariff meter is calculated per tariff (with one total sensor over both together, marked as an approximation). Missing data for a month keeps the linear extrapolation for that month, without any history nothing changes.
- The sensor "Refund/balance due (contract end)" gets the attributes `autarkie_variante`, `autarkie_monatswerte`, `autarkie_bisher`, `autarkie_naeherung` and `prognose_ohne_autarkie` (only when the self-sufficiency applies); the panel shows the forecast without it and the self-sufficiency so far. `autarkie_variante` names the source (`gesamtverbrauch`, `entitaet`, `manuell`). No new sensors. A tariff switch keeps the setting. Not included: a consumption sensor that measures the total consumption instead of the grid draw.

## [1.30.0] - 2026-11-16

This release brings together everything that was tested in the betas `1.30.0-beta.1` and `1.30.0-beta.2`. **Existing contracts keep working without any change.** The new category is optional; new sensors exist only for loans.

### Added

- **New category "Loan / financing"** (requested in #61) for annuity loans, instalment loans and car financing. A loan is kept **apart from the contracts**: it has a group of its own in the panel (overview, costs, contracts) and does not count in the totals of the contracts or in the cost split. In the form you enter the loan amount, the **nominal interest rate** and/or the **effective annual rate**, the term in months, the payment interval (monthly to yearly) and, optionally, the **rate** (empty = Tariffy calculates the annuity; a rate that does not fit the interest is reported), a **final payment / residual value** and the **date of the first payment** (empty = one interval after the start, a monthly loan: the end of the first month).
- Tariffy works out the **repayment plan**: the **remaining debt**, **paid so far** (interest and principal), the **remaining payments** until the end, interest so far and over the whole term, the payments made, the next rate split into interest and principal and the progress of the repayment. A loan has four sensors (**Remaining debt**, **Paid so far**, **Remaining payments**, **Interest paid so far**); other contracts get none.
- **Follow-up financing** with the existing "Renew contract" icon: the remaining debt is suggested as the new amount, with a new interest rate and term; the current term goes to the history. Not included: special repayments and an interest rate that changes during the term.

### Changed

- **The block "Outdoor meters" of a water contract** stands below the other blocks, over the whole width, with the meters in several columns next to each other (up to ten fit). The split of the water (outdoor water, wastewater-liable consumption and the two costs) is shown in the block "Consumption", next to "so far" and "cost so far".

### Fixed

- **Outdoor meters and one-time items stuck out of their column in the contract details.** A long entity id of an outdoor meter pushed the figures out of the block and over the neighbouring block. Names and entity ids now wrap, and a long description of a one-time item wraps as well.

## [1.29.1] - 2026-11-16

### Fixed

- **Editing a contract removed its one-time items and its outdoor meters.** Saving the form "Edit contract" (in the panel or in Home Assistant under "Reconfigure") dropped the one-time items (bonus, bill) and the outdoor meters of a water contract, because they were not on the list of values that an edit keeps. They are kept now. A tariff switch also keeps the one-time items of the contract. Contracts that never had one-time items or outdoor meters are not affected. If you added items or meters with 1.29.0 and then edited the contract, enter them again.

## [1.29.0] - 2026-11-16

This release brings together everything that was tested in the betas `1.28.0-beta.1` to `1.28.0-rc.9` and `1.29.0-beta.1` to `1.29.0-beta.3` (there is no stable 1.28.0; the numbering continued at 1.29.0 because GitHub lists numbers above 9 in the wrong order, see "Beta releases" in the documentation). **Existing contracts keep working without any change.** Everything new is optional and stored in the contract data; new sensors exist only where stated below. A few numbers change for existing contracts, they are listed under "Changed" and "Fixed".

### Added

- **Contract history and archive.** When the next contract takes over, the old term is saved (term, provider, tariff, prices, instalment, cost, consumption and balance at the end; up to 50 terms). The new **History** tab shows the terms under each contract. An expired contract without a next contract is marked **Expired** and can be **archived** (and restored) in the "Contracts" tab; nothing is deleted and nothing is archived automatically.
- **Add old contracts by hand** in the History tab (administrators): consumption, cost, instalments paid and balance are worked out automatically from the long-term statistics of the meter, and every value can be typed in.
- **Backup and restore.** The new **Backup** tab downloads all contracts as a file and restores contracts from such a file (only contracts that do not exist yet; the file is checked strictly; it contains personal data). **Deleted contracts are kept for 30 days** and can be brought back.
- **The name of a contract can be changed** when editing it.
- **Payment interval and yearly values for flat-rate contracts** (monthly, quarterly, half-yearly, yearly) and an optional **date of the first debit**. Internally the amount per month stays the basis, so existing contracts stay exactly as they are.
- **Renew flat-rate contracts** (insurance, internet, mobile, streaming, other) with a new start, end and amount; the old term goes to the history. Meant for a premium that rises every year.
- **Total cost over all terms** of a contract (tile, line, details, History tab).
- **One-time items per contract** (bonus for switching positive, broker's fee negative): they change the balance so far and the total cost.
- **Cost split in the "Costs" tab**: a ring chart per category (or per contract), switchable between "Cost so far" and "Per year", with a year selection and a bar for consumption against flat-rate contracts.
- **Notice period and minimum term** per contract (optional, in months). With a notice period the cancellation reminder counts from the last day to cancel: notice period 3 months and reminder "3 months before" means the message comes 6 months before the contract end. Without a notice period nothing changes.
- **More details for insurance contracts**: type of insurance and, for a car insurance, licence plate, odometer and allowed kilometres. The form asks only for what fits the type.
- **New category "Streaming"** for subscriptions (a flat-rate category with its own icon).
- **Outdoor meters for a water contract** (garden, pool, irrigation): water through such a meter is not charged wastewater (wastewater-liable consumption = main meter − outdoor meters, optional own price). The cost, the forecast and the recommended instalment use the weighted price. A contract **with** an outdoor meter gets four more sensors; **contracts without one get no new sensor and no other number**.
- The sidebar panel shows the flat-rate cards four per row on wide screens.

### Changed

- **"Cost so far" of flat-rate contracts counts the rates booked** instead of a share of the days: every rate counts on its payment day, a monthly rate from the first day of its month (17.99 € a month since 1 April shows 143.92 € on 13 November, eight rates). The yearly values, the instalment and everything about consumption contracts are unchanged.

### Fixed

- **A meter that reports in Wh or MWh gave a consumption that was 1000 times too high** (or too low). The unit of the consumption sensor is now read and the consumption is calculated in kWh (Wh ÷ 1000, MWh × 1000); kWh and every other unit stay exactly as they are. A template sensor as a workaround is no longer needed. Reported in #74.
- **"Cost so far" was 0.00 € when the instalment was filled in after the contract was created.** Contracts that were affected are corrected on their own.
- The list of a drop-down in the panel's dialogs was unreadable in some browsers, and date fields stuck out of the dialog on an iPhone.

## [1.27.3] - 2026-11-11

### Fixed

- **The sidebar panel was empty if you only have contracts of one kind** (for example only an electricity, gas or water contract, or only flat-rate contracts such as internet or mobile). The overview failed with "Failed to execute 'appendChild' on 'Node'" because it tried to add a group without contracts. The panel now skips empty groups. Reported in #50.

## [1.27.2] - 2026-11-10

### Added

- **Diagnostics download.** In Home Assistant under Settings > Devices & services > Tariffy > the contract's menu > "Download diagnostics" you get a file with the settings, the last calculated values, whether the last update succeeded, how the consumption was determined (manual start value or statistics, with the raw values) and the state of the meter sensor. Customer number, meter number, market location (MaLo-ID) and notification target are masked. Attach this file to a bug report.
- **A log line when the consumption becomes unknown.** When "Consumption so far" cannot be calculated, Tariffy writes one warning to the Home Assistant log with the reason (no debug logging needed), and one info line when it is known again. Nothing is logged while the state stays the same, so the log does not fill up.

## [1.27.1] - 2026-11-10

### Fixed

- **Consumption and balance sensors briefly turned "Unknown" when a "Meter reading at contract start" was entered and the meter was temporarily unavailable** (water, gas, electricity, including the low-tariff register of a dual-tariff contract). With a manual start value only the live state of the meter was read. When it is `unavailable` or `unknown`, the last recorded statistics value is now used. Without any reading the sensors stay unknown as before. Reported in #46.

## [1.27.0] - 2026-11-07

### Added

- **Sidebar panel "Tariffy".** A new entry in the sidebar shows all contracts at a glance, with live values, in German and English (dark, card based design, compact expandable layout on phones). It has three views: the **overview** (four header tiles with the instalments per month, the cost so far, the forecast at contract end and the next dates; below, the metered contracts and the flat-rate contracts with one card each), the **costs** (two tables with totals) and the **contracts** (list with all details). The panel is delivered by the integration, uses the system font, needs no build step and no extra entities. Everyone who can use Home Assistant sees the values; customer numbers, meter numbers, MaLo-ID and notification target are never sent to the panel. If the panel cannot be set up, a warning is logged and the integration works as before. See `docs/wiki/Panel.md` (German) and `docs/wiki/English.md`.
- **Administrators can work on contracts in the panel**, in the "Contracts" tab: acknowledge the low-instalment warning and the cancellation reminder, plan, edit or remove the next contract, edit a contract, create a new contract and delete one. Everything runs through the existing dialogs of Home Assistant (options flow, reconfigure flow, setup flow), so validation and storage are unchanged, and every action asks a second time (deleting needs the contract name typed). The panel offers no "Switch now": the contract switches itself on its planned date. Non-administrators only see the values; the backend checks the rights again.
- The contract data contains the instalments due until today (`abschlag_bisher_gezahlt`; stops at the contract end and respects an instalment change). It is only a value for the panel: no new sensor, existing installations get no new entities.

### Changed

- When the credit already covers the costs until the end of the contract, the panel shows "No instalment needed: the credit covers the costs until the contract ends" instead of a negative recommendation; otherwise it says "Raise the instalment to ... per month" or "Instalment could drop to ... per month". The sensor "Instalment adjustment (recommended)" itself is unchanged.
- The panel calls "Balance so far" "Balance today" and explains when the balance today and the forecast point in different directions (for example behind today, credit at the end).
- Flat-rate contracts (internet, mobile, insurance, other) have their own cards and their own table. Their cost so far is the instalments due until today.
- CI: the release workflow also runs on the `beta` branch and publishes pre-releases like `1.27.0-rc.1` (never marked as latest, so HACS only offers them to users who enabled beta versions). Stable releases from `main` work as before. See `docs/beta-releases.md`.

### Fixed

- Deleting a contract (in the panel or in Home Assistant) now also dismisses its open cancellation and low-instalment notifications. Until now they stayed in the notification list for good.
- The "Cancellation reminder" drop-down shows "3 months before" instead of a bare "3" (the texts already existed but were not connected). The stored values are unchanged.

## [1.26.7] - 2026-11-06

### Fixed

- **Reconfiguring a contract no longer loses the state the integration keeps itself.** The "Reconfigure" dialog of Home Assistant replaces the stored contract data with what its forms contain. The forms do not contain the integration's own values, so after every reconfiguration an acknowledged cancellation reminder or low-instalment warning came back, a push notification that was already sent could be sent again, and the consumption of the last contract term (the basis of the recommended instalment after a tariff switch) was lost. These values are now kept. The cancellation reminder starts over only when the contract end or the reminder lead time changes. Nothing else changes: all fields of the forms are stored exactly as before.

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

[Unreleased]: https://github.com/weskona/tariffy/compare/v1.27.0...HEAD
[1.27.0]: https://github.com/weskona/tariffy/compare/v1.26.7...v1.27.0
[1.26.7]: https://github.com/weskona/tariffy/compare/v1.26.6...v1.26.7
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
