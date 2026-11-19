[🇩🇪 Deutsch](Sensoren-Referenz) · 🇬🇧 English

# Sensor reference

This page lists all sensors and buttons that Tariffy creates for a contract: name, unit, meaning and attributes, ordered by category. It is meant for looking things up, for example when building a dashboard or an automation.

**Contents:**
- [Device and entities](#device-and-entities)
- [Sensors for all contracts](#sensors-for-all-contracts)
- [Electricity](#electricity)
- [Electricity (dual tariff)](#electricity-dual-tariff)
- [Gas](#gas)
- [Water](#water)
- [Insurance](#insurance)
- [Leasing](#leasing)
- [Loan](#loan)
- [Flat-rate contracts](#flat-rate-contracts)
- [Buttons](#buttons)
- [Example](#example)
- [See also](#see-also)

## Device and entities

- Every contract is **one device** in Home Assistant. The device name is the contract name, the **manufacturer** is the provider, the **model** is the category (for example `Electricity`, `Electricity (HT/NT)`, `Gas`, `Water`).
- Sensors and buttons of the contract belong to this device. Their **entity ID** consists of the device name and the name of the entity, for example `sensor.strom_haus_cost_so_far`. That is **an example**: the ID depends on the contract name and on the language in which Home Assistant created the entity. Check the real ID in the settings of the entity.
- The **Key column** in the tables is the ending of the `unique_id` (`<entry ID>_<key>`). It stays the same even if you rename the entity.
- The **names** come from the translations of the integration. The tables give them exactly as they appear in an English Home Assistant.
- **Currency:** amount sensors carry the currency from the Home Assistant configuration as their unit, for example `EUR`, `EUR/kWh`, `EUR/Monat`. The tables write `currency` for it. The word `Monat` in the unit is the same in all languages.
- **Update:** after Home Assistant has started, every 6 hours and daily at 00:00:01.
- **Dates:** the sensors **Contract start**, **Contract end**, **Next switch** and **Cancellation reminder** deliver a date as **text** in the format `DD.MM.YYYY`, not a date object of Home Assistant.
- A sensor without a value shows `unknown`. That is normal as long as prerequisites are missing, for example the consumption sensor.
- Which sensors exist is decided when the contract is loaded. If you only switch on a night rate, tiered pricing or an outdoor meter later, the sensors appear after the contract is reloaded.

> **Good to know:** The sensor **Unit price** carries the attributes `kundennummer` and `marktlokation`, among others. Keep that in mind when you share dashboards, screenshots or state data.

## Sensors for all contracts

Every contract gets these sensors, whatever the category. The four sensors for consumption and forecast only have a value if a **consumption sensor** is entered (see [Measuring-Consumption](EN-Measuring-Consumption)).

| Name | Key | Unit | Meaning | Attributes |
|---|---|---|---|---|
| Monthly payment | `abschlag` | currency/Monat | monthly instalment (for a payment that is not monthly, the amount per month) | – |
| Installment total (contract term) | `jahreskosten` | currency | instalment × term in months, only the payment plan, **not** a cost forecast | – |
| Remaining term | `restlaufzeit` | days | days until the contract end (negative after the end), empty without a contract end | – |
| Contract start | `beginn` | text `DD.MM.YYYY` | start date of the contract | – |
| Contract end | `ende` | text `DD.MM.YYYY` | end of the current contract | – |
| Provider | `anbieter` | – | name of the provider (category diagnostic) | – |
| Customer number | `kundennummer` | – | customer number (category diagnostic) | – |
| Tariff | `tarif` | – | tariff name (category diagnostic) | – |
| Next switch | `naechster_wechsel` | text `DD.MM.YYYY` | date of the planned next contract, empty without one | `anbieter`, `tarif`, `kundennummer`, `arbeitspreis`, `grundpreis`, `abschlag`, `jahresverbrauch`, `ende` of the planned contract |
| Cancellation reminder | `kuendigung_erinnerung` | text `DD.MM.YYYY` | date from which the reminder runs (based on the last day to cancel if a notice period is entered) | `aktiv`, `bestaetigt`, `monate_vorher`, `kuendigungsfrist_monate`, `kuendigung_bis` |
| Consumption (so far) | `verbrauch_bisher` | kWh for electricity; for gas and water the unit of the meter (Wh and MWh as kWh) | measured consumption since the contract start | `verbrauch_hochgerechnet`, `verbrauch_bisher_ht`, `verbrauch_bisher_nt` |
| Consumption (contract term projected) | `verbrauch_hochgerechnet` | as above | consumption projected over the real contract term | – |
| Refund/balance due (contract end) | `prognose_real` | currency | forecast: instalments over the term minus estimated cost. Positive credit, negative balance due. Icon: thumb up or down | `tendenz` (`Guthaben` or `Nachzahlung`), `verbrauch_hochgerechnet`, `abschlag_warnung_aktiv`; with PV self-sufficiency also `autarkie_variante`, `autarkie_monatswerte`, `autarkie_bisher`, `autarkie_bisher_nt`, `autarkie_naeherung`, `prognose_ohne_autarkie`; with a total-consumption sensor also `verbrauch_gesamt_bisher`, `verbrauch_gesamt_hochgerechnet`, `verbrauch_pv_gedeckt_bisher`, `verbrauch_pv_gedeckt_hochgerechnet` |
| Instalment adjustment (recommended) | `abschlag_anpassung_empfohlen` | currency/Monat | instalment that balances out exactly from today until the contract end. Icon: thumb down if a raise is recommended | `aktueller_abschlag`, `differenz` |

The values of the attribute `tendenz` are the German words `Guthaben` (credit) and `Nachzahlung` (balance due) in every language. The calculation path of these values is in [Payments-and-Costs](EN-Payments-and-Costs), the self-sufficiency attributes are in [PV-Self-Sufficiency](EN-PV-Self-Sufficiency).

## Electricity

In addition to the sensors for all contracts:

| Name | Key | Unit | Meaning | Attributes |
|---|---|---|---|---|
| Unit price | `arbeitspreis` | currency/kWh | price per kWh. For a dynamic tariff the statistics mean of the price sensor since the contract start plus the markup | `anbieter`, `tarif`, `kundennummer`, `sparte`, `jahresverbrauch`, `marktlokation`, `oekostrom`, `bonus`, `preisgarantie_bis`, `dynamischer_tarif` (whether a price sensor is set), `arbeitspreis_aktuell` (current price of the price sensor plus markup) |
| Base price | `grundpreis` | currency/Monat | monthly base price | – |
| Cost (so far) | `kosten_bisher` | currency | consumption so far × unit price + base price × months passed | `verbrauch_bisher`, `kosten_ht_bisher`, `kosten_nt_bisher` |
| Refund/balance due (so far) | `guthaben_bisher` | currency | instalments paid minus cost so far, plus one-time items of the running term. Icon: thumb up or down | `tendenz` (`Guthaben` or `Nachzahlung`), `kosten_bisher` |
| Consumption (last period) | `verbrauch_letzte_laufzeit` | kWh | consumption of the last term, frozen at the tariff switch | – |
| Monthly payment (recommended) | `empfohlener_abschlag` | currency/Monat | recommendation after a tariff switch, from the consumption of the last term | `verbrauch_letzte_laufzeit`, `verbrauch_letzte_laufzeit_monate`, `aktueller_abschlag`, `differenz` |
| Meter number | `zaehlernummer` | – | meter number (category diagnostic) | – |
| Feed-in tariff | `einspeiseverguetung` | currency/kWh | entered payment per kWh fed in, only the entered value | – |

Only if the option is used, these appear as well:

| Name | Key | Unit | Meaning | Attributes |
|---|---|---|---|---|
| Unit price (night) | `arbeitspreis_nacht` | currency/kWh | night price (Economy 7, TOU). Appears when a night price, annual day and night consumption and a unit price are entered | `verbrauch_tag`, `verbrauch_nacht`, `tou_jahreskosten` |
| Unit price (effective) | `effektiver_arbeitspreis` | currency/kWh | average price with tiered pricing | `tier_limits`, `tier_prices`, `tiered_jahreskosten`, `aktiv` |

More about the contract in [Contract-Electricity](EN-Contract-Electricity).

## Electricity (dual tariff)

All sensors of **Electricity** (with the high-tariff register as the main meter) and in addition:

| Name | Key | Unit | Meaning | Attributes |
|---|---|---|---|---|
| Unit price (low tariff / NT) | `arbeitspreis_nt` | currency/kWh | price of the low tariff, as entered | – |
| Meter number (low tariff / NT) | `zaehlernummer_nt` | – | meter number of the low-tariff register (category diagnostic) | – |
| Consumption, high tariff (so far) | `verbrauch_ht_bisher` | kWh | measured consumption of the high-tariff register since the contract start | – |
| Consumption, low tariff (so far) | `verbrauch_nt_bisher` | kWh | measured consumption of the low-tariff register since the contract start | – |
| Cost, high tariff (so far) | `kosten_ht_bisher` | currency | consumption cost of the high tariff without base price | `verbrauch_bisher_ht` |
| Cost, low tariff (so far) | `kosten_nt_bisher` | currency | consumption cost of the low tariff without base price | `verbrauch_bisher_nt` |

**Consumption (so far)**, **Cost (so far)** and the forecast apply to both registers together. As soon as both registers have a consumption, the sensor **Unit price** shows the average price of both registers weighted by consumption, before that the high-tariff price. More in [Contract-Electricity](EN-Contract-Electricity).

## Gas

The same sensors as **Electricity**, without **Feed-in tariff**, and in addition:

| Name | Key | Unit | Meaning | Attributes |
|---|---|---|---|---|
| Annual usage (kWh) | `verbrauch_kwh` | kWh | the entered annual consumption, converted to kWh (calorific value × state number for m³, CCF and ft³; therm and MBtu with a fixed factor) | `jahresverbrauch_m3` (the entered value in the unit of the contract data), `brennwert`, `zustandszahl` |

**Consumption (so far)** and **Consumption (contract term projected)** show the unit of the meter for gas, usually m³. **Cost (so far)** and the forecast calculate in kWh with calorific value × state number. The sensors for the night rate and tiered pricing are also possible for gas. More in [Contract-Gas](EN-Contract-Gas).

## Water

In addition to the sensors for all contracts:

| Name | Key | Unit | Meaning | Attributes |
|---|---|---|---|---|
| Unit price (wastewater) | `arbeitspreis_abwasser` | currency/water unit | wastewater price (for a percentage the calculated price, for a flat monthly rate the entered amount) | `typ`, `pauschal_monat` |
| Water price (combined) | `arbeitspreis_gesamt_wasser` | currency/water unit | fresh water plus wastewater | – |

Only with at least one **outdoor meter** (garden, pool) these appear as well:

| Name | Key | Unit | Meaning | Attributes |
|---|---|---|---|---|
| Outdoor water (consumption) | `garten_verbrauch` | unit of the meter | consumption of the outdoor meters, not liable for wastewater | – |
| Outdoor water (cost) | `garten_kosten` | currency | cost of this consumption without wastewater | – |
| Wastewater-liable consumption | `abwasserpflichtiger_verbrauch` | unit of the meter | main meter minus outdoor meters | – |
| Wastewater cost | `abwasser_kosten` | currency | wastewater share of the cost | – |

> **Good to know:** For water Tariffy does not create the sensors **Unit price**, **Base price**, **Cost (so far)**, **Refund/balance due (so far)**, **Consumption (last period)**, **Monthly payment (recommended)** and **Meter number**. The panel shows the cost so far and the balance today anyway, because they come from the contract data. The forecast at the contract end exists as a sensor. More in [Contract-Water](EN-Contract-Water).

## Insurance

In addition to the sensors for all contracts. The vehicle sensors only have a value for a car insurance.

| Name | Key | Unit | Meaning | Attributes |
|---|---|---|---|---|
| Type of insurance | `versicherungsart` | – | choice: Car, Building / house, Household contents, Liability, Health, Life, Legal protection, Accident, Other | – |
| Licence plate | `kennzeichen` | – | licence plate of the vehicle (category diagnostic) | – |
| Odometer at contract start | `km_start` | km | odometer at the start | – |
| Allowed kilometres per year | `km_pro_jahr` | km | agreed kilometres per year | – |

More in [Contract-Insurance](EN-Contract-Insurance).

## Leasing

In addition to the sensors for all contracts a leasing contract gets the vehicle sensors **Licence plate**, **Odometer at contract start** and **Allowed kilometres per year** (as for insurance) and three sensors for the kilometres:

| Name | Key | Unit | Meaning | Attributes |
|---|---|---|---|---|
| Kilometres driven | `leasing_km_gefahren` | km | odometer minus the reading at the start | `km_stand`, `km_erlaubt`, `km_soll`, `abweichung_soll`, `km_rest`, `km_rest_je_tag`, `km_je_tag`, `prozent_der_erlaubten` |
| Projected kilometres at return | `leasing_km_hochgerechnet` | km | projection of the kilometres until the return | `abweichung_ende`, `mehr_km`, `minder_km` |
| Expected extra/shortfall kilometre cost | `leasing_km_kosten` | currency | expected balance due or credit at the return | `nachzahlung`, `gutschrift`, `mehr_km`, `minder_km` |

More in [Contract-Leasing](EN-Contract-Leasing).

## Loan

In addition to the sensors for all contracts (without consumption for a loan) four sensors:

| Name | Key | Unit | Meaning | Attributes |
|---|---|---|---|---|
| Remaining debt | `kredit_restschuld` | currency | debt still open | `tilgung_prozent`, `rate`, `naechste_zahlung`, `zins_anteil`, `tilgung_anteil` |
| Paid so far | `kredit_gezahlt` | currency | instalments paid so far | `zinsen`, `tilgung`, `zahlungen` |
| Remaining payments | `kredit_restsumme` | currency | sum still to pay | `zahlungen_offen` |
| Interest paid so far | `kredit_zinsen_bisher` | currency | interest paid so far | `zinsen_gesamt` |

More in [Contract-Loan](EN-Contract-Loan).

## Flat-rate contracts

**Internet**, **Mobile**, **Streaming** and **Other** only have the sensors for all contracts. **Monthly payment** is the amount per month there, **Installment total (contract term)** the total amount of the term. The four sensors for consumption and forecast stay empty without a consumption sensor. Cost so far exists for these contracts only in the panel, as the instalments due until today.

## Buttons

Every contract has three buttons on the same device. A button is only **available** as long as its action makes sense.

| Name | Key | Available when | What it does |
|---|---|---|---|
| Switch now | `jetzt_wechseln` | a next contract is planned | takes over the planned next contract at once, without waiting for the date, and freezes the consumption of the ending term as at the automatic switch |
| Confirm cancellation | `kuendigung_bestaetigen` | the cancellation reminder is active | acknowledges the reminder and removes the persistent notification |
| Confirm low-instalment warning | `abschlag_warnung_bestaetigen` | the low-instalment warning is open and not yet acknowledged | acknowledges the warning. If the forecast worsens again later, Tariffy warns again |

An **entity ID** such as `button.strom_haus_switch_now` is an example again. In the panel the actions are called **Acknowledge warning** and **Acknowledge cancellation**. More in [Contract-End-and-Switching](EN-Contract-End-and-Switching).

## Example

The sensors of the contract **Strom Haus** from the sample data of the panel, reference date 12 July 2026 (contract 1 Jan to 31 Dec 2026, instalment 40 €):

| Name | Value |
|---|---|
| Monthly payment | 40 EUR/Monat |
| Installment total (contract term) | 478.32 EUR |
| Unit price | 0.2977 EUR/kWh |
| Base price | 11.51 EUR/Monat |
| Consumption (so far) | 1,481.17 kWh |
| Consumption (contract term projected) | 2,808.1 kWh |
| Cost (so far) | 513.54 EUR |
| Refund/balance due (so far) | −206.24 EUR (with one-time items +55 EUR) |
| Refund/balance due (contract end) | −495.29 EUR, attribute `tendenz`: `Nachzahlung` |
| Instalment adjustment (recommended) | 127.66 EUR/Monat |
| Remaining term | 172 days |
| Contract start | 01.01.2026 |
| Contract end | 31.12.2026 |

How these numbers fit together is worked out in [Payments-and-Costs](EN-Payments-and-Costs).

## See also

- [Dashboard-Examples](EN-Dashboard-Examples): cards with these sensors
- [Automations](EN-Automations): sensors and buttons in automations
- [Measuring-Consumption](EN-Measuring-Consumption) and [Payments-and-Costs](EN-Payments-and-Costs): how the values come about
- [PV-Self-Sufficiency](EN-PV-Self-Sufficiency): attributes about self-sufficiency
- [Panel-Overview](EN-Panel-Overview): the same values in the panel
