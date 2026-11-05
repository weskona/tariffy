"""Sidebar panel (beta): serves the panel and the contract data it displays.

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
DATA_KEY = f"{DOMAIN}_panel"

# Values shown by the panel. Deliberately a whitelist: the panel is visible to
# every user, so customer number, meter numbers, MaLo-ID, notification target
# and internal flags are not sent.
CONTRACT_FIELDS = (
    "sparte",
    "anbieter",
    "tarif",
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
    "abschlag_warnung_aktiv",
    "abschlag_warnung_zu_bestaetigen",
    "wechsel",
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
