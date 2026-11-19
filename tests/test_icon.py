"""Eigenes Icon pro Vertrag (Issue 93): Formular, Sensoren, Panel-Daten, Tarifwechsel, Sicherung."""

from __future__ import annotations

import json
from pathlib import Path

from homeassistant.data_entry_flow import FlowResultType

from custom_components.tariffy import backup, panel
from custom_components.tariffy.const import DOMAIN

from .test_panel import GOLDEN, frontend_env  # noqa: F401  (fixture)
from .test_reconfigure import _reconfigure

TRANSLATIONS = Path(__file__).parent.parent / "custom_components" / "tariffy" / "translations"
INTERNET = {
    "sparte": "internet", "anbieter": "Glasfaser", "abschlag": 40.0, "beginn": "2026-01-01",
    "ende": "2026-12-31", "erinnerung_monate": "0", "icon": "mdi:router-wireless",
}
STROM = {
    "sparte": "electricity", "anbieter": "Werke", "arbeitspreis": 0.3, "grundpreis": 10.0, "abschlag": 90.0,
    "beginn": "2026-01-01", "ende": "2026-12-31", "erinnerung_monate": "0", "icon": "mdi:home-lightning-bolt",
    "verbrauch_sensor": "sensor.strom",
}


async def test_the_first_step_offers_the_icon_in_both_languages(hass):
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": "user"})
    assert "icon" in {str(k) for k in result["data_schema"].schema}
    for language in ("en", "de"):
        texts = json.loads((TRANSLATIONS / f"{language}.json").read_text(encoding="utf-8"))["config"]["step"]
        for step in ("user", "reconfigure"):
            assert texts[step]["data"]["icon"] and texts[step]["data_description"]["icon"], (language, step)


async def test_a_contract_is_created_with_its_icon(hass):
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": "user"})
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"name": "Internet", "sparte": "internet", "anbieter": "Glasfaser", "erinnerung_monate": "0", "icon": "mdi:router-wireless"},
    )
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"zahlweise": "monthly", "abschlag": 40.0})
    assert result["type"] is FlowResultType.CREATE_ENTRY and result["data"]["icon"] == "mdi:router-wireless"


async def test_without_an_icon_nothing_changes(hass):
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": "user"})
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {"name": "Internet", "sparte": "internet", "anbieter": "Glasfaser", "erinnerung_monate": "0"}
    )
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {"zahlweise": "monthly", "abschlag": 40.0})
    assert "icon" not in result["data"]


async def test_the_panel_gets_the_icon(frontend_env, contract, hass):  # noqa: F811
    entry, d = await contract.setup(INTERNET, **GOLDEN)
    assert d["icon"] == "mdi:router-wireless"
    assert panel.contract_payload(hass, entry)["icon"] == "mdi:router-wireless"
    entry2, d2 = await contract.setup({k: v for k, v in INTERNET.items() if k != "icon"}, **GOLDEN)
    assert d2["icon"] is None and panel.contract_payload(hass, entry2)["icon"] is None


async def test_the_sensors_of_the_contract_use_the_icon_but_status_icons_stay(contract, hass):
    await contract.setup(STROM, **GOLDEN)
    states = [hass.states.get(e) for e in hass.states.async_entity_ids("sensor")]
    icons = {s.entity_id: s.attributes.get("icon") for s in states}
    custom = [e for e, i in icons.items() if i == "mdi:home-lightning-bolt"]
    assert custom, icons  # the figures of the contract
    # the balance sensors show a thumb up or down; the price sensor its own symbol: they keep theirs
    balance = [i for e, i in icons.items() if "refund" in e or "balance" in e]
    assert balance and all(i and i.startswith("mdi:thumb") for i in balance), balance


async def test_without_an_icon_the_sensors_keep_their_icons(contract, hass):
    await contract.setup({k: v for k, v in STROM.items() if k != "icon"}, **GOLDEN)
    icons = {hass.states.get(e).attributes.get("icon") for e in hass.states.async_entity_ids("sensor")}
    assert "mdi:home-lightning-bolt" not in icons and "mdi:currency-eur" in icons  # their own icons, as before


async def test_editing_keeps_the_icon_and_clearing_removes_it(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await contract.setup(INTERNET, **GOLDEN)
    assert (await _reconfigure(hass, entry))["icon"] == "mdi:router-wireless"
    assert (await _reconfigure(hass, entry, first={"icon": "mdi:wifi"}))["icon"] == "mdi:wifi"
    assert "icon" not in await _reconfigure(hass, entry, drop_first=("icon",))


async def test_a_tariff_switch_keeps_the_icon(contract):
    options = {"next_beginn": "2026-07-01", "next_ende": "2027-06-30", "next_anbieter": "Neu", "next_abschlag": 35.0}
    entry, _ = await contract.setup(INTERNET, options=options, **GOLDEN)
    assert entry.data["anbieter"] == "Neu" and entry.data["icon"] == "mdi:router-wireless"


def test_the_icon_survives_a_backup():
    assert backup.sanitize_contract({"title": "Internet", "data": INTERNET})["data"]["icon"] == "mdi:router-wireless"
