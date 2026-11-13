"""Verlaengern eines Pauschalvertrags (Versicherung, Internet, ...): neue Laufzeit, alte in der Historie."""

from __future__ import annotations

import pytest

from .test_coordinator import STROM
from .test_panel import GOLDEN, frontend_env  # noqa: F401  (fixture)

INSURANCE = {
    "sparte": "insurance",
    "anbieter": "Versicherung AG",
    "tarif": "Kasko",
    "abschlag": 50.0,
    "zahlweise": "yearly",
    "beginn": "2025-01-01",
    "ende": "2025-12-31",
    "erinnerung_monate": "3",
    "kundennummer": "K-1",
}
NEW = {"beginn": "2026-01-01", "ende": "2026-12-31", "abschlag": 660.0, "zahlweise": "yearly"}


async def _call(client, **extra):
    await client.send_json_auto_id({"type": "tariffy/renew", **extra})
    return await client.receive_json()


async def test_a_renewed_contract_runs_on_with_the_new_amount_and_keeps_the_old_term(
    frontend_env, contract, hass, hass_ws_client  # noqa: F811
):
    client = await hass_ws_client()
    entry, data = await contract.setup(INSURANCE, **{**GOLDEN, "today": "2026-01-10"})
    assert data["verlaengerbar"] is True and data["restlaufzeit"] < 0

    reply = await _call(client, entry_id=entry.entry_id, values=NEW)
    assert reply["success"] is True
    await hass.async_block_till_done()

    assert entry.data["beginn"] == "2026-01-01" and entry.data["ende"] == "2026-12-31"
    assert entry.data["abschlag"] == 55.0  # 660 a year
    assert entry.data["zahlweise"] == "yearly"
    assert entry.data["anbieter"] == "Versicherung AG" and entry.data["kundennummer"] == "K-1"  # the rest is kept
    (term,) = entry.data["_historie"]  # the old term
    assert term["beginn"] == "2025-01-01" and term["ende"] == "2025-12-31"
    assert term["abschlag"] == 50.0 and term["anbieter"] == "Versicherung AG" and term["tarif"] == "Kasko"
    assert term["abschlag_gezahlt"] == 600.0  # the yearly premium, debited once
    assert "kundennummer" not in term

    now = entry.runtime_data.data
    assert now["abschlag_jahr"] == 660.0
    assert now["historie"] == entry.data["_historie"]
    assert now["restlaufzeit"] > 300  # a full new year
    assert now["abschlag_bisher_gezahlt"] == 660.0  # the new premium, debited at the new start, with the new amount


async def test_a_second_renewal_adds_a_second_term(frontend_env, contract, hass, hass_ws_client):  # noqa: F811
    client = await hass_ws_client()
    entry, _ = await contract.setup(INSURANCE, **{**GOLDEN, "today": "2026-01-10"})
    await _call(client, entry_id=entry.entry_id, values=NEW)
    contract.freezer.move_to("2027-01-10 12:00:00")
    await entry.runtime_data.async_refresh()
    reply = await _call(client, entry_id=entry.entry_id, values={"beginn": "2027-01-01", "ende": "2027-12-31", "abschlag": 720.0})
    assert reply["success"] is True
    assert [t["abschlag"] for t in entry.data["_historie"]] == [50.0, 55.0]
    assert entry.data["abschlag"] == 60.0
    assert entry.data["zahlweise"] == "yearly"  # kept when not sent


async def test_the_old_terms_reminders_do_not_follow_into_the_new_term(frontend_env, contract, hass, hass_ws_client):  # noqa: F811
    client = await hass_ws_client()
    old = {**INSURANCE, "_kuendigung_bestaetigt": True, "_notify_gesendet": True,
           "_abschlag_ab_datum": "2025-06-01", "_abschlag_vorheriger_wert": 40.0}
    entry, _ = await contract.setup(old, **{**GOLDEN, "today": "2026-01-10"})
    await _call(client, entry_id=entry.entry_id, values=NEW)
    for key in ("_kuendigung_bestaetigt", "_notify_gesendet", "_abschlag_ab_datum", "_abschlag_vorheriger_wert"):
        assert key not in entry.data, key
    assert entry.runtime_data.data["erinnerung_datum"].isoformat() == "2026-09-30"  # the new end minus 3 months


async def test_the_interval_can_change_with_the_renewal(frontend_env, contract, hass, hass_ws_client):  # noqa: F811
    client = await hass_ws_client()
    entry, _ = await contract.setup(INSURANCE, **{**GOLDEN, "today": "2026-01-10"})
    await _call(client, entry_id=entry.entry_id, values={**NEW, "zahlweise": "quarterly", "abschlag": 165.0})
    assert entry.data["abschlag"] == 55.0 and entry.data["zahlweise"] == "quarterly"


@pytest.mark.parametrize(
    ("values", "code"),
    [
        ({**NEW, "ende": "2026-01-01"}, "invalid_dates"),  # not after the start
        ({**NEW, "ende": "2025-12-31"}, "invalid_dates"),
        ({**NEW, "beginn": "kein Datum"}, "invalid_dates"),
        ({**NEW, "abschlag": 0}, "invalid_abschlag"),
        ({**NEW, "abschlag": -5}, "invalid_abschlag"),
        ({k: v for k, v in NEW.items() if k != "abschlag"}, "invalid_abschlag"),
        ({**NEW, "zahlweise": "weekly"}, "invalid_zahlweise"),
    ],
)
async def test_unusable_input_changes_nothing(frontend_env, contract, hass_ws_client, values, code):  # noqa: F811
    client = await hass_ws_client()
    entry, _ = await contract.setup(INSURANCE, **{**GOLDEN, "today": "2026-01-10"})
    before = dict(entry.data)
    reply = await _call(client, entry_id=entry.entry_id, values=values)
    assert reply["error"]["code"] == code
    assert dict(entry.data) == before


async def test_only_flat_rate_contracts_with_an_end_can_be_renewed(frontend_env, contract, hass, hass_ws_client):  # noqa: F811
    client = await hass_ws_client()
    entry, data = await contract.setup(dict(STROM), **GOLDEN)
    assert data["verlaengerbar"] is False
    reply = await _call(client, entry_id=entry.entry_id, values=NEW)
    assert reply["error"]["code"] == "not_available"
    assert entry.data["beginn"] == STROM["beginn"]


async def test_without_an_end_date_there_is_nothing_to_renew(frontend_env, contract, hass, hass_ws_client):  # noqa: F811
    client = await hass_ws_client()
    data = {k: v for k, v in INSURANCE.items() if k != "ende"}
    entry, d = await contract.setup(data, **GOLDEN)
    assert d["verlaengerbar"] is False
    assert (await _call(client, entry_id=entry.entry_id, values=NEW))["error"]["code"] == "not_available"


async def test_an_archived_contract_is_not_renewed(frontend_env, contract, hass, hass_ws_client):  # noqa: F811
    client = await hass_ws_client()
    entry, _ = await contract.setup({**INSURANCE, "_archiviert": "2026-01-05"}, **{**GOLDEN, "today": "2026-01-10"})
    assert entry.runtime_data.data["verlaengerbar"] is False
    assert (await _call(client, entry_id=entry.entry_id, values=NEW))["error"]["code"] == "not_available"


async def test_unknown_contract(frontend_env, contract, hass, hass_ws_client):  # noqa: F811
    client = await hass_ws_client()
    await contract.setup(INSURANCE, **{**GOLDEN, "today": "2026-01-10"})
    assert (await _call(client, entry_id="nope", values=NEW))["error"]["code"] == "not_found"


async def test_administrators_only(
    frontend_env, contract, hass, hass_ws_client, hass_read_only_access_token  # noqa: F811
):
    client = await hass_ws_client(hass, hass_read_only_access_token)
    entry, _ = await contract.setup(INSURANCE, **{**GOLDEN, "today": "2026-01-10"})
    reply = await _call(client, entry_id=entry.entry_id, values=NEW)
    assert reply["error"]["code"] == "unauthorized"
    assert entry.data["beginn"] == "2025-01-01"


async def test_the_first_debit_of_the_new_term_can_be_given(frontend_env, contract, hass, hass_ws_client):  # noqa: F811
    client = await hass_ws_client()
    old = {**INSURANCE, "erste_zahlung": "2025-01-15"}
    entry, _ = await contract.setup(old, **{**GOLDEN, "today": "2026-01-10"})
    reply = await _call(client, entry_id=entry.entry_id, values={**NEW, "erste_zahlung": "2026-01-20"})
    assert reply["success"] is True
    assert entry.data["erste_zahlung"] == "2026-01-20"
    assert entry.runtime_data.data["naechste_zahlung"] is None or entry.runtime_data.data["naechste_zahlung"].isoformat() >= "2026-01-20"
    assert entry.runtime_data.data["abschlag_bisher_gezahlt"] == 0.0  # the new premium is debited on the 20th, today is the 10th


async def test_the_old_first_debit_does_not_follow_into_the_new_term(frontend_env, contract, hass, hass_ws_client):  # noqa: F811
    client = await hass_ws_client()
    entry, _ = await contract.setup({**INSURANCE, "erste_zahlung": "2025-01-15"}, **{**GOLDEN, "today": "2026-01-10"})
    await _call(client, entry_id=entry.entry_id, values=NEW)
    assert "erste_zahlung" not in entry.data  # the new term starts with the debit on its start
    assert entry.runtime_data.data["abschlag_bisher_gezahlt"] == 660.0


async def test_an_invalid_first_debit_is_refused(frontend_env, contract, hass, hass_ws_client):  # noqa: F811
    client = await hass_ws_client()
    entry, _ = await contract.setup(INSURANCE, **{**GOLDEN, "today": "2026-01-10"})
    before = dict(entry.data)
    reply = await _call(client, entry_id=entry.entry_id, values={**NEW, "erste_zahlung": "bald"})
    assert reply["error"]["code"] == "invalid_dates"
    assert dict(entry.data) == before
