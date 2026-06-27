# Tariffy – Vertragsverwaltung für Home Assistant

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz)
[![HA Version](https://img.shields.io/badge/Home%20Assistant-2024.11%2B-blue.svg)](https://www.home-assistant.io)
[![Version](https://img.shields.io/github/v/release/weskona/tariffy)](https://github.com/weskona/tariffy/releases)

---

## 🇩🇪 Deutsch

Tariffy ist eine Home Assistant Custom Integration zur Verwaltung von Energie- und Dienstleistungsverträgen. Strom, Gas, Internet, Mobilfunk, Versicherungen und mehr – alles als HA-Gerät mit Sensoren, automatischem Tarifwechsel und Kündigungs-Erinnerung.

### Features

- **Sparten:** Strom, Gas, Wasser, Internet, Mobilfunk, Versicherung, Sonstiges
- **Zweistufiger Konfigurationsflow** – sparten-abhängig (Energie, Gas, Pauschal)
- **Gas-Umrechnung** – m³ → kWh via Brennwert & Zustandszahl
- **Kosten-Sensoren** – Abschlag, geschätzte Jahreskosten, Abrechnungsprognose (Guthaben/Nachzahlung)
- **Automatischer Tarifwechsel** – Folgetarif hinterlegen, HA übernimmt ihn am Wechseldatum automatisch
- **Kündigungs-Erinnerung** – 1–4 Monate vorher, Dauerbenachrichtigung in HA + optionaler notify-Dienst, Bestätigen-Button
- **Ein Eintrag pro Vertrag** – jeder Vertrag wird als eigenes HA-Gerät angelegt

### Sensoren pro Vertrag

| Sensor | Beschreibung |
|--------|-------------|
| Arbeitspreis | €/kWh bzw. €/m³ (Energie) |
| Grundpreis | €/Monat (Energie) |
| Monatliche Kosten | Abschlag in €/Monat |
| Jahreskosten (Abschlag) | Abschlag × 12 |
| Geschätzte Jahreskosten | Verbrauch × Arbeitspreis + Grundpreis × 12 |
| Jahresverbrauch (kWh) | Umgerechneter Gas-Verbrauch (Gas) |
| Abrechnungsprognose | Abschlagssumme − geschätzte Kosten |
| Restlaufzeit | Tage bis Vertragsende |
| Vertragsende | Datum |
| Nächster Wechsel | Datum des geplanten Tarifwechsels |
| Kündigungs-Erinnerung | Datum ab dem erinnert wird |
| Anbieter, Tarif, Kundennummer, Zählernummer | Stammdaten |

### Installation via HACS

1. HACS → Integrationen → ⋮ → **Benutzerdefinierte Repositories**
2. URL: `https://github.com/weskona/tariffy` – Kategorie: **Integration**
3. Tariffy installieren → HA neu starten
4. Einstellungen → Integrationen → **Tariffy** → Hinzufügen

### Manuelle Installation

```bash
cp -r custom_components/tariffy /config/custom_components/
```
HA neu starten.

### Anforderungen

- Home Assistant 2024.11 oder neuer

---

## 🇬🇧 English

Tariffy is a Home Assistant custom integration for managing utility and service contracts. Electricity, gas, internet, mobile, insurance and more — each contract becomes a HA device with sensors, automatic tariff switching and cancellation reminders.

### Features

- **Categories:** Electricity, Gas, Water, Internet, Mobile, Insurance, Other
- **Two-step config flow** – category-dependent (Energy, Gas, Flat-rate)
- **Gas conversion** – m³ → kWh via calorific value & state number
- **Cost sensors** – monthly instalment, estimated annual cost, billing forecast (credit/surcharge)
- **Automatic tariff switch** – store the next tariff, HA promotes it automatically on the switch date
- **Cancellation reminder** – 1–4 months in advance, persistent notification in HA + optional notify service, confirm button
- **One entry per contract** – each contract is its own HA device

### Sensors per contract

| Sensor | Description |
|--------|-------------|
| Unit price | €/kWh or €/m³ (energy) |
| Base price | €/month (energy) |
| Monthly cost | Instalment in €/month |
| Annual cost (instalment) | Instalment × 12 |
| Estimated annual cost | Usage × unit price + base price × 12 |
| Annual usage (kWh) | Converted gas consumption (gas only) |
| Billing forecast | Instalment total − estimated cost |
| Remaining term | Days until contract end |
| Contract end | Date |
| Next switch | Date of planned tariff switch |
| Cancellation reminder | Date from which reminder is active |
| Provider, Tariff, Customer no., Meter no. | Master data |

### Installation via HACS

1. HACS → Integrations → ⋮ → **Custom repositories**
2. URL: `https://github.com/weskona/tariffy` – Category: **Integration**
3. Install Tariffy → restart HA
4. Settings → Integrations → **Tariffy** → Add

### Manual installation

```bash
cp -r custom_components/tariffy /config/custom_components/
```
Restart HA.

### Requirements

- Home Assistant 2024.11 or newer

---

## Lizenz / License

MIT © [weskona](https://github.com/weskona)
