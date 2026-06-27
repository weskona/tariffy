"""Buttons der Tariffy-Integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import TariffyCoordinator

if TYPE_CHECKING:
    from . import TariffyConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    entry: "TariffyConfigEntry",
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data
    async_add_entities(
        [
            VertragWechselButton(coordinator, entry),
            VertragKuendigungButton(coordinator, entry),
        ]
    )


class _VertragButton(CoordinatorEntity[TariffyCoordinator], ButtonEntity):
    """Basis für Vertrags-Buttons."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: TariffyCoordinator,
        entry: "TariffyConfigEntry",
        key: str,
    ) -> None:
        super().__init__(coordinator)
        self._attr_translation_key = key
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
        )


class VertragWechselButton(_VertragButton):
    """Schaltet manuell auf den hinterlegten nächsten Vertrag um."""

    def __init__(self, coordinator, entry) -> None:
        super().__init__(coordinator, entry, "jetzt_wechseln")

    @property
    def available(self) -> bool:
        return super().available and bool(self.coordinator.data.get("next"))

    async def async_press(self) -> None:
        await self.coordinator.async_force_switch()


class VertragKuendigungButton(_VertragButton):
    """Bestätigt die Kündigung und entfernt die Dauerbenachrichtigung."""

    def __init__(self, coordinator, entry) -> None:
        super().__init__(coordinator, entry, "kuendigung_bestaetigen")

    @property
    def available(self) -> bool:
        return super().available and bool(
            self.coordinator.data.get("erinnerung_aktiv")
        )

    async def async_press(self) -> None:
        await self.coordinator.async_confirm_kuendigung()
