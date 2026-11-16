"""Kredit / Finanzierung als Vertragsart (Issue 61): Formular, Berechnung, Anschlussfinanzierung."""

from __future__ import annotations

import pytest
from homeassistant.data_entry_flow import FlowResultType


from .test_insurance import _assert_texts, _keys, _start
from .test_panel import GOLDEN, frontend_env  # noqa: F401  (fixture)
from .test_reconfigure import _reconfigure

LOAN = {
    "sparte": "loan",
    "anbieter": "Hausbank",
    "tarif": "Baufinanzierung",
    "kredit_summe": 10000.0,
    "sollzins": 5.0,
    "effektivzins": 5.12,
    "laufzeit_monate": 12,
    "zahlweise": "monthly",
    "beginn": "2026-01-15",
    "erinnerung_monate": "0",
}
TODAY = {**GOLDEN, "today": "2026-06-20"}


async def test_the_form_asks_for_the_loan_and_is_translated(hass):
    result = await _start(hass, "loan")
    assert result["step_id"] == "kredit"
    assert _keys(result) == {
        "kredit_summe", "sollzins", "effektivzins", "laufzeit_monate", "zahlweise",
        "kredit_rate", "schlussrate", "erste_zahlung",
    }
    _assert_texts(result)


async def test_a_loan_is_created_with_the_figures(hass):
    result = await _start(hass, "loan")
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"kredit_summe": 10000, "sollzins": 5.0, "effektivzins": 5.12, "laufzeit_monate": 12.0, "zahlweise": "monthly"},
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    data = result["data"]
    assert data["sparte"] == "loan" and data["kredit_summe"] == 10000 and data["laufzeit_monate"] == 12
    assert isinstance(data["laufzeit_monate"], int)  # the number field sends a float


@pytest.mark.parametrize(
    ("values", "key", "code"),
    [
        ({"kredit_summe": 0, "sollzins": 5.0}, "kredit_summe", "kredit_summe"),
        ({"kredit_summe": 1000}, "base", "kredit_zins"),
    ],
)
async def test_a_loan_that_cannot_be_calculated_is_refused(hass, values, key, code):
    result = await _start(hass, "loan")
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {"laufzeit_monate": 12.0, "zahlweise": "monthly", **values}
    )
    assert result["type"] is FlowResultType.FORM and result["step_id"] == "kredit"
    assert result["errors"] == {key: code}


async def test_the_figures_of_the_running_loan(contract):
    _, d = await contract.setup(LOAN, **TODAY)
    assert d["kredit_rate"] == pytest.approx(856.07, abs=0.005)
    assert d["kredit_zahlungen_geleistet"] == 5
    assert d["kredit_restschuld"] == pytest.approx(10000 - d["kredit_tilgung_bisher"], abs=0.01)
    assert d["kredit_gezahlt"] + d["kredit_restsumme"] == pytest.approx(d["kredit_gesamtkosten"], abs=0.03)
    assert str(d["ende"]) == "2027-01-15"  # follows from the start and the term
    assert d["restlaufzeit"] == 209
    assert str(d["naechste_zahlung"]) == "2026-07-15" and str(d["erste_zahlung"]) == "2026-02-15"
    assert d["verlaengerbar"] is True  # a follow-up financing renews it
    assert d["abschlag_bisher_gezahlt"] is None  # none of the flat-rate figures
    assert d["kosten_gesamt"] == pytest.approx(d["kredit_gezahlt"], abs=0.01)


async def test_the_loan_has_its_own_sensors(contract, hass):
    _, d = await contract.setup(LOAN, **TODAY)
    ids = hass.states.async_entity_ids("sensor")
    assert [e for e in ids if "interest_paid_so_far" in e] and [e for e in ids if "remaining_payments" in e]
    debt = hass.states.get([e for e in ids if "remaining_debt" in e][0])
    assert float(debt.state) == pytest.approx(d["kredit_restschuld"], abs=0.01)
    assert debt.attributes["unit_of_measurement"] == "EUR" or debt.attributes["unit_of_measurement"]


async def test_a_flat_rate_contract_gets_no_loan_sensor(contract, hass):
    await contract.setup(
        {"sparte": "internet", "abschlag": 40.0, "beginn": "2026-01-01", "erinnerung_monate": "0"}, **TODAY
    )
    assert not [e for e in hass.states.async_entity_ids("sensor") if "remaining_debt" in e]


async def test_editing_the_loan_keeps_its_internal_state(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await contract.setup({**LOAN, "_einmalposten": [{"bezeichnung": "A", "betrag": 5.0, "datum": None}]}, **TODAY)
    data = await _reconfigure(hass, entry, second={"kredit_rate": 860.0})
    assert data["kredit_rate"] == 860.0 and data["kredit_summe"] == 10000.0
    assert data["_einmalposten"]
    assert isinstance(data["laufzeit_monate"], int)


async def _call(client, **extra):
    await client.send_json_auto_id({"type": "tariffy/renew", **extra})
    return await client.receive_json()


async def test_a_follow_up_financing_keeps_the_old_term_in_the_history(frontend_env, contract, hass, hass_ws_client):  # noqa: F811
    client = await hass_ws_client()
    entry, before = await contract.setup(LOAN, **{**GOLDEN, "today": "2027-01-20"})
    assert before["kredit_restschuld"] == pytest.approx(0.0, abs=0.1)
    reply = await _call(
        client, entry_id=entry.entry_id,
        values={"beginn": "2027-01-15", "kredit_summe": 4000, "sollzins": 3.5, "laufzeit_monate": 24},
    )
    assert reply["success"] is True
    await hass.async_block_till_done()
    assert entry.data["kredit_summe"] == 4000 and entry.data["sollzins"] == 3.5 and entry.data["laufzeit_monate"] == 24
    assert "effektivzins" not in entry.data and "kredit_rate" not in entry.data  # the new loan has its own figures
    (term,) = entry.data["_historie"]
    assert term["kredit_summe"] == 10000 and term["sollzins"] == 5.0 and term["kosten"] > 10000
    now = entry.runtime_data.data
    assert now["kredit_summe"] == 4000 and now["kredit_zahlungen_gesamt"] == 24
    assert str(now["ende"]) == "2029-01-15"
    assert now["laufzeiten_anzahl"] == 2


@pytest.mark.parametrize(
    ("values", "code"),
    [
        ({"beginn": "kaputt", "kredit_summe": 1000, "sollzins": 3, "laufzeit_monate": 12}, "invalid_dates"),
        ({"beginn": "2027-01-15", "kredit_summe": 0, "sollzins": 3, "laufzeit_monate": 12}, "invalid_kredit_summe"),
        ({"beginn": "2027-01-15", "kredit_summe": 1000, "sollzins": 3, "laufzeit_monate": 0}, "invalid_laufzeit_monate"),
        ({"beginn": "2027-01-15", "kredit_summe": 1000, "laufzeit_monate": 12}, "invalid_zins"),
    ],
)
async def test_a_bad_follow_up_is_refused(frontend_env, contract, hass, hass_ws_client, values, code):  # noqa: F811
    client = await hass_ws_client()
    entry, _ = await contract.setup(LOAN, **TODAY)
    reply = await _call(client, entry_id=entry.entry_id, values=values)
    assert reply["success"] is False and reply["error"]["code"] == code
    assert entry.data["kredit_summe"] == 10000.0 and "_historie" not in entry.data


def test_the_loan_survives_a_backup():
    from custom_components.tariffy import backup

    assert backup.sanitize_contract({"title": "Kredit", "data": LOAN})["data"]["kredit_summe"] == 10000.0
