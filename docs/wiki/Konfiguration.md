# Konfiguration

## Schritt 1 – Allgemeine Vertragsdaten (alle Sparten)

| Feld | Pflicht | Beschreibung |
|------|---------|-------------|
| Bezeichnung | ✅ | Anzeigename (z. B. „Strom Haus") |
| Sparte | ✅ | Strom, Strom (Zweizählertarif HT/NT), Gas, Wasser, Internet, Mobilfunk, Streaming, Kredit / Finanzierung, Leasing, Versicherung, Sonstiges |
| Anbieter | ✅ | Name des Anbieters |
| Kundennummer | – | Kundennummer beim Anbieter |
| Tarifname | – | Bezeichnung des Tarifs |
| Icon | – | Eigenes Icon des Vertrags, z. B. `mdi:car`. Gilt im Panel und für die Sensoren des Vertrags (Sensoren mit Statussymbol wie Guthaben/Nachzahlung behalten ihres). Leer = das Icon der Sparte. |
| Vertragsbeginn | – | Startdatum des Vertrags |
| Vertragsende | – | Enddatum / Laufzeit bis |
| Mindestlaufzeit (Monate) | – | Das Panel zeigt, bis wann der Vertrag mindestens läuft |
| Kündigungsfrist (Monate) | – | Wenn eingetragen, bezieht sich die Erinnerung auf den letzten Kündigungstag |
| Kündigung erinnern | ✅ | 0–4 Monate vorher (0 = deaktiviert); vor Vertragsende, mit Kündigungsfrist vor Ablauf der Frist |
| Benachrichtigungs-Ziel | – | notify-Dienst (z. B. `mobile_app_iphone`) |

## Schritt 2a – Strom-Details

| Feld | Pflicht | Beschreibung |
|------|---------|-------------|
| Arbeitspreis | ✅ | €/kWh – steht auf deiner Stromrechnung |
| Grundpreis | ✅ | €/Monat – monatlicher Festbetrag |
| Monatlicher Abschlag | ✅ | €/Monat – Vorauszahlung |
| Jahresverbrauch | – | kWh/Jahr – für die Kostenprognose |
| Verbrauchssensor | – | HA-Sensor des Stromzählers – für echte Verbrauchsmessung |
| Einspeisevergütung | – | €/kWh – Vergütung für eingespeisten Strom |
| Neukundenbonus | – | Einmaliger Bonus in € |
| Ökostrom | ✅ | Ja/Nein |
| Zählernummer | – | Für Dokumentation |
| Marktlokation (MaLo-ID) | – | Für Dokumentation |
| Preisgarantie bis | – | Datum |

## Schritt 2b – Gas-Details

Wie Strom, zusätzlich:

| Feld | Pflicht | Beschreibung |
|------|---------|-------------|
| Gaseinheit | ✅ | m³, CCF, therm, … |
| Jahresverbrauch | – | In der gewählten Einheit |
| Verbrauchssensor | – | HA-Sensor des Gaszählers |
| Brennwert | ✅ | kWh/m³ (ca. 10–12, steht auf der Gasrechnung) |
| Zustandszahl | ✅ | Umrechnungsfaktor Z (ca. 0,95, steht auf der Gasrechnung) |

> **Umrechnung:** kWh = m³ × Brennwert × Zustandszahl
>
> Brennwert und Zustandszahl akzeptieren sowohl Dezimalpunkt (`11.2`) als auch Dezimalkomma (`11,2`).

## Schritt 2c – Wasser-Details

| Feld | Pflicht | Beschreibung |
|------|---------|-------------|
| Wassereinheit | ✅ | m³, L, gal, … |
| Frischwasserpreis | ✅ | Preis pro Einheit |
| Grundpreis | ✅ | €/Monat |
| Monatlicher Abschlag | ✅ | €/Monat |
| Jahresverbrauch | – | Für die Kostenprognose |
| Verbrauchssensor | – | HA-Sensor des Wasserzählers |
| Abwasser-Typ | ✅ | Festpreis/Einheit, % des Frischwassers oder Monatspauschale |
| Abwassergebühr | – | Betrag je nach gewähltem Typ |
| Zählernummer | – | Für Dokumentation |

### Außenzähler (Garten, Pool, Bewässerung)

Bei einem **Wasservertrag** können im Tab **Verträge** des Panels (Block **Außenzähler**, nur Administratoren) bis zu zehn Außenzähler eingetragen werden. Wasser, das darüber läuft, fließt nicht in die Kanalisation. Je Zähler: **Name**, **Verbrauchssensor**, optional ein **Startwert** (Zählerstand am Vertragsbeginn, in der Einheit des Zählers) und optional ein **eigener Preis je Einheit** (sonst der Frischwasserpreis). Der Außenzähler gilt als Unterzähler, sein Verbrauch ist im Hauptzähler enthalten:

- **Abwasserpflichtiger Verbrauch = Hauptzähler − Summe der Außenzähler** (nie unter 0).
- Das Gartenwasser kostet Frischwasserpreis (oder den eigenen Preis), das übrige Wasser Frischwasser plus Abwasser. Die Kosten bisher, die Prognose und der empfohlene Abschlag rechnen mit dem daraus **gewichteten Preis** des Hauptzählers, wie beim Zweizählertarif.
- Ein Zähler in Litern wird in die Einheit des Hauptzählers umgerechnet.
- Für einen Vertrag mit Außenzähler gibt es vier zusätzliche Sensoren: **Gartenwasser (Verbrauch)**, **Gartenwasser (Kosten)**, **Abwasserpflichtiger Verbrauch**, **Abwasserkosten**. Die Gesamtkosten stehen wie immer in den Kosten-Sensoren. Ohne Außenzähler ändert sich nichts.


## Schritt 2d – Pauschalverträge (Internet, Mobilfunk, Streaming, Versicherung, …)

**Zahlweise und Betrag:** Du wählst die **Zahlweise** (monatlich, vierteljährlich, halbjährlich, jährlich) und trägst den **Betrag pro Zahlung** ein; Tariffy rechnet intern mit dem Betrag pro Monat. Zu den Kosten bisher zählen die **gebuchten Raten** (bei monatlicher Zahlung eine Rate ab dem ersten Tag ihres Monats); die erste nimmt Tariffy am Vertragsbeginn an, das echte Datum trägst du bei **Erste Abbuchung am** ein.

| Feld | Pflicht | Beschreibung |
|------|---------|-------------|
| Zahlweise | ✅ | monatlich, vierteljährlich, halbjährlich oder jährlich |
| Betrag pro Zahlung | ✅ | € pro Zahlung in der gewählten Zahlweise (zum Beispiel der Jahresbeitrag) |
| Erste Abbuchung am | – | Leer = Vertragsbeginn |
| Grundpreis | – | €/Monat (falls separat ausgewiesen) |

**Versicherungen** haben vor den Kosten einen eigenen Schritt **Art der Versicherung** (Auto (Kfz), Gebäude / Haus, Hausrat, Haftpflicht, Kranken, Leben, Rechtsschutz, Unfall, Sonstige). **Nur bei einer Kfz-Versicherung** folgt danach ein Schritt mit Angaben zum Auto; alle anderen Arten gehen gleich weiter zu den Kosten. Alle Versicherungsangaben sind optional und dienen der Dokumentation, es wird nichts berechnet.

| Feld (nur Kfz) | Pflicht | Beschreibung |
|------|---------|-------------|
| Kennzeichen | – | Wie die Kundennummer persönlich: nicht im Seitenleisten-Panel sichtbar, im Diagnose-Download geschwärzt |
| Kilometerstand bei Vertragsbeginn | – | in km |
| Erlaubte Kilometer pro Jahr | – | in km |

## Kredit / Finanzierung

Die Sparte **Kredit / Finanzierung** ist für Annuitätendarlehen (Baufinanzierung), Ratenkredite und Autofinanzierungen. Sie läuft **getrennt von den Verträgen**: Der Kredit hat im Panel eine eigene Gruppe und zählt nicht in die Summen der Verträge (Abschläge pro Monat, Kosten bisher, Kostenaufteilung). Nach dem allgemeinen Schritt folgt ein Schritt mit den Kreditdaten:

| Feld | Pflicht | Beschreibung |
|------|---------|-------------|
| Kreditsumme | ✅ | Der geliehene Betrag in € |
| Sollzins | – | % pro Jahr (nominal). Mit ihm rechnen die Banken die Rate. |
| Effektiver Jahreszins | – | %; zur Information und als Ersatz, wenn es keinen Sollzins gibt. **Einer der beiden Zinssätze ist nötig.** |
| Laufzeit | ✅ | Monate ab Vertragsbeginn. Das Vertragsende ergibt sich daraus. |
| Zahlweise | ✅ | monatlich, vierteljährlich, halbjährlich oder jährlich |
| Rate je Zahlung | – | Die Rate aus deinem Vertrag. **Leer = Tariffy rechnet die Annuität aus.** Passt die Rate nicht zum Zins (mehr als 1 % Abweichung), zeigt Tariffy die berechnete Rate und weist darauf hin. |
| Schlussrate / Restwert | – | Ein Betrag, der am Ende noch offen ist und mit der letzten Rate gezahlt wird (Autofinanzierung) |
| Datum der ersten Rate | – | Leer = ein Zahlungsintervall nach dem Beginn (bei monatlicher Zahlung: Ende des ersten Monats) |

**Berechnung:** Jede Rate besteht aus Zinsen auf die Restschuld und Tilgung; der Zinsanteil sinkt von Rate zu Rate. Der Zins je Zahlung ist der Sollzins geteilt durch die Zahlungen pro Jahr, ohne Sollzins wird er aus dem effektiven Jahreszins abgeleitet. Eine Rate zählt ab ihrem Datum. **Nicht enthalten:** Sondertilgungen und ein wechselnder Zins innerhalb der Laufzeit.

**Angezeigt** werden die **Restschuld**, **Gezahlt bisher** (Zinsen und Tilgung), die **Restsumme** (noch zu zahlen bis zum Ende), Zinsen bisher und über die Laufzeit, die gezahlten Raten, die nächste Rate mit der Aufteilung in Zins und Tilgung und der Fortschritt der Tilgung. Für jeden Kredit gibt es vier Sensoren: **Restschuld**, **Gezahlt bisher**, **Restsumme** und **Zinsen bisher**.

**Anschlussfinanzierung:** Im Tab **Verträge** hat der Kredit das Symbol **Vertrag verlängern**. Der Dialog schlägt die Restschuld als neue Summe vor, dazu Zins und Laufzeit; die bisherige Laufzeit kommt in die Historie. Ein Kredit hat kein Symbol für einen Folgevertrag.

## Leasing

Die Sparte **Leasing** ist für einen Auto-Leasingvertrag. Die Rate läuft wie jeder **Pauschalvertrag** (Rate, Beginn, Ende = Rückgabedatum, Erinnerung, Kündigungsfrist) und zählt in den Summen mit; im Panel steht der Vertrag in der Gruppe **Kredite / Finanzierungen**. Dazu behält Tariffy die **Kilometer** im Blick. Alle Angaben zu den Kilometern sind freiwillig.

| Feld | Pflicht | Beschreibung |
|------|---------|-------------|
| Kennzeichen | – | Gilt als persönlich: wird im Seitenpanel nicht angezeigt |
| Kilometerzähler-Sensor | – | Sensor des Fahrzeugs mit dem Kilometerstand in km (Meilen werden umgerechnet). Er hat Vorrang vor dem von Hand eingetragenen Wert. |
| Aktueller Kilometerstand | – | Nur wenn es keinen Sensor gibt: von Hand eintragen und ab und zu aktualisieren (Vertrag bearbeiten) |
| Kilometerstand bei Vertragsbeginn | – | Beginn des Leasings. Leer = 0 |
| Erlaubte Kilometer pro Jahr | – | Aus dem Vertrag |
| Erlaubte Kilometer über die ganze Laufzeit | – | Freiwillig. Leer = Kilometer pro Jahr mal Laufzeit. |
| Toleranz nach oben / unten | – | Mehrkilometer (Minderkilometer) bis zu diesem Wert werden nicht berechnet (gutgeschrieben) |
| Preis je Mehrkilometer / Gutschrift je Minderkilometer | – | In € pro km, für den erwarteten Saldo |

**Berechnung:** Die gefahrenen Kilometer sind der Kilometerstand minus der Stand bei Beginn. Das **Soll bis heute** ist die Erlaubnis, gleichmäßig auf die Laufzeit verteilt. Die **Hochrechnung bei Rückgabe** ist der bisherige Schnitt je Tag, bis zum Rückgabedatum fortgeschrieben (ab zwei Wochen Fahrt). `Abweichung = Hochrechnung − erlaubt`; **Mehrkilometer** sind, was die Toleranz nach oben übersteigt, **Minderkilometer**, was die Toleranz nach unten übersteigt. Mit den Preisen ergibt sich die **erwartete Nachzahlung oder Gutschrift** bei Rückgabe. Nach dem Rückgabedatum sind die gefahrenen Kilometer das Ergebnis.

**Angezeigt** wird in der Vertragskarte eine Zeile mit den gefahrenen Kilometern und was das Tempo bei Rückgabe bedeutet, in den Details ein Block **Leasing-Kilometer** (Kilometerstand, gefahren, erlaubt, Soll bis heute, noch übrig und erlaubt pro Tag ab jetzt, dein Schnitt, Hochrechnung, Mehr-/Minderkilometer und der erwartete Saldo). Ein Leasingvertrag hat drei weitere Sensoren: **Gefahrene Kilometer**, **Kilometer bei Rückgabe (Hochrechnung)**, **Erwartete Mehr-/Minderkilometer-Kosten**, dazu die Fahrzeug-Sensoren der Versicherung (Kennzeichen, Stand bei Beginn, erlaubt pro Jahr). Die Kilometerkosten zählen **nicht** in die Summen des Vertrags: Sie sind eine Schätzung für die Rückgabe.

**Gut zu wissen:** Ein **Tarifwechsel** oder ein geplanter Folgevertrag behält Fahrzeug, Sensor und Kilometerregeln; Kilometerstand bei Beginn und der von Hand eingetragene Wert gehören zur alten Laufzeit und entfallen. Bei **Vertrag verlängern** bleiben die Angaben, wie sie sind: Prüfe bei einem anderen Fahrzeug unter **Bearbeiten** den Stand bei Beginn und die Erlaubnis.
