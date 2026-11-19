[🇩🇪 Deutsch](Panel-Rechte-und-Design) · 🇬🇧 English

# Panel: Permissions and design

This page explains **who sees and may do what in the Tariffy panel** (administrators and other users), how the **light and dark theme** and the **phone view** work, what you see when there are **no contracts** or **loading fails**, and what the panel deliberately does **not** do.

**Contents:**
- [Administrators and other users](#administrators-and-other-users)
- [Personal data](#personal-data)
- [Light and dark theme](#light-and-dark-theme)
- [Phone view](#phone-view)
- [Empty state and error state](#empty-state-and-error-state)
- [Example: the same contract with two users](#example-the-same-contract-with-two-users)
- [What the panel does not do](#what-the-panel-does-not-do)
- [Troubleshooting](#troubleshooting)
- [See also](#see-also)

## Administrators and other users

**All users** of Home Assistant see the panel, but not everyone may do everything. What matters is whether the user account is an administrator in Home Assistant.

| | All users | Administrators only |
|---|---|---|
| View the tabs **Overview**, **Costs**, **Contracts**, **History** | yes | yes |
| Tab **Backup** | not visible | yes ([Panel backup](EN-Panel-Backup)) |
| Contract details with selected values | yes | yes |
| Customer number, meter number(s), MaLo ID with copy symbol | no | yes |
| Icons in the contract list (pencil, calendar, renew) and **"New contract"** | no | yes |
| **"Acknowledge warning"**, **"Acknowledge cancellation"**, Archive, Restore | no | yes |
| **Add an old contract**, edit terms | no | yes |
| Change one-off items, instalments paid and outdoor meters | no | yes |
| Edit, delete, renew a contract, plan the next contract | no | yes |

The check exists twice: the panel hides the buttons and dialogs for other users, and the **backend checks it again**. A non-administrator cannot trigger the actions through the API either. For other users the block **One-time items** (and similarly the blocks Instalments paid and Outdoor meters) is only visible if there are entries.

> **Good to know:** If you see no buttons, you are probably not signed in as an administrator. That is intended and not an error.

## Personal data

Personal details are only sent to administrators:

- **All users** do **not** get: customer number, meter numbers, MaLo ID, licence plate, notification target and internal markers. They are not even sent to the panel; other browsers never receive them.
- **Administrators** also see the **customer number, meter number(s) and MaLo ID** in the block **Contract** of the contract details (tab **Contracts**), each with a symbol to **copy** it ("Copied" confirms it). The **licence plate** and the **notification target** stay hidden for them too.
- The **backup file** contains personal data, see [Panel backup](EN-Panel-Backup).

## Light and dark theme

The panel follows the **theme of Home Assistant**: if Home Assistant is in **light** mode (by profile, automatic switching or system setting), Tariffy shows light colours, otherwise dark ones. If Home Assistant reports no mode, the system setting of the browser decides. There is no setting of its own in Tariffy. A change in Home Assistant applies at once, without reloading the page. The colours for credit, balance due and warnings are darker in light mode so they stay readable.

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/english-costs.png" alt="Costs tab in the dark theme: dark background, light text, red and green amounts" width="100%"></p>

*Figure: The Costs tab in the dark theme.*

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/english-costs-light.png" alt="Costs tab in the light theme: light background, dark text, darkened red and green amounts" width="100%"></p>

*Figure: The same tab in the light theme. The amounts for credit and balance due are tinted darker.*

## Phone view

The panel adapts to the width, not to the device: when it is up to about 760 pixels wide (phone, narrow window), the tiles stand one below the other and the contract cards become **expandable rows**, and the tables become cards with one row per column. On a phone the menu button appears at the top left when Home Assistant is narrow. On a wide screen more cards stand side by side.

<table align="center"><tr><td align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-overview.png" alt="Overview on a phone: tiles one below the other and contracts as collapsed rows (dark design)" width="300"><br><sub>Dark</sub></td><td align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-overview-light.png" alt="Overview on a phone: tiles one below the other and contracts as collapsed rows (light design)" width="300"><br><sub>Light</sub></td></tr></table>

*Figure: The overview in the narrow view (German labels in this screenshot).*

You can see the individual tabs in the phone view on the pages [Panel overview](EN-Panel-Overview), [Panel costs](EN-Panel-Costs), [Panel contracts](EN-Panel-Contracts), [Panel history](EN-Panel-History) and [Panel backup](EN-Panel-Backup).

## Empty state and error state

While the panel loads it says "Loading contracts ...". Two states show that something is missing:

- **No contracts yet:** there is no contract. The panel shows "No contracts yet", the text "Add a contract under Settings → Devices & services → Tariffy." and the link **Add a contract**.
- **Error while loading:** the panel shows "The panel could not load the contracts." and below it the technical message from Home Assistant.

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/state-empty.png" alt="Panel without contracts: tab bar, below it the heading Noch keine Verträge, the text about adding a contract and the link Vertrag anlegen" width="100%"></p>

*Figure: The empty state (German labels in this screenshot).*

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/state-error.png" alt="Panel in the error state: the heading Das Panel konnte die Verträge nicht laden and below it the message Unknown command" width="100%"></p>

*Figure: The error state (German labels in this screenshot). Below the heading the screenshot shows "Unknown command." (a sample text from the test environment); in your Home Assistant the message from Home Assistant stands there.*

What you can do is in the section [Troubleshooting](#troubleshooting).

## Example: the same contract with two users

The contract **Strom Haus** shows the same to everybody in the overview: −495 € forecast, badge **Balance due likely**. In the tab **Contracts** the accounts differ:

| What | Administrator | Other user |
|---|---|---|
| Row Strom Haus | calendar and pencil icons in front of the arrow | only the arrow |
| Expanded, block **Contract** | also customer number and meter number with copy symbol | only provider, tariff, start, end, remaining term, reminder from |
| Block **One-time items** | items, pencils and **Add item** | only the items (switching bonus +80.00 €, broker's fee −25.00 €) |
| Under **Recommendations** | **"Acknowledge warning"** | only the note "Raise the instalment to 127.66 € per month" |
| Tabs | Overview, Costs, Contracts, History, **Backup** | Overview, Costs, Contracts, History |

## What the panel does not do

- It calculates nothing itself but shows the values of the integration. All values are the same as those of the sensors ([Sensor reference](EN-Sensor-Reference)).
- It writes only through the dialogs of Home Assistant. These stay available unchanged under Settings → Devices & services → Tariffy; the sensors and buttons of the integration stay as they are.
- There is no "switch now" function: the switch to the next contract happens by itself on the planned date ([Panel contracts](EN-Panel-Contracts)).
- It archives and deletes nothing by itself.
- It does not send customer number, meter numbers, MaLo ID, licence plate and notification target to non-administrators.
- It has no theme setting of its own: light or dark comes from Home Assistant.
- The panel exists only while there is at least one contract.

## Troubleshooting

| Problem | Solution |
|---|---|
| No "Tariffy" entry in the sidebar | Check the version in HACS (the panel exists from 1.27.0), restart Home Assistant, hard-reload the page (Ctrl+F5). Check in your profile whether the entry is hidden. Look in the log for "Tariffy: panel": the panel can fail without disturbing the contracts. |
| Panel black or empty | Hard-reload the page (Ctrl+F5; on a phone: reload the page or clear the app cache). If that does not help: restart Home Assistant and look in the log for "Tariffy: panel". |
| The panel shows the old interface or buttons are missing | Hard-reload the page, the browser cached the old file. |
| No buttons visible | The actions exist for administrators only. |
| "The form could not be loaded" | Home Assistant was briefly unreachable or the contract is not loaded right now. Close the dialog and open it again. |
| "The panel could not load the contracts." | Reload the page; if it stays, look in the log for "Tariffy: panel" and report a bug. |
| Report a problem | With the [bug report form](https://github.com/weskona/tariffy/issues/new/choose) and the exact version. |

More help in [Troubleshooting](EN-Troubleshooting) and [FAQ](EN-FAQ).

## See also

- [Panel overview](EN-Panel-Overview): the start into the panel.
- [Panel contracts](EN-Panel-Contracts): all actions for administrators.
- [Panel backup](EN-Panel-Backup): the tab for administrators only.
- [Troubleshooting](EN-Troubleshooting): general help.
