"""Tests for the pure helper functions in coordinator.py."""

from __future__ import annotations

from datetime import date

import pytest

from custom_components.tariffy.coordinator import (
    _abschlag_bisher_gezahlt,
    _extract_tiers,
    _f,
    _minus_months,
    _parse_date,
    _pick_verbrauch_delta,
    _tiered_cost,
)


class TestParsing:
    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("1.5", 1.5),
            (2, 2.0),
            ("0", 0.0),
            (None, None),
            ("", None),
            ("unknown", None),
            ("unavailable", None),
            ([], None),
        ],
    )
    def test_f(self, value, expected):
        assert _f(value) == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("2026-07-12", date(2026, 7, 12)),
            (date(2026, 1, 2), date(2026, 1, 2)),
            (None, None),
            ("", None),
            ("12.07.2026", None),
            ("garbage", None),
        ],
    )
    def test_parse_date(self, value, expected):
        assert _parse_date(value) == expected


class TestMinusMonths:
    def test_zero_months_is_identity(self):
        assert _minus_months(date(2026, 5, 31), 0) == date(2026, 5, 31)

    def test_simple(self):
        assert _minus_months(date(2026, 12, 31), 3) == date(2026, 9, 30)

    def test_clamps_to_month_end(self):
        assert _minus_months(date(2026, 3, 31), 1) == date(2026, 2, 28)

    def test_leap_year(self):
        assert _minus_months(date(2028, 3, 31), 1) == date(2028, 2, 29)

    def test_crosses_year_boundary(self):
        assert _minus_months(date(2026, 2, 15), 4) == date(2025, 10, 15)


class TestTieredCost:
    def test_no_tiers_returns_none(self):
        assert _tiered_cost(100, [], []) is None
        assert _tiered_cost(100, [5], []) is None

    def test_within_first_block(self):
        assert _tiered_cost(3, [5, 10], [0.5, 0.8, 1.2]) == 1.5

    def test_spans_all_blocks(self):
        # 5 * 0.5 + 5 * 0.8 + 5 * 1.2
        assert _tiered_cost(15, [5, 10], [0.5, 0.8, 1.2]) == 12.5

    def test_exactly_on_limit(self):
        assert _tiered_cost(10, [5, 10], [0.5, 0.8, 1.2]) == 6.5

    def test_zero_consumption(self):
        assert _tiered_cost(0, [5, 10], [0.5, 0.8, 1.2]) == 0.0

    def test_last_block_is_unlimited_when_limit_is_none(self):
        assert _tiered_cost(100, [5, None], [1.0, 2.0]) == 5 * 1.0 + 95 * 2.0


class TestExtractTiers:
    def test_individual_fields(self):
        data = {
            "tier_limit_0": "5",
            "tier_price_0": "0.5",
            "tier_limit_1": "10",
            "tier_price_1": "0.8",
            "tier_price_2": "1.2",
        }
        assert _extract_tiers(data) == ([5.0, 10.0, None], [0.5, 0.8, 1.2])

    def test_stops_at_first_missing_price(self):
        data = {"tier_price_0": "0.5", "tier_price_2": "9"}
        assert _extract_tiers(data) == ([None], [0.5])

    def test_legacy_list_form_wins(self):
        data = {
            "tier_limits": [5, 10],
            "tier_prices": [0.5, 0.8, 1.2],
            "tier_price_0": "99",
        }
        assert _extract_tiers(data) == ([5, 10], [0.5, 0.8, 1.2])

    def test_empty(self):
        assert _extract_tiers({}) == ([], [])


class TestPickVerbrauchDelta:
    def test_prefers_state_delta_when_no_reset(self):
        # sum glitched to double, raw state stayed continuous
        assert _pick_verbrauch_delta(
            aktuell_sum=2000.0, offset_sum=1000.0, aktuell_state=1100.4, offset_state=1100.0
        ) == 0.4

    def test_uses_sum_delta_after_real_reset(self):
        # raw state fell below the contract-start value: meter was reset
        assert _pick_verbrauch_delta(
            aktuell_sum=1050.0, offset_sum=1000.0, aktuell_state=20.0, offset_state=980.0
        ) == 50.0

    def test_equal_state_is_zero_not_reset(self):
        assert _pick_verbrauch_delta(500.0, 400.0, 100.0, 100.0) == 0.0

    def test_falls_back_to_sum_without_states(self):
        assert _pick_verbrauch_delta(120.5, 100.0, None, None) == 20.5

    def test_none_when_nothing_usable(self):
        assert _pick_verbrauch_delta(None, None, None, None) is None
        assert _pick_verbrauch_delta(10.0, None, None, None) is None

    def test_rounds_to_two_decimals(self):
        assert _pick_verbrauch_delta(None, None, 10.123456, 0.0) == 10.12


class TestAbschlagBisherGezahlt:
    BEGINN = date(2026, 1, 1)

    def test_no_history_is_simple_product(self):
        assert _abschlag_bisher_gezahlt(40, 6.0, self.BEGINN, {}) == 240.0

    def test_change_is_applied_from_its_date_only(self):
        data = {"_abschlag_ab_datum": "2026-04-01", "_abschlag_vorheriger_wert": 30.0}
        monate_alt = (date(2026, 4, 1) - self.BEGINN).days / 30.44
        result = _abschlag_bisher_gezahlt(50, 6.0, self.BEGINN, data)
        assert result == pytest.approx(30 * monate_alt + 50 * (6.0 - monate_alt))

    def test_change_not_yet_in_the_past_uses_old_value(self):
        data = {"_abschlag_ab_datum": "2026-12-01", "_abschlag_vorheriger_wert": 30.0}
        assert _abschlag_bisher_gezahlt(50, 6.0, self.BEGINN, data) == 180.0

    def test_change_on_or_before_contract_start_is_ignored(self):
        data = {"_abschlag_ab_datum": "2026-01-01", "_abschlag_vorheriger_wert": 30.0}
        assert _abschlag_bisher_gezahlt(50, 6.0, self.BEGINN, data) == 300.0

    def test_incomplete_history_is_ignored(self):
        assert (
            _abschlag_bisher_gezahlt(
                50, 6.0, self.BEGINN, {"_abschlag_ab_datum": "2026-04-01"}
            )
            == 300.0
        )
