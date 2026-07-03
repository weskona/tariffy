# Tariffy – Vertragsverwaltung für Home Assistant

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz)
[![HA Version](https://img.shields.io/badge/Home%20Assistant-2026.6%2B-blue.svg)](https://www.home-assistant.io)
[![Version](https://img.shields.io/github/v/release/weskona/tariffy)](https://github.com/weskona/tariffy/releases)

**[🇬🇧 English version below](#-english)**

---

## 🇩🇪 Deutsch

Tariffy ist eine Home Assistant Custom Integration zur Verwaltung von Energie- und Dienstleistungsverträgen. Strom, Gas, Wasser, Internet, Mobilfunk, Versicherungen und mehr – jeder Vertrag wird als eigenes HA-Gerät mit Sensoren angelegt. Tariffy erinnert automatisch an Kündigungsfristen, wechselt Tarife zum Stichtag und berechnet Kosten sowie Abrechnungsprognosen auf Basis echter Verbrauchsdaten.

---

### Features

- **Sparten:** Strom, Gas, Wasser, Internet, Mobilfunk, Versicherung, Sonstiges
- **Echte Verbrauchsmessung** – beliebigen HA-Sensor als Zähler einbinden; Tariffy liest den Stand zum Vertragsbeginn aus den Long-Term Statistics und berechnet Verbrauch seit Vertragsbeginn sowie hochgerechneten Jahresverbrauch
- **Abrechnungsprognose (real)** – Prognose basierend auf dem tatsächlich gemessenen Verbrauch (Guthaben oder Nachzahlung)
- **Automatischer Tarifwechsel** – Folgetarif hinterlegen, HA übernimmt ihn am Wechseldatum automatisch
- **Kündigungs-Erinnerung** – 1–4 Monate vor Vertragsende, Dauerbenachrichtigung + optionaler notify-Dienst, Bestätigen-Button
- **Gas-Umrechnung** – Jahresverbrauch in m³ wird automatisch via Brennwert & Zustandszahl in kWh umgerechnet
- **Wasser** – Frischwasser + Abwasser (Festpreis, % oder Monatspauschale)
- **Staffelpreise** – länderspezifisch (US, AU, ES, …)
- **Tag/Nacht-Tarif** – Economy 7, TOU (GB, US, AU, …)
- **Einspeisevergütung** – Vergütung pro eingespeister kWh (Photovoltaik)
- **Auto-Refresh nach HA-Start** – Sensoren aktualisieren sich automatisch sobald die Long-Term Statistics nach einem Neustart bereit sind
- **Prüfintervall** – alle 6 Stunden

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
| Vertragsbeginn | – | Startdatum des Vertrags |
| Vertragsende | – | Enddatum / Laufzeit bis |
| Kündigung erinnern | ✅ | 0–4 Monate vorher (0 = deaktiviert) |
| Benachrichtigungs-Ziel | – | notify-Dienst (z. B. `mobile_app_iphone`) |

#### Schritt 2a – Strom-Details

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

#### Schritt 2b – Gas-Details

Wie Strom, zusätzlich:

| Feld | Pflicht | Beschreibung |
|------|---------|-------------|
| Gaseinheit | ✅ | m³, CCF, therm, … |
| Jahresverbrauch | – | In der gewählten Einheit |
| Verbrauchssensor | – | HA-Sensor des Gaszählers |
| Brennwert | ✅ | kWh/m³ (ca. 10–12, steht auf der Gasrechnung) |
| Zustandszahl | ✅ | Umrechnungsfaktor Z (ca. 0,95, steht auf der Gasrechnung) |

> **Umrechnung:** kWh = m³ × Brennwert × Zustandszahl

#### Schritt 2c – Wasser-Details

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

#### Schritt 2d – Pauschalverträge (Internet, Mobilfunk, Versicherung, …)

| Feld | Pflicht | Beschreibung |
|------|---------|-------------|
| Monatlicher Abschlag | ✅ | €/Monat |
| Grundpreis | – | €/Monat (falls separat ausgewiesen) |

---

### Sensoren pro Vertrag

| Sensor | Einheit | Sparte | Beschreibung |
|--------|---------|--------|-------------|
| Arbeitspreis | €/kWh | Energie | Verbrauchsabhängiger Preis |
| Grundpreis | €/Monat | Energie | Monatliche Grundgebühr |
| Monatliche Kosten | €/Monat | Alle | Monatlicher Abschlag |
| Jahreskosten (Abschlag) | €/Jahr | Alle | Abschlag × 12 |
| Geschätzte Jahreskosten | €/Jahr | Energie | Verbrauch × Arbeitspreis + Grundpreis × 12 |
| Einspeisevergütung | €/kWh | Strom | Eingetragene Vergütung pro kWh |
| Jahresverbrauch (kWh) | kWh | Gas | m³ umgerechnet via Brennwert & Zustandszahl |
| Frischwasserpreis | €/m³ | Wasser | Preis pro Einheit Frischwasser |
| Abwasserpreis | €/m³ | Wasser | Abwassergebühr |
| Gesamtwasserpreis | €/m³ | Wasser | Frischwasser + Abwasser kombiniert |
| Verbrauch bisher (Vertrag) | kWh/m³ | Energie+Wasser | Gemessener Verbrauch seit Vertragsbeginn |
| Hochgerechneter Jahresverbrauch | kWh/m³ | Energie+Wasser | Aktueller Verbrauch auf 12 Monate hochgerechnet |
| Abrechnungsprognose (real) | € | Energie+Wasser | Prognose auf Basis des echten Verbrauchs |
| Restlaufzeit | Tage | Alle | Tage bis Vertragsende |
| Vertragsbeginn | Datum | Alle | Startdatum des Vertrags |
| Vertragsende | Datum | Alle | Ende des aktuellen Vertrags |
| Nächster Wechsel | Datum | Alle | Datum des geplanten Tarifwechsels |
| Kündigungs-Erinnerung | Datum | Alle | Datum ab dem erinnert wird |
| Anbieter | – | Alle | Name des Anbieters |
| Tarif | – | Alle | Tarifbezeichnung |
| Kundennummer | – | Alle | Kundennummer (Diagnose) |
| Zählernummer | – | Energie | Zählernummer (Diagnose) |

> Sensoren für **Nachttarif** (Economy 7 / TOU) und **Staffelpreise** erscheinen nur wenn im Config Flow aktiviert.

---

### Echte Verbrauchsmessung

Wenn ein **Verbrauchssensor** eingetragen ist, liest Tariffy beim Vertragsbeginn den historischen Zählerstand aus den **Long-Term Statistics** und berechnet:

```
Verbrauch bisher      = aktueller Zählerstand − Zählerstand am Vertragsbeginn
Hochgerechnet         = Verbrauch bisher ÷ vergangene Tage × 365
Geschätzte Kosten     = Hochgerechnet × Arbeitspreis + Grundpreis × 12
Abrechnungsprognose   = Jahresabschlag − Geschätzte Kosten
```

**Positiv** = Guthaben · **Negativ** = Nachzahlung

> Der Sensor muss Long-Term Statistics aktiviert haben und mindestens seit Vertragsbeginn existieren.

---

### Buttons pro Vertrag

| Button | Beschreibung |
|--------|-------------|
| Jetzt wechseln | Übernimmt den hinterlegten Folgetarif sofort (ohne auf das Datum zu warten) |
| Kündigung bestätigen | Quittiert die Erinnerung und entfernt die Dauerbenachrichtigung |

---

### Tarifwechsel

Unter **Einstellungen → Integrationen → Tariffy → [Vertrag] → Optionen** kannst du einen Folgetarif hinterlegen:

- Wechseldatum, neuer Anbieter, Kundennummer, Tarifname
- Neue Preise und Verbrauchswerte

Am Wechseldatum übernimmt HA den neuen Tarif automatisch. Nicht angegebene Felder behalten ihren aktuellen Wert.

---

### Kündigungs-Erinnerung

Wenn Vertragsende gesetzt und der Erinnerungszeitraum erreicht ist:

1. **Dauerbenachrichtigung** im HA-Benachrichtigungscenter
2. Einmalige **Push-Benachrichtigung** via konfiguriertem notify-Dienst
3. Button **„Kündigung bestätigen"** zum Quittieren

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

## 🇬🇧 English

Tariffy is a Home Assistant custom integration for managing utility and service contracts. Electricity, gas, water, internet, mobile, insurance and more — each contract becomes its own HA device with dedicated sensors. Tariffy automatically reminds you of cancellation deadlines, switches tariffs on the switch date, and calculates costs and billing forecasts based on real consumption data.

---

### Features

- **Categories:** Electricity, Gas, Water, Internet, Mobile, Insurance, Other
- **Real consumption tracking** – connect any HA sensor as your meter; Tariffy reads the meter value at contract start from Long-Term Statistics and calculates consumption since contract start and projected annual usage
- **Real billing forecast** – forecast based on actual measured consumption (credit or surcharge)
- **Automatic tariff switch** – store the next tariff, HA promotes it automatically on the switch date
- **Cancellation reminder** – 1–4 months before contract end, persistent notification + optional notify service
- **Gas conversion** – annual consumption in m³ is automatically converted to kWh via calorific value & state number
- **Water** – fresh water + wastewater (fixed price, % or flat rate)
- **Tiered pricing** – country-specific (US, AU, ES, …)
- **Time-of-Use / Night rate** – Economy 7, TOU (GB, US, AU, …)
- **Feed-in tariff** – per kWh fed into the grid (solar)
- **Auto-refresh after HA startup** – sensors update automatically once Long-Term Statistics are ready after a restart
- **Check interval** – every 6 hours

---

### Sensors per contract

| Sensor | Unit | Category | Description |
|--------|------|----------|-------------|
| Unit price | €/kWh | Energy | Consumption-based price |
| Base price | €/month | Energy | Monthly base fee |
| Monthly cost | €/month | All | Monthly instalment |
| Annual cost (instalment) | €/year | All | Instalment × 12 |
| Estimated annual cost | €/year | Energy | Usage × unit price + base price × 12 |
| Feed-in tariff | €/kWh | Electricity | Configured feed-in rate |
| Annual usage (kWh) | kWh | Gas | m³ converted via calorific value & state number |
| Fresh water price | €/m³ | Water | Price per unit |
| Wastewater price | €/m³ | Water | Wastewater charge |
| Combined water price | €/m³ | Water | Fresh water + wastewater |
| Consumption so far | kWh/m³ | Energy+Water | Measured consumption since contract start |
| Projected annual consumption | kWh/m³ | Energy+Water | Current consumption extrapolated to 12 months |
| Billing forecast (real) | € | Energy+Water | Forecast based on real consumption |
| Remaining term | Days | All | Days until contract end |
| Contract start | Date | All | Start date of contract |
| Contract end | Date | All | End of current contract |
| Next switch | Date | All | Date of planned tariff switch |
| Cancellation reminder | Date | All | Date from which the reminder is active |
| Provider | – | All | Provider name |
| Tariff | – | All | Tariff name |
| Customer number | – | All | Customer number (diagnostic) |
| Meter number | – | Energy | Meter number (diagnostic) |

> **Night rate** and **tiered pricing** sensors only appear when enabled in the config flow.

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

## Lizenz / License

MIT © [weskona](https://github.com/weskona)
