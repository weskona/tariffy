"""Config- und Options-Flow der Tariffy-Integration (sparten-abhängig)."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
    OptionsFlowWithReload,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import selector
from homeassistant.util import dt as dt_util

from .backup import BackupError, sanitize_contract
from .const import (
    CONF_ABSCHLAG,
    CONF_ABSCHLAG_AB_DATUM,
    CONF_ABSCHLAG_VORHERIGER_WERT,
    CONF_ABSCHLAG_WARNUNG,
    CONF_ABSCHLAG_WARNUNG_BESTAETIGT,
    CONF_ABSCHLAG_WARNUNG_NOTIFY_GESENDET,
    CONF_ABSCHLAG_WARNUNG_SCHWELLE,
    DEFAULT_ABSCHLAG_WARNUNG_SCHWELLE,
    CONF_ANBIETER,
    CONF_ARBEITSPREIS,
    CONF_BEGINN,
    CONF_BONUS,
    CONF_BRENNWERT,
    CONF_ENDE,
    CONF_ERINNERUNG_MONATE,
    CONF_KUENDIGUNG_BESTAETIGT,
    CONF_NOTIFY_GESENDET,
    CONF_VERBRAUCH_LETZTE_LAUFZEIT,
    CONF_VERBRAUCH_LETZTE_LAUFZEIT_MONATE,
    CONF_HISTORIE,
    CONF_ARCHIVIERT,
    CONF_GRUNDPREIS,
    CONF_JAHRESVERBRAUCH,
    CONF_KENNZEICHEN,
    CONF_KM_PRO_JAHR,
    CONF_KM_START,
    CONF_KUNDENNUMMER,
    CONF_MARKTLOKATION,
    CONF_NOTIFY_TARGET,
    CONF_OEKOSTROM,
    CONF_PREISGARANTIE,
    CONF_SPARTE,
    CONF_TARIF,
    CONF_VERSICHERUNGSART,
    CONF_ZAEHLERNUMMER,
    CONF_ERSTE_ZAHLUNG,
    CONF_ZAHLWEISE,
    CONF_ZUSTANDSZAHL,
    CONF_ABWASSER_TYP,
    ABWASSER_TYPEN,
    ABWASSER_TYP_PREIS,
    ABWASSER_TYP_PROZENT,
    ABWASSER_TYP_PAUSCHAL,
    CONF_ARBEITSPREIS_ABWASSER,
    CONF_GAS_EINHEIT,
    CONF_ARBEITSPREIS_NACHT,
    CONF_ARBEITSPREIS_SENSOR,
    CONF_ARBEITSPREIS_AUFSCHLAG,
    CONF_EINSPEISEVERGUETUNG,
    CONF_JAHRESVERBRAUCH_NACHT,
    CONF_JAHRESVERBRAUCH_TAG,

    CONF_TIERED,
    CONF_TIER_LIMITS,
    CONF_TIER_PRICES,
    LAENDER_TAG_NACHT,
    LAENDER_TIERED,
    LAENDER_ABWASSER_PROZENT,
    LAENDER_ABWASSER_PAUSCHAL,
    MAX_TIERS,
    CONF_VERBRAUCH_SENSOR,
    CONF_VERBRAUCH_START_WERT,
    CONF_WASSER_EINHEIT,
    DOMAIN,
    ENERGIE_SPARTEN,
    DEFAULT_ZAHLWEISE,
    ERINNERUNG_OPTIONS,
    GAS_EINHEITEN,
    GAS_SPARTE,
    NEXT_PREFIX,
    SPARTEN,
    VERSICHERUNGSARTEN,
    VERBRAUCH_EINHEIT,
    VERBRAUCH_M3_EINHEIT,
    WASSER_EINHEITEN,
    WASSER_SPARTE,
    SPARTE_ELECTRICITY_HT_NT,
    SPARTE_INSURANCE,
    CONF_ARBEITSPREIS_NT,
    CONF_VERBRAUCH_SENSOR_NT,
    CONF_VERBRAUCH_START_WERT_NT,
    CONF_ZAEHLERNUMMER_NT,
    ZAHLWEISE_MONATE,
)


# --------------------------------------------------------------------- helpers
def _opt(key: str, default: Any = None) -> vol.Optional:
    if default in (None, ""):
        return vol.Optional(key)
    return vol.Optional(key, description={"suggested_value": default})


def _parse_dezimal(value: Any) -> float | None:
    """Wandelt Texteingabe in float um — akzeptiert Dezimalkomma (11,2) und
    Dezimalpunkt (11.2). HTML5-Zahlenfelder (NumberSelector) behandeln das
    Komma je nach Browser/Locale nicht zuverlässig, daher als Textfeld mit
    eigener Normalisierung, die NACH der Formularvalidierung im jeweiligen
    async_step_* angewendet wird (nicht im Schema selbst — voluptuous_serialize
    kann keine eigenen Funktionen in vol.All zu JSON fürs Frontend konvertieren).
    Gibt None bei ungültiger Eingabe zurück, statt zu werfen.
    """
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return None


def _validiere_dezimal_felder(
    user_input: dict[str, Any],
    keys: tuple[str, str] = (CONF_BRENNWERT, CONF_ZUSTANDSZAHL),
) -> dict[str, str]:
    """Parst Brennwert/Zustandszahl (oder deren next_-Varianten) im user_input
    in-place (Komma->Punkt).

    Gibt ein errors-dict im Format von async_show_form(errors=...) zurück
    (leer, wenn alles geparst werden konnte).
    """
    errors: dict[str, str] = {}
    for key in keys:
        if user_input.get(key):
            parsed = _parse_dezimal(user_input[key])
            if parsed is None:
                errors[key] = "invalid_number"
            else:
                user_input[key] = parsed
    return errors


def _stamp_abschlag_change(alt: dict[str, Any], neu: dict[str, Any]) -> dict[str, Any]:
    """Merkt Datum + vorherigen Wert, wenn sich der Abschlag beim Bearbeiten
    aendert — sonst wuerden "Guthaben/Nachzahlung (Bisher)" und "Abschlag
    (Anpassung empfohlen)" faelschlich den NEUEN Abschlag auf die Zeit VOR
    der Aenderung anwenden (rueckwirkende Neuberechnung).

    Mehrere Aenderungen am SELBEN Tag zaehlen als eine einzige Korrektur
    (kein neuer Stempel) — sonst wuerde z.B. ein Tippfehler, der noch am
    selben Tag korrigiert wird, faelschlich so behandelt, als haette der
    Zwischenwert die ganze bisherige Vertragslaufzeit gegolten.
    """
    alter_abschlag = alt.get(CONF_ABSCHLAG)
    neuer_abschlag = neu.get(CONF_ABSCHLAG)
    heute = dt_util.now().date().isoformat()
    bereits_heute_gestempelt = alt.get(CONF_ABSCHLAG_AB_DATUM) == heute
    if (
        alter_abschlag is not None
        # War vorher kein Abschlag eingetragen (0 ist der Vorgabewert beim Anlegen), ist das Eintragen
        # keine Preisaenderung: der Betrag gilt dann fuer die ganze Laufzeit.
        and float(alter_abschlag) > 0
        and neuer_abschlag is not None
        and round(float(alter_abschlag), 2) != round(float(neuer_abschlag), 2)
        and not bereits_heute_gestempelt
    ):
        return {
            **neu,
            CONF_ABSCHLAG_AB_DATUM: heute,
            CONF_ABSCHLAG_VORHERIGER_WERT: float(alter_abschlag),
        }
    if (
        bereits_heute_gestempelt
        and neuer_abschlag is not None
        and alt.get(CONF_ABSCHLAG_VORHERIGER_WERT) is not None
        and round(float(neuer_abschlag), 2) == round(float(alt[CONF_ABSCHLAG_VORHERIGER_WERT]), 2)
    ):
        # Korrektur am selben Tag landet exakt wieder beim urspruenglichen
        # Wert (Netto-Aenderung heute = keine) - Historie sauber entfernen
        # statt einen wirkungslosen Stempel stehen zu lassen.
        ergebnis = {
            k: v for k, v in neu.items()
            if k not in (CONF_ABSCHLAG_AB_DATUM, CONF_ABSCHLAG_VORHERIGER_WERT)
        }
        return ergebnis
    # Kein NEUER Wechsel (gleicher Wert oder Korrektur eines Wechsels von
    # heute) - vorhandene Historie beibehalten, falls neu sie (z.B. weil das
    # Formular sie nicht mitfuehrt) nicht schon enthaelt.
    ergebnis = dict(neu)
    for key in (CONF_ABSCHLAG_AB_DATUM, CONF_ABSCHLAG_VORHERIGER_WERT):
        if key in alt and key not in ergebnis:
            ergebnis[key] = alt[key]
    return ergebnis


# Werte, die der Coordinator selbst in entry.data ablegt und die in keinem Formular
# vorkommen. Beim Neukonfigurieren ersetzt Home Assistant entry.data komplett durch
# das, was die Formulare liefern; ohne diese Rueckgabe gingen sie dabei verloren
# (bestaetigte Kuendigung/Warnung kaeme zurueck, "Benachrichtigung gesendet" wuerde
# vergessen, der Verbrauch der letzten Laufzeit ginge verloren).
_INTERNER_ZUSTAND = (
    CONF_KUENDIGUNG_BESTAETIGT,
    CONF_NOTIFY_GESENDET,
    CONF_ABSCHLAG_WARNUNG_BESTAETIGT,
    CONF_ABSCHLAG_WARNUNG_NOTIFY_GESENDET,
    CONF_VERBRAUCH_LETZTE_LAUFZEIT,
    CONF_VERBRAUCH_LETZTE_LAUFZEIT_MONATE,
    CONF_HISTORIE,
    CONF_ARCHIVIERT,
)


def _keep_internal_state(alt: dict[str, Any], neu: dict[str, Any]) -> dict[str, Any]:
    """Uebernimmt den internen Zustand des Coordinators in die neuen Vertragsdaten.

    Die Kuendigungs-Erinnerung gehoert zu Vertragsende und Vorlaufzeit: aendert
    sich eines von beiden, beginnt sie neu (Bestaetigung und "Benachrichtigung
    gesendet" werden verworfen), sonst bleibt sie wie sie war."""
    ergebnis = dict(neu)
    for key in _INTERNER_ZUSTAND:
        if key in alt and key not in ergebnis:
            ergebnis[key] = alt[key]
    if alt.get(CONF_ENDE) != ergebnis.get(CONF_ENDE) or str(
        alt.get(CONF_ERINNERUNG_MONATE, "")
    ) != str(ergebnis.get(CONF_ERINNERUNG_MONATE, "")):
        ergebnis.pop(CONF_KUENDIGUNG_BESTAETIGT, None)
        ergebnis.pop(CONF_NOTIFY_GESENDET, None)
    return ergebnis


def _dezimal_feld() -> selector.TextSelector:
    # Reines Textfeld im Schema (muss JSON-serialisierbar bleiben fürs
    # Frontend) — die Komma/Punkt-Normalisierung passiert in der jeweiligen
    # async_step_*-Funktion, siehe _parse_dezimal.
    return selector.TextSelector()


def _dezimal_default(value: Any) -> str:
    # TextSelector verlangt zwingend einen str-Default. Wird hier ein float
    # durchgereicht (z.B. beim Bearbeiten eines bestehenden Vertrags, dessen
    # Brennwert/Zustandszahl bereits als float gespeichert ist) und vom Nutzer
    # unveraendert abgeschickt, kommt der rohe float statt eines Strings an —
    # vol.Schema wirft dann "expected str", bevor _parse_dezimal ueberhaupt
    # laeuft. Deshalb hier IMMER zu str normalisieren.
    return "" if value in (None, "") else str(value)


def _preis(step=None) -> selector.NumberSelector:
    # HA's NumberSelectorConfig lehnt jeden numerischen step < 0.001 hart ab
    # (vol.Range(min=1e-3) in homeassistant/helpers/selector.py) -- ein Preis-
    # Aufruf mit 0.0001 (Arbeitspreise) wuerde also nicht bloss ungenau, sondern
    # mit MultipleInvalid abstuerzen, sobald das Formular gerendert wird. Fuer
    # jeden Wunsch-step unterhalb dieser Grenze bleibt "any" der einzig gueltige
    # Fallback -- eine feinere Eingabe-Praezision laesst sich ueber step ohnehin
    # nicht erzwingen (der Feldwert selbst wird nur per vol.Coerce(float)
    # validiert, nicht gerundet).
    valid_step = step if (step is not None and step >= 0.001) else "any"
    return selector.NumberSelector(
        selector.NumberSelectorConfig(
            min=0, step=valid_step, mode=selector.NumberSelectorMode.BOX
        )
    )


def _abschlag_warnung_fields(d: dict[str, Any]) -> dict[Any, Any]:
    """Optionale Warnung, wenn die Prognose zum Vertragsende eine Nachzahlung
    ueber der Schwelle erwarten laesst. Nur sinnvoll fuer Sparten mit echter
    Verbrauchsmessung (Energie/Wasser), daher hier statt in _common_schema."""
    return {
        vol.Optional(
            CONF_ABSCHLAG_WARNUNG, default=bool(d.get(CONF_ABSCHLAG_WARNUNG, False))
        ): selector.BooleanSelector(),
        vol.Optional(
            CONF_ABSCHLAG_WARNUNG_SCHWELLE,
            default=d.get(CONF_ABSCHLAG_WARNUNG_SCHWELLE, DEFAULT_ABSCHLAG_WARNUNG_SCHWELLE),
        ): _preis(1.0),
    }


def _verbrauch() -> selector.NumberSelector:
    return selector.NumberSelector(
        selector.NumberSelectorConfig(min=0, step="any",
            mode=selector.NumberSelectorMode.BOX,
            unit_of_measurement=VERBRAUCH_EINHEIT,
        )
    )


def _verbrauch_m3() -> selector.NumberSelector:
    return selector.NumberSelector(
        selector.NumberSelectorConfig(min=0, step="any",
            mode=selector.NumberSelectorMode.BOX,
            unit_of_measurement=VERBRAUCH_M3_EINHEIT,
        )
    )


def _verbrauch_start_wert_field(
    d: dict[str, Any], key: str = CONF_VERBRAUCH_START_WERT
) -> dict[Any, Any]:
    """Optionaler manueller Zaehlerstand bei Vertragsbeginn -- Fallback/
    Override fuer die automatische Offset-Ermittlung ueber Recorder-
    Statistiken (siehe coordinator.py). Wird verwendet, sobald gesetzt,
    unabhaengig davon ob die Statistik verfuegbar waere, da der Nutzer den
    wahren Wert oft besser kennt (z.B. vom Zaehler oder der Abrechnung
    abgelesen). `key` erlaubt Wiederverwendung fuer das Niedertarif-Register
    (CONF_VERBRAUCH_START_WERT_NT) beim Zweizaehlertarif."""
    return {
        _opt(key, d.get(key)): selector.NumberSelector(
            selector.NumberSelectorConfig(min=0, step="any", mode=selector.NumberSelectorMode.BOX)
        ),
    }


def _select(options, translation_key=None, custom=False) -> selector.SelectSelector:
    cfg: dict = dict(
        options=options,
        mode=selector.SelectSelectorMode.DROPDOWN,
        custom_value=custom,
    )
    if translation_key is not None:
        cfg["translation_key"] = translation_key
    return selector.SelectSelector(selector.SelectSelectorConfig(**cfg))


def _notify_options(hass: HomeAssistant) -> list:
    dienste = sorted(hass.services.async_services().get("notify", {}))
    return [
        selector.SelectOptionDict(value=n, label=f"notify.{n}") for n in dienste
    ]


def _country_features(hass) -> dict:
    """Gibt länderspezifische Feature-Flags zurück."""
    country = (hass.config.country or "").upper()
    return {
        "hat_tag_nacht": country in LAENDER_TAG_NACHT,
        "hat_tiered": country in LAENDER_TIERED,
        "hat_abwasser_prozent": country in LAENDER_ABWASSER_PROZENT,
        "hat_abwasser_pauschal": country in LAENDER_ABWASSER_PAUSCHAL,
        "hat_einspeisung": True,  # feed-in tariff available worldwide
        "country": country,
    }


def _einspeisung_fields(d: dict, enabled: bool = True) -> dict:
    """Einspeiseverguetung-Felder — nur Eingabewert, keine Berechnung."""
    if not enabled:
        return {}
    return {
        _opt(CONF_EINSPEISEVERGUETUNG, d.get(CONF_EINSPEISEVERGUETUNG)): _preis(None),
    }


def _tiered_fields(d: dict, enabled: bool = True) -> dict:
    """Gibt Staffelpreis-Felder zurück — nur wenn im Land verfügbar."""
    if not enabled:
        return {}
    fields: dict = {}
    fields[vol.Required(CONF_TIERED, default=bool(d.get(CONF_TIERED, False)))] = (
        selector.BooleanSelector()
    )
    limits = d.get(CONF_TIER_LIMITS) or []
    prices = d.get(CONF_TIER_PRICES) or []
    for i in range(MAX_TIERS):
        limit_key = f"tier_limit_{i}"
        price_key = f"tier_price_{i}"
        default_limit = limits[i] if i < len(limits) else None
        default_price = prices[i] if i < len(prices) else None
        fields[_opt(limit_key, default_limit)] = selector.NumberSelector(
            selector.NumberSelectorConfig(min=0, step="any", mode=selector.NumberSelectorMode.BOX)
        )
        fields[_opt(price_key, default_price)] = selector.NumberSelector(
            selector.NumberSelectorConfig(min=0, step="any", mode=selector.NumberSelectorMode.BOX)
        )
    return fields


def _dynamischer_tarif_fields(d: dict[str, Any]) -> dict:
    """Dynamischer Tarif (Boersen-/Spotpreis): externer Preissensor + Aufschlag.

    Der manuell eingegebene Arbeitspreis bleibt als Fallback erhalten, falls
    fuer den Sensor noch keine ausreichende Statistik-Historie vorliegt."""
    return {
        _opt(CONF_ARBEITSPREIS_SENSOR, d.get(CONF_ARBEITSPREIS_SENSOR)): selector.EntitySelector(
            selector.EntitySelectorConfig(domain="sensor")
        ),
        _opt(CONF_ARBEITSPREIS_AUFSCHLAG, d.get(CONF_ARBEITSPREIS_AUFSCHLAG)): _preis(0.0001),
    }


def _tag_nacht_fields(d: dict, enabled: bool = True) -> dict:
    """Tag/Nacht-Felder (Economy 7, TOU) — nur wenn im Land verfügbar."""
    if not enabled:
        return {}
    return {
        _opt(CONF_ARBEITSPREIS_NACHT, d.get(CONF_ARBEITSPREIS_NACHT)): _preis(None),
        _opt(CONF_JAHRESVERBRAUCH_TAG, d.get(CONF_JAHRESVERBRAUCH_TAG)): selector.NumberSelector(
            selector.NumberSelectorConfig(min=0, step="any", mode=selector.NumberSelectorMode.BOX)
        ),
        _opt(CONF_JAHRESVERBRAUCH_NACHT, d.get(CONF_JAHRESVERBRAUCH_NACHT)): selector.NumberSelector(
            selector.NumberSelectorConfig(min=0, step="any", mode=selector.NumberSelectorMode.BOX)
        ),
    }


# ------------------------------------------------------------------- schemas
def _common_schema(
    hass: HomeAssistant,
    d: dict[str, Any],
    *,
    mit_name: bool,
    name: str | None = None,
) -> vol.Schema:
    """Schritt 1: für alle Sparten gleich. `name` ist der bisherige Name beim Bearbeiten."""
    fields: dict[Any, Any] = {}
    if mit_name:
        # FIX: vol.Required mit leerem String-Default → vol.Optional ohne Default
        # verhindert den 400-Fehler beim Laden des Config-Flows
        if name:
            fields[vol.Required("name", default=name)] = selector.TextSelector()
        else:
            fields[vol.Required("name")] = selector.TextSelector()
    fields[vol.Required(CONF_SPARTE, default=d.get(CONF_SPARTE, "electricity"))] = _select(
        SPARTEN, translation_key="sparte"
    )
    # FIX: leerer String-Default durch vol.Optional ersetzt
    if d.get(CONF_ANBIETER):
        fields[vol.Required(CONF_ANBIETER, default=d[CONF_ANBIETER])] = selector.TextSelector()
    else:
        fields[vol.Required(CONF_ANBIETER)] = selector.TextSelector()
    fields[_opt(CONF_KUNDENNUMMER, d.get(CONF_KUNDENNUMMER))] = selector.TextSelector()
    fields[_opt(CONF_TARIF, d.get(CONF_TARIF))] = selector.TextSelector()
    fields[_opt(CONF_BEGINN, d.get(CONF_BEGINN))] = selector.DateSelector()
    fields[_opt(CONF_ENDE, d.get(CONF_ENDE))] = selector.DateSelector()
    fields[
        vol.Required(
            CONF_ERINNERUNG_MONATE, default=d.get(CONF_ERINNERUNG_MONATE, "3")
        )
    ] = _select(ERINNERUNG_OPTIONS, translation_key="erinnerung")
    notify_options = _notify_options(hass)
    if notify_options:
        fields[_opt(CONF_NOTIFY_TARGET, d.get(CONF_NOTIFY_TARGET))] = _select(notify_options, custom=True)
    return vol.Schema(fields)


def _energie_schema(d: dict[str, Any], features: dict | None = None) -> vol.Schema:
    """Schritt 2 für Strom."""
    f = features or {}
    return vol.Schema(
        {
            vol.Required(
                CONF_ARBEITSPREIS, default=d.get(CONF_ARBEITSPREIS, 0.0)
            ): _preis(0.0001),
            **_dynamischer_tarif_fields(d),
            vol.Required(
                CONF_GRUNDPREIS, default=d.get(CONF_GRUNDPREIS, 0.0)
            ): _preis(0.01),
            vol.Required(
                CONF_ABSCHLAG, default=d.get(CONF_ABSCHLAG, 0.0)
            ): _preis(0.01),
            _opt(CONF_JAHRESVERBRAUCH, d.get(CONF_JAHRESVERBRAUCH)): _verbrauch(),
            _opt(CONF_VERBRAUCH_SENSOR, d.get(CONF_VERBRAUCH_SENSOR)): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor")
            ),
            **_verbrauch_start_wert_field(d),
            **_abschlag_warnung_fields(d),
            **_einspeisung_fields(d),
            _opt(CONF_BONUS, d.get(CONF_BONUS)): _preis(0.01),
            vol.Required(
                CONF_OEKOSTROM, default=bool(d.get(CONF_OEKOSTROM, False))
            ): selector.BooleanSelector(),
            _opt(CONF_ZAEHLERNUMMER, d.get(CONF_ZAEHLERNUMMER)): selector.TextSelector(),
            _opt(
                CONF_MARKTLOKATION, d.get(CONF_MARKTLOKATION)
            ): selector.TextSelector(),
            _opt(CONF_PREISGARANTIE, d.get(CONF_PREISGARANTIE)): selector.DateSelector(),
            **_tiered_fields(d, enabled=f.get("hat_tiered", False)),
            **_tag_nacht_fields(d, enabled=f.get("hat_tag_nacht", False)),
        }
    )


def _energie_ht_nt_schema(d: dict[str, Any], features: dict | None = None) -> vol.Schema:
    """Schritt 2 für Strom mit Zweizählertarif (Hoch-/Niedertarif).

    Identisch zu _energie_schema(), zusätzlich ein zweites Register
    (Arbeitspreis/Verbrauchssensor/manueller Zählerstand-Fallback/
    Zählernummer) für den Niedertarif. CONF_ARBEITSPREIS/CONF_VERBRAUCH_SENSOR/
    CONF_ZAEHLERNUMMER (ohne Suffix) bleiben dabei implizit der Hochtarif."""
    f = features or {}
    return vol.Schema(
        {
            vol.Required(
                CONF_ARBEITSPREIS, default=d.get(CONF_ARBEITSPREIS, 0.0)
            ): _preis(0.0001),
            vol.Required(
                CONF_ARBEITSPREIS_NT, default=d.get(CONF_ARBEITSPREIS_NT, 0.0)
            ): _preis(0.0001),
            **_dynamischer_tarif_fields(d),
            vol.Required(
                CONF_GRUNDPREIS, default=d.get(CONF_GRUNDPREIS, 0.0)
            ): _preis(0.01),
            vol.Required(
                CONF_ABSCHLAG, default=d.get(CONF_ABSCHLAG, 0.0)
            ): _preis(0.01),
            _opt(CONF_JAHRESVERBRAUCH, d.get(CONF_JAHRESVERBRAUCH)): _verbrauch(),
            _opt(CONF_VERBRAUCH_SENSOR, d.get(CONF_VERBRAUCH_SENSOR)): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor")
            ),
            **_verbrauch_start_wert_field(d),
            _opt(CONF_VERBRAUCH_SENSOR_NT, d.get(CONF_VERBRAUCH_SENSOR_NT)): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor")
            ),
            **_verbrauch_start_wert_field(d, key=CONF_VERBRAUCH_START_WERT_NT),
            **_abschlag_warnung_fields(d),
            **_einspeisung_fields(d),
            _opt(CONF_BONUS, d.get(CONF_BONUS)): _preis(0.01),
            vol.Required(
                CONF_OEKOSTROM, default=bool(d.get(CONF_OEKOSTROM, False))
            ): selector.BooleanSelector(),
            _opt(CONF_ZAEHLERNUMMER, d.get(CONF_ZAEHLERNUMMER)): selector.TextSelector(),
            _opt(CONF_ZAEHLERNUMMER_NT, d.get(CONF_ZAEHLERNUMMER_NT)): selector.TextSelector(),
            _opt(
                CONF_MARKTLOKATION, d.get(CONF_MARKTLOKATION)
            ): selector.TextSelector(),
            _opt(CONF_PREISGARANTIE, d.get(CONF_PREISGARANTIE)): selector.DateSelector(),
            **_tiered_fields(d, enabled=f.get("hat_tiered", False)),
        }
    )


def _gas_schema(d: dict[str, Any], features: dict | None = None) -> vol.Schema:
    """Schritt 2 für Gas."""
    f = features or {}
    return vol.Schema(
        {
            vol.Required(
                CONF_GAS_EINHEIT, default=d.get(CONF_GAS_EINHEIT, "m³")
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=GAS_EINHEITEN,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                CONF_ARBEITSPREIS, default=d.get(CONF_ARBEITSPREIS, 0.0)
            ): _preis(0.0001),
            vol.Required(
                CONF_GRUNDPREIS, default=d.get(CONF_GRUNDPREIS, 0.0)
            ): _preis(0.01),
            vol.Required(
                CONF_ABSCHLAG, default=d.get(CONF_ABSCHLAG, 0.0)
            ): _preis(0.01),
            _opt(CONF_JAHRESVERBRAUCH, d.get(CONF_JAHRESVERBRAUCH)): _verbrauch_m3(),
            _opt(CONF_VERBRAUCH_SENSOR, d.get(CONF_VERBRAUCH_SENSOR)): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor")
            ),
            **_verbrauch_start_wert_field(d),
            vol.Required(
                CONF_BRENNWERT, default=_dezimal_default(d.get(CONF_BRENNWERT, 11.0))
            ): _dezimal_feld(),
            vol.Required(
                CONF_ZUSTANDSZAHL, default=_dezimal_default(d.get(CONF_ZUSTANDSZAHL, 0.95))
            ): _dezimal_feld(),
            **_abschlag_warnung_fields(d),
            _opt(CONF_BONUS, d.get(CONF_BONUS)): _preis(0.01),
            vol.Required(
                CONF_OEKOSTROM, default=bool(d.get(CONF_OEKOSTROM, False))
            ): selector.BooleanSelector(),
            _opt(CONF_ZAEHLERNUMMER, d.get(CONF_ZAEHLERNUMMER)): selector.TextSelector(),
            _opt(
                CONF_MARKTLOKATION, d.get(CONF_MARKTLOKATION)
            ): selector.TextSelector(),
            _opt(CONF_PREISGARANTIE, d.get(CONF_PREISGARANTIE)): selector.DateSelector(),
            **_tiered_fields(d, enabled=f.get("hat_tiered", True)),
            **_tag_nacht_fields(d, enabled=f.get("hat_tag_nacht", False)),
        }
    )


def _zahlweise_von(d: dict[str, Any]) -> str:
    zahlweise = d.get(CONF_ZAHLWEISE)
    return zahlweise if zahlweise in ZAHLWEISE_MONATE else DEFAULT_ZAHLWEISE


def _versicherung_fields(d: dict[str, Any]) -> dict[Any, Any]:
    """Zusatzangaben einer Versicherung: Art und, fuer eine Kfz-Versicherung,
    Kennzeichen, Kilometerstand bei Vertragsbeginn und Kilometer pro Jahr.
    Alles optional und nur zur Dokumentation."""
    km = selector.NumberSelector(
        selector.NumberSelectorConfig(
            min=0, step=1, mode=selector.NumberSelectorMode.BOX, unit_of_measurement="km"
        )
    )
    return {
        _opt(CONF_VERSICHERUNGSART, d.get(CONF_VERSICHERUNGSART)): _select(
            VERSICHERUNGSARTEN, translation_key=CONF_VERSICHERUNGSART
        ),
        _opt(CONF_KENNZEICHEN, d.get(CONF_KENNZEICHEN)): selector.TextSelector(),
        _opt(CONF_KM_START, d.get(CONF_KM_START)): km,
        _opt(CONF_KM_PRO_JAHR, d.get(CONF_KM_PRO_JAHR)): km,
    }


def _pauschal_schema(d: dict[str, Any], *, versicherung: bool = False) -> vol.Schema:
    """Schritt 2 für Pauschalverträge (Internet, Mobilfunk, Versicherung, …); bei einer
    Versicherung zusätzlich mit den Versicherungsangaben.

    Der Betrag wird pro Zahlung eingegeben (monatlich, vierteljährlich, halbjährlich,
    jährlich); gespeichert wird weiter der Betrag pro Monat (siehe _pauschal_monatlich)."""
    zahlweise = _zahlweise_von(d)
    betrag = round(float(d.get(CONF_ABSCHLAG) or 0.0) * ZAHLWEISE_MONATE[zahlweise], 2)
    return vol.Schema(
        {
            vol.Required(CONF_ZAHLWEISE, default=zahlweise): _select(
                list(ZAHLWEISE_MONATE), translation_key="zahlweise"
            ),
            vol.Required(CONF_ABSCHLAG, default=betrag): _preis(0.01),
            _opt(CONF_ERSTE_ZAHLUNG, d.get(CONF_ERSTE_ZAHLUNG)): selector.DateSelector(),
            _opt(CONF_GRUNDPREIS, d.get(CONF_GRUNDPREIS)): _preis(0.01),
            **(_versicherung_fields(d) if versicherung else {}),
        }
    )


def _pauschal_monatlich(user_input: dict[str, Any]) -> dict[str, Any]:
    """Rechnet den Betrag pro Zahlung in den Monatsbetrag um, den die Integration speichert."""
    daten = dict(user_input)
    zahlweise = _zahlweise_von(daten)
    daten[CONF_ZAHLWEISE] = zahlweise
    if daten.get(CONF_ABSCHLAG) is not None:
        daten[CONF_ABSCHLAG] = round(float(daten[CONF_ABSCHLAG]) / ZAHLWEISE_MONATE[zahlweise], 6)
    return daten


def _wasser_schema(d: dict[str, Any], features: dict | None = None) -> vol.Schema:
    """Schritt 2 für Wasser (Frischwasser + optionales Abwasser, international)."""
    f = features or {}
    # Abwasser-Typ: länderspezifisch vorauswählen
    if not d.get(CONF_ABWASSER_TYP):
        if f.get("hat_abwasser_prozent"):
            default_typ = ABWASSER_TYP_PROZENT
        elif f.get("hat_abwasser_pauschal"):
            default_typ = ABWASSER_TYP_PAUSCHAL
        else:
            default_typ = ABWASSER_TYP_PREIS
    else:
        default_typ = d[CONF_ABWASSER_TYP]
    return vol.Schema(
        {
            vol.Required(
                CONF_WASSER_EINHEIT, default=d.get(CONF_WASSER_EINHEIT, "m³")
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=WASSER_EINHEITEN,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                CONF_ARBEITSPREIS, default=d.get(CONF_ARBEITSPREIS, 0.0)
            ): _preis(None),
            vol.Required(
                CONF_GRUNDPREIS, default=d.get(CONF_GRUNDPREIS, 0.0)
            ): _preis(None),
            vol.Required(
                CONF_ABSCHLAG, default=d.get(CONF_ABSCHLAG, 0.0)
            ): _preis(None),
            # Abwasser-Typ wählen
            vol.Required(
                CONF_ABWASSER_TYP, default=default_typ
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=ABWASSER_TYPEN,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            # Abwasser-Wert: Bedeutung abhängig vom Typ
            # price_per_unit: Preis/Einheit | percentage: % | flat_rate: €/Monat
            _opt(CONF_ARBEITSPREIS_ABWASSER, d.get(CONF_ARBEITSPREIS_ABWASSER)): _preis(None),
            _opt(CONF_JAHRESVERBRAUCH, d.get(CONF_JAHRESVERBRAUCH)): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0, step="any", mode=selector.NumberSelectorMode.BOX
                )
            ),
            _opt(CONF_VERBRAUCH_SENSOR, d.get(CONF_VERBRAUCH_SENSOR)): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor")
            ),
            **_verbrauch_start_wert_field(d),
            **_abschlag_warnung_fields(d),
            _opt(CONF_ZAEHLERNUMMER, d.get(CONF_ZAEHLERNUMMER)): selector.TextSelector(),
            **_tiered_fields(d, enabled=f.get("hat_tiered", True)),
        }
    )


def _next_schema(d: dict[str, Any], *, energie: bool, gas: bool = False, ht_nt: bool = False) -> vol.Schema:
    def k(b: str) -> str:
        return NEXT_PREFIX + b

    fields: dict[Any, Any] = {
        _opt(k(CONF_BEGINN), d.get(k(CONF_BEGINN))): selector.DateSelector(),
        _opt(k(CONF_ANBIETER), d.get(k(CONF_ANBIETER))): selector.TextSelector(),
        _opt(
            k(CONF_KUNDENNUMMER), d.get(k(CONF_KUNDENNUMMER))
        ): selector.TextSelector(),
        _opt(k(CONF_TARIF), d.get(k(CONF_TARIF))): selector.TextSelector(),
    }
    if energie:
        fields[_opt(k(CONF_ARBEITSPREIS), d.get(k(CONF_ARBEITSPREIS)))] = _preis(0.0001)
        if ht_nt:
            fields[_opt(k(CONF_ARBEITSPREIS_NT), d.get(k(CONF_ARBEITSPREIS_NT)))] = _preis(0.0001)
            fields[_opt(k(CONF_VERBRAUCH_SENSOR_NT), d.get(k(CONF_VERBRAUCH_SENSOR_NT)))] = (
                selector.EntitySelector(selector.EntitySelectorConfig(domain="sensor"))
            )
            fields[_opt(k(CONF_ZAEHLERNUMMER_NT), d.get(k(CONF_ZAEHLERNUMMER_NT)))] = (
                selector.TextSelector()
            )
        if not gas:
            fields[_opt(k(CONF_ARBEITSPREIS_SENSOR), d.get(k(CONF_ARBEITSPREIS_SENSOR)))] = (
                selector.EntitySelector(selector.EntitySelectorConfig(domain="sensor"))
            )
            fields[_opt(k(CONF_ARBEITSPREIS_AUFSCHLAG), d.get(k(CONF_ARBEITSPREIS_AUFSCHLAG)))] = (
                _preis(0.0001)
            )
        fields[_opt(k(CONF_GRUNDPREIS), d.get(k(CONF_GRUNDPREIS)))] = _preis(0.01)
        fields[_opt(k(CONF_ABSCHLAG), d.get(k(CONF_ABSCHLAG)))] = _preis(0.01)
        fields[_opt(k(CONF_JAHRESVERBRAUCH), d.get(k(CONF_JAHRESVERBRAUCH)))] = (
            _verbrauch()
        )
        if gas:
            # Neuer Gasanbieter/-mix kann einen anderen Brennwert/Zustandszahl
            # haben — bisher fehlten diese Felder hier komplett, wodurch der
            # alte Wert unveraendert in den neuen Vertrag uebernommen wurde.
            fields[
                vol.Optional(
                    k(CONF_GAS_EINHEIT), default=d.get(k(CONF_GAS_EINHEIT), "m³")
                )
            ] = selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=GAS_EINHEITEN, mode=selector.SelectSelectorMode.DROPDOWN,
                )
            )
            fields[
                vol.Optional(k(CONF_BRENNWERT), default=_dezimal_default(d.get(k(CONF_BRENNWERT), "")))
            ] = _dezimal_feld()
            fields[
                vol.Optional(k(CONF_ZUSTANDSZAHL), default=_dezimal_default(d.get(k(CONF_ZUSTANDSZAHL), "")))
            ] = _dezimal_feld()
    else:
        fields[_opt(k(CONF_ABSCHLAG), d.get(k(CONF_ABSCHLAG)))] = _preis(0.01)
        fields[_opt(k(CONF_GRUNDPREIS), d.get(k(CONF_GRUNDPREIS)))] = _preis(0.01)
    fields[_opt(k(CONF_ENDE), d.get(k(CONF_ENDE)))] = selector.DateSelector()
    return vol.Schema(fields)


# ------------------------------------------------------------------- flows
class TariffyConfigFlow(ConfigFlow, domain=DOMAIN):
    """Anlegen eines Vertrags in zwei Schritten."""

    VERSION = 1

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}
        self._entry_title: str = ""

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if user_input is not None:
            self._data = dict(user_input)
            self._entry_title = self._data.pop("name", "")
            if user_input[CONF_SPARTE] == GAS_SPARTE:
                return await self.async_step_gas()
            if user_input[CONF_SPARTE] == WASSER_SPARTE:
                return await self.async_step_wasser()
            if user_input[CONF_SPARTE] == SPARTE_ELECTRICITY_HT_NT:
                return await self.async_step_energie_ht_nt()
            if user_input[CONF_SPARTE] in ENERGIE_SPARTEN:
                return await self.async_step_energie()
            return await self.async_step_pauschal()
        return self.async_show_form(
            step_id="user", data_schema=_common_schema(self.hass, {}, mit_name=True)
        )

    async def async_step_import(self, import_data: dict[str, Any]) -> ConfigFlowResult:
        """Legt einen Vertrag aus einer Sicherung an (Name, Daten, Folgevertrag)."""
        try:
            contract = sanitize_contract(import_data)
        except BackupError:
            return self.async_abort(reason="invalid_backup")
        return self.async_create_entry(
            title=contract["title"], data=contract["data"], options=contract["options"]
        )

    async def async_step_energie(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if user_input is not None:
            data = {**self._data, **user_input}
            return self.async_create_entry(title=self._entry_title, data=data)
        return self.async_show_form(
            step_id="energie", data_schema=_energie_schema({}, _country_features(self.hass))
        )

    async def async_step_energie_ht_nt(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if user_input is not None:
            data = {**self._data, **user_input}
            return self.async_create_entry(title=self._entry_title, data=data)
        return self.async_show_form(
            step_id="energie_ht_nt",
            data_schema=_energie_ht_nt_schema({}, _country_features(self.hass)),
        )

    async def async_step_pauschal(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if user_input is not None:
            data = {**self._data, **_pauschal_monatlich(user_input)}
            return self.async_create_entry(title=self._entry_title, data=data)
        return self.async_show_form(
            step_id="pauschal",
            data_schema=_pauschal_schema(
                {}, versicherung=self._data.get(CONF_SPARTE) == SPARTE_INSURANCE
            ),
        )

    async def async_step_gas(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            errors = _validiere_dezimal_felder(user_input)
            if not errors:
                data = {**self._data, **user_input}
                return self.async_create_entry(title=self._entry_title, data=data)
        return self.async_show_form(
            step_id="gas",
            data_schema=_gas_schema(user_input or {}, _country_features(self.hass)),
            errors=errors,
        )

    async def async_step_wasser(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if user_input is not None:
            data = {**self._data, **user_input}
            return self.async_create_entry(title=self._entry_title, data=data)
        return self.async_show_form(
            step_id="wasser",
            data_schema=_wasser_schema({}, _country_features(self.hass))
        )

    # ---- Reconfigure (gleiche Zwei-Schritt-Logik) ----
    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        entry = self._get_reconfigure_entry()
        if user_input is not None:
            self._data = dict(user_input)
            # der Name ist der Titel des Vertrags, kein Vertragsdatum; leer = bleibt wie er ist
            self._entry_title = str(self._data.pop("name", "") or "").strip() or entry.title
            if user_input[CONF_SPARTE] == GAS_SPARTE:
                return await self.async_step_reconfigure_gas()
            if user_input[CONF_SPARTE] == WASSER_SPARTE:
                return await self.async_step_reconfigure_wasser()
            if user_input[CONF_SPARTE] == SPARTE_ELECTRICITY_HT_NT:
                return await self.async_step_reconfigure_energie_ht_nt()
            if user_input[CONF_SPARTE] in ENERGIE_SPARTEN:
                return await self.async_step_reconfigure_energie()
            return await self.async_step_reconfigure_pauschal()
        return self.async_show_form(
            step_id="reconfigure",
            data_schema=_common_schema(self.hass, dict(entry.data), mit_name=True, name=entry.title),
        )

    async def async_step_reconfigure_energie(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        entry = self._get_reconfigure_entry()
        if user_input is not None:
            neu = _keep_internal_state(
                entry.data, _stamp_abschlag_change(entry.data, {**self._data, **user_input})
            )
            return self.async_update_reload_and_abort(
                entry, title=self._entry_title or entry.title, data=neu
            )
        return self.async_show_form(
            step_id="reconfigure_energie",
            data_schema=_energie_schema(dict(entry.data), _country_features(self.hass)),
        )

    async def async_step_reconfigure_energie_ht_nt(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        entry = self._get_reconfigure_entry()
        if user_input is not None:
            neu = _keep_internal_state(
                entry.data, _stamp_abschlag_change(entry.data, {**self._data, **user_input})
            )
            return self.async_update_reload_and_abort(
                entry, title=self._entry_title or entry.title, data=neu
            )
        return self.async_show_form(
            step_id="reconfigure_energie_ht_nt",
            data_schema=_energie_ht_nt_schema(dict(entry.data), _country_features(self.hass)),
        )

    async def async_step_reconfigure_pauschal(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        entry = self._get_reconfigure_entry()
        if user_input is not None:
            neu = _keep_internal_state(
                entry.data,
                _stamp_abschlag_change(
                    entry.data, {**self._data, **_pauschal_monatlich(user_input)}
                ),
            )
            return self.async_update_reload_and_abort(
                entry, title=self._entry_title or entry.title, data=neu
            )
        return self.async_show_form(
            step_id="reconfigure_pauschal",
            data_schema=_pauschal_schema(
                dict(entry.data),
                versicherung=self._data.get(CONF_SPARTE, entry.data.get(CONF_SPARTE)) == SPARTE_INSURANCE,
            ),
        )

    async def async_step_reconfigure_gas(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        entry = self._get_reconfigure_entry()
        errors: dict[str, str] = {}
        if user_input is not None:
            errors = _validiere_dezimal_felder(user_input)
            if not errors:
                neu = _keep_internal_state(
                entry.data, _stamp_abschlag_change(entry.data, {**self._data, **user_input})
            )
                return self.async_update_reload_and_abort(
                entry, title=self._entry_title or entry.title, data=neu
            )
        return self.async_show_form(
            step_id="reconfigure_gas",
            data_schema=_gas_schema(user_input or dict(entry.data), _country_features(self.hass)),
            errors=errors,
        )

    async def async_step_reconfigure_wasser(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        entry = self._get_reconfigure_entry()
        if user_input is not None:
            neu = _keep_internal_state(
                entry.data, _stamp_abschlag_change(entry.data, {**self._data, **user_input})
            )
            return self.async_update_reload_and_abort(
                entry, title=self._entry_title or entry.title, data=neu
            )
        return self.async_show_form(
            step_id="reconfigure_wasser",
            data_schema=_wasser_schema(dict(entry.data), _country_features(self.hass)),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry) -> OptionsFlow:
        return TariffyOptionsFlow()


class TariffyOptionsFlow(OptionsFlowWithReload):
    """Den nächsten/zukünftigen Vertrag pflegen."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        gas = self.config_entry.data.get(CONF_SPARTE) == GAS_SPARTE
        errors: dict[str, str] = {}
        if user_input is not None:
            if gas:
                errors = _validiere_dezimal_felder(
                    user_input,
                    keys=(NEXT_PREFIX + CONF_BRENNWERT, NEXT_PREFIX + CONF_ZUSTANDSZAHL),
                )
            if not errors:
                if not user_input.get(NEXT_PREFIX + CONF_BEGINN):
                    return self.async_create_entry(title="", data={})
                cleaned = {
                    key: val for key, val in user_input.items() if val not in (None, "")
                }
                return self.async_create_entry(title="", data=cleaned)
        energie = self.config_entry.data.get(CONF_SPARTE) in ENERGIE_SPARTEN
        ht_nt = self.config_entry.data.get(CONF_SPARTE) == SPARTE_ELECTRICITY_HT_NT
        return self.async_show_form(
            step_id="init",
            data_schema=_next_schema(
                user_input or dict(self.config_entry.options), energie=energie, gas=gas, ht_nt=ht_nt
            ),
            errors=errors,
        )
