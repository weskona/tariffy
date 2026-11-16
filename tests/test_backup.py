"""Sicherung und Wiederherstellung: Export, Import aus Datei, geloeschte Vertraege."""

from __future__ import annotations

import copy
import json
from datetime import timedelta
from unittest.mock import patch

import pytest
from homeassistant.config_entries import ConfigEntryState
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.tariffy import backup
from custom_components.tariffy.const import DOMAIN

from .test_coordinator import STROM
from .test_panel import GOLDEN, frontend_env  # noqa: F401  (fixture)
from .test_panel_fixtures import CONTRACTS

COORDINATOR = "custom_components.tariffy.coordinator"
NEXT = {"next_beginn": "2027-01-01", "next_ende": "2027-12-31", "next_anbieter": "Neu", "next_abschlag": 55.0}
RICH = {
    **STROM,
    "kundennummer": "K-123",
    "zaehlernummer": "Z-456",
    "notify_target": "mobile_app_pixel",
    "_historie": [{"anbieter": "Alt", "beginn": "2024-01-01", "ende": "2024-12-31", "kosten": 480.0, "eigene": ["kosten"]}],
    "_archiviert": "2027-02-01",
    "_kuendigung_bestaetigt": True,
}


@pytest.fixture(autouse=True)
def _statistics():
    """The contracts of these tests need no recorder."""
    async def none(*_args, **_kwargs):
        return (None, None)

    async def nothing(*_args, **_kwargs):
        return None

    with (
        patch(f"{COORDINATOR}._get_latest_sum", none),
        patch(f"{COORDINATOR}._get_historic_value", none),
        patch(f"{COORDINATOR}._get_average_price", nothing),
    ):
        yield


async def _add(hass, title, data, options=None):
    entry = MockConfigEntry(domain=DOMAIN, title=title, data=data, options=options or {})
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    return entry


def _entries(hass):
    return {entry.title: entry for entry in hass.config_entries.async_entries(DOMAIN)}


async def _call(client, type_, **extra):
    await client.send_json_auto_id({"type": f"tariffy/{type_}", **extra})
    return await client.receive_json()


class TestFormat:
    def test_every_key_of_the_preview_contracts_survives_a_round_trip(self):
        """The whitelist knows every key a real contract has (the preview data come from the backend)."""
        for title, data, _sensors, options in CONTRACTS:
            clean = backup.sanitize_contract({"title": title, "data": data, "options": options})
            assert clean == {"title": title, "data": data, "options": options}, title

    def test_unknown_keys_are_dropped_and_known_ones_kept(self):
        clean = backup.sanitize_contract(
            {"title": " Strom ", "data": {**RICH, "evil": "x", "__class__": 1}, "options": {**NEXT, "other": 1}}
        )
        assert clean["title"] == "Strom"
        assert "evil" not in clean["data"] and "__class__" not in clean["data"]
        assert clean["data"]["kundennummer"] == "K-123" and clean["data"]["_historie"] == RICH["_historie"]
        assert clean["options"] == NEXT

    @pytest.mark.parametrize(
        "raw",
        [
            None,
            [],
            {"tariffy_backup": 2, "contracts": []},  # unknown format
            {"tariffy_backup": 1},  # no contracts
            {"tariffy_backup": 1, "contracts": "x"},
            {"tariffy_backup": 1, "contracts": [{"title": "", "data": STROM}]},  # no name
            {"tariffy_backup": 1, "contracts": [{"title": "A", "data": {"sparte": "rocket"}}]},  # unknown kind
            {"tariffy_backup": 1, "contracts": [{"title": "A", "data": "x"}]},
            {"tariffy_backup": 1, "contracts": [{"title": "A", "data": {**STROM, "tarif": {"a": {"b": {"c": {"d": 1}}}}}}]},  # too deep
            {"tariffy_backup": 1, "contracts": [{"title": "A", "data": {**STROM, "tarif": object()}}]},  # not JSON
            {"tariffy_backup": 1, "contracts": [{"title": "A", "data": {**STROM, "abschlag": float("inf")}}]},
            {"tariffy_backup": 1, "contracts": [{"title": "A", "data": {**STROM, "tarif": "x" * 5000}}]},
            {"tariffy_backup": 1, "contracts": [{"title": "A", "data": STROM}] * 201},  # too many
        ],
    )
    def test_unusable_files_are_refused(self, raw):
        with pytest.raises(backup.BackupError) as err:
            backup.sanitize_backup(raw)
        assert err.value.code == "invalid_backup"


class TestExportAndRestore:
    async def test_the_backup_has_everything(self, frontend_env, hass, hass_ws_client):  # noqa: F811
        client = await hass_ws_client()
        await _add(hass, "Strom Haus", RICH, NEXT)
        await _add(hass, "Wasser", {**STROM, "sparte": "water"})
        reply = await _call(client, "backup_export")
        assert reply["success"] is True
        data = reply["result"]["backup"]
        assert data["tariffy_backup"] == 1 and data["version"] and data["created"]
        by_title = {c["title"]: c for c in data["contracts"]}
        assert set(by_title) == {"Strom Haus", "Wasser"}
        assert by_title["Strom Haus"]["data"] == RICH  # personal data, history, flags: all of it
        assert by_title["Strom Haus"]["options"] == NEXT
        json.dumps(data)  # can be written to a file
        assert backup.sanitize_backup(data)  # and read back

    async def test_restoring_creates_what_is_missing_and_leaves_the_rest_alone(
        self, frontend_env, hass, hass_ws_client  # noqa: F811
    ):
        client = await hass_ws_client()
        strom = await _add(hass, "Strom Haus", RICH, NEXT)
        await _add(hass, "Wasser", {**STROM, "sparte": "water", "abschlag": 28.0})
        saved = (await _call(client, "backup_export"))["result"]["backup"]

        # a contract is lost, another one was changed since the backup
        wasser = _entries(hass)["Wasser"]
        await hass.config_entries.async_remove(wasser.entry_id)
        hass.config_entries.async_update_entry(strom, data={**strom.data, "abschlag": 99.0})
        await hass.async_block_till_done()

        reply = await _call(client, "backup_preview", backup=saved)
        assert reply["result"]["contracts"] == [
            {"title": "Strom Haus", "sparte": "electricity", "action": "skip"},
            {"title": "Wasser", "sparte": "water", "action": "create"},
        ]
        assert "Wasser" not in _entries(hass)  # a preview creates nothing

        reply = await _call(client, "backup_restore", backup=saved)
        assert reply["result"] == {"created": ["Wasser"], "skipped": ["Strom Haus"]}
        await hass.async_block_till_done()
        entries = _entries(hass)
        assert entries["Wasser"].data["abschlag"] == 28.0
        assert entries["Wasser"].state is ConfigEntryState.LOADED
        assert entries["Strom Haus"].data["abschlag"] == 99.0  # never touched
        assert entries["Strom Haus"].entry_id == strom.entry_id

        again = await _call(client, "backup_restore", backup=saved)
        assert again["result"] == {"created": [], "skipped": ["Strom Haus", "Wasser"]}
        assert len(hass.config_entries.async_entries(DOMAIN)) == 2

    async def test_a_restored_contract_is_the_same_contract(self, frontend_env, hass, hass_ws_client):  # noqa: F811
        client = await hass_ws_client()
        original = await _add(hass, "Strom Haus", RICH, NEXT)
        saved = (await _call(client, "backup_export"))["result"]["backup"]
        await hass.config_entries.async_remove(original.entry_id)
        await hass.async_block_till_done()
        await _call(client, "backup_restore", backup=saved)
        await hass.async_block_till_done()
        restored = _entries(hass)["Strom Haus"]
        assert dict(restored.data) == RICH
        assert dict(restored.options) == NEXT
        assert restored.entry_id != original.entry_id  # a new entry, nothing is shared

    async def test_the_same_contract_twice_in_a_file_is_created_once(self, frontend_env, hass, hass_ws_client):  # noqa: F811
        client = await hass_ws_client()
        await _add(hass, "Wasser", {**STROM, "sparte": "water"})  # the panel exists once there is a contract
        contract = {"title": "Strom", "data": STROM, "options": {}}
        file = {"tariffy_backup": 1, "contracts": [contract, copy.deepcopy(contract)]}
        reply = await _call(client, "backup_restore", backup=file)
        assert reply["result"] == {"created": ["Strom"], "skipped": ["Strom"]}

    async def test_a_broken_file_changes_nothing(self, frontend_env, hass, hass_ws_client):  # noqa: F811
        client = await hass_ws_client()
        await _add(hass, "Strom Haus", STROM)
        good = {"title": "Neu", "data": STROM, "options": {}}
        broken = {"title": "Kaputt", "data": {"sparte": "rocket"}}
        for type_ in ("backup_preview", "backup_restore"):
            reply = await _call(client, type_, backup={"tariffy_backup": 1, "contracts": [good, broken]})
            assert reply["error"]["code"] == "invalid_backup"
        assert set(_entries(hass)) == {"Strom Haus"}  # nothing of the file was created

    async def test_only_administrators(
        self, frontend_env, hass, hass_ws_client, hass_read_only_access_token  # noqa: F811
    ):
        client = await hass_ws_client(hass, hass_read_only_access_token)
        await _add(hass, "Strom Haus", STROM)
        file = {"tariffy_backup": 1, "contracts": [{"title": "Neu", "data": STROM}]}
        for type_, extra in (
            ("backup_export", {}),
            ("backup_preview", {"backup": file}),
            ("backup_restore", {"backup": file}),
            ("deleted_list", {}),
            ("deleted_restore", {"item_id": "x"}),
            ("deleted_discard", {"item_id": "x"}),
        ):
            reply = await _call(client, type_, **extra)
            assert reply["error"]["code"] == "unauthorized", type_
        assert set(_entries(hass)) == {"Strom Haus"}

    async def test_the_import_step_refuses_bad_data_itself(self, hass):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": "import"}, data={"title": "X", "data": {"sparte": "rocket"}}
        )
        assert result["type"] == "abort" and result["reason"] == "invalid_backup"
        assert not hass.config_entries.async_entries(DOMAIN)


class TestDeletedContracts:
    async def test_a_deleted_contract_can_be_brought_back(self, frontend_env, hass, hass_ws_client):  # noqa: F811
        client = await hass_ws_client()
        entry = await _add(hass, "Strom Haus", RICH, NEXT)
        assert (await _call(client, "deleted_list"))["result"]["deleted"] == []

        await hass.config_entries.async_remove(entry.entry_id)
        await hass.async_block_till_done()
        listed = (await _call(client, "deleted_list"))["result"]["deleted"]
        assert len(listed) == 1
        assert listed[0]["title"] == "Strom Haus" and listed[0]["sparte"] == "electricity"
        assert "data" not in listed[0]  # the list shows no personal data

        reply = await _call(client, "deleted_restore", item_id=listed[0]["id"])
        assert reply["result"] == {"title": "Strom Haus"}
        await hass.async_block_till_done()
        restored = _entries(hass)["Strom Haus"]
        assert dict(restored.data) == RICH and dict(restored.options) == NEXT
        assert (await _call(client, "deleted_list"))["result"]["deleted"] == []  # used up

    async def test_it_cannot_be_restored_over_an_existing_contract(self, frontend_env, hass, hass_ws_client):  # noqa: F811
        client = await hass_ws_client()
        entry = await _add(hass, "Strom Haus", STROM)
        await hass.config_entries.async_remove(entry.entry_id)
        await hass.async_block_till_done()
        await _add(hass, "Strom Haus", STROM)  # a new one with the same name
        (item,) = (await _call(client, "deleted_list"))["result"]["deleted"]
        reply = await _call(client, "deleted_restore", item_id=item["id"])
        assert reply["error"]["code"] == "exists"
        assert len(hass.config_entries.async_entries(DOMAIN)) == 1
        assert len((await _call(client, "deleted_list"))["result"]["deleted"]) == 1  # still there

    async def test_a_deleted_contract_can_be_forgotten_at_once(self, frontend_env, hass, hass_ws_client):  # noqa: F811
        client = await hass_ws_client()
        entry = await _add(hass, "Strom Haus", RICH)
        other = await _add(hass, "Wasser", {**STROM, "sparte": "water"})
        await hass.config_entries.async_remove(entry.entry_id)
        await hass.config_entries.async_remove(other.entry_id)
        await hass.async_block_till_done()
        await _add(hass, "Gas", {**STROM, "sparte": "gas"})  # the panel exists while there is a contract
        listed = (await _call(client, "deleted_list"))["result"]["deleted"]
        assert {item["title"] for item in listed} == {"Strom Haus", "Wasser"}
        strom = next(item for item in listed if item["title"] == "Strom Haus")
        reply = await _call(client, "deleted_discard", item_id=strom["id"])
        assert reply["success"] is True
        assert [i["title"] for i in (await _call(client, "deleted_list"))["result"]["deleted"]] == ["Wasser"]
        reply = await _call(client, "deleted_discard", item_id=strom["id"])
        assert reply["error"]["code"] == "not_found"
        reply = await _call(client, "deleted_restore", item_id=strom["id"])
        assert reply["error"]["code"] == "not_found"  # really gone

    async def test_unknown_id(self, frontend_env, hass, hass_ws_client):  # noqa: F811
        client = await hass_ws_client()
        await _add(hass, "Strom Haus", STROM)
        reply = await _call(client, "deleted_restore", item_id="nope")
        assert reply["error"]["code"] == "not_found"

    async def test_old_ones_expire_and_the_list_is_limited(self, frontend_env, hass, hass_ws_client, freezer):  # noqa: F811
        client = await hass_ws_client()
        freezer.move_to("2026-07-01 12:00:00")
        first = await _add(hass, "Alt", STROM)
        await hass.config_entries.async_remove(first.entry_id)
        await hass.async_block_till_done()
        assert len((await _call(client, "deleted_list"))["result"]["deleted"]) == 1
        freezer.tick(timedelta(days=31))
        assert (await _call(client, "deleted_list"))["result"]["deleted"] == []  # after 30 days

        for index in range(backup.DELETED_MAX + 3):
            entry = await _add(hass, f"V{index}", STROM)
            await hass.config_entries.async_remove(entry.entry_id)
        await hass.async_block_till_done()
        listed = (await _call(client, "deleted_list"))["result"]["deleted"]
        assert len(listed) == backup.DELETED_MAX
        assert listed[0]["title"] == f"V{backup.DELETED_MAX + 2}"  # newest first

    async def test_a_failing_backup_never_blocks_the_removal(self, frontend_env, hass):  # noqa: F811
        entry = await _add(hass, "Strom Haus", STROM)

        async def boom(*_args, **_kwargs):
            raise RuntimeError("disk full")

        with patch("custom_components.tariffy.backup._load_deleted", boom):
            assert await hass.config_entries.async_remove(entry.entry_id)
        assert not hass.config_entries.async_entries(DOMAIN)
