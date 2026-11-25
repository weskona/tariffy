[🇩🇪 Deutsch](Vertraege-Anlegen) · 🇬🇧 English

# Creating contracts

This page gives you the overview of all categories, the general fields of the first form, the ways to edit and delete a contract and typical mistakes. The fields of each category are on the respective category pages.

**Contents:**

- [Where do you create a contract?](#where-do-you-create-a-contract)
- [All categories at a glance](#all-categories-at-a-glance)
- [The general fields (step 1)](#the-general-fields-step-1)
- [Editing a contract](#editing-a-contract)
- [Deleting a contract](#deleting-a-contract)
- [Typical mistakes](#typical-mistakes)

## Where do you create a contract?

There are two ways that lead to the same form:

1. **In the panel:** the **Contracts** tab, button **New contract** (administrators only).
2. **In Home Assistant:** **Settings → Devices & services → Add integration → Tariffy**.

The first form is called **Add contract** ("General contract data.") and is the same for all categories. The **Category** decides which form follows. In the panel the forms appear in a dialog; the button is called **Next** on every step except the last one, and **Save** on the last. Every contract becomes its own device, as described in [Getting started](EN-Getting-Started).

![The New contract dialog in the panel, here the Gas details step with gas unit, unit price, base price, monthly instalment, calorific value and state number](https://raw.githubusercontent.com/wiki/weskona/tariffy/images/new-contract-dialog.png)

*Figure: The "New contract" dialog in the panel (German panel), here the second step of a gas contract with the buttons "Speichern" (Save) and "Abbrechen" (Cancel).*

## All categories at a glance

The **Category** selection offers these entries in this order:

| Category | Billing | Forms after step 1 | Page |
|---|---|---|---|
| Electricity | by consumption | **Electricity details** | [Contract electricity](EN-Contract-Electricity) |
| Electricity (dual tariff, HT/NT) | by consumption, two meter registers | **Electricity details (dual tariff, HT/NT)** | [Contract electricity](EN-Contract-Electricity#dual-tariff-htnt) |
| Gas | by consumption | **Gas details** | [Contract gas](EN-Contract-Gas) |
| Water | by consumption | **Water contract details** | [Contract water](EN-Contract-Water) |
| Internet | flat rate | **Cost** | [Contract internet and mobile](EN-Contract-Internet-and-Mobile) |
| Mobile | flat rate | **Cost** | [Contract internet and mobile](EN-Contract-Internet-and-Mobile) |
| Streaming | flat rate | **Cost** | [Contract streaming](EN-Contract-Streaming) |
| Loan / financing | own repayment plan, not part of the totals of the contracts | **Loan / financing** | [Contract loan](EN-Contract-Loan) |
| Leasing | flat rate plus kilometres | **Leasing**, then **Cost** | [Contract leasing](EN-Contract-Leasing) |
| Insurance | flat rate | **Insurance**, for a car **Car insurance**, then **Cost** | [Contract insurance](EN-Contract-Insurance) |
| House costs | flat rate plus type | **House costs** (type), then **Cost** | [Contract house costs](EN-Contract-House-Costs) |
| Other | flat rate | **Cost** | [Contract other](EN-Contract-Other) |

**Metered contracts** (electricity, electricity HT/NT, gas, water) use a meter sensor to work out real cost, balance and forecast. **Flat-rate contracts** have an amount per payment and a payment interval (monthly, quarterly, half-yearly, yearly). In the panel loan and leasing stand in the group **Loans / financing**.

> **Good to know:** The category decides which sensors a contract gets. You can pick it again in the edit form, but it is better to create the contract with the right category right away. Which sensors exist where is listed in the [Sensor reference](EN-Sensor-Reference).

## The general fields (step 1)

| Field | Required | Description |
|---|---|---|
| Label (e.g. Electricity House) | yes | Short name; it appears in the device name and in the panel. When editing the field is called **Name**. |
| Category | yes | See the table above. |
| Provider | yes | Name of the energy provider or supplier. |
| Customer number | no | Your customer number from the provider's documents. |
| Tariff name | no | Name of the tariff, for example "Eco Power Plus". |
| Icon | no | Own icon of the contract, for example `mdi:car`. Used in the panel and for the sensors of the contract (sensors with a status icon such as refund/balance due keep theirs). Empty = the icon of the category. |
| Contract start | no | Date from which the contract is valid. Without a start there is no consumption tracking. |
| Contract end / valid until | no | Last day of the contract term. |
| Minimum term (months) | no | The panel shows until when the contract runs at least (start plus minimum term). |
| Notice period (months) | no | Months before contract end by which the cancellation must be received. If set, the reminder refers to this deadline instead of the contract end. |
| Cancellation reminder | yes | **No reminder**, **1 month before** up to **4 months before** (default: 3 months). Refers to the contract end, or to the end of the notice period if one is entered. |
| Notification target (notify service) | no | Home Assistant notification service for the reminder, for example `mobile_app_iphone`. The field only appears if Home Assistant knows at least one notify service; custom values are possible. |

A date field is a normal date picker, the fields for months are number fields. How the reminder works exactly is described at [Contract end and switching](EN-Contract-End-and-Switching).

> **Good to know:** Without a **Contract end** there is no cancellation reminder, because the date is calculated from the contract end.

## Editing a contract

This is how you change an existing contract:

1. In the panel open the **Contracts** tab and click the pencil **Edit contract** in the row of the contract (administrators only). Alternatively use the menu of the Tariffy entry in Home Assistant (Reconfigure).
2. The same form opens as when creating, but with the stored values and the title **Edit contract · Strom Haus** (with the name of your contract).
3. Change the values and click **Next**, or on the last step **Save**.
4. In the panel Tariffy asks one last time: "Save the changes? The contract data is replaced with what the form shows." Confirm with **Yes, save**.
5. Home Assistant reloads the contract and works with the new values.

![The Edit contract dialog for Strom Haus with the fields of the electricity details and the buttons Save, Cancel and Delete contract](https://raw.githubusercontent.com/wiki/weskona/tariffy/images/edit-contract-dialog.png)

*Figure: The dialog "Edit contract · Strom Haus" (electricity details, German panel) with the buttons "Speichern" (Save), "Abbrechen" (Cancel) and "Vertrag löschen" (Delete contract).*

What is kept when editing and what changes:

- **Kept** are the history and the notes of Tariffy: history, one-time items, instalment history, outdoor meters, the consumption of the last term and archived contracts.
- **The cancellation reminder starts again** if you change the contract end, **Cancellation reminder** or **Notice period (months)**: a reminder you already confirmed is open again.
- **If the instalment changes**, Tariffy remembers the date of the change. The new amount then counts from today only, so that "Refund/balance due (so far)" is not recalculated retroactively. An instalment that you set from 0 to an amount for the first time counts for the whole term instead. If the supplier changed the instalment itself, you enter the history, see [Payment history and one-off items](EN-Payment-History-and-One-off-Items).
- If you leave the field **Name** empty, the previous name stays.

For a planned tariff switch there is not this form but the next contract: [Next contract or renew](EN-Next-Contract-or-Renew).

## Deleting a contract

The dialog **Edit contract** has the red button **Delete contract**. Then Tariffy asks: "Delete the contract "Strom Haus" for good? This cannot be undone. Type its name to confirm." The button **Delete for good** stays locked until you have typed the exact name of the contract.

![The delete confirmation in the Edit contract dialog: an input field for the name, next to it the buttons Delete for good and Cancel](https://raw.githubusercontent.com/wiki/weskona/tariffy/images/delete-contract-dialog.png)

*Figure: The confirmation when deleting (German panel). The button "Endgültig löschen" (Delete for good) is locked as long as the typed name does not match (in the picture only "Strom" is typed instead of "Strom Haus").*

After deleting:

- The sensors and buttons of the contract are gone. The long-term statistics that Home Assistant already recorded stay in the database.
- Tariffy remembers the contract for **30 days** (the last 20), even if you deleted it directly in Home Assistant. In the **Backup** tab you can bring it back with **Restore**. This is not possible if a contract with the same name and category exists in the meantime. Everything about it is at [Panel backup](EN-Panel-Backup).

> **Good to know:** If a contract just expires, you do not have to delete it: an expired contract can be archived and then stays in the history, see [Archive and history](EN-Archive-and-History).

## Typical mistakes

| Problem | Cause and solution |
|---|---|
| Cost, balance and forecast stay empty | The **Consumption sensor**, the **Contract start** or the **Unit price** is missing. Consumption tracking needs a sensor and a start. |
| Consumption is unknown although a sensor is entered | The long-term statistic of the sensor does not reach back to the contract start (for example after renaming or recreating it). Enter the **Meter reading at contract start (optional)**, it takes priority. See [Measuring consumption](EN-Measuring-Consumption). |
| No cancellation reminder | **Contract end** is missing or **Cancellation reminder** is set to **No reminder**. |
| "Not a valid number." for calorific value or state number | These two fields are text fields. A dot or a comma is allowed (`11.2` or `11,2`), nothing else. |
| The balance looks wrong because the instalment is missing | The **Monthly instalment** is a required field with default 0. Enter the real amount. |
| Wrong or missing sensors | The **Category** does not fit, for example Electricity instead of Electricity (dual tariff, HT/NT). Tiered prices and night rate only appear if a matching country is set in Home Assistant, see the category pages. |
| The panel is missing in the sidebar | The panel appears only once at least one contract is loaded. Then hard-reload the browser page (Ctrl+F5). |

More help is in [Troubleshooting](EN-Troubleshooting).

## See also

- [Getting started](EN-Getting-Started)
- [Contract electricity](EN-Contract-Electricity), [Contract gas](EN-Contract-Gas), [Contract water](EN-Contract-Water)
- [Panel contracts](EN-Panel-Contracts)
- [Panel backup](EN-Panel-Backup)
- [Payments and costs](EN-Payments-and-Costs)
- [Troubleshooting](EN-Troubleshooting)
