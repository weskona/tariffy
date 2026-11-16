"""Alte Laufzeiten von Hand eintragen: automatisch ermittelte und eigene Werte."""

from __future__ import annotations

from datetime import date
from unittest.mock import patch

import pytest

from custom_components.tariffy import history

from .test_coordinator import SENSOR, STROM
from .test_panel import GOLDEN, frontend_env  # noqa: F401  (fixture)

COORDINATOR = "custom_components.tariffy.coordinator"
SENSOR_NT = "sensor.strom_nt"

# the meter statistics of the old term: (sum, state) at the start and the day after the end
STATS = {
    SENSOR: {date(2024, 1, 1): (1000.0, 1000.0), date(2025, 1, 1): (4200.0, 4200.0)},
    SENSOR_NT: {date(2024, 1, 1): (500.0, 500.0), date(2025, 1, 1): (800.0, 800.0)},
}
TERM = {"beginn": "2024-01-01", "ende": "2024-12-31", "arbeitspreis": 0.30, "grundpreis": 10.0, "abschlag": 90.0}
MONTHS = round(365 / 30.44, 2)


def _statistics(stats=STATS):
    async def fake(_hass, entity_id, at_date):
        return stats.get(entity_id, {}).get(at_date, (None, None))

    return patch(f"{COORDINATOR}._get_historic_value", fake)


async def _calc(hass, entry, **values):
    with _statistics():
        return await history.async_calc(hass, entry, {**TERM, **values})


async def test_everything_is_worked_out_from_the_statistics(contract, hass):
    entry, _ = await contract.setup(STROM, **GOLDEN)
    result = await _calc(hass, entry)
    assert result["source"] == "statistics"
    assert result["sensors"] == [SENSOR]
    assert result["months"] == MONTHS
    values = result["values"]
    assert values["verbrauch"] == pytest.approx(3200.0)
    assert values["abschlag_gezahlt"] == pytest.approx(round(90.0 * MONTHS, 2))
    assert values["kosten"] == pytest.approx(round(3200.0 * 0.30 + 10.0 * MONTHS, 2))
    assert values["saldo"] == pytest.approx(round(values["abschlag_gezahlt"] - values["kosten"], 2))


async def test_a_value_entered_by_hand_wins_and_the_rest_follows_from_it(contract, hass):
    entry, _ = await contract.setup(STROM, **GOLDEN)
    result = await _calc(hass, entry, verbrauch=3000)
    assert result["source"] == "manual"
    assert result["values"]["verbrauch"] == 3000.0
    assert result["values"]["kosten"] == pytest.approx(round(3000.0 * 0.30 + 10.0 * MONTHS, 2))

    result = await _calc(hass, entry, kosten=1000, abschlag_gezahlt=1100)
    assert result["values"]["kosten"] == 1000.0
    assert result["values"]["saldo"] == 100.0  # 1100 paid - 1000 cost

    result = await _calc(hass, entry, saldo=-12.5)
    assert result["values"]["saldo"] == -12.5


async def test_without_statistics_only_what_can_be_calculated_is_filled(contract, hass):
    entry, _ = await contract.setup(STROM, **GOLDEN)
    with _statistics({}):
        result = await history.async_calc(hass, entry, dict(TERM))
    assert result["source"] is None
    assert result["values"]["verbrauch"] is None
    assert result["values"]["kosten"] is None and result["values"]["saldo"] is None
    assert result["values"]["abschlag_gezahlt"] == pytest.approx(round(90.0 * MONTHS, 2))
    # with the consumption typed in, the cost can be worked out after all
    with _statistics({}):
        result = await history.async_calc(hass, entry, {**TERM, "verbrauch": 3000})
    assert result["values"]["kosten"] is not None


async def test_a_flat_rate_contract_costs_what_was_paid(contract, hass):
    internet = {"sparte": "internet", "anbieter": "Glasfaser", "abschlag": 40.0, "beginn": "2026-01-01", "ende": "2026-12-31"}
    entry, _ = await contract.setup(internet, **GOLDEN)
    with _statistics({}):
        result = await history.async_calc(hass, entry, {"beginn": "2024-01-01", "ende": "2024-12-31", "abschlag": 40.0})
    values = result["values"]
    assert values["abschlag_gezahlt"] == pytest.approx(round(40.0 * MONTHS, 2))
    assert values["kosten"] == values["abschlag_gezahlt"]
    assert values["verbrauch"] is None and values["saldo"] is None
    assert result["source"] is None


async def test_gas_is_converted_to_kwh_for_the_cost(contract, hass):
    gas = {**STROM, "sparte": "gas", "brennwert": "10", "zustandszahl": "0.9", "gas_einheit": "m³"}
    entry, _ = await contract.setup(gas, **GOLDEN)
    result = await _calc(hass, entry)
    assert result["values"]["verbrauch"] == pytest.approx(3200.0)  # m³, as the meter counts
    assert result["values"]["kosten"] == pytest.approx(round(3200.0 * 10 * 0.9 * 0.30 + 10.0 * MONTHS, 2))


async def test_both_registers_of_a_dual_tariff_are_added(contract, hass):
    ht_nt = {**STROM, "sparte": "electricity_ht_nt", "verbrauch_sensor_nt": SENSOR_NT}
    entry, _ = await contract.setup(ht_nt, **GOLDEN)
    result = await _calc(hass, entry)
    assert result["values"]["verbrauch"] == pytest.approx(3200.0 + 300.0)
    assert result["sensors"] == [SENSOR, SENSOR_NT]


@pytest.mark.parametrize(
    ("values", "code"),
    [
        ({"ende": "2023-12-31"}, "invalid_dates"),  # ends before it starts
        ({"beginn": "kein Datum"}, "invalid_dates"),
        ({"arbeitspreis": -1}, "invalid_arbeitspreis"),
        ({"abschlag": "viel"}, "invalid_abschlag"),
        ({"verbrauch": float("nan")}, "invalid_verbrauch"),
    ],
)
async def test_unusable_input_is_refused(contract, hass, values, code):
    entry, _ = await contract.setup(STROM, **GOLDEN)
    with pytest.raises(history.HistoryError) as err:
        await _calc(hass, entry, **values)
    assert err.value.code == code


async def _call(client, type_, **extra):
    await client.send_json_auto_id({"type": f"tariffy/{type_}", **extra})
    return await client.receive_json()


class TestPanelCommands:
    async def test_calc_save_edit_and_delete(self, frontend_env, contract, hass, hass_ws_client):  # noqa: F811
        client = await hass_ws_client()
        entry, _ = await contract.setup(STROM, **GOLDEN)
        id_ = entry.entry_id

        with _statistics():
            reply = await _call(client, "history_calc", entry_id=id_, values=TERM)
        assert reply["success"] is True
        assert reply["result"]["values"]["verbrauch"] == pytest.approx(3200.0)
        assert "_historie" not in entry.data  # a preview stores nothing

        with _statistics():
            reply = await _call(client, "history_save", entry_id=id_, values={**TERM, "anbieter": "Alt AG", "tarif": "Basis"})
        assert reply["success"] is True and reply["result"]["index"] == 0
        (term,) = entry.data["_historie"]
        assert term["anbieter"] == "Alt AG" and term["tarif"] == "Basis"
        assert term["manuell"] is True and term["quelle"] == "statistics"
        assert term["eigene"] == []  # nothing typed in: everything was worked out
        assert term["verbrauch"] == pytest.approx(3200.0)
        assert term["sparte"] == "electricity"
        assert not {"kundennummer", "zaehlernummer", "notify_target"} & set(term)
        assert entry.runtime_data.data["historie"] == entry.data["_historie"]  # the panel sees it

        # an earlier term is put in front (the list is ordered by start date)
        earlier = {"beginn": "2022-01-01", "ende": "2022-12-31", "abschlag": 70.0, "anbieter": "Noch älter"}
        with _statistics({}):
            reply = await _call(client, "history_save", entry_id=id_, values=earlier)
        assert reply["result"]["index"] == 0
        assert [t["anbieter"] for t in entry.data["_historie"]] == ["Noch älter", "Alt AG"]

        # editing replaces the entry at that position
        with _statistics():
            reply = await _call(client, "history_save", entry_id=id_, index=1, values={**TERM, "anbieter": "Alt AG", "verbrauch": 3000})
        assert reply["success"] is True
        assert entry.data["_historie"][1]["verbrauch"] == 3000.0
        assert entry.data["_historie"][1]["quelle"] == "manual"
        assert entry.data["_historie"][1]["eigene"] == ["verbrauch"]
        assert len(entry.data["_historie"]) == 2

        reply = await _call(client, "history_delete", entry_id=id_, index=0)
        assert reply["success"] is True
        assert [t["anbieter"] for t in entry.data["_historie"]] == ["Alt AG"]
        reply = await _call(client, "history_delete", entry_id=id_, index=0)
        assert reply["success"] is True
        assert "_historie" not in entry.data

    async def test_errors(self, frontend_env, contract, hass, hass_ws_client):  # noqa: F811
        client = await hass_ws_client()
        entry, _ = await contract.setup(STROM, **GOLDEN)
        id_ = entry.entry_id
        reply = await _call(client, "history_save", entry_id=id_, values={**TERM, "ende": "2020-01-01"})
        assert reply["error"]["code"] == "invalid_dates"
        reply = await _call(client, "history_save", entry_id="does-not-exist", values=TERM)
        assert reply["error"]["code"] == "not_found"
        reply = await _call(client, "history_save", entry_id=id_, index=3, values=TERM)
        assert reply["error"]["code"] == "not_found"
        reply = await _call(client, "history_delete", entry_id=id_, index=0)
        assert reply["error"]["code"] == "not_found"
        reply = await _call(client, "history_calc", entry_id="does-not-exist", values=TERM)
        assert reply["error"]["code"] == "not_found"
        assert "_historie" not in entry.data

    async def test_too_many_terms(self, frontend_env, contract, hass, hass_ws_client):  # noqa: F811
        client = await hass_ws_client()
        full = [{"beginn": f"2000-{i // 28 + 1:02d}-{i % 28 + 1:02d}", "ende": "2000-12-31"} for i in range(50)]
        entry, _ = await contract.setup({**STROM, "_historie": full}, **GOLDEN)
        reply = await _call(client, "history_save", entry_id=entry.entry_id, values=TERM)
        assert reply["error"]["code"] == "too_many"
        assert len(entry.data["_historie"]) == 50

    async def test_only_administrators(
        self, frontend_env, contract, hass, hass_ws_client, hass_read_only_access_token  # noqa: F811
    ):
        client = await hass_ws_client(hass, hass_read_only_access_token)
        entry, _ = await contract.setup(STROM, **GOLDEN)
        for type_, extra in (
            ("history_calc", {"values": TERM}),
            ("history_save", {"values": TERM}),
            ("history_delete", {"index": 0}),
        ):
            reply = await _call(client, type_, entry_id=entry.entry_id, **extra)
            assert reply["error"]["code"] == "unauthorized"
        assert "_historie" not in entry.data

    async def test_editing_the_archived_term_keeps_the_archive_marker(
        self, frontend_env, contract, hass, hass_ws_client  # noqa: F811
    ):
        client = await hass_ws_client()
        entry, _ = await contract.setup(STROM, **{**GOLDEN, "today": "2027-02-01"})
        await entry.runtime_data.async_archive()
        (term,) = entry.data["_historie"]
        assert term["archiviert"] is True
        values = {"beginn": term["beginn"], "ende": term["ende"], "abschlag": 40.0, "kosten": 500, "abschlag_gezahlt": 480}
        reply = await _call(client, "history_save", entry_id=entry.entry_id, index=0, values=values)
        assert reply["success"] is True
        assert entry.data["_historie"][0]["archiviert"] is True
        assert entry.data["_historie"][0]["kosten"] == 500.0

    async def test_restoring_removes_the_archive_entry_even_if_it_is_not_the_last(
        self, frontend_env, contract, hass, hass_ws_client  # noqa: F811
    ):
        client = await hass_ws_client()
        entry, _ = await contract.setup(STROM, **{**GOLDEN, "today": "2027-02-01"})
        await entry.runtime_data.async_archive()
        later = {"beginn": "2030-01-01", "ende": "2030-12-31", "anbieter": "Später"}
        reply = await _call(client, "history_save", entry_id=entry.entry_id, values=later)
        assert reply["success"] is True
        assert entry.data["_historie"][-1]["anbieter"] == "Später"  # sorted behind the archived term
        await entry.runtime_data.async_restore()
        assert [t.get("anbieter") for t in entry.data["_historie"]] == ["Später"]
        assert "_archiviert" not in entry.data
