"""Insurance contracts: type, licence plate and odometer figures (issue #57)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.helpers import entity_registry as er

from custom_components.tariffy import panel
from custom_components.tariffy.const import DOMAIN
from custom_components.tariffy.diagnostics import async_get_config_entry_diagnostics

from .test_reconfigure import _form_defaults

NEW_FIELDS = {"versicherungsart", "kennzeichen", "km_start", "km_pro_jahr"}

KFZ = {
    "sparte": "insurance",
    "anbieter": "Versicherer AG",
    "abschlag": 45.0,
    "beginn": "2026-01-01",
    "ende": "2026-12-31",
    "versicherungsart": "car",
    "kennzeichen": "B-XY 1234",
    "km_start": 12000.0,
    "km_pro_jahr": 10000.0,
    "erinnerung_monate": "0",
}


async def _start(hass, sparte):
    """Name and kind chosen: the result is the step the kind leads to."""
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": "user"})
    return await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"name": "Vertrag", "sparte": sparte, "anbieter": "Anbieter", "erinnerung_monate": "0"},
    )


def _keys(result):
    return {str(k) for k in result["data_schema"].schema}


TRANSLATIONS = Path(__file__).parent.parent / "custom_components" / "tariffy" / "translations"


def _assert_texts(result):
    """Every field of the form has a label and a description in both languages, and the step has a title."""
    for language in ("en", "de"):
        step = json.loads((TRANSLATIONS / f"{language}.json").read_text(encoding="utf-8"))["config"]["step"][result["step_id"]]
        assert step["title"] and step["description"], (language, result["step_id"])
        for key in _keys(result):
            assert step["data"].get(key), (language, result["step_id"], key)
            if "versicherung" in result["step_id"]:  # the new steps explain every field
                assert step["data_description"].get(key), (language, result["step_id"], key)


async def test_every_step_of_an_insurance_has_its_texts(hass, setup_contract):
    result = await _start(hass, "insurance")
    _assert_texts(result)
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"versicherungsart": "car"})
    _assert_texts(result)
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {})
    _assert_texts(result)
    entry, _ = await setup_contract(dict(KFZ))
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "reconfigure", "entry_id": entry.entry_id}
    )
    for _step in range(4):
        _assert_texts(result)
        result = await hass.config_entries.flow.async_configure(result["flow_id"], _form_defaults(result))
        if result["type"] is not FlowResultType.FORM:
            break
    assert result["type"] is FlowResultType.ABORT


async def test_the_name_of_an_insurance_can_be_changed_in_the_longer_flow(hass, setup_contract):
    entry, _ = await setup_contract(dict(KFZ))
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "reconfigure", "entry_id": entry.entry_id}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {**_form_defaults(result), "name": "Kfz Allianz"}
    )
    for _step in range(3):
        result = await hass.config_entries.flow.async_configure(result["flow_id"], _form_defaults(result))
    assert result["type"] is FlowResultType.ABORT
    await hass.async_block_till_done()
    assert entry.title == "Kfz Allianz"
    assert "name" not in entry.data


async def test_an_insurance_asks_what_it_covers_first(hass):
    result = await _start(hass, "insurance")
    assert result["step_id"] == "versicherung"
    assert _keys(result) == {"versicherungsart"}
    assert result["last_step"] is False  # the costs follow


async def test_a_car_insurance_asks_for_the_car_details_and_then_for_the_costs(hass):
    result = await _start(hass, "insurance")
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"versicherungsart": "car"})
    assert result["step_id"] == "versicherung_kfz"
    assert _keys(result) == {"kennzeichen", "km_start", "km_pro_jahr"}
    assert result["last_step"] is False
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {"kennzeichen": "B-XY 1234", "km_start": 12000, "km_pro_jahr": 10000}
    )
    assert result["step_id"] == "pauschal"
    assert not NEW_FIELDS & _keys(result)  # the cost step has no insurance fields
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"abschlag": 45.0})
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"]["versicherungsart"] == "car"
    assert result["data"]["kennzeichen"] == "B-XY 1234"
    assert result["data"]["km_start"] == 12000
    assert result["data"]["km_pro_jahr"] == 10000
    assert result["data"]["abschlag"] == 45.0


@pytest.mark.parametrize("art", ["house", "household", "liability", "health", "life", "legal", "accident", "other"])
async def test_every_other_kind_goes_straight_to_the_costs(hass, art):
    result = await _start(hass, "insurance")
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"versicherungsart": art})
    assert result["step_id"] == "pauschal"  # no plate, no kilometres
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"abschlag": 20.0})
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"]["versicherungsart"] == art
    assert not {"kennzeichen", "km_start", "km_pro_jahr"} & set(result["data"])


async def test_the_details_are_optional(hass):
    result = await _start(hass, "insurance")
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {})
    assert result["step_id"] == "pauschal"
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"abschlag": 20.0})
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert "versicherungsart" not in result["data"]


async def test_a_car_insurance_may_leave_the_car_details_empty(hass):
    result = await _start(hass, "insurance")
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"versicherungsart": "car"})
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {})
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"abschlag": 20.0})
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"]["versicherungsart"] == "car"


@pytest.mark.parametrize("sparte", ["internet", "mobile", "other"])
async def test_other_flat_rate_contracts_go_straight_to_the_costs(hass, sparte):
    result = await _start(hass, sparte)
    assert result["step_id"] == "pauschal"
    assert not NEW_FIELDS & _keys(result)


async def _reconfigure_to(hass, entry, art):
    """Edit an insurance: general data, type, [car details], costs; returns the entry data."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "reconfigure", "entry_id": entry.entry_id}
    )
    result = await hass.config_entries.flow.async_configure(result["flow_id"], _form_defaults(result))
    assert result["step_id"] == "reconfigure_versicherung"
    assert _form_defaults(result)["versicherungsart"] == entry.data.get("versicherungsart")  # filled in
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"versicherungsart": art})
    steps = [result["step_id"]]
    if art == "car":
        assert result["step_id"] == "reconfigure_versicherung_kfz"
        assert _form_defaults(result)["kennzeichen"] == "B-XY 1234"
        result = await hass.config_entries.flow.async_configure(result["flow_id"], _form_defaults(result))
        steps.append(result["step_id"])
    assert result["step_id"] == "reconfigure_pauschal"
    result = await hass.config_entries.flow.async_configure(result["flow_id"], _form_defaults(result))
    assert result["type"] is FlowResultType.ABORT and result["reason"] == "reconfigure_successful"
    await hass.async_block_till_done()
    return entry.data, steps


async def test_editing_a_car_insurance_keeps_the_car_details(hass, setup_contract):
    entry, _ = await setup_contract({**KFZ, "_historie": [{"anbieter": "Alt"}]})
    data, steps = await _reconfigure_to(hass, entry, "car")
    assert steps == ["reconfigure_versicherung_kfz", "reconfigure_pauschal"]
    assert data["kennzeichen"] == "B-XY 1234" and data["km_start"] == 12000.0 and data["km_pro_jahr"] == 10000.0
    assert data["_historie"] == [{"anbieter": "Alt"}]  # internal state stays


async def test_changing_the_type_away_from_car_drops_the_car_details(hass, setup_contract):
    entry, _ = await setup_contract(dict(KFZ))
    data, steps = await _reconfigure_to(hass, entry, "house")
    assert steps == ["reconfigure_pauschal"]  # no car step
    assert data["versicherungsart"] == "house"
    assert not {"kennzeichen", "km_start", "km_pro_jahr"} & set(data)


async def test_an_insurance_has_sensors_for_them(hass, setup_contract):
    entry, data = await setup_contract(dict(KFZ))
    assert data["versicherungsart"] == "car"
    assert data["km_start"] == 12000.0
    registry = er.async_get(hass)
    unique_ids = {e.unique_id for e in er.async_entries_for_config_entry(registry, entry.entry_id)}
    for key in NEW_FIELDS:
        assert f"{entry.entry_id}_{key}" in unique_ids
    states = {
        key: hass.states.get(registry.async_get_entity_id("sensor", DOMAIN, f"{entry.entry_id}_{key}"))
        for key in NEW_FIELDS
    }
    assert states["versicherungsart"].state == "car"
    assert states["kennzeichen"].state == "B-XY 1234"
    assert float(states["km_start"].state) == 12000.0
    assert states["km_pro_jahr"].attributes["unit_of_measurement"] == "km"


async def test_other_contracts_get_no_such_sensors(hass, setup_contract):
    entry, _ = await setup_contract(
        {"sparte": "internet", "anbieter": "Provider", "abschlag": 40.0, "beginn": "2026-01-01",
         "ende": "2026-12-31", "erinnerung_monate": "0"}
    )
    unique_ids = {
        e.unique_id for e in er.async_entries_for_config_entry(er.async_get(hass), entry.entry_id)
    }
    assert not any(uid.endswith(f"_{key}") for uid in unique_ids for key in NEW_FIELDS)


async def test_the_panel_shows_type_and_kilometres_but_not_the_plate(hass, setup_contract):
    entry, _ = await setup_contract(dict(KFZ))
    payload = panel.contract_payload(hass, entry)
    assert payload["versicherungsart"] == "car"
    assert payload["km_start"] == 12000.0
    assert payload["km_pro_jahr"] == 10000.0
    assert "kennzeichen" not in payload
    assert "B-XY 1234" not in json.dumps(payload)


async def test_the_diagnostics_mask_the_plate(hass, setup_contract):
    entry, _ = await setup_contract(dict(KFZ))
    result = await async_get_config_entry_diagnostics(hass, entry)
    assert "B-XY 1234" not in json.dumps(result)
