"""Kuendigungsfrist und Mindestlaufzeit: die Erinnerung bezieht sich auf die Frist."""

from __future__ import annotations

import pytest

from .test_coordinator import SENSOR, STROM, TestTariffSwitch
from .test_panel import GOLDEN, frontend_env  # noqa: F401  (fixture)
from .test_reconfigure import _contract, _reconfigure

TODAY = {**GOLDEN, "today": "2026-07-12"}


async def test_without_a_notice_period_nothing_changes(contract):
    _, d = await contract.setup({**STROM, "erinnerung_monate": "3"}, **TODAY)
    assert str(d["erinnerung_datum"]) == "2026-09-30"  # 3 months before the end, as always
    assert d["kuendigungsfrist"] is None and d["kuendigung_bis"] is None
    assert d["erinnerung_aktiv"] is False


async def test_the_reminder_counts_from_the_cancellation_deadline(contract):
    # 3 months notice, reminder 3 months before: the reminder comes 6 months before the end
    _, d = await contract.setup({**STROM, "erinnerung_monate": "3", "kuendigungsfrist": 3.0}, **TODAY)
    assert str(d["kuendigung_bis"]) == "2026-09-30"
    assert str(d["erinnerung_datum"]) == "2026-06-30"
    assert d["kuendigungsfrist"] == 3
    assert d["erinnerung_aktiv"] is True  # 2026-07-12 is after the reminder date


async def test_no_reminder_stays_off_with_a_notice_period(contract):
    _, d = await contract.setup({**STROM, "erinnerung_monate": "0", "kuendigungsfrist": 3}, **TODAY)
    assert d["erinnerung_datum"] is None and d["erinnerung_aktiv"] is False
    assert str(d["kuendigung_bis"]) == "2026-09-30"  # still shown


async def test_minimum_term_runs_from_the_start(contract):
    _, d = await contract.setup({**STROM, "mindestlaufzeit": 12}, **TODAY)
    assert d["mindestlaufzeit"] == 12 and str(d["mindestlaufzeit_bis"]) == "2027-01-01"


@pytest.mark.parametrize("value", [0, "", None, "abc"])
async def test_empty_or_zero_means_not_set(contract, value):
    _, d = await contract.setup({**STROM, "kuendigungsfrist": value, "mindestlaufzeit": value}, **TODAY)
    assert d["kuendigungsfrist"] is None and d["mindestlaufzeit"] is None
    assert d["kuendigung_bis"] is None and d["mindestlaufzeit_bis"] is None


async def test_the_notice_period_survives_a_tariff_switch(setup_contract):
    entry, d = await setup_contract(
        {**STROM, "kuendigungsfrist": 3, "mindestlaufzeit": 12},
        today="2026-07-12",
        options=dict(TestTariffSwitch.OPTIONS),
        latest=(2481.17, 2481.17),
        offset=(1000.0, 1000.0),
        sensor_states={SENSOR: "2481.17"},
    )
    assert entry.data["anbieter"] == "Neuer Anbieter"
    assert entry.data["kuendigungsfrist"] == 3  # the reminder keeps its lead
    assert "mindestlaufzeit" not in entry.data  # a new contract has its own minimum term


async def test_the_notice_period_can_be_set_changed_and_emptied(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await _contract(contract)
    data = await _reconfigure(hass, entry, first={"kuendigungsfrist": 3.0, "mindestlaufzeit": 12.0})
    assert data["kuendigungsfrist"] == 3 and data["mindestlaufzeit"] == 12
    assert "_kuendigung_bestaetigt" not in data  # a new deadline: the reminder starts over
    hass.config_entries.async_update_entry(entry, data={**entry.data, "_kuendigung_bestaetigt": True})
    data = await _reconfigure(hass, entry)  # saved unchanged: the acknowledgement stays
    assert data["_kuendigung_bestaetigt"] is True and data["kuendigungsfrist"] == 3
    data = await _reconfigure(hass, entry, first={"kuendigungsfrist": 1.0})
    assert data["kuendigungsfrist"] == 1
    assert "_kuendigung_bestaetigt" not in data
    data = await _reconfigure(hass, entry, drop_first=("kuendigungsfrist", "mindestlaufzeit"))
    assert "kuendigungsfrist" not in data and "mindestlaufzeit" not in data
