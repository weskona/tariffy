"""Zaehler in Wh oder MWh statt kWh (Issue 74): der Verbrauch wird in kWh gerechnet."""

from __future__ import annotations

import pytest

from .test_coordinator import SENSOR, STROM

TODAY = "2026-07-12"


def _states(hass, unit, value):
    attrs = {"unit_of_measurement": unit} if unit else {}
    hass.states.async_set(SENSOR, value, attrs)


async def test_kwh_is_unchanged(contract, hass):
    _states(hass, "kWh", "2481.17")
    _, d = await contract.setup(STROM, today=TODAY, latest=(2481.17, 2481.17), offset=(1000.0, 1000.0))
    assert d["verbrauch_bisher"] == pytest.approx(1481.17)
    assert d["kosten_bisher"] == pytest.approx(1481.17 * 0.2977 + 11.51 * 192 / 30.44, abs=0.02)


async def test_a_sensor_without_a_unit_is_unchanged(contract, hass):
    _states(hass, None, "2481.17")
    _, d = await contract.setup(STROM, today=TODAY, latest=(2481.17, 2481.17), offset=(1000.0, 1000.0))
    assert d["verbrauch_bisher"] == pytest.approx(1481.17)


async def test_wh_is_converted_to_kwh(contract, hass):
    _states(hass, "Wh", "2481170")
    _, d = await contract.setup(STROM, today=TODAY, latest=(2481170.0, 2481170.0), offset=(1000000.0, 1000000.0))
    assert d["verbrauch_bisher"] == pytest.approx(1481.17)  # not 1,481,170
    assert d["kosten_bisher"] == pytest.approx(1481.17 * 0.2977 + 11.51 * 192 / 30.44, abs=0.02)
    assert d["verbrauch_hochgerechnet"] < 5000  # a year of a household, not 53,000 kWh


async def test_mwh_is_converted_to_kwh(contract, hass):
    _states(hass, "MWh", "2.48117")
    _, d = await contract.setup(STROM, today=TODAY, latest=(2.48117, 2.48117), offset=(1.0, 1.0))
    assert d["verbrauch_bisher"] == pytest.approx(1481.17)


async def test_a_manual_start_value_is_read_in_the_unit_of_the_meter(contract, hass):
    _states(hass, "Wh", "2481170")
    data = {**STROM, "verbrauch_start_wert": 1000000.0}  # the reading as the meter shows it
    _, d = await contract.setup(data, today=TODAY)
    assert d["verbrauch_bisher"] == pytest.approx(1481.17)


async def test_the_low_tariff_register_is_converted_too(contract, hass):
    hass.states.async_set("sensor.nt", "500000", {"unit_of_measurement": "Wh"})
    _states(hass, "Wh", "2481170")
    data = {
        **STROM, "sparte": "electricity_ht_nt", "verbrauch_sensor_nt": "sensor.nt",
        "arbeitspreis_nt": 0.2, "arbeitspreis": 0.3,
    }
    _, d = await contract.setup(
        data, today=TODAY, latest=(2481170.0, 2481170.0), offset=(1000000.0, 1000000.0),
        latest_nt=(500000.0, 500000.0), offset_nt=(100000.0, 100000.0),
    )
    assert d["verbrauch_bisher_ht"] == pytest.approx(1481.17)
    assert d["verbrauch_bisher_nt"] == pytest.approx(400.0)


async def test_the_panel_names_kwh_for_a_wh_meter(contract, hass):
    from custom_components.tariffy import panel

    _states(hass, "Wh", "2481170")
    entry, _ = await contract.setup(STROM, today=TODAY, latest=(2481170.0, 2481170.0), offset=(1000000.0, 1000000.0))
    assert panel.contract_payload(hass, entry)["verbrauch_einheit"] == "kWh"
    _states(hass, "kWh", "2481.17")
    assert panel.contract_payload(hass, entry)["verbrauch_einheit"] == "kWh"
    _states(hass, "m³", "12")
    assert panel.contract_payload(hass, entry)["verbrauch_einheit"] == "m³"  # other units are shown as they are


async def test_an_old_term_is_worked_out_in_kwh_for_a_wh_meter(contract, hass):
    from datetime import date
    from unittest.mock import patch

    from custom_components.tariffy import history

    _states(hass, "Wh", "2481170")
    entry, _ = await contract.setup(STROM, today=TODAY, latest=(2481170.0, 2481170.0), offset=(1000000.0, 1000000.0))
    stats = {date(2024, 1, 1): (1000000.0, 1000000.0), date(2025, 1, 1): (4200000.0, 4200000.0)}

    async def fake(_hass, _entity_id, at_date):
        return stats.get(at_date, (None, None))

    with patch("custom_components.tariffy.coordinator._get_historic_value", fake):
        result = await history.async_calc(
            hass, entry, {"beginn": "2024-01-01", "ende": "2024-12-31", "arbeitspreis": 0.30, "abschlag": 90.0}
        )
    assert result["values"]["verbrauch"] == pytest.approx(3200.0)  # kWh, not 3,200,000
