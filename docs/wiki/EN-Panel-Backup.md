[🇩🇪 Deutsch](Panel-Sicherung) · 🇬🇧 English

# Panel: Backup

The **Backup** tab is only visible to administrators. It has three areas: download a backup just for Tariffy, restore from a backup file and **bring back contracts deleted in the last 30 days**.

**Contents:**
- [The three areas](#the-three-areas)
- [Download a backup](#download-a-backup)
- [Restore from a file](#restore-from-a-file)
- [Deleted contracts](#deleted-contracts)
- [Example: bring back Strom 2023](#example-bring-back-strom-2023)
- [Limits](#limits)
- [On a phone](#on-a-phone)
- [See also](#see-also)

## The three areas

The normal Home Assistant backups include Tariffy completely. The tab adds a backup just for Tariffy (more in [Backup and migration](EN-Backup-and-Migration)).

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/english-backup.png"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/english-backup-light.png" alt="Backup tab with the areas Create a backup with the button Download backup, Restore from a file with the file chooser and Deleted contracts with the entry Strom 2023 and the buttons Restore and Forget now" width="100%"></picture></p>

*Figure: The Backup tab (mock data of 12 July 2026). The "Choose File" field comes from the browser and is labelled in the browser's language.*

| Area | Button | Purpose |
|---|---|---|
| **Create a backup** | **Download backup** | Saves all contracts in one file. |
| **Restore from a file** | File chooser, then **Restore (n)** | Creates missing contracts from a backup file. |
| **Deleted contracts** | **Restore**, **Forget now** | Brings a deleted contract back or forgets it at once. |

## Download a backup

The button **Download backup** saves all contracts in one file `tariffy-backup-<date>.json`: contract data, history, archived contracts, planned next contract and the internal state (for example acknowledged reminders). Afterwards the panel says "Backup downloaded: n contracts."

> **Good to know:** **The file contains personal data** (customer number, meter number, market location ID, notification target). Keep it safe and do not pass it on.

## Restore from a file

1. You choose the backup file.
2. The panel shows what would happen: contracts that do not exist yet are **created** ("will be created"), contracts with the same name and kind are **skipped** ("skipped: exists already") and never changed. If there is nothing to create, it says "Nothing to restore: the contracts of this file exist already."
3. With **Restore (n)** and a confirmation ("Create n missing contract(s) from this file? Existing contracts are not changed." with **Yes, restore**) the missing contracts are created. Afterwards it says "Restored: n created, m skipped."

- The file is checked strictly (known settings only, simple values only, at most 1 MB and 200 contracts); a broken file creates nothing. The panel then says "This file is not a valid Tariffy backup." or, for a file that is too large, "The file is too large."
- Restored contracts are **new contracts with new sensors**; the statistics of the old contract stay with its sensors in Home Assistant.

## Deleted contracts

When a contract is deleted (in the panel or in Home Assistant), Tariffy keeps it for **30 days** (at most the last 20) and offers it here. Each entry shows name, category and the deletion date ("Electricity · deleted 01/07/2026").

- **Restore** creates the contract again, after a confirmation (Bring back "Strom 2023"?, **Yes, bring back**). That is not possible if a contract with the same name and kind exists meanwhile ("A contract with this name and kind exists already.").
- **Forget now** removes an entry at once, including its personal data, after a confirmation ("Forget ... for good? It can not be brought back afterwards.", **Yes, forget**).
- The data are in Home Assistant's storage (`.storage/tariffy.deleted`) and removed after 30 days.
- If there is nothing to bring back, it says "No deleted contracts."

## Example: bring back Strom 2023

In the mock data the contract **Strom 2023** (category electricity) was deleted on 01.07.2026. Today is 12.07.2026, so it is eleven days old and can still be brought back.

1. Open the tab **Backup**, area **Deleted contracts**.
2. Click **Restore** next to "Strom 2023".
3. Answer the confirmation with **Yes, bring back**.
4. At the top of the page the message `"Strom 2023" is back.` appears in green, and the contract is in the overview again.

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/desktop-backup-actions.png" alt="Backup tab after bringing a contract back: at the top in green the message Strom 2023 ist wieder da, below it the three areas unchanged" width="100%"></p>

*Figure: The green message at the top confirms that the contract is back (German labels in this screenshot).*

Had the contract been deleted for more than 30 days, the entry would be gone already.

## Limits

- **The panel only exists while there is at least one contract.** If the last contract was deleted, add any new contract first (Settings → Devices & services → Tariffy → Add), then the panel is back and you can bring the deleted contract back in the Backup tab.
- Non-administrators do not see the tab, and the backend rejects the actions through the API as well ([Panel permissions and design](EN-Panel-Permissions-and-Design)).
- The backup file does not replace a Home Assistant backup: it contains the contracts, but not the long-term statistics.

## On a phone

On a phone the three areas stand one below the other.

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-backup.png"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-backup-light.png" alt="Backup tab on a phone: the three areas one below the other" width="300"></picture></p>

*Figure: The Backup tab on a phone (German labels in this screenshot).*

## See also

- [Backup and migration](EN-Backup-and-Migration): backup, moving to another installation, restoring in context.
- [Panel contracts](EN-Panel-Contracts): delete a contract.
- [Panel history](EN-Panel-History): bring archived contracts back.
- [Panel permissions and design](EN-Panel-Permissions-and-Design): who sees the tab.
