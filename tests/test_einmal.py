"""Einmalposten (Wechselbonus positiv, Maklerhonorar negativ) pro Vertrag."""

from __future__ import annotations

import pytest

from .test_coordinator import STROM
from .test_panel import GOLDEN, frontend_env  # noqa: F401  (fixture)


async def _call(client, kind, **extra):
    await client.send_json_auto_id({"type": f"tariffy/{kind}", **extra})
    return await client.receive_json()


async def test_bonus_and_fee_move_the_balance_and_the_total(frontend_env, contract, hass, hass_ws_client):  # noqa: F811
    client = await hass_ws_client()
    entry, base = await contract.setup(STROM, **GOLDEN)
    reply = await _call(client, "einmal_save", entry_id=entry.entry_id,
                        values={"bezeichnung": "Wechselbonus", "betrag": 100, "datum": "2026-02-01"})
    assert reply["success"] is True
    reply = await _call(client, "einmal_save", entry_id=entry.entry_id,
                        values={"bezeichnung": "Makler", "betrag": -30, "datum": "2026-02-01"})
    assert reply["success"] is True
    await hass.async_block_till_done()

    now = entry.runtime_data.data
    assert now["einmal_summe"] == 70.0
    assert [p["bezeichnung"] for p in now["einmalposten"]] == ["Wechselbonus", "Makler"]
    assert now["guthaben_bisher"] == pytest.approx(base["guthaben_bisher"] + 70.0, abs=0.01)
    assert now["kosten_gesamt"] == pytest.approx(base["kosten_bisher"] - 70.0, abs=0.01)
    assert now["kosten_bisher"] == base["kosten_bisher"]  # consumption cost untouched
    assert now["prognose_real"] == base["prognose_real"]  # the warning stays consumption-only


async def test_a_future_item_counts_from_its_date(frontend_env, contract, hass, hass_ws_client):  # noqa: F811
    client = await hass_ws_client()
    entry, base = await contract.setup(STROM, **GOLDEN)
    await _call(client, "einmal_save", entry_id=entry.entry_id,
                values={"bezeichnung": "Bonus", "betrag": 50, "datum": "2026-12-01"})
    await hass.async_block_till_done()
    now = entry.runtime_data.data
    assert now["einmal_summe"] == 0.0
    assert now["guthaben_bisher"] == base["guthaben_bisher"]
    assert len(now["einmalposten"]) == 1


async def test_edit_and_delete(frontend_env, contract, hass, hass_ws_client):  # noqa: F811
    client = await hass_ws_client()
    entry, _ = await contract.setup(STROM, **GOLDEN)
    await _call(client, "einmal_save", entry_id=entry.entry_id, values={"bezeichnung": "A", "betrag": 10})
    await _call(client, "einmal_save", entry_id=entry.entry_id, index=0,
                values={"bezeichnung": "B", "betrag": -5, "datum": "2026-03-01"})
    assert entry.data["_einmalposten"] == [{"bezeichnung": "B", "betrag": -5.0, "datum": "2026-03-01"}]
    assert (await _call(client, "einmal_delete", entry_id=entry.entry_id, index=3))["success"] is False
    assert (await _call(client, "einmal_delete", entry_id=entry.entry_id, index=0))["success"] is True
    assert "_einmalposten" not in entry.data


@pytest.mark.parametrize(
    ("values", "code"),
    [
        ({"bezeichnung": "", "betrag": 5}, "invalid_bezeichnung"),
        ({"bezeichnung": "X", "betrag": 0}, "invalid_betrag"),
        ({"bezeichnung": "X", "betrag": "abc"}, "invalid_betrag"),
        ({"bezeichnung": "X", "betrag": 5, "datum": "kaputt"}, "invalid_dates"),
    ],
)
async def test_bad_input_is_refused(frontend_env, contract, hass, hass_ws_client, values, code):  # noqa: F811
    client = await hass_ws_client()
    entry, _ = await contract.setup(STROM, **GOLDEN)
    reply = await _call(client, "einmal_save", entry_id=entry.entry_id, values=values)
    assert reply["success"] is False and reply["error"]["code"] == code
    assert "_einmalposten" not in entry.data
