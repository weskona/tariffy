"""Diagnose-Download fuer einen Vertrag (Einstellungen > Geraete > Diagnose).

Persoenliche Daten (Kundennummer, Zaehlernummer, Marktlokation,
Benachrichtigungsziel) werden geschwaerzt.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.core import HomeAssistant

from . import TariffyConfigEntry
from .const import (
    CONF_KUNDENNUMMER,
    CONF_MARKTLOKATION,
    CONF_NOTIFY_TARGET,
    CONF_VERBRAUCH_SENSOR,
    CONF_VERBRAUCH_SENSOR_NT,
    CONF_ZAEHLERNUMMER,
    CONF_ZAEHLERNUMMER_NT,
)

TO_REDACT = {
    CONF_KUNDENNUMMER,
    CONF_MARKTLOKATION,
    CONF_NOTIFY_TARGET,
    CONF_ZAEHLERNUMMER,
    CONF_ZAEHLERNUMMER_NT,
}


def _plain(value: Any) -> Any:
    """Macht Datumswerte und verschachtelte Daten JSON-tauglich."""
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(k): _plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_plain(v) for v in value]
    return value


def _meter_state(hass: HomeAssistant, entity_id: str | None) -> dict[str, Any] | None:
    if not entity_id:
        return None
    state = hass.states.get(entity_id)
    if state is None:
        return {"entity_id": entity_id, "state": "fehlt"}
    return {
        "entity_id": entity_id,
        "state": state.state,
        "last_changed": state.last_changed.isoformat(),
        "last_updated": state.last_updated.isoformat(),
        "unit": state.attributes.get("unit_of_measurement"),
        "state_class": state.attributes.get("state_class"),
    }


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: TariffyConfigEntry
) -> dict[str, Any]:
    coordinator = entry.runtime_data
    last_exception = coordinator.last_exception
    return {
        "entry": {
            "title": entry.title,
            "data": async_redact_data(_plain(dict(entry.data)), TO_REDACT),
            "options": async_redact_data(_plain(dict(entry.options)), TO_REDACT),
        },
        "update": {
            "last_update_success": coordinator.last_update_success,
            "last_exception": repr(last_exception) if last_exception else None,
            "update_interval": str(coordinator.update_interval),
        },
        "verbrauch": _plain(coordinator.verbrauch_diag),
        "zaehler": _meter_state(hass, entry.data.get(CONF_VERBRAUCH_SENSOR)),
        "zaehler_nt": _meter_state(hass, entry.data.get(CONF_VERBRAUCH_SENSOR_NT)),
        "daten": async_redact_data(_plain(coordinator.data or {}), TO_REDACT),
    }
