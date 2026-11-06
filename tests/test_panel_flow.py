"""The panel's "plan the next contract" form is the options flow of the integration.

The panel renders the form Home Assistant serialises for its REST API and sends back
only the filled fields. These tests pin that contract from the backend side: every
field type the real forms use is one the panel can draw, every field has a label, and
what the panel sends is accepted (and stored) by the real flow.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from homeassistant.data_entry_flow import FlowResultType

from .test_coordinator import STROM
from .test_panel import GOLDEN, frontend_env  # noqa: F401  (fixture)

FIXTURES = json.loads((Path(__file__).parent / "frontend" / "fixtures.json").read_text(encoding="utf-8"))
FORMS = FIXTURES["flows"]
TRANSLATIONS = Path(__file__).parent.parent / "custom_components" / "tariffy" / "translations"
PANEL_KINDS = {"date", "text", "number", "select", "entity", "boolean"}  # keep in sync with _fieldSpec()
RECONFIGURE = FIXTURES["reconfigure"]


def _kind(field: dict) -> str:
    return next(iter(field["selector"]))


@pytest.mark.parametrize("contract_id", sorted(FORMS))
def test_every_field_can_be_drawn_by_the_panel(contract_id):
    kinds = {_kind(field) for field in FORMS[contract_id]["data_schema"]}
    assert kinds <= PANEL_KINDS, f"the panel cannot draw {kinds - PANEL_KINDS}, extend _fieldSpec()"


@pytest.mark.parametrize("language", ["de", "en"])
def test_every_field_has_a_label_and_every_error_a_text(language):
    texts = json.loads((TRANSLATIONS / f"{language}.json").read_text(encoding="utf-8"))["options"]
    labels = texts["step"]["init"]["data"]
    for form in FORMS.values():
        for field in form["data_schema"]:
            assert field["name"] in labels, f"{field['name']} has no {language} label"
    assert "invalid_number" in texts["error"]
    assert texts["step"]["init"]["description"]


@pytest.mark.parametrize("contract_id", sorted(RECONFIGURE))
def test_every_reconfigure_field_can_be_drawn_by_the_panel(contract_id):
    for step in RECONFIGURE[contract_id].values():
        for field in step["data_schema"]:
            assert _kind(field) in PANEL_KINDS, f"{field['name']}: extend _fieldSpec()"


@pytest.mark.parametrize("language", ["de", "en"])
def test_every_reconfigure_field_and_option_has_a_text(language):
    texts = json.loads((TRANSLATIONS / f"{language}.json").read_text(encoding="utf-8"))
    for contract_id, steps in RECONFIGURE.items():
        for step in steps.values():
            labels = texts["config"]["step"][step["step_id"]]["data"]
            for field in step["data_schema"]:
                assert field["name"] in labels, f"{step['step_id']}.{field['name']} has no {language} label"
                select = field["selector"].get("select")
                if select and select.get("translation_key"):
                    options = texts["selector"][select["translation_key"]]["options"]
                    for value in select["options"]:
                        assert value in options, f"{select['translation_key']}.{value} has no {language} text"
    assert "invalid_number" in texts["config"]["error"]
    assert "reconfigure_successful" in texts["config"]["abort"]


def test_the_first_step_comes_before_the_data_of_the_sparte():
    # the panel treats every reconfigure step except "reconfigure" as the last one (it asks before saving)
    for steps in RECONFIGURE.values():
        assert steps["first"]["step_id"] == "reconfigure"
        assert steps["second"]["step_id"].startswith("reconfigure_")


def _panel_values(form: dict, **filled) -> dict:
    """What the panel sends: only the fields that were filled in."""
    names = {field["name"] for field in form["data_schema"]}
    assert set(filled) <= names, f"not in the form: {set(filled) - names}"
    return filled


async def _run(hass, entry, values):
    result = await hass.config_entries.options.async_init(entry.entry_id)
    assert result["type"] is FlowResultType.FORM
    return await hass.config_entries.options.async_configure(result["flow_id"], values)


class TestFlowAcceptsWhatThePanelSends:
    async def test_filled_fields_are_stored(self, frontend_env, contract, hass):  # noqa: F811
        entry, _ = await contract.setup(STROM, **GOLDEN)
        values = _panel_values(
            FORMS["contract-1"], next_beginn="2027-01-01", next_anbieter="Neuer Anbieter",
            next_abschlag=44.98, next_arbeitspreis=0.31,
        )
        result = await _run(hass, entry, values)
        assert result["type"] is FlowResultType.CREATE_ENTRY
        await hass.async_block_till_done()
        assert entry.options == values

    async def test_gas_with_decimal_comma_text(self, frontend_env, contract, hass):  # noqa: F811
        gas = {**STROM, "sparte": "gas", "gas_einheit": "m³", "brennwert": "11.2", "zustandszahl": "0.95"}
        entry, _ = await contract.setup(gas, **GOLDEN)
        values = _panel_values(
            FORMS["contract-2"], next_beginn="2027-01-01", next_gas_einheit="m³", next_brennwert="11,2",
        )
        result = await _run(hass, entry, values)
        assert result["type"] is FlowResultType.CREATE_ENTRY

    async def test_an_invalid_text_number_comes_back_as_a_form_error(self, frontend_env, contract, hass):  # noqa: F811
        gas = {**STROM, "sparte": "gas", "gas_einheit": "m³", "brennwert": "11.2", "zustandszahl": "0.95"}
        entry, _ = await contract.setup(gas, **GOLDEN)
        result = await _run(hass, entry, {"next_beginn": "2027-01-01", "next_brennwert": "abc"})
        assert result["type"] is FlowResultType.FORM
        assert result["errors"] == {"next_brennwert": "invalid_number"}

    async def test_an_empty_form_removes_the_planned_contract(self, frontend_env, contract, hass):  # noqa: F811
        planned = {"next_beginn": "2027-01-01", "next_anbieter": "Neuer Anbieter"}
        entry, _ = await contract.setup(STROM, **GOLDEN, options=planned)
        result = await _run(hass, entry, {})
        assert result["type"] is FlowResultType.CREATE_ENTRY
        await hass.async_block_till_done()
        assert entry.options == {}
        assert entry.data["anbieter"] == "Stadtwerke"  # the current contract is untouched

    async def test_the_form_offers_the_stored_plan_as_suggested_values(self, frontend_env, contract, hass):  # noqa: F811
        planned = {"next_beginn": "2027-01-01", "next_anbieter": "Neuer Anbieter"}
        entry, _ = await contract.setup(STROM, **GOLDEN, options=planned)
        result = await hass.config_entries.options.async_init(entry.entry_id)
        suggested = {
            str(key): key.description["suggested_value"]
            for key in result["data_schema"].schema
            if key.description and "suggested_value" in key.description
        }
        assert suggested == planned


class TestCancellationAfterSaving:
    CANCEL = {**STROM, "ende": "2026-09-30", "erinnerung_monate": "3"}

    async def test_the_contract_is_loaded_again_and_the_cancellation_can_be_acknowledged(
        self, frontend_env, contract, hass, hass_ws_client  # noqa: F811
    ):
        client = await hass_ws_client()  # connect before the test clock moves
        entry, data = await contract.setup(self.CANCEL, **{**GOLDEN, "today": "2026-07-01"})
        assert data["erinnerung_aktiv"] is True

        result = await _run(hass, entry, {"next_beginn": "2027-01-01", "next_anbieter": "Neuer Anbieter"})
        assert result["type"] is FlowResultType.CREATE_ENTRY
        await hass.async_block_till_done()
        assert entry.options["next_anbieter"] == "Neuer Anbieter"

        # this is what the panel does after the save, once the contract has reloaded
        await client.send_json_auto_id(
            {"type": "tariffy/action", "entry_id": entry.entry_id, "action": "confirm_cancellation"}
        )
        reply = await client.receive_json()
        assert reply["success"] is True
        await hass.async_block_till_done()
        assert entry.data["_kuendigung_bestaetigt"] is True
        assert entry.options["next_anbieter"] == "Neuer Anbieter"  # the plan is still there
