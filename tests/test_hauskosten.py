"""House costs (issue 121): waste fees, street cleaning, rainwater, ... as a flat-rate contract with a type."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
from homeassistant.data_entry_flow import FlowResultType

from custom_components.tariffy import backup
from custom_components.tariffy.const import (
    BASIS_FELDER,
    DOMAIN,
    HAUSKOSTENARTEN,
    METERED_SPARTEN,
    SPARTEN,
)

from .test_panel import GOLDEN, frontend_env  # noqa: F401  (fixture)
from .test_reconfigure import _form_defaults

ROOT = Path(__file__).parent.parent / "custom_components" / "tariffy"
HAUS = {
    "sparte": "hauskosten",
    "hauskostenart": "waste",
    "anbieter": "Stadt Musterstadt",
    "tarif": "Restmüll und Biotonne",
    "abschlag": 31.0,
    "zahlweise": "quarterly",
    "beginn": "2026-01-01",
    "erinnerung_monate": "0",
}


async def _start(hass):
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": "user"})
    return await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"name": "Abfall", "sparte": "hauskosten", "anbieter": "Stadt", "erinnerung_monate": "0"},
    )


def _keys(result):
    return {str(k) for k in result["data_schema"].schema}


def _texts(language):
    return json.loads((ROOT / "translations" / f"{language}.json").read_text(encoding="utf-8"))


def test_house_costs_are_a_flat_rate_category_in_the_list():
    assert "hauskosten" in SPARTEN
    assert "hauskosten" not in METERED_SPARTEN  # no consumption: it counts like any flat-rate contract
    assert "hauskostenart" in BASIS_FELDER  # a tariff switch keeps the type


async def test_house_costs_ask_for_the_type_first_and_then_for_the_costs(hass):
    result = await _start(hass)
    assert result["step_id"] == "hauskosten"
    assert _keys(result) == {"hauskostenart"}
    assert result["last_step"] is False  # the costs follow
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"hauskostenart": "waste"})
    assert result["step_id"] == "pauschal"
    assert "hauskostenart" not in _keys(result)
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"abschlag": 31.0})
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"]["hauskostenart"] == "waste"
    assert result["data"]["sparte"] == "hauskosten"


@pytest.mark.parametrize("art", HAUSKOSTENARTEN)
async def test_every_listed_type_is_accepted(hass, art):
    result = await _start(hass)
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"hauskostenart": art})
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"abschlag": 10.0})
    assert result["data"]["hauskostenart"] == art


async def test_a_type_can_also_be_typed_freely(hass):
    result = await _start(hass)
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"hauskostenart": "Gartenabfall"})
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"abschlag": 8.0})
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"]["hauskostenart"] == "Gartenabfall"


async def test_the_type_is_optional(hass):
    result = await _start(hass)
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {})
    assert result["step_id"] == "pauschal"
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"abschlag": 10.0})
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert "hauskostenart" not in result["data"]


def test_the_texts_of_the_steps_and_the_list_exist_in_both_languages():
    for language in ("en", "de"):
        texts = _texts(language)
        for step in ("hauskosten", "reconfigure_hauskosten"):
            node = texts["config"]["step"][step]
            assert node["title"] and node["description"], (language, step)
            assert node["data"]["hauskostenart"] and node["data_description"]["hauskostenart"], (language, step)
        options = texts["selector"]["hauskostenart"]["options"]
        assert set(options) == set(HAUSKOSTENARTEN), language
        assert all(options.values()), language
        assert texts["selector"]["sparte"]["options"]["hauskosten"], language
    strings = json.loads((ROOT / "strings.json").read_text(encoding="utf-8"))
    assert strings["selector"]["hauskostenart"] == _texts("en")["selector"]["hauskostenart"]


def test_the_panel_names_every_listed_type_in_both_languages():
    source = (ROOT / "frontend" / "tariffy-i18n.js").read_text(encoding="utf-8")
    blocks = re.findall(r"hauskostenart: \{(.*?)\n    \},", source, flags=re.S)
    assert len(blocks) == 2  # English and German
    for block in blocks:
        assert set(re.findall(r"(\w+): \"", block)) == set(HAUSKOSTENARTEN)
    assert source.count(" hauskosten: \"") == 2  # the category name in both languages


async def test_house_costs_count_like_a_flat_rate_contract(frontend_env, contract, hass):  # noqa: F811
    entry, data = await contract.setup(dict(HAUS), **GOLDEN)
    assert data["hauskostenart"] == "waste"
    assert data["abschlag"] == 31.0 and data["abschlag_jahr"] == 372.0
    assert data["abschlag_bisher_gezahlt"] == 279.0  # three quarterly debits of 93 euro by 12 July
    assert data["verlaengerbar"] is True  # house costs can be renewed like any flat-rate contract
    assert data["prognose_real"] is None  # nothing is measured


async def test_the_type_reaches_the_panel_and_survives_a_backup(frontend_env, contract, hass):  # noqa: F811
    from custom_components.tariffy import panel

    entry, _ = await contract.setup(dict(HAUS), **GOLDEN)
    payload = panel.contract_payload(hass, entry)
    assert payload["hauskostenart"] == "waste" and payload["sparte"] == "hauskosten"
    clean = backup.sanitize_contract({"title": entry.title, "data": dict(entry.data), "options": {}})
    assert clean["data"]["hauskostenart"] == "waste"


async def test_the_type_can_be_changed_when_the_contract_is_edited(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await contract.setup(dict(HAUS), **GOLDEN)
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "reconfigure", "entry_id": entry.entry_id}
    )
    result = await hass.config_entries.flow.async_configure(result["flow_id"], _form_defaults(result))
    assert result["step_id"] == "reconfigure_hauskosten"
    assert _form_defaults(result)["hauskostenart"] == "waste"  # the form shows the stored type
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"hauskostenart": "street_cleaning"})
    result = await hass.config_entries.flow.async_configure(result["flow_id"], _form_defaults(result))
    assert result["type"] is FlowResultType.ABORT
    await hass.async_block_till_done()
    assert entry.data["hauskostenart"] == "street_cleaning"
    assert entry.data["abschlag"] == 31.0 and entry.data["zahlweise"] == "quarterly"  # the rest is kept
