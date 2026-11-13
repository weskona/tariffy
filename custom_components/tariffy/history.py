"""Alte Laufzeiten von Hand in die Vertragshistorie eintragen.

Der Nutzer gibt Zeitraum, Anbieter, Tarif, Preise und Abschlag einer frueheren
Laufzeit ein. Verbrauch, Kosten, gezahlte Abschlaege und Saldo werden, soweit
moeglich, automatisch ermittelt: der Verbrauch aus den Langzeitstatistiken des
Zaehlers, der Rest daraus berechnet. Jeder dieser Werte kann auch selbst
eingetragen werden und hat dann Vorrang.

Es werden nur Werte gespeichert, die das Panel ohnehin zeigt (keine Kunden- oder
Zaehlernummern).
"""

from __future__ import annotations

from datetime import date, timedelta
import math
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

from . import coordinator as coord
from .const import (
    CONF_ABSCHLAG,
    CONF_ANBIETER,
    CONF_ARBEITSPREIS,
    CONF_ARCHIVIERT,
    CONF_BEGINN,
    CONF_BRENNWERT,
    CONF_ENDE,
    CONF_ERSTE_ZAHLUNG,
    CONF_GRUNDPREIS,
    CONF_HISTORIE,
    CONF_SPARTE,
    CONF_TARIF,
    CONF_ZAHLWEISE,
    CONF_VERBRAUCH_SENSOR,
    CONF_VERBRAUCH_SENSOR_NT,
    CONF_ZUSTANDSZAHL,
    GAS_SPARTE,
    HISTORIE_MAX,
    METERED_SPARTEN,
    ZAHLWEISE_MONATE,
)

METERED = METERED_SPARTEN
NUMBER_FIELDS = (
    "arbeitspreis",
    "grundpreis",
    "abschlag",
    "verbrauch",
    "kosten",
    "abschlag_gezahlt",
    "saldo",
)
AUTO_FIELDS = ("verbrauch", "kosten", "abschlag_gezahlt", "saldo")
TEXT_FIELDS = ("anbieter", "tarif")


class HistoryError(ValueError):
    """Eingabe nicht brauchbar; `code` steht fuer die Meldung des Panels."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def _number(value: Any, name: str, *, negative: bool = False) -> float | None:
    if value in (None, ""):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError) as err:
        raise HistoryError(f"invalid_{name}") from err
    if not math.isfinite(number) or (number < 0 and not negative):
        raise HistoryError(f"invalid_{name}")
    return number


def _dates(values: dict[str, Any]) -> tuple[date, date]:
    try:
        beginn = date.fromisoformat(str(values.get("beginn")))
        ende = date.fromisoformat(str(values.get("ende")))
    except ValueError as err:
        raise HistoryError("invalid_dates") from err
    if ende < beginn:
        raise HistoryError("invalid_dates")
    return beginn, ende


async def _verbrauch_aus_statistik(
    hass: HomeAssistant, entry: ConfigEntry, beginn: date, ende: date
) -> tuple[float | None, list[str]]:
    """Verbrauch zwischen Beginn und Ende (einschliesslich) aus den Statistiken des
    Zaehlers, wie ihn auch der Coordinator fuer den laufenden Vertrag bestimmt."""
    sensors = [
        sensor
        for sensor in (
            entry.data.get(CONF_VERBRAUCH_SENSOR),
            entry.data.get(CONF_VERBRAUCH_SENSOR_NT),
        )
        if sensor
    ]
    if not sensors:
        return None, []
    total = 0.0
    for sensor in sensors:
        start = await coord._get_historic_value(hass, sensor, beginn)
        end = await coord._get_historic_value(hass, sensor, ende + timedelta(days=1))
        delta = coord._pick_verbrauch_delta(end[0], start[0], end[1], start[1])
        if delta is None or delta < 0:
            return None, sensors
        total += delta
    return round(total, 2), sensors


async def async_calc(
    hass: HomeAssistant, entry: ConfigEntry, values: dict[str, Any]
) -> dict[str, Any]:
    """Alle Werte einer Laufzeit: eingetragene bleiben, leere werden berechnet.

    Rueckgabe: `values` (die vier berechneten Felder), `source` (woher der Verbrauch
    kommt: "manual", "statistics" oder None), `sensors`, `months`."""
    beginn, ende = _dates(values)
    months = round((ende - beginn).days / 30.44, 2)
    number = {name: _number(values.get(name), name, negative=name == "saldo") for name in NUMBER_FIELDS}
    sparte = entry.data.get(CONF_SPARTE)
    metered = sparte in METERED

    verbrauch = number["verbrauch"]
    source = "manual" if verbrauch is not None else None
    sensors: list[str] = []
    if metered and verbrauch is None:
        verbrauch, sensors = await _verbrauch_aus_statistik(hass, entry, beginn, ende)
        source = "statistics" if verbrauch is not None else None
    if not metered:
        verbrauch = None
        source = None

    abschlag_gezahlt = number["abschlag_gezahlt"]
    if abschlag_gezahlt is None and number["abschlag"] is not None:
        abschlag_gezahlt = round(number["abschlag"] * months, 2)

    kosten = number["kosten"]
    if kosten is None:
        if not metered:
            kosten = abschlag_gezahlt
        elif verbrauch is not None and number["arbeitspreis"] is not None:
            menge = verbrauch
            brennwert = coord._f(entry.data.get(CONF_BRENNWERT))
            zustandszahl = coord._f(entry.data.get(CONF_ZUSTANDSZAHL))
            if sparte == GAS_SPARTE and brennwert and zustandszahl:
                menge = verbrauch * brennwert * zustandszahl
            kosten = round(
                menge * number["arbeitspreis"] + (number["grundpreis"] or 0) * months, 2
            )

    saldo = number["saldo"]
    if saldo is None and metered and kosten is not None and abschlag_gezahlt is not None:
        saldo = round(abschlag_gezahlt - kosten, 2)

    return {
        "values": {
            "verbrauch": verbrauch,
            "kosten": kosten,
            "abschlag_gezahlt": abschlag_gezahlt,
            "saldo": saldo,
        },
        "source": source,
        "sensors": sensors,
        "months": months,
    }


async def async_build_term(
    hass: HomeAssistant, entry: ConfigEntry, values: dict[str, Any]
) -> dict[str, Any]:
    """Der Eintrag fuer die Historie aus den eingegebenen und berechneten Werten."""
    calc = await async_calc(hass, entry, values)
    number = {name: _number(values.get(name), name, negative=name == "saldo") for name in NUMBER_FIELDS}
    text = {name: str(values.get(name) or "").strip()[:100] or None for name in TEXT_FIELDS}
    term = {
        "sparte": entry.data.get(CONF_SPARTE),
        CONF_ANBIETER: text["anbieter"],
        CONF_TARIF: text["tarif"],
        CONF_BEGINN: str(values["beginn"]),
        CONF_ENDE: str(values["ende"]),
        CONF_ARBEITSPREIS: number["arbeitspreis"],
        CONF_GRUNDPREIS: number["grundpreis"],
        CONF_ABSCHLAG: number["abschlag"],
        "kosten": calc["values"]["kosten"],
        "abschlag_gezahlt": calc["values"]["abschlag_gezahlt"],
        "saldo": calc["values"]["saldo"],
        "verbrauch": calc["values"]["verbrauch"],
        "manuell": True,
        "quelle": calc["source"],
        # was der Nutzer selbst eingetragen hat (der Rest wird beim Bearbeiten neu berechnet)
        "eigene": [name for name in AUTO_FIELDS if number[name] is not None],
    }
    return term


def _sorted(historie: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(historie, key=lambda term: str(term.get(CONF_BEGINN) or ""))


async def async_save_term(
    hass: HomeAssistant,
    entry: ConfigEntry,
    values: dict[str, Any],
    index: int | None = None,
) -> int:
    """Legt eine Laufzeit an oder ersetzt die mit `index`. Gibt ihre Position zurueck."""
    term = await async_build_term(hass, entry, values)
    historie = list(entry.data.get(CONF_HISTORIE) or [])
    if index is not None:
        if not 0 <= index < len(historie):
            raise HistoryError("not_found")
        old = historie[index]
        if old.get("archiviert"):  # die Markierung des Archivierens bleibt erhalten
            term["archiviert"] = True
        historie[index] = term
    else:
        if len(historie) >= HISTORIE_MAX:
            raise HistoryError("too_many")
        historie.append(term)
    historie = _sorted(historie)
    hass.config_entries.async_update_entry(entry, data={**entry.data, CONF_HISTORIE: historie})
    return historie.index(term)


def delete_term(hass: HomeAssistant, entry: ConfigEntry, index: int) -> None:
    historie = list(entry.data.get(CONF_HISTORIE) or [])
    if not 0 <= index < len(historie):
        raise HistoryError("not_found")
    del historie[index]
    data = dict(entry.data)
    if historie:
        data[CONF_HISTORIE] = historie
    else:
        data.pop(CONF_HISTORIE, None)
    hass.config_entries.async_update_entry(entry, data=data)


# Zustand des alten Vertragsabschnitts, der beim Verlaengern nicht in die neue Laufzeit mitgeht
_RENEW_RESET = (
    "_kuendigung_bestaetigt",
    "_notify_gesendet",
    "_abschlag_ab_datum",
    "_abschlag_vorheriger_wert",
    "_abschlag_warnung_bestaetigt",
    "_abschlag_warnung_notify_gesendet",
    CONF_ARCHIVIERT,
    CONF_ERSTE_ZAHLUNG,
)


async def async_renew(hass: HomeAssistant, entry: ConfigEntry, values: dict[str, Any]) -> None:
    """Verlaengert einen Pauschalvertrag (Versicherung, Internet, ...): die bisherige Laufzeit
    kommt in die Historie, der Vertrag laeuft mit neuem Beginn, Ende und Betrag weiter."""
    coordinator = entry.runtime_data
    if not (coordinator.data or {}).get("verlaengerbar"):
        raise HistoryError("not_available")
    beginn, ende = _dates(values)
    if ende <= beginn:
        raise HistoryError("invalid_dates")
    betrag = _number(values.get("abschlag"), "abschlag")
    if betrag is None or betrag <= 0:
        raise HistoryError("invalid_abschlag")
    zahlweise = values.get(CONF_ZAHLWEISE) or entry.data.get(CONF_ZAHLWEISE) or "monthly"
    if zahlweise not in ZAHLWEISE_MONATE:
        raise HistoryError("invalid_zahlweise")

    erste = values.get("erste_zahlung")
    if erste not in (None, ""):
        try:
            erste = date.fromisoformat(str(erste)).isoformat()
        except ValueError as err:
            raise HistoryError("invalid_dates") from err

    historie = list(entry.data.get(CONF_HISTORIE) or [])
    historie.append(coordinator._historie_eintrag(dt_util.now().date()))
    data = {key: value for key, value in entry.data.items() if key not in _RENEW_RESET}
    if erste not in (None, ""):
        data[CONF_ERSTE_ZAHLUNG] = erste
    data.update(
        {
            CONF_BEGINN: beginn.isoformat(),
            CONF_ENDE: ende.isoformat(),
            CONF_ABSCHLAG: round(betrag / ZAHLWEISE_MONATE[zahlweise], 6),
            CONF_ZAHLWEISE: zahlweise,
            CONF_HISTORIE: _sorted(historie)[-HISTORIE_MAX:],
        }
    )
    await coordinator._dismiss_notifications()
    hass.config_entries.async_update_entry(entry, data=data)
