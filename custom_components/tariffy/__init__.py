"""Die Tariffy-Integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_SPARTE, PLATFORMS, SPARTEN_MIGRATION
from .coordinator import TariffyCoordinator

_LOGGER = logging.getLogger(__name__)

type TariffyConfigEntry = ConfigEntry[TariffyCoordinator]


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migration alter Config Entries auf neue Version."""
    _LOGGER.debug("Tariffy: Migration von Version %s", entry.version)

    data = dict(entry.data)
    changed = False

    # v1: Sparten-Migration (strom -> electricity, wasser -> water etc.)
    sparte = data.get(CONF_SPARTE, "")
    if sparte in SPARTEN_MIGRATION:
        data[CONF_SPARTE] = SPARTEN_MIGRATION[sparte]
        _LOGGER.info(
            "Tariffy '%s': Sparte migriert '%s' -> '%s'",
            entry.title, sparte, data[CONF_SPARTE],
        )
        changed = True

    if changed:
        hass.config_entries.async_update_entry(entry, data=data)

    return True


async def async_setup_entry(hass: HomeAssistant, entry: TariffyConfigEntry) -> bool:
    """Einen Vertrag (ConfigEntry) einrichten."""
    coordinator = TariffyCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    return True


async def _async_update_listener(
    hass: HomeAssistant, entry: TariffyConfigEntry
) -> None:
    """Reload bei Konfigurationsaenderung."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(
    hass: HomeAssistant, entry: TariffyConfigEntry
) -> bool:
    """Einen Vertrag entladen."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
