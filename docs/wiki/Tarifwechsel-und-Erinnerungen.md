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

**Mit Kündigungsfrist:** Trägst du beim Vertrag eine **Kündigungsfrist** (in Monaten) ein, bezieht sich die Erinnerung auf den **letzten Kündigungstag** (Vertragsende minus Frist) statt auf das Vertragsende. Beispiel: Vertragsende 31.12., Kündigungsfrist 3 Monate, Erinnerung „3 Monate vorher": Die Kündigung muss bis 30.09. vorliegen, die Meldung kommt am 30.06., also 6 Monate vor dem Vertragsende. Die Meldung nennt den letzten Kündigungstag. Ohne Kündigungsfrist ändert sich nichts. Die **Mindestlaufzeit** (in Monaten) zeigt das Panel als „bis <Beginn + Mindestlaufzeit>"; sie beeinflusst keine Erinnerung. Beide Felder sind freiwillig; der Sensor „Kündigungs-Erinnerung" hat dazu die Attribute `kuendigungsfrist_monate` und `kuendigung_bis`. Bei einem Tarifwechsel bleibt die Kündigungsfrist erhalten, die Mindestlaufzeit nicht.


## PV-Autarkie in der Prognose (optional)

Mit einer PV-Anlage (auch mit Batterie) schwankt der Netzbezug mit der Jahreszeit: Wer im Winter beobachtet, überschätzt die Restlaufzeit, wer im Sommer beobachtet, unterschätzt sie. Bei einem **Stromvertrag** (auch Zweizählertarif) lässt sich die **PV-Autarkie** berücksichtigen. Sie gilt **nur für die Restlaufzeit**; der bisherige Verbrauch bleibt unverändert. Sie fließt in die **Prognose zum Vertragsende**, den **empfohlenen Abschlag** und den hochgerechneten Verbrauch ein. **Standardmäßig aus; ohne die Option ändert sich nichts.**

**Einrichtung:** Im Vertragsformular **PV-Autarkie in der Prognose berücksichtigen** einschalten und die Quelle der Autarkie angeben. Es gibt drei, die in dieser Reihenfolge gelten: **(1) Gesamtverbrauch des Hauses** als Sensor (kWh, mit Langzeitstatistik, zum Beispiel der Hausverbrauch aus dem Energie-Dashboard; die genaueste Quelle, weil sie auf Energiesummen beruht und mit Batterie funktioniert), **(2) ein Autarkie-Sensor in %** (mit Statistik, zum Beispiel die Autarkie der Fronius-Integration; es wird der **Monatsmittelwert** des Vorjahres genommen) oder **(3) eigene Werte in %**: ein Wert für alle Monate oder zwölf Werte für Januar bis Dezember, getrennt durch Leerzeichen oder Semikolon (zum Beispiel `10 10 25 50 70 80 85 80 60 35 15 10`). Eigene Werte gelten auch für Monate, für die die Statistik fehlt, und reichen allein (zum Beispiel im ersten Jahr einer PV-Anlage ohne Historie). Der **Verbrauchssensor des Vertrags muss den Netzbezug messen**. Beim Zweizählertarif gibt es zu (1) optional einen zweiten Gesamtverbrauchs-Sensor für die Niedertarif-Zeit; ohne ihn wird die Autarkie über beide Tarife zusammen berechnet und auf beide angewendet (eine Näherung, im Attribut `autarkie_naeherung` gekennzeichnet). Ein Autarkie-Sensor (2) und eigene Werte (3) gelten für beide Tarife gleich.

**Berechnung:** Für jeden Monat der Restlaufzeit wird der **gleiche Monat des Vorjahres** genommen: bei (1) aus den Langzeitstatistiken `Autarkie = 1 − Netzbezug / Gesamtverbrauch`, bei (2) der Monatsmittelwert des Sensors, bei (3) der eigene Wert; auf 0 bis 100 % begrenzt. Fehlt der Wert für einen Monat, gilt für diesen Monat der eigene Wert (3), sonst keine Anpassung. Die Autarkie im gemessenen Zeitraum kommt aus derselben Quelle (bei (3) aus den eigenen Werten der bereits gemessenen Monate, nach Tagen gewichtet). Da der Verbrauchssensor schon den Netzbezug misst, steckt die Autarkie in den bisherigen Messwerten; der tägliche Netzbezug wird deshalb **saisonal normalisiert**: `Netzbezug des Monats = Netzbezug je Tag bisher × Tage × (1 − Autarkie des Monats) / (1 − Autarkie bisher)`. Beim Zweizählertarif wird je Tarif gerechnet. Fehlen die Daten für einen Monat (oder für den gemessenen Zeitraum), bleibt es für diesen Monat bei der linearen Hochrechnung; fehlt jede Historie, ändert sich nichts und es gibt keinen Fehler.

**Anzeige:** Der Sensor **Guthaben/Nachzahlung (Vertragsende)** bekommt (nur wenn die Autarkie die Prognose bestimmt) die Attribute `autarkie_variante`, `autarkie_monatswerte` (je Monat Autarkie in % und Faktor, beim Zweizählertarif auch für den Niedertarif), `autarkie_bisher`, `autarkie_naeherung` und `prognose_ohne_autarkie`. Das Panel zeigt in den Vertragsdetails die Prognose ohne Autarkie und die Autarkie bisher. Das Attribut `autarkie_variante` nennt die Quelle (`gesamtverbrauch`, `entitaet` oder `manuell`), in `autarkie_monatswerte` steht je Monat, ob der Wert aus der Statistik oder von dir kam. **Nicht enthalten:** ein Verbrauchssensor, der den Gesamtverbrauch statt des Netzbezugs misst.

## Abschlag-Warnung (optional)

Pro Vertrag zuschaltbar (Strom/Gas/Wasser mit konfiguriertem Verbrauchssensor): warnt per Dauerbenachrichtigung (+ optional Push-Benachrichtigung), wenn die Prognose zum Vertragsende (`prognose_real`, siehe „Guthaben/Nachzahlung (Vertragsende)" oben) eine Nachzahlung über einer einstellbaren Schwelle erwarten lässt.

- **Aktivieren**: Checkbox „Warnen, wenn Abschlag zu niedrig ist" im Config-/Reconfigure-Flow des Vertrags. Standardmäßig aus.
- **Warnschwelle** (€ Nachzahlung, Default 50 €): Warnung feuert, wenn `prognose_real < -Schwelle`.
- **Quittieren**: Button „Abschlag-Warnung bestätigen" entfernt die Meldung für die aktuelle Episode. Verbessert sich die Prognose danach wieder über die Schwelle und verschlechtert sie sich später erneut, wird automatisch wieder gewarnt — kein dauerhaftes Stummschalten.
- Der Rohzustand (unabhängig vom Bestätigt-Status) steht als Attribut `abschlag_warnung_aktiv` am Sensor „Guthaben/Nachzahlung (Vertragsende)".
- Die Benachrichtigung nennt zusätzlich einen konkreten Empfehlungswert ("Abschlag auf ca. X €/Monat anpassen") aus dem Sensor „Abschlag (Anpassung empfohlen)", sofern berechenbar.

> **Keine rückwirkende Neuberechnung bei Abschlags-Änderung.** Erhöhst oder senkst du deinen Abschlag mitten im Vertrag, merkt sich Tariffy Datum und vorherigen Wert und wendet den alten Abschlag korrekt nur bis zu diesem Zeitpunkt an, den neuen erst danach — „Guthaben/Nachzahlung (Bisher)" und „Abschlag (Anpassung empfohlen)" springen nicht plötzlich so, als hätte der neue Abschlag schon seit Vertragsbeginn gegolten. Mehrere Korrekturen am selben Tag zählen als eine Änderung.
