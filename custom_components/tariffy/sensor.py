"""Sensoren der Tariffy-Integration."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
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
    CONF_BEGINN,
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


_CURRENCY_ICON: dict[str, str] = {
    "EUR": "mdi:currency-eur",
    "USD": "mdi:currency-usd",
    "GBP": "mdi:currency-gbp",
    "JPY": "mdi:currency-jpy",
    "CNY": "mdi:currency-cny",
    "KRW": "mdi:currency-krw",
    "INR": "mdi:currency-inr",
    "RUB": "mdi:currency-rub",
    "BRL": "mdi:currency-brl",
    "TRY": "mdi:currency-try",
    "ILS": "mdi:currency-ils",
    "MYR": "mdi:currency-myr",
    "NGN": "mdi:currency-ngn",
    "PHP": "mdi:currency-php",
    "THB": "mdi:currency-thb",
    "TWD": "mdi:currency-twd",
    "VND": "mdi:currency-vnd",
}


def _fmt_date(d: date | None) -> str | None:
    return d.strftime("%d.%m.%Y") if d else None


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



@dataclass(frozen=True, kw_only=True)
class VertragSensorDescription(SensorEntityDescription):
    value_fn: Callable[[dict[str, Any]], Any]
    attr_fn: Callable[[dict[str, Any]], dict[str, Any]] | None = None
    icon_fn: Callable[[dict[str, Any]], str] | None = None
    energie_only: bool = False
    gas_only: bool = False
    wasser_only: bool = False
    strom_only: bool = False
    tag_nacht_only: bool = False
    tiered_only: bool = False
    currency_icon: bool = False


def _guthaben_icon_fn(key: str) -> Callable[[dict[str, Any]], str]:
    """Icon-Funktion fuer Guthaben/Nachzahlung-Sensoren (Daumen hoch/runter)."""
    def _icon(d: dict[str, Any]) -> str:
        wert = d.get(key)
        if wert is None:
            return "mdi:calculator-variant"
        return "mdi:thumb-up" if wert >= 0 else "mdi:thumb-down"
    return _icon


SENSOREN: tuple[VertragSensorDescription, ...] = (
    VertragSensorDescription(
        key=CONF_ARBEITSPREIS,
        translation_key="arbeitspreis",
        icon="mdi:lightning-bolt",
        state_class=SensorStateClass.MEASUREMENT,
        energie_only=True,
        value_fn=lambda d: d.get(CONF_ARBEITSPREIS),
        attr_fn=_arbeitspreis_attrs,
    ),
    VertragSensorDescription(
        key=CONF_GRUNDPREIS,
        translation_key="grundpreis",
        icon="mdi:calendar-month",
        state_class=SensorStateClass.MEASUREMENT,
        energie_only=True,
        value_fn=lambda d: d.get(CONF_GRUNDPREIS),
    ),
    VertragSensorDescription(
        key=CONF_ABSCHLAG,
        translation_key="abschlag",
        state_class=SensorStateClass.MEASUREMENT,
        currency_icon=True,
        value_fn=lambda d: d.get(CONF_ABSCHLAG),
    ),
    VertragSensorDescription(
        key="jahreskosten",
        translation_key="jahreskosten",
        icon="mdi:cash-multiple",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.get("jahreskosten"),
    ),
    VertragSensorDescription(
        key="verbrauch_kwh",
        translation_key="verbrauch_kwh",
        icon="mdi:fire",
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
        key="restlaufzeit",
        translation_key="restlaufzeit",
        icon="mdi:calendar-clock",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.DAYS,
        value_fn=lambda d: d.get("restlaufzeit"),
    ),
    VertragSensorDescription(
        key=CONF_BEGINN,
        translation_key="beginn",
        icon="mdi:calendar-start",
        value_fn=lambda d: _fmt_date(d.get(CONF_BEGINN)),
    ),
    VertragSensorDescription(
        key=CONF_ENDE,
        translation_key="ende",
        icon="mdi:calendar-end",
        value_fn=lambda d: _fmt_date(d.get(CONF_ENDE)),
    ),
    VertragSensorDescription(
        key=CONF_ANBIETER,
        translation_key="anbieter",
        icon="mdi:domain",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda d: d.get(CONF_ANBIETER),
    ),
    VertragSensorDescription(
        key=CONF_KUNDENNUMMER,
        translation_key="kundennummer",
        icon="mdi:card-account-details",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda d: d.get(CONF_KUNDENNUMMER),
    ),
    VertragSensorDescription(
        key=CONF_ZAEHLERNUMMER,
        translation_key="zaehlernummer",
        icon="mdi:counter",
        entity_category=EntityCategory.DIAGNOSTIC,
        energie_only=True,
        value_fn=lambda d: d.get(CONF_ZAEHLERNUMMER),
    ),
    VertragSensorDescription(
        key=CONF_TARIF,
        translation_key="tarif",
        icon="mdi:tag-text",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda d: d.get(CONF_TARIF),
    ),
    VertragSensorDescription(
        key="naechster_wechsel",
        translation_key="naechster_wechsel",
        icon="mdi:calendar-arrow-right",
        value_fn=lambda d: _fmt_date(d.get("wechsel")),
        attr_fn=lambda d: _next_attrs(d.get("next") or {}),
    ),
    VertragSensorDescription(
        key="kuendigung_erinnerung",
        translation_key="kuendigung_erinnerung",
        icon="mdi:bell-alert",
        value_fn=lambda d: _fmt_date(d.get("erinnerung_datum")),
        attr_fn=lambda d: {
            "aktiv": d.get("erinnerung_aktiv"),
            "bestaetigt": d.get("erinnerung_bestaetigt"),
            "monate_vorher": d.get("erinnerung_monate"),
        },
    ),
    VertragSensorDescription(
        key="arbeitspreis_abwasser",
        translation_key="arbeitspreis_abwasser",
        icon="mdi:water-minus",
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
        icon="mdi:water-plus",
        state_class=SensorStateClass.MEASUREMENT,
        wasser_only=True,
        value_fn=lambda d: d.get("arbeitspreis_gesamt_wasser"),
    ),
    VertragSensorDescription(
        key="einspeiseverguetung",
        translation_key="einspeiseverguetung",
        icon="mdi:transmission-tower-export",
        state_class=SensorStateClass.MEASUREMENT,
        strom_only=True,
        value_fn=lambda d: d.get(CONF_EINSPEISEVERGUETUNG),
    ),
    VertragSensorDescription(
        key="arbeitspreis_nacht",
        translation_key="arbeitspreis_nacht",
        icon="mdi:weather-night",
        state_class=SensorStateClass.MEASUREMENT,
        energie_only=True,
        tag_nacht_only=True,
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
        icon="mdi:stairs-up",
        state_class=SensorStateClass.MEASUREMENT,
        energie_only=True,
        tiered_only=True,
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
        icon="mdi:counter",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.get("verbrauch_bisher"),
        attr_fn=lambda d: {
            "verbrauch_hochgerechnet": d.get("verbrauch_hochgerechnet"),
        },
    ),
    VertragSensorDescription(
        key="verbrauch_hochgerechnet",
        translation_key="verbrauch_hochgerechnet",
        icon="mdi:chart-bell-curve",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.get("verbrauch_hochgerechnet"),
    ),
    VertragSensorDescription(
        key="prognose_real",
        translation_key="prognose_real",
        icon="mdi:calculator-variant",
        icon_fn=_guthaben_icon_fn("prognose_real"),
        value_fn=lambda d: d.get("prognose_real"),
        attr_fn=lambda d: {
            "tendenz": None if d.get("prognose_real") is None else (
                "Guthaben" if d.get("prognose_real", 0) >= 0 else "Nachzahlung"
            ),
            "verbrauch_hochgerechnet": d.get("verbrauch_hochgerechnet"),
        },
    ),
    VertragSensorDescription(
        key="kosten_bisher",
        translation_key="kosten_bisher",
        currency_icon=True,
        state_class=SensorStateClass.MEASUREMENT,
        energie_only=True,
        value_fn=lambda d: d.get("kosten_bisher"),
        attr_fn=lambda d: {
            "verbrauch_bisher": d.get("verbrauch_bisher"),
        },
    ),
    VertragSensorDescription(
        key="guthaben_bisher",
        translation_key="guthaben_bisher",
        icon="mdi:calculator-variant",
        icon_fn=_guthaben_icon_fn("guthaben_bisher"),
        state_class=SensorStateClass.MEASUREMENT,
        energie_only=True,
        value_fn=lambda d: d.get("guthaben_bisher"),
        attr_fn=lambda d: {
            "tendenz": None if d.get("guthaben_bisher") is None else (
                "Guthaben" if d.get("guthaben_bisher", 0) >= 0 else "Nachzahlung"
            ),
            "kosten_bisher": d.get("kosten_bisher"),
        },
    ),
    VertragSensorDescription(
        key="verbrauch_letzte_laufzeit",
        translation_key="verbrauch_letzte_laufzeit",
        icon="mdi:history",
        state_class=SensorStateClass.MEASUREMENT,
        energie_only=True,
        value_fn=lambda d: d.get("verbrauch_letzte_laufzeit"),
    ),
    VertragSensorDescription(
        key="empfohlener_abschlag",
        translation_key="empfohlener_abschlag",
        icon="mdi:cash-check",
        state_class=SensorStateClass.MEASUREMENT,
        energie_only=True,
        value_fn=lambda d: d.get("empfohlener_abschlag"),
        attr_fn=lambda d: {
            "verbrauch_letzte_laufzeit": d.get("verbrauch_letzte_laufzeit"),
            "verbrauch_letzte_laufzeit_monate": d.get("verbrauch_letzte_laufzeit_monate"),
            "aktueller_abschlag": d.get("abschlag"),
            "differenz": (
                round(d["empfohlener_abschlag"] - d["abschlag"], 2)
                if d.get("empfohlener_abschlag") is not None and d.get("abschlag") is not None
                else None
            ),
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
    hat_tag_nacht = bool(coordinator.data.get("hat_tag_nacht"))
    hat_tiered = bool(coordinator.data.get("ist_tiered"))

    def _passend(desc: VertragSensorDescription) -> bool:
        if desc.energie_only and not ist_energie:
            return False
        if desc.gas_only and not ist_gas:
            return False
        if desc.wasser_only and not ist_wasser:
            return False
        if desc.strom_only and not ist_strom:
            return False
        if desc.tag_nacht_only and not hat_tag_nacht:
            return False
        if desc.tiered_only and not hat_tiered:
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
        d = coordinator.data or {}
        sparte = d.get(CONF_SPARTE)
        currency = d.get("currency", "€")
        wasser_einheit = d.get("wasser_einheit", "m³")
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            manufacturer=d.get(CONF_ANBIETER) or None,
            model=(sparte or "").capitalize() or None,
        )
        key = description.key
        if key in (CONF_ARBEITSPREIS, "arbeitspreis_abwasser", "arbeitspreis_gesamt_wasser", CONF_EINSPEISEVERGUETUNG, "arbeitspreis_nacht", "effektiver_arbeitspreis"):
            if sparte == WASSER_SPARTE:
                self._attr_native_unit_of_measurement = f"{currency}/{wasser_einheit}"
            else:
                self._attr_native_unit_of_measurement = f"{currency}/kWh"
        elif key in (CONF_ABSCHLAG, "grundpreis"):
            self._attr_native_unit_of_measurement = f"{currency}/Monat"
        elif key == "jahreskosten":
            self._attr_native_unit_of_measurement = currency
        elif key in ("prognose_real", "bonus", "kosten_bisher", "guthaben_bisher"):
            self._attr_native_unit_of_measurement = currency
        elif key in ("verbrauch_bisher", "verbrauch_hochgerechnet", "verbrauch_letzte_laufzeit"):
            if sparte == GAS_SPARTE:
                self._attr_native_unit_of_measurement = d.get("gas_einheit", "m³")
            elif sparte == WASSER_SPARTE:
                self._attr_native_unit_of_measurement = d.get("wasser_einheit", "m³")
            else:
                self._attr_native_unit_of_measurement = VERBRAUCH_KWH_EINHEIT
        elif key == "empfohlener_abschlag":
            self._attr_native_unit_of_measurement = f"{currency}/Monat"

    @property
    def icon(self) -> str | None:
        if self.entity_description.icon_fn is not None:
            return self.entity_description.icon_fn(self.coordinator.data or {})
        if self.entity_description.currency_icon:
            currency = (self.coordinator.data or {}).get("currency", "EUR")
            return _CURRENCY_ICON.get(currency, "mdi:cash")
        return self.entity_description.icon

    @property
    def native_value(self) -> Any:
        return self.entity_description.value_fn(self.coordinator.data)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        if self.entity_description.attr_fn is not None:
            return self.entity_description.attr_fn(self.coordinator.data)
        return None
