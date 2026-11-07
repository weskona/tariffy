"""Tests for the sidebar panel backend (panel registration and contract data)."""

from __future__ import annotations

from datetime import date
from unittest.mock import patch

import pytest
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component

from custom_components.tariffy import panel
from custom_components.tariffy.const import DOMAIN

from .test_coordinator import SENSOR, STROM

GOLDEN = {
    "today": "2026-07-12",
    "latest": (2481.17, 2481.17),
    "offset": (1000.0, 1000.0),
    "sensor_states": {SENSOR: "2481.17"},
}
SECRET = {
    **STROM,
    "kundennummer": "K-12345",
    "zaehlernummer": "Z-999",
    "marktlokation": "DE0001",
    "notify_target": "mobile_app_secret",
}


@pytest.fixture
async def frontend_env(hass: HomeAssistant):
    """http and websocket_api running and the frontend marked as loaded.

    The real frontend component needs the large `hass_frontend` package, which
    the panel code does not use; registering a panel only needs the component to
    be present.
    """
    for component in ("http", "websocket_api"):
        assert await async_setup_component(hass, component, {})
    hass.config.components.add("frontend")
    await hass.async_block_till_done()


class TestPanelRegistration:
    async def test_panel_is_registered(self, frontend_env, contract, hass):
        await contract.setup(STROM, **GOLDEN)
        registered = hass.data["frontend_panels"]["tariffy"]
        assert registered.sidebar_title == "Tariffy"
        assert registered.sidebar_icon == "mdi:cash-multiple"
        assert registered.require_admin is False
        config = registered.config["_panel_custom"]
        assert config["name"] == "tariffy-panel"
        assert config["module_url"].startswith("/tariffy_static/tariffy-panel.js?v=")

    async def test_registered_once_for_several_contracts(self, frontend_env, contract, hass):
        await contract.setup(STROM, **GOLDEN)
        with patch.object(panel.panel_custom, "async_register_panel") as register:
            from pytest_homeassistant_custom_component.common import MockConfigEntry

            second = MockConfigEntry(domain=DOMAIN, title="Zweiter", data=STROM)
            second.add_to_hass(hass)
            assert await hass.config_entries.async_setup(second.entry_id)
            await hass.async_block_till_done()
        register.assert_not_called()
        assert second.state is ConfigEntryState.LOADED

    async def test_static_file_is_served(self, frontend_env, contract, hass_client):
        await contract.setup(STROM, **GOLDEN)
        client = await hass_client()
        response = await client.get("/tariffy_static/tariffy-panel.js")
        assert response.status == 200
        assert "tariffy-panel" in await response.text()

    async def test_panel_is_removed_with_the_last_contract(self, frontend_env, contract, hass):
        entry, _ = await contract.setup(STROM, **GOLDEN)
        assert "tariffy" in hass.data["frontend_panels"]
        assert await hass.config_entries.async_unload(entry.entry_id)
        await hass.async_block_till_done()
        assert "tariffy" not in hass.data["frontend_panels"]
        # and it comes back when the contract is loaded again
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        assert "tariffy" in hass.data["frontend_panels"]


class TestPanelNeverBreaksTheIntegration:
    async def test_setup_without_frontend(self, contract):
        # no http / frontend loaded at all (e.g. a minimal installation)
        entry, data = await contract.setup(STROM, **GOLDEN)
        assert entry.state is ConfigEntryState.LOADED
        assert data["prognose_real"] == pytest.approx(-495.29, abs=0.05)

    async def test_failing_registration_only_logs(self, frontend_env, contract, caplog):
        with patch.object(
            panel.panel_custom, "async_register_panel", side_effect=RuntimeError("boom")
        ):
            entry, data = await contract.setup(STROM, **GOLDEN)
        assert entry.state is ConfigEntryState.LOADED
        assert data["kosten_bisher"] is not None
        assert "panel could not be set up (boom)" in caplog.text

    async def test_failing_static_registration_only_logs(self, frontend_env, contract, hass, caplog):
        with patch.object(
            hass.http, "async_register_static_paths", side_effect=RuntimeError("nope")
        ):
            entry, _ = await contract.setup(STROM, **GOLDEN)
        assert entry.state is ConfigEntryState.LOADED
        assert "panel could not be set up (nope)" in caplog.text


class TestContractData:
    async def test_websocket_returns_the_contract(self, frontend_env, contract, hass_ws_client):
        client = await hass_ws_client()  # connect before the test clock moves
        entry, _ = await contract.setup(STROM, **GOLDEN)
        await client.send_json_auto_id({"type": "tariffy/contracts"})
        result = (await client.receive_json())["result"]["contracts"]
        assert len(result) == 1
        c = result[0]
        assert c["entry_id"] == entry.entry_id
        assert c["title"] == "Test"
        assert c["sparte"] == "electricity"
        assert c["anbieter"] == "Stadtwerke"
        assert c["currency"] == "EUR"
        assert c["beginn"] == "2026-01-01"
        assert c["ende"] == "2026-12-31"
        assert c["prognose_real"] == pytest.approx(-495.29, abs=0.05)
        assert c["kosten_bisher"] == pytest.approx(513.54, abs=0.02)
        assert c["guthaben_bisher"] == pytest.approx(-261.24, abs=0.02)
        assert c["next"] is None

    async def test_private_data_is_not_sent(self, frontend_env, contract, hass_ws_client):
        client = await hass_ws_client()
        await contract.setup(SECRET, **GOLDEN)
        await client.send_json_auto_id({"type": "tariffy/contracts"})
        contracts = (await client.receive_json())["result"]["contracts"]
        raw = str(contracts)
        for secret in ("K-12345", "Z-999", "DE0001", "mobile_app_secret"):
            assert secret not in raw
        assert not any(key.startswith("_") for key in contracts[0])

    async def test_consumption_unit_comes_from_the_meter_sensor(self, frontend_env, contract, hass, hass_ws_client):
        client = await hass_ws_client()
        hass.states.async_set(SENSOR, "2481.17", {"unit_of_measurement": "kWh"})
        await contract.setup(STROM, **{**GOLDEN, "sensor_states": {}})
        await client.send_json_auto_id({"type": "tariffy/contracts"})
        c = (await client.receive_json())["result"]["contracts"][0]
        assert c["verbrauch_einheit"] == "kWh"

    async def test_next_contract_summary(self, frontend_env, contract, hass_ws_client):
        client = await hass_ws_client()
        await contract.setup(
            STROM,
            **{**GOLDEN, "today": "2026-06-01"},
            options={"next_beginn": "2027-01-01", "next_anbieter": "Neu", "next_abschlag": 55.0},
        )
        await client.send_json_auto_id({"type": "tariffy/contracts"})
        c = (await client.receive_json())["result"]["contracts"][0]
        assert c["wechsel"] == "2027-01-01"
        assert c["next"]["anbieter"] == "Neu"
        assert c["next"]["abschlag"] == 55.0
        assert c["next"]["tarif"] is None

    async def test_unloaded_contracts_are_not_listed(self, frontend_env, contract, hass, hass_ws_client):
        client = await hass_ws_client()  # connect before the test clock moves
        entry, _ = await contract.setup(STROM, **GOLDEN)
        assert await hass.config_entries.async_unload(entry.entry_id)
        await client.send_json_auto_id({"type": "tariffy/contracts"})
        assert (await client.receive_json())["result"]["contracts"] == []

    async def test_subscription_pushes_updates(self, frontend_env, contract, hass, hass_ws_client):
        client = await hass_ws_client()  # connect before the test clock moves
        entry, _ = await contract.setup(STROM, **GOLDEN)
        await client.send_json_auto_id({"type": "tariffy/subscribe"})
        assert (await client.receive_json())["success"] is True
        first = (await client.receive_json())["event"]["contracts"]
        assert first[0]["verbrauch_bisher"] == pytest.approx(1481.17)

        contract.values["latest"] = (2581.17, 2581.17)
        hass.states.async_set(SENSOR, "2581.17")
        await entry.runtime_data.async_refresh()
        await hass.async_block_till_done()
        update = (await client.receive_json())["event"]["contracts"]
        assert update[0]["verbrauch_bisher"] == pytest.approx(1581.17)


class TestJsonSafe:
    def test_dates_and_non_finite_numbers(self):
        assert panel._json_safe(date(2026, 7, 12)) == "2026-07-12"
        assert panel._json_safe(float("nan")) is None
        assert panel._json_safe(float("inf")) is None
        assert panel._json_safe({"a": [date(2026, 1, 1), 1.5, None]}) == {
            "a": ["2026-01-01", 1.5, None]
        }


async def _action(client, entry_id, action):
    await client.send_json_auto_id(
        {"type": "tariffy/action", "entry_id": entry_id, "action": action}
    )
    return await client.receive_json()


class TestActions:
    """Confirm cancellation / confirm instalment warning.

    Same coordinator methods and preconditions as the button entities,
    restricted to administrators."""

    NEXT = {"next_beginn": "2027-01-01", "next_anbieter": "Neuer Anbieter", "next_abschlag": 55.0}
    CANCEL = {**STROM, "ende": "2026-09-30", "erinnerung_monate": "3"}
    WARN = {**STROM, "abschlag_warnung": True, "abschlag_warnung_schwelle": 50.0}

    async def test_switch_now_is_not_a_panel_action(self, frontend_env, contract, hass, hass_ws_client):
        client = await hass_ws_client()
        entry, _ = await contract.setup(STROM, **GOLDEN, options=dict(self.NEXT))
        reply = await _action(client, entry.entry_id, "switch_now")
        assert reply["success"] is False
        assert reply["error"]["code"] == "invalid_format"
        assert entry.data["anbieter"] == "Stadtwerke"  # not switched
        assert entry.options["next_anbieter"] == "Neuer Anbieter"

    async def test_confirm_cancellation(self, frontend_env, contract, hass, hass_ws_client):
        client = await hass_ws_client()
        entry, data = await contract.setup(self.CANCEL, **{**GOLDEN, "today": "2026-07-01"})
        assert data["erinnerung_aktiv"] is True
        assert any(k.startswith("tariffy_kuendigung_") for k in hass.data["persistent_notification"])

        reply = await _action(client, entry.entry_id, "confirm_cancellation")
        assert reply["success"] is True
        await hass.async_block_till_done()
        assert entry.data["_kuendigung_bestaetigt"] is True
        assert entry.runtime_data.data["erinnerung_aktiv"] is False
        assert not any(k.startswith("tariffy_kuendigung_") for k in hass.data["persistent_notification"])

    async def test_confirm_instalment_warning(self, frontend_env, contract, hass, hass_ws_client):
        client = await hass_ws_client()
        entry, data = await contract.setup(self.WARN, **GOLDEN)
        assert data["abschlag_warnung_zu_bestaetigen"] is True

        reply = await _action(client, entry.entry_id, "confirm_abschlag_warning")
        assert reply["success"] is True
        await hass.async_block_till_done()
        assert entry.data["_abschlag_warnung_bestaetigt"] is True
        assert entry.runtime_data.data["abschlag_warnung_zu_bestaetigen"] is False

    @pytest.mark.parametrize(
        ("data", "options", "action"),
        [
            (STROM, {}, "confirm_cancellation"),  # reminder not active
            (STROM, {}, "confirm_abschlag_warning"),  # warning not active
        ],
    )
    async def test_unavailable_actions_are_refused(self, frontend_env, contract, hass_ws_client, data, options, action):
        client = await hass_ws_client()
        entry, before = await contract.setup(data, **GOLDEN, options=options)
        reply = await _action(client, entry.entry_id, action)
        assert reply["success"] is False
        assert reply["error"]["code"] == "not_available"
        assert entry.data["anbieter"] == "Stadtwerke"  # nothing changed

    async def test_unknown_contract(self, frontend_env, contract, hass_ws_client):
        client = await hass_ws_client()
        await contract.setup(STROM, **GOLDEN)
        reply = await _action(client, "does-not-exist", "confirm_cancellation")
        assert reply["error"]["code"] == "not_found"

    async def test_unloaded_contract(self, frontend_env, contract, hass, hass_ws_client):
        client = await hass_ws_client()
        entry, _ = await contract.setup(STROM, **GOLDEN)
        assert await hass.config_entries.async_unload(entry.entry_id)
        reply = await _action(client, entry.entry_id, "confirm_cancellation")
        assert reply["error"]["code"] == "not_found"

    async def test_unknown_action_is_rejected(self, frontend_env, contract, hass_ws_client):
        client = await hass_ws_client()
        entry, _ = await contract.setup(STROM, **GOLDEN)
        reply = await _action(client, entry.entry_id, "delete_everything")
        assert reply["success"] is False
        assert reply["error"]["code"] == "invalid_format"

    async def test_non_admin_cannot_run_actions(
        self, frontend_env, contract, hass, hass_ws_client, hass_read_only_access_token
    ):
        client = await hass_ws_client(hass, hass_read_only_access_token)
        entry, _ = await contract.setup(self.WARN, **GOLDEN)
        reply = await _action(client, entry.entry_id, "confirm_abschlag_warning")
        assert reply["success"] is False
        assert reply["error"]["code"] == "unauthorized"
        assert not entry.data.get("_abschlag_warnung_bestaetigt")  # not acknowledged

    async def test_non_admin_can_still_read_the_contracts(
        self, frontend_env, contract, hass, hass_ws_client, hass_read_only_access_token
    ):
        client = await hass_ws_client(hass, hass_read_only_access_token)
        await contract.setup(STROM, **GOLDEN)
        await client.send_json_auto_id({"type": "tariffy/contracts"})
        assert len((await client.receive_json())["result"]["contracts"]) == 1
