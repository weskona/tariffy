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


## Sidebar panel

The **Tariffy panel** is a page of its own in the Home Assistant sidebar. It shows all contracts at a glance and lets administrators maintain them there. It replaces no function of the integration: everything is stored through the existing dialogs of Home Assistant, and the sensors and buttons stay as they are.

**After the update:** the panel is part of the integration, there is nothing to install or set up. Restart Home Assistant and hard-reload the browser page once (Ctrl+F5) so the new panel file is loaded.

**Open it:** the **Tariffy** entry (icon `mdi:cash-multiple`) appears in the sidebar as soon as a contract is loaded. Every user sees the panel; it follows the language of Home Assistant (German, otherwise English) and turns cards into expandable rows on phones.

**Five views**

| View | Content |
|---|---|
| **Overview** | Four tiles on top: the **monthly instalments** (with the yearly figure and a bar that splits metered and flat-rate contracts), the **cost so far** (with the instalments due until today and the balance), the **forecast at contract end** (per contract, the worst first; contracts with consumption metering only) and the **next dates** (cancellation deadline, switch, contract end); below two groups with one card per contract: **metered contracts** (electricity, gas, water) and **flat-rate contracts** (internet, mobile, insurance, other). The cards are tinted by their state (green credit, red balance due, orange cancellation due). A metered card shows the forecast at contract end as the big figure next to the progress ring, at most three figures (cost so far, balance today, consumption), instalments paid vs. cost, the remaining term and notes. If the balance today and the forecast point in different directions (behind today, credit at the end), a line says why. A flat-rate card shows the monthly instalment, the cost so far and the contract end with a term bar, without ring and consumption. The overview has no editing actions. |
| **Costs** | Two tables like the overview. **Metered contracts:** cost so far, balance today, balance at contract end, instalment and recommended instalment. **Flat-rate contracts:** cost so far (the instalments due until today), remaining term, contract end and instalment; there is no balance or forecast. Both tables share one column grid, so "cost so far" and "instalment" sit exactly below each other. Each table has a total row, the overall total sits below |
| **Contracts** | Expandable details per contract, in the same two groups: contract data, prices, consumption, recommendations. This is also where **everything that changes a contract** lives, as icons in each row (calendar: plan or edit the next contract, pencil: edit the contract) and the button **New contract** at the top (administrators only) |
| **History** | The **earlier terms** of every contract (term, provider, tariff, instalment, cost, consumption and balance at the end) and the **archived contracts** |
| **Backup** | Administrators only: **download a backup**, **restore from a file** and bring back the **deleted contracts** of the last 30 days (see below) |

Plus is credit, minus is balance due. When the credit already covers the costs until contract end, the recommended instalment shows "0.00 €" with the note "Credit covers the costs", never a negative amount. The values are the sensors' values and update by themselves.

**Who sees and may do what**

- **All users** see the contracts, but only selected values. Customer number, meter numbers, MaLo ID, notification target and internal markers are **not** sent to the panel.
- **Administrators only** get the buttons and dialogs below. The backend checks this again, so a non-administrator cannot trigger the actions through the API either.

**Acknowledging:** planning, editing, creating and deleting are in the **Contracts** tab (icons in the row, button at the top). The overview is read-only and has no buttons. "Acknowledge warning" and "Acknowledge cancellation" appear in the expanded details of the contract in the **Contracts** tab, depending on the situation; the card in the overview keeps the note with the reason. They do the same as the buttons of the contract and ask a second time before anything happens.

**History and archive:** when the next contract takes over on its planned date, Tariffy replaces the contract data (it always did). New: the old term is saved first, with its term, provider, tariff, prices, instalment, cost, consumption and balance at the end, and shown in the **History** tab under the contract. There are no entries for terms that are already over; the history starts with the first switch after the update. At most 50 terms per contract are kept; customer and meter numbers are not part of them. **Adding an old contract by hand:** in the **History** tab (administrators only) the button **Add an old contract** creates an earlier term, for example a contract from two years ago, and the pencil in its row edits it (it can be deleted there too). You pick the contract the term belongs to (meter and kind come from it) and enter start and end, and optionally provider, tariff, price per unit, base price and instalment. **Consumption, cost, instalments paid and balance are worked out automatically** where possible: the consumption from the long-term statistics of the meter in Home Assistant (between start and end; if there are no statistics for that time you enter it yourself), the cost from consumption, price and base price (gas with the calorific value and state number of the contract), the instalments paid from the instalment and the duration, the balance from both. For flat-rate contracts the cost is what was paid. The grey fields show the calculated value and where it comes from; **you can type your own value into any field**, it then takes precedence and the rest follows from it. When you edit a term, the values you did not type are calculated again. Nothing is saved until you click **Save**. If the old contract had another tariff name or other prices, just enter them; tiered prices, dynamic prices and separate prices for high and low tariff are not calculated (enter the cost yourself).

A contract whose end has passed and that has no next contract gets the badge **Expired** in the overview and a note that it can be archived. In the **Contracts** tab its details have the button **Archive** (asks first, administrators only). Then the contract leaves the overview, the costs, the contracts and the totals, appears in the **History** and its reminders and warnings are off. Nothing is deleted: the sensors and their statistics stay, and **Restore** in the History brings the contract back. Nothing is archived automatically.

**Backup and restore:** the normal Home Assistant backups include Tariffy completely. The **Backup** tab (administrators only) adds a backup just for Tariffy:

- **Download backup:** saves all contracts in one file `tariffy-backup-<date>.json`: contract data, history, archived contracts, planned next contract and the internal state (for example acknowledged reminders). **The file contains personal data** (customer number, meter number, market location ID, notification target). Keep it safe and do not pass it on.
- **Restore from a file:** you choose the file and first see what would happen: contracts that do not exist yet are **created**, contracts with the same name and kind are **skipped** and never changed. Only after a confirmation anything is created. The file is checked strictly (known settings only, simple values only, at most 1 MB and 200 contracts); a broken file creates nothing. Restored contracts are new contracts with new sensors; the statistics of the old contract stay with its sensors in Home Assistant.
- **Deleted contracts:** when a contract is deleted (in the panel or in Home Assistant), Tariffy keeps it for **30 days** (at most the last 20) and offers it in the **Backup** tab to **bring back**, after a confirmation. That is not possible if a contract with the same name and kind exists meanwhile. The data are in Home Assistant's storage (`.storage/tariffy.deleted`) and removed after 30 days; **Forget now** (asks first) removes an entry at once, including its personal data.
- **Limit:** the panel exists only while there is at least one contract. If the last contract was deleted, add any new contract first and the panel is back.

**Renew a flat-rate contract:** for contracts without consumption (insurance, internet, mobile, other) that have a **contract end**, every row of the **Contracts** tab has an icon **Renew contract** (two arrows in a circle, administrators only). The dialog suggests: start the day after the current end, new end one year later, interval and amount as before. You enter for example the new premium, and the dialog shows at once by how many percent the contract gets dearer or cheaper (compared per month). With **Renew**:

- The current term goes to the **history** (term, provider, tariff, instalment, instalments paid). So there is one entry per year and you see how the premium rises.
- The contract runs on with the new start, end and amount. Provider, tariff, customer number and everything else stay.
- Acknowledged cancellation reminders and the date of an earlier instalment change belong to the old term and start over; the reminder follows the new end.

Metered contracts (electricity, gas, water) have the **next contract** for this, which takes over by itself on its planned date. Increases in the middle of a term are entered with **Edit contract** (the new instalment applies from the day you save).

**Total cost over all terms:** when a contract has a **history** (for example because you **renew** it every year, or because the next contract took over), Tariffy shows the **total cost** over all terms: the earlier terms from the history plus the running one. For flat-rate contracts it is a tile of its own on the card, for metered contracts a line under the remaining term; it is also in the contract details and, in the **History** tab, under the earlier terms, each with "since <date> · n terms". For an earlier term its cost counts if there is one, otherwise the instalments paid. If a term has neither, it says "at least …" because the sum is not complete. For an archived contract the last term is already in the history and is not counted twice. Without a history there is no extra display.

**Plan the next contract:** "Plan next contract" (or "Edit next contract") shows the same form as "Configure" in Home Assistant; empty fields keep the current value. If a cancellation reminder is due, the box "Mark the cancellation as done" (on by default) acknowledges it in the same step. "Remove planned contract" removes only the plan, after a question. There is deliberately no "switch now" in the panel (it would replace the current contract before the new one starts); the switch happens by itself on the planned date.

**Edit a contract:** "Edit contract" shows the two forms of "Reconfigure" (general data, then the data of the sparte) and asks once more before saving. Acknowledged reminders, "notification sent" markers and the frozen consumption of the last contract term are kept; the cancellation reminder starts over only when the contract end or the reminder lead time changes. An empty optional field removes its value. For **flat-rate contracts** (internet, mobile, insurance, other) the cost step asks for the **payment interval** (monthly, quarterly, half-yearly, yearly) and the **amount per payment**, for an insurance for example the yearly premium. Tariffy still works with the amount per month internally (600 € a year is 50 € a month); existing contracts are monthly and stay unchanged. Changing only the interval is not a price change. When the premium rises, enter the new amount (it applies from the day you save) or renew the contract. The first field is the **name** of the contract and can be changed (empty keeps the old one); it renames the contract and its device, while sensors, entity IDs and contract data stay.

**New contract:** "New contract" (top of the Contracts tab) runs the setup dialog of Home Assistant (name, sparte and provider first, then the data of the sparte). The contract appears in the panel by itself.

**Delete a contract:** "Delete contract" is in the edit dialog and works only after you type the name of the contract; only then the button "Delete for good" becomes active. Sensors, buttons, the device and open notifications of the contract are removed; the long-term statistics Home Assistant already recorded stay in its database. Deleting the **last** contract removes the panel from the sidebar until you add a contract under Settings → Integrations → Tariffy.

**Troubleshooting:** no "Tariffy" entry → check that the installed version in HACS is 1.27.0 or newer, restart Home Assistant, hard-reload the page and check whether the entry is hidden in your profile (look for "Tariffy: panel" in the log; a panel failure never affects the contracts). Old interface or missing buttons → hard-reload the page. No buttons at all → the actions are for administrators only. Please report problems with the [bug report form](https://github.com/weskona/tariffy/issues/new/choose) and the exact version.

Screenshots: [docs/panel-preview](https://github.com/weskona/tariffy/tree/main/docs/panel-preview)

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

