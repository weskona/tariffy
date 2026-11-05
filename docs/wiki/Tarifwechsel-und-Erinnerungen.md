# Tarifwechsel und Erinnerungen

## Buttons pro Vertrag

| Button | Beschreibung |
|--------|-------------|
| Jetzt wechseln | Übernimmt den hinterlegten Folgetarif sofort (ohne auf das Datum zu warten) — friert den Verbrauch der endenden Laufzeit exakt wie beim automatischen Wechsel ein |
| Kündigung bestätigen | Quittiert die Erinnerung und entfernt die Dauerbenachrichtigung |
| Abschlag-Warnung bestätigen | Quittiert die Nachzahlungs-Warnung und entfernt die Dauerbenachrichtigung (meldet sich automatisch neu, falls sich die Prognose später wieder verschlechtert) |


## Tarifwechsel

Unter **Einstellungen → Integrationen → Tariffy → [Vertrag] → Optionen** kannst du einen Folgetarif hinterlegen:

- Wechseldatum, neuer Anbieter, Kundennummer, Tarifname
- Neue Preise und Verbrauchswerte

Am Wechseldatum übernimmt HA den neuen Tarif automatisch — geprüft täglich exakt um 00:00:01 Uhr, zusätzlich beim regulären 6h-Poll und beim HA-Start als Fallback. Nicht angegebene Felder behalten ihren aktuellen Wert.


## Kündigungs-Erinnerung

Wenn Vertragsende gesetzt und der Erinnerungszeitraum erreicht ist:

1. **Dauerbenachrichtigung** im HA-Benachrichtigungscenter
2. Einmalige **Push-Benachrichtigung** via konfiguriertem notify-Dienst
3. Button **„Kündigung bestätigen"** zum Quittieren


## Abschlag-Warnung (optional)

Pro Vertrag zuschaltbar (Strom/Gas/Wasser mit konfiguriertem Verbrauchssensor): warnt per Dauerbenachrichtigung (+ optional Push-Benachrichtigung), wenn die Prognose zum Vertragsende (`prognose_real`, siehe „Guthaben/Nachzahlung (Vertragsende)" oben) eine Nachzahlung über einer einstellbaren Schwelle erwarten lässt.

- **Aktivieren**: Checkbox „Warnen, wenn Abschlag zu niedrig ist" im Config-/Reconfigure-Flow des Vertrags. Standardmäßig aus.
- **Warnschwelle** (€ Nachzahlung, Default 50 €): Warnung feuert, wenn `prognose_real < -Schwelle`.
- **Quittieren**: Button „Abschlag-Warnung bestätigen" entfernt die Meldung für die aktuelle Episode. Verbessert sich die Prognose danach wieder über die Schwelle und verschlechtert sie sich später erneut, wird automatisch wieder gewarnt — kein dauerhaftes Stummschalten.
- Der Rohzustand (unabhängig vom Bestätigt-Status) steht als Attribut `abschlag_warnung_aktiv` am Sensor „Guthaben/Nachzahlung (Vertragsende)".
- Die Benachrichtigung nennt zusätzlich einen konkreten Empfehlungswert ("Abschlag auf ca. X €/Monat anpassen") aus dem Sensor „Abschlag (Anpassung empfohlen)", sofern berechenbar.

> **Keine rückwirkende Neuberechnung bei Abschlags-Änderung.** Erhöhst oder senkst du deinen Abschlag mitten im Vertrag, merkt sich Tariffy Datum und vorherigen Wert und wendet den alten Abschlag korrekt nur bis zu diesem Zeitpunkt an, den neuen erst danach — „Guthaben/Nachzahlung (Bisher)" und „Abschlag (Anpassung empfohlen)" springen nicht plötzlich so, als hätte der neue Abschlag schon seit Vertragsbeginn gegolten. Mehrere Korrekturen am selben Tag zählen als eine Änderung.
