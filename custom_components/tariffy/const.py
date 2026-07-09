"""Konstanten für die Tariffy-Integration."""

from __future__ import annotations

from homeassistant.const import Platform

DOMAIN = "tariffy"
PLATFORMS = [Platform.SENSOR, Platform.BUTTON]

# Allgemeine Schlüssel
CONF_SPARTE = "sparte"
CONF_ANBIETER = "anbieter"
CONF_KUNDENNUMMER = "kundennummer"
CONF_TARIF = "tarif"
CONF_BEGINN = "beginn"
CONF_ENDE = "ende"

# Kosten
CONF_ARBEITSPREIS = "arbeitspreis"
CONF_GRUNDPREIS = "grundpreis"
CONF_ABSCHLAG = "abschlag"

# Energie-spezifisch (Strom/Gas)
CONF_JAHRESVERBRAUCH = "jahresverbrauch"
CONF_GAS_EINHEIT = "gas_einheit"
CONF_ZAEHLERNUMMER = "zaehlernummer"
CONF_MARKTLOKATION = "marktlokation"
CONF_PREISGARANTIE = "preisgarantie"
CONF_BONUS = "bonus"
CONF_OEKOSTROM = "oekostrom"

# Gas-spezifisch
CONF_BRENNWERT = "brennwert"
CONF_ZUSTANDSZAHL = "zustandszahl"

# Wasser-spezifisch
CONF_ARBEITSPREIS_ABWASSER = "arbeitspreis_abwasser"
CONF_ABWASSER_TYP = "abwasser_typ"
CONF_WASSER_EINHEIT = "wasser_einheit"

# Abwasser-Berechnungstypen
ABWASSER_TYP_PREIS = "price_per_unit"    # fixer Preis pro Einheit (DE/AT/CH)
ABWASSER_TYP_PROZENT = "percentage"      # % des Frischwasserpreises (US/UK/AU)
ABWASSER_TYP_PAUSCHAL = "flat_rate"      # Pauschal pro Monat (FR/BE)
ABWASSER_TYPEN = [ABWASSER_TYP_PREIS, ABWASSER_TYP_PROZENT, ABWASSER_TYP_PAUSCHAL]

# Tiered / gestaffelte Preise (Strom, Gas, Wasser)
CONF_TIERED = "tiered"                   # aktiviert Staffelpreise
CONF_TIER_LIMITS = "tier_limits"         # Liste von Obergrenzen je Block [5, 10, 20]
CONF_TIER_PRICES = "tier_prices"         # Liste von Preisen je Block [0.5, 0.8, 1.2]
MAX_TIERS = 5                            # max. Anzahl Blöcke

# Tag/Nacht-Tarif (Time-of-Use)
CONF_ARBEITSPREIS_NACHT = "arbeitspreis_nacht"
CONF_JAHRESVERBRAUCH_NACHT = "jahresverbrauch_nacht"
CONF_JAHRESVERBRAUCH_TAG = "jahresverbrauch_tag"

# Länder mit Tag/Nacht-Tarifen (Economy 7, TOU)
LAENDER_TAG_NACHT = {"GB", "US", "CA", "AU", "NZ", "IE"}

# Länder mit gestaffelten Preisen (Tiered)
LAENDER_TIERED = {"US", "CA", "AU", "NZ", "ES", "PT", "IT", "GR", "IL", "IN", "BR", "MX", "ZA", "CN", "JP", "KR"}

# Länder mit Abwasser als % (water sewerage percentage)
LAENDER_ABWASSER_PROZENT = {"US", "CA", "AU", "NZ", "GB", "IE"}

# Länder mit Abwasser-Pauschale
LAENDER_ABWASSER_PAUSCHAL = {"FR", "BE", "LU"}

# Echte Verbrauchsmessung
CONF_VERBRAUCH_SENSOR = "verbrauch_sensor"
CONF_VERBRAUCH_LETZTE_LAUFZEIT = "verbrauch_letzte_laufzeit"
CONF_VERBRAUCH_LETZTE_LAUFZEIT_MONATE = "verbrauch_letzte_laufzeit_monate"

# Einspeiseverguetung (nur Strom)
CONF_EINSPEISEVERGUETUNG = "einspeiseverguetung"

# Feed-in tariff: available worldwide, no country restriction

ENERGIE_SPARTEN = ("electricity", "gas")
GAS_SPARTE = "gas"
WASSER_SPARTE = "water"
ENERGIE_SPARTEN_MIT_WASSER = ("strom", "gas", "wasser")

# Kündigungs-Erinnerung
CONF_ERINNERUNG_MONATE = "erinnerung_monate"
CONF_NOTIFY_TARGET = "notify_target"
ERINNERUNG_OPTIONS = ["0", "1", "2", "3", "4"]

# Interne Statusflags
CONF_KUENDIGUNG_BESTAETIGT = "_kuendigung_bestaetigt"
CONF_NOTIFY_GESENDET = "_notify_gesendet"

NOTIFY_ID_PREFIX = "tariffy_kuendigung_"

# Zukünftiger Vertrag
NEXT_PREFIX = "next_"

# Felder die beim Wechsel übernommen werden
BASIS_FELDER = [
    CONF_ANBIETER,
    CONF_KUNDENNUMMER,
    CONF_TARIF,
    CONF_ARBEITSPREIS,
    CONF_GRUNDPREIS,
    CONF_ABSCHLAG,
    CONF_JAHRESVERBRAUCH,
    CONF_GAS_EINHEIT,
    CONF_BRENNWERT,
    CONF_ZUSTANDSZAHL,
    CONF_ZAEHLERNUMMER,
    CONF_MARKTLOKATION,
    CONF_PREISGARANTIE,
    CONF_BONUS,
    CONF_OEKOSTROM,
    CONF_BEGINN,
    CONF_ENDE,
    CONF_VERBRAUCH_SENSOR,
    CONF_ARBEITSPREIS_ABWASSER,
    CONF_ABWASSER_TYP,
    CONF_WASSER_EINHEIT,
    CONF_TIERED,
    CONF_TIER_LIMITS,
    CONF_TIER_PRICES,
    CONF_ARBEITSPREIS_NACHT,
    CONF_JAHRESVERBRAUCH_NACHT,
    CONF_JAHRESVERBRAUCH_TAG,
    CONF_EINSPEISEVERGUETUNG,
]

SPARTEN = [
    "electricity",
    "gas",
    "water",
    "internet",
    "mobile",
    "insurance",
    "other",
]

# Rueckwaertskompatibilitaet: alte Sparten-Werte -> neue
SPARTEN_MIGRATION = {
    "strom": "electricity",
    "wasser": "water",
    "mobilfunk": "mobile",
    "versicherung": "insurance",
    "sonstiges": "other",
    # gas, internet bleiben gleich
}

# Wassereinheiten
WASSER_EINHEITEN = ["m³", "L", "gal", "ft³", "CCF"]

# Gas-Verbrauchseinheiten mit Umrechnungsfaktoren zu kWh
# Brennwert wird separat angegeben (nur für m³, CCF, ft³)
GAS_EINHEITEN = ["m³", "CCF", "therm", "ft³", "MBtu", "kWh"]

# Einheiten — dynamisch aus HA-Währung gebaut
# Feste Nicht-Währungs-Einheiten
GRUNDPREIS_SUFFIX = "/month"
ABSCHLAG_SUFFIX = "/month"
JAHRESKOSTEN_SUFFIX = "/year"
VERBRAUCH_KWH_EINHEIT = "kWh"
VERBRAUCH_EINHEIT = "kWh"
VERBRAUCH_M3_EINHEIT = "m³"
BRENNWERT_SUFFIX_M3 = "kWh/m³"
BRENNWERT_SUFFIX_CCF = "kWh/CCF"
BRENNWERT_SUFFIX_FT3 = "kWh/ft³"
