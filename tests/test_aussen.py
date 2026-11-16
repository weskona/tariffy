"""Aussenzaehler (Garten, Pool, ...) eines Wasservertrags: nicht abwasserpflichtig (Issue 73)."""

from __future__ import annotations

import pytest

from .test_panel import frontend_env  # noqa: F401  (fixture)

MAIN = "sensor.wasser_haupt"
GARDEN = "sensor.wasser_garten"
WATER = {
    "sparte": "water",
    "anbieter": "Stadtwerke",
    "arbeitspreis": 2.0,
    "grundpreis": 5.0,
    "abschlag": 30.0,
    "beginn": "2026-01-01",
    "ende": "2026-12-31",
    "erinnerung_monate": "0",
    "verbrauch_sensor": MAIN,
    "abwasser_typ": "price_per_unit",
    "arbeitspreis_abwasser": 3.0,
}
GARTEN = {"name": "Garten", "sensor": GARDEN}
MONTHS = 192 / 30.44  # 2026-01-01 .. 2026-07-12


async def _setup(contract, hass, *, zaehler=None, main=150.0, garden=40.0, garden_unit="m³", **data):
    hass.states.async_set(MAIN, str(main), {"unit_of_measurement": "m³"})
    hass.states.async_set(GARDEN, str(garden), {"unit_of_measurement": garden_unit})
    extra = {GARDEN: ((garden, garden), (0.0, 0.0))}
    payload = {**WATER, **data}
    if zaehler is not None:
        payload["_aussenzaehler"] = zaehler
    return await contract.setup(
        payload, today="2026-07-12", latest=(main, main), offset=(0.0, 0.0), extra=extra
    )


async def test_without_an_outdoor_meter_nothing_changes(contract, hass):
    _, d = await _setup(contract, hass)
    assert d["aussenzaehler"] == [] and d["garten_verbrauch"] is None
    assert d["arbeitspreis_gesamt_wasser"] == pytest.approx(5.0)
    assert d["kosten_bisher"] == pytest.approx(150 * 5.0 + 5.0 * MONTHS, abs=0.02)
    assert not [e for e in hass.states.async_entity_ids("sensor") if "outdoor_water" in e]


async def test_the_outdoor_water_is_taken_out_of_the_wastewater(contract, hass):
    _, d = await _setup(contract, hass, zaehler=[GARTEN])
    assert d["garten_verbrauch"] == pytest.approx(40.0)
    assert d["abwasserpflichtiger_verbrauch"] == pytest.approx(110.0)  # 150 - 40
    assert d["garten_kosten"] == pytest.approx(80.0)  # 40 at the fresh-water price 2.0
    assert d["abwasser_kosten"] == pytest.approx(330.0)  # 110 at the wastewater price 3.0
    # total: 110 at 5.0 + 40 at 2.0 + base price
    assert d["kosten_bisher"] == pytest.approx(110 * 5.0 + 40 * 2.0 + 5.0 * MONTHS, abs=0.02)
    assert d["aussenzaehler"][0]["name"] == "Garten" and d["aussenzaehler"][0]["kosten"] == pytest.approx(80.0)
    assert [e for e in hass.states.async_entity_ids("sensor") if "outdoor_water" in e]  # extra sensors exist


async def test_an_own_price_for_the_outdoor_meter(contract, hass):
    _, d = await _setup(contract, hass, zaehler=[{**GARTEN, "preis": 1.5}])
    assert d["garten_kosten"] == pytest.approx(60.0)
    assert d["kosten_bisher"] == pytest.approx(110 * 5.0 + 40 * 1.5 + 5.0 * MONTHS, abs=0.02)


async def test_several_meters_add_up(contract, hass):
    _, d = await _setup(contract, hass, zaehler=[GARTEN, {"name": "Pool", "sensor": GARDEN}])
    assert d["garten_verbrauch"] == pytest.approx(80.0)
    assert d["abwasserpflichtiger_verbrauch"] == pytest.approx(70.0)


async def test_more_than_the_main_meter_is_capped(contract, hass):
    _, d = await _setup(contract, hass, zaehler=[GARTEN], main=30.0, garden=40.0)
    assert d["garten_verbrauch"] == pytest.approx(30.0)  # cannot exceed what the main meter counted
    assert d["abwasserpflichtiger_verbrauch"] == pytest.approx(0.0)


async def test_a_meter_in_litres_is_converted_to_m3(contract, hass):
    _, d = await _setup(contract, hass, zaehler=[GARTEN], garden=40000.0, garden_unit="L")
    assert d["garten_verbrauch"] == pytest.approx(40.0)


async def test_a_start_value_is_read_in_the_unit_of_the_meter(contract, hass):
    _, d = await _setup(contract, hass, zaehler=[{**GARTEN, "start_wert": 10.0}])
    assert d["garten_verbrauch"] == pytest.approx(30.0)  # 40 now, 10 at the start


async def test_the_forecast_follows_the_weighted_price(contract, hass):
    _, plain = await _setup(contract, hass)
    _, d = await _setup(contract, hass, zaehler=[GARTEN])
    assert d["prognose_real"] > plain["prognose_real"]  # cheaper without wastewater on the garden water


async def test_flat_rate_wastewater_is_not_affected_by_the_meter(contract, hass):
    _, d = await _setup(contract, hass, zaehler=[GARTEN], abwasser_typ="flat_rate", arbeitspreis_abwasser=8.0)
    assert d["abwasser_kosten"] == pytest.approx(0.0)
    assert d["kosten_bisher"] == pytest.approx(150 * 2.0 + 5.0 * MONTHS, abs=0.02)


async def _call(client, kind, **extra):
    await client.send_json_auto_id({"type": f"tariffy/{kind}", **extra})
    return await client.receive_json()


async def test_save_edit_and_delete(frontend_env, contract, hass, hass_ws_client):  # noqa: F811
    client = await hass_ws_client()
    entry, _ = await _setup(contract, hass)
    reply = await _call(client, "aussen_save", entry_id=entry.entry_id, values={"name": "Garten", "sensor": GARDEN, "start_wert": 5})
    assert reply["success"] is True
    await hass.async_block_till_done()
    assert entry.data["_aussenzaehler"] == [{"name": "Garten", "sensor": GARDEN, "start_wert": 5.0}]
    reply = await _call(client, "aussen_save", entry_id=entry.entry_id, index=0, values={"name": "Beet", "sensor": GARDEN, "preis": 1.2})
    assert reply["success"] is True
    assert entry.data["_aussenzaehler"] == [{"name": "Beet", "sensor": GARDEN, "preis": 1.2}]
    assert (await _call(client, "aussen_delete", entry_id=entry.entry_id, index=4))["success"] is False
    assert (await _call(client, "aussen_delete", entry_id=entry.entry_id, index=0))["success"] is True
    assert "_aussenzaehler" not in entry.data


@pytest.mark.parametrize(
    ("values", "code"),
    [
        ({"name": "", "sensor": GARDEN}, "invalid_name"),
        ({"name": "X", "sensor": "kein sensor"}, "invalid_sensor"),
        ({"name": "X", "sensor": MAIN}, "same_sensor"),
        ({"name": "X", "sensor": GARDEN, "preis": -1}, "invalid_preis"),
        ({"name": "X", "sensor": GARDEN, "start_wert": "abc"}, "invalid_start_wert"),
    ],
)
async def test_bad_input_is_refused(frontend_env, contract, hass, hass_ws_client, values, code):  # noqa: F811
    client = await hass_ws_client()
    entry, _ = await _setup(contract, hass)
    reply = await _call(client, "aussen_save", entry_id=entry.entry_id, values=values)
    assert reply["success"] is False and reply["error"]["code"] == code
    assert "_aussenzaehler" not in entry.data


async def test_only_water_contracts_have_outdoor_meters(frontend_env, contract, hass, hass_ws_client):  # noqa: F811
    client = await hass_ws_client()
    hass.states.async_set(GARDEN, "1")
    entry, _ = await contract.setup(
        {"sparte": "electricity", "arbeitspreis": 0.3, "abschlag": 40.0, "beginn": "2026-01-01", "erinnerung_monate": "0"},
        today="2026-07-12",
    )
    reply = await _call(client, "aussen_save", entry_id=entry.entry_id, values=GARTEN)
    assert reply["success"] is False and reply["error"]["code"] == "not_available"


async def test_the_meters_stay_after_a_tariff_switch_without_their_start_value(contract, hass):
    options = {"next_beginn": "2026-07-01", "next_ende": "2027-06-30", "next_anbieter": "Neu", "next_arbeitspreis": 2.5}
    entry, _ = await _setup(contract, hass, zaehler=[{**GARTEN, "start_wert": 10.0}], **{})
    contract.hass.config_entries.async_update_entry(entry, options=options)
    await entry.runtime_data.async_refresh()
    await hass.async_block_till_done()
    assert entry.data["anbieter"] == "Neu"
    assert entry.data["_aussenzaehler"] == [GARTEN]  # still connected, the start value belonged to the old contract


def test_the_meters_survive_a_backup():
    from custom_components.tariffy import backup

    contract = {"title": "Wasser", "data": {**WATER, "_aussenzaehler": [{**GARTEN, "start_wert": 3.0, "preis": 1.2}]}}
    assert backup.sanitize_contract(contract)["data"]["_aussenzaehler"] == [{**GARTEN, "start_wert": 3.0, "preis": 1.2}]
