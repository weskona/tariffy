[🇩🇪 Deutsch](Sicherung-und-Umzug) · 🇬🇧 English

# Backup and migration

This page shows how to save your contracts to a file, restore them from it, take them along to a new Home Assistant installation, and bring back a contract you deleted by mistake. It is for everyone who does not want to lose their contract data. Everything here is for administrators only.

**Contents:**

- [Which backups exist](#which-backups-exist)
- [Creating a backup](#creating-a-backup)
- [Restoring from a backup](#restoring-from-a-backup)
- [What is in the backup and what is not](#what-is-in-the-backup-and-what-is-not)
- [Moving to a new Home Assistant instance](#moving-to-a-new-home-assistant-instance)
- [Deleted contracts: 30 days to change your mind](#deleted-contracts-30-days-to-change-your-mind)
- [Example with numbers](#example-with-numbers)

## Which backups exist

- **The normal Home Assistant backup** includes Tariffy: the contracts are in Home Assistant's storage. This is the way if you restore Home Assistant as a whole.
- **The Tariffy backup** in the **Backup** tab of the panel is a single file with only your contracts. It helps if you need only the contracts, if you move to a fresh installation, or if you want a copy before a bigger change.
- **Deleted contracts** are remembered by Tariffy for 30 days by itself, without you doing anything.

<table align="center"><tr><td align="center" width="50%"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/english-backup.png" alt="The Backup tab with the three blocks Create a backup, Restore from a file and Deleted contracts, in the last one a contract Strom 2023 with the buttons Restore and Forget now (dark design)" width="100%"><br><sub>Dark</sub></td><td align="center" width="50%"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/english-backup-light.png" alt="The Backup tab with the three blocks Create a backup, Restore from a file and Deleted contracts, in the last one a contract Strom 2023 with the buttons Restore and Forget now (light design)" width="100%"><br><sub>Light</sub></td></tr></table>

*Figure: The "Backup" tab with mock data dated 12 Jul 2026. More about the tab is on [Panel-Backup](EN-Panel-Backup).*

## Creating a backup

1. In the panel open the **Backup** tab.
2. Under **Create a backup** click **Download backup**.
3. Your browser saves the file `tariffy-backup-<date>.json`. Tariffy reports "Backup downloaded: n contracts."

> **Important:** The file contains **personal data** (customer number, meter number, market location, notification target). Keep it safe and do not pass it on.

## Restoring from a backup

1. Open the **Backup** tab and choose your file under **Restore from a file**.
2. Tariffy first shows what would happen: contracts that do not exist yet say "will be created", contracts that exist already say "skipped: exists already". Nothing has been created up to here.
3. Click **Restore (n)** and confirm with **Yes, restore**.
4. Tariffy reports "Restored: x created, y skipped."

The rules behind it:

- **Only missing contracts are created.** "Existing" means the same **name** and the same **kind**. Existing contracts are **never changed**, not even if the values differ.
- If the same contract appears twice in the file, it is created once.
- The file is checked strictly: known settings only, simple values only, at most 200 contracts, every text at most 2000 characters. The panel accepts files up to 1 MB ("The file is too large." above that). If the file is broken ("This file is not a valid Tariffy backup."), **nothing** is created, not even the valid contracts before the broken one.
- A restored contract is a **new contract** with new sensors and buttons, but with the same data as before.

## What is in the backup and what is not

**In the backup** is everything that belongs to the contract:

- the contract name and all settings from the contract form, including customer number, meter number, market location and notification target,
- the history, a possible archive marker, one-off items, the payment history and the outdoor meters,
- the planned next contract,
- the internal state, for example acknowledged reminders and the frozen consumption of the last term.

**Not in the backup** is everything that does not belong to Tariffy:

- the long-term statistics of your meters and the meter sensors themselves (the contract only refers to their entity ID),
- the contract's sensors and buttons and their own statistics; they are created anew when restoring,
- dashboard cards and automations that use your contract entities,
- notify services the notification target points to,
- the list of deleted contracts (see below).

## Moving to a new Home Assistant instance

1. **Old instance:** download the backup in the **Backup** tab.
2. **New instance:** install Tariffy (see [Getting-Started](EN-Getting-Started)) and restart Home Assistant.
3. On the new instance first set up your **meter sensors**, with **the same entity IDs** as before (for example `sensor.meter_electricity`). The backup holds only the ID the contract uses. You also need the notify service for the notification target there again.
4. Create **any contract**, for example a placeholder with a different name. The panel only exists once at least one contract exists; without the panel there is no **Backup** tab.
5. In the panel open the **Backup** tab, choose the file, check the preview and click **Restore (n)**.
6. Check the contracts in the panel and the new sensors. Change dashboard cards and automations to the new entity IDs.
7. Delete the placeholder contract. It stays in the list of deleted contracts for 30 days; with **Forget now** you remove it at once.

> **Good to know:** Because your meters' statistics are not in the backup, on the new instance Tariffy depends on the long-term statistics there. If they do not reach back to the contract start, enter a value in the field **Meter reading at contract start (optional)** of the contract; it takes precedence over the automatic methods (see [Measuring-Consumption](EN-Measuring-Consumption)).

> **Good to know:** If a sensor on the new instance already has the same name as a new one, Home Assistant appends `_2` to the ID. Check the IDs under **Settings → Devices & services → Entities** before you adapt automations (see [Automations](EN-Automations)).

## Deleted contracts: 30 days to change your mind

If you delete a contract, in the panel or in Home Assistant, Tariffy keeps a copy for **30 days**, at most the **last 20**. You find them in the **Backup** tab under **Deleted contracts** with "deleted <date>".

![The dialog for deleting a contract for good: to confirm, the name Strom Haus has to be typed, below it the buttons Endgültig löschen and Abbrechen](https://raw.githubusercontent.com/wiki/weskona/tariffy/images/delete-contract-dialog.png)

*Figure: The delete dialog with mock data (German interface): the contract name has to be typed to confirm.*

- **Restore** (with the question "Bring back "<name>"?") creates the contract again, with new sensors. That is not possible if a contract with the same name and kind exists in the meantime ("A contract with this name and kind exists already.").
- **Forget now** (with a question) removes the entry at once and for good, including personal data.
- After 30 days an entry disappears by itself. The copy is in Home Assistant's storage (`.storage/tariffy.deleted`).
- Deleting never fails because of the copy: if it cannot be made, the contract is deleted anyway.

> **Good to know:** The long-term statistics Home Assistant already recorded stay in the database when deleting, the contract's sensors and buttons are removed. If you only want to put a contract aside without deleting it, better use the archive (see [Archive-and-History](EN-Archive-and-History)).

## Example with numbers

Example (based on the integration's tests): you have the contracts "Strom Haus" (instalment 40 €) and "Wasser" and download the backup. Afterwards you delete "Wasser" and change the instalment of "Strom Haus" to 99 €.

1. You choose the file. The preview shows: "Strom Haus", skipped (exists already); "Wasser", will be created.
2. After **Restore (1)** Tariffy reports: "Restored: 1 created, 1 skipped."
3. "Wasser" is back with its old data, with new sensors. "Strom Haus" still has the instalment 99 €, the backup did not overwrite it.
4. A second restore with the same file creates nothing more: 0 created, 2 skipped.

## See also

- [Panel-Backup](EN-Panel-Backup): the Backup tab in the panel
- [Archive-and-History](EN-Archive-and-History): archive contracts instead of deleting them
- [Creating-Contracts](EN-Creating-Contracts): create a contract from scratch
- [Measuring-Consumption](EN-Measuring-Consumption): meters, statistics and the meter reading at contract start
- [Getting-Started](EN-Getting-Started): install Tariffy and create the first contract
- [Troubleshooting](EN-Troubleshooting): when something does not work
