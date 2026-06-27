"""Config- und Options-Flow der Tariffy-Integration (sparten-abhängig)."""

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
    CONF_ABSCHLAG,
    CONF_ANBIETER,
    CONF_ARBEITSPREIS,
    CONF_BEGINN,
    CONF_BONUS,
    CONF_BRENNWERT,
    CONF_ENDE,
    CONF_ERINNERUNG_MONATE,
    CONF_GRUNDPREIS,
    CONF_JAHRESVERBRAUCH,
    CONF_KUNDENNUMMER,
    CONF_MARKTLOKATION,
    CONF_NOTIFY_TARGET,
    CONF_OEKOSTROM,
    CONF_PREISGARANTIE,
    CONF_SPARTE,
    CONF_TARIF,
    CONF_ZAEHLERNUMMER,
    CONF_ZUSTANDSZAHL,
    DOMAIN,
    ENERGIE_SPARTEN,
    ERINNERUNG_OPTIONS,
    GAS_SPARTE,
    NEXT_PREFIX,
    SPARTEN,
    VERBRAUCH_EINHEIT,
    VERBRAUCH_M3_EINHEIT,
)


# --------------------------------------------------------------------- helpers
def _opt(key: str, default: Any = None) -> vol.Optional:
    if default in (None, ""):
        return vol.Optional(key)
    return vol.Optional(key, description={"suggested_value": default})


def _preis(step=None) -> selector.NumberSelector:
    return selector.NumberSelector(
        selector.NumberSelectorConfig(
            min=0, step="any", mode=selector.NumberSelectorMode.BOX
        )
    )


def _verbrauch() -> selector.NumberSelector:
    return selector.NumberSelector(
        selector.NumberSelectorConfig(min=0, step="any",
            mode=selector.NumberSelectorMode.BOX,
            unit_of_measurement=VERBRAUCH_EINHEIT,
        )
    )


def _verbrauch_m3() -> selector.NumberSelector:
    return selector.NumberSelector(
        selector.NumberSelectorConfig(min=0, step="any",
            mode=selector.NumberSelectorMode.BOX,
            unit_of_measurement=VERBRAUCH_M3_EINHEIT,
        )
    )


def _select(options, translation_key=None, custom=False) -> selector.SelectSelector:
    return selector.SelectSelector(
        selector.SelectSelectorConfig(
            options=options,
            mode=selector.SelectSelectorMode.DROPDOWN,
            custom_value=custom,
        )
    )


def _notify_options(hass: HomeAssistant) -> list:
    dienste = sorted(hass.services.async_services().get("notify", {}))
    return [
        selector.SelectOptionDict(value=n, label=f"notify.{n}") for n in dienste
    ]


# ------------------------------------------------------------------- schemas
def _common_schema(
    hass: HomeAssistant, d: dict[str, Any], *, mit_name: bool
) -> vol.Schema:
    """Schritt 1: für alle Sparten gleich."""
    fields: dict[Any, Any] = {}
    if mit_name:
        # FIX: vol.Required mit leerem String-Default → vol.Optional ohne Default
        # verhindert den 400-Fehler beim Laden des Config-Flows
        fields[vol.Required("name")] = selector.TextSelector()
    fields[vol.Required(CONF_SPARTE, default=d.get(CONF_SPARTE, "strom"))] = _select(
        SPARTEN
    )
    # FIX: leerer String-Default durch vol.Optional ersetzt
    if d.get(CONF_ANBIETER):
        fields[vol.Required(CONF_ANBIETER, default=d[CONF_ANBIETER])] = selector.TextSelector()
    else:
        fields[vol.Required(CONF_ANBIETER)] = selector.TextSelector()
    fields[_opt(CONF_KUNDENNUMMER, d.get(CONF_KUNDENNUMMER))] = selector.TextSelector()
    fields[_opt(CONF_TARIF, d.get(CONF_TARIF))] = selector.TextSelector()
    fields[_opt(CONF_BEGINN, d.get(CONF_BEGINN))] = selector.DateSelector()
    fields[_opt(CONF_ENDE, d.get(CONF_ENDE))] = selector.DateSelector()
    fields[
        vol.Required(
            CONF_ERINNERUNG_MONATE, default=d.get(CONF_ERINNERUNG_MONATE, "3")
        )
    ] = _select(ERINNERUNG_OPTIONS)
    notify_options = _notify_options(hass)
    if notify_options:
        fields[_opt(CONF_NOTIFY_TARGET, d.get(CONF_NOTIFY_TARGET))] = _select(notify_options, custom=True)
    return vol.Schema(fields)


def _energie_schema(d: dict[str, Any]) -> vol.Schema:
    """Schritt 2 für Strom."""
    return vol.Schema(
        {
            vol.Required(
                CONF_ARBEITSPREIS, default=d.get(CONF_ARBEITSPREIS, 0.0)
            ): _preis(0.0001),
            vol.Required(
                CONF_GRUNDPREIS, default=d.get(CONF_GRUNDPREIS, 0.0)
            ): _preis(0.01),
            vol.Required(
                CONF_ABSCHLAG, default=d.get(CONF_ABSCHLAG, 0.0)
            ): _preis(0.01),
            _opt(CONF_JAHRESVERBRAUCH, d.get(CONF_JAHRESVERBRAUCH)): _verbrauch(),
            _opt(CONF_BONUS, d.get(CONF_BONUS)): _preis(0.01),
            vol.Required(
                CONF_OEKOSTROM, default=bool(d.get(CONF_OEKOSTROM, False))
            ): selector.BooleanSelector(),
            _opt(CONF_ZAEHLERNUMMER, d.get(CONF_ZAEHLERNUMMER)): selector.TextSelector(),
            _opt(
                CONF_MARKTLOKATION, d.get(CONF_MARKTLOKATION)
            ): selector.TextSelector(),
            _opt(CONF_PREISGARANTIE, d.get(CONF_PREISGARANTIE)): selector.DateSelector(),
        }
    )


def _gas_schema(d: dict[str, Any]) -> vol.Schema:
    """Schritt 2 für Gas (Verbrauch in m³ + Umrechnung auf kWh)."""
    return vol.Schema(
        {
            vol.Required(
                CONF_ARBEITSPREIS, default=d.get(CONF_ARBEITSPREIS, 0.0)
            ): _preis(0.0001),
            vol.Required(
                CONF_GRUNDPREIS, default=d.get(CONF_GRUNDPREIS, 0.0)
            ): _preis(0.01),
            vol.Required(
                CONF_ABSCHLAG, default=d.get(CONF_ABSCHLAG, 0.0)
            ): _preis(0.01),
            _opt(CONF_JAHRESVERBRAUCH, d.get(CONF_JAHRESVERBRAUCH)): _verbrauch_m3(),
            vol.Required(
                CONF_BRENNWERT, default=d.get(CONF_BRENNWERT, 11.0)
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(min=0, step="any", mode=selector.NumberSelectorMode.BOX
                )
            ),
            vol.Required(
                CONF_ZUSTANDSZAHL, default=d.get(CONF_ZUSTANDSZAHL, 0.95)
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(min=0, step="any", mode=selector.NumberSelectorMode.BOX
                )
            ),
            _opt(CONF_BONUS, d.get(CONF_BONUS)): _preis(0.01),
            vol.Required(
                CONF_OEKOSTROM, default=bool(d.get(CONF_OEKOSTROM, False))
            ): selector.BooleanSelector(),
            _opt(CONF_ZAEHLERNUMMER, d.get(CONF_ZAEHLERNUMMER)): selector.TextSelector(),
            _opt(
                CONF_MARKTLOKATION, d.get(CONF_MARKTLOKATION)
            ): selector.TextSelector(),
            _opt(CONF_PREISGARANTIE, d.get(CONF_PREISGARANTIE)): selector.DateSelector(),
        }
    )


def _pauschal_schema(d: dict[str, Any]) -> vol.Schema:
    """Schritt 2 für Pauschalverträge (Internet, Mobilfunk, …)."""
    return vol.Schema(
        {
            vol.Required(
                CONF_ABSCHLAG, default=d.get(CONF_ABSCHLAG, 0.0)
            ): _preis(0.01),
            _opt(CONF_GRUNDPREIS, d.get(CONF_GRUNDPREIS)): _preis(0.01),
        }
    )


def _next_schema(d: dict[str, Any], *, energie: bool) -> vol.Schema:
    def k(b: str) -> str:
        return NEXT_PREFIX + b

    fields: dict[Any, Any] = {
        _opt(k(CONF_BEGINN), d.get(k(CONF_BEGINN))): selector.DateSelector(),
        _opt(k(CONF_ANBIETER), d.get(k(CONF_ANBIETER))): selector.TextSelector(),
        _opt(
            k(CONF_KUNDENNUMMER), d.get(k(CONF_KUNDENNUMMER))
        ): selector.TextSelector(),
        _opt(k(CONF_TARIF), d.get(k(CONF_TARIF))): selector.TextSelector(),
    }
    if energie:
        fields[_opt(k(CONF_ARBEITSPREIS), d.get(k(CONF_ARBEITSPREIS)))] = _preis(0.0001)
        fields[_opt(k(CONF_GRUNDPREIS), d.get(k(CONF_GRUNDPREIS)))] = _preis(0.01)
        fields[_opt(k(CONF_ABSCHLAG), d.get(k(CONF_ABSCHLAG)))] = _preis(0.01)
        fields[_opt(k(CONF_JAHRESVERBRAUCH), d.get(k(CONF_JAHRESVERBRAUCH)))] = (
            _verbrauch()
        )
    else:
        fields[_opt(k(CONF_ABSCHLAG), d.get(k(CONF_ABSCHLAG)))] = _preis(0.01)
        fields[_opt(k(CONF_GRUNDPREIS), d.get(k(CONF_GRUNDPREIS)))] = _preis(0.01)
    fields[_opt(k(CONF_ENDE), d.get(k(CONF_ENDE)))] = selector.DateSelector()
    return vol.Schema(fields)


# ------------------------------------------------------------------- flows
class TariffyConfigFlow(ConfigFlow, domain=DOMAIN):
    """Anlegen eines Vertrags in zwei Schritten."""

    VERSION = 1

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if user_input is not None:
            self._data = dict(user_input)
            self._name = self._data.pop("name", "")
            if user_input[CONF_SPARTE] == GAS_SPARTE:
                return await self.async_step_gas()
            if user_input[CONF_SPARTE] in ENERGIE_SPARTEN:
                return await self.async_step_energie()
            return await self.async_step_pauschal()
        return self.async_show_form(
            step_id="user", data_schema=_common_schema(self.hass, {}, mit_name=True)
        )

    async def async_step_energie(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if user_input is not None:
            data = {**self._data, **user_input}
            return self.async_create_entry(title=self._name, data=data)
        return self.async_show_form(
            step_id="energie", data_schema=_energie_schema({})
        )

    async def async_step_pauschal(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if user_input is not None:
            data = {**self._data, **user_input}
            return self.async_create_entry(title=self._name, data=data)
        return self.async_show_form(
            step_id="pauschal", data_schema=_pauschal_schema({})
        )

    async def async_step_gas(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if user_input is not None:
            data = {**self._data, **user_input}
            name = data.pop("name")
            return self.async_create_entry(title=name, data=data)
        return self.async_show_form(step_id="gas", data_schema=_gas_schema({}))

    # ---- Reconfigure (gleiche Zwei-Schritt-Logik) ----
    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        entry = self._get_reconfigure_entry()
        if user_input is not None:
            self._data = dict(user_input)
            if user_input[CONF_SPARTE] == GAS_SPARTE:
                return await self.async_step_reconfigure_gas()
            if user_input[CONF_SPARTE] in ENERGIE_SPARTEN:
                return await self.async_step_reconfigure_energie()
            return await self.async_step_reconfigure_pauschal()
        return self.async_show_form(
            step_id="reconfigure",
            data_schema=_common_schema(self.hass, dict(entry.data), mit_name=False),
        )

    async def async_step_reconfigure_energie(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        entry = self._get_reconfigure_entry()
        if user_input is not None:
            return self.async_update_reload_and_abort(
                entry, data={**self._data, **user_input}
            )
        return self.async_show_form(
            step_id="reconfigure_energie",
            data_schema=_energie_schema(dict(entry.data)),
        )

    async def async_step_reconfigure_pauschal(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        entry = self._get_reconfigure_entry()
        if user_input is not None:
            return self.async_update_reload_and_abort(
                entry, data={**self._data, **user_input}
            )
        return self.async_show_form(
            step_id="reconfigure_pauschal",
            data_schema=_pauschal_schema(dict(entry.data)),
        )

    async def async_step_reconfigure_gas(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        entry = self._get_reconfigure_entry()
        if user_input is not None:
            return self.async_update_reload_and_abort(
                entry, data={**self._data, **user_input}
            )
        return self.async_show_form(
            step_id="reconfigure_gas",
            data_schema=_gas_schema(dict(entry.data)),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry) -> OptionsFlow:
        return TariffyOptionsFlow()


class TariffyOptionsFlow(OptionsFlow):
    """Den nächsten/zukünftigen Vertrag pflegen."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if user_input is not None:
            if not user_input.get(NEXT_PREFIX + CONF_BEGINN):
                return self.async_create_entry(title="", data={})
            cleaned = {
                key: val for key, val in user_input.items() if val not in (None, "")
            }
            return self.async_create_entry(title="", data=cleaned)
        energie = self.config_entry.data.get(CONF_SPARTE) in ENERGIE_SPARTEN
        return self.async_show_form(
            step_id="init",
            data_schema=_next_schema(dict(self.config_entry.options), energie=energie),
        )
