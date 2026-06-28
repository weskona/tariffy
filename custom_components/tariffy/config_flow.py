"""Config- und Options-Flow der Tariffy-Integration (sparten-abhaengig)."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import selector

from .const import (
    ABWASSER_TYPEN,
    ABWASSER_TYP_PAUSCHAL,
    ABWASSER_TYP_PREIS,
    ABWASSER_TYP_PROZENT,
    CONF_ABSCHLAG,
    CONF_ABWASSER_TYP,
    CONF_ANBIETER,
    CONF_ARBEITSPREIS,
    CONF_ARBEITSPREIS_ABWASSER,
    CONF_ARBEITSPREIS_NACHT,
    CONF_BEGINN,
    CONF_BONUS,
    CONF_BRENNWERT,
    CONF_EINSPEISEVERGUETUNG,
    CONF_EINSPEISUNG_SENSOR,
    CONF_ENDE,
    CONF_ERINNERUNG_MONATE,
    CONF_GAS_EINHEIT,
    CONF_GRUNDPREIS,
    CONF_JAHRESVERBRAUCH,
    CONF_JAHRESVERBRAUCH_NACHT,
    CONF_JAHRESVERBRAUCH_TAG,
    CONF_KUNDENNUMMER,
    CONF_MARKTLOKATION,
    CONF_NOTIFY_TARGET,
    CONF_OEKOSTROM,
    CONF_PREISGARANTIE,
    CONF_SPARTE,
    CONF_TARIF,
    CONF_TIERED,
    CONF_TIER_LIMITS,
    CONF_TIER_PRICES,
    CONF_VERBRAUCH_SENSOR,
    CONF_WASSER_EINHEIT,
    CONF_ZAEHLERNUMMER,
    CONF_ZUSTANDSZAHL,
    DOMAIN,
    ENERGIE_SPARTEN,
    ERINNERUNG_OPTIONS,
    GAS_EINHEITEN,
    GAS_SPARTE,
    LAENDER_ABWASSER_PAUSCHAL,
    LAENDER_ABWASSER_PROZENT,
    LAENDER_TAG_NACHT,
    LAENDER_TIERED,
    MAX_TIERS,
    NEXT_PREFIX,
    SPARTEN,
    VERBRAUCH_EINHEIT,
    VERBRAUCH_M3_EINHEIT,
    WASSER_EINHEITEN,
    WASSER_SPARTE,
)


# ------------------------------------------------------------------ helpers

def _opt(key: str, default: Any = None) -> vol.Optional:
    if default in (None, ""):
        return vol.Optional(key)
    return vol.Optional(key, description={"suggested_value": default})


def _preis(step=None) -> selector.NumberSelector:
    return selector.NumberSelector(
        selector.NumberSelectorConfig(min=0, step="any", mode=selector.NumberSelectorMode.BOX)
    )


def _verbrauch() -> selector.NumberSelector:
    return selector.NumberSelector(
        selector.NumberSelectorConfig(
            min=0, step="any", mode=selector.NumberSelectorMode.BOX,
            unit_of_measurement=VERBRAUCH_EINHEIT,
        )
    )


def _verbrauch_m3() -> selector.NumberSelector:
    return selector.NumberSelector(
        selector.NumberSelectorConfig(
            min=0, step="any", mode=selector.NumberSelectorMode.BOX,
            unit_of_measurement=VERBRAUCH_M3_EINHEIT,
        )
    )


def _select(options, custom=False) -> selector.SelectSelector:
    return selector.SelectSelector(
        selector.SelectSelectorConfig(
            options=options,
            mode=selector.SelectSelectorMode.DROPDOWN,
            custom_value=custom,
        )
    )


def _country_features(hass: HomeAssistant) -> dict:
    """Gibt laenderspezifische Feature-Flags zurueck."""
    country = (hass.config.country or "").upper()
    return {
        "hat_tag_nacht": country in LAENDER_TAG_NACHT,
        "hat_tiered": country in LAENDER_TIERED,
        "hat_abwasser_prozent": country in LAENDER_ABWASSER_PROZENT,
        "hat_abwasser_pauschal": country in LAENDER_ABWASSER_PAUSCHAL,
        "hat_einspeisung": True,  # weltweit verfuegbar
        "country": country,
    }


def _tiered_fields(d: dict, enabled: bool = True) -> dict:
    """Staffelpreis-Felder — nur wenn im Land verfuegbar."""
    if not enabled:
        return {}
    fields: dict = {}
    fields[vol.Required(CONF_TIERED, default=bool(d.get(CONF_TIERED, False)))] = (
        selector.BooleanSelector()
    )
    limits = d.get(CONF_TIER_LIMITS) or []
    prices = d.get(CONF_TIER_PRICES) or []
    for i in range(MAX_TIERS):
        default_limit = limits[i] if i < len(limits) else None
        default_price = prices[i] if i < len(prices) else None
        fields[_opt(f"tier_limit_{i}", default_limit)] = selector.NumberSelector(
            selector.NumberSelectorConfig(min=0, step="any", mode=selector.NumberSelectorMode.BOX)
        )
        fields[_opt(f"tier_price_{i}", default_price)] = selector.NumberSelector(
            selector.NumberSelectorConfig(min=0, step="any", mode=selector.NumberSelectorMode.BOX)
        )
    return fields


def _tag_nacht_fields(d: dict, enabled: bool = False) -> dict:
    """Tag/Nacht-Felder — nur wenn im Land verfuegbar."""
    if not enabled:
        return {}
    return {
        _opt(CONF_ARBEITSPREIS_NACHT, d.get(CONF_ARBEITSPREIS_NACHT)): _preis(),
        _opt(CONF_JAHRESVERBRAUCH_TAG, d.get(CONF_JAHRESVERBRAUCH_TAG)): selector.NumberSelector(
            selector.NumberSelectorConfig(min=0, step="any", mode=selector.NumberSelectorMode.BOX)
        ),
        _opt(CONF_JAHRESVERBRAUCH_NACHT, d.get(CONF_JAHRESVERBRAUCH_NACHT)): selector.NumberSelector(
            selector.NumberSelectorConfig(min=0, step="any", mode=selector.NumberSelectorMode.BOX)
        ),
    }


def _einspeisung_fields(d: dict, enabled: bool = True) -> dict:
    """Einspeiseverguetung-Felder — weltweit fuer Strom."""
    if not enabled:
        return {}
    return {
        _opt(CONF_EINSPEISEVERGUETUNG, d.get(CONF_EINSPEISEVERGUETUNG)): _preis(),
        _opt(CONF_EINSPEISUNG_SENSOR, d.get(CONF_EINSPEISUNG_SENSOR)): selector.EntitySelector(
            selector.EntitySelectorConfig(domain="sensor")
        ),
    }


# ------------------------------------------------------------------ schemas

def _common_schema(
    hass: HomeAssistant, d: dict[str, Any], *, mit_name: bool
) -> vol.Schema:
    fields: dict[Any, Any] = {}
    if mit_name:
        fields[vol.Required("name")] = selector.TextSelector()
    fields[vol.Required(CONF_SPARTE, default=d.get(CONF_SPARTE, "electricity"))] = _select(SPARTEN)
    if d.get(CONF_ANBIETER):
        fields[vol.Required(CONF_ANBIETER, default=d[CONF_ANBIETER])] = selector.TextSelector()
    else:
        fields[vol.Required(CONF_ANBIETER)] = selector.TextSelector()
    fields[_opt(CONF_KUNDENNUMMER, d.get(CONF_KUNDENNUMMER))] = selector.TextSelector()
    fields[_opt(CONF_TARIF, d.get(CONF_TARIF))] = selector.TextSelector()
    fields[_opt(CONF_BEGINN, d.get(CONF_BEGINN))] = selector.DateSelector()
    fields[_opt(CONF_ENDE, d.get(CONF_ENDE))] = selector.DateSelector()
    fields[vol.Required(CONF_ERINNERUNG_MONATE, default=d.get(CONF_ERINNERUNG_MONATE, "3"))] = (
        _select(ERINNERUNG_OPTIONS)
    )
    notify_dienste = sorted(hass.services.async_services().get("notify", {}))
    if notify_dienste:
        notify_opts = [selector.SelectOptionDict(value=n, label=f"notify.{n}") for n in notify_dienste]
        fields[_opt(CONF_NOTIFY_TARGET, d.get(CONF_NOTIFY_TARGET))] = selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=notify_opts,
                mode=selector.SelectSelectorMode.DROPDOWN,
                custom_value=True,
            )
        )
    return vol.Schema(fields)


def _energie_schema(d: dict[str, Any], features: dict | None = None) -> vol.Schema:
    f = features or {}
    return vol.Schema({
        vol.Required(CONF_ARBEITSPREIS, default=d.get(CONF_ARBEITSPREIS, 0.0)): _preis(),
        vol.Required(CONF_GRUNDPREIS, default=d.get(CONF_GRUNDPREIS, 0.0)): _preis(),
        vol.Required(CONF_ABSCHLAG, default=d.get(CONF_ABSCHLAG, 0.0)): _preis(),
        _opt(CONF_JAHRESVERBRAUCH, d.get(CONF_JAHRESVERBRAUCH)): _verbrauch(),
        _opt(CONF_BONUS, d.get(CONF_BONUS)): _preis(),
        vol.Required(CONF_OEKOSTROM, default=bool(d.get(CONF_OEKOSTROM, False))): selector.BooleanSelector(),
        _opt(CONF_ZAEHLERNUMMER, d.get(CONF_ZAEHLERNUMMER)): selector.TextSelector(),
        _opt(CONF_MARKTLOKATION, d.get(CONF_MARKTLOKATION)): selector.TextSelector(),
        _opt(CONF_PREISGARANTIE, d.get(CONF_PREISGARANTIE)): selector.DateSelector(),
        _opt(CONF_VERBRAUCH_SENSOR, d.get(CONF_VERBRAUCH_SENSOR)): selector.EntitySelector(
            selector.EntitySelectorConfig(domain="sensor")
        ),
        **_tiered_fields(d, enabled=f.get("hat_tiered", True)),
        **_tag_nacht_fields(d, enabled=f.get("hat_tag_nacht", False)),
        **_einspeisung_fields(d, enabled=f.get("hat_einspeisung", True)),
    })


def _gas_schema(d: dict[str, Any], features: dict | None = None) -> vol.Schema:
    f = features or {}
    return vol.Schema({
        vol.Required(CONF_GAS_EINHEIT, default=d.get(CONF_GAS_EINHEIT, "m³")): _select(GAS_EINHEITEN),
        vol.Required(CONF_ARBEITSPREIS, default=d.get(CONF_ARBEITSPREIS, 0.0)): _preis(),
        vol.Required(CONF_GRUNDPREIS, default=d.get(CONF_GRUNDPREIS, 0.0)): _preis(),
        vol.Required(CONF_ABSCHLAG, default=d.get(CONF_ABSCHLAG, 0.0)): _preis(),
        _opt(CONF_JAHRESVERBRAUCH, d.get(CONF_JAHRESVERBRAUCH)): _verbrauch_m3(),
        vol.Required(CONF_BRENNWERT, default=d.get(CONF_BRENNWERT, 11.0)): selector.NumberSelector(
            selector.NumberSelectorConfig(min=0, step="any", mode=selector.NumberSelectorMode.BOX)
        ),
        vol.Required(CONF_ZUSTANDSZAHL, default=d.get(CONF_ZUSTANDSZAHL, 0.95)): selector.NumberSelector(
            selector.NumberSelectorConfig(min=0, step="any", mode=selector.NumberSelectorMode.BOX)
        ),
        _opt(CONF_BONUS, d.get(CONF_BONUS)): _preis(),
        vol.Required(CONF_OEKOSTROM, default=bool(d.get(CONF_OEKOSTROM, False))): selector.BooleanSelector(),
        _opt(CONF_ZAEHLERNUMMER, d.get(CONF_ZAEHLERNUMMER)): selector.TextSelector(),
        _opt(CONF_MARKTLOKATION, d.get(CONF_MARKTLOKATION)): selector.TextSelector(),
        _opt(CONF_PREISGARANTIE, d.get(CONF_PREISGARANTIE)): selector.DateSelector(),
        _opt(CONF_VERBRAUCH_SENSOR, d.get(CONF_VERBRAUCH_SENSOR)): selector.EntitySelector(
            selector.EntitySelectorConfig(domain="sensor")
        ),
        **_tiered_fields(d, enabled=f.get("hat_tiered", True)),
        **_tag_nacht_fields(d, enabled=f.get("hat_tag_nacht", False)),
    })


def _pauschal_schema(d: dict[str, Any]) -> vol.Schema:
    return vol.Schema({
        vol.Required(CONF_ABSCHLAG, default=d.get(CONF_ABSCHLAG, 0.0)): _preis(),
        _opt(CONF_GRUNDPREIS, d.get(CONF_GRUNDPREIS)): _preis(),
    })


def _wasser_schema(d: dict[str, Any], features: dict | None = None) -> vol.Schema:
    f = features or {}
    if not d.get(CONF_ABWASSER_TYP):
        if f.get("hat_abwasser_prozent"):
            default_typ = ABWASSER_TYP_PROZENT
        elif f.get("hat_abwasser_pauschal"):
            default_typ = ABWASSER_TYP_PAUSCHAL
        else:
            default_typ = ABWASSER_TYP_PREIS
    else:
        default_typ = d[CONF_ABWASSER_TYP]
    return vol.Schema({
        vol.Required(CONF_WASSER_EINHEIT, default=d.get(CONF_WASSER_EINHEIT, "m³")): _select(WASSER_EINHEITEN),
        vol.Required(CONF_ARBEITSPREIS, default=d.get(CONF_ARBEITSPREIS, 0.0)): _preis(),
        vol.Required(CONF_GRUNDPREIS, default=d.get(CONF_GRUNDPREIS, 0.0)): _preis(),
        vol.Required(CONF_ABSCHLAG, default=d.get(CONF_ABSCHLAG, 0.0)): _preis(),
        vol.Required(CONF_ABWASSER_TYP, default=default_typ): _select(ABWASSER_TYPEN),
        _opt(CONF_ARBEITSPREIS_ABWASSER, d.get(CONF_ARBEITSPREIS_ABWASSER)): _preis(),
        _opt(CONF_JAHRESVERBRAUCH, d.get(CONF_JAHRESVERBRAUCH)): selector.NumberSelector(
            selector.NumberSelectorConfig(min=0, step="any", mode=selector.NumberSelectorMode.BOX)
        ),
        _opt(CONF_ZAEHLERNUMMER, d.get(CONF_ZAEHLERNUMMER)): selector.TextSelector(),
        _opt(CONF_VERBRAUCH_SENSOR, d.get(CONF_VERBRAUCH_SENSOR)): selector.EntitySelector(
            selector.EntitySelectorConfig(domain="sensor")
        ),
        **_tiered_fields(d, enabled=f.get("hat_tiered", True)),
    })


def _next_schema(d: dict[str, Any], *, energie: bool) -> vol.Schema:
    def k(b: str) -> str:
        return NEXT_PREFIX + b
    fields: dict[Any, Any] = {
        _opt(k(CONF_BEGINN), d.get(k(CONF_BEGINN))): selector.DateSelector(),
        _opt(k(CONF_ANBIETER), d.get(k(CONF_ANBIETER))): selector.TextSelector(),
        _opt(k(CONF_KUNDENNUMMER), d.get(k(CONF_KUNDENNUMMER))): selector.TextSelector(),
        _opt(k(CONF_TARIF), d.get(k(CONF_TARIF))): selector.TextSelector(),
    }
    if energie:
        fields[_opt(k(CONF_ARBEITSPREIS), d.get(k(CONF_ARBEITSPREIS)))] = _preis()
        fields[_opt(k(CONF_GRUNDPREIS), d.get(k(CONF_GRUNDPREIS)))] = _preis()
        fields[_opt(k(CONF_ABSCHLAG), d.get(k(CONF_ABSCHLAG)))] = _preis()
        fields[_opt(k(CONF_JAHRESVERBRAUCH), d.get(k(CONF_JAHRESVERBRAUCH)))] = _verbrauch()
    else:
        fields[_opt(k(CONF_ABSCHLAG), d.get(k(CONF_ABSCHLAG)))] = _preis()
        fields[_opt(k(CONF_GRUNDPREIS), d.get(k(CONF_GRUNDPREIS)))] = _preis()
    fields[_opt(k(CONF_ENDE), d.get(k(CONF_ENDE)))] = selector.DateSelector()
    return vol.Schema(fields)


# ------------------------------------------------------------------ flows

class TariffyConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}
        self._name: str = ""

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if user_input is not None:
            self._data = dict(user_input)
            self._name = self._data.pop("name", "")
            sparte = user_input[CONF_SPARTE]
            if sparte == GAS_SPARTE:
                return await self.async_step_gas()
            if sparte == WASSER_SPARTE:
                return await self.async_step_wasser()
            if sparte in ENERGIE_SPARTEN:
                return await self.async_step_energie()
            return await self.async_step_pauschal()
        return self.async_show_form(
            step_id="user",
            data_schema=_common_schema(self.hass, {}, mit_name=True),
        )

    async def async_step_energie(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(title=self._name, data={**self._data, **user_input})
        return self.async_show_form(
            step_id="energie",
            data_schema=_energie_schema({}, _country_features(self.hass)),
        )

    async def async_step_pauschal(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(title=self._name, data={**self._data, **user_input})
        return self.async_show_form(
            step_id="pauschal",
            data_schema=_pauschal_schema({}),
        )

    async def async_step_gas(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(title=self._name, data={**self._data, **user_input})
        return self.async_show_form(
            step_id="gas",
            data_schema=_gas_schema({}, _country_features(self.hass)),
        )

    async def async_step_wasser(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(title=self._name, data={**self._data, **user_input})
        return self.async_show_form(
            step_id="wasser",
            data_schema=_wasser_schema({}, _country_features(self.hass)),
        )

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        entry = self._get_reconfigure_entry()
        if user_input is not None:
            self._data = dict(user_input)
            sparte = user_input[CONF_SPARTE]
            if sparte == GAS_SPARTE:
                return await self.async_step_reconfigure_gas()
            if sparte == WASSER_SPARTE:
                return await self.async_step_reconfigure_wasser()
            if sparte in ENERGIE_SPARTEN:
                return await self.async_step_reconfigure_energie()
            return await self.async_step_reconfigure_pauschal()
        return self.async_show_form(
            step_id="reconfigure",
            data_schema=_common_schema(self.hass, dict(entry.data), mit_name=False),
        )

    async def async_step_reconfigure_energie(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        entry = self._get_reconfigure_entry()
        if user_input is not None:
            return self.async_update_reload_and_abort(entry, data={**self._data, **user_input})
        return self.async_show_form(
            step_id="reconfigure_energie",
            data_schema=_energie_schema(dict(entry.data), _country_features(self.hass)),
        )

    async def async_step_reconfigure_pauschal(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        entry = self._get_reconfigure_entry()
        if user_input is not None:
            return self.async_update_reload_and_abort(entry, data={**self._data, **user_input})
        return self.async_show_form(
            step_id="reconfigure_pauschal",
            data_schema=_pauschal_schema(dict(entry.data)),
        )

    async def async_step_reconfigure_gas(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        entry = self._get_reconfigure_entry()
        if user_input is not None:
            return self.async_update_reload_and_abort(entry, data={**self._data, **user_input})
        return self.async_show_form(
            step_id="reconfigure_gas",
            data_schema=_gas_schema(dict(entry.data), _country_features(self.hass)),
        )

    async def async_step_reconfigure_wasser(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        entry = self._get_reconfigure_entry()
        if user_input is not None:
            return self.async_update_reload_and_abort(entry, data={**self._data, **user_input})
        return self.async_show_form(
            step_id="reconfigure_wasser",
            data_schema=_wasser_schema(dict(entry.data), _country_features(self.hass)),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry) -> OptionsFlow:
        return TariffyOptionsFlow()


class TariffyOptionsFlow(OptionsFlow):
    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if user_input is not None:
            if not user_input.get(NEXT_PREFIX + CONF_BEGINN):
                return self.async_create_entry(title="", data={})
            return self.async_create_entry(
                title="",
                data={k: v for k, v in user_input.items() if v not in (None, "")},
            )
        energie = self.config_entry.data.get(CONF_SPARTE) in ENERGIE_SPARTEN
        return self.async_show_form(
            step_id="init",
            data_schema=_next_schema(dict(self.config_entry.options), energie=energie),
        )
