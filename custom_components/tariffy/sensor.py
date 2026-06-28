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
    CONF_ABSCHLAG,
    CONF_ANBIETER,
    CONF_ARBEITSPREIS,
    CONF_ARBEITSPREIS_ABWASSER,
    CONF_ARBEITSPREIS_NACHT,
    CONF_EINSPEISEVERGUETUNG,
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
    DOMAIN,
    ENERGIE_SPARTEN,
    GAS_SPARTE,
    NEXT_PREFIX,
    VERBRAUCH_KWH_EINHEIT,
    WASSER_SPARTE,
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
    wasser_only: bool = False
    strom_only: bool = False


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
        # Einheit wird dynamisch gesetzt
        state_class=SensorStateClass.MEASUREMENT,
        energie_only=True,
        value_fn=lambda d: d.get(CONF_GRUNDPREIS),
    ),
    VertragSensorDescription(
        key="monatliche_kosten",
        translation_key="monatliche_kosten",
        # Einheit wird dynamisch gesetzt
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.get(CONF_ABSCHLAG),
    ),
    VertragSensorDescription(
        key="jahreskosten",
        translation_key="jahreskosten",
        # Einheit wird dynamisch gesetzt
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.get("jahreskosten"),
    ),
    VertragSensorDescription(
        key="geschaetzte_jahreskosten",
        translation_key="geschaetzte_jahreskosten",
        # Einheit wird dynamisch gesetzt
        state_class=SensorStateClass.MEASUREMENT,
        energie_only=True,
        value_fn=lambda d: d.get("geschaetzte_jahreskosten"),
    ),
    VertragSensorDescription(
        key="verbrauch_kwh",
        translation_key="verbrauch_kwh",
        native_unit_of_measurement=VERBRAUCH_KWH_EINHEIT,
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
        # Einheit wird dynamisch gesetzt
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
    VertragSensorDescription(
        key="arbeitspreis_abwasser",
        translation_key="arbeitspreis_abwasser",
        state_class=SensorStateClass.MEASUREMENT,
        wasser_only=True,
        value_fn=lambda d: d.get(CONF_ARBEITSPREIS_ABWASSER),
        attr_fn=lambda d: {
            "typ": d.get("abwasser_typ"),
            "pauschal_monat": d.get("abwasser_pauschal_monat"),
        },
    ),
    VertragSensorDescription(
        key="arbeitspreis_gesamt_wasser",
        translation_key="arbeitspreis_gesamt_wasser",
        state_class=SensorStateClass.MEASUREMENT,
        wasser_only=True,
        value_fn=lambda d: d.get("arbeitspreis_gesamt_wasser"),
    ),
    VertragSensorDescription(
        key="einspeiseverguetung",
        translation_key="einspeiseverguetung",
        state_class=SensorStateClass.MEASUREMENT,
        strom_only=True,
        value_fn=lambda d: d.get(CONF_EINSPEISEVERGUETUNG),
    ),
    VertragSensorDescription(
        key="einnahmen_einspeisung",
        translation_key="einnahmen_einspeisung",
        state_class=SensorStateClass.MEASUREMENT,
        strom_only=True,
        value_fn=lambda d: d.get("einnahmen_einspeisung"),
        attr_fn=lambda d: {
            "einspeisung_kwh": d.get("einspeisung_kwh"),
        },
    ),
    VertragSensorDescription(
        key="nettokosten",
        translation_key="nettokosten",
        state_class=SensorStateClass.MEASUREMENT,
        strom_only=True,
        value_fn=lambda d: d.get("nettokosten"),
        attr_fn=lambda d: {
            "jahreskosten_abschlag": d.get("jahreskosten"),
            "einnahmen_einspeisung": d.get("einnahmen_einspeisung"),
        },
    ),
    VertragSensorDescription(
        key="arbeitspreis_nacht",
        translation_key="arbeitspreis_nacht",
        state_class=SensorStateClass.MEASUREMENT,
        energie_only=True,
        value_fn=lambda d: d.get("arbeitspreis_nacht"),
        attr_fn=lambda d: {
            "verbrauch_tag": d.get("jahresverbrauch_tag"),
            "verbrauch_nacht": d.get("jahresverbrauch_nacht"),
            "tou_jahreskosten": d.get("tou_jahreskosten"),
        },
    ),
    VertragSensorDescription(
        key="effektiver_arbeitspreis",
        translation_key="effektiver_arbeitspreis",
        state_class=SensorStateClass.MEASUREMENT,
        energie_only=True,
        value_fn=lambda d: d.get("effektiver_arbeitspreis"),
        attr_fn=lambda d: {
            "tier_limits": d.get("tier_limits"),
            "tier_prices": d.get("tier_prices"),
            "tiered_jahreskosten": d.get("tiered_jahreskosten"),
            "aktiv": d.get("ist_tiered"),
        },
    ),
    VertragSensorDescription(
        key="verbrauch_bisher",
        translation_key="verbrauch_bisher",
        state_class=SensorStateClass.MEASUREMENT,
        energie_only=True,
        value_fn=lambda d: d.get("verbrauch_bisher"),
        attr_fn=lambda d: {
            "verbrauch_hochgerechnet": d.get("verbrauch_hochgerechnet"),
        },
    ),
    VertragSensorDescription(
        key="verbrauch_hochgerechnet",
        translation_key="verbrauch_hochgerechnet",
        state_class=SensorStateClass.MEASUREMENT,
        energie_only=True,
        value_fn=lambda d: d.get("verbrauch_hochgerechnet"),
    ),
    VertragSensorDescription(
        key="prognose_real",
        translation_key="prognose_real",
        # Einheit wird dynamisch gesetzt
        energie_only=True,
        value_fn=lambda d: d.get("prognose_real"),
        attr_fn=lambda d: {
            "tendenz": None if d.get("prognose_real") is None else (
                "Guthaben" if d.get("prognose_real", 0) >= 0 else "Nachzahlung"
            ),
            "verbrauch_hochgerechnet": d.get("verbrauch_hochgerechnet"),
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

    ist_wasser = sparte == WASSER_SPARTE
    ist_strom = sparte in ("electricity", "strom")

    def _passend(desc: VertragSensorDescription) -> bool:
        if desc.energie_only and not ist_energie:
            return False
        if desc.gas_only and not ist_gas:
            return False
        if desc.wasser_only and not ist_wasser:
            return False
        if desc.strom_only and not ist_strom:
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
        if description.key in (CONF_ARBEITSPREIS, "arbeitspreis_abwasser", "arbeitspreis_gesamt_wasser", CONF_EINSPEISEVERGUETUNG):
            currency = coordinator.data.get("currency", "€")
            wasser_einheit = coordinator.data.get("wasser_einheit", "m³")
            if sparte in ("electricity", "strom"):
                self._attr_native_unit_of_measurement = f"{currency}/kWh"
            elif sparte == GAS_SPARTE:
                self._attr_native_unit_of_measurement = f"{currency}/kWh"
            elif sparte == WASSER_SPARTE:
                self._attr_native_unit_of_measurement = f"{currency}/{wasser_einheit}"
            else:
                self._attr_native_unit_of_measurement = currency

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Dynamische Einheit basierend auf HA-Währung."""
        static = self._attr_native_unit_of_measurement
        if static is not None:
            return static
        d = self.coordinator.data
        currency = d.get("currency", "€")
        key = self.entity_description.key
        if key in ("monatliche_kosten", "grundpreis"):
            return f"{currency}/month"
        if key in ("jahreskosten", "geschaetzte_jahreskosten"):
            return f"{currency}/year"
        if key in ("prognose", "prognose_real", "bonus", "einnahmen_einspeisung", "nettokosten"):
            return currency
        return None

    @property
    def native_value(self) -> Any:
        return self.entity_description.value_fn(self.coordinator.data)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        if self.entity_description.attr_fn is not None:
            return self.entity_description.attr_fn(self.coordinator.data)
        return None
