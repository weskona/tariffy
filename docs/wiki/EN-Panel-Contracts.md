[🇩🇪 Deutsch](Panel-Vertraege) · 🇬🇧 English

# Panel: Contracts

The **Contracts** tab is the workspace of the panel: here you expand the details of every contract, and here are **all actions that change a contract**: create, edit, plan the next contract, renew, archive, delete. All users may look at the tab, only administrators may change things.

**Contents:**
- [The contract list](#the-contract-list)
- [The contract details](#the-contract-details)
- [Buttons](#buttons)
- [Acknowledge: warning and cancellation](#acknowledge-warning-and-cancellation)
- [New contract](#new-contract)
- [Edit a contract](#edit-a-contract)
- [Plan the next contract](#plan-the-next-contract)
- [Renew a flat-rate contract](#renew-a-flat-rate-contract)
- [Instalments paid](#instalments-paid)
- [One-off items](#one-off-items)
- [Archive](#archive)
- [Delete a contract](#delete-a-contract)
- [Example: add a one-off item](#example-add-a-one-off-item)
- [On a phone](#on-a-phone)
- [Errors and notes](#errors-and-notes)
- [See also](#see-also)

## The contract list

The contracts stand in the same groups as in the overview: **Metered contracts**, **Flat-rate contracts** and **Loans / financing**. Each row shows the icon, name, provider and tariff, the badge (for example **Balance due likely**, **Credit**, **Cancel now**, **Switch on 01.01.2027**) and, on the right, the balance at contract end (metered) or the amount "39.99 € / month" (flat rate). A click on the row expands the details (arrow at the far right).

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/list-1280.png" alt="Contracts tab on a 1280 pixel wide screen: the button New contract at the top right, below it the contracts as collapsed rows with badge, balance and icons" width="100%"></p>

*Figure: The Contracts tab with collapsed rows (mock data of 12 July 2026; the labels are German in this screenshot).*

As an **administrator** you see icons in front of the arrow in every row, from right to left:

| Icon | Name | Where |
|---|---|---|
| Pencil | Edit contract | every contract |
| Calendar | Plan next contract (or Edit next contract if one is already entered) | every contract except loans |
| Two arrows in a circle | Renew contract (for loans: follow-up financing) | flat-rate contracts and loans that can be renewed |

At the top right is the button **New contract**. Other users see the list without icons and without this button.

## The contract details

Expanded, a metered contract shows several blocks side by side (stacked on narrow screens):

| Block | Content |
|---|---|
| **Contract** | Provider, tariff, start, end, remaining term, reminder from; if set, minimum term, notice period and "Cancel by". **Only administrators** also see the customer number, meter number(s) and MaLo ID here, each with a symbol to copy it. |
| **Prices** | Unit price, base price, instalment per month and per year, for contracts with a history **Total cost** ("since 01.01.2024 · 3 terms"). |
| **One-time items** | Credits and bills, see [One-off items](#one-off-items). Visible to other users only if there are items. |
| **Consumption** | So far, projected for the term, cost so far, credit / balance due so far and at contract end. With a total-consumption sensor the grid **Total consumption**, **Covered by PV** and **Grid draw (billed)** is added, with PV self-sufficiency the forecast without self-sufficiency ([PV self-sufficiency](EN-PV-Self-Sufficiency)). |
| **Recommendations** | The **Instalment adjustment** (recommended instalment) and, depending on the situation, the buttons to acknowledge. |
| **Next contract** | Appears when a next contract is entered: start, end, provider, tariff, price, instalment. |
| **Instalments paid** | The history of the amounts really paid, see [Instalments paid](#instalments-paid). Loans do not have it. |

For flat-rate contracts the blocks are similar, without consumption; for streaming the instalment is called "Price / month". Further blocks exist only for certain categories: **Outdoor meters** for water ([Water contract](EN-Contract-Water)), **Leasing kilometres** for leasing ([Leasing contract](EN-Contract-Leasing)) and **Loan** with all loan values ([Loan contract](EN-Contract-Loan)).

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/english-contracts.png"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/english-contracts-light.png" alt="Contracts tab with expanded details for Strom Haus and Gas Heizung: blocks Contract, Prices, One-time items and Consumption, below them Recommendations and the button Acknowledge warning" width="100%"></picture></p>

*Figure: Expanded details. For Strom Haus the button "Acknowledge warning" sits under Recommendations.*

## Buttons

These are all buttons that change contracts, with their exact names in the panel. All of them exist for administrators only.

| Button | Where | What it does | Asks first |
|---|---|---|---|
| "New contract" | top of the Contracts tab | Starts the setup dialog of Home Assistant; the contract then appears in the panel by itself. | no, the dialog itself is the step |
| "Edit contract" | pencil in the row | Opens the two forms of "Reconfigure": the general data first, then the data of the category. | yes, before saving |
| "Plan next contract" | calendar in the row | Enters a future tariff that takes over by itself on the switch date. | no |
| "Edit next contract" | calendar in the row, when one is already entered | Changes the planned next contract. | no |
| "Acknowledge warning" | details, block Recommendations | Acknowledges the instalment warning. | yes |
| "Acknowledge cancellation" | details, block Recommendations | Acknowledges the cancellation reminder. | yes |
| "Delete contract" | in the edit dialog | Deletes the contract. | yes, the name has to be typed |
| "Delete for good" | in the delete question | Carries out the deletion, active only when the name matches. | see above |
| "Remove planned contract" | in the next-contract dialog | Removes only the plan, not the current contract. | yes |
| "Mark the cancellation as done" | box in the next-contract dialog (only when a cancellation reminder is due) | Acknowledges the cancellation in the same step as saving the next contract. | no |

Further named buttons: **Renew contract** (icon, [see below](#renew-a-flat-rate-contract)), **Archive** (only when the contract has expired, [see below](#archive)), **Edit instalments** and **Add item**.

## Acknowledge: warning and cancellation

The card in the overview only shows the note with the reason. You acknowledge in the expanded details, in the block **Recommendations**, depending on the situation:

- **"Acknowledge warning"** acknowledges the instalment warning (like the button "Acknowledge instalment warning"). The button only appears if the warning is switched on in the contract data and the forecast is below the threshold.
- **"Acknowledge cancellation"** acknowledges the cancellation reminder (like the button "Acknowledge cancellation"). It appears while the reminder is active.

Both ask a **second time** so nothing is triggered by accident: for the warning button the question is "Acknowledge the instalment warning? It will not be shown again for this contract unless the forecast recovers first.", for the cancellation button "Acknowledge the cancellation reminder? The reminder is dismissed for this contract." You answer with **Yes, acknowledge** or **Cancel**. More about the reminder in [Contract end and switching](EN-Contract-End-and-Switching).

## New contract

The button **"New contract"** (top of the Contracts tab) runs the setup dialog of Home Assistant inside the panel: name, category and provider first, then the data of the category. The picture shows the second step for a gas contract (gas unit, unit price, calorific value, state number and more fields). With **Save** you create the contract, it appears in the panel by itself. The fields are the same as in the setup under Settings → Devices & services, see [Creating contracts](EN-Creating-Contracts).

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/new-contract-dialog.png" alt="Dialog New contract, second step for gas: gas unit, unit price, base price, monthly instalment, calorific value, state number, warning threshold and more fields, at the bottom the buttons Save and Cancel" width="520"></p>

*Figure: The dialog "New contract", here the data of the gas category (German labels in this screenshot).*

## Edit a contract

**"Edit contract"** (pencil) shows the two forms of "Reconfigure": the general data first (with Next), then the data of the category. Everything the forms contain is replaced by what you save. Before saving the panel asks once more ("Save the changes? The contract data is replaced with what the form shows." with **Yes, save**).

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/edit-contract-dialog.png" alt="Dialog Edit contract for Strom Haus, step with prices and consumption: unit price, base price, monthly instalment, consumption sensor, warning threshold and more fields, at the bottom Save, Cancel and Delete contract" width="520"></p>

*Figure: The dialog "Edit contract" for Strom Haus with the data of the category (German labels in this screenshot). At the bottom: Save, Cancel and "Delete contract".*

- Acknowledged reminders, "notification sent" markers and the frozen consumption of the last contract term are kept. The cancellation reminder starts over only when the contract end or the reminder lead time changes.
- If the instalment changes, Tariffy remembers the date of the change so the calculation for the time before keeps using the old instalment.
- An empty optional field removes its value.
- **The name** of the contract is the first field of the first step and can be changed (empty keeps the old one). It renames the contract and its device, while sensors, entity IDs and contract data stay.
- **Flat-rate contracts** (internet, mobile, streaming, insurance, other): in the cost step you choose the **payment interval** (monthly, quarterly, half-yearly, yearly) and enter the **amount per payment**, for an insurance for example the yearly premium. Tariffy still works with the amount per month internally (600 € a year is 50 € a month); existing contracts are monthly and stay unchanged. Changing only the interval is not a price change. When the premium rises, you enter the new amount (it applies from the day you save) or renew the contract.
- **Cost so far with payment in advance:** when it is not paid monthly the **debits** count, not a monthly share: an insurance that was paid 896.63 € shortly after the start shows 896.63 € under "Cost so far", the second debit is added after a year. Tariffy assumes the first debit at the **contract start**; you enter the real date in the field **Date of the first debit**. The contract details show the first and the **next payment**. Debits after the contract end already belong to the next term. With monthly payment everything stays as it was. Details: [Payments and costs](EN-Payments-and-Costs).
- Increases in the middle of the term of a metered contract are entered here (the new instalment applies from the day you save).

## Plan the next contract

**"Plan next contract"** (calendar icon; **"Edit next contract"** if one is already entered) shows the same form as "Configure" in Home Assistant, titled "Next contract · name". You enter the switch date and the new values (provider, customer number, tariff name, instalment, base price, contract end). Fields you leave empty keep the current value. On the switch date Home Assistant takes over the next contract by itself (see [Contract end and switching](EN-Contract-End-and-Switching) and [Next contract or renew](EN-Next-Contract-or-Renew)).

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/next-contract-dialog.png" alt="Dialog Next contract for Internet: switch date, new provider, customer number, tariff name, new instalment, new base price, new contract end and the box Mark the cancellation as done" width="520"></p>

*Figure: The dialog "Next contract" for the contract Internet, with the box "Mark the cancellation as done" (German labels in this screenshot).*

- If a cancellation reminder is due, there is the box **"Mark the cancellation as done"** (on by default). It acknowledges the cancellation in the same step in which you save the next contract. If that fails, a note tells you to use "Acknowledge cancellation" instead.
- **"Remove planned contract"** removes only the plan, not the current contract. It asks first ("Remove the planned next contract? The current contract stays as it is." with **Yes, remove**).
- There is deliberately no "switch now" in the panel: it would replace the current contract at once although the new one only starts on the planned date. The switch happens by itself on that date.

## Renew a flat-rate contract

For contracts without consumption (insurance, internet, mobile, streaming, other) every row has an icon **Renew contract** (two arrows in a circle). The dialog suggests: start the day after the current end, new end one year later (for a contract **without an end**: start today, end empty; the contract then runs on without an end after a price adjustment), interval and amount as before. You enter for example the new premium, and the dialog shows at once by how many percent the contract gets dearer or cheaper (compared per month). With **Renew**:

- The current term goes to the **history** (term, provider, tariff, instalment, instalments paid). So there is one entry per year and you see how the premium rises.
- The contract runs on with the new start, end and amount. Provider, tariff, customer number and everything else stay.
- Acknowledged cancellation reminders and the date of an earlier instalment change belong to the old term and start over; the reminder follows the new end.

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/renew-dialog.png" alt="Dialog Renew contract for Internet: start, end, payment interval yearly, amount per payment 432 with the note 10.0 percent cheaper, first debit optional" width="520"></p>

*Figure: "Renew contract": with a yearly payment of 432 € the dialog shows "10.0 % cheaper (36.00 € instead of 39.99 € per month)" (German labels in this screenshot).*

Metered contracts (electricity, gas, water) have the **next contract** for this, which takes over by itself on its planned date. Loans have the **follow-up financing** instead of renewing ([Loan contract](EN-Contract-Loan)).

## Instalments paid

When the supplier changes the instalment by itself, Tariffy calculates the new amount retroactively as long as you enter nothing. That is why every contract with an instalment (not the loan) has the block **Instalments paid**. There you enter **what was paid from when**, for example for gas months 1–7 178 €, month 8 174.41 €, months 9–11 215 €:

| Month | Instalment |
|-------|----------|
| March to July | 178.00 € |
| August | 174.41 € |
| September until today | 215.00 € |

- The dialog **Edit instalments** has **one field per payment of the term**, matching the **payment interval**: for monthly payment one field per month, for quarterly four a year, for half-yearly two, for yearly one. For payments that are not monthly the debit date stands before the field, and you enter the amount **per payment**. Payments that **have not come yet are locked** and show the current instalment. If the contract has no end, the payments are listed until today. Saving applies to all payments together.
- A change also applies to **the following payments that still have the same amount**: you enter 178 in March, 174.41 in August and 215 in September; nothing more to do. An empty field takes over the amount of the payment before.
- The **last payment is the current instalment**: Tariffy takes its amount as the instalment of the contract. The contract needs a start.
- Only the payments where the amount changes are stored (at most 60).
- With the history, **Paid so far**, **Credit / balance due so far**, the **forecast at contract end** and the **recommended instalment** use the amounts that really applied. Without rows the current instalment applies as before.
- When you **renew** a flat-rate contract and on a **tariff switch** the new term starts without the old history; the old term is in the history with its values.

The calculation rules are in [Payment history and one-off items](EN-Payment-History-and-One-off-Items).

## One-off items

Every contract has the block **One-time items** in its details. There you enter one-time amounts that are not part of the instalment, with **Description**, **Amount** and **Date**:

- a **positive** amount is a **credit**, for example a switching bonus,
- a **negative** amount is a **bill**, for example a broker's fee.

**Add item** creates an item, the pencil in its row edits it (it can be deleted there too). The row **Net** under the items shows the sum. An item counts from its date (without a date at once). It changes the **balance so far** and the **total cost** over all terms: a bonus lowers the cost, a bill raises it. **The forecast at contract end and the warning for a too low instalment still depend on the consumption only.** One-off items apply to every kind of contract, are kept when you renew and on a tariff switch, and are part of the backup. For the streaming category the block does not appear as long as the contract has no one-off items. The field **New customer bonus** in the contract form stays as it was and is only displayed.

## Archive

A contract whose end has passed and that has no next contract gets the badge **Expired** in the overview and a note that it can be archived. In the details there is the button **Archive** (asks first, "Yes, archive"). Then the contract leaves the overview, the costs, the contracts and the totals, appears in the **History**, and its reminders and warnings are off. Nothing is deleted; **Restore** in the History brings it back. Nothing is archived automatically. More in [Panel history](EN-Panel-History) and [Archive and history](EN-Archive-and-History).

## Delete a contract

**"Delete contract"** is in the edit dialog. Because this cannot be undone, the question opens: "Delete the contract ... for good? This cannot be undone. Type its name to confirm." The button **"Delete for good"** only becomes active when you type the **name of the contract**.

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/delete-contract-dialog.png" alt="Delete question in the dialog Edit contract for Strom Haus: note about deleting for good, input field for the name with a red border because only Strom is typed, and the still greyed-out button Delete for good" width="520"></p>

*Figure: The delete question. As long as the name does not match (here only "Strom" instead of "Strom Haus"), "Delete for good" stays locked (German labels in this screenshot).*

- Sensors, buttons and the device of the contract are removed, and so are open notifications about cancellation and instalment. The panel says: "Its sensors and buttons are removed. The long-term statistics Home Assistant already recorded stay in its database." They can be removed in the developer tools under Statistics.
- Tariffy remembers the deleted contract for **30 days** and offers it in the **Backup** tab to bring back ([Panel backup](EN-Panel-Backup)).
- Deleting the **last** contract removes the panel from the sidebar. You then add a new contract under Settings → Devices & services → Tariffy → Add.

## Example: add a one-off item

You still have to book a fee of 12.50 € on the contract **Strom Haus**. In the mock data the switching bonus (+80.00 €, 15.01.2026) and the broker's fee (−25.00 €, 20.01.2026) are already there, and the row **Net** shows +55.00 €.

1. Tab **Contracts**, expand the row **Strom Haus**.
2. In the block **One-time items** click **Add item**.
3. In the dialog "Add a one-time item" enter "Gebühr" as **Description**, "-12,5" as **Amount (+ credit, − bill)**, and the **Date** as you like.
4. **Save**.

Then the item is in the list and **Net** shows +42.50 € (55.00 € − 12.50 €). By calculation the **Credit / balance due so far** also falls from −206.24 € to −218.74 €, because the item counts in the balance from its date. The **forecast at contract end** (−495 €) and the recommended instalment (127.66 €) do not change because they depend on the consumption only.

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/once-dialog.png" alt="Dialog Add a one-time item for Strom Haus: description Gebühr, amount minus 12,5, date empty, buttons Save and Cancel" width="520"></p>

*Figure: The dialog "Add a one-time item" with the example "Gebühr", −12.5 (German labels in this screenshot).*

## On a phone

On a phone the icons stand in the row under the name, and the detail blocks expand one below the other. Everything else works as on the desktop.

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-contracts.png"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-contracts-light.png" alt="Contracts tab on a phone: the button New contract on top, below it the contracts as cards with icons for next contract and edit" width="300"></picture></p>

*Figure: The Contracts tab on a phone (German labels in this screenshot).*

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/list-390.png" alt="Contracts tab at 390 pixels width: New contract on top, each card with badge, balance and the icons renew, next contract, edit and arrow" width="300"></p>

*Figure: The same list at 390 pixels width (German labels in this screenshot).*

## Errors and notes

If an action fails, the message "Action failed: ..." appears in red under the button. For deleting it is "Deleting failed: ...", for saving "Saving failed: ...".

| Message or problem | Solution |
|---|---|
| "The form could not be loaded" | Home Assistant was briefly unreachable or the contract is not loaded right now. Close the dialog and open it again. |
| "This form has fields the panel cannot show yet. Please use the setup of Home Assistant." | Edit the contract under Settings → Devices & services → Tariffy. |
| No buttons or icons visible | The actions exist for administrators only ([Panel permissions and design](EN-Panel-Permissions-and-Design)). |
| Old interface, buttons missing | Hard-reload the page (Ctrl+F5). |

## See also

- [Panel overview](EN-Panel-Overview) and [Panel costs](EN-Panel-Costs): the views without actions.
- [Panel history](EN-Panel-History): earlier terms, archive, adding old contracts by hand.
- [Panel backup](EN-Panel-Backup): bring back deleted contracts.
- [Creating contracts](EN-Creating-Contracts): the fields when creating.
- [Payments and costs](EN-Payments-and-Costs), [Payment history and one-off items](EN-Payment-History-and-One-off-Items), [Contract end and switching](EN-Contract-End-and-Switching), [Next contract or renew](EN-Next-Contract-or-Renew): the background of the actions.
