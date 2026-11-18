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
import re
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

from . import coordinator as coord
from .const import (
    ABSCHLAG_VERLAUF_MAX,
    CONF_ABSCHLAG,
    CONF_ABSCHLAG_VERLAUF,
    CONF_ANBIETER,
    CONF_ARBEITSPREIS,
    AUSSENZAEHLER_MAX,
    CONF_ARCHIVIERT,
    CONF_AUSSENZAEHLER,
    CONF_EFFEKTIVZINS,
    CONF_KREDIT_RATE,
    CONF_KREDIT_SUMME,
    CONF_LAUFZEIT_MONATE,
    CONF_SCHLUSSRATE,
    CONF_SOLLZINS,
    SPARTE_LOAN,
    CONF_BEGINN,
    CONF_BRENNWERT,
    CONF_EINMALPOSTEN,
    CONF_ENDE,
    EINMALPOSTEN_MAX,
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
    WASSER_SPARTE,
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
        delta = coord._pick_verbrauch_delta(
            end[0], start[0], end[1], start[1], await coord._einheit_faktor(hass, sensor)
        )
        if delta is None or delta < 0:
            return None, sensors
        total += delta
    return round(total, 2), sensors


async def async_calc(
    hass: HomeAssistant, entry: ConfigEntry, values: dict[str, Any], rows: Any = None
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

    # Abschlaege nach Monaten (optional): was in der alten Laufzeit wann wirklich gezahlt wurde
    plan = _verlauf_zeilen(rows, _intervall(entry), ende) if rows else []
    abschlag_gezahlt = number["abschlag_gezahlt"]
    if abschlag_gezahlt is None and plan and not metered:
        # Pauschalvertrag: gezaehlt wird jede Abbuchung der alten Laufzeit (ab dem Beginn, im Zahlungsrhythmus) mit
        # dem Betrag, der an ihrem Tag galt
        intervall = _intervall(entry)
        summe = 0.0
        for n in range(1200):
            termin = coord._plus_months(beginn, n * intervall)
            if termin > ende:
                break
            summe += round(coord._abschlag_am(plan, plan[-1][1], termin) * intervall, 2)
        abschlag_gezahlt = round(summe, 2)
    elif abschlag_gezahlt is None and plan:
        abschlag_gezahlt = round(coord._abschlag_aus_plan(plan, plan[-1][1], (ende - beginn).days / 30.44, beginn), 2)
    elif abschlag_gezahlt is None and number["abschlag"] is not None:
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
    hass: HomeAssistant, entry: ConfigEntry, values: dict[str, Any], rows: Any = None
) -> dict[str, Any]:
    """Der Eintrag fuer die Historie aus den eingegebenen und berechneten Werten."""
    calc = await async_calc(hass, entry, values, rows)
    plan = _verlauf_zeilen(rows, _intervall(entry), date.fromisoformat(str(values["ende"]))) if rows else []
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
        CONF_ABSCHLAG: number["abschlag"] if number["abschlag"] is not None or not plan else plan[-1][1],
        "kosten": calc["values"]["kosten"],
        "abschlag_gezahlt": calc["values"]["abschlag_gezahlt"],
        "saldo": calc["values"]["saldo"],
        "verbrauch": calc["values"]["verbrauch"],
        "manuell": True,
        "quelle": calc["source"],
        # was der Nutzer selbst eingetragen hat (der Rest wird beim Bearbeiten neu berechnet)
        "eigene": [name for name in AUTO_FIELDS if number[name] is not None],
    }
    if plan:  # damit sich die Abschlaege nach Monaten beim Bearbeiten wieder zeigen
        term["abschlag_verlauf"] = [{"ab": tag.isoformat(), "betrag": betrag} for tag, betrag in plan]
    return term


def _sorted(historie: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(historie, key=lambda term: str(term.get(CONF_BEGINN) or ""))


async def async_save_term(
    hass: HomeAssistant,
    entry: ConfigEntry,
    values: dict[str, Any],
    index: int | None = None,
    rows: Any = None,
) -> int:
    """Legt eine Laufzeit an oder ersetzt die mit `index`. Gibt ihre Position zurueck."""
    term = await async_build_term(hass, entry, values, rows)
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
    CONF_ABSCHLAG_VERLAUF,  # der Verlauf gehoert zur alten Laufzeit
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
    if entry.data.get(CONF_SPARTE) == SPARTE_LOAN:
        await _renew_kredit(hass, entry, values)
        return
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


async def _renew_kredit(hass: HomeAssistant, entry: ConfigEntry, values: dict[str, Any]) -> None:
    """Anschlussfinanzierung: die bisherige Laufzeit kommt in die Historie, der Kredit laeuft mit neuer
    Summe, neuem Zins und neuer Laufzeit weiter (die Summe ist meist die Restschuld)."""
    coordinator = entry.runtime_data
    try:
        beginn = date.fromisoformat(str(values.get("beginn")))
    except ValueError as err:
        raise HistoryError("invalid_dates") from err
    summe = _number(values.get(CONF_KREDIT_SUMME), "kredit_summe")
    if summe is None or summe <= 0:
        raise HistoryError("invalid_kredit_summe")
    laufzeit = _number(values.get(CONF_LAUFZEIT_MONATE), "laufzeit_monate")
    if laufzeit is None or laufzeit < 1:
        raise HistoryError("invalid_laufzeit_monate")
    soll = _number(values.get(CONF_SOLLZINS), "sollzins")
    effektiv = _number(values.get(CONF_EFFEKTIVZINS), "effektivzins")
    if soll is None and effektiv is None:
        raise HistoryError("invalid_zins")
    rate = _number(values.get(CONF_KREDIT_RATE), "kredit_rate")
    schluss = _number(values.get(CONF_SCHLUSSRATE), "schlussrate")
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
    reset = (*_RENEW_RESET, CONF_SOLLZINS, CONF_EFFEKTIVZINS, CONF_KREDIT_RATE, CONF_SCHLUSSRATE)
    data = {key: value for key, value in entry.data.items() if key not in reset}
    data.update(
        {
            CONF_BEGINN: beginn.isoformat(),
            CONF_KREDIT_SUMME: summe,
            CONF_LAUFZEIT_MONATE: int(laufzeit),
            CONF_ZAHLWEISE: zahlweise,
            CONF_HISTORIE: _sorted(historie)[-HISTORIE_MAX:],
        }
    )
    data.pop(CONF_ENDE, None)  # the end follows from the start and the term
    for key, wert in (
        (CONF_SOLLZINS, soll),
        (CONF_EFFEKTIVZINS, effektiv),
        (CONF_KREDIT_RATE, rate),
        (CONF_SCHLUSSRATE, schluss),
        (CONF_ERSTE_ZAHLUNG, erste if erste not in (None, "") else None),
    ):
        if wert is not None:
            data[key] = wert
    await coordinator._dismiss_notifications()
    hass.config_entries.async_update_entry(entry, data=data)


# ------------------------------------------------------------ Abschlagsverlauf
def _verlauf_zeilen(rows: Any, intervall: int, bis: date) -> list[tuple[date, float]]:
    """Die Zeilen `{"ab": Datum, "betrag": Betrag je Zahlung}` eines Abschlagsverlaufs, aufsteigend nach Datum, mit
    dem Betrag je Monat. Nur Tage bis `bis`, jeder Tag einmal, Betrag ueber null, hoechstens ABSCHLAG_VERLAUF_MAX."""
    if not isinstance(rows, list):
        raise HistoryError("invalid_dates")
    if len(rows) > ABSCHLAG_VERLAUF_MAX:
        raise HistoryError("too_many")
    je_tag: dict[date, float] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise HistoryError("invalid_dates")
        try:
            tag = date.fromisoformat(str(row.get("ab")))
        except ValueError as err:
            raise HistoryError("invalid_dates") from err
        if tag > bis or tag in je_tag:
            raise HistoryError("invalid_dates")
        betrag = _number(row.get("betrag"), "abschlag")
        if betrag is None or betrag <= 0:
            raise HistoryError("invalid_abschlag")
        je_tag[tag] = round(betrag / intervall, 6)
    return sorted(je_tag.items())


def _intervall(entry: ConfigEntry) -> int:
    return ZAHLWEISE_MONATE.get(entry.data.get(CONF_ZAHLWEISE), ZAHLWEISE_MONATE["monthly"])


def save_abschlag_verlauf(hass: HomeAssistant, entry: ConfigEntry, rows: Any) -> None:
    """Setzt den Abschlagsverlauf (siehe const.CONF_ABSCHLAG_VERLAUF) auf die uebergebenen Zeilen; eine leere
    Liste entfernt ihn. Der Betrag der letzten Zeile ist danach der aktuelle Abschlag des Vertrags."""
    if entry.data.get(CONF_SPARTE) == SPARTE_LOAN:
        raise HistoryError("not_available")
    plan = _verlauf_zeilen(rows, _intervall(entry), dt_util.now().date())  # nur Vergangenes
    data = dict(entry.data)
    if not plan:
        data.pop(CONF_ABSCHLAG_VERLAUF, None)
    else:
        data[CONF_ABSCHLAG_VERLAUF] = [{"ab": tag.isoformat(), "betrag": betrag} for tag, betrag in plan]
        data[CONF_ABSCHLAG] = plan[-1][1]
    hass.config_entries.async_update_entry(entry, data=data)


# ------------------------------------------------------------ Einmalposten
def _einmal_posten(values: dict[str, Any]) -> dict[str, Any]:
    bezeichnung = str(values.get("bezeichnung") or "").strip()[:100]
    if not bezeichnung:
        raise HistoryError("invalid_bezeichnung")
    betrag = _number(values.get("betrag"), "betrag", negative=True)
    if betrag is None or betrag == 0:
        raise HistoryError("invalid_betrag")
    datum = values.get("datum")
    if datum in (None, ""):
        datum = None
    else:
        try:
            datum = date.fromisoformat(str(datum)).isoformat()
        except ValueError as err:
            raise HistoryError("invalid_dates") from err
    return {"bezeichnung": bezeichnung, "betrag": round(betrag, 2), "datum": datum}


def save_einmal(
    hass: HomeAssistant, entry: ConfigEntry, values: dict[str, Any], index: int | None = None
) -> None:
    """Legt einen Einmalposten an oder ersetzt den mit `index`."""
    posten = _einmal_posten(values)
    liste = list(entry.data.get(CONF_EINMALPOSTEN) or [])
    if index is not None:
        if not 0 <= index < len(liste):
            raise HistoryError("not_found")
        liste[index] = posten
    else:
        if len(liste) >= EINMALPOSTEN_MAX:
            raise HistoryError("too_many")
        liste.append(posten)
    hass.config_entries.async_update_entry(entry, data={**entry.data, CONF_EINMALPOSTEN: liste})


def delete_einmal(hass: HomeAssistant, entry: ConfigEntry, index: int) -> None:
    liste = list(entry.data.get(CONF_EINMALPOSTEN) or [])
    if not 0 <= index < len(liste):
        raise HistoryError("not_found")
    del liste[index]
    data = dict(entry.data)
    if liste:
        data[CONF_EINMALPOSTEN] = liste
    else:
        data.pop(CONF_EINMALPOSTEN, None)
    hass.config_entries.async_update_entry(entry, data=data)


# ------------------------------------------------------- Aussenzaehler (Wasser)
_ENTITY_ID = re.compile(r"^[a-z0-9_]+\.[a-z0-9_]+$")


def _aussenzaehler(values: dict[str, Any], haupt: str | None) -> dict[str, Any]:
    name = str(values.get("name") or "").strip()[:100]
    if not name:
        raise HistoryError("invalid_name")
    sensor = str(values.get("sensor") or "").strip().lower()
    if not _ENTITY_ID.match(sensor) or len(sensor) > 255:
        raise HistoryError("invalid_sensor")
    if sensor == haupt:
        raise HistoryError("same_sensor")
    eintrag: dict[str, Any] = {"name": name, "sensor": sensor}
    start = _number(values.get("start_wert"), "start_wert")
    if start is not None:
        eintrag["start_wert"] = start
    preis = _number(values.get("preis"), "preis")
    if preis is not None:
        eintrag["preis"] = preis
    return eintrag


def save_aussenzaehler(
    hass: HomeAssistant, entry: ConfigEntry, values: dict[str, Any], index: int | None = None
) -> bool:
    """Legt einen Aussenzaehler an oder ersetzt den mit `index`. Nur fuer Wasservertraege.
    Gibt zurueck, ob sich dadurch aendert, ob der Vertrag Aussenzaehler hat (dann muss er neu laden,
    damit die zusaetzlichen Sensoren entstehen)."""
    if entry.data.get(CONF_SPARTE) != WASSER_SPARTE:
        raise HistoryError("not_available")
    eintrag = _aussenzaehler(values, entry.data.get(CONF_VERBRAUCH_SENSOR))
    liste = list(entry.data.get(CONF_AUSSENZAEHLER) or [])
    war_leer = not liste
    if index is not None:
        if not 0 <= index < len(liste):
            raise HistoryError("not_found")
        liste[index] = eintrag
    else:
        if len(liste) >= AUSSENZAEHLER_MAX:
            raise HistoryError("too_many")
        liste.append(eintrag)
    hass.config_entries.async_update_entry(entry, data={**entry.data, CONF_AUSSENZAEHLER: liste})
    return war_leer


def delete_aussenzaehler(hass: HomeAssistant, entry: ConfigEntry, index: int) -> bool:
    """Loescht einen Aussenzaehler; gibt zurueck, ob es der letzte war."""
    liste = list(entry.data.get(CONF_AUSSENZAEHLER) or [])
    if not 0 <= index < len(liste):
        raise HistoryError("not_found")
    del liste[index]
    data = dict(entry.data)
    if liste:
        data[CONF_AUSSENZAEHLER] = liste
    else:
        data.pop(CONF_AUSSENZAEHLER, None)
    hass.config_entries.async_update_entry(entry, data=data)
    return not liste
