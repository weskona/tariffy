# Tariffy

_Vertragsverwaltung für Home Assistant_ (Integrations-Domain: `vertraege`)

Verwaltet Versorgungs- und sonstige Verträge (Strom, Gas, Wasser, Internet, …) als
Home-Assistant-Geräte: aktueller Tarif, Anbieter, Kundennummer, Laufzeit – plus einen
**im Voraus hinterlegten Folgevertrag**, der am Wechseldatum automatisch übernommen wird.

## Konzept

- **Ein Eintrag = ein Vertrag.** Über *Einstellungen → Geräte & Dienste → Integration
  hinzufügen → Verträge* legst du beliebig viele an.
- **Aktueller Vertrag** lebt in `entry.data` (per *Konfigurieren/Neu konfigurieren* änderbar).
- **Nächster Vertrag** lebt in den **Optionen** (`entry.options`). Trägst du dort ein
  Wechseldatum + die neuen Werte ein, schaltet ein Coordinator (Prüfung alle 6 h) am
  Stichtag automatisch um: `nächster → aktuell`, Optionen werden geleert.
- **Button „Jetzt wechseln"** löst den Wechsel manuell sofort aus (z. B. zum Testen).

## Entitäten je Vertrag

| Entität | Beschreibung |
|---|---|
| `sensor.<name>_arbeitspreis` | Arbeitspreis, Einheit je Sparte (Strom/Gas €/kWh, Wasser €/m³, sonst €). Attribute: Anbieter, Tarif, Kundennummer, Sparte |
| `sensor.<name>_grundpreis` | Grundpreis (€/Monat) |
| `sensor.<name>_restlaufzeit` | Tage bis Vertragsende |
| `sensor.<name>_vertragsende` | Datum (device_class date) |
| `sensor.<name>_anbieter` / `_kundennummer` / `_tarif` | Stammdaten |
| `sensor.<name>_naechster_wechsel` | Datum des geplanten Wechsels; Attribute = Daten des Folgevertrags |
| `button.<name>_jetzt_wechseln` | Sofort umschalten (nur verfügbar, wenn Folgevertrag hinterlegt) |
| `sensor.<name>_kuendigungs_erinnerung` | Datum, ab dem an die Kündigung erinnert wird; Attribute: `aktiv`, `bestaetigt`, `monate_vorher` |
| `button.<name>_kuendigung_bestaetigen` | Erinnerung quittieren (nur verfügbar, solange aktiv) |

## Sparten-abhängige Felder

Der Anlege-/Bearbeiten-Dialog ist zweistufig: Schritt 1 allgemein, Schritt 2 je nach Sparte.

**Strom/Gas (Energie):** Arbeitspreis, Grundpreis, Abschlag, geschätzter Jahresverbrauch,
Neukundenbonus, Ökostrom, Zählernummer, Marktlokation (MaLo-ID), Preisgarantie.
Daraus berechnet:
- `geschaetzte_jahreskosten` = Jahresverbrauch × Arbeitspreis + Grundpreis × 12
- `jahreskosten` = Abschlag × 12 (Abschlagssumme)
- `prognose` = Abschlagssumme − geschätzte Kosten (positiv = Guthaben, negativ = Nachzahlung;
  Tendenz als Attribut)

**Gas:** zusätzlich Verbrauch in **m³** plus **Brennwert** (kWh/m³) und **Zustandszahl**; daraus wird `verbrauch_kwh = m³ × Brennwert × Zustandszahl` berechnet und für die geschätzten Jahreskosten verwendet (eigener Sensor `verbrauch_kwh`).

**Pauschal (Internet/Mobilfunk/…):** nur Abschlag (+ optional Grundpreis); die Energie-Sensoren
werden für diese Sparten nicht angelegt.

Beim automatischen Wechsel werden im „nächsten Vertrag" nicht ausgefüllte Felder aus dem
aktuellen übernommen (z. B. bleibt die Zählernummer beim Anbieterwechsel erhalten).

## Kündigungs-Erinnerung

Pro Vertrag wählbar: **Keine / 1 / 2 / 3 / 4 Monate vor Vertragsende** erinnern, plus
optional ein **notify-Ziel** (Dropdown aller `notify.*`-Dienste, z. B. dein Handy).

Ist der Zeitpunkt erreicht (`Vertragsende − X Monate`), passiert beim nächsten
Coordinator-Lauf (alle 6 h):

- eine **dauerhafte Benachrichtigung** wird gesetzt – und bei jedem Lauf erneut gesetzt,
  falls du sie wegklickst. Sie verschwindet erst endgültig über den Button
  **„Kündigung bestätigen"**.
- einmalig eine **notify-Push** an das gewählte Ziel.

Bestätigst du, oder läuft der Vertrag aus / wird auf den Folgevertrag umgeschaltet, wird
die Erinnerung zurückgesetzt.

Der Arbeitspreis-Sensor lässt sich direkt im **Energie-Dashboard** als Kostenquelle nutzen.

## Installation

**Manuell:** Ordner `custom_components/vertraege` nach `/config/custom_components/`
kopieren, Home Assistant neu starten.

**HACS:** als *Custom repository* (Kategorie *Integration*) hinzufügen, installieren, neu starten.

## Hinweise

- Für **dynamische Börsentarife** (Tibber, EPEX Spot, aWATTar) ist diese Integration nicht
  gedacht – die liefern den Live-Preis über eigene Integrationen. Dies hier verwaltet
  **Festpreis-Verträge inkl. Stammdaten und geplantem Anbieterwechsel**.
- Eine Erinnerung vor Ablauf der Kündigungsfrist lässt sich als simple Automation auf
  `sensor.<name>_restlaufzeit` bauen (z. B. Trigger bei `< 90`).
