"""Kredit / Finanzierung: Tilgungsplan eines Annuitaetendarlehens.

Reine Rechnung ohne Home Assistant. Aus Summe, Zins, Laufzeit und Zahlweise ergibt sich der
Plan: jede Rate besteht aus Zinsen (auf die Restschuld) und Tilgung; die Restschuld sinkt
von Rate zu Rate, der Zinsanteil mit ihr. Eine eingetragene Rate hat Vorrang vor der
berechneten; eine Schlussrate bzw. ein Restwert wird am Ende gezahlt.

Der Zins je Zahlung ist der Sollzins (nominal) geteilt durch die Zahlungen pro Jahr, so wie
Banken die Rate rechnen. Fehlt der Sollzins, wird er aus dem effektiven Jahreszins abgeleitet.
Der Plan ist bewusst einfach: keine Sondertilgungen, ein fester Zins ueber die ganze Laufzeit.
"""

from __future__ import annotations

import calendar
from datetime import date
from typing import Any

from .const import (
    CONF_BEGINN,
    CONF_EFFEKTIVZINS,
    CONF_ERSTE_ZAHLUNG,
    CONF_KREDIT_RATE,
    CONF_KREDIT_SUMME,
    CONF_LAUFZEIT_MONATE,
    CONF_SCHLUSSRATE,
    CONF_SOLLZINS,
    CONF_ZAHLWEISE,
    DEFAULT_ZAHLWEISE,
    ZAHLWEISE_MONATE,
)

# Eine eingetragene Rate, die um mehr als diesen Anteil von der berechneten abweicht, wird gemeldet.
ABWEICHUNG_SCHWELLE = 0.01


def _zahl(wert: Any) -> float | None:
    try:
        zahl = float(wert)
    except (TypeError, ValueError):
        return None
    return zahl if zahl == zahl else None  # NaN raus


def _datum(wert: Any) -> date | None:
    try:
        return date.fromisoformat(str(wert)) if wert else None
    except ValueError:
        return None


def plus_monate(tag: date, monate: int) -> date:
    index = tag.month - 1 + monate
    jahr = tag.year + index // 12
    monat = index % 12 + 1
    return date(jahr, monat, min(tag.day, calendar.monthrange(jahr, monat)[1]))


def periodenzins(sollzins: float | None, effektivzins: float | None, intervall: int) -> float | None:
    """Zinssatz je Zahlung (Anteil, nicht Prozent). Der Sollzins gilt als nominal pro Jahr; ohne ihn
    wird der Satz aus dem effektiven Jahreszins abgeleitet. None, wenn beides fehlt."""
    if sollzins is not None:
        return sollzins / 100 * intervall / 12
    if effektivzins is not None:
        return (1 + effektivzins / 100) ** (intervall / 12) - 1
    return None


def annuitaet(summe: float, satz: float, anzahl: int, schluss: float = 0.0) -> float:
    """Gleichbleibende Rate, die `summe` in `anzahl` Zahlungen bis auf `schluss` tilgt."""
    if anzahl <= 0:
        return summe
    if satz <= 0:
        return (summe - schluss) / anzahl
    faktor = (1 + satz) ** anzahl
    return (summe - schluss / faktor) * satz * faktor / (faktor - 1)


def plan(summe: float, satz: float, rate: float, anzahl: int) -> tuple[list[dict[str, float]], float]:
    """Der Tilgungsplan: je Zahlung Zinsen, Tilgung und Restschuld danach. Gibt auch die Restschuld
    nach der letzten Zahlung zurueck (die Schlussrate). Ist die Schuld frueher getilgt, endet der Plan."""
    zahlungen: list[dict[str, float]] = []
    rest = summe
    for _ in range(anzahl):
        if rest <= 0.005:
            break
        zins = rest * satz
        tilgung = min(rate - zins, rest)
        rest -= tilgung
        zahlungen.append({"zins": zins, "tilgung": tilgung, "rest": max(rest, 0.0)})
    return zahlungen, max(rest, 0.0)


def berechne(data: dict[str, Any], heute: date) -> dict[str, Any]:
    """Alle Werte eines Kredits zum Stichtag. Leer, wenn Summe, Laufzeit oder Zins fehlen."""
    summe = _zahl(data.get(CONF_KREDIT_SUMME))
    laufzeit = _zahl(data.get(CONF_LAUFZEIT_MONATE))
    soll = _zahl(data.get(CONF_SOLLZINS))
    effektiv = _zahl(data.get(CONF_EFFEKTIVZINS))
    beginn = _datum(data.get(CONF_BEGINN))
    zahlweise = data.get(CONF_ZAHLWEISE)
    intervall = ZAHLWEISE_MONATE.get(zahlweise, ZAHLWEISE_MONATE[DEFAULT_ZAHLWEISE])
    ergebnis: dict[str, Any] = {"ende": plus_monate(beginn, int(laufzeit)) if (beginn and laufzeit) else None}
    if not summe or summe <= 0 or not laufzeit or laufzeit < 1 or beginn is None:
        return ergebnis
    satz = periodenzins(soll, effektiv, intervall)
    if satz is None or satz < 0:
        return ergebnis

    anzahl = max(1, round(laufzeit / intervall))
    schluss_eingabe = max(_zahl(data.get(CONF_SCHLUSSRATE)) or 0.0, 0.0)
    berechnet = annuitaet(summe, satz, anzahl, schluss_eingabe)
    eingegeben = _zahl(data.get(CONF_KREDIT_RATE))
    rate = eingegeben if eingegeben and eingegeben > 0 else berechnet
    zahlungen, schlussrate = plan(summe, satz, rate, anzahl)
    erste = _datum(data.get(CONF_ERSTE_ZAHLUNG)) or plus_monate(beginn, intervall)

    termine = [plus_monate(erste, i * intervall) for i in range(len(zahlungen))]
    # Die Schlussrate wird mit der letzten Rate gezahlt
    for eintrag in zahlungen:
        eintrag["betrag"] = eintrag["zins"] + eintrag["tilgung"]
    if zahlungen and schlussrate > 0.005:
        zahlungen[-1]["betrag"] += schlussrate
        zahlungen[-1]["tilgung"] += schlussrate
        zahlungen[-1]["rest"] = 0.0

    geleistet = [i for i, tag in enumerate(termine) if tag <= heute]
    offen = [i for i in range(len(zahlungen)) if i not in geleistet]
    zinsen_bisher = sum(zahlungen[i]["zins"] for i in geleistet)
    tilgung_bisher = sum(zahlungen[i]["tilgung"] for i in geleistet)
    gezahlt = zinsen_bisher + tilgung_bisher
    restsumme = sum(zahlungen[i]["betrag"] for i in offen)
    zinsen_gesamt = sum(z["zins"] for z in zahlungen)
    gesamt = sum(z["betrag"] for z in zahlungen)
    naechste = zahlungen[offen[0]] if offen else None

    abweichung = None
    if eingegeben and eingegeben > 0 and berechnet > 0:
        abweichung = (eingegeben - berechnet) / berechnet

    ergebnis.update(
        {
            "kredit_summe": summe,
            "kredit_sollzins": soll,
            "kredit_effektivzins": effektiv,
            "kredit_rate": round(rate, 2),
            "kredit_rate_berechnet": round(berechnet, 2),
            "kredit_rate_abweichung": round(abweichung * 100, 2) if abweichung is not None else None,
            "kredit_rate_passt": abs(abweichung) <= ABWEICHUNG_SCHWELLE if abweichung is not None else None,
            "kredit_zahlungen_gesamt": len(zahlungen),
            "kredit_zahlungen_geleistet": len(geleistet),
            "kredit_restschuld": round(max(summe - tilgung_bisher, 0.0), 2),
            "kredit_zinsen_bisher": round(zinsen_bisher, 2),
            "kredit_tilgung_bisher": round(tilgung_bisher, 2),
            "kredit_gezahlt": round(gezahlt, 2),
            "kredit_restsumme": round(restsumme, 2),
            "kredit_zinsen_gesamt": round(zinsen_gesamt, 2),
            "kredit_gesamtkosten": round(gesamt, 2),
            "kredit_schlussrate": round(schlussrate, 2),
            "kredit_tilgung_prozent": round(min(tilgung_bisher / summe * 100, 100.0), 1),
            "kredit_erste_zahlung": erste,
            "kredit_naechste_zahlung": termine[offen[0]] if offen else None,
            "kredit_naechste_betrag": round(naechste["betrag"], 2) if naechste else None,
            "kredit_zins_anteil": round(naechste["zins"], 2) if naechste else None,
            "kredit_tilgung_anteil": round(naechste["tilgung"], 2) if naechste else None,
        }
    )
    return ergebnis
