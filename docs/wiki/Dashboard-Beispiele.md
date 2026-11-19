🇩🇪 Deutsch · [🇬🇧 English](EN-Dashboard-Examples)

# Dashboard-Beispiele

Das Tariffy-Panel zeigt alle Verträge fertig an. Wer einzelne Werte auf einem eigenen Home-Assistant-Dashboard haben möchte, nimmt dafür die Sensoren und Buttons der Integration. Diese Seite zeigt Beispiele für eine Entitäten-Karte, eine Markdown-Karte und Buttons.

**Inhalt:**
- [Vorbereitung: Entity-IDs finden](#vorbereitung-entity-ids-finden)
- [Entitäten-Karte](#entitäten-karte)
- [Entitäten-Karte mit Attributen](#entitäten-karte-mit-attributen)
- [Markdown-Karte](#markdown-karte)
- [Markdown-Karte mit PV-Autarkie](#markdown-karte-mit-pv-autarkie)
- [Buttons](#buttons)
- [Beispiel](#beispiel)
- [Siehe auch](#siehe-auch)

## Vorbereitung: Entity-IDs finden

**Alle Entity-IDs in den Beispielen sind Beispiele.** Sie heißen so, wie der Vertrag `Strom Haus` in einem deutschen Home Assistant. Deine IDs hängen vom Vertragsnamen und von der Sprache ab, in der die Entitäten angelegt wurden. Passe sie an:

1. Öffne in Home Assistant Einstellungen, Geräte & Dienste, Tariffy und dann das Gerät Deines Vertrags.
2. Klicke auf die Entität und dann auf das Zahnrad: Dort steht die **Entity-ID**.
3. Ersetze die IDs in den Beispielen durch Deine.

Welche Sensoren es für Deine Sparte gibt, steht in der [Sensoren-Referenz](Sensoren-Referenz). Eine ID, die es für Deinen Vertrag nicht gibt, zeigt die Karte als nicht verfügbar. Ein Sensor ohne Wert zeigt `unbekannt`.

## Entitäten-Karte

Die einfachste Karte listet die wichtigsten Sensoren eines Vertrags:

```yaml
type: entities
title: Strom Haus
entities:
  - entity: sensor.strom_haus_kosten_bisher
  - entity: sensor.strom_haus_guthaben_nachzahlung_bisher
  - entity: sensor.strom_haus_guthaben_nachzahlung_vertragsende
  - entity: sensor.strom_haus_abschlag_anpassung_empfohlen
  - entity: sensor.strom_haus_verbrauch_bisher
  - entity: sensor.strom_haus_restlaufzeit
```

Die Sensoren bringen ihre Einheit und ihr Symbol mit (Daumen hoch oder runter bei Guthaben und Nachzahlung). **Guthaben/Nachzahlung** ist positiv bei Guthaben und negativ bei Nachzahlung.

## Entitäten-Karte mit Attributen

Einzelne Attribute eines Sensors lassen sich mit Zeilen vom Typ `attribute` anzeigen. Die Namen der Attribute stehen in der [Sensoren-Referenz](Sensoren-Referenz):

```yaml
type: entities
title: Prognose Strom Haus
entities:
  - entity: sensor.strom_haus_guthaben_nachzahlung_vertragsende
    name: Prognose zum Vertragsende
  - type: attribute
    entity: sensor.strom_haus_guthaben_nachzahlung_vertragsende
    attribute: tendenz
    name: Tendenz
  - type: attribute
    entity: sensor.strom_haus_guthaben_nachzahlung_vertragsende
    attribute: verbrauch_hochgerechnet
    name: Verbrauch hochgerechnet
    suffix: kWh
  - type: attribute
    entity: sensor.strom_haus_abschlag_anpassung_empfohlen
    attribute: differenz
    name: Abstand zum Abschlag
```

- Das Attribut `tendenz` hat die Werte `Guthaben` und `Nachzahlung`.
- `verbrauch_hochgerechnet` ist in der Einheit des Verbrauchssensors. Bei Strom ist das kWh.
- `differenz` am Sensor **Abschlag (Anpassung empfohlen)** ist die empfohlene Anpassung minus Dein aktueller Abschlag.
- Das Attribut `arbeitspreis_aktuell` am Sensor **Arbeitspreis** hat nur bei einem dynamischen Tarif einen Wert.

## Markdown-Karte

Eine Markdown-Karte kann Werte und Attribute in einem Satz verbinden. Das Beispiel prüft vorher, ob der Sensor schon einen Wert hat:

```yaml
type: markdown
title: Strom Haus
content: >
  {% set kosten = 'sensor.strom_haus_kosten_bisher' %}
  {% set saldo = 'sensor.strom_haus_guthaben_nachzahlung_vertragsende' %}
  Kosten bisher: **{{ states(kosten) }} {{ state_attr(kosten, 'unit_of_measurement') }}**

  {% if states(saldo) not in ['unknown', 'unavailable'] %}
  Prognose zum Vertragsende: **{{ states(saldo) | float | round(2) }} {{ state_attr(saldo, 'unit_of_measurement') }}**
  ({{ state_attr(saldo, 'tendenz') }})
  {% else %}
  Die Prognose ist noch nicht verfügbar.
  {% endif %}
```

Mit den Zahlen aus den Beispieldaten des Panels (Vertrag Strom Haus, Stichtag 12.07.2026) steht auf der Karte ungefähr: Kosten bisher 513,54 EUR, Prognose zum Vertragsende −495,29 EUR (Nachzahlung).

## Markdown-Karte mit PV-Autarkie

Mit der [PV-Autarkie](PV-Autarkie) und einem Gesamtverbrauchs-Sensor hat der Sensor **Guthaben/Nachzahlung (Vertragsende)** weitere Attribute. Die Karte zeigt sie nur, wenn sie vorhanden sind:

```yaml
type: markdown
title: PV-Autarkie
content: >
  {% set s = 'sensor.strom_haus_guthaben_nachzahlung_vertragsende' %}
  {% if state_attr(s, 'verbrauch_gesamt_bisher') is not none %}
  Gesamtverbrauch bisher: {{ state_attr(s, 'verbrauch_gesamt_bisher') }} kWh

  Durch PV gedeckt: {{ state_attr(s, 'verbrauch_pv_gedeckt_bisher') }} kWh

  Autarkie bisher: {{ state_attr(s, 'autarkie_bisher') }} %

  Prognose ohne Autarkie: {{ state_attr(s, 'prognose_ohne_autarkie') }}
  {% else %}
  Keine Autarkie-Werte vorhanden.
  {% endif %}
```

Die Attribute gibt es nur, wenn die Autarkie die Prognose bestimmt. Die vier Werte zum Gesamtverbrauch gibt es nur mit einem Gesamtverbrauchs-Sensor.

## Buttons

Die Buttons eines Vertrags lassen sich in einer Entitäten-Karte als Zeilen mit einem Knopf zeigen:

```yaml
type: entities
title: Aktionen Strom Haus
entities:
  - entity: button.strom_haus_abschlag_warnung_bestaetigen
  - entity: button.strom_haus_kuendigung_bestaetigen
  - entity: button.strom_haus_jetzt_wechseln
```

Ein Button ist **nicht verfügbar**, solange seine Aktion keinen Sinn hat: **Jetzt wechseln** nur mit geplantem Folgevertrag, **Kündigung bestätigen** nur bei aktiver Erinnerung, **Abschlag-Warnung bestätigen** nur bei offener Warnung. Willst Du sie nur bei Bedarf sehen, packe die Karte in eine bedingte Karte (Typ `conditional`) mit der Bedingung, dass der Button nicht den Zustand `unavailable` hat.

## Beispiel

Ein Vertrag, drei Karten: Die Entitäten-Karte aus dem ersten Abschnitt zeigt mit den Beispieldaten (Strom Haus, 12.07.2026) diese Zeilen.

| Zeile | Wert |
|---|---|
| Kosten (Bisher) | 513,54 EUR |
| Guthaben/Nachzahlung (Bisher) | −206,24 EUR |
| Guthaben/Nachzahlung (Vertragsende) | −495,29 EUR |
| Abschlag (Anpassung empfohlen) | 127,66 EUR/Monat |
| Verbrauch (Bisher) | 1.481,17 kWh |
| Restlaufzeit | 172 Tage |

Die Nachzahlung wächst von −206 EUR heute auf −495 EUR zum Vertragsende. Der empfohlene Abschlag von 127,66 EUR gegenüber 40 EUR zeigt, wie viel höher der Abschlag sein müsste. Den Rechenweg zeigt [Abschlaege-und-Kosten](Abschlaege-und-Kosten).

> **Gut zu wissen:** Die Attribute `kundennummer` und `marktlokation` am Sensor **Arbeitspreis** sind persönliche Daten. Zeige sie auf einem Dashboard nur, wenn Du es willst, und denke daran, wenn Du Dashboards teilst.

## Siehe auch

- [Sensoren-Referenz](Sensoren-Referenz): alle Sensoren, Buttons und Attribute
- [Automationen](Automationen): Sensoren und Buttons in Automationen
- [Panel-Uebersicht](Panel-Uebersicht): das fertige Panel
- [PV-Autarkie](PV-Autarkie)
