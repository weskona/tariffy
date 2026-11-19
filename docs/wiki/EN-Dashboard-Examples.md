[🇩🇪 Deutsch](Dashboard-Beispiele) · 🇬🇧 English

# Dashboard examples

The Tariffy panel shows all contracts ready-made. If you want single values on a Home Assistant dashboard of your own, use the sensors and buttons of the integration. This page shows examples for an entities card, a markdown card and buttons.

**Contents:**
- [Preparation: finding the entity IDs](#preparation-finding-the-entity-ids)
- [Entities card](#entities-card)
- [Entities card with attributes](#entities-card-with-attributes)
- [Markdown card](#markdown-card)
- [Markdown card with PV self-sufficiency](#markdown-card-with-pv-self-sufficiency)
- [Buttons](#buttons)
- [Example](#example)
- [See also](#see-also)

## Preparation: finding the entity IDs

**All entity IDs in the examples are examples.** They are named the way the contract `Strom Haus` is named in an English Home Assistant. Your IDs depend on the contract name and on the language in which the entities were created. Adjust them:

1. In Home Assistant open Settings, Devices & services, Tariffy and then the device of your contract.
2. Click the entity and then the cogwheel: the **entity ID** is shown there.
3. Replace the IDs in the examples with yours.

Which sensors exist for your category is listed in the [Sensor-Reference](EN-Sensor-Reference). An ID that does not exist for your contract is shown by the card as unavailable. A sensor without a value shows `unknown`.

## Entities card

The simplest card lists the most important sensors of a contract:

```yaml
type: entities
title: Strom Haus
entities:
  - entity: sensor.strom_haus_cost_so_far
  - entity: sensor.strom_haus_refund_balance_due_so_far
  - entity: sensor.strom_haus_refund_balance_due_contract_end
  - entity: sensor.strom_haus_instalment_adjustment_recommended
  - entity: sensor.strom_haus_consumption_so_far
  - entity: sensor.strom_haus_remaining_term
```

The sensors bring their unit and their icon (thumb up or down for credit and balance due). **Refund/balance due** is positive for a credit and negative for a balance due.

## Entities card with attributes

Single attributes of a sensor can be shown with rows of the type `attribute`. The names of the attributes are listed in the [Sensor-Reference](EN-Sensor-Reference):

```yaml
type: entities
title: Forecast Strom Haus
entities:
  - entity: sensor.strom_haus_refund_balance_due_contract_end
    name: Forecast at contract end
  - type: attribute
    entity: sensor.strom_haus_refund_balance_due_contract_end
    attribute: tendenz
    name: Trend
  - type: attribute
    entity: sensor.strom_haus_refund_balance_due_contract_end
    attribute: verbrauch_hochgerechnet
    name: Projected consumption
    suffix: kWh
  - type: attribute
    entity: sensor.strom_haus_instalment_adjustment_recommended
    attribute: differenz
    name: Distance to the instalment
```

- The attribute `tendenz` has the values `Guthaben` (credit) and `Nachzahlung` (balance due).
- `verbrauch_hochgerechnet` is in the unit of the consumption sensor. For electricity that is kWh.
- `differenz` on the sensor **Instalment adjustment (recommended)** is the recommended adjustment minus your current instalment.
- The attribute `arbeitspreis_aktuell` on the sensor **Unit price** only has a value for a dynamic tariff.

## Markdown card

A markdown card can combine values and attributes in one sentence. The example first checks whether the sensor has a value yet:

```yaml
type: markdown
title: Strom Haus
content: >
  {% set cost = 'sensor.strom_haus_cost_so_far' %}
  {% set balance = 'sensor.strom_haus_refund_balance_due_contract_end' %}
  Cost so far: **{{ states(cost) }} {{ state_attr(cost, 'unit_of_measurement') }}**

  {% if states(balance) not in ['unknown', 'unavailable'] %}
  Forecast at contract end: **{{ states(balance) | float | round(2) }} {{ state_attr(balance, 'unit_of_measurement') }}**
  ({{ state_attr(balance, 'tendenz') }})
  {% else %}
  The forecast is not available yet.
  {% endif %}
```

With the numbers from the sample data of the panel (contract Strom Haus, reference date 12 July 2026) the card shows roughly: cost so far 513.54 EUR, forecast at contract end −495.29 EUR (Nachzahlung).

## Markdown card with PV self-sufficiency

With [PV-Self-Sufficiency](EN-PV-Self-Sufficiency) and a total-consumption sensor the sensor **Refund/balance due (contract end)** has further attributes. The card only shows them if they exist:

```yaml
type: markdown
title: PV self-sufficiency
content: >
  {% set s = 'sensor.strom_haus_refund_balance_due_contract_end' %}
  {% if state_attr(s, 'verbrauch_gesamt_bisher') is not none %}
  Total consumption so far: {{ state_attr(s, 'verbrauch_gesamt_bisher') }} kWh

  Covered by PV: {{ state_attr(s, 'verbrauch_pv_gedeckt_bisher') }} kWh

  Self-sufficiency so far: {{ state_attr(s, 'autarkie_bisher') }} %

  Forecast without self-sufficiency: {{ state_attr(s, 'prognose_ohne_autarkie') }}
  {% else %}
  No self-sufficiency values available.
  {% endif %}
```

The attributes only exist if the self-sufficiency determines the forecast. The four values about the total consumption only exist with a total-consumption sensor.

## Buttons

The buttons of a contract can be shown in an entities card as rows with a button:

```yaml
type: entities
title: Actions Strom Haus
entities:
  - entity: button.strom_haus_confirm_low_instalment_warning
  - entity: button.strom_haus_confirm_cancellation
  - entity: button.strom_haus_switch_now
```

A button is **unavailable** as long as its action makes no sense: **Switch now** only with a planned next contract, **Confirm cancellation** only with an active reminder, **Confirm low-instalment warning** only with an open warning. If you only want to see them when needed, put the card into a conditional card (type `conditional`) with the condition that the button does not have the state `unavailable`.

## Example

One contract, three cards: the entities card from the first section shows these rows with the sample data (Strom Haus, 12 July 2026).

| Row | Value |
|---|---|
| Cost (so far) | 513.54 EUR |
| Refund/balance due (so far) | −206.24 EUR |
| Refund/balance due (contract end) | −495.29 EUR |
| Instalment adjustment (recommended) | 127.66 EUR/Monat |
| Consumption (so far) | 1,481.17 kWh |
| Remaining term | 172 days |

The balance due grows from −206 EUR today to −495 EUR at the contract end. The recommended instalment of 127.66 EUR compared with 40 EUR shows how much higher the instalment would have to be. The calculation path is shown in [Payments-and-Costs](EN-Payments-and-Costs).

> **Good to know:** The attributes `kundennummer` and `marktlokation` on the sensor **Unit price** are personal data. Only show them on a dashboard if you want to, and keep it in mind when you share dashboards.

## See also

- [Sensor-Reference](EN-Sensor-Reference): all sensors, buttons and attributes
- [Automations](EN-Automations): sensors and buttons in automations
- [Panel-Overview](EN-Panel-Overview): the finished panel
- [PV-Self-Sufficiency](EN-PV-Self-Sufficiency)
