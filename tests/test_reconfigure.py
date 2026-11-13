"""Reconfiguring a contract must not lose what the coordinator stored itself.

Home Assistant replaces `entry.data` with what the reconfigure forms return. The
forms do not contain the coordinator's own state (acknowledged reminders, "push
sent" markers, the consumption of the last contract term), so the flow hands it
back. These tests drive the real flow the way a form submission does.
"""

from __future__ import annotations

import pytest
from homeassistant.data_entry_flow import FlowResultType

from .test_coordinator import STROM
from .test_panel import GOLDEN, frontend_env  # noqa: F401  (fixture)

INTERNAL = {
    "_kuendigung_bestaetigt": True,
    "_notify_gesendet": True,
    "verbrauch_letzte_laufzeit": 1481.17,
    "verbrauch_letzte_laufzeit_monate": 12.0,
}
REMINDER = {"_kuendigung_bestaetigt", "_notify_gesendet"}
# The low-instalment markers are handed back by the flow as well, but the coordinator
# manages them itself (it clears them while no warning is active), so they are not
# asserted here.


def _form_defaults(form) -> dict:
    """What a form sends when the user changes nothing: defaults and stored values."""
    values = {}
    for key in form["data_schema"].schema:
        if key.default is not vol_UNDEFINED:
            values[str(key)] = key.default()
        elif key.description and "suggested_value" in key.description:
            values[str(key)] = key.description["suggested_value"]
    return values


from voluptuous.schema_builder import UNDEFINED as vol_UNDEFINED  # noqa: E402


async def _reconfigure(hass, entry, first=None, second=None, drop=()):
    result = await hass.config_entries.flow.async_init(
        "tariffy", context={"source": "reconfigure", "entry_id": entry.entry_id}
    )
    assert result["step_id"] == "reconfigure"
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {**_form_defaults(result), **(first or {})}
    )
    assert result["type"] is FlowResultType.FORM
    values = {**_form_defaults(result), **(second or {})}
    for name in drop:  # a field the user emptied: the panel leaves it out
        values.pop(name, None)
    result = await hass.config_entries.flow.async_configure(result["flow_id"], values)
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reconfigure_successful"
    await hass.async_block_till_done()
    return entry.data


async def _contract(contract, **extra):
    data = {**STROM, "ende": "2026-12-31", "erinnerung_monate": "3", **INTERNAL, **extra}
    return await contract.setup(data, **GOLDEN)


async def test_nothing_is_lost_when_the_form_is_saved_unchanged(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await _contract(contract)
    data = await _reconfigure(hass, entry)
    for key, value in INTERNAL.items():
        assert data[key] == value, key
    assert data["anbieter"] == "Stadtwerke"
    assert data["ende"] == "2026-12-31"


async def test_the_form_offers_the_name_first_with_the_current_one(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await _contract(contract)
    result = await hass.config_entries.flow.async_init(
        "tariffy", context={"source": "reconfigure", "entry_id": entry.entry_id}
    )
    first = next(iter(result["data_schema"].schema))
    assert str(first) == "name" and first.default() == "Test"


@pytest.mark.parametrize("sparte", ["electricity", "gas", "internet", "insurance"])
async def test_the_name_can_be_changed(frontend_env, contract, hass, sparte):  # noqa: F811
    from homeassistant.helpers import device_registry as dr, entity_registry as er

    entry, _ = await _contract(contract, sparte=sparte)
    entities_before = {e.entity_id for e in er.async_entries_for_config_entry(er.async_get(hass), entry.entry_id)}
    extra = {"brennwert": "11.2", "zustandszahl": "0.95"} if sparte == "gas" else {}
    data = await _reconfigure(hass, entry, first={"name": "  Autoversicherung  "}, second=extra)
    assert entry.title == "Autoversicherung"  # trimmed
    assert "name" not in data  # the name is the title, not a contract value
    assert data["anbieter"] == "Stadtwerke"
    device = dr.async_get(hass).async_get_device(identifiers={("tariffy", entry.entry_id)})
    assert device is not None and device.name == "Autoversicherung"
    entities_after = {e.entity_id for e in er.async_entries_for_config_entry(er.async_get(hass), entry.entry_id)}
    assert entities_after == entities_before  # entity ids stay as they are


async def test_an_empty_name_keeps_the_old_one(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await _contract(contract)
    await _reconfigure(hass, entry, first={"name": "   "})
    assert entry.title == "Test"


async def test_edited_fields_are_stored_and_internal_state_stays(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await _contract(contract)
    data = await _reconfigure(hass, entry, first={"tarif": "Neu"}, second={"arbeitspreis": 0.31})
    assert data["tarif"] == "Neu"
    assert data["arbeitspreis"] == 0.31
    assert data["verbrauch_letzte_laufzeit"] == 1481.17
    assert data["_kuendigung_bestaetigt"] is True


async def test_history_and_archive_flag_survive_a_reconfiguration(frontend_env, contract, hass):  # noqa: F811
    history = [{"anbieter": "Alt", "beginn": "2025-01-01", "ende": "2025-12-31", "kosten": 480.0}]
    entry, _ = await _contract(contract, _historie=history, _archiviert="2026-05-01")
    data = await _reconfigure(hass, entry, first={"tarif": "Neu"})
    assert data["tarif"] == "Neu"
    assert data["_historie"] == history
    assert data["_archiviert"] == "2026-05-01"


@pytest.mark.parametrize(
    ("first", "what"),
    [({"ende": "2027-03-31"}, "end date"), ({"erinnerung_monate": "1"}, "lead time")],
)
async def test_the_reminder_starts_over_when_its_basis_changes(frontend_env, contract, hass, first, what):  # noqa: F811
    entry, _ = await _contract(contract)
    data = await _reconfigure(hass, entry, first=first)
    assert not (REMINDER & set(data)), f"reminder state must be reset when the {what} changes"
    # everything else that belongs to the contract is kept
    assert data["verbrauch_letzte_laufzeit"] == 1481.17


async def test_an_instalment_change_is_still_stamped(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await _contract(contract)
    data = await _reconfigure(hass, entry, second={"abschlag": 100.0})
    assert data["abschlag"] == 100.0
    assert data["_abschlag_vorheriger_wert"] == 40.0
    assert data["_abschlag_ab_datum"] == "2026-07-12"
    assert data["_kuendigung_bestaetigt"] is True


async def test_a_cleared_optional_field_is_removed(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await _contract(contract, kundennummer="K-1")
    result = await hass.config_entries.flow.async_init(
        "tariffy", context={"source": "reconfigure", "entry_id": entry.entry_id}
    )
    values = _form_defaults(result)
    values.pop("kundennummer")  # the form leaves a cleared optional field out
    result = await hass.config_entries.flow.async_configure(result["flow_id"], values)
    result = await hass.config_entries.flow.async_configure(result["flow_id"], _form_defaults(result))
    assert result["reason"] == "reconfigure_successful"
    await hass.async_block_till_done()
    assert "kundennummer" not in entry.data
