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
    CONF_ABWASSER_TYP,
    ABWASSER_TYPEN,
    ABWASSER_TYP_PREIS,
    ABWASSER_TYP_PROZENT,
    ABWASSER_TYP_PAUSCHAL,
    CONF_ARBEITSPREIS_ABWASSER,
    CONF_GAS_EINHEIT,
    CONF_ARBEITSPREIS_NACHT,
    CONF_EINSPEISEVERGUETUNG,
    CONF_EINSPEISUNG_SENSOR,
    CONF_JAHRESVERBRAUCH_NACHT,
    CONF_JAHRESVERBRAUCH_TAG,

    CONF_TIERED,
    CONF_TIER_LIMITS,
    CONF_TIER_PRICES,
    LAENDER_TAG_NACHT,
    LAENDER_TIERED,
    LAENDER_ABWASSER_PROZENT,
    LAENDER_ABWASSER_PAUSCHAL,
    MAX_TIERS,
    CONF_VERBRAUCH_SENSOR,
    CONF_WASSER_EINHEIT,
    DOMAIN,
    ENERGIE_SPARTEN,
    ERINNERUNG_OPTIONS,
    GAS_EINHEITEN,
    GAS_SPARTE,
    NEXT_PREFIX,
    SPARTEN,
    VERBRAUCH_EINHEIT,
    VERBRAUCH_M3_EINHEIT,
    WASSER_EINHEITEN,
    WASSER_SPARTE,
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


def _country_features(hass) -> dict:
    """Gibt länderspezifische Feature-Flags zurück."""
    country = (hass.config.country or "").upper()
    return {
        "hat_tag_nacht": country in LAENDER_TAG_NACHT,
        "hat_tiered": country in LAENDER_TIERED,
        "hat_abwasser_prozent": country in LAENDER_ABWASSER_PROZENT,
        "hat_abwasser_pauschal": country in LAENDER_ABWASSER_PAUSCHAL,
        "hat_einspeisung": True,  # feed-in tariff available worldwide
        "country": country,
    }


def _einspeisung_fields(d: dict, enabled: bool = True) -> dict:
    """Einspeiseverguetung-Felder — optional, nur Strom."""
    if not enabled:
        return {}
    return {
        _opt(CONF_EINSPEISEVERGUETUNG, d.get(CONF_EINSPEISEVERGUETUNG)): _preis(None),
        _opt(CONF_EINSPEISUNG_SENSOR, d.get(CONF_EINSPEISUNG_SENSOR)): selector.EntitySelector(
            selector.EntitySelectorConfig(domain="sensor")
        ),
    }


def _tiered_fields(d: dict, enabled: bool = True) -> dict:
    """Gibt Staffelpreis-Felder zurück — nur wenn im Land verfügbar."""
    if not enabled:
        return {}
    fields: dict = {}
    fields[vol.Required(CONF_TIERED, default=bool(d.get(CONF_TIERED, False)))] = (
        selector.BooleanSelector()
    )
    limits = d.get(CONF_TIER_LIMITS) or []
    prices = d.get(CONF_TIER_PRICES) or []
    for i in range(MAX_TIERS):
        limit_key = f"tier_limit_{i}"
        price_key = f"tier_price_{i}"
        default_limit = limits[i] if i < len(limits) else None
        default_price = prices[i] if i < len(prices) else None
        fields[_opt(limit_key, default_limit)] = selector.NumberSelector(
            selector.NumberSelectorConfig(min=0, step="any", mode=selector.NumberSelectorMode.BOX)
        )
        fields[_opt(price_key, default_price)] = selector.NumberSelector(
            selector.NumberSelectorConfig(min=0, step="any", mode=selector.NumberSelectorMode.BOX)
        )
    return fields


def _tag_nacht_fields(d: dict, enabled: bool = True) -> dict:
    """Tag/Nacht-Felder (Economy 7, TOU) — nur wenn im Land verfügbar."""
    if not enabled:
        return {}
    return {
        _opt(CONF_ARBEITSPREIS_NACHT, d.get(CONF_ARBEITSPREIS_NACHT)): _preis(None),
        _opt(CONF_JAHRESVERBRAUCH_TAG, d.get(CONF_JAHRESVERBRAUCH_TAG)): selector.NumberSelector(
            selector.NumberSelectorConfig(min=0, step="any", mode=selector.NumberSelectorMode.BOX)
        ),
        _opt(CONF_JAHRESVERBRAUCH_NACHT, d.get(CONF_JAHRESVERBRAUCH_NACHT)): selector.NumberSelector(
            selector.NumberSelectorConfig(min=0, step="any", mode=selector.NumberSelectorMode.BOX)
        ),
    }


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
            _opt(CONF_VERBRAUCH_SENSOR, d.get(CONF_VERBRAUCH_SENSOR)): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor")
            ),
            **_tiered_fields(d),
        }
    )


def _gas_schema(d: dict[str, Any], features: dict | None = None) -> vol.Schema:
    """Schritt 2 für Gas."""
    f = features or {}
    return vol.Schema(
        {
            vol.Required(
                CONF_GAS_EINHEIT, default=d.get(CONF_GAS_EINHEIT, "m³")
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=GAS_EINHEITEN,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
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
            _opt(CONF_VERBRAUCH_SENSOR, d.get(CONF_VERBRAUCH_SENSOR)): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor")
            ),
            **_tiered_fields(d, enabled=f.get("hat_tiered", True)),
            **_tag_nacht_fields(d, enabled=f.get("hat_tag_nacht", False)),
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


def _wasser_schema(d: dict[str, Any], features: dict | None = None) -> vol.Schema:
    """Schritt 2 für Wasser (Frischwasser + optionales Abwasser, international)."""
    f = features or {}
    # Abwasser-Typ: länderspezifisch vorauswählen
    if not d.get(CONF_ABWASSER_TYP):
        if f.get("hat_abwasser_prozent"):
            default_typ = ABWASSER_TYP_PROZENT
        elif f.get("hat_abwasser_pauschal"):
            default_typ = ABWASSER_TYP_PAUSCHAL
        else:
            default_typ = ABWASSER_TYP_PREIS
    else:
        default_typ = d[CONF_ABWASSER_TYP]
    abwasser_typ = default_typ
    return vol.Schema(
        {
            vol.Required(
                CONF_WASSER_EINHEIT, default=d.get(CONF_WASSER_EINHEIT, "m³")
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=WASSER_EINHEITEN,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                CONF_ARBEITSPREIS, default=d.get(CONF_ARBEITSPREIS, 0.0)
            ): _preis(None),
            vol.Required(
                CONF_GRUNDPREIS, default=d.get(CONF_GRUNDPREIS, 0.0)
            ): _preis(None),
            vol.Required(
                CONF_ABSCHLAG, default=d.get(CONF_ABSCHLAG, 0.0)
            ): _preis(None),
            # Abwasser-Typ wählen
            vol.Required(
                CONF_ABWASSER_TYP, default=default_typ
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=ABWASSER_TYPEN,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            # Abwasser-Wert: Bedeutung abhängig vom Typ
            # price_per_unit: Preis/Einheit | percentage: % | flat_rate: €/Monat
            _opt(CONF_ARBEITSPREIS_ABWASSER, d.get(CONF_ARBEITSPREIS_ABWASSER)): _preis(None),
            _opt(CONF_JAHRESVERBRAUCH, d.get(CONF_JAHRESVERBRAUCH)): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0, step="any", mode=selector.NumberSelectorMode.BOX
                )
            ),
            _opt(CONF_ZAEHLERNUMMER, d.get(CONF_ZAEHLERNUMMER)): selector.TextSelector(),
            _opt(CONF_VERBRAUCH_SENSOR, d.get(CONF_VERBRAUCH_SENSOR)): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor")
            ),
            **_tiered_fields(d, enabled=f.get("hat_tiered", True)),
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
            if user_input[CONF_SPARTE] == WASSER_SPARTE:
                return await self.async_step_wasser()
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
        return self.async_show_form(
            step_id="gas",
            data_schema=_gas_schema({}, _country_features(self.hass))
        )

    async def async_step_wasser(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if user_input is not None:
            data = {**self._data, **user_input}
            name = data.pop("name")
            return self.async_create_entry(title=name, data=data)
        return self.async_show_form(
            step_id="wasser",
            data_schema=_wasser_schema({}, _country_features(self.hass))
        )

    # ---- Reconfigure (gleiche Zwei-Schritt-Logik) ----
    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        entry = self._get_reconfigure_entry()
        if user_input is not None:
            self._data = dict(user_input)
            if user_input[CONF_SPARTE] == GAS_SPARTE:
                return await self.async_step_reconfigure_gas()
            if user_input[CONF_SPARTE] == WASSER_SPARTE:
                return await self.async_step_reconfigure_wasser()
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
            data_schema=_energie_schema(dict(entry.data), _country_features(self.hass)),
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
            data_schema=_gas_schema(dict(entry.data), _country_features(self.hass)),
        )

    async def async_step_reconfigure_wasser(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        entry = self._get_reconfigure_entry()
        if user_input is not None:
            return self.async_update_reload_and_abort(
                entry, data={**self._data, **user_input}
            )
        return self.async_show_form(
            step_id="reconfigure_wasser",
            data_schema=_wasser_schema(dict(entry.data), _country_features(self.hass)),
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
