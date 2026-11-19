🇩🇪 Deutsch · [🇬🇧 English](EN-Automations)

# Automationen

Tariffy erinnert und warnt schon selbst mit Benachrichtigungen. Mit Automationen kannst Du das erweitern: eine zweite Meldung auf einem anderen Kanal, eine tägliche Wiederholung oder eine eigene Schwelle. Diese Seite bringt vier fertige Beispiele zum Anpassen.

**Inhalt:**

- [Bevor Du loslegst](#bevor-du-loslegst)
- [Kündigungs-Erinnerung](#kündigungs-erinnerung)
- [Abschlag-Warnung](#abschlag-warnung)
- [Nachzahlung droht](#nachzahlung-droht)
- [Leasing: Kilometer-Warnung](#leasing-kilometer-warnung)

## Bevor Du loslegst

> **Wichtig:** Die Beispiele sind **aus dem Code der Integration geschrieben**, nicht an einem laufenden Home Assistant ausprobiert. Die Entitäten-IDs sind **Beispiele** und musst Du anpassen. Prüfe jede Automation mit **Ausführen** oder im Entwicklerwerkzeug **Vorlage**, bevor Du Dich darauf verlässt.

**Entitäten-IDs finden:** Jede Entität bekommt ihre ID aus dem Vertragsnamen und dem Sensornamen, in der Sprache, in der Home Assistant beim Anlegen lief. Für einen Vertrag „Strom Haus" könnten sie so aussehen. Kopiere die echte ID unter **Einstellungen → Geräte & Dienste → Entitäten**.

| Sensor | Beispiel-ID | Was die Beispiele nutzen |
|--------|-------------|--------------------------|
| Kündigungs-Erinnerung | `sensor.strom_haus_kundigungs_erinnerung` | Wert: Erinnerungsdatum als Text (TT.MM.JJJJ); Attribute `aktiv`, `bestaetigt`, `monate_vorher`, `kuendigungsfrist_monate`, `kuendigung_bis` |
| Guthaben/Nachzahlung (Vertragsende) | `sensor.strom_haus_guthaben_nachzahlung_vertragsende` | Wert: Prognose in €, negativ ist Nachzahlung; Attribut `abschlag_warnung_aktiv` |
| Abschlag (Anpassung empfohlen) | `sensor.strom_haus_abschlag_anpassung_empfohlen` | Wert: empfohlener Abschlag pro Monat; Attribute `aktueller_abschlag`, `differenz` |
| Kilometer bei Rückgabe (Hochrechnung) | `sensor.auto_leasing_kilometer_bei_ruckgabe_hochrechnung` | Attribute `mehr_km`, `minder_km`, `abweichung_ende` |
| Erwartete Mehr-/Minderkilometer-Kosten | `sensor.auto_leasing_erwartete_mehr_minderkilometer_kosten` | Wert: erwartete Kosten in €; Attribute `nachzahlung`, `gutschrift` |

Die Buttons heißen „Jetzt wechseln", „Kündigung bestätigen" und „Abschlag-Warnung bestätigen" (siehe [Vertragsende-und-Wechsel](Vertragsende-und-Wechsel)). Tariffy löst **keine eigenen Ereignisse** aus; die Beispiele arbeiten deshalb mit den Zuständen und Attributen der Sensoren. Die eingebauten Meldungen im Benachrichtigungscenter haben die Kennungen `tariffy_kuendigung_<entry_id>` und `tariffy_abschlag_warnung_<entry_id>`.

Die Beispiele nutzen die Schreibweise ab Home Assistant 2024.10 (`triggers`, `actions`, `trigger:`, `action:`). Tariffy braucht ohnehin Home Assistant 2025.8 oder neuer. `notify.mobile_app_dein_handy` ist ein Platzhalter für Deinen eigenen notify-Dienst.

## Kündigungs-Erinnerung

Die eingebaute Erinnerung meldet sich einmal per Dauerbenachrichtigung und einmal per Push an das Benachrichtigungs-Ziel des Vertrags. Diese Automation wiederholt die Meldung **jeden Morgen um 9 Uhr**, solange die Erinnerung aktiv ist, und meldet sie zusätzlich sofort, wenn sie beginnt. Sie hört von selbst auf, sobald Du **Kündigung bestätigen** drückst, denn das Attribut `aktiv` wird dann `false`, und sobald das Vertragsende vorbei ist.

```yaml
alias: Tariffy Strom Haus - Kündigung erinnern
description: Meldet die Kündigungs-Erinnerung sofort und danach täglich um 9 Uhr, bis sie bestätigt ist.
mode: single
triggers:
  - trigger: state
    entity_id: sensor.strom_haus_kundigungs_erinnerung
    attribute: aktiv
    to: true
  - trigger: time
    at: "09:00:00"
conditions:
  - condition: template
    value_template: >-
      {{ state_attr('sensor.strom_haus_kundigungs_erinnerung', 'aktiv') == true }}
actions:
  - action: notify.mobile_app_dein_handy
    data:
      title: "Strom Haus: Kündigung nicht vergessen"
      message: >-
        Letzter Kündigungstag:
        {{ state_attr('sensor.strom_haus_kundigungs_erinnerung', 'kuendigung_bis')
           or 'keine Kündigungsfrist hinterlegt, siehe Vertragsende' }}.
        Danach im Panel oder am Gerät auf "Kündigung bestätigen" drücken.
```

Das Attribut `kuendigung_bis` ist nur gefüllt, wenn beim Vertrag eine Kündigungsfrist eingetragen ist und ein Vertragsende gesetzt ist; sonst ist es leer, und die Vorlage nimmt den Ersatztext.

> **Gut zu wissen:** Trägst Du beim Vertrag ein Benachrichtigungs-Ziel ein, schickt Tariffy zusätzlich seine eigene Push-Meldung. Willst Du nur die Meldung der Automation, lass das Ziel im Vertrag leer.

## Abschlag-Warnung

Ist beim Vertrag die Option „Warnen, wenn Abschlag zu niedrig ist" an (Strom, Gas, Wasser mit Verbrauchssensor), setzt Tariffy das Attribut `abschlag_warnung_aktiv` auf `true`, wenn die Prognose zum Vertragsende eine Nachzahlung über der Warnschwelle (Standard 50 €) erwarten lässt. Das Attribut bleibt auch nach dem Quittieren `true`, solange die Prognose schlecht ist; es zeigt den Rohzustand. Die Automation löst deshalb nur aus, wenn die Warnung **neu entsteht**, und nennt den empfohlenen Abschlag.

```yaml
alias: Tariffy Strom Haus - Abschlag zu niedrig
description: Meldet, wenn Tariffy eine Nachzahlung erwartet, und nennt den empfohlenen Abschlag.
mode: single
triggers:
  - trigger: state
    entity_id: sensor.strom_haus_guthaben_nachzahlung_vertragsende
    attribute: abschlag_warnung_aktiv
    to: true
actions:
  - action: notify.mobile_app_dein_handy
    data:
      title: "Strom Haus: Abschlag zu niedrig"
      message: >-
        Zum Vertragsende droht eine Nachzahlung von etwa
        {{ states('sensor.strom_haus_guthaben_nachzahlung_vertragsende') | float(0) | abs | round(2) }} €.
        {% set empfohlen = states('sensor.strom_haus_abschlag_anpassung_empfohlen') %}
        {% if empfohlen | is_number %}
        Empfohlener Abschlag: {{ empfohlen | float | round(2) }} € pro Monat.
        {% endif %}
```

## Nachzahlung droht

Diese Automation braucht die Option „Warnen, wenn Abschlag zu niedrig ist" nicht, sondern prüft die Prognose selbst gegen Deine eigene Schwelle. Sie meldet, wenn die Prognose zum Vertragsende **30 Minuten lang** schlechter als −100 € ist. Die Wartezeit verhindert Meldungen bei kurzem Schwanken.

```yaml
alias: Tariffy Strom Haus - Nachzahlung über 100 Euro
description: Eigene Schwelle für die Prognose zum Vertragsende.
mode: single
triggers:
  - trigger: numeric_state
    entity_id: sensor.strom_haus_guthaben_nachzahlung_vertragsende
    below: -100
    for: "00:30:00"
actions:
  - action: notify.mobile_app_dein_handy
    data:
      title: "Strom Haus: Nachzahlung droht"
      message: >-
        Prognose zum Vertragsende:
        {{ states('sensor.strom_haus_guthaben_nachzahlung_vertragsende') | float(0) | round(2) }} €
        (negativ ist Nachzahlung).
```

Beispiel mit Zahlen (ausgedacht): Steht der Sensor auf −137,50, kommt die Meldung „Prognose zum Vertragsende: -137.5 € (negativ ist Nachzahlung)." (In Vorlagen schreibt Home Assistant Dezimalpunkte.) Fällt der Wert vor Ablauf der 30 Minuten wieder über −100, kommt keine Meldung.

> **Gut zu wissen:** Die Automation löst nur aus, wenn der Wert die Schwelle neu unterschreitet. War er schon darunter, als Du sie anlegst, meldet sie sich erst, wenn er zwischendurch wieder darüber lag.

## Leasing: Kilometer-Warnung

Bei einem Leasingvertrag mit Kilometerstand und erlaubten Kilometern rechnet Tariffy hoch, wie viele Kilometer Du bei der Rückgabe haben wirst. Der Sensor „Kilometer bei Rückgabe (Hochrechnung)" hat das Attribut `mehr_km`: die Mehrkilometer **nach Abzug der Toleranz**. Die Hochrechnung gibt es erst, wenn der Vertrag mindestens 14 Tage läuft; vorher ist das Attribut leer. Die Automation meldet, sobald `mehr_km` über 0 steigt.

```yaml
alias: Tariffy Leasing - Mehrkilometer drohen
description: Meldet, wenn die Hochrechnung Mehrkilometer über der Toleranz zeigt.
mode: single
triggers:
  - trigger: numeric_state
    entity_id: sensor.auto_leasing_kilometer_bei_ruckgabe_hochrechnung
    attribute: mehr_km
    above: 0
actions:
  - action: notify.mobile_app_dein_handy
    data:
      title: "Leasing: Mehrkilometer drohen"
      message: >-
        Hochrechnung bei Rückgabe:
        {{ states('sensor.auto_leasing_kilometer_bei_ruckgabe_hochrechnung') | float(0) | round(0) }} km.
        Mehrkilometer nach Toleranz:
        {{ state_attr('sensor.auto_leasing_kilometer_bei_ruckgabe_hochrechnung', 'mehr_km') }} km.
        {% set kosten = states('sensor.auto_leasing_erwartete_mehr_minderkilometer_kosten') %}
        {% if kosten | is_number %}
        Erwartete Kosten: {{ kosten | float | round(2) }} €.
        {% endif %}
```

Die erwarteten Kosten gibt es nur, wenn beim Vertrag ein Preis je Mehr- oder Minderkilometer eingetragen ist (siehe [Vertrag-Leasing](Vertrag-Leasing)). Das Attribut `abweichung_ende` zeigt die Abweichung zu den erlaubten Kilometern vor Abzug der Toleranz.

## Siehe auch

- [Vertragsende-und-Wechsel](Vertragsende-und-Wechsel): Erinnerung, Buttons und Wechsel im Detail
- [Abschlaege-und-Kosten](Abschlaege-und-Kosten): Abschlag-Warnung und empfohlener Abschlag
- [Sensoren-Referenz](Sensoren-Referenz): Alle Sensoren und Attribute
- [Vertrag-Leasing](Vertrag-Leasing): Kilometerregeln beim Leasing
- [Dashboard-Beispiele](Dashboard-Beispiele): Karten für Dein Dashboard
