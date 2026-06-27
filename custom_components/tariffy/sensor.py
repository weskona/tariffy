"""Sensoren der Tariffy-Integration."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import EntityCategory, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ABSCHLAG_EINHEIT,
    ARBEITSPREIS_EINHEIT,
    CONF_ABSCHLAG,
    CONF_ANBIETER,
    CONF_ARBEITSPREIS,
    CONF_BONUS,
    CONF_BRENNWERT,
    CONF_ENDE,
    CONF_GRUNDPREIS,
    CONF_JAHRESVERBRAUCH,
    CONF_KUNDENNUMMER,
    CONF_MARKTLOKATION,
    CONF_OEKOSTROM,
    CONF_PREISGARANTIE,
    CONF_SPARTE,
    CONF_TARIF,
    CONF_ZAEHLERNUMMER,
    CONF_ZUSTANDSZAHL,
    DEFAULT_ARBEITSPREIS_EINHEIT,
    DOMAIN,
    ENERGIE_SPARTEN,
    EURO_EINHEIT,
    GAS_SPARTE,
    GRUNDPREIS_EINHEIT,
    JAHRESKOSTEN_EINHEIT,
    NEXT_PREFIX,
    VERBRAUCH_EINHEIT,
)
from .coordinator import TariffyCoordinator

if TYPE_CHECKING:
    from . import TariffyConfigEntry


def _next_attrs(nxt: dict[str, Any]) -> dict[str, Any]:
    if not nxt:
        return {}
    return {
        "anbieter": nxt.get(NEXT_PREFIX + CONF_ANBIETER),
        "tarif": nxt.get(NEXT_PREFIX + CONF_TARIF),
        "kundennummer": nxt.get(NEXT_PREFIX + CONF_KUNDENNUMMER),
        "arbeitspreis": nxt.get(NEXT_PREFIX + CONF_ARBEITSPREIS),
        "grundpreis": nxt.get(NEXT_PREFIX + CONF_GRUNDPREIS),
        "abschlag": nxt.get(NEXT_PREFIX + CONF_ABSCHLAG),
        "jahresverbrauch": nxt.get(NEXT_PREFIX + CONF_JAHRESVERBRAUCH),
        "ende": nxt.get(NEXT_PREFIX + CONF_ENDE),
    }


def _arbeitspreis_attrs(d: dict[str, Any]) -> dict[str, Any]:
    return {
        "anbieter": d.get(CONF_ANBIETER),
        "tarif": d.get(CONF_TARIF),
        "kundennummer": d.get(CONF_KUNDENNUMMER),
        "sparte": d.get(CONF_SPARTE),
        "jahresverbrauch": d.get(CONF_JAHRESVERBRAUCH),
        "marktlokation": d.get(CONF_MARKTLOKATION),
        "oekostrom": d.get(CONF_OEKOSTROM),
        "bonus": d.get(CONF_BONUS),
        "preisgarantie_bis": (
            d.get(CONF_PREISGARANTIE).isoformat()
            if d.get(CONF_PREISGARANTIE)
            else None
        ),
    }


def _prognose_attrs(d: dict[str, Any]) -> dict[str, Any]:
    diff = d.get("prognose")
    return {
        "tendenz": None if diff is None else ("Guthaben" if diff >= 0 else "Nachzahlung"),
        "abschlagssumme": d.get("jahreskosten"),
        "geschaetzte_kosten": d.get("geschaetzte_jahreskosten"),
    }


@dataclass(frozen=True, kw_only=True)
class VertragSensorDescription(SensorEntityDescription):
    value_fn: Callable[[dict[str, Any]], Any]
    attr_fn: Callable[[dict[str, Any]], dict[str, Any]] | None = None
    energie_only: bool = False
    gas_only: bool = False


SENSOREN: tuple[VertragSensorDescription, ...] = (
    VertragSensorDescription(
        key=CONF_ARBEITSPREIS,
        translation_key="arbeitspreis",
        state_class=SensorStateClass.MEASUREMENT,
        energie_only=True,
        value_fn=lambda d: d.get(CONF_ARBEITSPREIS),
        attr_fn=_arbeitspreis_attrs,
    ),
    VertragSensorDescription(
        key=CONF_GRUNDPREIS,
        translation_key="grundpreis",
        native_unit_of_measurement=GRUNDPREIS_EINHEIT,
        state_class=SensorStateClass.MEASUREMENT,
        energie_only=True,
        value_fn=lambda d: d.get(CONF_GRUNDPREIS),
    ),
    VertragSensorDescription(
        key="monatliche_kosten",
        translation_key="monatliche_kosten",
        native_unit_of_measurement=ABSCHLAG_EINHEIT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.get(CONF_ABSCHLAG),
    ),
    VertragSensorDescription(
        key="jahreskosten",
        translation_key="jahreskosten",
        native_unit_of_measurement=JAHRESKOSTEN_EINHEIT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.get("jahreskosten"),
    ),
    VertragSensorDescription(
        key="geschaetzte_jahreskosten",
        translation_key="geschaetzte_jahreskosten",
        native_unit_of_measurement=JAHRESKOSTEN_EINHEIT,
        state_class=SensorStateClass.MEASUREMENT,
        energie_only=True,
        value_fn=lambda d: d.get("geschaetzte_jahreskosten"),
    ),
    VertragSensorDescription(
        key="verbrauch_kwh",
        translation_key="verbrauch_kwh",
        native_unit_of_measurement=VERBRAUCH_EINHEIT,
        state_class=SensorStateClass.MEASUREMENT,
        gas_only=True,
        value_fn=lambda d: d.get("verbrauch_kwh"),
        attr_fn=lambda d: {
            "jahresverbrauch_m3": d.get(CONF_JAHRESVERBRAUCH),
            "brennwert": d.get(CONF_BRENNWERT),
            "zustandszahl": d.get(CONF_ZUSTANDSZAHL),
        },
    ),
    VertragSensorDescription(
        key="prognose",
        translation_key="prognose",
        native_unit_of_measurement=EURO_EINHEIT,
        energie_only=True,
        value_fn=lambda d: d.get("prognose"),
        attr_fn=_prognose_attrs,
    ),
    VertragSensorDescription(
        key="restlaufzeit",
        translation_key="restlaufzeit",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.DAYS,
        value_fn=lambda d: d.get("restlaufzeit"),
    ),
    VertragSensorDescription(
        key=CONF_ENDE,
        translation_key="ende",
        device_class=SensorDeviceClass.DATE,
        value_fn=lambda d: d.get(CONF_ENDE),
    ),
    VertragSensorDescription(
        key=CONF_ANBIETER,
        translation_key="anbieter",
        value_fn=lambda d: d.get(CONF_ANBIETER),
    ),
    VertragSensorDescription(
        key=CONF_KUNDENNUMMER,
        translation_key="kundennummer",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda d: d.get(CONF_KUNDENNUMMER),
    ),
    VertragSensorDescription(
        key=CONF_ZAEHLERNUMMER,
        translation_key="zaehlernummer",
        entity_category=EntityCategory.DIAGNOSTIC,
        energie_only=True,
        value_fn=lambda d: d.get(CONF_ZAEHLERNUMMER),
    ),
    VertragSensorDescription(
        key=CONF_TARIF,
        translation_key="tarif",
        value_fn=lambda d: d.get(CONF_TARIF),
    ),
    VertragSensorDescription(
        key="naechster_wechsel",
        translation_key="naechster_wechsel",
        device_class=SensorDeviceClass.DATE,
        value_fn=lambda d: d.get("wechsel"),
        attr_fn=lambda d: _next_attrs(d.get("next") or {}),
    ),
    VertragSensorDescription(
        key="kuendigung_erinnerung",
        translation_key="kuendigung_erinnerung",
        device_class=SensorDeviceClass.DATE,
        value_fn=lambda d: d.get("erinnerung_datum"),
        attr_fn=lambda d: {
            "aktiv": d.get("erinnerung_aktiv"),
            "bestaetigt": d.get("erinnerung_bestaetigt"),
            "monate_vorher": d.get("erinnerung_monate"),
        },
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: "TariffyConfigEntry",
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data
    sparte = coordinator.data.get(CONF_SPARTE)
    ist_energie = sparte in ENERGIE_SPARTEN
    ist_gas = sparte == GAS_SPARTE

    def _passend(desc: VertragSensorDescription) -> bool:
        if desc.energie_only and not ist_energie:
            return False
        if desc.gas_only and not ist_gas:
            return False
        return True

    async_add_entities(
        VertragSensor(coordinator, entry, desc) for desc in SENSOREN if _passend(desc)
    )


class VertragSensor(CoordinatorEntity[TariffyCoordinator], SensorEntity):
    _attr_has_entity_name = True
    entity_description: VertragSensorDescription

    def __init__(
        self,
        coordinator: TariffyCoordinator,
        entry: "TariffyConfigEntry",
        description: VertragSensorDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        sparte = coordinator.data.get(CONF_SPARTE)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            manufacturer=coordinator.data.get(CONF_ANBIETER) or None,
            model=(sparte or "").capitalize() or None,
        )
        if description.key == CONF_ARBEITSPREIS:
            self._attr_native_unit_of_measurement = ARBEITSPREIS_EINHEIT.get(
                sparte, DEFAULT_ARBEITSPREIS_EINHEIT
            )

    @property
    def native_value(self) -> Any:
        return self.entity_description.value_fn(self.coordinator.data)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        if self.entity_description.attr_fn is not None:
            return self.entity_description.attr_fn(self.coordinator.data)
        return None
