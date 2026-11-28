"""#126: own consumption of the last term in the history beats the frozen value."""

from custom_components.tariffy.coordinator import _verbrauch_letzte_laufzeit_aus_historie as pick


def test_own_value_wins_with_months():
    hist = [
        {"beginn": "2025-10-01", "ende": "2026-04-30", "verbrauch": 905.0, "eigene": ["verbrauch"]},
        {"beginn": "2026-05-01", "ende": "2026-07-31", "verbrauch": 11.0, "eigene": ["verbrauch"]},
    ]
    assert pick(hist) == (11.0, round(92 / 30.44, 2))


def test_automatic_value_is_not_used():
    hist = [{"beginn": "2026-05-01", "ende": "2026-07-31", "verbrauch": 11.0, "eigene": []}]
    assert pick(hist) is None


def test_empty_or_invalid_history():
    assert pick(None) is None
    assert pick([]) is None
    assert pick(["x"]) is None
    assert pick([{"eigene": ["verbrauch"], "verbrauch": 0}]) is None


def test_missing_dates_gives_no_months():
    assert pick([{"eigene": ["verbrauch"], "verbrauch": 5.0}]) == (5.0, None)
