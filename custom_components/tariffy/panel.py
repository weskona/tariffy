"""Sidebar panel: serves the panel and the contract data it displays.

The panel only reads. Everything here is best effort: if the panel cannot be
set up (no frontend, http not loaded, ...) a warning is logged and the
integration continues exactly as without a panel.
"""

from __future__ import annotations

from datetime import date, datetime
from functools import partial
import logging
import math
from pathlib import Path
from typing import Any

import voluptuous as vol

from homeassistant.components import frontend, panel_custom, websocket_api
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry, ConfigEntryState
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import (
    async_dispatcher_connect,
    async_dispatcher_send,
)
from homeassistant.loader import async_get_integration

from . import backup, history
from .const import (
    CONF_VERBRAUCH_SENSOR,
    DOMAIN,
    NEXT_PREFIX,
)

_LOGGER = logging.getLogger(__name__)

PANEL_URL_PATH = "tariffy"
PANEL_ELEMENT = "tariffy-panel"
PANEL_TITLE = "Tariffy"
PANEL_ICON = "mdi:cash-multiple"
STATIC_URL = "/tariffy_static"
PANEL_FILE = "tariffy-panel.js"
SIGNAL_CONTRACTS = f"{DOMAIN}_contracts_updated"

# Actions of the panel. Same coordinator methods and same preconditions as the
# button entities (see button.py), so the panel can never do more than the
# buttons can. "Switch now" is deliberately not offered: the next contract
# switches in by itself on its start date.
ACTION_CONFIRM_CANCELLATION = "confirm_cancellation"
ACTION_CONFIRM_WARNING = "confirm_abschlag_warning"
# Archive an expired contract / bring it back. Panel only: it stores a flag in the
# contract data and changes no entity.
ACTION_ARCHIVE = "archive_contract"
ACTION_RESTORE = "restore_contract"
ACTIONS = (
    ACTION_CONFIRM_CANCELLATION,
    ACTION_CONFIRM_WARNING,
    ACTION_ARCHIVE,
    ACTION_RESTORE,
)
DATA_KEY = f"{DOMAIN}_panel"

# Values shown by the panel. Deliberately a whitelist: the panel is visible to
# every user, so customer number, meter numbers, MaLo-ID, notification target
# and internal flags are not sent.
CONTRACT_FIELDS = (
    "sparte",
    "anbieter",
    "tarif",
    "versicherungsart",
    "km_start",
    "km_pro_jahr",
    "currency",
    "beginn",
    "ende",
    "restlaufzeit",
    "arbeitspreis",
    "arbeitspreis_ht",
    "arbeitspreis_nt",
    "arbeitspreis_nacht",
    "effektiver_arbeitspreis",
    "arbeitspreis_gesamt_wasser",
    "grundpreis",
    "abschlag",
    "abschlag_bisher_gezahlt",
    "zahlweise",
    "abschlag_jahr",
    "abschlag_je_zahlung",
    "kosten_jahr",
    "erste_zahlung",
    "naechste_zahlung",
    "jahreskosten",
    "verbrauch_bisher",
    "verbrauch_bisher_ht",
    "verbrauch_bisher_nt",
    "verbrauch_hochgerechnet",
    "verbrauch_letzte_laufzeit",
    "verbrauch_letzte_laufzeit_monate",
    "kosten_bisher",
    "kosten_ht_bisher",
    "kosten_nt_bisher",
    "guthaben_bisher",
    "prognose_real",
    "abschlag_anpassung_empfohlen",
    "empfohlener_abschlag",
    "erinnerung_datum",
    "erinnerung_aktiv",
    "erinnerung_bestaetigt",
    "erinnerung_monate",
    "kuendigungsfrist",
    "kuendigung_bis",
    "mindestlaufzeit",
    "mindestlaufzeit_bis",
    "abschlag_warnung_aktiv",
    "abschlag_warnung_zu_bestaetigen",
    "wechsel",
    "archiviert",
    "archiviert_am",
    "archivierbar",
    "verlaengerbar",
    "historie",
    "einmalposten",
    "einmal_summe",
    "kosten_gesamt",
    "kosten_gesamt_vollstaendig",
    "laufzeiten_anzahl",
    "seit",
)
NEXT_FIELDS = ("beginn", "ende", "anbieter", "tarif", "arbeitspreis", "abschlag")


def _json_safe(value: Any) -> Any:
    """Make a coordinator value safe for JSON (dates, NaN, nested containers)."""
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(v) for v in value]
    return value


def contract_payload(hass: HomeAssistant, entry: ConfigEntry) -> dict[str, Any]:
    """Data of one contract as shown by the panel."""
    data = entry.runtime_data.data or {}
    payload: dict[str, Any] = {"entry_id": entry.entry_id, "title": entry.title}
    for key in CONTRACT_FIELDS:
        payload[key] = _json_safe(data.get(key))

    nxt = data.get("next") or {}
    payload["next"] = (
        {key: _json_safe(nxt.get(NEXT_PREFIX + key)) for key in NEXT_FIELDS}
        if nxt
        else None
    )

    # Unit of the raw consumption values: the unit of the user's meter sensor.
    sensor_id = entry.data.get(CONF_VERBRAUCH_SENSOR)
    state = hass.states.get(sensor_id) if sensor_id else None
    payload["verbrauch_einheit"] = (
        state.attributes.get("unit_of_measurement") if state else None
    )
    return payload


@callback
def async_contracts(hass: HomeAssistant) -> list[dict[str, Any]]:
    """All loaded contracts."""
    contracts = []
    for entry in hass.config_entries.async_entries(DOMAIN):
        if entry.state is not ConfigEntryState.LOADED:
            continue
        if getattr(entry, "runtime_data", None) is None:
            continue
        contracts.append(contract_payload(hass, entry))
    return contracts


@callback
def async_notify(hass: HomeAssistant) -> None:
    """Tell open panels that the contract data changed."""
    async_dispatcher_send(hass, SIGNAL_CONTRACTS)


@callback
def async_attach_entry(hass: HomeAssistant, entry: ConfigEntry, coordinator) -> None:
    """Push a new snapshot to open panels whenever the coordinator updates."""
    entry.async_on_unload(coordinator.async_add_listener(partial(async_notify, hass)))


@websocket_api.websocket_command({vol.Required("type"): "tariffy/contracts"})
@callback
def ws_contracts(hass: HomeAssistant, connection, msg: dict[str, Any]) -> None:
    """Return all contracts."""
    connection.send_result(msg["id"], {"contracts": async_contracts(hass)})


@websocket_api.websocket_command({vol.Required("type"): "tariffy/subscribe"})
@callback
def ws_subscribe(hass: HomeAssistant, connection, msg: dict[str, Any]) -> None:
    """Send all contracts now and again after every change."""

    @callback
    def _push() -> None:
        connection.send_message(
            websocket_api.event_message(msg["id"], {"contracts": async_contracts(hass)})
        )

    connection.subscriptions[msg["id"]] = async_dispatcher_connect(
        hass, SIGNAL_CONTRACTS, _push
    )
    connection.send_result(msg["id"])
    _push()


def _action_available(action: str, data: dict[str, Any]) -> bool:
    """Whether an action is currently possible, like the button's `available`."""
    if action == ACTION_CONFIRM_CANCELLATION:
        return bool(data.get("erinnerung_aktiv"))
    if action == ACTION_CONFIRM_WARNING:
        return bool(data.get("abschlag_warnung_zu_bestaetigen"))
    if action == ACTION_ARCHIVE:
        return bool(data.get("archivierbar"))
    if action == ACTION_RESTORE:
        return bool(data.get("archiviert"))
    return False


@websocket_api.require_admin
@websocket_api.websocket_command(
    {
        vol.Required("type"): "tariffy/action",
        vol.Required("entry_id"): str,
        vol.Required("action"): vol.In(ACTIONS),
    }
)
@websocket_api.async_response
async def ws_action(hass: HomeAssistant, connection, msg: dict[str, Any]) -> None:
    """Run one of the contract actions (administrators only)."""
    entry = hass.config_entries.async_get_entry(msg["entry_id"])
    if (
        entry is None
        or entry.domain != DOMAIN
        or entry.state is not ConfigEntryState.LOADED
        or getattr(entry, "runtime_data", None) is None
    ):
        connection.send_error(msg["id"], "not_found", "Contract not found or not loaded")
        return

    coordinator = entry.runtime_data
    action = msg["action"]
    if not _action_available(action, coordinator.data or {}):
        connection.send_error(
            msg["id"], "not_available", f"Action {action} is not available right now"
        )
        return

    if action == ACTION_CONFIRM_CANCELLATION:
        await coordinator.async_confirm_kuendigung()
    elif action == ACTION_CONFIRM_WARNING:
        await coordinator.async_confirm_abschlag_warnung()
    elif action == ACTION_ARCHIVE:
        await coordinator.async_archive()
    else:
        await coordinator.async_restore()
    connection.send_result(msg["id"], {"ok": True})


def _loaded_entry(hass: HomeAssistant, entry_id: str) -> ConfigEntry | None:
    entry = hass.config_entries.async_get_entry(entry_id)
    if (
        entry is None
        or entry.domain != DOMAIN
        or entry.state is not ConfigEntryState.LOADED
        or getattr(entry, "runtime_data", None) is None
    ):
        return None
    return entry


HISTORY_VALUES = vol.Schema({str: vol.Any(None, str, int, float)})


@websocket_api.require_admin
@websocket_api.websocket_command(
    {
        vol.Required("type"): "tariffy/history_calc",
        vol.Required("entry_id"): str,
        vol.Required("values"): HISTORY_VALUES,
    }
)
@websocket_api.async_response
async def ws_history_calc(hass: HomeAssistant, connection, msg: dict[str, Any]) -> None:
    """Berechnet die automatisch ermittelbaren Werte einer alten Laufzeit (nur Vorschau)."""
    entry = _loaded_entry(hass, msg["entry_id"])
    if entry is None:
        connection.send_error(msg["id"], "not_found", "Contract not found or not loaded")
        return
    try:
        result = await history.async_calc(hass, entry, msg["values"])
    except history.HistoryError as err:
        connection.send_error(msg["id"], err.code, err.code)
        return
    connection.send_result(msg["id"], result)


@websocket_api.require_admin
@websocket_api.websocket_command(
    {
        vol.Required("type"): "tariffy/history_save",
        vol.Required("entry_id"): str,
        vol.Required("values"): HISTORY_VALUES,
        vol.Optional("index"): vol.All(int, vol.Range(min=0)),
    }
)
@websocket_api.async_response
async def ws_history_save(hass: HomeAssistant, connection, msg: dict[str, Any]) -> None:
    """Legt eine alte Laufzeit an oder ersetzt eine vorhandene."""
    entry = _loaded_entry(hass, msg["entry_id"])
    if entry is None:
        connection.send_error(msg["id"], "not_found", "Contract not found or not loaded")
        return
    try:
        index = await history.async_save_term(hass, entry, msg["values"], msg.get("index"))
    except history.HistoryError as err:
        connection.send_error(msg["id"], err.code, err.code)
        return
    await entry.runtime_data.async_refresh()
    connection.send_result(msg["id"], {"index": index})


@websocket_api.require_admin
@websocket_api.websocket_command(
    {
        vol.Required("type"): "tariffy/renew",
        vol.Required("entry_id"): str,
        vol.Required("values"): HISTORY_VALUES,
    }
)
@websocket_api.async_response
async def ws_renew(hass: HomeAssistant, connection, msg: dict[str, Any]) -> None:
    """Verlaengert einen Pauschalvertrag mit neuem Betrag und Ende."""
    entry = _loaded_entry(hass, msg["entry_id"])
    if entry is None:
        connection.send_error(msg["id"], "not_found", "Contract not found or not loaded")
        return
    try:
        await history.async_renew(hass, entry, msg["values"])
    except history.HistoryError as err:
        connection.send_error(msg["id"], err.code, err.code)
        return
    await entry.runtime_data.async_refresh()
    connection.send_result(msg["id"], {"ok": True})


@websocket_api.require_admin
@websocket_api.websocket_command(
    {
        vol.Required("type"): "tariffy/history_delete",
        vol.Required("entry_id"): str,
        vol.Required("index"): vol.All(int, vol.Range(min=0)),
    }
)
@websocket_api.async_response
async def ws_history_delete(hass: HomeAssistant, connection, msg: dict[str, Any]) -> None:
    """Loescht eine Laufzeit aus der Historie."""
    entry = _loaded_entry(hass, msg["entry_id"])
    if entry is None:
        connection.send_error(msg["id"], "not_found", "Contract not found or not loaded")
        return
    try:
        history.delete_term(hass, entry, msg["index"])
    except history.HistoryError as err:
        connection.send_error(msg["id"], err.code, err.code)
        return
    await entry.runtime_data.async_refresh()
    connection.send_result(msg["id"], {"ok": True})


@websocket_api.require_admin
@websocket_api.websocket_command(
    {
        vol.Required("type"): "tariffy/einmal_save",
        vol.Required("entry_id"): str,
        vol.Required("values"): HISTORY_VALUES,
        vol.Optional("index"): vol.All(int, vol.Range(min=0)),
    }
)
@websocket_api.async_response
async def ws_einmal_save(hass: HomeAssistant, connection, msg: dict[str, Any]) -> None:
    """Legt einen Einmalposten (Bonus oder Rechnung) an oder ersetzt ihn."""
    entry = _loaded_entry(hass, msg["entry_id"])
    if entry is None:
        connection.send_error(msg["id"], "not_found", "Contract not found or not loaded")
        return
    try:
        history.save_einmal(hass, entry, msg["values"], msg.get("index"))
    except history.HistoryError as err:
        connection.send_error(msg["id"], err.code, err.code)
        return
    await entry.runtime_data.async_refresh()
    connection.send_result(msg["id"], {"ok": True})


@websocket_api.require_admin
@websocket_api.websocket_command(
    {
        vol.Required("type"): "tariffy/einmal_delete",
        vol.Required("entry_id"): str,
        vol.Required("index"): vol.All(int, vol.Range(min=0)),
    }
)
@websocket_api.async_response
async def ws_einmal_delete(hass: HomeAssistant, connection, msg: dict[str, Any]) -> None:
    """Loescht einen Einmalposten."""
    entry = _loaded_entry(hass, msg["entry_id"])
    if entry is None:
        connection.send_error(msg["id"], "not_found", "Contract not found or not loaded")
        return
    try:
        history.delete_einmal(hass, entry, msg["index"])
    except history.HistoryError as err:
        connection.send_error(msg["id"], err.code, err.code)
        return
    await entry.runtime_data.async_refresh()
    connection.send_result(msg["id"], {"ok": True})


@websocket_api.require_admin
@websocket_api.websocket_command({vol.Required("type"): "tariffy/backup_export"})
@websocket_api.async_response
async def ws_backup_export(hass: HomeAssistant, connection, msg: dict[str, Any]) -> None:
    """Alle Vertraege als Sicherung (enthaelt persoenliche Daten, nur fuer Administratoren)."""
    connection.send_result(msg["id"], {"backup": await backup.async_build_backup(hass)})


@websocket_api.require_admin
@websocket_api.websocket_command(
    {vol.Required("type"): "tariffy/backup_preview", vol.Required("backup"): dict}
)
@callback
def ws_backup_preview(hass: HomeAssistant, connection, msg: dict[str, Any]) -> None:
    """Zeigt, was das Wiederherstellen taete (legt nichts an)."""
    try:
        contracts = backup.sanitize_backup(msg["backup"])
    except backup.BackupError as err:
        connection.send_error(msg["id"], err.code, err.code)
        return
    connection.send_result(msg["id"], {"contracts": backup.plan(hass, contracts)})


@websocket_api.require_admin
@websocket_api.websocket_command(
    {vol.Required("type"): "tariffy/backup_restore", vol.Required("backup"): dict}
)
@websocket_api.async_response
async def ws_backup_restore(hass: HomeAssistant, connection, msg: dict[str, Any]) -> None:
    """Legt die fehlenden Vertraege einer Sicherung an, vorhandene bleiben unberuehrt."""
    try:
        result = await backup.async_restore(hass, msg["backup"])
    except backup.BackupError as err:
        connection.send_error(msg["id"], err.code, err.code)
        return
    connection.send_result(msg["id"], result)


@websocket_api.require_admin
@websocket_api.websocket_command({vol.Required("type"): "tariffy/deleted_list"})
@websocket_api.async_response
async def ws_deleted_list(hass: HomeAssistant, connection, msg: dict[str, Any]) -> None:
    """Die geloeschten Vertraege, die sich noch zurueckholen lassen."""
    connection.send_result(msg["id"], {"deleted": await backup.async_deleted(hass)})


@websocket_api.require_admin
@websocket_api.websocket_command(
    {vol.Required("type"): "tariffy/deleted_restore", vol.Required("item_id"): str}
)
@websocket_api.async_response
async def ws_deleted_restore(hass: HomeAssistant, connection, msg: dict[str, Any]) -> None:
    """Holt einen geloeschten Vertrag zurueck."""
    try:
        title = await backup.async_restore_deleted(hass, msg["item_id"])
    except backup.BackupError as err:
        connection.send_error(msg["id"], err.code, err.code)
        return
    connection.send_result(msg["id"], {"title": title})


@websocket_api.require_admin
@websocket_api.websocket_command(
    {vol.Required("type"): "tariffy/deleted_discard", vol.Required("item_id"): str}
)
@websocket_api.async_response
async def ws_deleted_discard(hass: HomeAssistant, connection, msg: dict[str, Any]) -> None:
    """Vergisst einen geloeschten Vertrag endgueltig."""
    try:
        await backup.async_discard_deleted(hass, msg["item_id"])
    except backup.BackupError as err:
        connection.send_error(msg["id"], err.code, err.code)
        return
    connection.send_result(msg["id"], {"ok": True})


async def async_setup_panel(hass: HomeAssistant) -> None:
    """Register the panel once per Home Assistant. Never raises."""
    state = hass.data.setdefault(
        DATA_KEY, {"commands": False, "static": False, "panel": False}
    )
    try:
        if getattr(hass, "http", None) is None or "frontend" not in hass.config.components:
            _LOGGER.debug("Tariffy: no frontend available, panel not registered")
            return

        if not state["commands"]:
            websocket_api.async_register_command(hass, ws_contracts)
            websocket_api.async_register_command(hass, ws_subscribe)
            websocket_api.async_register_command(hass, ws_action)
            websocket_api.async_register_command(hass, ws_history_calc)
            websocket_api.async_register_command(hass, ws_history_save)
            websocket_api.async_register_command(hass, ws_history_delete)
            websocket_api.async_register_command(hass, ws_renew)
            websocket_api.async_register_command(hass, ws_einmal_save)
            websocket_api.async_register_command(hass, ws_einmal_delete)
            for command in (
                ws_backup_export,
                ws_backup_preview,
                ws_backup_restore,
                ws_deleted_list,
                ws_deleted_restore,
                ws_deleted_discard,
            ):
                websocket_api.async_register_command(hass, command)
            state["commands"] = True

        if not state["static"]:
            await hass.http.async_register_static_paths(
                [
                    StaticPathConfig(
                        STATIC_URL, str(Path(__file__).parent / "frontend"), True
                    )
                ]
            )
            state["static"] = True

        if not state["panel"]:
            version = (await async_get_integration(hass, DOMAIN)).version
            await panel_custom.async_register_panel(
                hass,
                frontend_url_path=PANEL_URL_PATH,
                webcomponent_name=PANEL_ELEMENT,
                sidebar_title=PANEL_TITLE,
                sidebar_icon=PANEL_ICON,
                module_url=f"{STATIC_URL}/{PANEL_FILE}?v={version}",
                embed_iframe=False,
                require_admin=False,
            )
            state["panel"] = True
    except Exception as err:  # noqa: BLE001 - the panel must never break the integration
        _LOGGER.warning("Tariffy: panel could not be set up (%s)", err)


async def async_unload_panel(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Remove the panel when the last contract is unloaded. Never raises."""
    state = hass.data.get(DATA_KEY)
    if not state or not state["panel"]:
        return
    try:
        others_loaded = [
            e
            for e in hass.config_entries.async_entries(DOMAIN)
            if e.entry_id != entry.entry_id and e.state is ConfigEntryState.LOADED
        ]
        if not others_loaded:
            frontend.async_remove_panel(hass, PANEL_URL_PATH, warn_if_unknown=False)
            state["panel"] = False
    except Exception as err:  # noqa: BLE001
        _LOGGER.warning("Tariffy: panel could not be removed (%s)", err)


__all__ = [
    "async_attach_entry",
    "async_contracts",
    "async_notify",
    "async_setup_panel",
    "async_unload_panel",
    "contract_payload",
]
