"""Tests for the cost / forecast calculation in TariffyCoordinator.

Each test sets up a real config entry in a Home Assistant test instance, with
the recorder queries replaced (see conftest.setup_contract), and asserts on the
coordinator data that the sensors are built from.
"""

from __future__ import annotations

from datetime import date

import pytest
from homeassistant.core import HomeAssistant

GOLDEN_KW = {
    "today": "2026-07-12",
    "latest": (2481.17, 2481.17),
    "offset": (1000.0, 1000.0),
    "sensor_states": {"sensor.zaehler": "2481.17"},
}
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


T_MONATE = 364 / 30.44  # 2026-01-01 .. 2026-12-31
T_BISHER = 192 / 30.44  # until 2026-07-12


class TestForecastAfterInstalmentChange:
    """Raised from 40 to 100 EUR on 2026-05-01: the end forecast must count the
    older, lower instalment, exactly like "balance so far" does."""

    CHANGED = {**STROM, "abschlag": 100.0, "_abschlag_ab_datum": "2026-05-01", "_abschlag_vorheriger_wert": 40.0}

    @staticmethod
    def _projected_cost(d):
        return round(d["verbrauch_hochgerechnet"] * 0.2977 + 11.51 * T_MONATE, 2)

    async def test_forecast_counts_the_instalments_really_paid(self, setup_contract):
        _, d = await setup_contract(self.CHANGED, **GOLDEN_KW)
        monate_alt = 120 / 30.44
        gezahlt = 40.0 * monate_alt + 100.0 * (T_BISHER - monate_alt)
        erwartet = gezahlt + 100.0 * (T_MONATE - T_BISHER) - self._projected_cost(d)
        assert d["prognose_real"] == pytest.approx(erwartet, abs=0.05)
        # before the fix this showed +222.19 although the balance so far is negative
        assert d["guthaben_bisher"] < 0
        assert d["prognose_real"] < 100

    async def test_forecast_and_balance_so_far_are_consistent(self, setup_contract):
        _, d = await setup_contract(self.CHANGED, **GOLDEN_KW)
        rest = T_MONATE - T_BISHER
        # end = balance so far + instalments still to pay - cost still to come
        erwartet = d["guthaben_bisher"] + 100.0 * rest - (self._projected_cost(d) - d["kosten_bisher"])
        assert d["prognose_real"] == pytest.approx(erwartet, abs=0.05)

    async def test_instalment_total_stays_the_plain_payment_plan(self, setup_contract):
        _, d = await setup_contract(self.CHANGED, **GOLDEN_KW)
        assert d["jahreskosten"] == pytest.approx(100.0 * T_MONATE, abs=0.01)

    async def test_warning_uses_the_corrected_forecast(self, setup_contract):
        data = {**self.CHANGED, "abschlag_warnung": True, "abschlag_warnung_schwelle": 10.0}
        _, d = await setup_contract(data, **GOLDEN_KW)
        assert d["prognose_real"] < -10
        assert d["abschlag_warnung_aktiv"] is True


class TestForecastWithoutInstalmentChangeIsUnchanged:
    """The forecast of contracts whose instalment was never changed must stay
    exactly instalment x term - projected cost."""

    @staticmethod
    def _alt(d, abschlag, monate):
        kosten = round(d["verbrauch_hochgerechnet"] * 0.2977 + 11.51 * monate, 2)
        return round(round(abschlag * monate, 2) - kosten, 2)

    async def test_fixed_term(self, setup_contract):
        _, d = await setup_contract(STROM, **GOLDEN_KW)
        assert d["prognose_real"] == self._alt(d, 40.0, T_MONATE)

    async def test_contract_without_end_date_older_than_a_year(self, setup_contract):
        data = {**STROM, "beginn": "2025-01-01"}
        del data["ende"]
        _, d = await setup_contract(
            data, today="2026-07-12", latest=(2481.17, 2481.17), offset=(1000.0, 1000.0),
            sensor_states={SENSOR: "2481.17"},
        )
        assert d["prognose_real"] == self._alt(d, 40.0, 12.0)

    async def test_odd_amounts_and_dates(self, setup_contract):
        data = {**STROM, "abschlag": 37.77, "beginn": "2026-02-17", "ende": "2027-02-16"}
        _, d = await setup_contract(
            data, today="2026-08-03", latest=(1800.0, 1800.0), offset=(1000.0, 1000.0),
            sensor_states={SENSOR: "1800"},
        )
        monate = (date(2027, 2, 16) - date(2026, 2, 17)).days / 30.44
        assert d["prognose_real"] == self._alt(d, 37.77, monate)


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

    async def test_manual_start_value_survives_unavailable_meter(self, setup_contract):
        data = {**STROM, "verbrauch_start_wert": 5000.0}
        _, d = await setup_contract(
            data,
            latest=(5300.5, 5300.5),
            offset=(1.0, 1.0),
            sensor_states={SENSOR: "unavailable"},
        )
        # live state missing -> last recorded statistics state is used
        assert d["verbrauch_bisher"] == pytest.approx(300.5)

    async def test_manual_start_value_unknown_without_any_reading(self, setup_contract):
        data = {**STROM, "verbrauch_start_wert": 5000.0}
        _, d = await setup_contract(
            data, sensor_states={SENSOR: "unavailable"}
        )
        assert d["verbrauch_bisher"] is None

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


class TestManualStartValueWithUnavailableMeter:
    """Issue #46: a meter that is briefly unavailable must not turn the
    consumption sensors unknown, in every contract type."""

    async def test_gas(self, setup_contract):
        data = {**TestGas.GAS, "verbrauch_start_wert": 1000.0}
        _, d = await setup_contract(
            data,
            today="2026-07-12",
            latest=(1100.0, 1100.0),
            offset=(1.0, 1.0),
            sensor_states={SENSOR: "unavailable"},
        )
        assert d["verbrauch_bisher"] == pytest.approx(100.0)
        assert d["guthaben_bisher"] is not None

    async def test_water(self, setup_contract):
        data = {**TestWater.WATER, "verbrauch_sensor": SENSOR, "verbrauch_start_wert": 148.0}
        _, d = await setup_contract(
            data,
            today="2026-07-12",
            latest=(211.5663, 211.5663),
            offset=(1.0, 1.0),
            sensor_states={SENSOR: "unavailable"},
        )
        assert d["verbrauch_bisher"] == pytest.approx(63.57)
        assert d["guthaben_bisher"] is not None

    async def test_dual_tariff_both_registers(self, setup_contract):
        data = {
            **TestDualTariff.HT_NT,
            "verbrauch_start_wert": 1000.0,
            "verbrauch_start_wert_nt": 500.0,
        }
        _, d = await setup_contract(
            data,
            today="2026-07-12",
            latest=(1300.0, 1300.0),
            offset=(1.0, 1.0),
            latest_nt=(800.0, 800.0),
            offset_nt=(1.0, 1.0),
            sensor_states={SENSOR: "unavailable", SENSOR_NT: "unknown"},
        )
        assert d["verbrauch_bisher_ht"] == pytest.approx(300.0)
        assert d["verbrauch_bisher_nt"] == pytest.approx(300.0)
        assert d["verbrauch_bisher"] == pytest.approx(600.0)


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

    async def test_consumption_is_frozen_on_cold_start_switch(self, setup_contract):
        # The switch falls into the very first refresh after a Home Assistant
        # start: the contract-start meter value is not cached yet.
        entry, _ = await setup_contract(
            STROM,
            today="2026-07-12",
            options=dict(self.OPTIONS),
            latest=(2481.17, 2481.17),
            offset=(1000.0, 1000.0),
            sensor_states={SENSOR: "2481.17"},
        )
        assert entry.data["verbrauch_letzte_laufzeit"] == pytest.approx(1481.17)
        assert entry.data["verbrauch_letzte_laufzeit_monate"] == pytest.approx(
            192 / 30.44, abs=0.01
        )

    async def test_cold_start_switch_without_statistics_freezes_nothing(self, setup_contract):
        # Same as before the fix: no start value available -> nothing frozen,
        # and the switch itself still happens.
        entry, _ = await setup_contract(
            STROM,
            today="2026-07-12",
            options=dict(self.OPTIONS),
            latest=(None, None),
            offset=(None, None),
            sensor_states={SENSOR: "unavailable"},
        )
        assert entry.data["anbieter"] == "Neuer Anbieter"
        assert "verbrauch_letzte_laufzeit" not in entry.data

    async def test_cold_start_switch_with_manual_start_value_is_unchanged(self, setup_contract):
        # Users with a manual start value never had the consumption frozen;
        # this must not start producing different numbers.
        entry, _ = await setup_contract(
            {**STROM, "verbrauch_start_wert": 1000.0},
            today="2026-07-12",
            options=dict(self.OPTIONS),
            latest=(2481.17, 2481.17),
            offset=(1.0, 1.0),
            sensor_states={SENSOR: "2481.17"},
        )
        assert entry.data["anbieter"] == "Neuer Anbieter"
        assert "verbrauch_letzte_laufzeit" not in entry.data

    async def test_cold_start_switch_sums_both_dual_tariff_registers(self, setup_contract):
        entry, _ = await setup_contract(
            {
                **STROM,
                "sparte": "electricity_ht_nt",
                "arbeitspreis_nt": 0.20,
                "verbrauch_sensor_nt": SENSOR_NT,
            },
            today="2026-07-12",
            options=dict(self.OPTIONS),
            latest=(1300.0, 1300.0),
            offset=(1000.0, 1000.0),
            latest_nt=(800.0, 800.0),
            offset_nt=(500.0, 500.0),
            sensor_states={SENSOR: "1300", SENSOR_NT: "800"},
        )
        assert entry.data["verbrauch_letzte_laufzeit"] == pytest.approx(600.0)

    async def test_switch_button_freezes_consumption(self, setup_contract, hass: HomeAssistant):
        entry, _ = await setup_contract(
            STROM,
            today="2026-07-12",
            options=dict(self.OPTIONS, next_beginn="2027-01-01"),
            latest=(2481.17, 2481.17),
            offset=(1000.0, 1000.0),
            sensor_states={SENSOR: "2481.17"},
        )
        assert entry.options["next_beginn"] == "2027-01-01"
        await entry.runtime_data.async_force_switch()
        await hass.async_block_till_done()
        assert entry.data["anbieter"] == "Neuer Anbieter"
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


class TestInstalmentsDueForFlatRateContracts:
    """Pauschalvertraege (Internet, Mobilfunk, ...) haben keinen Verbrauch; ihre Kosten
    bisher sind die bis heute faelligen Abschlaege (`abschlag_bisher_gezahlt`)."""

    INTERNET = {
        "sparte": "internet", "anbieter": "Glasfaser", "abschlag": 39.99,
        "beginn": "2025-10-01", "ende": "2026-09-30", "erinnerung_monate": "0",
    }

    async def test_until_today(self, setup_contract):
        _, d = await setup_contract(self.INTERNET, today="2026-07-12")
        assert d["abschlag_bisher_gezahlt"] == pytest.approx(39.99 * 284 / 30.44, abs=0.01)

    async def test_stops_at_the_contract_end(self, setup_contract):
        _, d = await setup_contract(self.INTERNET, today="2026-12-01")
        assert d["abschlag_bisher_gezahlt"] == pytest.approx(39.99 * 364 / 30.44, abs=0.01)

    async def test_without_an_end_date_it_keeps_counting(self, setup_contract):
        data = {k: v for k, v in self.INTERNET.items() if k != "ende"}
        _, d = await setup_contract(data, today="2027-10-01")
        assert d["abschlag_bisher_gezahlt"] == pytest.approx(39.99 * 730 / 30.44, abs=0.01)

    async def test_not_started_yet_is_zero(self, setup_contract):
        data = {**self.INTERNET, "beginn": "2026-08-01", "ende": "2027-07-31"}
        _, d = await setup_contract(data, today="2026-07-12")
        assert d["abschlag_bisher_gezahlt"] == 0.0

    async def test_an_instalment_change_is_respected(self, setup_contract):
        data = {**self.INTERNET, "_abschlag_ab_datum": "2026-01-01", "_abschlag_vorheriger_wert": 30.0}
        _, d = await setup_contract(data, today="2026-07-12")
        expected = 30.0 * 92 / 30.44 + 39.99 * (284 - 92) / 30.44
        assert d["abschlag_bisher_gezahlt"] == pytest.approx(expected, abs=0.01)

    async def test_without_a_start_date_there_is_no_value(self, setup_contract):
        data = {k: v for k, v in self.INTERNET.items() if k != "beginn"}
        _, d = await setup_contract(data, today="2026-07-12")
        assert d["abschlag_bisher_gezahlt"] is None

    async def test_it_adds_no_entity(self, setup_contract, hass):
        await setup_contract(self.INTERNET, today="2026-07-12")
        assert not [e for e in hass.states.async_entity_ids() if "abschlag_bisher_gezahlt" in e]


class TestContractHistory:
    """The previous term is kept when the next contract takes over; an expired contract
    can be archived. Both live in internal keys: no new entity, nothing shown to old setups."""

    OPTIONS = {
        "next_beginn": "2027-01-01",
        "next_ende": "2027-12-31",
        "next_anbieter": "Neuer Anbieter",
        "next_arbeitspreis": 0.25,
        "next_abschlag": 55.0,
    }

    async def test_the_switch_keeps_the_ended_term(self, contract):
        await contract.setup(
            STROM,
            today="2026-12-31",
            options=dict(self.OPTIONS),
            latest=(2481.17, 2481.17),
            offset=(1000.0, 1000.0),
            sensor_states={SENSOR: "2481.17"},
        )
        assert contract.entry.data["anbieter"] == "Stadtwerke"
        await contract.advance_to("2027-01-01")
        entry = contract.entry
        assert entry.data["anbieter"] == "Neuer Anbieter"
        (term,) = entry.data["_historie"]
        assert term["anbieter"] == "Stadtwerke"
        assert term["beginn"] == "2026-01-01"
        assert term["ende"] == "2026-12-31"
        assert term["arbeitspreis"] == 0.2977
        assert term["abschlag"] == 40.0
        assert term["kosten"] is not None and term["kosten"] > 0
        assert term["verbrauch"] == pytest.approx(1481.17)
        assert term["abgeschlossen"] == "2027-01-01"
        assert not {"kundennummer", "zaehlernummer", "marktlokation", "notify_target"} & set(term)
        assert entry.runtime_data.data["historie"] == entry.data["_historie"]

    async def test_a_contract_without_end_date_ends_on_the_switch_day(self, contract):
        data = {k: v for k, v in STROM.items() if k != "ende"}
        await contract.setup(data, today="2027-01-01", options=dict(self.OPTIONS))
        (term,) = contract.entry.data["_historie"]
        assert term["ende"] == "2027-01-01"

    async def test_only_the_newest_terms_are_kept(self, contract):
        old = [{"anbieter": f"Alt {i}"} for i in range(50)]
        await contract.setup(
            {**STROM, "_historie": old}, today="2027-01-01", options=dict(self.OPTIONS)
        )
        history = contract.entry.data["_historie"]
        assert len(history) == 50
        assert history[0]["anbieter"] == "Alt 1"  # the oldest one dropped out
        assert history[-1]["anbieter"] == "Stadtwerke"

    async def test_no_history_without_a_switch(self, setup_contract):
        entry, d = await setup_contract(STROM, today="2026-07-12")
        assert "_historie" not in entry.data
        assert d["historie"] == []
        assert d["archiviert"] is False

    @pytest.mark.parametrize(
        ("today", "extra", "options", "expected"),
        [
            ("2027-01-02", {}, {}, True),  # ended, nothing planned
            ("2026-12-31", {}, {}, False),  # the end day itself is not over yet
            ("2026-07-12", {}, {}, False),  # still running
            ("2027-01-02", {"ende": None}, {}, False),  # no end date: never expires
            ("2027-01-02", {"_archiviert": "2027-01-01"}, {}, False),  # already archived
        ],
    )
    async def test_which_contracts_can_be_archived(self, setup_contract, today, extra, options, expected):
        data = {**STROM, **extra}
        if data.get("ende") is None:
            data.pop("ende")
        _, d = await setup_contract(data, today=today, options=options)
        assert d["archivierbar"] is expected

    async def test_an_archived_contract_stays_quiet(self, contract, hass):
        data = {**STROM, "ende": "2026-09-30", "erinnerung_monate": "3", "abschlag_warnung": True}
        await contract.setup(data, today="2026-07-01")
        assert contract.entry.runtime_data.data["erinnerung_aktiv"] is True
        await contract.entry.runtime_data.async_archive()
        await hass.async_block_till_done()
        d = contract.entry.runtime_data.data
        assert d["archiviert"] is True
        assert d["erinnerung_aktiv"] is False
        assert d["abschlag_warnung_aktiv"] is False
        assert not any(k.startswith("tariffy_") for k in hass.data["persistent_notification"])
        await contract.entry.runtime_data.async_restore()
        await hass.async_block_till_done()
        assert contract.entry.runtime_data.data["erinnerung_aktiv"] is True

    async def test_restoring_keeps_the_earlier_terms(self, contract, hass):
        earlier = [{"anbieter": "Alt", "beginn": "2024-01-01", "ende": "2024-12-31"}]
        await contract.setup({**STROM, "_historie": earlier}, today="2027-02-01")
        await contract.entry.runtime_data.async_archive()
        assert len(contract.entry.data["_historie"]) == 2
        await contract.entry.runtime_data.async_restore()
        assert contract.entry.data["_historie"] == earlier

    async def test_planning_a_contract_after_archiving_does_not_add_the_term_twice(self, contract, hass):
        await contract.setup({**STROM, "_archiviert": "2027-01-15"}, today="2027-02-01", options=dict(self.OPTIONS))
        history = contract.entry.data.get("_historie") or []
        assert history == []  # the archived contract had no entry here; none is made for the switch
        assert "_archiviert" not in contract.entry.data  # the new contract is active again


class TestYearlyValuesAndPaymentInterval:
    """`abschlag` is always the amount per month; the interval and the yearly values are display data."""

    INSURANCE = {
        "sparte": "insurance",
        "anbieter": "Versicherung AG",
        "abschlag": 50.0,
        "beginn": "2026-01-01",
        "ende": "2026-12-31",
    }

    async def test_yearly_values(self, setup_contract):
        _, d = await setup_contract({**self.INSURANCE, "zahlweise": "yearly"}, today="2026-07-12")
        assert d["zahlweise"] == "yearly"
        assert d["abschlag_jahr"] == 600.0
        assert d["abschlag_je_zahlung"] == 600.0
        assert d["kosten_jahr"] == 600.0

    async def test_the_base_price_counts_for_the_yearly_cost_only(self, setup_contract):
        _, d = await setup_contract({**self.INSURANCE, "grundpreis": 5.0}, today="2026-07-12")
        assert d["abschlag_jahr"] == 600.0
        assert d["kosten_jahr"] == 660.0

    @pytest.mark.parametrize(
        ("zahlweise", "per_payment"), [("monthly", 50.0), ("quarterly", 150.0), ("halfyearly", 300.0), ("yearly", 600.0)]
    )
    async def test_the_amount_of_one_payment(self, setup_contract, zahlweise, per_payment):
        _, d = await setup_contract({**self.INSURANCE, "zahlweise": zahlweise}, today="2026-07-12")
        assert d["abschlag_je_zahlung"] == per_payment

    @pytest.mark.parametrize("stored", [None, "", "weekly"])
    async def test_existing_contracts_are_monthly(self, setup_contract, stored):
        data = dict(self.INSURANCE)
        if stored is not None:
            data["zahlweise"] = stored
        _, d = await setup_contract(data, today="2026-07-12")
        assert d["zahlweise"] == "monthly"
        assert d["abschlag_je_zahlung"] == 50.0

    async def test_no_instalment_no_yearly_values(self, setup_contract):
        data = {k: v for k, v in self.INSURANCE.items() if k != "abschlag"}
        _, d = await setup_contract(data, today="2026-07-12")
        assert d["abschlag_jahr"] is None and d["kosten_jahr"] is None and d["abschlag_je_zahlung"] is None

    async def test_nothing_else_changes(self, setup_contract):
        _, monthly = await setup_contract(dict(self.INSURANCE), today="2026-07-12")
        _, yearly = await setup_contract({**self.INSURANCE, "zahlweise": "yearly"}, today="2026-07-12")
        for key in ("abschlag", "jahreskosten", "abschlag_bisher_gezahlt", "restlaufzeit"):
            assert monthly[key] == yearly[key], key


class TestTotalCostOverAllTerms:
    """Cost over the whole life of a contract: the earlier terms from the history plus the running one."""

    INSURANCE = {
        "sparte": "insurance",
        "anbieter": "Versicherung AG",
        "abschlag": 100.0,
        "beginn": "2026-06-01",
        "ende": "2027-05-31",
    }

    @staticmethod
    def _term(beginn, ende, **values):
        return {"anbieter": "Versicherung AG", "beginn": beginn, "ende": ende, **values}

    async def test_earlier_terms_and_the_running_one_are_added(self, setup_contract):
        history = [
            self._term("2024-06-01", "2025-05-31", abschlag_gezahlt=1100.0),
            self._term("2025-06-01", "2026-05-31", abschlag_gezahlt=1200.0),
        ]
        _, d = await setup_contract({**self.INSURANCE, "_historie": history}, today="2026-07-12")
        running = d["abschlag_bisher_gezahlt"]
        assert 100 < running < 200  # about 1.4 months of 100
        assert d["kosten_gesamt"] == pytest.approx(1100.0 + 1200.0 + running, abs=0.01)
        assert d["laufzeiten_anzahl"] == 3
        assert d["seit"].isoformat() == "2024-06-01"
        assert d["kosten_gesamt_vollstaendig"] is True

    async def test_a_term_with_a_cost_uses_it_before_the_instalments(self, setup_contract):
        history = [self._term("2025-06-01", "2026-05-31", kosten=1234.5, abschlag_gezahlt=1200.0)]
        _, d = await setup_contract({**self.INSURANCE, "_historie": history}, today="2026-07-12")
        assert d["kosten_gesamt"] == pytest.approx(1234.5 + d["abschlag_bisher_gezahlt"], abs=0.01)

    async def test_without_history_it_is_the_running_term(self, setup_contract):
        _, d = await setup_contract(dict(self.INSURANCE), today="2026-07-12")
        assert d["kosten_gesamt"] == d["abschlag_bisher_gezahlt"]
        assert d["laufzeiten_anzahl"] == 1
        assert d["seit"].isoformat() == "2026-06-01"

    async def test_an_archived_contract_does_not_count_its_last_term_twice(self, contract):
        await contract.setup({**self.INSURANCE, "ende": "2026-06-30"}, today="2026-08-01")
        await contract.entry.runtime_data.async_archive()
        (term,) = contract.entry.data["_historie"]
        d = contract.entry.runtime_data.data
        assert d["archiviert"] is True
        assert d["kosten_gesamt"] == pytest.approx(term["abschlag_gezahlt"], abs=0.01)  # only the history entry
        assert d["laufzeiten_anzahl"] == 1

    async def test_a_term_without_any_cost_makes_the_total_a_lower_bound(self, setup_contract):
        history = [self._term("2024-06-01", "2025-05-31"), self._term("2025-06-01", "2026-05-31", abschlag_gezahlt=1200.0)]
        _, d = await setup_contract({**self.INSURANCE, "_historie": history}, today="2026-07-12")
        assert d["kosten_gesamt_vollstaendig"] is False
        assert d["kosten_gesamt"] == pytest.approx(1200.0 + d["abschlag_bisher_gezahlt"], abs=0.01)

    async def test_metered_contracts_use_the_measured_cost(self, setup_contract):
        history = [self._term("2025-01-01", "2025-12-31", kosten=900.0)]
        _, d = await setup_contract({**STROM, "_historie": history}, today="2026-07-12", **dict(
            latest=(2481.17, 2481.17), offset=(1000.0, 1000.0), sensor_states={SENSOR: "2481.17"}))
        assert d["kosten_gesamt"] == pytest.approx(900.0 + d["kosten_bisher"], abs=0.01)
        assert d["laufzeiten_anzahl"] == 2
