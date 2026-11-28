"""A few weeks before the end of a contract "adjust the instalment" is no monthly amount any more (forum reports):
the whole expected difference would fall on the last month. The sensor keeps its value; the panel, the attributes and
the notification say what is expected and what fits a whole term."""

from __future__ import annotations

import pytest

from custom_components.tariffy import panel

from .test_coordinator import SENSOR, STROM
from .test_panel import frontend_env  # noqa: F401  (fixture)

DATA = {**STROM, "abschlag_warnung": True, "abschlag_warnung_schwelle": 50.0}
KW = {"latest": (2481.17, 2481.17), "offset": (1000.0, 1000.0), "sensor_states": {SENSOR: "2481.17"}}


async def test_far_from_the_end_nothing_changes(setup_contract, hass):
    entry, d = await setup_contract(DATA, today="2026-07-12", **KW)
    assert d["restlaufzeit"] == 172
    assert d["abschlag_kurz_vor_ende"] is False
    assert d["abschlag_anpassung_empfohlen"] == pytest.approx(127.66, abs=0.01)
    note = hass.data["persistent_notification"][f"tariffy_abschlag_warnung_{entry.entry_id}"]["message"]
    assert "für die restliche Laufzeit" in note and "Schlussrechnung" not in note


async def test_a_few_weeks_before_the_end_the_term_amount_is_offered(setup_contract):
    _, d = await setup_contract(DATA, today="2026-11-28", **KW)
    assert d["restlaufzeit"] == 33
    assert d["abschlag_kurz_vor_ende"] is True
    # what a whole term costs a month: the estimated cost of the term divided by its months
    assert d["abschlag_naechste_laufzeit"] == pytest.approx(52.06, abs=0.05)
    # the sensor value is the same calculation as before (automations may use it)
    assert d["abschlag_anpassung_empfohlen"] == pytest.approx(173.02, abs=0.05)


async def test_the_limit_is_two_months(setup_contract):
    _, early = await setup_contract(DATA, today="2026-10-30", **KW)  # 62 days, just above two months
    _, late = await setup_contract(DATA, today="2026-11-02", **KW)  # 59 days
    assert early["abschlag_kurz_vor_ende"] is False
    assert late["abschlag_kurz_vor_ende"] is True


async def test_without_an_instalment_there_is_nothing_to_say(setup_contract):
    _, d = await setup_contract({k: v for k, v in DATA.items() if k != "abschlag"}, today="2026-11-28", **KW)
    assert d["abschlag_anpassung_empfohlen"] is None and d["abschlag_kurz_vor_ende"] is False


async def test_the_notification_says_the_balance_comes_with_the_final_bill(setup_contract, hass):
    entry, d = await setup_contract(DATA, today="2026-11-28", **KW)
    note = hass.data["persistent_notification"][f"tariffy_abschlag_warnung_{entry.entry_id}"]["message"]
    assert "Schlussrechnung" in note and "52.06" in note
    assert "für die restliche Laufzeit" not in note  # no absurd monthly amount for the last weeks
    assert "144.21" in note  # the expected balance due is still named


async def test_the_panel_gets_the_fields(frontend_env, setup_contract, hass):  # noqa: F811
    entry, _ = await setup_contract(DATA, today="2026-11-28", **KW)
    payload = panel.contract_payload(hass, entry)
    assert payload["abschlag_kurz_vor_ende"] is True
    assert payload["abschlag_naechste_laufzeit"] == pytest.approx(52.06, abs=0.05)


async def test_the_sensor_shows_the_attributes(setup_contract, hass):
    entry, _ = await setup_contract(DATA, today="2026-11-28", **KW)
    states = [s for s in hass.states.async_all("sensor") if "kurz_vor_ende" in s.attributes]
    assert len(states) == 1
    assert states[0].attributes["kurz_vor_ende"] is True
    assert states[0].attributes["abschlag_naechste_laufzeit"] == pytest.approx(52.06, abs=0.05)
