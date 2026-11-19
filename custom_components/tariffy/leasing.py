"""Leasing (Issue 90): Kilometerstand gegen die vereinbarten Kilometer.

Reine Rechnung ohne Home Assistant. Ein Leasingvertrag erlaubt eine Gesamtfahrleistung ueber die Laufzeit
(Kilometer pro Jahr mal Laufzeit oder ein Gesamtwert). Zur Rueckgabe werden Mehrkilometer nachberechnet
und Minderkilometer gutgeschrieben, meist erst ausserhalb einer Toleranz (Freigrenze):

    Abweichung = Fahrleistung bei Rueckgabe - erlaubte Gesamtkilometer
    Mehrkilometer   = max(0, Abweichung - Toleranz oben)
    Minderkilometer = max(0, -Abweichung - Toleranz unten)

Die Fahrleistung bei Rueckgabe wird aus dem bisherigen Schnitt je Tag hochgerechnet. Die Rate selbst ist
ein normaler Pauschalbetrag und steht nicht hier.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from .const import (
    CONF_BEGINN,
    CONF_ENDE,
    CONF_KM_AKTUELL,
    CONF_KM_GESAMT,
    CONF_KM_PRO_JAHR,
    CONF_KM_START,
    CONF_KM_TOL_OBEN,
    CONF_KM_TOL_UNTEN,
    CONF_PREIS_MEHRKM,
    CONF_PREIS_MINDERKM,
)

# Weniger Tage reichen fuer eine Hochrechnung nicht (ein Tag Fahrt ergaebe sonst Unsinn)
MIN_TAGE = 14


def _zahl(wert: Any) -> float | None:
    try:
        zahl = float(wert)
    except (TypeError, ValueError):
        return None
    return zahl if zahl == zahl else None


def _datum(wert: Any) -> date | None:
    if isinstance(wert, date):
        return wert
    try:
        return date.fromisoformat(str(wert)) if wert else None
    except ValueError:
        return None


def erlaubt_gesamt(data: dict[str, Any], gesamttage: int) -> float | None:
    """Erlaubte Gesamtkilometer: der eingetragene Gesamtwert, sonst Kilometer pro Jahr mal Laufzeit."""
    gesamt = _zahl(data.get(CONF_KM_GESAMT))
    if gesamt is not None and gesamt > 0:
        return gesamt
    je_jahr = _zahl(data.get(CONF_KM_PRO_JAHR))
    if je_jahr is not None and je_jahr > 0 and gesamttage > 0:
        return round(je_jahr * gesamttage / 365.25, 0)
    return None


def berechne(data: dict[str, Any], heute: date, km_sensor: float | None) -> dict[str, Any]:
    """Alle Kilometerwerte eines Leasingvertrags zum Stichtag. Leer, wenn der Kilometerstand fehlt.

    `km_sensor`: aktueller Stand des Kilometerzaehlers aus Home Assistant; er hat Vorrang vor dem
    von Hand eingetragenen Stand."""
    aktuell = km_sensor if km_sensor is not None else _zahl(data.get(CONF_KM_AKTUELL))
    start = _zahl(data.get(CONF_KM_START)) or 0.0
    beginn = _datum(data.get(CONF_BEGINN))
    ende = _datum(data.get(CONF_ENDE))
    gesamttage = (ende - beginn).days if beginn and ende and ende > beginn else 0
    erlaubt = erlaubt_gesamt(data, gesamttage)
    ergebnis: dict[str, Any] = {"leasing_km_erlaubt": erlaubt}
    if aktuell is None or aktuell < start:
        return ergebnis
    gefahren = aktuell - start
    ergebnis.update({"leasing_km_stand": round(aktuell, 0), "leasing_km_gefahren": round(gefahren, 0)})
    if erlaubt is None or not gesamttage or beginn is None:
        return ergebnis

    vergangen = min(max((heute - beginn).days, 0), gesamttage)
    rest_tage = max(gesamttage - vergangen, 0)
    soll = erlaubt * vergangen / gesamttage
    ergebnis.update(
        {
            "leasing_km_soll": round(soll, 0),
            "leasing_km_abweichung": round(gefahren - soll, 0),
            "leasing_km_rest": round(erlaubt - gefahren, 0),
            "leasing_km_rest_je_tag": round((erlaubt - gefahren) / rest_tage, 1) if rest_tage else None,
            "leasing_km_je_tag": round(gefahren / vergangen, 1) if vergangen else None,
            "leasing_km_prozent": round(gefahren / erlaubt * 100, 1) if erlaubt else None,
        }
    )
    if vergangen < MIN_TAGE:
        return ergebnis  # zu frueh fuer eine belastbare Hochrechnung

    hochgerechnet = gefahren / vergangen * gesamttage if vergangen else gefahren
    abweichung = hochgerechnet - erlaubt
    oben = max(_zahl(data.get(CONF_KM_TOL_OBEN)) or 0.0, 0.0)
    unten = max(_zahl(data.get(CONF_KM_TOL_UNTEN)) or 0.0, 0.0)
    mehr = max(0.0, abweichung - oben)
    minder = max(0.0, -abweichung - unten)
    preis_mehr = _zahl(data.get(CONF_PREIS_MEHRKM))
    preis_minder = _zahl(data.get(CONF_PREIS_MINDERKM))
    nachzahlung = mehr * preis_mehr if preis_mehr else None
    gutschrift = minder * preis_minder if preis_minder else None
    if nachzahlung is None and gutschrift is None:
        saldo = None
    else:
        saldo = (nachzahlung or 0.0) - (gutschrift or 0.0)
    ergebnis.update(
        {
            "leasing_km_hochgerechnet": round(hochgerechnet, 0),
            "leasing_km_abweichung_ende": round(abweichung, 0),
            "leasing_mehr_km": round(mehr, 0),
            "leasing_minder_km": round(minder, 0),
            "leasing_nachzahlung": round(nachzahlung, 2) if nachzahlung is not None else None,
            "leasing_gutschrift": round(gutschrift, 2) if gutschrift is not None else None,
            "leasing_km_kosten": round(saldo, 2) if saldo is not None else None,
        }
    )
    return ergebnis
