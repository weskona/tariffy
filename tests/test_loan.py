"""Kredit / Finanzierung: Tilgungsplan (Annuitaet) und seine Kennzahlen."""

from __future__ import annotations

from datetime import date

import pytest

from custom_components.tariffy import loan

BASIS = {
    "sparte": "loan",
    "kredit_summe": 10000.0,
    "sollzins": 5.0,
    "laufzeit_monate": 12,
    "beginn": "2026-01-15",
    "zahlweise": "monthly",
}


def test_the_annuity_matches_the_textbook_value():
    # 10,000 at 5 % nominal over 12 months: 856.07 a month
    assert loan.annuitaet(10000, 0.05 / 12, 12) == pytest.approx(856.07, abs=0.005)


def test_a_loan_without_interest_is_paid_off_in_equal_parts():
    assert loan.annuitaet(1200, 0.0, 12) == pytest.approx(100.0)
    assert loan.annuitaet(1200, 0.0, 12, 600) == pytest.approx(50.0)


def test_the_plan_pays_the_loan_off_and_the_interest_share_falls():
    zahlungen, schluss = loan.plan(10000, 0.05 / 12, 856.07, 12)
    assert len(zahlungen) == 12
    assert zahlungen[0]["zins"] == pytest.approx(41.67, abs=0.005)
    assert zahlungen[0]["tilgung"] == pytest.approx(856.07 - 41.67, abs=0.01)
    assert [z["zins"] for z in zahlungen] == sorted((z["zins"] for z in zahlungen), reverse=True)
    assert schluss == pytest.approx(0.0, abs=0.1)  # the rate is rounded to cents


def test_a_final_payment_is_reached_by_the_annuity():
    rate = loan.annuitaet(20000, 0.045 / 12, 36, 8000)
    _, schluss = loan.plan(20000, 0.045 / 12, rate, 36)
    assert schluss == pytest.approx(8000, abs=0.01)


def test_the_nominal_rate_is_preferred_over_the_effective_one():
    assert loan.periodenzins(5.0, 5.12, 1) == pytest.approx(0.05 / 12)
    assert loan.periodenzins(None, 5.12, 1) == pytest.approx((1.0512) ** (1 / 12) - 1)
    assert loan.periodenzins(None, None, 1) is None
    assert loan.periodenzins(5.0, None, 3) == pytest.approx(0.0125)  # quarterly


def test_nothing_is_calculated_without_the_essentials():
    assert loan.berechne({**BASIS, "kredit_summe": None}, date(2026, 6, 1)).get("kredit_rate") is None
    assert loan.berechne({**BASIS, "sollzins": None}, date(2026, 6, 1)).get("kredit_rate") is None
    assert loan.berechne({**BASIS, "laufzeit_monate": 0}, date(2026, 6, 1)).get("kredit_rate") is None


def test_the_figures_in_the_middle_of_the_term():
    d = loan.berechne(BASIS, date(2026, 6, 20))  # first payment 15 Feb, so 5 payments by 20 June
    assert d["ende"] == date(2027, 1, 15)
    assert d["kredit_rate"] == pytest.approx(856.07, abs=0.005)
    assert d["kredit_zahlungen_geleistet"] == 5 and d["kredit_zahlungen_gesamt"] == 12
    assert d["kredit_erste_zahlung"] == date(2026, 2, 15)
    assert d["kredit_naechste_zahlung"] == date(2026, 7, 15)
    assert d["kredit_gezahlt"] == pytest.approx(d["kredit_zinsen_bisher"] + d["kredit_tilgung_bisher"], abs=0.02)
    assert d["kredit_restschuld"] == pytest.approx(10000 - d["kredit_tilgung_bisher"], abs=0.01)
    # what was paid plus what is still to pay is the whole cost of the loan
    assert d["kredit_gezahlt"] + d["kredit_restsumme"] == pytest.approx(d["kredit_gesamtkosten"], abs=0.03)
    assert d["kredit_zinsen_gesamt"] == pytest.approx(d["kredit_gesamtkosten"] - 10000, abs=0.03)
    assert d["kredit_zins_anteil"] + d["kredit_tilgung_anteil"] == pytest.approx(d["kredit_naechste_betrag"], abs=0.01)
    assert 0 < d["kredit_tilgung_prozent"] < 100


def test_before_the_start_nothing_is_paid():
    d = loan.berechne(BASIS, date(2026, 1, 1))
    assert d["kredit_zahlungen_geleistet"] == 0 and d["kredit_gezahlt"] == 0
    assert d["kredit_restschuld"] == 10000.0


def test_after_the_end_the_loan_is_paid_off():
    d = loan.berechne(BASIS, date(2027, 3, 1))
    assert d["kredit_restschuld"] == pytest.approx(0.0, abs=0.06)
    assert d["kredit_restsumme"] == 0 and d["kredit_naechste_zahlung"] is None
    assert d["kredit_gezahlt"] == pytest.approx(d["kredit_gesamtkosten"], abs=0.01)


def test_the_first_payment_can_be_set():
    d = loan.berechne({**BASIS, "erste_zahlung": "2026-01-31"}, date(2026, 1, 31))
    assert d["kredit_erste_zahlung"] == date(2026, 1, 31)
    assert d["kredit_zahlungen_geleistet"] == 1  # the payment of the day counts


def test_a_rate_entered_by_hand_wins_and_a_gap_is_reported():
    d = loan.berechne({**BASIS, "kredit_rate": 900.0}, date(2026, 6, 20))
    assert d["kredit_rate"] == 900.0 and d["kredit_rate_berechnet"] == pytest.approx(856.07, abs=0.005)
    assert d["kredit_rate_passt"] is False and d["kredit_rate_abweichung"] == pytest.approx(5.13, abs=0.01)
    early = loan.berechne({**BASIS, "kredit_rate": 1000.0}, date(2026, 6, 20))
    assert early["kredit_zahlungen_gesamt"] < 12  # a clearly higher rate pays the loan off earlier
    ok = loan.berechne({**BASIS, "kredit_rate": 856.0}, date(2026, 6, 20))
    assert ok["kredit_rate_passt"] is True


def test_a_rate_that_is_too_low_leaves_a_final_payment():
    d = loan.berechne({**BASIS, "kredit_rate": 800.0}, date(2027, 3, 1))
    assert d["kredit_schlussrate"] > 0  # what is left at the end is paid with the last payment
    assert d["kredit_restschuld"] == pytest.approx(0.0, abs=0.01)


def test_a_final_payment_is_part_of_the_last_payment():
    d = loan.berechne({**BASIS, "schlussrate": 4000.0, "laufzeit_monate": 12}, date(2026, 12, 1))
    assert d["kredit_schlussrate"] == pytest.approx(4000.0, abs=0.02)
    assert d["kredit_restschuld"] > 3900  # not yet paid
    after = loan.berechne({**BASIS, "schlussrate": 4000.0}, date(2027, 1, 15))
    assert after["kredit_restschuld"] == pytest.approx(0.0, abs=0.06)


def test_quarterly_payments():
    d = loan.berechne({**BASIS, "zahlweise": "quarterly", "laufzeit_monate": 24}, date(2026, 12, 1))
    assert d["kredit_zahlungen_gesamt"] == 8
    assert d["kredit_erste_zahlung"] == date(2026, 4, 15)
    assert d["kredit_zahlungen_geleistet"] == 3  # 15 Apr, 15 Jul, 15 Oct
