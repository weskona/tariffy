[🇩🇪 Deutsch](Automationen) · 🇬🇧 English

# Automations

Tariffy already reminds and warns with notifications. With automations you can extend that: a second message on another channel, a daily repeat or your own threshold. This page gives four ready examples to adapt.

**Contents:**

- [Before you start](#before-you-start)
- [Cancellation reminder](#cancellation-reminder)
- [Instalment warning](#instalment-warning)
- [Back-payment threatens](#back-payment-threatens)
- [Leasing: kilometre warning](#leasing-kilometre-warning)

## Before you start

> **Important:** The examples are **written from the integration's code**, not tried out on a running Home Assistant. The entity IDs are **examples** and you have to adjust them. Test every automation with **Run** or in the **Template** developer tool before you rely on it.

**Finding the entity IDs:** Every entity gets its ID from the contract name and the sensor name, in the language Home Assistant was running in when it was created. For a contract "Strom Haus" they could look like this. Copy the real ID under **Settings → Devices & services → Entities**.

| Sensor | Example ID | What the examples use |
|--------|------------|-----------------------|
| Cancellation reminder | `sensor.strom_haus_cancellation_reminder` | Value: reminder date as text (DD.MM.YYYY); attributes `aktiv`, `bestaetigt`, `monate_vorher`, `kuendigungsfrist_monate`, `kuendigung_bis` |
| Refund/balance due (contract end) | `sensor.strom_haus_refund_balance_due_contract_end` | Value: forecast in €, negative means balance due; attribute `abschlag_warnung_aktiv` |
| Instalment adjustment (recommended) | `sensor.strom_haus_instalment_adjustment_recommended` | Value: recommended instalment per month; attributes `aktueller_abschlag`, `differenz` |
| Projected kilometres at return | `sensor.car_lease_projected_kilometres_at_return` | Attributes `mehr_km`, `minder_km`, `abweichung_ende` |
| Expected extra/shortfall kilometre cost | `sensor.car_lease_expected_extra_shortfall_kilometre_cost` | Value: expected cost in €; attributes `nachzahlung`, `gutschrift` |

The buttons are called "Switch now", "Confirm cancellation" and "Confirm low-instalment warning" (see [Contract-End-and-Switching](EN-Contract-End-and-Switching)). Tariffy fires **no events of its own**; the examples therefore work with the states and attributes of the sensors. The built-in messages in the notification centre have the IDs `tariffy_kuendigung_<entry_id>` and `tariffy_abschlag_warnung_<entry_id>`.

The examples use the notation from Home Assistant 2024.10 on (`triggers`, `actions`, `trigger:`, `action:`). Tariffy needs Home Assistant 2025.8 or newer anyway. `notify.mobile_app_your_phone` is a placeholder for your own notify service.

## Cancellation reminder

The built-in reminder reports once as a persistent notification and once as a push to the contract's notification target. This automation repeats the message **every morning at 9:00** while the reminder is active, and reports it at once when it starts. It stops by itself as soon as you press **Confirm cancellation**, because the attribute `aktiv` then becomes `false`, and once the contract end has passed.

```yaml
alias: Tariffy Strom Haus - remind to cancel
description: Reports the cancellation reminder at once and then daily at 9:00 until it is acknowledged.
mode: single
triggers:
  - trigger: state
    entity_id: sensor.strom_haus_cancellation_reminder
    attribute: aktiv
    to: true
  - trigger: time
    at: "09:00:00"
conditions:
  - condition: template
    value_template: >-
      {{ state_attr('sensor.strom_haus_cancellation_reminder', 'aktiv') == true }}
actions:
  - action: notify.mobile_app_your_phone
    data:
      title: "Strom Haus: do not forget to cancel"
      message: >-
        Last day to cancel:
        {{ state_attr('sensor.strom_haus_cancellation_reminder', 'kuendigung_bis')
           or 'no notice period stored, see the contract end' }}.
        Afterwards press "Confirm cancellation" in the panel or on the device.
```

The attribute `kuendigung_bis` is only filled if the contract has a notice period and a contract end; otherwise it is empty and the template takes the fallback text.

> **Good to know:** If you enter a notification target in the contract, Tariffy sends its own push message as well. If you want only the automation's message, leave the target in the contract empty.

## Instalment warning

If the contract has the option "Warn if instalment is too low" switched on (electricity, gas, water with a consumption sensor), Tariffy sets the attribute `abschlag_warnung_aktiv` to `true` when the forecast at contract end expects a balance due above the warning threshold (default 50 €). The attribute stays `true` after acknowledging as long as the forecast is bad; it shows the raw state. The automation therefore triggers only when the warning **newly arises**, and names the recommended instalment.

```yaml
alias: Tariffy Strom Haus - instalment too low
description: Reports when Tariffy expects a balance due and names the recommended instalment.
mode: single
triggers:
  - trigger: state
    entity_id: sensor.strom_haus_refund_balance_due_contract_end
    attribute: abschlag_warnung_aktiv
    to: true
actions:
  - action: notify.mobile_app_your_phone
    data:
      title: "Strom Haus: instalment too low"
      message: >-
        A balance due of about
        {{ states('sensor.strom_haus_refund_balance_due_contract_end') | float(0) | abs | round(2) }} €
        is expected at the contract end.
        {% set recommended = states('sensor.strom_haus_instalment_adjustment_recommended') %}
        {% if recommended | is_number %}
        Recommended instalment: {{ recommended | float | round(2) }} € per month.
        {% endif %}
```

## Back-payment threatens

This automation does not need the option "Warn if instalment is too low", it checks the forecast itself against your own threshold. It reports when the forecast at contract end is worse than −100 € for **30 minutes**. The waiting time avoids messages on short fluctuations.

```yaml
alias: Tariffy Strom Haus - balance due over 100 euros
description: Own threshold for the forecast at contract end.
mode: single
triggers:
  - trigger: numeric_state
    entity_id: sensor.strom_haus_refund_balance_due_contract_end
    below: -100
    for: "00:30:00"
actions:
  - action: notify.mobile_app_your_phone
    data:
      title: "Strom Haus: balance due threatens"
      message: >-
        Forecast at contract end:
        {{ states('sensor.strom_haus_refund_balance_due_contract_end') | float(0) | round(2) }} €
        (negative means balance due).
```

Example with numbers (made up): if the sensor stands at −137.5, the message "Forecast at contract end: -137.5 € (negative means balance due)." arrives. If the value rises above −100 again before the 30 minutes are over, no message comes.

> **Good to know:** The automation only triggers when the value newly drops below the threshold. If it was already below when you create it, it only reports after the value was above in between.

## Leasing: kilometre warning

For a leasing contract with an odometer and allowed kilometres, Tariffy projects how many kilometres you will have at return. The sensor "Projected kilometres at return" has the attribute `mehr_km`: the extra kilometres **after deducting the tolerance**. The projection exists only once the contract has run for at least 14 days; before that the attribute is empty. The automation reports as soon as `mehr_km` rises above 0.

```yaml
alias: Tariffy Leasing - extra kilometres threaten
description: Reports when the projection shows extra kilometres above the tolerance.
mode: single
triggers:
  - trigger: numeric_state
    entity_id: sensor.car_lease_projected_kilometres_at_return
    attribute: mehr_km
    above: 0
actions:
  - action: notify.mobile_app_your_phone
    data:
      title: "Leasing: extra kilometres threaten"
      message: >-
        Projection at return:
        {{ states('sensor.car_lease_projected_kilometres_at_return') | float(0) | round(0) }} km.
        Extra kilometres after tolerance:
        {{ state_attr('sensor.car_lease_projected_kilometres_at_return', 'mehr_km') }} km.
        {% set cost = states('sensor.car_lease_expected_extra_shortfall_kilometre_cost') %}
        {% if cost | is_number %}
        Expected cost: {{ cost | float | round(2) }} €.
        {% endif %}
```

The expected cost exists only if the contract has a price per extra or shortfall kilometre (see [Contract-Leasing](EN-Contract-Leasing)). The attribute `abweichung_ende` shows the deviation from the allowed kilometres before the tolerance is deducted.

## See also

- [Contract-End-and-Switching](EN-Contract-End-and-Switching): reminder, buttons and switching in detail
- [Payments-and-Costs](EN-Payments-and-Costs): instalment warning and recommended instalment
- [Sensor-Reference](EN-Sensor-Reference): all sensors and attributes
- [Contract-Leasing](EN-Contract-Leasing): kilometre rules for leasing
- [Dashboard-Examples](EN-Dashboard-Examples): cards for your dashboard
