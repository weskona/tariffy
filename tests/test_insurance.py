"""Insurance contracts: type, licence plate and odometer figures (issue #57)."""

from __future__ import annotations

import json

import pytest
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.helpers import entity_registry as er

from custom_components.tariffy import panel
from custom_components.tariffy.const import DOMAIN
from custom_components.tariffy.diagnostics import async_get_config_entry_diagnostics

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


async def _pauschal_form(hass, sparte):
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": "user"})
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"name": "Vertrag", "sparte": sparte, "anbieter": "Anbieter", "erinnerung_monate": "0"},
    )
    assert result["step_id"] == "pauschal"
    return result


async def test_the_insurance_form_asks_for_the_extra_fields(hass):
    result = await _pauschal_form(hass, "insurance")
    keys = {str(k) for k in result["data_schema"].schema}
    assert NEW_FIELDS <= keys


@pytest.mark.parametrize("sparte", ["internet", "mobile", "other"])
async def test_other_flat_rate_forms_do_not(hass, sparte):
    result = await _pauschal_form(hass, sparte)
    keys = {str(k) for k in result["data_schema"].schema}
    assert not NEW_FIELDS & keys


async def test_the_values_are_stored(hass):
    result = await _pauschal_form(hass, "insurance")
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            "abschlag": 45.0,
            "versicherungsart": "car",
            "kennzeichen": "B-XY 1234",
            "km_start": 12000,
            "km_pro_jahr": 10000,
        },
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"]["versicherungsart"] == "car"
    assert result["data"]["kennzeichen"] == "B-XY 1234"
    assert result["data"]["km_pro_jahr"] == 10000


async def test_the_fields_are_optional(hass):
    result = await _pauschal_form(hass, "insurance")
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"abschlag": 20.0})
    assert result["type"] is FlowResultType.CREATE_ENTRY


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
