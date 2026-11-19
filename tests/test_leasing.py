"""Leasing als Vertragsart (Issue 90): Formular, Kilometerrechnung, Sensoren, Tarifwechsel."""

from __future__ import annotations

from datetime import date

import pytest
from homeassistant.data_entry_flow import FlowResultType

from custom_components.tariffy import backup, leasing

from .test_insurance import _assert_texts, _keys, _start
from .test_panel import GOLDEN, frontend_env  # noqa: F401  (fixture)
from .test_reconfigure import _reconfigure

KM = "sensor.auto_kilometerstand"
LEASING = {
    "sparte": "leasing",
    "anbieter": "Autobank",
    "tarif": "Leasing",
    "abschlag": 299.0,
    "beginn": "2026-01-01",
    "ende": "2027-01-01",  # 365 days
    "km_start": 20000.0,
    "km_gesamt": 12000.0,
    "km_toleranz_oben": 0.0,
    "km_toleranz_unten": 0.0,
    "preis_mehrkm": 0.10,
    "preis_minderkm": 0.05,
    "km_sensor": KM,
    "erinnerung_monate": "0",
}
TODAY = {**GOLDEN, "today": "2026-07-01"}  # day 181 of 365


def _day(km):
    """The test day with the odometer sensor at `km`."""
    return {**TODAY, "sensor_states": {**TODAY["sensor_states"], KM: str(km)}}


# ---------------------------------------------------------------- the pure calculation
def test_the_allowed_kilometres_come_from_the_total_or_from_the_years():
    assert leasing.erlaubt_gesamt({"km_gesamt": 30000, "km_pro_jahr": 10000}, 1095) == 30000  # the total wins
    assert leasing.erlaubt_gesamt({"km_pro_jahr": 10000}, 1461) == pytest.approx(40000, abs=10)  # 4 years
    assert leasing.erlaubt_gesamt({"km_pro_jahr": 10000}, 0) is None
    assert leasing.erlaubt_gesamt({}, 365) is None


def test_projection_extra_kilometres_and_their_price():
    """By hand: 6000 km in 181 of 365 days -> 6000/181*365 = 12099.45 km at return, 99.45 over 12000."""
    d = leasing.berechne(LEASING, date(2026, 7, 1), 26000.0)
    assert d["leasing_km_gefahren"] == 6000 and d["leasing_km_stand"] == 26000
    assert d["leasing_km_soll"] == pytest.approx(12000 * 181 / 365, abs=0.5)
    assert d["leasing_km_abweichung"] == pytest.approx(6000 - 12000 * 181 / 365, abs=0.5)
    assert d["leasing_km_hochgerechnet"] == pytest.approx(6000 / 181 * 365, abs=0.5)
    assert d["leasing_mehr_km"] == pytest.approx(6000 / 181 * 365 - 12000, abs=0.5) and d["leasing_minder_km"] == 0
    assert d["leasing_nachzahlung"] == pytest.approx((6000 / 181 * 365 - 12000) * 0.10, abs=0.01)
    assert d["leasing_gutschrift"] is None or d["leasing_gutschrift"] == 0
    assert d["leasing_km_kosten"] == d["leasing_nachzahlung"]
    assert d["leasing_km_rest"] == 6000 and d["leasing_km_rest_je_tag"] == pytest.approx(6000 / 184, abs=0.05)


def test_the_tolerance_upwards_is_not_charged():
    d = leasing.berechne({**LEASING, "km_toleranz_oben": 500.0}, date(2026, 7, 1), 26000.0)
    assert d["leasing_km_abweichung_ende"] == pytest.approx(99.45, abs=0.5)
    assert d["leasing_mehr_km"] == 0 and d["leasing_nachzahlung"] == 0


def test_kilometres_not_driven_are_credited_beyond_the_tolerance():
    """2000 km in 181 days -> 4033.15 km at return, 7966.85 under 12000; 1000 km tolerance."""
    d = leasing.berechne({**LEASING, "km_toleranz_unten": 1000.0}, date(2026, 7, 1), 22000.0)
    assert d["leasing_km_hochgerechnet"] == pytest.approx(2000 / 181 * 365, abs=0.5)
    minder = 12000 - 2000 / 181 * 365 - 1000
    assert d["leasing_minder_km"] == pytest.approx(minder, abs=0.5) and d["leasing_mehr_km"] == 0
    assert d["leasing_gutschrift"] == pytest.approx(minder * 0.05, abs=0.01)
    assert d["leasing_km_kosten"] == pytest.approx(-minder * 0.05, abs=0.01)  # a credit is negative


def test_without_prices_there_is_no_money_figure():
    data = {k: v for k, v in LEASING.items() if k not in ("preis_mehrkm", "preis_minderkm")}
    d = leasing.berechne(data, date(2026, 7, 1), 26000.0)
    assert d["leasing_mehr_km"] > 0 and d["leasing_km_kosten"] is None and d["leasing_nachzahlung"] is None


def test_the_manual_odometer_is_used_without_a_sensor_and_the_sensor_wins():
    data = {**LEASING, "km_aktuell": 25000.0}
    assert leasing.berechne(data, date(2026, 7, 1), None)["leasing_km_gefahren"] == 5000
    assert leasing.berechne(data, date(2026, 7, 1), 26000.0)["leasing_km_gefahren"] == 6000


@pytest.mark.parametrize("stand", [None, 19000.0])  # nothing yet, or below the start
def test_no_usable_odometer_means_no_figures(stand):
    d = leasing.berechne(LEASING, date(2026, 7, 1), stand)
    assert "leasing_km_gefahren" not in d and "leasing_km_hochgerechnet" not in d


def test_a_projection_needs_two_weeks():
    d = leasing.berechne(LEASING, date(2026, 1, 8), 20300.0)  # day 7
    assert d["leasing_km_gefahren"] == 300 and "leasing_km_hochgerechnet" not in d
    assert d["leasing_km_rest"] == 11700  # the plain figures are there


def test_after_the_return_date_the_driven_kilometres_are_the_result():
    d = leasing.berechne(LEASING, date(2027, 3, 1), 33000.0)
    assert d["leasing_km_hochgerechnet"] == 13000 and d["leasing_mehr_km"] == 1000
    assert d["leasing_nachzahlung"] == pytest.approx(100.0, abs=0.01)


def test_the_years_give_the_allowance_without_a_total():
    data = {k: v for k, v in LEASING.items() if k != "km_gesamt"} | {"km_pro_jahr": 12000.0}
    assert leasing.berechne(data, date(2026, 7, 1), 26000.0)["leasing_km_erlaubt"] == pytest.approx(11992, abs=2)


# ---------------------------------------------------------------- the form
async def test_the_form_asks_for_the_kilometres_and_is_translated(hass):
    result = await _start(hass, "leasing")
    assert result["step_id"] == "leasing"
    assert _keys(result) == {
        "kennzeichen", "km_sensor", "km_aktuell", "km_start", "km_pro_jahr", "km_gesamt",
        "km_toleranz_oben", "km_toleranz_unten", "preis_mehrkm", "preis_minderkm",
    }
    _assert_texts(result)


async def test_a_leasing_contract_is_created_in_two_steps(hass):
    result = await _start(hass, "leasing")
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {"km_start": 5000, "km_gesamt": 30000, "km_sensor": KM, "preis_mehrkm": 0.08}
    )
    assert result["type"] is FlowResultType.FORM and result["step_id"] == "pauschal"  # the rate follows
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {"zahlweise": "monthly", "abschlag": 249.0}
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    data = result["data"]
    assert data["sparte"] == "leasing" and data["km_gesamt"] == 30000 and data["km_sensor"] == KM
    assert data["abschlag"] == 249.0 and data["preis_mehrkm"] == 0.08


async def test_the_kilometre_fields_are_optional(hass):
    result = await _start(hass, "leasing")
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {})
    assert result["step_id"] == "pauschal"


# ---------------------------------------------------------------- the running contract
async def test_the_figures_of_the_running_lease(contract):
    _, d = await contract.setup(LEASING, **_day(26000))
    assert d["leasing_km_gefahren"] == 6000 and d["leasing_km_erlaubt"] == 12000
    assert d["leasing_mehr_km"] == pytest.approx(6000 / 181 * 365 - 12000, abs=0.5)
    assert d["abschlag"] == 299.0 and d["verlaengerbar"] is True  # still a flat-rate contract
    assert d["km_toleranz_oben"] == 0.0 and d["preis_mehrkm"] == 0.10


async def test_the_sensor_in_miles_is_converted(contract, hass):
    hass.states.async_set(KM, "10000", {"unit_of_measurement": "mi"})
    data = {**LEASING, "km_start": 0.0, "km_gesamt": 30000.0}
    _, d = await contract.setup(data, **TODAY)
    assert d["leasing_km_stand"] == pytest.approx(16093, abs=1)


async def test_a_missing_or_broken_sensor_falls_back_to_the_manual_odometer(contract):
    _, d = await contract.setup({**LEASING, "km_aktuell": 25000.0}, **_day("unavailable"))
    assert d["leasing_km_gefahren"] == 5000


async def test_without_any_odometer_nothing_breaks(contract):
    data = {k: v for k, v in LEASING.items() if k != "km_sensor"}
    _, d = await contract.setup(data, **TODAY)
    assert "leasing_km_gefahren" not in d and d["abschlag"] == 299.0


async def test_the_lease_has_its_own_sensors_and_the_vehicle_ones(contract, hass):
    _, d = await contract.setup({**LEASING, "kennzeichen": "B-XY 1"}, **_day(26000))
    ids = hass.states.async_entity_ids("sensor")
    driven = hass.states.get([e for e in ids if "kilometres_driven" in e][0])
    assert float(driven.state) == 6000 and driven.attributes["unit_of_measurement"] == "km"
    assert driven.attributes["km_erlaubt"] == 12000
    assert [e for e in ids if "projected_kilometres" in e] and [e for e in ids if "kilometre_cost" in e]
    assert [e for e in ids if "odometer_at_contract_start" in e]  # the car sensors of the insurance, too


async def test_other_contracts_get_no_leasing_sensor(contract, hass):
    await contract.setup(
        {"sparte": "internet", "abschlag": 40.0, "beginn": "2026-01-01", "erinnerung_monate": "0"}, **TODAY
    )
    assert not [e for e in hass.states.async_entity_ids("sensor") if "kilometres_driven" in e]


async def test_editing_keeps_the_kilometre_fields_and_internal_state(frontend_env, contract, hass):  # noqa: F811
    einmal = [{"bezeichnung": "Sonderzahlung", "betrag": 1000.0, "datum": None}]
    entry, _ = await contract.setup({**LEASING, "_einmalposten": einmal}, **_day(26000))
    data = await _reconfigure(hass, entry, second={"abschlag": 310.0})
    assert data["abschlag"] == 310.0 and data["km_gesamt"] == 12000.0 and data["km_sensor"] == KM
    assert data["_einmalposten"]


async def test_a_tariff_switch_keeps_the_vehicle_but_not_the_old_odometer(contract):
    options = {"next_beginn": "2026-07-01", "next_ende": "2027-07-01", "next_anbieter": "Neu", "next_abschlag": 320.0}
    data = {**LEASING, "km_aktuell": 25000.0, "kennzeichen": "B-XY 1", "km_pro_jahr": 10000.0}
    entry, _ = await contract.setup(data, options=options, **_day(26000))
    new = entry.data
    assert new["anbieter"] == "Neu" and new["abschlag"] == 320.0 and new["beginn"] == "2026-07-01"
    assert new["km_sensor"] == KM and new["km_gesamt"] == 12000.0 and new["kennzeichen"] == "B-XY 1"
    assert new["preis_mehrkm"] == 0.10 and new["km_toleranz_oben"] == 0.0 and new["km_pro_jahr"] == 10000.0
    assert "km_start" not in new and "km_aktuell" not in new  # they belonged to the old term


def test_the_lease_survives_a_backup():
    data = backup.sanitize_contract({"title": "Leasing", "data": LEASING})["data"]
    assert data["km_gesamt"] == 12000.0 and data["preis_mehrkm"] == 0.10 and data["km_sensor"] == KM
