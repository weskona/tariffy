# Tariffy – Vertragsverwaltung für Home Assistant

Tariffy ist eine Home Assistant Custom Integration zur Verwaltung von Energie- und Dienstleistungsverträgen. Jeder Vertrag wird als eigenes HA-Gerät mit Sensoren angelegt. Tariffy erinnert an Kündigungsfristen, wechselt Tarife zum Stichtag und berechnet Kosten sowie Abrechnungsprognosen auf Basis echter Verbrauchsdaten.

**Seiten in diesem Wiki**

- [Installation](Installation)
- [Konfiguration](Konfiguration)
- [Sensoren](Sensoren)
- [Verbrauchsmessung](Verbrauchsmessung)
- [Tarifwechsel und Erinnerungen](Tarifwechsel-und-Erinnerungen)
- [Panel](Panel)
- [Fehlerbehebung](Fehlerbehebung)
- [English documentation](English)

Quellcode, Releases und Changelog: [weskona/tariffy](https://github.com/weskona/tariffy) · [Changelog](https://github.com/weskona/tariffy/blob/main/CHANGELOG.md) · [Fehler melden](https://github.com/weskona/tariffy/issues)

## Features

- **Sparten:** Strom, Gas, Wasser, Internet, Mobilfunk, Versicherung, Sonstiges
- **Echte Verbrauchsmessung** – beliebigen HA-Sensor als Zähler einbinden; Tariffy liest den Stand zum Vertragsbeginn aus den Long-Term Statistics und berechnet Verbrauch seit Vertragsbeginn sowie hochgerechneten Jahresverbrauch
- **Abrechnungsprognose (real)** – Prognose basierend auf dem tatsächlich gemessenen Verbrauch (Guthaben oder Nachzahlung)
- **Verbrauch letzte Vertragslaufzeit** – wird beim Tarifwechsel eingefroren; Basis für den empfohlenen Abschlag
- **Empfohlener Abschlag** – berechnet aus realem Verbrauch der letzten Laufzeit × aktuelle Preise
- **Automatischer Tarifwechsel** – Folgetarif hinterlegen, HA übernimmt ihn am Wechseldatum automatisch
- **Kündigungs-Erinnerung** – 1–4 Monate vor Vertragsende, Dauerbenachrichtigung + optionaler notify-Dienst, Bestätigen-Button
- **Gas-Umrechnung** – Jahresverbrauch in m³ wird automatisch via Brennwert & Zustandszahl in kWh umgerechnet
- **Wasser** – Frischwasser + Abwasser (Festpreis, % oder Monatspauschale)
- **Staffelpreise** – länderspezifisch (US, AU, ES, …)
- **Tag/Nacht-Tarif** – Economy 7, TOU (GB, US, AU, …)
- **Zweizählertarif (HT/NT)** – eigene Sparte für einen echten Zweiregister-Stromzähler (Hochtarif/Niedertarif): zweiter Arbeitspreis, zweiter Verbrauchssensor und zweite Zählernummer, unabhängig vom Hochtarif-Register erfasst. Die üblichen Sensoren (Kosten/Guthaben/Prognose Bisher) bleiben über beide Register kombiniert, per automatisch gewichtetem Durchschnittspreis; zusätzlich stehen eigene Verbrauchs-/Kosten-Sensoren pro Register zur Verfügung
- **Dynamischer Tarif (Spotpreis)** – externen HA-Sensor (Tibber, aWATTar, Nordpool, …) statt eines festen Arbeitspreises referenzieren; der effektive Preis wird als Statistik-Durchschnitt des Sensors über die bisherige Vertragslaufzeit + fester Aufschlag berechnet, mit automatischem Fallback auf den manuellen Preis solange keine Statistik-Historie vorliegt
- **Einspeisevergütung** – Vergütung pro eingespeister kWh (Photovoltaik)
- **Auto-Refresh nach HA-Start** – Sensoren aktualisieren sich automatisch sobald die Long-Term Statistics nach einem Neustart bereit sind
- **Prüfintervall** – alle 6 Stunden, zusätzlich täglich exakt um 00:00:01 Uhr für einen pünktlichen Tarifwechsel bei Datumswechsel
