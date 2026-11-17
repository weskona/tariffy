"""PV-Autarkie in der Prognose der Endkosten (Issue 86).

Reine Rechnung ohne Home Assistant. Mit einer PV-Anlage (und Batterie) schwankt der Netzbezug
stark mit der Jahreszeit: wer im Winter beobachtet, ueberschaetzt die Restlaufzeit, wer im Sommer
beobachtet, unterschaetzt sie. Die Autarkie eines Monats ist der Anteil des Hausverbrauchs, den die
Anlage deckt:

    a_m = 1 - Netzbezug_m / Gesamtverbrauch_m          (auf 0 bis 100 % begrenzt)

Der Verbrauchssensor des Vertrags misst den Netzbezug; die Autarkie steckt also schon in den
bisherigen Messwerten. Fuer jeden Monat der Restlaufzeit wird der taegliche Netzbezug deshalb
saisonal normalisiert (Autarkie desselben Monats im Vorjahr gegen die Autarkie im gemessenen Zeitraum):

    Netzbezug_m = Netzbezug_je_Tag_bisher * Tage_m * (1 - a_m) / (1 - a_bisher)

Ohne Daten fuer einen Monat (oder fuer den gemessenen Zeitraum) bleibt es bei der linearen
Hochrechnung (Faktor 1).
"""

from __future__ import annotations

from datetime import date, timedelta

# Ist die Autarkie im gemessenen Zeitraum nahe 100 %, ist die Normalisierung nicht mehr belastbar
MIN_ANTEIL_NETZ = 0.05
MAX_FAKTOR = 4.0


def autarkie(bezug: float | None, gesamt: float | None) -> float | None:
    """Autarkie als Anteil 0..1; None, wenn sie sich nicht berechnen laesst."""
    if bezug is None or gesamt is None or gesamt <= 0 or bezug < 0:
        return None
    return min(1.0, max(0.0, 1.0 - bezug / gesamt))


def restmonate(heute: date, tage: int) -> list[tuple[int, int, int]]:
    """Die Tage ab `heute` (einschliesslich), zusammengefasst je Kalendermonat: (Jahr, Monat, Tage)."""
    ergebnis: list[tuple[int, int, int]] = []
    for i in range(max(tage, 0)):
        tag = heute + timedelta(days=i)
        if ergebnis and ergebnis[-1][:2] == (tag.year, tag.month):
            jahr, monat, anzahl = ergebnis[-1]
            ergebnis[-1] = (jahr, monat, anzahl + 1)
        else:
            ergebnis.append((tag.year, tag.month, 1))
    return ergebnis


def vorjahresmonat(jahr: int, monat: int) -> tuple[date, date]:
    """Erster Tag des Monats im Vorjahr und erster Tag des Folgemonats (Fenster fuer die Statistik)."""
    start = date(jahr - 1, monat, 1)
    ende = date(jahr - 1 + (monat == 12), monat % 12 + 1, 1)
    return start, ende


def faktor(a_monat: float | None, a_bisher: float | None) -> float:
    """Saison-Faktor fuer den Netzbezug eines Monats gegenueber dem gemessenen Zeitraum."""
    if a_monat is None or a_bisher is None or (1.0 - a_bisher) < MIN_ANTEIL_NETZ:
        return 1.0
    return min(MAX_FAKTOR, max(0.0, (1.0 - a_monat) / (1.0 - a_bisher)))


def rest_verbrauch(
    bisher: float, vergangene_tage: int, monate: list[tuple[int, int, int]], faktoren: list[float]
) -> float:
    """Netzbezug der Restlaufzeit: der Tagesschnitt bisher, je Monat mit seinem Faktor."""
    if vergangene_tage <= 0:
        return 0.0
    je_tag = bisher / vergangene_tage
    return sum(je_tag * tage * f for (_, _, tage), f in zip(monate, faktoren, strict=True))


# --------------------------------------------------------------- manuelle Werte (Variante 3)
def parse_manuell(text: object) -> tuple[list[float] | None, bool]:
    """Manuelle Autarkie in %: ein Wert (gilt fuer alle Monate) oder zwoelf Werte (Januar bis Dezember),
    getrennt durch Leerzeichen oder Semikolon; Dezimalkomma oder -punkt. Gibt (Werte, Fehler) zurueck:
    leer ist kein Fehler (dann None), alles andere Unbrauchbare ist einer."""
    roh = str(text or "").replace(";", " ").strip()
    if not roh:
        return None, False
    werte: list[float] = []
    for teil in roh.split():
        try:
            wert = float(teil.replace(",", "."))
        except ValueError:
            return None, True
        if not 0.0 <= wert <= 100.0:
            return None, True
        werte.append(wert)
    if len(werte) == 1:
        return werte * 12, False
    if len(werte) == 12:
        return werte, False
    return None, True


def manuell_zeitraum(werte: list[float], start: date, ende: date) -> float | None:
    """Mittlere manuelle Autarkie (Anteil 0..1) ueber die Tage von `start` bis vor `ende`, nach Tagen
    gewichtet. None, wenn der Zeitraum leer ist."""
    tage = (ende - start).days
    if tage <= 0:
        return None
    summe = 0.0
    for i in range(tage):
        summe += werte[(start + timedelta(days=i)).month - 1]
    return summe / tage / 100.0
