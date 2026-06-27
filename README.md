# Tariffy – Contract Management for Home Assistant

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz)
[![HA Version](https://img.shields.io/badge/Home%20Assistant-2026.6%2B-blue.svg)](https://www.home-assistant.io)
[![Version](https://img.shields.io/github/v/release/weskona/tariffy)](https://github.com/weskona/tariffy/releases)

**[🇩🇪 Deutsche Version](#-deutsch)**

---

## 🇬🇧 English

Tariffy is a Home Assistant custom integration for managing utility and service contracts. Electricity, gas, water, internet, mobile, insurance and more — each contract becomes its own HA device with dedicated sensors. Tariffy automatically reminds you of cancellation deadlines, switches tariffs on the switch date, and calculates costs and billing forecasts.

---

### Features

- **Categories:** Electricity, Gas, Water, Internet, Mobile, Insurance, Other
- **Two-step config flow** – category-dependent (Energy, Gas, Flat-rate)
- **Gas conversion** – annual consumption in m³ is automatically converted to kWh via calorific value & state number
- **Cost sensors** – monthly instalment, estimated annual cost, billing forecast (credit or surcharge)
- **Automatic tariff switch** – store the next tariff, HA promotes it automatically on the switch date
- **Cancellation reminder** – 1–4 months before contract end, persistent notification in HA + optional notify service, confirm button
- **Check interval** – every 6 hours Tariffy checks whether a switch date or cancellation deadline has been reached
- **One entry per contract** – each contract is its own HA device with dedicated sensors and buttons

---

### Configuration

#### Step 1 – General contract data (all categories)

| Field | Required | Description |
|-------|----------|-------------|
| Label | ✅ | Display name of the device (e.g. "Electricity House") |
| Category | ✅ | Electricity, Gas, Water, Internet, Mobile, Insurance, Other |
| Provider | ✅ | Name of the provider |
| Customer number | – | Customer number with the provider |
| Tariff name | – | Name of the tariff |
| Contract start | – | Start date of the contract |
| Contract end | – | End date / valid until |
| Cancellation reminder | ✅ | 0–4 months before contract end (0 = disabled) |
| Notification target | – | notify service for push notification (e.g. `mobile_app_iphone`) |

#### Step 2a – Electricity details

| Field | Required | Description |
|-------|----------|-------------|
| Unit price | ✅ | €/kWh |
| Base price | ✅ | €/month |
| Monthly instalment | ✅ | €/month |
| Annual usage | – | kWh/year |
| Sign-up bonus | – | One-time bonus in € |
| Green energy | ✅ | Yes/No |
| Meter number | – | For documentation |
| Market location (MaLo) | – | For documentation |
| Price guarantee until | – | Date |

#### Step 2b – Gas details

Same as electricity, plus:

| Field | Required | Description |
|-------|----------|-------------|
| Annual usage | – | **m³**/year (automatically converted to kWh) |
| Calorific value | ✅ | kWh/m³ (shown on your gas bill, approx. 10–12) |
| State number | ✅ | Conversion factor (shown on your gas bill, approx. 0.95) |

> **Conversion:** kWh = m³ × calorific value × state number

#### Step 2c – Flat-rate contracts (Internet, Mobile, Insurance, …)

| Field | Required | Description |
|-------|----------|-------------|
| Monthly instalment | ✅ | €/month |
| Base price | – | €/month (if separate) |

---

### Sensors per contract

| Sensor | Unit | Category | Description |
|--------|------|----------|-------------|
| Unit price | €/kWh or €/m³ | Energy | Consumption-based price |
| Base price | €/month | Energy | Monthly base fee |
| Monthly cost | €/month | All | Monthly instalment |
| Annual cost (instalment) | €/year | All | Instalment × 12 |
| Estimated annual cost | €/year | Energy | Usage × unit price + base price × 12 |
| Annual usage (kWh) | kWh | Gas | m³ converted via calorific value & state number |
| Billing forecast | € | Energy | Instalment total − estimated cost (positive = credit, negative = surcharge) |
| Remaining term | Days | All | Days until contract end |
| Contract end | Date | All | End of current contract |
| Cancellation reminder | Date | All | Date from which the reminder is active |
| Next switch | Date | All | Date of planned tariff switch |
| Provider | – | All | Provider name |
| Tariff | – | All | Tariff name |
| Customer number | – | All | Customer number (diagnostic) |
| Meter number | – | Energy | Meter number (diagnostic) |

---

### Buttons per contract

| Button | Description |
|--------|-------------|
| Switch now | Immediately applies the stored next tariff (without waiting for the switch date) |
| Confirm cancellation | Acknowledges the cancellation reminder and removes the persistent notification |

---

### Tariff switch

Under **Settings → Integrations → Tariffy → [Contract] → Options** you can store a follow-up tariff:

- Switch date (start of new contract)
- New provider, customer number, tariff name
- New prices and consumption values

On the switch date HA automatically applies the new tariff. All sensors update immediately. Fields not specified (e.g. meter number) retain their current value.

---

### Cancellation reminder

When a contract end date is set and the reminder period (1–4 months) is reached:

1. A **persistent notification** appears in the HA notification center and stays until confirmed
2. Optionally a one-time **push notification** is sent via the configured notify service
3. The **"Confirm cancellation"** button becomes active — press it to acknowledge the reminder

> **Check interval:** Tariffy checks every **6 hours** whether a switch date or cancellation deadline has been reached.

---

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

- Home Assistant 2026.6 or newer

---

## 🇩🇪 Deutsch

Tariffy ist eine Home Assistant Custom Integration zur Verwaltung von Energie- und Dienstleistungsverträgen. Strom, Gas, Wasser, Internet, Mobilfunk, Versicherungen und mehr – jeder Vertrag wird als eigenes HA-Gerät mit Sensoren angelegt. Tariffy erinnert automatisch an Kündigungsfristen, wechselt Tarife zum Stichtag und berechnet Kosten und Abrechnungsprognosen.

---

### Features

- **Sparten:** Strom, Gas, Wasser, Internet, Mobilfunk, Versicherung, Sonstiges
- **Zweistufiger Konfigurationsflow** – sparten-abhängig (Energie, Gas, Pauschal)
- **Gas-Umrechnung** – Jahresverbrauch in m³ wird automatisch via Brennwert & Zustandszahl in kWh umgerechnet
- **Kosten-Sensoren** – Abschlag, geschätzte Jahreskosten, Abrechnungsprognose (Guthaben oder Nachzahlung)
- **Automatischer Tarifwechsel** – Folgetarif hinterlegen, HA übernimmt ihn am Wechseldatum automatisch
- **Kündigungs-Erinnerung** – 1–4 Monate vor Vertragsende, Dauerbenachrichtigung + optionaler notify-Dienst, Bestätigen-Button
- **Prüfintervall** – alle 6 Stunden wird geprüft ob ein Wechseldatum oder Kündigungsfrist erreicht wurde
- **Ein Eintrag pro Vertrag** – jeder Vertrag ist ein eigenes HA-Gerät

---

### Konfiguration

#### Schritt 1 – Allgemeine Vertragsdaten (alle Sparten)

| Feld | Pflicht | Beschreibung |
|------|---------|-------------|
| Bezeichnung | ✅ | Anzeigename (z. B. „Strom Haus") |
| Sparte | ✅ | Strom, Gas, Wasser, Internet, Mobilfunk, Versicherung, Sonstiges |
| Anbieter | ✅ | Name des Anbieters |
| Kundennummer | – | Kundennummer beim Anbieter |
| Tarifname | – | Bezeichnung des Tarifs |
| Vertragsbeginn | – | Startdatum |
| Vertragsende | – | Enddatum / Laufzeit bis |
| Kündigung erinnern | ✅ | 0–4 Monate vorher (0 = deaktiviert) |
| Benachrichtigungs-Ziel | – | notify-Dienst (z. B. `mobile_app_iphone`) |

#### Schritt 2a – Strom-Details

| Feld | Pflicht | Beschreibung |
|------|---------|-------------|
| Arbeitspreis | ✅ | €/kWh |
| Grundpreis | ✅ | €/Monat |
| Monatlicher Abschlag | ✅ | €/Monat |
| Jahresverbrauch | – | kWh/Jahr |
| Neukundenbonus | – | Einmaliger Bonus in € |
| Ökostrom | ✅ | Ja/Nein |
| Zählernummer | – | Für Dokumentation |
| Marktlokation (MaLo-ID) | – | Für Dokumentation |
| Preisgarantie bis | – | Datum |

#### Schritt 2b – Gas-Details

Wie Strom, zusätzlich:

| Feld | Pflicht | Beschreibung |
|------|---------|-------------|
| Jahresverbrauch | – | **m³**/Jahr (wird automatisch in kWh umgerechnet) |
| Brennwert | ✅ | kWh/m³ (ca. 10–12, steht auf der Gasrechnung) |
| Zustandszahl | ✅ | Umrechnungsfaktor (ca. 0,95, steht auf der Gasrechnung) |

> **Umrechnung:** kWh = m³ × Brennwert × Zustandszahl

#### Schritt 2c – Pauschalverträge (Internet, Mobilfunk, Versicherung, …)

| Feld | Pflicht | Beschreibung |
|------|---------|-------------|
| Monatlicher Abschlag | ✅ | €/Monat |
| Grundpreis | – | €/Monat (falls separat) |

---

### Sensoren pro Vertrag

| Sensor | Einheit | Sparte | Beschreibung |
|--------|---------|--------|-------------|
| Arbeitspreis | €/kWh bzw. €/m³ | Energie | Verbrauchsabhängiger Preis |
| Grundpreis | €/Monat | Energie | Monatliche Grundgebühr |
| Monatliche Kosten | €/Monat | Alle | Monatlicher Abschlag |
| Jahreskosten (Abschlag) | €/Jahr | Alle | Abschlag × 12 |
| Geschätzte Jahreskosten | €/Jahr | Energie | Verbrauch × Arbeitspreis + Grundpreis × 12 |
| Jahresverbrauch (kWh) | kWh | Gas | m³ umgerechnet via Brennwert & Zustandszahl |
| Abrechnungsprognose | € | Energie | Abschlagssumme − geschätzte Kosten |
| Restlaufzeit | Tage | Alle | Tage bis Vertragsende |
| Vertragsende | Datum | Alle | Ende des aktuellen Vertrags |
| Kündigungs-Erinnerung | Datum | Alle | Datum ab dem erinnert wird |
| Nächster Wechsel | Datum | Alle | Datum des geplanten Tarifwechsels |
| Anbieter | – | Alle | Name des Anbieters |
| Tarif | – | Alle | Tarifbezeichnung |
| Kundennummer | – | Alle | Kundennummer (Diagnose) |
| Zählernummer | – | Energie | Zählernummer (Diagnose) |

---

### Buttons pro Vertrag

| Button | Beschreibung |
|--------|-------------|
| Jetzt wechseln | Übernimmt den Folgetarif sofort |
| Kündigung bestätigen | Quittiert die Erinnerung und entfernt die Dauerbenachrichtigung |

---

### Tarifwechsel

Unter **Einstellungen → Integrationen → Tariffy → [Vertrag] → Optionen** Folgetarif hinterlegen. Am Wechseldatum übernimmt HA automatisch.

---

### Kündigungs-Erinnerung

1. **Dauerbenachrichtigung** im HA-Benachrichtigungscenter
2. Einmalige **Push-Benachrichtigung** via notify-Dienst
3. Button **„Kündigung bestätigen"** zum Quittieren

> **Prüfintervall:** alle **6 Stunden**

---

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

- Home Assistant 2026.6 oder neuer

---

## Lizenz / License

MIT © [weskona](https://github.com/weskona)
