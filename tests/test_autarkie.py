"""PV-Autarkie in der Prognose der Endkosten (Issue 86)."""

from __future__ import annotations

from datetime import date
import json
from unittest.mock import patch

import pytest

from custom_components.tariffy import autarkie as pv

from .test_insurance import TRANSLATIONS, _keys, _start
from .test_panel import frontend_env  # noqa: F401  (fixture)
from .test_reconfigure import _reconfigure

COORDINATOR = "custom_components.tariffy.coordinator"


# ----------------------------------------------------------------- pure calculation
@pytest.mark.parametrize(
    ("bezug", "gesamt", "erwartet"),
    [
        (50, 300, 1 - 50 / 300),
        (300, 300, 0.0),
        (0, 300, 1.0),
        (400, 300, 0.0),  # more grid draw than consumption: no autarky below 0
        (-5, 300, None),  # nonsense
        (50, 0, None),  # no total consumption
        (50, -1, None),
        (None, 300, None),
        (50, None, None),
    ],
)
def test_the_autarky_of_a_month(bezug, gesamt, erwartet):
    assert pv.autarkie(bezug, gesamt) == (pytest.approx(erwartet) if erwartet is not None else None)


def test_the_remaining_days_are_grouped_by_month():
    assert pv.restmonate(date(2026, 12, 20), 20) == [(2026, 12, 12), (2027, 1, 8)]  # across the new year
    assert pv.restmonate(date(2026, 2, 27), 3) == [(2026, 2, 2), (2026, 3, 1)]
    assert pv.restmonate(date(2026, 7, 1), 0) == []


def test_the_window_in_the_previous_year():
    assert pv.vorjahresmonat(2026, 7) == (date(2025, 7, 1), date(2025, 8, 1))
    assert pv.vorjahresmonat(2027, 12) == (date(2026, 12, 1), date(2027, 1, 1))  # December ends in January
    assert pv.vorjahresmonat(2028, 2) == (date(2027, 2, 1), date(2027, 3, 1))


def test_the_season_factor():
    assert pv.faktor(0.8, 0.5) == pytest.approx(0.4)  # sunnier than the measured period: less grid draw
    assert pv.faktor(0.2, 0.5) == pytest.approx(1.6)  # darker: more
    assert pv.faktor(None, 0.5) == 1.0  # no data for the month: no change
    assert pv.faktor(0.8, None) == 1.0
    assert pv.faktor(0.8, 0.99) == 1.0  # nearly self-sufficient while measuring: not reliable
    assert pv.faktor(0.0, 0.01) == pytest.approx(1 / 0.99)
    assert pv.faktor(0.0, 0.9) == pv.MAX_FAKTOR  # 1 / 0.1 = 10, capped
    assert pv.faktor(1.0, 0.5) == 0.0  # fully self-sufficient month: no grid draw


def test_the_remaining_consumption():
    monate = [(2026, 7, 31), (2026, 8, 30)]
    assert pv.rest_verbrauch(1800, 180, monate, [1.0, 1.0]) == pytest.approx(10 * 61)
    assert pv.rest_verbrauch(1800, 180, monate, [0.5, 2.0]) == pytest.approx(10 * (31 * 0.5 + 30 * 2.0))
    assert pv.rest_verbrauch(1800, 0, monate, [1.0, 1.0]) == 0.0


# ------------------------------------------------- the forecast of a contract (with the statistics of last year)
NETZ, HAUS, NT, HAUS_NT = "sensor.netz", "sensor.haus", "sensor.netz_nt", "sensor.haus_nt"
ELEKTRO = {
    "sparte": "electricity", "anbieter": "Stadtwerke", "arbeitspreis": 0.30, "grundpreis": 10.0, "abschlag": 100.0,
    "beginn": "2026-01-01", "ende": "2026-12-31", "verbrauch_sensor": NETZ, "erinnerung_monate": "0",
}
# last year, per month: grid draw and total consumption in kWh (Jan-Jun 200/300, then the sunny months)
NETZ_2025 = [200] * 6 + [50, 50, 100, 150, 200, 250]
HAUS_2025 = [300] * 12


class Stats:
    """The statistics of a few sensors: a monthly series for 2025 and what has been counted in 2026 so far.

    The meters counted through 2025 (so the sum on 1 January 2026 is the total of 2025, which is also the
    start of a contract that begins that day) and `bisher` more since. A sensor without a series has no history."""

    def __init__(self, series: dict[str, list[int] | None], bisher: dict[str, float]):
        self.series, self.bisher = series, bisher

    def base(self, entity):
        monthly = self.series.get(entity)
        return float(sum(monthly)) if monthly else 0.0

    async def historic(self, _hass, entity, at):
        monthly = self.series.get(entity)
        if at.year >= 2026:
            if monthly is None and entity != NETZ and entity not in (NT,):
                return None, None  # the total consumption has no history at all
            return self.base(entity), self.base(entity)
        if not monthly:
            return None, None
        total = float(sum(monthly[: at.month - 1]))
        return total, total

    def latest(self, entity):
        value = self.base(entity) + self.bisher[entity]
        return (value, value)


def _stats(netz=NETZ_2025, haus=HAUS_2025, **more):
    return Stats({NETZ: netz, HAUS: haus, **more}, {NETZ: 1800.0, HAUS: 3600.0, NT: 600.0, HAUS_NT: 1500.0})


async def _setup(contract, data, stats=None, today="2026-07-01"):
    stats = stats or _stats()
    extra = {HAUS: (stats.latest(HAUS), (stats.base(HAUS),) * 2), HAUS_NT: (stats.latest(HAUS_NT), (stats.base(HAUS_NT),) * 2)}
    with patch(f"{COORDINATOR}._get_historic_value", stats.historic):
        return await contract.setup(
            data, today=today, latest=stats.latest(NETZ), offset=(stats.base(NETZ),) * 2,
            latest_nt=stats.latest(NT), offset_nt=(stats.base(NT),) * 2, extra=extra,
        )


def _expected_projection():
    """By hand: 1800 kWh in 181 days, a_bisher = 50 %; the months July to December of last year."""
    je_tag = 1800 / 181
    faktoren = [(n / 300) / 0.5 for n in NETZ_2025[6:]]
    tage = [31, 31, 30, 31, 30, 30]  # 183 days left of the 364 of the term
    return 1800 + je_tag * sum(d * f for d, f in zip(tage, faktoren, strict=True))


PV = {**ELEKTRO, "pv_autarkie": True, "gesamtverbrauch_sensor": HAUS}


async def test_without_the_option_nothing_changes(contract):
    _, d = await _setup(contract, ELEKTRO)
    assert d["verbrauch_hochgerechnet"] == pytest.approx(1800 / 181 * 364, abs=0.1)  # the linear extrapolation
    assert d["autarkie_aktiv"] is False and d["autarkie_monatswerte"] == [] and d["prognose_ohne_autarkie"] is None


async def test_the_remaining_term_follows_last_years_autarky(contract):
    _, d = await _setup(contract, PV)
    assert d["autarkie_aktiv"] is True and d["autarkie_variante"] == "gesamtverbrauch"
    assert d["verbrauch_hochgerechnet"] == pytest.approx(_expected_projection(), abs=0.5)
    assert d["autarkie_bisher"] == 50.0
    assert [m["monat"] for m in d["autarkie_monatswerte"]] == ["2026-07", "2026-08", "2026-09", "2026-10", "2026-11", "2026-12"]
    assert d["autarkie_monatswerte"][0]["autarkie"] == pytest.approx(83.3, abs=0.05)  # 1 - 50/300 in July 2025
    assert d["autarkie_monatswerte"][0]["faktor"] == pytest.approx(0.333, abs=0.001)
    assert d["autarkie_monatswerte"][-1]["tage"] == 30
    assert d["verbrauch_hochgerechnet"] < 1800 / 181 * 364  # the linear extrapolation overestimates here
    assert d["prognose_ohne_autarkie"] is not None and d["prognose_ohne_autarkie"] < d["prognose_real"]  # (less cost, more credit)


async def test_the_forecast_without_autarky_is_the_old_one(contract):
    _, plain = await _setup(contract, ELEKTRO)
    _, d = await _setup(contract, PV)
    assert d["prognose_ohne_autarkie"] == pytest.approx(plain["prognose_real"], abs=0.01)
    assert d["kosten_bisher"] == plain["kosten_bisher"]  # what has been measured stays as it is
    assert d["verbrauch_bisher"] == plain["verbrauch_bisher"]


@pytest.mark.parametrize(
    "stats",
    [
        _stats(netz=None, haus=None),  # no statistics of last year at all
        _stats(haus=None),  # the total consumption has no history
        _stats(netz=None),  # the grid draw has no history of last year
        _stats(netz=[0] * 12, haus=[0] * 12),  # nothing was consumed
    ],
)
async def test_missing_history_keeps_the_linear_extrapolation(contract, stats):
    _, d = await _setup(contract, PV, stats)
    assert d["autarkie_aktiv"] is False
    assert d["verbrauch_hochgerechnet"] == pytest.approx(1800 / 181 * 364, abs=0.1)
    assert d["prognose_real"] is not None  # no error, no unavailable


async def test_without_a_total_consumption_sensor_nothing_changes(contract):
    _, d = await _setup(contract, {**ELEKTRO, "pv_autarkie": True})
    assert d["autarkie_aktiv"] is False


async def test_autarky_below_zero_is_clamped(contract):
    # more grid draw than consumption last year: 0 %, never negative
    _, d = await _setup(contract, PV, _stats(netz=[400] * 12, haus=[300] * 12))
    assert d["autarkie_aktiv"] is True and all(m["autarkie"] == 0.0 for m in d["autarkie_monatswerte"])


async def test_the_new_year_in_the_remaining_term(contract):
    data = {**PV, "beginn": "2026-04-01", "ende": "2027-03-31"}
    _, d = await _setup(contract, data, today="2026-12-15")
    months = [m["monat"] for m in d["autarkie_monatswerte"]]
    assert months[0] == "2026-12" and "2027-01" in months and months[-1] == "2027-03"
    assert d["autarkie_monatswerte"][0]["tage"] == 17  # the rest of December, from the 15th


# ---------------------------------------------------------------- dual tariff
HT_NT = {**PV, "sparte": "electricity_ht_nt", "verbrauch_sensor_nt": NT, "arbeitspreis_nt": 0.20}
NT_2025 = [100] * 6 + [100, 100, 100, 120, 140, 160]
HAUS_NT_2025 = [200] * 12


async def test_dual_tariff_with_one_total_sensor_is_an_approximation(contract):
    _, d = await _setup(contract, HT_NT, _stats(**{NT: NT_2025}))
    assert d["autarkie_aktiv"] is True and d["autarkie_naeherung"] is True
    assert "autarkie_nt" in d["autarkie_monatswerte"][0] and d["autarkie_monatswerte"][0]["autarkie"] == d["autarkie_monatswerte"][0]["autarkie_nt"]
    months = d["autarkie_monatswerte"]
    assert months[-1]["autarkie"] == 0.0  # December last year: the grid draw of both tariffs exceeded the total, clamped
    # both tariffs get the same factors; the projection is the daily average so far times the days times the factor
    expected = 2400 + 2400 / 181 * sum(m["tage"] * m["faktor"] for m in months)
    assert d["verbrauch_hochgerechnet"] == pytest.approx(expected, abs=1.0)


async def test_dual_tariff_with_two_total_sensors_is_worked_out_per_tariff(contract):
    data = {**HT_NT, "gesamtverbrauch_sensor_nt": HAUS_NT}
    _, d = await _setup(contract, data, _stats(**{NT: NT_2025, HAUS_NT: HAUS_NT_2025}))
    assert d["autarkie_aktiv"] is True and d["autarkie_naeherung"] is False
    juli = d["autarkie_monatswerte"][0]
    assert juli["autarkie"] == pytest.approx(83.3, abs=0.05)  # high tariff: 1 - 50/300
    assert juli["autarkie_nt"] == pytest.approx(50.0, abs=0.05)  # low tariff: 1 - 100/200
    assert d["autarkie_bisher"] == 50.0 and d["autarkie_bisher_nt"] == pytest.approx(60.0, abs=0.05)  # 1 - 600/1500


# --------------------------------------- the total consumption and what the PV covers (follow-up of Issue 86)
async def test_the_total_consumption_and_the_pv_share_are_worked_out(contract):
    """By hand: house 3600 kWh in 181 of 364 days; grid draw 1800 so far."""
    _, d = await _setup(contract, PV)
    assert d["verbrauch_gesamt_bisher"] == 3600.0
    assert d["verbrauch_pv_gedeckt_bisher"] == 1800.0  # total - grid draw
    gesamt_hoch = 3600 / 181 * 364  # the total is extended linearly
    assert d["verbrauch_gesamt_hochgerechnet"] == pytest.approx(gesamt_hoch, abs=0.1)
    # what the PV covers by the end: the linear total minus the season-normalised grid draw
    assert d["verbrauch_pv_gedeckt_hochgerechnet"] == pytest.approx(gesamt_hoch - _expected_projection(), abs=0.2)
    assert d["verbrauch_hochgerechnet"] == pytest.approx(_expected_projection(), abs=0.1)  # the grid draw is as before
    assert (d["verbrauch_gesamt_bisher"] - d["verbrauch_pv_gedeckt_bisher"]) == d["verbrauch_bisher"]


async def test_the_figures_of_the_grid_draw_and_the_costs_do_not_change(contract):
    """The follow-up only adds figures: the forecast is the one of 1.31.0 (hand-calculated above)."""
    _, d = await _setup(contract, PV)
    assert d["verbrauch_hochgerechnet"] == pytest.approx(_expected_projection(), abs=0.1)
    assert d["verbrauch_bisher"] == 1800.0 and d["kosten_bisher"] == pytest.approx(1800 * 0.30 + 10 * 181 / 30.44, abs=3.0)


@pytest.mark.parametrize(
    "data", [{**ELEKTRO, "pv_autarkie": True, "autarkie_manuell": "10 10 20 40 60 70 80 75 50 30 15 10"}, ELEKTRO]
)
async def test_without_a_total_sensor_or_the_option_there_is_no_total(contract, data):
    _, d = await _setup(contract, data)
    for key in ("verbrauch_gesamt_bisher", "verbrauch_gesamt_hochgerechnet", "verbrauch_pv_gedeckt_bisher", "verbrauch_pv_gedeckt_hochgerechnet"):
        assert d[key] is None, key


async def test_dual_tariff_adds_both_tariffs_with_two_total_sensors(contract):
    data = {**HT_NT, "gesamtverbrauch_sensor_nt": HAUS_NT}
    _, d = await _setup(contract, data, _stats(**{NT: NT_2025, HAUS_NT: HAUS_NT_2025}))
    assert d["verbrauch_gesamt_bisher"] == 3600.0 + 1500.0  # high and low tariff added
    assert d["verbrauch_pv_gedeckt_bisher"] == (3600 - 1800) + (1500 - 600)
    assert d["verbrauch_gesamt_hochgerechnet"] == pytest.approx(5100 / 181 * 364, abs=0.2)


async def test_dual_tariff_with_one_total_sensor_counts_it_once(contract):
    _, d = await _setup(contract, HT_NT, _stats(**{NT: NT_2025}))
    assert d["verbrauch_gesamt_bisher"] == 3600.0  # the one sensor covers both tariffs
    assert d["verbrauch_pv_gedeckt_bisher"] == 3600 - 2400


async def test_more_grid_draw_than_total_consumption_gives_no_negative_pv_share(contract):
    stats = _stats()
    stats.bisher[HAUS] = 1000.0  # less than the 1800 kWh of grid draw: nonsense, but never negative
    _, d = await _setup(contract, PV, stats)
    assert d["verbrauch_pv_gedeckt_bisher"] == 0.0 and d["verbrauch_pv_gedeckt_hochgerechnet"] >= 0.0


async def test_a_total_of_zero_shows_zero_pv(contract):
    stats = _stats()
    stats.bisher[HAUS] = 0.0
    _, d = await _setup(contract, PV, stats)
    # no self-sufficiency can be worked out without a total: no option effect, no figures, no error
    assert d["autarkie_aktiv"] is False and d["verbrauch_gesamt_bisher"] is None and d["prognose_real"] is not None


async def test_the_sensor_carries_the_new_attributes_only_with_a_total_sensor(contract, hass):
    await _setup(contract, PV)
    attrs = [hass.states.get(e).attributes for e in hass.states.async_entity_ids("sensor") if "refund_balance_due_contract_end" in e][0]
    assert attrs["verbrauch_gesamt_bisher"] == 3600.0 and attrs["verbrauch_pv_gedeckt_bisher"] == 1800.0
    assert "verbrauch_gesamt_hochgerechnet" in attrs and "verbrauch_pv_gedeckt_hochgerechnet" in attrs


async def test_the_panel_gets_the_new_figures(frontend_env, contract, hass):  # noqa: F811
    from custom_components.tariffy import panel

    entry, _ = await _setup(contract, PV)
    payload = panel.contract_payload(hass, entry)
    assert payload["verbrauch_gesamt_bisher"] == 3600.0 and payload["verbrauch_pv_gedeckt_bisher"] == 1800.0


# ------------------------------------------------------------------- the sensor
async def test_the_sensor_shows_the_attributes_only_when_it_applies(contract, hass):
    await _setup(contract, PV)
    states = [hass.states.get(e) for e in hass.states.async_entity_ids("sensor") if "refund_balance_due_contract_end" in e]
    assert states and states[0].attributes["autarkie_variante"] == "gesamtverbrauch"
    assert "autarkie_monatswerte" in states[0].attributes and "prognose_ohne_autarkie" in states[0].attributes


async def test_other_contracts_have_no_autarky_attributes(contract, hass):
    await _setup(contract, ELEKTRO)
    states = [hass.states.get(e) for e in hass.states.async_entity_ids("sensor") if "refund_balance_due_contract_end" in e]
    assert states and not [k for k in states[0].attributes if k.startswith("autarkie") or k == "prognose_ohne_autarkie"]


# ------------------------------------------------------------- the form and the contract data
@pytest.mark.parametrize(
    ("sparte", "step", "extra"),
    [("electricity", "energie", set()), ("electricity_ht_nt", "energie_ht_nt", {"gesamtverbrauch_sensor_nt"})],
)
async def test_the_form_offers_the_option_and_is_translated(hass, sparte, step, extra):
    result = await _start(hass, sparte)
    assert result["step_id"] == step
    keys = _keys(result)
    assert {"pv_autarkie", "gesamtverbrauch_sensor"} | extra <= keys
    for language in ("en", "de"):
        texts = json.loads((TRANSLATIONS / f"{language}.json").read_text(encoding="utf-8"))["config"]["step"]
        for name in (step, f"reconfigure_{step}"):
            for key in {"pv_autarkie", "gesamtverbrauch_sensor"} | extra:
                assert texts[name]["data"][key] and texts[name]["data_description"][key], (language, name, key)


async def test_gas_and_water_do_not_offer_it(hass):
    for sparte in ("gas", "water"):
        assert "pv_autarkie" not in _keys(await _start(hass, sparte))


async def test_editing_keeps_the_option_and_the_sensors(frontend_env, contract, hass):  # noqa: F811
    data = {**HT_NT, "gesamtverbrauch_sensor_nt": HAUS_NT}
    entry, _ = await _setup(contract, data, _stats(**{NT: NT_2025, HAUS_NT: HAUS_NT_2025}))
    new = await _reconfigure(hass, entry)
    assert new["pv_autarkie"] is True
    assert new["gesamtverbrauch_sensor"] == HAUS and new["gesamtverbrauch_sensor_nt"] == HAUS_NT


async def test_a_tariff_switch_keeps_the_option_and_the_sensors(contract):
    options = {"next_beginn": "2026-07-01", "next_ende": "2027-06-30", "next_anbieter": "Neu", "next_arbeitspreis": 0.25}
    stats = _stats()
    extra = {HAUS: (stats.latest(HAUS), (stats.base(HAUS),) * 2)}
    with patch(f"{COORDINATOR}._get_historic_value", stats.historic):
        entry, _ = await contract.setup(
            PV, today="2026-07-01", options=options, latest=stats.latest(NETZ), offset=(stats.base(NETZ),) * 2, extra=extra
        )
    assert entry.data["anbieter"] == "Neu"
    assert entry.data["pv_autarkie"] is True and entry.data["gesamtverbrauch_sensor"] == HAUS


# ------------------------------------------------- variant 3 (own values) and variant 2 (a sensor in %)
MANUELL = "10 10 20 40 60 70 80 75 50 30 15 10"  # January to December
MANUELL_LISTE = [10, 10, 20, 40, 60, 70, 80, 75, 50, 30, 15, 10]


@pytest.mark.parametrize(
    ("text", "werte", "fehler"),
    [
        ("", None, False),
        (None, None, False),
        ("   ", None, False),
        ("40", [40.0] * 12, False),
        ("12,5", [12.5] * 12, False),  # decimal comma
        (MANUELL, [float(v) for v in MANUELL_LISTE], False),
        ("10;10;20;40;60;70;80;75;50;30;15;10", [float(v) for v in MANUELL_LISTE], False),  # semicolons
        ("10 20 30", None, True),  # neither one nor twelve values
        ("abc", None, True),
        ("101", None, True),  # above 100 %
        ("-1", None, True),
        ("10 " * 11 + "x", None, True),
    ],
)
def test_the_own_values_are_parsed_and_checked(text, werte, fehler):
    assert pv.parse_manuell(text) == (werte, fehler)


def test_the_own_values_over_the_measured_period():
    liste = [float(v) for v in MANUELL_LISTE]
    # 1 January to 30 June 2026: 181 days
    erwartet = (10 * 31 + 10 * 28 + 20 * 31 + 40 * 30 + 60 * 31 + 70 * 30) / 181 / 100
    assert pv.manuell_zeitraum(liste, date(2026, 1, 1), date(2026, 7, 1)) == pytest.approx(erwartet)
    assert pv.manuell_zeitraum(liste, date(2026, 7, 1), date(2026, 7, 1)) is None  # empty period
    assert pv.manuell_zeitraum([50.0] * 12, date(2026, 1, 1), date(2026, 3, 1)) == pytest.approx(0.5)


def _projection(a_bisher, a_monate_prozent):
    """By hand: 1800 kWh in 181 days; the months July to December with 31, 31, 30, 31, 30, 30 days left."""
    tage = [31, 31, 30, 31, 30, 30]
    faktoren = [(1 - a / 100) / (1 - a_bisher) for a in a_monate_prozent]
    return 1800 + 1800 / 181 * sum(d * f for d, f in zip(tage, faktoren, strict=True))


async def test_own_values_alone_are_enough_even_without_any_history(contract):
    data = {**ELEKTRO, "pv_autarkie": True, "autarkie_manuell": MANUELL}
    _, d = await _setup(contract, data, _stats(netz=None, haus=None))  # the first year of a PV system
    assert d["autarkie_aktiv"] is True and d["autarkie_variante"] == "manuell"
    a_bisher = (10 * 31 + 10 * 28 + 20 * 31 + 40 * 30 + 60 * 31 + 70 * 30) / 181 / 100
    assert d["verbrauch_hochgerechnet"] == pytest.approx(_projection(a_bisher, MANUELL_LISTE[6:]), abs=0.5)
    assert d["autarkie_bisher"] == pytest.approx(a_bisher * 100, abs=0.05)
    assert [m["autarkie"] for m in d["autarkie_monatswerte"]] == [80.0, 75.0, 50.0, 30.0, 15.0, 10.0]
    assert {m["quelle"] for m in d["autarkie_monatswerte"]} == {"manuell"}


async def test_one_value_for_all_months_changes_nothing_in_the_season(contract):
    # the same autarky in every month: no season, so the forecast is the linear one
    data = {**ELEKTRO, "pv_autarkie": True, "autarkie_manuell": "40"}
    _, d = await _setup(contract, data, _stats(netz=None, haus=None))
    assert d["autarkie_aktiv"] is False
    assert d["verbrauch_hochgerechnet"] == pytest.approx(1800 / 181 * 364, abs=0.1)


async def test_own_values_fill_the_months_without_statistics(contract):
    # September last year has no total consumption (0 kWh): that month takes the own value, the others the statistics
    haus = list(HAUS_2025)
    haus[8] = 0
    data = {**PV, "autarkie_manuell": MANUELL}
    _, d = await _setup(contract, data, _stats(haus=haus))
    assert d["autarkie_variante"] == "gesamtverbrauch"
    quellen = {m["monat"]: m["quelle"] for m in d["autarkie_monatswerte"]}
    assert quellen["2026-09"] == "manuell" and quellen["2026-07"] == "statistik" and quellen["2026-12"] == "statistik"
    sept = next(m for m in d["autarkie_monatswerte"] if m["monat"] == "2026-09")
    assert sept["autarkie"] == 50.0  # the own value of September


def _mittel(werte_2025, bisher):
    async def fake(_hass, entity_id, start, end):
        assert entity_id == "sensor.autarkie"
        if start.year == 2026:
            return bisher
        return werte_2025.get(start.month)

    return patch(f"{COORDINATOR}._get_average_price", fake)


MITTEL_2025 = {7: 80.0, 8: 80.0, 9: 60.0, 10: 40.0, 11: 20.0, 12: 10.0}


async def test_a_self_sufficiency_sensor_in_percent(contract):
    data = {**ELEKTRO, "pv_autarkie": True, "autarkie_sensor": "sensor.autarkie"}
    with _mittel(MITTEL_2025, 40.0):
        _, d = await _setup(contract, data, _stats(netz=None, haus=None))
    assert d["autarkie_aktiv"] is True and d["autarkie_variante"] == "entitaet"
    assert d["verbrauch_hochgerechnet"] == pytest.approx(_projection(0.4, [80, 80, 60, 40, 20, 10]), abs=0.5)
    assert d["autarkie_bisher"] == 40.0
    assert {m["quelle"] for m in d["autarkie_monatswerte"]} == {"statistik"}
    assert d["verbrauch_gesamt_bisher"] is None and d["verbrauch_pv_gedeckt_hochgerechnet"] is None  # no total consumption


async def test_the_sensor_values_are_clamped(contract):
    data = {**ELEKTRO, "pv_autarkie": True, "autarkie_sensor": "sensor.autarkie"}
    with _mittel({m: 140.0 for m in range(7, 13)}, 40.0):
        _, d = await _setup(contract, data, _stats(netz=None, haus=None))
    assert all(m["autarkie"] == 100.0 for m in d["autarkie_monatswerte"])  # more than 100 % cannot be


async def test_a_month_without_sensor_data_takes_the_own_value(contract):
    data = {**ELEKTRO, "pv_autarkie": True, "autarkie_sensor": "sensor.autarkie", "autarkie_manuell": MANUELL}
    with _mittel({m: v for m, v in MITTEL_2025.items() if m != 9}, 40.0):
        _, d = await _setup(contract, data, _stats(netz=None, haus=None))
    quellen = {m["monat"]: m["quelle"] for m in d["autarkie_monatswerte"]}
    assert quellen["2026-09"] == "manuell" and quellen["2026-08"] == "statistik"


async def test_the_total_consumption_comes_first(contract):
    data = {**PV, "autarkie_sensor": "sensor.autarkie", "autarkie_manuell": MANUELL}
    with _mittel(MITTEL_2025, 40.0):
        _, d = await _setup(contract, data)
    assert d["autarkie_variante"] == "gesamtverbrauch"
    assert d["verbrauch_hochgerechnet"] == pytest.approx(_expected_projection(), abs=0.5)  # not the sensor, not the own values


async def test_a_sensor_or_own_values_apply_to_both_tariffs_alike(contract):
    data = {**HT_NT, "gesamtverbrauch_sensor": None, "autarkie_manuell": MANUELL}
    data.pop("gesamtverbrauch_sensor")
    _, d = await _setup(contract, data, _stats(netz=None, haus=None, **{NT: None}))
    assert d["autarkie_variante"] == "manuell" and d["autarkie_naeherung"] is False  # no approximation: same value by design
    assert all(m["autarkie"] == m["autarkie_nt"] for m in d["autarkie_monatswerte"])


# ------------------------------------------------------------------ form: the new fields
async def test_the_form_has_the_sensor_and_the_own_values(hass):
    for sparte in ("electricity", "electricity_ht_nt"):
        assert {"autarkie_sensor", "autarkie_manuell"} <= _keys(await _start(hass, sparte))
    for language in ("en", "de"):
        texts = json.loads((TRANSLATIONS / f"{language}.json").read_text(encoding="utf-8"))["config"]
        for step in ("energie", "reconfigure_energie", "energie_ht_nt", "reconfigure_energie_ht_nt"):
            for key in ("autarkie_sensor", "autarkie_manuell"):
                assert texts["step"][step]["data"][key] and texts["step"][step]["data_description"][key], (language, step, key)
        assert texts["error"]["pv_manuell"] and texts["error"]["pv_manuell_gleich"]


async def test_unusable_own_values_are_refused_and_good_ones_saved(hass):
    base = {"arbeitspreis": 0.3, "grundpreis": 10, "abschlag": 100, "pv_autarkie": True}
    result = await _start(hass, "electricity")
    bad = await hass.config_entries.flow.async_configure(result["flow_id"], {**base, "autarkie_manuell": "10 20 30"})
    assert bad["type"].value == "form" and bad["errors"] == {"autarkie_manuell": "pv_manuell"}
    assert bad["step_id"] == "energie"
    good = await hass.config_entries.flow.async_configure(bad["flow_id"], {**base, "autarkie_manuell": MANUELL})
    assert good["type"].value == "create_entry" and good["data"]["autarkie_manuell"] == MANUELL


async def test_equal_own_values_without_a_sensor_are_refused_with_a_hint(hass):
    """One value (or twelve equal ones) changes nothing on its own: the season factor is always 1 (Issue 86)."""
    base = {"arbeitspreis": 0.3, "grundpreis": 10, "abschlag": 100, "pv_autarkie": True}
    for text in ("40", "40,0", "40 40 40 40 40 40 40 40 40 40 40 40"):
        result = await _start(hass, "electricity")
        bad = await hass.config_entries.flow.async_configure(result["flow_id"], {**base, "autarkie_manuell": text})
        assert bad["type"].value == "form", text
        assert bad["errors"] == {"autarkie_manuell": "pv_manuell_gleich"}, text


async def test_equal_own_values_stay_possible_with_a_sensor_or_when_off(hass):
    base = {"arbeitspreis": 0.3, "grundpreis": 10, "abschlag": 100}
    # next to a sensor a single value is a fallback for months without data
    result = await _start(hass, "electricity")
    good = await hass.config_entries.flow.async_configure(
        result["flow_id"], {**base, "pv_autarkie": True, "autarkie_sensor": "sensor.autarkie", "autarkie_manuell": "40"}
    )
    assert good["type"].value == "create_entry"
    # switched off: nothing is checked beyond the format
    result = await _start(hass, "electricity")
    good = await hass.config_entries.flow.async_configure(result["flow_id"], {**base, "autarkie_manuell": "40"})
    assert good["type"].value == "create_entry"


async def test_editing_keeps_the_new_fields(frontend_env, contract, hass):  # noqa: F811
    data = {**PV, "autarkie_sensor": "sensor.autarkie", "autarkie_manuell": MANUELL}
    entry, _ = await _setup(contract, data)
    new = await _reconfigure(hass, entry)
    assert new["autarkie_sensor"] == "sensor.autarkie" and new["autarkie_manuell"] == MANUELL
