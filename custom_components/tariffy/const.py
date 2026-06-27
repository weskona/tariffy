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
CONF_ZAEHLERNUMMER = "zaehlernummer"
CONF_MARKTLOKATION = "marktlokation"
CONF_PREISGARANTIE = "preisgarantie"
CONF_BONUS = "bonus"
CONF_OEKOSTROM = "oekostrom"

# Gas-spezifisch
CONF_BRENNWERT = "brennwert"
CONF_ZUSTANDSZAHL = "zustandszahl"

# Echte Verbrauchsmessung
CONF_VERBRAUCH_SENSOR = "verbrauch_sensor"

ENERGIE_SPARTEN = ("strom", "gas")
GAS_SPARTE = "gas"

# Kündigungs-Erinnerung
CONF_ERINNERUNG_MONATE = "erinnerung_monate"
CONF_NOTIFY_TARGET = "notify_target"
ERINNERUNG_OPTIONS = ["0", "1", "2", "3", "4"]

# Interne Statusflags (entry.data; werden bei Datenänderung/Wechsel zurückgesetzt)
CONF_KUENDIGUNG_BESTAETIGT = "_kuendigung_bestaetigt"
CONF_NOTIFY_GESENDET = "_notify_gesendet"

NOTIFY_ID_PREFIX = "tariffy_kuendigung_"

# Zukünftiger Vertrag -> entry.options, gleiche Keys mit Präfix
NEXT_PREFIX = "next_"

# Felder, die beim Wechsel nächster -> aktuell übernommen werden.
BASIS_FELDER = [
    CONF_ANBIETER,
    CONF_KUNDENNUMMER,
    CONF_TARIF,
    CONF_ARBEITSPREIS,
    CONF_GRUNDPREIS,
    CONF_ABSCHLAG,
    CONF_JAHRESVERBRAUCH,
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
]

SPARTEN = [
    "strom",
    "gas",
    "wasser",
    "internet",
    "mobilfunk",
    "versicherung",
    "sonstiges",
]

# Einheiten
ARBEITSPREIS_EINHEIT = {
    "strom": "€/kWh",
    "gas": "€/kWh",
    "wasser": "€/m³",
}
DEFAULT_ARBEITSPREIS_EINHEIT = "€"
GRUNDPREIS_EINHEIT = "€/Monat"
ABSCHLAG_EINHEIT = "€/Monat"
JAHRESKOSTEN_EINHEIT = "€/Jahr"
VERBRAUCH_EINHEIT = "kWh"
VERBRAUCH_M3_EINHEIT = "m³"
BRENNWERT_EINHEIT = "kWh/m³"
EURO_EINHEIT = "€"
