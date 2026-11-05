"""Tests for the cost / forecast calculation in TariffyCoordinator.

Each test sets up a real config entry in a Home Assistant test instance, with
the recorder queries replaced (see conftest.setup_contract), and asserts on the
coordinator data that the sensors are built from.
"""

from __future__ import annotations

import pytest
from homeassistant.core import HomeAssistant

SENSOR = "sensor.zaehler"
SENSOR_NT = "sensor.zaehler_nt"

STROM = {
    "sparte": "electricity",
    "anbieter": "Stadtwerke",
    "arbeitspreis": 0.2977,
    "grundpreis": 11.51,
    "abschlag": 40.0,
    "beginn": "2026-01-01",
    "ende": "2026-12-31",
    "verbrauch_sensor": SENSOR,
    "erinnerung_monate": "0",
}


class TestFourCostSensorsGoldenExample:
    """The worked example from the README (electricity contract, day 192)."""

    async def test_values_match_readme(self, setup_contract):
        _, d = await setup_contract(
            STROM,
            today="2026-07-12",
            latest=(2481.17, 2481.17),
            offset=(1000.0, 1000.0),
            sensor_states={SENSOR: "2481.17"},
        )
        assert d["verbrauch_bisher"] == pytest.approx(1481.17)
        assert d["kosten_bisher"] == pytest.approx(513.54, abs=0.02)
        assert d["guthaben_bisher"] == pytest.approx(-261.24, abs=0.02)
        assert d["verbrauch_hochgerechnet"] == pytest.approx(2808.1, abs=0.1)
        assert d["jahreskosten"] == pytest.approx(478.32, abs=0.02)
        assert d["prognose_real"] == pytest.approx(-495.29, abs=0.05)

    async def test_without_consumption_sensor_only_instalment_total(self, setup_contract):
        data = {k: v for k, v in STROM.items() if k != "verbrauch_sensor"}
        _, d = await setup_contract(data, today="2026-07-12")
        assert d["jahreskosten"] == pytest.approx(478.32, abs=0.02)
        assert d["verbrauch_bisher"] is None
        assert d["kosten_bisher"] is None
        assert d["guthaben_bisher"] is None
        assert d["prognose_real"] is None

    async def test_no_projection_on_first_day(self, setup_contract):
        _, d = await setup_contract(
            STROM,
            today="2026-01-01",
            latest=(1010.0, 1010.0),
            offset=(1000.0, 1000.0),
            sensor_states={SENSOR: "1010"},
        )
        assert d["verbrauch_bisher"] == 10.0
        assert d["verbrauch_hochgerechnet"] is None
        assert d["prognose_real"] is None
        assert d["kosten_bisher"] == pytest.approx(10 * 0.2977, abs=0.01)

    async def test_contract_without_end_projects_onto_365_days(self, setup_contract):
        data = {**STROM}
        del data["ende"]
        _, d = await setup_contract(
            data,
            today="2026-07-12",
            latest=(1192.0, 1192.0),
            offset=(1000.0, 1000.0),
            sensor_states={SENSOR: "1192"},
        )
        assert d["verbrauch_hochgerechnet"] == pytest.approx(192 / 192 * 365, abs=0.1)
        assert d["restlaufzeit"] is None

    async def test_changed_instalment_is_not_applied_retroactively(self, setup_contract):
        data = {
            **STROM,
            "abschlag": 60.0,
            "_abschlag_ab_datum": "2026-04-01",
            "_abschlag_vorheriger_wert": 40.0,
        }
        _, d = await setup_contract(
            data,
            today="2026-07-12",
            latest=(2481.17, 2481.17),
            offset=(1000.0, 1000.0),
            sensor_states={SENSOR: "2481.17"},
        )
        plain = 60.0 * (192 / 30.44)
        assert d["guthaben_bisher"] > d["kosten_bisher"] * -1 - plain  # sanity
        gezahlt = d["guthaben_bisher"] + d["kosten_bisher"]
        assert gezahlt < plain  # old, lower instalment applied before 2026-04-01
        assert gezahlt > 40.0 * (192 / 30.44)


class TestConsumptionTracking:
    async def test_manual_start_value_beats_statistics(self, setup_contract):
        data = {**STROM, "verbrauch_start_wert": 5000.0}
        _, d = await setup_contract(
            data,
            latest=(99999.0, 99999.0),
            offset=(1.0, 1.0),
            sensor_states={SENSOR: "5300.5"},
        )
        assert d["verbrauch_bisher"] == pytest.approx(300.5)

    async def test_meter_reset_is_handled_via_sum(self, setup_contract):
        _, d = await setup_contract(
            STROM,
            latest=(1050.0, 20.0),
            offset=(1000.0, 980.0),
            sensor_states={SENSOR: "20"},
        )
        # raw state fell below the start value -> use the sum delta
        assert d["verbrauch_bisher"] == pytest.approx(50.0)

    async def test_sum_glitch_is_ignored(self, setup_contract):
        _, d = await setup_contract(
            STROM,
            latest=(2000.0, 1100.4),
            offset=(1000.0, 1100.0),
            sensor_states={SENSOR: "1100.4"},
        )
        assert d["verbrauch_bisher"] == pytest.approx(0.4)

    async def test_unknown_when_no_statistics_and_sensor_unavailable(self, setup_contract):
        _, d = await setup_contract(
            STROM, sensor_states={SENSOR: "unavailable"}
        )
        assert d["verbrauch_bisher"] is None
        assert d["kosten_bisher"] is None


class TestGas:
    GAS = {
        "sparte": "gas",
        "arbeitspreis": 0.10,
        "grundpreis": 10.0,
        "abschlag": 80.0,
        "beginn": "2026-01-01",
        "ende": "2026-12-31",
        "verbrauch_sensor": SENSOR,
        "gas_einheit": "m³",
        "brennwert": "11.2",
        "zustandszahl": "0.95",
        "jahresverbrauch": 1000.0,
        "erinnerung_monate": "0",
    }

    async def test_annual_estimate_is_converted_to_kwh(self, setup_contract):
        _, d = await setup_contract(dict(self.GAS))
        assert d["verbrauch_kwh"] == pytest.approx(1000 * 11.2 * 0.95, abs=0.1)

    @pytest.mark.parametrize(("unit", "factor"), [("therm", 29.3071), ("MBtu", 293.071), ("kWh", 1.0)])
    async def test_fixed_factor_units_need_no_calorific_value(self, setup_contract, unit, factor):
        data = {**self.GAS, "gas_einheit": unit}
        del data["brennwert"]
        _, d = await setup_contract(data)
        assert d["verbrauch_kwh"] == pytest.approx(round(1000 * factor, 1))

    async def test_costs_use_kwh_but_consumption_stays_in_m3(self, setup_contract):
        _, d = await setup_contract(
            dict(self.GAS),
            today="2026-07-12",
            latest=(1100.0, 1100.0),
            offset=(1000.0, 1000.0),
            sensor_states={SENSOR: "1100"},
        )
        assert d["verbrauch_bisher"] == pytest.approx(100.0)  # raw m³
        monate = 192 / 30.44
        assert d["kosten_bisher"] == pytest.approx(
            100 * 11.2 * 0.95 * 0.10 + 10.0 * monate, abs=0.02
        )


class TestWater:
    WATER = {
        "sparte": "water",
        "arbeitspreis": 2.0,
        "grundpreis": 5.0,
        "abschlag": 30.0,
        "beginn": "2026-01-01",
        "ende": "2026-12-31",
        "erinnerung_monate": "0",
    }

    async def test_fixed_wastewater_price_is_added(self, setup_contract):
        _, d = await setup_contract(
            {**self.WATER, "abwasser_typ": "price_per_unit", "arbeitspreis_abwasser": 3.0}
        )
        assert d["arbeitspreis_gesamt_wasser"] == pytest.approx(5.0)

    async def test_percentage_wastewater(self, setup_contract):
        _, d = await setup_contract(
            {**self.WATER, "abwasser_typ": "percentage", "arbeitspreis_abwasser": 80.0}
        )
        assert d["arbeitspreis_abwasser"] == pytest.approx(1.6)
        assert d["arbeitspreis_gesamt_wasser"] == pytest.approx(3.6)

    async def test_flat_rate_leaves_unit_price_unchanged(self, setup_contract):
        _, d = await setup_contract(
            {**self.WATER, "abwasser_typ": "flat_rate", "arbeitspreis_abwasser": 12.0}
        )
        assert d["abwasser_pauschal_monat"] == 12.0
        assert d["arbeitspreis_gesamt_wasser"] == pytest.approx(2.0)

    async def test_total_price_drives_costs(self, setup_contract):
        data = {
            **self.WATER,
            "abwasser_typ": "price_per_unit",
            "arbeitspreis_abwasser": 3.0,
            "verbrauch_sensor": SENSOR,
        }
        _, d = await setup_contract(
            data,
            today="2026-07-12",
            latest=(150.0, 150.0),
            offset=(100.0, 100.0),
            sensor_states={SENSOR: "150"},
        )
        assert d["kosten_bisher"] == pytest.approx(50 * 5.0 + 5.0 * (192 / 30.44), abs=0.02)


class TestDualTariff:
    HT_NT = {
        **STROM,
        "sparte": "electricity_ht_nt",
        "arbeitspreis": 0.30,
        "arbeitspreis_nt": 0.20,
        "verbrauch_sensor_nt": SENSOR_NT,
    }

    async def test_registers_are_summed_with_weighted_price(self, setup_contract):
        _, d = await setup_contract(
            dict(self.HT_NT),
            today="2026-07-12",
            latest=(1300.0, 1300.0),
            offset=(1000.0, 1000.0),
            latest_nt=(800.0, 800.0),
            offset_nt=(500.0, 500.0),
            sensor_states={SENSOR: "1300", SENSOR_NT: "800"},
        )
        assert d["verbrauch_bisher_ht"] == pytest.approx(300.0)
        assert d["verbrauch_bisher_nt"] == pytest.approx(300.0)
        assert d["verbrauch_bisher"] == pytest.approx(600.0)
        assert d["arbeitspreis"] == pytest.approx(0.25)  # (300*.30 + 300*.20) / 600
        assert d["arbeitspreis_ht"] == pytest.approx(0.30)
        assert d["kosten_ht_bisher"] == pytest.approx(90.0)
        assert d["kosten_nt_bisher"] == pytest.approx(60.0)

    async def test_nt_register_missing_keeps_ht_price(self, setup_contract):
        data = {k: v for k, v in self.HT_NT.items() if k != "verbrauch_sensor_nt"}
        _, d = await setup_contract(
            data,
            latest=(1300.0, 1300.0),
            offset=(1000.0, 1000.0),
            sensor_states={SENSOR: "1300"},
        )
        assert d["verbrauch_bisher"] == pytest.approx(300.0)
        assert d["verbrauch_bisher_nt"] is None
        assert d["arbeitspreis"] == pytest.approx(0.30)


class TestPricing:
    async def test_dynamic_tariff_uses_average_plus_markup(self, setup_contract):
        data = {**STROM, "arbeitspreis_sensor": "sensor.spot", "arbeitspreis_aufschlag": 0.05}
        _, d = await setup_contract(
            data, average_price=0.20, sensor_states={"sensor.spot": "0.31"}
        )
        assert d["arbeitspreis"] == pytest.approx(0.25)
        assert d["arbeitspreis_aktuell"] == pytest.approx(0.36)

    async def test_dynamic_tariff_falls_back_to_manual_price_without_history(self, setup_contract):
        data = {**STROM, "arbeitspreis_sensor": "sensor.spot", "arbeitspreis_aufschlag": 0.05}
        _, d = await setup_contract(
            data, average_price=None, sensor_states={"sensor.spot": "0.31"}
        )
        assert d["arbeitspreis"] == pytest.approx(0.2977)

    async def test_tiered_pricing(self, setup_contract):
        data = {
            **STROM,
            "tiered": True,
            "tier_limit_0": "1000",
            "tier_price_0": "0.10",
            "tier_price_1": "0.20",
            "jahresverbrauch": 1500.0,
        }
        _, d = await setup_contract(data)
        assert d["tiered_jahreskosten"] == pytest.approx(1000 * 0.10 + 500 * 0.20)
        assert d["effektiver_arbeitspreis"] == pytest.approx(200.0 / 1500.0, abs=1e-6)

    async def test_day_night_costs(self, setup_contract):
        data = {
            **STROM,
            "arbeitspreis": 0.30,
            "arbeitspreis_nacht": 0.10,
            "jahresverbrauch_tag": 2000.0,
            "jahresverbrauch_nacht": 1000.0,
        }
        _, d = await setup_contract(data)
        assert d["hat_tag_nacht"] is True
        assert d["tou_jahreskosten"] == pytest.approx(2000 * 0.30 + 1000 * 0.10)


class TestRecommendations:
    async def test_instalment_adjustment_balances_to_contract_end(self, setup_contract):
        _, d = await setup_contract(
            STROM,
            today="2026-07-12",
            latest=(2481.17, 2481.17),
            offset=(1000.0, 1000.0),
            sensor_states={SENSOR: "2481.17"},
        )
        # paying the recommended instalment for the remaining term closes the gap
        rest_monate = 364 / 30.44 - 192 / 30.44
        gezahlt = 40.0 * (192 / 30.44)
        projected_cost = d["jahreskosten"] - d["prognose_real"]
        assert d["abschlag_anpassung_empfohlen"] * rest_monate + gezahlt == pytest.approx(
            projected_cost, abs=0.05
        )

    async def test_recommended_instalment_from_frozen_last_period(self, setup_contract):
        data = {
            **STROM,
            "verbrauch_letzte_laufzeit": 3000.0,
            "verbrauch_letzte_laufzeit_monate": 12.0,
        }
        _, d = await setup_contract(data)
        assert d["empfohlener_abschlag"] == pytest.approx((3000 * 0.2977 + 11.51 * 12) / 12, abs=0.01)

    async def test_recommended_instalment_defaults_to_12_months(self, setup_contract):
        data = {**STROM, "verbrauch_letzte_laufzeit": 1200.0}
        _, d = await setup_contract(data)
        assert d["empfohlener_abschlag"] == pytest.approx((1200 * 0.2977 + 11.51 * 12) / 12, abs=0.01)


class TestTariffSwitch:
    OPTIONS = {
        "next_beginn": "2026-07-01",
        "next_ende": "2027-06-30",
        "next_anbieter": "Neuer Anbieter",
        "next_arbeitspreis": 0.25,
        "next_abschlag": 55.0,
    }

    async def test_switch_on_due_date_promotes_next_contract(self, setup_contract):
        entry, d = await setup_contract(
            STROM,
            today="2026-07-12",
            options=dict(self.OPTIONS),
            latest=(2481.17, 2481.17),
            offset=(1000.0, 1000.0),
            sensor_states={SENSOR: "2481.17"},
        )
        assert entry.data["anbieter"] == "Neuer Anbieter"
        assert entry.data["arbeitspreis"] == 0.25
        assert entry.data["beginn"] == "2026-07-01"
        assert entry.data["verbrauch_sensor"] == SENSOR  # kept: next value empty
        assert entry.options == {}
        assert d["wechsel"] is None

    async def test_consumption_of_ended_period_is_frozen(self, contract):
        # Normal operation: earlier refreshes have cached the start-of-contract
        # meter value, the switch then happens on the due date.
        await contract.setup(
            STROM,
            today="2026-06-30",
            options=dict(self.OPTIONS, next_beginn="2026-07-01"),
            latest=(2000.0, 2000.0),
            offset=(1000.0, 1000.0),
            sensor_states={SENSOR: "2000"},
        )
        assert contract.entry.data["anbieter"] == "Stadtwerke"
        contract.values["latest"] = (2481.17, 2481.17)
        contract.hass.states.async_set(SENSOR, "2481.17")
        await contract.advance_to("2026-07-12")
        entry = contract.entry
        assert entry.data["anbieter"] == "Neuer Anbieter"
        assert entry.data["verbrauch_letzte_laufzeit"] == pytest.approx(1481.17)
        assert entry.data["verbrauch_letzte_laufzeit_monate"] == pytest.approx(
            192 / 30.44, abs=0.01
        )

    @pytest.mark.xfail(
        strict=True,
        reason=(
            "Known limitation: when the switch falls into the very first refresh "
            "after a Home Assistant start, the contract-start meter value is not "
            "cached yet and the consumption of the ended period is not frozen."
        ),
    )
    async def test_consumption_is_frozen_on_cold_start_switch(self, setup_contract):
        entry, _ = await setup_contract(
            STROM,
            today="2026-07-12",
            options=dict(self.OPTIONS),
            latest=(2481.17, 2481.17),
            offset=(1000.0, 1000.0),
            sensor_states={SENSOR: "2481.17"},
        )
        assert entry.data["verbrauch_letzte_laufzeit"] == pytest.approx(1481.17)

    async def test_future_switch_date_changes_nothing(self, setup_contract):
        options = {**self.OPTIONS, "next_beginn": "2027-01-01"}
        entry, d = await setup_contract(STROM, today="2026-07-12", options=options)
        assert entry.data["anbieter"] == "Stadtwerke"
        assert entry.options["next_beginn"] == "2027-01-01"
        assert d["wechsel"].isoformat() == "2027-01-01"

    async def test_old_sparte_values_are_migrated(self, setup_contract):
        entry, d = await setup_contract({**STROM, "sparte": "strom"})
        assert d["sparte"] == "electricity"
        assert entry.data["sparte"] == "electricity"


class TestCancellationReminder:
    DATA = {**STROM, "ende": "2026-09-30", "erinnerung_monate": "3"}

    async def test_active_inside_reminder_window(self, setup_contract, hass: HomeAssistant):
        _, d = await setup_contract(self.DATA, today="2026-07-01")
        assert d["erinnerung_datum"].isoformat() == "2026-06-30"
        assert d["erinnerung_aktiv"] is True
        notifications = hass.data["persistent_notification"]
        assert any(key.startswith("tariffy_kuendigung_") for key in notifications)

    async def test_not_active_before_window(self, setup_contract):
        _, d = await setup_contract(self.DATA, today="2026-06-29")
        assert d["erinnerung_aktiv"] is False

    async def test_not_active_after_contract_end(self, setup_contract):
        _, d = await setup_contract(self.DATA, today="2026-10-01")
        assert d["erinnerung_aktiv"] is False

    async def test_disabled_with_zero_months(self, setup_contract):
        _, d = await setup_contract({**self.DATA, "erinnerung_monate": "0"}, today="2026-07-01")
        assert d["erinnerung_datum"] is None
        assert d["erinnerung_aktiv"] is False

    async def test_confirmed_reminder_is_inactive(self, setup_contract):
        _, d = await setup_contract({**self.DATA, "_kuendigung_bestaetigt": True}, today="2026-07-01")
        assert d["erinnerung_aktiv"] is False

    async def test_remaining_days(self, setup_contract):
        _, d = await setup_contract(self.DATA, today="2026-09-20")
        assert d["restlaufzeit"] == 10


class TestInstalmentWarning:
    # consumption makes prognose_real about -495 (see golden example)
    DATA = {**STROM, "abschlag_warnung": True, "abschlag_warnung_schwelle": 50.0}
    KWARGS = {
        "today": "2026-07-12",
        "latest": (2481.17, 2481.17),
        "offset": (1000.0, 1000.0),
        "sensor_states": {SENSOR: "2481.17"},
    }

    async def test_warns_when_forecast_exceeds_threshold(self, setup_contract):
        _, d = await setup_contract(self.DATA, **self.KWARGS)
        assert d["abschlag_warnung_aktiv"] is True
        assert d["abschlag_warnung_zu_bestaetigen"] is True

    async def test_threshold_is_respected(self, setup_contract):
        data = {**self.DATA, "abschlag_warnung_schwelle": 1000.0}
        _, d = await setup_contract(data, **self.KWARGS)
        assert d["abschlag_warnung_aktiv"] is False

    async def test_off_by_default(self, setup_contract):
        _, d = await setup_contract(STROM, **self.KWARGS)
        assert d["abschlag_warnung_aktiv"] is False

    async def test_acknowledged_warning_stays_active_but_not_pending(self, setup_contract):
        data = {**self.DATA, "_abschlag_warnung_bestaetigt": True}
        _, d = await setup_contract(data, **self.KWARGS)
        assert d["abschlag_warnung_aktiv"] is True
        assert d["abschlag_warnung_zu_bestaetigen"] is False

    async def test_flags_are_reset_once_forecast_recovers(self, setup_contract):
        data = {
            **self.DATA,
            "abschlag": 200.0,  # instalments now cover the projected cost
            "_abschlag_warnung_bestaetigt": True,
            "_abschlag_warnung_notify_gesendet": True,
        }
        entry, d = await setup_contract(data, **self.KWARGS)
        assert d["abschlag_warnung_aktiv"] is False
        assert entry.data["_abschlag_warnung_bestaetigt"] is False
        assert entry.data["_abschlag_warnung_notify_gesendet"] is False


class TestSensorSetAfterSwitch:
    """Regression: since 1.26.3 the entry was no longer reloaded after a tariff
    switch, so sensors that only exist for some contracts (tiered pricing, night
    rate) were not created for the new contract until Home Assistant restarted.
    """

    NEXT = {
        "next_beginn": "2026-07-01",
        "next_ende": "2027-06-30",
        "next_tiered": True,
        "next_tier_limits": [1000.0],
        "next_tier_prices": [0.10, 0.20],
        "next_jahresverbrauch": 1500.0,
    }

    def _tiered_sensor(self, hass: HomeAssistant, entry):
        from homeassistant.helpers import entity_registry as er

        return er.async_get(hass).async_get_entity_id(
            "sensor", "tariffy", f"{entry.entry_id}_effektiver_arbeitspreis"
        )

    async def test_new_sensors_exist_after_switch(self, contract, hass: HomeAssistant):
        entry, d = await contract.setup(
            STROM,
            today="2026-06-30",
            options=dict(self.NEXT),
            latest=(1100.0, 1100.0),
            offset=(1000.0, 1000.0),
            sensor_states={SENSOR: "1100"},
        )
        assert d["ist_tiered"] is False
        assert self._tiered_sensor(hass, entry) is None

        await contract.advance_to("2026-07-12")

        assert entry.data["tiered"] is True
        assert entry.options == {}
        assert entry.runtime_data.data["ist_tiered"] is True
        assert self._tiered_sensor(hass, entry) is not None

    async def test_manual_switch_button_rebuilds_sensors_too(self, contract, hass: HomeAssistant):
        entry, _ = await contract.setup(
            STROM,
            today="2026-06-30",
            options=dict(self.NEXT, next_beginn="2027-01-01"),
            latest=(1100.0, 1100.0),
            offset=(1000.0, 1000.0),
            sensor_states={SENSOR: "1100"},
        )
        assert self._tiered_sensor(hass, entry) is None

        await entry.runtime_data.async_force_switch()
        await hass.async_block_till_done()

        assert entry.data["tiered"] is True
        assert self._tiered_sensor(hass, entry) is not None
