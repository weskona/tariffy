[🇩🇪 Deutsch](FAQ) · 🇬🇧 English

# FAQ

Answers to the questions that come up most often. If you have a problem, look here first and then in [Troubleshooting](EN-Troubleshooting).

**Contents:**
- [The panel is empty or black](#the-panel-is-empty-or-black)
- [Do I have to reload the page after an update?](#do-i-have-to-reload-the-page-after-an-update)
- [Why are consumption or costs missing?](#why-are-consumption-or-costs-missing)
- [Why is the consumption not in kWh?](#why-is-the-consumption-not-in-kwh)
- [Next contract or renew?](#next-contract-or-renew)
- [Where does Tariffy store my data?](#where-does-tariffy-store-my-data)
- [Who can see personal data?](#who-can-see-personal-data)
- [What happens when I delete a contract?](#what-happens-when-i-delete-a-contract)
- [Can I create several contracts?](#can-i-create-several-contracts)
- [How often does Tariffy recalculate?](#how-often-does-tariffy-recalculate)
- [Why is a sensor missing?](#why-is-a-sensor-missing)
- [Can I test beta versions?](#can-i-test-beta-versions)

## The panel is empty or black

There are three cases:

- **The message "No contracts yet":** The panel shows it when there is no contract. Create one under Settings → Devices & services → Tariffy (link "Add a contract"). The panel is only available once at least one contract exists.
- **The message "The panel could not load the contracts.":** Hard-reload the browser page (Ctrl+F5). If the error stays, see [Troubleshooting](EN-Troubleshooting#the-panel-is-empty-or-black).
- **A black area without a message:** This was a bug up to version 1.31.0 and is fixed in 1.32.0 (the panel stayed black until another dashboard was opened and back). Update and hard-reload the page. A panel that stayed empty after a contract was created or changed is fixed in 1.32.0 as well.

## Do I have to reload the page after an update?

Yes, once. The panel consists of several files that the browser caches for a long time. After an update, hard-reload the page once (Ctrl+F5, on a Mac Cmd+Shift+R) and the new version runs.

## Why are consumption or costs missing?

Costs, balance and forecast need a configured **unit price**. "Cost (so far)", "Refund/balance due (so far)" and "Refund/balance due (contract end)" also need a **consumption sensor** with long-term statistics. How to set up the sensor is described in [Measuring Consumption](EN-Measuring-Consumption). The troubleshooting steps are in [Troubleshooting](EN-Troubleshooting#consumption-or-costs-stay-empty).

## Why is the consumption not in kWh?

The sensors "Consumption (so far)" and "Consumption (contract term projected)" show the raw meter difference in the unit of your sensor, for gas and water usually m³. Only for the cost calculation does Tariffy convert gas internally to kWh via calorific value × state number. So this is intended, not a bug.

Example (numbers for illustration only): 120 m³ of gas with a calorific value of 10.0 kWh/m³ and a state number of 0.95 give 120 × 10.0 × 0.95 = 1,140 kWh. The consumption sensors still show 120 m³, the costs are calculated with 1,140 kWh.

## Next contract or renew?

- **Plan next contract** when a different tariff or a different provider takes over on a key date. Tariffy switches by itself on the switch date.
- **Renew contract** when the same contract keeps running with a new start, end and amount, for example after a premium adjustment. It exists for contracts without consumption (insurance, internet, mobile, streaming, other) and for the loan as follow-up financing.

The difference in all details is on [Next Contract or Renew](EN-Next-Contract-or-Renew).

## Where does Tariffy store my data?

Everything stays in your Home Assistant:

- The **contract data** is stored in the settings of the contract in Home Assistant (every contract is its own entry of the integration).
- The **consumption** comes from the long-term statistics of your sensor; Tariffy only reads them.
- **Deleted contracts** are kept for 30 days in the storage of Home Assistant under `.storage/tariffy.deleted` (the last 20 at most).
- The **backup file** from the **Backup** tab lies wherever you save it. It contains personal data, so treat it accordingly.
- The integration brings no additional Python packages (`requirements` in `manifest.json` is empty) and is classified as `calculated`, so it only calculates with values from Home Assistant.

The normal backups of Home Assistant include Tariffy. More on [Backup and Migration](EN-Backup-and-Migration).

## Who can see personal data?

Tariffy sends the **customer number, meter number(s) and market location ID** to administrators only. They stand in the **Contract** block of the contract details (tab **Contracts**); the browsers of other users never receive them. The **number plate** and the **notification target** are not shown by the panel even to administrators. For every action that changes something, the backend checks the rights again, so a non-administrator cannot trigger them through the API either. The details are on [Panel: Permissions and Design](EN-Panel-Permissions-and-Design).

Two places contain the personal data nevertheless: the **backup file** and the **entry of a deleted contract** (30 days). With **Forget now** in the **Backup** tab, a deleted contract disappears with its data at once. The **diagnostics download** redacts customer number, meter number(s), market location, number plate and notification target (see [Troubleshooting](EN-Troubleshooting#download-diagnostics)).

## What happens when I delete a contract?

- Open notifications of the contract (cancellation reminder and low-instalment warning) are removed.
- The contract and its sensors are gone. But Tariffy remembers the contract for **30 days** and offers it for **Restore** in the **Backup** tab. This does not work if a contract with the same name and category exists in the meantime.
- A restored contract is a new contract with new sensors. The statistics of the old contract stay with its sensors in Home Assistant.

If you only want the contract out of the overview, **archive** it instead: nothing is deleted then. See [Archive and History](EN-Archive-and-History).

## Can I create several contracts?

Yes. Every contract is created as its own entry with its own device and its own sensors; the integration has no upper limit for contracts, not even for several contracts of the same category. You add more under Settings → Devices & services → Tariffy or in the panel with **New contract** (administrators only). More on [Creating Contracts](EN-Creating-Contracts).

## How often does Tariffy recalculate?

Every 6 hours and after the start of Home Assistant, as soon as the long-term statistics are ready. A planned tariff switch is checked additionally every day at 00:00:01. The button **Switch now** triggers it at once. Everything else is on [Contract End and Switching](EN-Contract-End-and-Switching).

## Why is a sensor missing?

Sensors for night rate, tiered pricing, dual-tariff meter (HT/NT), leasing and loan exist only if the category or the option is used. The list is in the [Sensor Reference](EN-Sensor-Reference).

## Can I test beta versions?

Yes, through HACS, without anyone else noticing. The steps are on [Releases and Beta](EN-Releases-and-Beta).

> **Good to know:** Not every question is here. If you do not find yours, [open an issue](https://github.com/weskona/tariffy/issues/new/choose) or ask in the [Discussions](https://github.com/weskona/tariffy/discussions).

## See also

- [Troubleshooting](EN-Troubleshooting)
- [Getting Started](EN-Getting-Started)
- [Sensor Reference](EN-Sensor-Reference)
- [Releases and Beta](EN-Releases-and-Beta)
