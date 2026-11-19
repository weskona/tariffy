[🇩🇪 Deutsch](Fehlerbehebung) · 🇬🇧 English

# Troubleshooting

This page is sorted by symptom: what you see, what causes it and what to do. At the end it shows how to collect logs and diagnostics for a bug report. Short answers to common questions are in the [FAQ](EN-FAQ).

**Contents:**
- [The panel is empty or black](#the-panel-is-empty-or-black)
- [Consumption or costs stay empty](#consumption-or-costs-stay-empty)
- [Statistics do not reach back to the contract start](#statistics-do-not-reach-back-to-the-contract-start)
- [Wrong unit](#wrong-unit)
- [Forecasts look wrong](#forecasts-look-wrong)
- [Sensors do not appear](#sensors-do-not-appear)
- [Tariff switch did not happen](#tariff-switch-did-not-happen)
- [Reminders and warnings do not come](#reminders-and-warnings-do-not-come)
- [No notification on the phone](#no-notification-on-the-phone)
- [Backup and restore](#backup-and-restore)
- [Error messages in the form](#error-messages-in-the-form)
- [Update listener warning](#update-listener-warning)
- [Enable the debug log](#enable-the-debug-log)
- [Download diagnostics](#download-diagnostics)
- [Write a bug report](#write-a-bug-report)

## The panel is empty or black

| Symptom | Cause | Fix |
|---|---|---|
| Message "No contracts yet" | There is no contract. | Create a contract under Settings → Devices & services → Tariffy (link "Add a contract"). The panel exists from the first contract on; if the last contract was deleted, create a new one first. |
| Message "The panel could not load the contracts." | The panel did not get the contract data. | Hard-reload the page (Ctrl+F5). Then filter the Home Assistant log for `tariffy`. |
| Black or empty area | After an update an old version is still in the browser cache. | Hard-reload the page (Ctrl+F5). On version 1.31.0 or older: update to 1.32.0, which fixes the black panel and the empty panel after creating a contract. |
| No "Tariffy" entry in the sidebar | The panel could not be set up (for example a frontend or HTTP component is missing). The integration then runs on without a panel. | Search the log for `Tariffy: panel could not be set up` and restart Home Assistant. |
| No buttons in the panel | Actions exist for administrators only. | Sign in with an administrator account. |

## Consumption or costs stay empty

Costs, balance and forecast need a configured unit price. "Cost (so far)", "Refund/balance due (so far)" and "Refund/balance due (contract end)" also need a consumption sensor. The sensor must have long-term statistics, see [Measuring Consumption](EN-Measuring-Consumption).

1. Check under Developer tools → States that the consumption sensor exists and has a value.
2. Check in the attributes of the sensor that `state_class` is set (`total_increasing` or `total`).
3. If the consumption stays empty, the log contains a warning like `Tariffy '<contract>': Verbrauch bisher ist unbekannt (Sensor ...)` with details. The log only reports the change to "unknown" and later "known again".
4. Download the [diagnostics](#download-diagnostics): the block `verbrauch` shows what Tariffy found while calculating, `zaehler` the current state of your sensor (`state` is `fehlt` if the entity does not exist).

## Statistics do not reach back to the contract start

If the sensor was renamed or recreated, enter a manual **"Meter reading at contract start (optional)"** in the contract data. It has priority over the automatic methods.

## Wrong unit

The sensors "Consumption (so far)" and "Consumption (contract term projected)" show the raw meter difference in the unit of your sensor (usually m³). Only for the cost calculation is it converted internally to kWh via calorific value × state number. If a sensor still shows an unexpected unit, it comes from the consumption sensor: the diagnostics show it in the block `zaehler` under `unit`.

## Forecasts look wrong

- **The value is very high or very low:** Check the meter reading at contract start and the unit of the sensor (see above). A wrong start value distorts consumption, costs and forecast.
- **The sign is confusing:** Refund/balance due is positive for a refund and negative for a balance due.
- **The instalment changed:** Enter under **Instalments paid** what was paid from when, see [Payment History and One-off Items](EN-Payment-History-and-One-off-Items).
- **PV system:** Without [PV Self-Sufficiency](EN-PV-Self-Sufficiency) the forecast overestimates the rest of the term in winter and underestimates it in summer.

## Sensors do not appear

Sensors for night rate, tiered pricing and dual-tariff meter (HT/NT) exist only if the respective category or option is used. Loan and leasing have sensors of their own, other categories do not get them. The list is in the [Sensor Reference](EN-Sensor-Reference).

## Tariff switch did not happen

The switch is checked every day at 00:00:01, every 6 hours and after Home Assistant starts. The button **Switch now** triggers it at once. The panel has no button for it: there the contract switches by itself on the planned date. More on [Contract End and Switching](EN-Contract-End-and-Switching).

## Reminders and warnings do not come

- **Cancellation reminder:** It needs a contract end and a reminder period that has been reached. With a notice period entered, the reminder refers to the last day for cancellation, not to the contract end. The message appears as a persistent notification in the notification centre until you acknowledge it with the button **Confirm cancellation**.
- **Low-instalment warning:** It is off by default. Switch on "Warn if instalment is too low" in the contract form. It applies to electricity, gas and water with a consumption sensor and fires when the forecast at contract end expects a balance due above the threshold (default 50 €). You acknowledge it with **Confirm low-instalment warning**; if the forecast worsens again later, it reports again.
- **Archived contracts:** Their reminders and warnings are off (see [Archive and History](EN-Archive-and-History)).
- **Deleted contracts:** Their open notifications are removed on deletion.

## No notification on the phone

The push notification goes to the service you entered in the field "Notification target (notify service)", for example `notify.mobile_app`. If it is not reachable, Tariffy writes `notify.<service> nicht erreichbar (...)` to the log. Check the name under Developer tools → Actions. The persistent notification in the notification centre appears regardless.

## Backup and restore

| Symptom | Cause | Fix |
|---|---|---|
| "This file is not a valid Tariffy backup." | The file is not a Tariffy backup or was modified. Tariffy checks strictly: only known settings, only simple values, at most 1 MB and 200 contracts. | Use the unchanged file from **Download backup**. |
| "The file is too large." | The file exceeds the limit. | Use the original file, add nothing by hand. |
| "A contract with this name and kind exists already." | When restoring, a contract with the same name and category exists. | Rename or delete the existing contract and restore again. |
| "This backup does not exist any more." | The entry of the deleted contract is older than 30 days or was removed with **Forget now**. | Restore from a backup file or a Home Assistant backup. |
| "Restoring failed." | Something went wrong while creating. | Filter the log for `tariffy` and write a [bug report](#write-a-bug-report). |
| Contracts were skipped while restoring | Contracts with the same name and category are never changed. | This is intended. |

More about the functions on [Panel: Backup](EN-Panel-Backup) and [Backup and Migration](EN-Backup-and-Migration).

## Error messages in the form

These messages come from the form when you create or edit a contract:

| Message | Meaning and fix |
|---|---|
| "Not a valid number. Use a dot or comma as the decimal separator (e.g. 11.2 or 11,2)." | A number field contains text or another format. Enter only digits and a dot or comma. |
| "Enter a loan amount above zero." | The loan has no amount or it is 0. |
| "Enter the nominal or the effective interest rate." | Both interest fields of the loan are empty. |
| "Enter one value or twelve values between 0 and 100, separated by spaces or semicolons." | Own PV self-sufficiency values are not one value or twelve values between 0 and 100, for example `10 10 25 50 70 80 85 80 60 35 15 10`. |
| "Without a sensor, all values being equal changes nothing in the forecast: enter twelve different monthly values (January to December) or a sensor." | A single value does not change the forecast. Enter twelve different monthly values or choose a sensor, see [PV Self-Sufficiency](EN-PV-Self-Sufficiency). |
| "The backup is not valid." | While restoring, Tariffy rejected a contract from the backup (abort with `invalid_backup`). The file is damaged or modified, see the table in the section Backup and restore. |

## Update listener warning

The Home Assistant warning "update listener … should use it for scheduling a reload" is fixed in Tariffy 1.26.3 ([issue 2](https://github.com/weskona/tariffy/issues/2)). Update Tariffy.

## Enable the debug log

The logger of the integration is called `custom_components.tariffy`. Add this to `configuration.yaml`:

```yaml
logger:
  logs:
    custom_components.tariffy: debug
```

Restart Home Assistant, reproduce the problem and open Settings → System → Logs. Filter for `tariffy` and copy the matching lines. Remove the entry afterwards so the log does not grow needlessly.

## Download diagnostics

Home Assistant offers a diagnostics download for every contract (Settings → Devices & services → Tariffy → on the contract, in the ⋮ menu the entry for downloading diagnostics). The file contains:

- `entry`: title, contract data and options
- `update`: whether the last calculation succeeded, the last exception and the interval
- `verbrauch`: what Tariffy found while determining the consumption
- `zaehler` and `zaehler_nt`: state, unit and `state_class` of the consumption sensor (and of the low-tariff sensor)
- `daten`: the calculated values of the contract

**Redacted** are number plate, customer number, market location, notification target and meter number(s). Not redacted are, among others, contract name, provider, tariff, prices and the entity IDs. Look through the file anyway before you attach it publicly.

## Write a bug report

Open an [issue with the form "Bug Report"](https://github.com/weskona/tariffy/issues/new/choose). Required are the Tariffy version (HACS → Tariffy, or `custom_components/tariffy/manifest.json`), the Home Assistant version, the installation method (HACS or manual), what is affected, the category and a description of the problem with the steps to reproduce it. For consumption and cost problems these help in addition:

1. the entity ID of the consumption sensor (for a dual-tariff meter also of the low-tariff sensor) and its `state_class`
2. the contract start date
3. log lines with `tariffy` (best with the [debug log](#enable-the-debug-log))
4. the [diagnostics](#download-diagnostics)

For beta versions give the exact version, for example `1.33.0-beta.1`. The form requires that you use the latest version, searched the existing issues and replaced personal data (customer number, meter number, market location ID, tokens) with `xxx`. Questions about usage belong in the [Discussions](https://github.com/weskona/tariffy/discussions), ideas in the form "Feature Request".

> **Good to know:** The title of the issue should start with a few words instead of `<short summary>`, for example "Consumption (so far) too high".

## See also

- [FAQ](EN-FAQ)
- [Measuring Consumption](EN-Measuring-Consumption)
- [Panel: Backup](EN-Panel-Backup)
- [Releases and Beta](EN-Releases-and-Beta)
- [Development](EN-Development)
