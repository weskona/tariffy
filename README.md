# Tariffy – Contract Management for Home Assistant

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz)
[![HA Version](https://img.shields.io/badge/Home%20Assistant-2026.6%2B-blue.svg)](https://www.home-assistant.io)
[![Version](https://img.shields.io/github/v/release/weskona/tariffy)](https://github.com/weskona/tariffy/releases)

**[🇩🇪 Deutsche Version weiter unten](#-deutsch)**

---

## 🇬🇧 English

Tariffy is a Home Assistant custom integration for managing utility and service contracts. Electricity, gas, water, internet, mobile, insurance and more — each contract becomes its own HA device with dedicated sensors. Tariffy automatically reminds you of cancellation deadlines, switches tariffs on the switch date, and calculates costs and billing forecasts based on real consumption data.

---

### Features

- **Categories:** Electricity, Gas, Water, Internet, Mobile, Insurance, Other
- **Real consumption tracking** – connect any HA sensor as your meter; Tariffy reads the meter value at contract start from Long-Term Statistics and calculates consumption since contract start and projected annual usage
- **Real billing forecast** – forecast based on actual measured consumption (credit or surcharge)
- **Last contract period consumption** – frozen at tariff switch; used to calculate the recommended monthly payment for the new period
- **Recommended monthly payment** – based on last period's real consumption × current rates
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
| Unit price (night) | €/kWh | Energy | Night rate (TOU/Economy 7) |
| Unit price (effective) | €/kWh | Energy | Effective average price (tiered) |
| Unit price (wastewater) | €/m³ | Water | Wastewater charge |
| Water price (combined) | €/m³ | Water | Fresh water + wastewater |
| Base price | €/month | Energy | Monthly base fee |
| Monthly payment | €/month | All | Monthly instalment |
| Monthly payment (recommended) | €/month | Energy | Based on last period consumption × current rates |
| Cost (contract period) | € | All | Instalment × contract duration in months |
| Cost (so far) | € | Energy+Water | Actual costs incurred since contract start (real consumption) |
| Feed-in tariff | €/kWh | Electricity | Configured feed-in rate |
| Annual consumption (kWh) | kWh | Gas | m³ converted via calorific value & state number |
| Consumption (so far) | kWh/m³ | Energy+Water | Measured consumption since contract start |
| Consumption (contract term projected) | kWh/m³ | Energy+Water | Current consumption extrapolated to the full contract term (not a fixed calendar year) |
| Consumption (last period) | kWh/m³ | Energy | Frozen at tariff switch — basis for recommended payment |
| Cost (forecast real) | € | Energy+Water | Forecast based on real consumption |
| Remaining term | Days | All | Days until contract end |
| Contract start | Date | All | Start date of contract |
| Contract end | Date | All | End of current contract |
| Next switch | Date | All | Date of planned tariff switch |
| Cancellation reminder | Date | All | Date from which the reminder is active |
| Provider | – | All | Provider name (diagnostic) |
| Tariff | – | All | Tariff name (diagnostic) |
| Customer number | – | All | Customer number (diagnostic) |
| Meter number | – | Energy | Meter number (diagnostic) |

> **Night rate** and **tiered pricing** sensors only appear when enabled in the config flow.

---

### Real consumption tracking

When a **consumption sensor** is configured, Tariffy reads the historical meter value at contract start from **Long-Term Statistics** and calculates:

```
Consumption so far                    = current meter value − meter value at contract start
Consumption (contract term projected) = consumption so far ÷ days elapsed × contract term (days)
Cost (so far)                         = consumption so far × unit price + base price × months elapsed
Cost (forecast real)                  = instalment total − projected cost over contract period
```

**Positive** = credit · **Negative** = surcharge

The contract term used for the projection is `contract end − contract start` in days (falls back to 365 if no end date is set) — a contract that runs for e.g. 6 months is projected onto those 6 months, not a full calendar year.

Both the current meter value and the historical value at contract start are read from the recorder's **cumulative `sum` statistic**, not the sensor's raw state. This makes the calculation robust against sensors with `state_class: total_increasing` that legitimately reset periodically (some smart-meter integrations reset their raw counter on every reading cycle) — the recorder's `sum` already accounts for such resets. A meter that never resets at all is still preferable where available.

> The sensor must have Long-Term Statistics enabled and must have existed since at least the contract start date.

---

### Last contract period & recommended payment

When a tariff switch occurs, Tariffy freezes the total consumption of the expiring contract period:

```
Consumption (last period)          = meter at switch date − meter at contract start
Monthly payment (recommended)      = (last period consumption × new unit price + new base price × months) / months
```

`months` is the **actual duration of the expiring contract period** in months (frozen at the moment of switching), not a fixed 12 — relevant if the previous contract ran shorter or longer than a year. Falls back to 12 for periods frozen before this was tracked.

This gives a data-driven recommendation for the monthly instalment in the new contract.

---

### Buttons per contract

| Button | Description |
|--------|-------------|
| Switch now | Promotes the stored next tariff immediately (without waiting for the switch date) |
| Confirm cancellation | Acknowledges the reminder and removes the persistent notification |

---

### Tariff switch

Under **Settings → Integrations → Tariffy → [Contract] → Options** you can store a successor tariff:

- Switch date, new provider, customer number, tariff name
- New prices and consumption values

On the switch date HA promotes the new tariff automatically. Fields left blank keep their current value.

---

### Cancellation reminder

When contract end is set and the reminder period is reached:

1. **Persistent notification** in the HA notification centre
2. One-time **push notification** via the configured notify service
3. **"Confirm cancellation"** button to acknowledge

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

Tariffy ist eine Home Assistant Custom Integration zur Verwaltung von Energie- und Dienstleistungsverträgen. Strom, Gas, Wasser, Internet, Mobilfunk, Versicherungen und mehr – jeder Vertrag wird als eigenes HA-Gerät mit Sensoren angelegt. Tariffy erinnert automatisch an Kündigungsfristen, wechselt Tarife zum Stichtag und berechnet Kosten sowie Abrechnungsprognosen auf Basis echter Verbrauchsdaten.

---

### Features

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
- **Einspeisevergütung** – Vergütung pro eingespeister kWh (Photovoltaik)
- **Auto-Refresh nach HA-Start** – Sensoren aktualisieren sich automatisch sobald die Long-Term Statistics nach einem Neustart bereit sind
- **Prüfintervall** – alle 6 Stunden, zusätzlich täglich exakt um 00:00:01 Uhr für einen pünktlichen Tarifwechsel bei Datumswechsel

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
>
> Brennwert und Zustandszahl akzeptieren sowohl Dezimalpunkt (`11.2`) als auch Dezimalkomma (`11,2`).

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
| Arbeitspreis (Nacht) | €/kWh | Energie | Nachttarif (TOU/Economy 7) |
| Arbeitspreis (Effektiv) | €/kWh | Energie | Effektiver Ø-Preis bei Staffeltarif |
| Arbeitspreis (Abwasser) | €/m³ | Wasser | Abwassergebühr |
| Wasserpreis (Gesamt) | €/m³ | Wasser | Frischwasser + Abwasser kombiniert |
| Grundpreis | €/Monat | Energie | Monatliche Grundgebühr |
| Abschlag | €/Monat | Alle | Monatlicher Abschlag |
| Abschlag (Empfohlen) | €/Monat | Energie | Basiert auf realem Verbrauch der letzten Laufzeit × aktuelle Preise |
| Abschlag (Vertragslaufzeit) | € | Alle | Abschlag × Laufzeit in Monaten (reiner Zahlungsplan, keine Kosten-Prognose) |
| Kosten (Bisher) | € | Energie+Wasser | Tatsächlich angefallene Kosten seit Vertragsbeginn (Echte Messung) |
| Guthaben/Nachzahlung (Bisher) | € | Energie | Abschlag bisher gezahlt − Kosten (Bisher), Stand von heute (keine Hochrechnung). Icon zeigt 👍/👎 je nach Vorzeichen |
| Einspeisevergütung | €/kWh | Strom | Eingetragene Vergütung pro kWh |
| Jahresverbrauch (kWh) | kWh | Gas | m³ umgerechnet via Brennwert & Zustandszahl |
| Verbrauch (Bisher) | kWh/m³ | Energie+Wasser | Gemessener Verbrauch seit Vertragsbeginn |
| Verbrauch (Vertragslaufzeit hochgerechnet) | kWh/m³ | Energie+Wasser | Aktueller Verbrauch auf die tatsächliche Vertragslaufzeit hochgerechnet (kein festes Kalenderjahr) |
| Verbrauch (Letzte Laufzeit) | kWh/m³ | Energie | Eingefroren beim Tarifwechsel |
| Guthaben/Nachzahlung (Vertragsende) | € | Energie+Wasser | Prognose auf Basis des echten Verbrauchs. Icon zeigt 👍/👎 je nach Vorzeichen |
| Restlaufzeit | Tage | Alle | Tage bis Vertragsende |
| Vertragsbeginn | Datum | Alle | Startdatum des Vertrags |
| Vertragsende | Datum | Alle | Ende des aktuellen Vertrags |
| Nächster Wechsel | Datum | Alle | Datum des geplanten Tarifwechsels |
| Kündigungs-Erinnerung | Datum | Alle | Datum ab dem erinnert wird |
| Anbieter | – | Alle | Name des Anbieters (Diagnose) |
| Tarif | – | Alle | Tarifbezeichnung (Diagnose) |
| Kundennummer | – | Alle | Kundennummer (Diagnose) |
| Zählernummer | – | Energie | Zählernummer (Diagnose) |

> Sensoren für **Nachttarif** (Economy 7 / TOU) und **Staffelpreise** erscheinen nur wenn im Config Flow aktiviert.

---

### Echte Verbrauchsmessung

Wenn ein **Verbrauchssensor** eingetragen ist, liest Tariffy beim Vertragsbeginn den historischen Zählerstand aus den **Long-Term Statistics** und berechnet:

```
Verbrauch (Bisher)                          = aktueller Zählerstand − Zählerstand am Vertragsbeginn
Verbrauch (Vertragslaufzeit hochgerechnet)  = Verbrauch bisher ÷ vergangene Tage × Vertragslaufzeit (Tage)
Kosten (Bisher)                             = Verbrauch bisher × Arbeitspreis + Grundpreis × vergangene Monate
Guthaben/Nachzahlung (Bisher)                = Abschlag × vergangene Monate − Kosten (Bisher)
Guthaben/Nachzahlung (Vertragsende)           = Abschlag (Vertragslaufzeit) − hochgerechnete Kosten über Laufzeit
```

**Positiv** = Guthaben · **Negativ** = Nachzahlung

Die für die Hochrechnung verwendete Vertragslaufzeit ist `Vertragsende − Vertragsbeginn` in Tagen (Fallback 365 ohne Enddatum) — ein Vertrag über z. B. 6 Monate wird auf diese 6 Monate hochgerechnet, nicht auf ein volles Kalenderjahr.

Sowohl der aktuelle Zählerstand als auch der historische Wert zum Vertragsbeginn werden aus der kumulierten **`sum`-Statistik** des Recorders gelesen, nicht aus dem rohen Sensor-Zustand. Das macht die Berechnung robust gegenüber Sensoren mit `state_class: total_increasing`, die erlaubterweise periodisch zurücksetzen (manche Smart-Meter-Integrationen setzen ihren Rohzähler bei jedem Ablesezyklus zurück) — die `sum`-Statistik des Recorders berücksichtigt solche Resets bereits. Ein Zähler, der nie zurücksetzt, ist trotzdem vorzuziehen, wo verfügbar.

> Der Sensor muss Long-Term Statistics aktiviert haben und mindestens seit Vertragsbeginn existieren.

---

### Verbrauch letzte Laufzeit & empfohlener Abschlag

Beim Tarifwechsel friert Tariffy den Gesamtverbrauch der ablaufenden Vertragslaufzeit ein:

```
Verbrauch (Letzte Laufzeit) = Zählerstand am Wechseltag − Zählerstand am Vertragsbeginn
Abschlag (Empfohlen)        = (Letzte Laufzeit × neuer Arbeitspreis + neuer Grundpreis × Monate) / Monate
```

`Monate` ist die **tatsächliche Dauer der ablaufenden Vertragslaufzeit** in Monaten (eingefroren im Moment des Wechsels), nicht pauschal 12 — relevant, wenn der vorherige Vertrag kürzer oder länger als ein Jahr lief. Fallback auf 12, wenn die Laufzeit vor Einführung dieser Berechnung eingefroren wurde.

So erhält man eine datenbasierte Empfehlung für den monatlichen Abschlag im neuen Vertrag.

---

### Buttons pro Vertrag

| Button | Beschreibung |
|--------|-------------|
| Jetzt wechseln | Übernimmt den hinterlegten Folgetarif sofort (ohne auf das Datum zu warten) — friert den Verbrauch der endenden Laufzeit exakt wie beim automatischen Wechsel ein |
| Kündigung bestätigen | Quittiert die Erinnerung und entfernt die Dauerbenachrichtigung |

---

### Tarifwechsel

Unter **Einstellungen → Integrationen → Tariffy → [Vertrag] → Optionen** kannst du einen Folgetarif hinterlegen:

- Wechseldatum, neuer Anbieter, Kundennummer, Tarifname
- Neue Preise und Verbrauchswerte

Am Wechseldatum übernimmt HA den neuen Tarif automatisch — geprüft täglich exakt um 00:00:01 Uhr, zusätzlich beim regulären 6h-Poll und beim HA-Start als Fallback. Nicht angegebene Felder behalten ihren aktuellen Wert.

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

## Lizenz / License

MIT © [weskona](https://github.com/weskona)
