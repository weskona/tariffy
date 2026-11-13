# Konfiguration

## Schritt 1 – Allgemeine Vertragsdaten (alle Sparten)

| Feld | Pflicht | Beschreibung |
|------|---------|-------------|
| Bezeichnung | ✅ | Anzeigename (z. B. „Strom Haus") |
| Sparte | ✅ | Strom, Strom (Zweizählertarif HT/NT), Gas, Wasser, Internet, Mobilfunk, Versicherung, Sonstiges |
| Anbieter | ✅ | Name des Anbieters |
| Kundennummer | – | Kundennummer beim Anbieter |
| Tarifname | – | Bezeichnung des Tarifs |
| Vertragsbeginn | – | Startdatum des Vertrags |
| Vertragsende | – | Enddatum / Laufzeit bis |
| Kündigung erinnern | ✅ | 0–4 Monate vorher (0 = deaktiviert) |
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

## Schritt 2d – Pauschalverträge (Internet, Mobilfunk, Versicherung, …)

**Zahlweise und Betrag:** Du wählst die **Zahlweise** (monatlich, vierteljährlich, halbjährlich, jährlich) und trägst den **Betrag pro Zahlung** ein; Tariffy rechnet intern mit dem Betrag pro Monat. Bei nicht monatlicher Zahlweise zählen die **Abbuchungen** zu den Kosten bisher; die erste nimmt Tariffy am Vertragsbeginn an, das echte Datum trägst du bei **Erste Abbuchung am** ein.

| Feld | Pflicht | Beschreibung |
|------|---------|-------------|
| Zahlweise | ✅ | monatlich, vierteljährlich, halbjährlich oder jährlich |
| Betrag pro Zahlung | ✅ | € pro Zahlung in der gewählten Zahlweise (zum Beispiel der Jahresbeitrag) |
| Erste Abbuchung am | – | Nur bei nicht monatlicher Zahlweise; leer = Vertragsbeginn |
| Grundpreis | – | €/Monat (falls separat ausgewiesen) |

**Versicherungen** haben vor den Kosten einen eigenen Schritt **Art der Versicherung** (Auto (Kfz), Gebäude / Haus, Hausrat, Haftpflicht, Kranken, Leben, Rechtsschutz, Unfall, Sonstige). **Nur bei einer Kfz-Versicherung** folgt danach ein Schritt mit Angaben zum Auto; alle anderen Arten gehen gleich weiter zu den Kosten. Alle Versicherungsangaben sind optional und dienen der Dokumentation, es wird nichts berechnet.

| Feld (nur Kfz) | Pflicht | Beschreibung |
|------|---------|-------------|
| Kennzeichen | – | Wie die Kundennummer persönlich: nicht im Seitenleisten-Panel sichtbar, im Diagnose-Download geschwärzt |
| Kilometerstand bei Vertragsbeginn | – | in km |
| Erlaubte Kilometer pro Jahr | – | in km |
