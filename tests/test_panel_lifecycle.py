"""Creating and deleting contracts from the panel.

Creating runs the integration's own setup flow ("Add entry"), deleting is Home
Assistant's "remove config entry". These tests drive both the way the panel does
and check what the panel then sees.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from homeassistant.config_entries import ConfigEntryState
from homeassistant.data_entry_flow import FlowResultType

from custom_components.tariffy import panel
from custom_components.tariffy.const import DOMAIN

from .test_coordinator import STROM
from .test_panel import GOLDEN, frontend_env  # noqa: F401  (fixture)
from .test_reconfigure import _form_defaults

FIXTURES = json.loads((Path(__file__).parent / "frontend" / "fixtures.json").read_text(encoding="utf-8"))
CREATE = FIXTURES["create"]
TRANSLATIONS = Path(__file__).parent.parent / "custom_components" / "tariffy" / "translations"
PANEL_KINDS = {"date", "text", "number", "select", "entity", "boolean"}  # keep in sync with _fieldSpec()


def _forms():
    yield "user", CREATE["first"]
    for sparte, form in CREATE["steps"].items():
        yield sparte, form


@pytest.mark.parametrize(("name", "form"), list(_forms()), ids=[n for n, _ in _forms()])
def test_every_field_of_the_setup_flow_can_be_drawn_by_the_panel(name, form):
    for field in form["data_schema"]:
        assert next(iter(field["selector"])) in PANEL_KINDS, f"{name}.{field['name']}: extend _fieldSpec()"


@pytest.mark.parametrize("language", ["de", "en"])
def test_every_field_and_option_of_the_setup_flow_has_a_text(language):
    texts = json.loads((TRANSLATIONS / f"{language}.json").read_text(encoding="utf-8"))
    for name, form in _forms():
        labels = texts["config"]["step"][form["step_id"]]["data"]
        for field in form["data_schema"]:
            assert field["name"] in labels, f"{form['step_id']}.{field['name']} has no {language} label"
            select = field["selector"].get("select")
            if select and select.get("translation_key"):
                options = texts["selector"][select["translation_key"]]["options"]
                for value in select["options"]:
                    assert value in options, f"{select['translation_key']}.{value} has no {language} text"


def test_the_panel_knows_which_step_is_the_first():
    # the panel treats every step except "user" as the last one of a new contract
    assert CREATE["first"]["step_id"] == "user"
    assert all(form["step_id"] != "user" for form in CREATE["steps"].values())


async def _create(hass, sparte, first=None, second=None):
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": "user"})
    assert result["step_id"] == "user"
    values = {**_form_defaults(result), "name": "Neuer Vertrag", "sparte": sparte, "anbieter": "Anbieter", **(first or {})}
    result = await hass.config_entries.flow.async_configure(result["flow_id"], values)
    assert result["type"] is FlowResultType.FORM
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {**_form_defaults(result), **(second or {})}
    )
    await hass.async_block_till_done()
    return result


@pytest.mark.parametrize(
    ("sparte", "second"),
    [
        ("electricity", {"arbeitspreis": 0.31, "abschlag": 55.0}),
        ("electricity_ht_nt", {"arbeitspreis": 0.31, "arbeitspreis_nt": 0.2, "abschlag": 55.0}),
        ("gas", {"arbeitspreis": 0.1, "abschlag": 80.0, "brennwert": "11,2"}),
        ("water", {"arbeitspreis": 2.0, "abschlag": 20.0}),
        ("internet", {"abschlag": 39.99}),
    ],
)
async def test_a_contract_created_the_way_the_panel_does_it_shows_up(
    frontend_env, contract, hass, sparte, second  # noqa: F811
):
    await contract.setup(STROM, **GOLDEN)  # an existing contract, and the patched recorder
    result = await _create(hass, sparte, second=second)
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Neuer Vertrag"

    entry = result["result"]
    assert entry.state is ConfigEntryState.LOADED
    assert entry.data["sparte"] == sparte
    assert "name" not in entry.data  # the name is the title, not stored data
    titles = {c["title"]: c for c in panel.async_contracts(hass)}
    assert set(titles) == {"Test", "Neuer Vertrag"}
    assert titles["Neuer Vertrag"]["sparte"] == sparte


async def test_removing_a_contract_takes_it_and_its_open_messages_away(frontend_env, contract, hass):  # noqa: F811
    data = {**STROM, "ende": "2026-09-30", "erinnerung_monate": "3"}
    entry, state = await contract.setup(data, **{**GOLDEN, "today": "2026-07-01"})
    assert state["erinnerung_aktiv"] is True
    ids = [key for key in hass.data["persistent_notification"] if entry.entry_id in key]
    assert any(key.startswith("tariffy_kuendigung_") for key in ids)

    other = (await _create(hass, "internet", second={"abschlag": 39.99}))["result"]

    await hass.config_entries.async_remove(entry.entry_id)
    await hass.async_block_till_done()
    assert not [key for key in hass.data["persistent_notification"] if entry.entry_id in key]
    assert hass.config_entries.async_get_entry(entry.entry_id) is None
    assert [c["entry_id"] for c in panel.async_contracts(hass)] == [other.entry_id]


async def test_removing_the_last_contract_removes_the_panel(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await contract.setup(STROM, **GOLDEN)
    assert "tariffy" in hass.data["frontend_panels"]
    await hass.config_entries.async_remove(entry.entry_id)
    await hass.async_block_till_done()
    assert "tariffy" not in hass.data["frontend_panels"]
