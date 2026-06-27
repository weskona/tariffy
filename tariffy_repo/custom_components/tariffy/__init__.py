"""Die Tariffy-Integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import PLATFORMS
from .coordinator import TariffyCoordinator

type TariffyConfigEntry = ConfigEntry[TariffyCoordinator]


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
    """Reload bei Konfigurationsänderung."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(
    hass: HomeAssistant, entry: TariffyConfigEntry
) -> bool:
    """Einen Vertrag entladen."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
