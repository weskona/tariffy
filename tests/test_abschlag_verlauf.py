"""Abschlagsverlauf: der Versorger hat den Abschlag selbst geaendert, der Nutzer traegt ein, was wann gezahlt wurde."""

from __future__ import annotations

from datetime import date

import pytest

from custom_components.tariffy import backup, history
from custom_components.tariffy import coordinator as coord

from .test_coordinator import STROM
from .test_panel import GOLDEN, frontend_env  # noqa: F401  (fixture)
from .test_reconfigure import _reconfigure

HEUTE = "2026-11-18"  # 321 days after the start
TAG = {**GOLDEN, "today": HEUTE}
# gas as in the report: months 1-7 178 euro, month 8 174.41, months 9-11 215 (the current one)
VERLAUF = [
    {"ab": "2026-01-01", "betrag": 178.0},
    {"ab": "2026-08-01", "betrag": 174.41},
    {"ab": "2026-09-01", "betrag": 215.0},
]
GAS = {**STROM, "sparte": "gas", "abschlag": 215.0, "_abschlag_verlauf": VERLAUF}
INTERNET = {
    "sparte": "internet", "anbieter": "Glasfaser", "abschlag": 215.0, "beginn": "2026-01-01",
    "ende": "2026-12-31", "erinnerung_monate": "0", "_abschlag_verlauf": VERLAUF,
}


def _monate(ab: str, bis: str = "2026-01-01") -> float:
    return (date.fromisoformat(ab) - date.fromisoformat(bis)).days / 30.44


async def _call(client, kind="abschlag_verlauf_save", **extra):
    await client.send_json_auto_id({"type": f"tariffy/{kind}", **extra})
    return await client.receive_json()


# ---------------------------------------------------------------- the pure calculation
def test_the_plan_is_sorted_one_entry_per_day_and_junk_is_ignored():
    data = {"_abschlag_verlauf": [
        {"ab": "2026-08-01", "betrag": 174.41}, {"ab": "2026-01-01", "betrag": 178}, {"ab": "2026-08-01", "betrag": 170},
        {"ab": "kaputt", "betrag": 5}, {"ab": "2026-03-01", "betrag": -1}, {"ab": "2026-03-01"}, "x", None,
    ]}
    assert coord.abschlag_plan(data) == [(date(2026, 1, 1), 178.0), (date(2026, 8, 1), 170.0)]  # the later one of a day wins
    assert coord.abschlag_plan({}) == [] and coord.abschlag_plan({"_abschlag_verlauf": "x"}) == []


def test_which_amount_applied_on_a_day():
    plan = coord.abschlag_plan({"_abschlag_verlauf": VERLAUF})
    assert coord._abschlag_am(plan, 215.0, date(2026, 3, 1)) == 178.0
    assert coord._abschlag_am(plan, 215.0, date(2026, 7, 31)) == 178.0
    assert coord._abschlag_am(plan, 215.0, date(2026, 8, 1)) == 174.41
    assert coord._abschlag_am(plan, 215.0, date(2026, 8, 31)) == 174.41
    assert coord._abschlag_am(plan, 215.0, date(2026, 9, 1)) == 215.0  # the last entry is the current instalment
    assert coord._abschlag_am(plan, 215.0, date(2025, 12, 1)) == 178.0  # before the first entry: its amount


def test_the_paid_so_far_follows_the_periods():
    """By hand (months = days / 30.44 as everywhere): 178 until 1 Aug, 174.41 until 1 Sep, 215 after, 321 days in."""
    plan = coord.abschlag_plan({"_abschlag_verlauf": VERLAUF})
    v = 321 / 30.44
    erwartet = 178 * _monate("2026-08-01") + 174.41 * (_monate("2026-09-01") - _monate("2026-08-01")) + 215 * (v - _monate("2026-09-01"))
    assert coord._abschlag_aus_plan(plan, 215.0, v, date(2026, 1, 1)) == pytest.approx(erwartet, abs=0.001)
    assert erwartet == pytest.approx(1968.2, abs=0.1)


def test_a_single_entry_is_the_old_calculation():
    plan = [(date(2026, 1, 1), 40.0)]
    assert coord._abschlag_aus_plan(plan, 40.0, 6.5, date(2026, 1, 1)) == pytest.approx(40 * 6.5)


def test_the_time_before_the_first_entry_uses_its_amount():
    plan = [(date(2026, 4, 1), 100.0), (date(2026, 7, 1), 120.0)]
    v = 200 / 30.44  # 200 days: the first entry begins after 90 days, the second after 181
    erwartet = 100 * _monate("2026-07-01") + 120 * (v - _monate("2026-07-01"))
    assert coord._abschlag_aus_plan(plan, 120.0, v, date(2026, 1, 1)) == pytest.approx(erwartet, abs=0.001)


def test_entries_after_today_do_not_count_yet():
    plan = [(date(2026, 1, 1), 100.0), (date(2026, 12, 1), 200.0)]
    assert coord._abschlag_aus_plan(plan, 200.0, 3.0, date(2026, 1, 1)) == pytest.approx(300.0)


# ---------------------------------------------------------------- the running contract
async def test_a_metered_contract_uses_the_instalments_that_were_paid(contract):
    _, d = await contract.setup(GAS, **TAG)
    assert d["abschlag_bisher_gezahlt"] == pytest.approx(1968.2, abs=0.1)
    assert d["guthaben_bisher"] == pytest.approx(d["abschlag_bisher_gezahlt"] - d["kosten_bisher"], abs=0.02)
    assert [(e["ab"], e["betrag"]) for e in d["abschlagsverlauf"]] == [(e["ab"], e["betrag"]) for e in VERLAUF]


async def test_without_a_history_the_old_calculation_stays(contract):
    plain = {k: v for k, v in GAS.items() if k != "_abschlag_verlauf"}
    _, d = await contract.setup(plain, **TAG)
    assert d["abschlag_bisher_gezahlt"] == pytest.approx(215 * 321 / 30.44, abs=0.01)
    assert d["abschlagsverlauf"] == []
    _, e = await contract.setup({**plain, "_abschlag_verlauf": []}, **TAG)  # an empty list is no history
    assert e["abschlag_bisher_gezahlt"] == d["abschlag_bisher_gezahlt"]


async def test_the_old_single_change_still_works_without_a_history(contract):
    stamp = {k: v for k, v in GAS.items() if k != "_abschlag_verlauf"} | {"_abschlag_ab_datum": "2026-09-01", "_abschlag_vorheriger_wert": 178.0}
    _, d = await contract.setup(stamp, **TAG)
    v = 321 / 30.44
    assert d["abschlag_bisher_gezahlt"] == pytest.approx(178 * _monate("2026-09-01") + 215 * (v - _monate("2026-09-01")), abs=0.01)


async def test_the_history_replaces_the_single_change(contract):
    both = {**GAS, "_abschlag_ab_datum": "2026-10-01", "_abschlag_vorheriger_wert": 1.0}
    _, d = await contract.setup(both, **TAG)
    assert d["abschlag_bisher_gezahlt"] == pytest.approx(1968.2, abs=0.1)


async def test_the_forecast_follows_the_history(contract):
    _, mit = await contract.setup(GAS, **TAG)
    _, ohne = await contract.setup({k: v for k, v in GAS.items() if k != "_abschlag_verlauf"}, **TAG)
    # less was paid so far than the current amount would give: the recommended instalment goes up
    assert mit["abschlag_bisher_gezahlt"] < ohne["abschlag_bisher_gezahlt"]
    assert mit["prognose_real"] < ohne["prognose_real"]


async def test_a_flat_contract_counts_every_instalment_with_the_amount_of_its_month(contract):
    """Jan to Jul 178 (7), Aug 174.41, Sep to Nov 215 (3): the 11 instalments due by 18 November."""
    _, d = await contract.setup(INTERNET, **TAG)
    assert d["abschlag_bisher_gezahlt"] == pytest.approx(7 * 178 + 174.41 + 3 * 215, abs=0.01)


async def test_a_quarterly_flat_contract_uses_the_amount_at_each_debit(contract):
    data = {**INTERNET, "zahlweise": "quarterly", "abschlag": 120.0,
            "_abschlag_verlauf": [{"ab": "2026-01-01", "betrag": 100.0}, {"ab": "2026-07-01", "betrag": 120.0}]}
    _, d = await contract.setup(data, **TAG)
    assert d["abschlag_bisher_gezahlt"] == pytest.approx(3 * 100 * 2 + 3 * 120 * 2, abs=0.01)  # debits 1 Jan, 1 Apr, 1 Jul, 1 Oct


async def test_junk_in_the_history_is_ignored(contract):
    _, d = await contract.setup({**GAS, "_abschlag_verlauf": ["x", {"ab": "kaputt"}, *VERLAUF]}, **TAG)
    assert d["abschlag_bisher_gezahlt"] == pytest.approx(1968.2, abs=0.1)


# ---------------------------------------------------------------- the panel command
async def test_save_sets_the_history_and_the_current_instalment(frontend_env, contract, hass, hass_ws_client):  # noqa: F811
    client = await hass_ws_client()
    entry, _ = await contract.setup({k: v for k, v in GAS.items() if k != "_abschlag_verlauf"} | {"abschlag": 178.0}, **TAG)
    rows = [{"ab": "2026-09-01", "betrag": "215"}, {"ab": "2026-01-01", "betrag": 178}, {"ab": "2026-08-01", "betrag": 174.41}]
    reply = await _call(client, entry_id=entry.entry_id, rows=rows)
    assert reply["success"] is True
    await hass.async_block_till_done()
    assert entry.data["_abschlag_verlauf"] == VERLAUF  # sorted by date
    assert entry.data["abschlag"] == 215.0  # the newest entry is the current instalment
    assert entry.runtime_data.data["abschlag_bisher_gezahlt"] == pytest.approx(1968.2, abs=0.1)


async def test_an_empty_list_removes_the_history(frontend_env, contract, hass, hass_ws_client):  # noqa: F811
    client = await hass_ws_client()
    entry, _ = await contract.setup(GAS, **TAG)
    assert (await _call(client, entry_id=entry.entry_id, rows=[]))["success"] is True
    assert "_abschlag_verlauf" not in entry.data and entry.data["abschlag"] == 215.0  # the amount stays


async def test_a_quarterly_contract_takes_the_amount_per_payment(frontend_env, contract, hass, hass_ws_client):  # noqa: F811
    client = await hass_ws_client()
    entry, _ = await contract.setup({k: v for k, v in INTERNET.items() if k != "_abschlag_verlauf"} | {"zahlweise": "quarterly"}, **TAG)
    await _call(client, entry_id=entry.entry_id, rows=[{"ab": "2026-01-01", "betrag": 300}])
    assert entry.data["_abschlag_verlauf"] == [{"ab": "2026-01-01", "betrag": 100.0}]  # stored per month
    await hass.async_block_till_done()
    assert entry.runtime_data.data["abschlagsverlauf"][0]["betrag_je_zahlung"] == 300.0


@pytest.mark.parametrize(
    ("rows", "code"),
    [
        ([{"ab": "2026-12-01", "betrag": 200}], "invalid_dates"),  # in the future
        ([{"ab": "kaputt", "betrag": 200}], "invalid_dates"),
        ([{"ab": "2026-01-01", "betrag": 100}, {"ab": "2026-01-01", "betrag": 120}], "invalid_dates"),  # the same day twice
        ([{"ab": "2026-01-01", "betrag": 0}], "invalid_abschlag"),
        ([{"ab": "2026-01-01", "betrag": -5}], "invalid_abschlag"),
        ([{"ab": "2026-01-01", "betrag": "abc"}], "invalid_abschlag"),
        ([{"ab": "2026-01-01"}], "invalid_abschlag"),
        ([{"ab": "2020-01-01", "betrag": 1}] * 61, "too_many"),
    ],
)
async def test_bad_rows_are_refused_and_nothing_changes(frontend_env, contract, hass, hass_ws_client, rows, code):  # noqa: F811
    client = await hass_ws_client()
    entry, _ = await contract.setup(GAS, **TAG)
    reply = await _call(client, entry_id=entry.entry_id, rows=rows)
    assert reply["success"] is False and reply["error"]["code"] == code
    assert entry.data["_abschlag_verlauf"] == VERLAUF and entry.data["abschlag"] == 215.0


async def test_a_loan_has_no_instalment_history(frontend_env, contract, hass, hass_ws_client):  # noqa: F811
    client = await hass_ws_client()
    loan = {"sparte": "loan", "anbieter": "Bank", "kredit_summe": 1000.0, "sollzins": 5.0, "laufzeit_monate": 12,
            "zahlweise": "monthly", "beginn": "2026-01-01", "erinnerung_monate": "0"}
    entry, _ = await contract.setup(loan, **TAG)
    reply = await _call(client, entry_id=entry.entry_id, rows=[{"ab": "2026-01-01", "betrag": 5}])
    assert reply["success"] is False and reply["error"]["code"] == "not_available"


async def test_only_administrators_may_save(frontend_env, contract, hass, hass_ws_client, hass_read_only_access_token):  # noqa: F811
    client = await hass_ws_client(access_token=hass_read_only_access_token)
    entry, _ = await contract.setup(GAS, **TAG)
    reply = await _call(client, entry_id=entry.entry_id, rows=[])
    assert reply["success"] is False and reply["error"]["code"] == "unauthorized"
    assert entry.data["_abschlag_verlauf"] == VERLAUF


async def test_an_unknown_contract_is_refused(frontend_env, contract, hass, hass_ws_client):  # noqa: F811
    client = await hass_ws_client()
    await contract.setup(GAS, **TAG)
    assert (await _call(client, entry_id="gibtsnicht", rows=[]))["error"]["code"] == "not_found"


async def test_the_panel_gets_the_history(frontend_env, contract, hass):  # noqa: F811
    from custom_components.tariffy import panel

    entry, _ = await contract.setup(GAS, **TAG)
    payload = panel.contract_payload(hass, entry)
    assert [e["ab"] for e in payload["abschlagsverlauf"]] == ["2026-01-01", "2026-08-01", "2026-09-01"]
    assert "_abschlag_verlauf" not in payload  # the raw internal list is not sent


# ---------------------------------------------------------------- editing, renewing, switching, backup
async def test_editing_keeps_the_history(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await contract.setup(GAS, **TAG)
    data = await _reconfigure(hass, entry)
    assert data["_abschlag_verlauf"] == VERLAUF and data["abschlag"] == 215.0


async def test_a_new_instalment_in_the_form_adds_an_entry(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await contract.setup(GAS, **TAG)
    data = await _reconfigure(hass, entry, second={"abschlag": 230.0})
    assert data["abschlag"] == 230.0
    assert data["_abschlag_verlauf"] == [*VERLAUF, {"ab": HEUTE, "betrag": 230.0}]
    # a correction on the same day replaces that entry instead of adding another one
    data = await _reconfigure(hass, entry, second={"abschlag": 225.0})
    assert data["_abschlag_verlauf"] == [*VERLAUF, {"ab": HEUTE, "betrag": 225.0}]


async def test_an_unchanged_instalment_adds_nothing(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await contract.setup(GAS, **TAG)
    assert (await _reconfigure(hass, entry))["_abschlag_verlauf"] == VERLAUF


async def test_a_renewed_term_starts_without_the_old_history(frontend_env, contract, hass, hass_ws_client):  # noqa: F811
    client = await hass_ws_client()
    entry, _ = await contract.setup(INTERNET, **TAG)
    reply = await _call(client, "renew", entry_id=entry.entry_id,
                        values={"beginn": "2027-01-01", "ende": "2027-12-31", "abschlag": 250.0})
    assert reply["success"] is True
    await hass.async_block_till_done()
    assert "_abschlag_verlauf" not in entry.data and entry.data["abschlag"] == 250.0
    assert len(entry.data["_historie"]) == 1


async def test_a_tariff_switch_starts_without_the_old_history(contract):
    options = {"next_beginn": "2026-11-01", "next_ende": "2027-10-31", "next_anbieter": "Neu", "next_abschlag": 190.0}
    entry, _ = await contract.setup(GAS, options=options, **TAG)
    assert entry.data["anbieter"] == "Neu" and entry.data["abschlag"] == 190.0
    assert "_abschlag_verlauf" not in entry.data


def test_the_history_survives_a_backup():
    data = backup.sanitize_contract({"title": "Gas", "data": GAS})["data"]
    assert data["_abschlag_verlauf"] == VERLAUF


# ---------------------------------------------------------------- an earlier term entered by hand, with its instalments by month
ALT = {"beginn": "2025-03-01", "ende": "2026-02-28", "arbeitspreis": 0.30, "grundpreis": 10.0}  # 364 days
ALT_ROWS = [
    {"ab": "2025-03-01", "betrag": 178}, {"ab": "2025-08-01", "betrag": "174.41"}, {"ab": "2025-09-01", "betrag": 215},
]


def _alt_gezahlt() -> float:
    """By hand (days / 30.44): 178 until 1 Aug, 174.41 until 1 Sep, 215 until the end after 364 days."""
    a, b, v = 153 / 30.44, 184 / 30.44, 364 / 30.44
    return 178 * a + 174.41 * (b - a) + 215 * (v - b)


async def test_an_old_term_works_out_what_was_paid_from_the_months(contract, hass):
    entry, _ = await contract.setup(GAS, **TAG)
    calc = await history.async_calc(hass, entry, ALT, ALT_ROWS)
    assert calc["values"]["abschlag_gezahlt"] == pytest.approx(_alt_gezahlt(), abs=0.01)
    assert _alt_gezahlt() == pytest.approx(2343.6, abs=0.2)
    # without the months the old calculation: the typed instalment for the whole term
    plain = await history.async_calc(hass, entry, {**ALT, "abschlag": 215.0})
    assert plain["values"]["abschlag_gezahlt"] == pytest.approx(215 * round(364 / 30.44, 2), abs=0.01)  # months rounded as before


async def test_a_typed_amount_paid_wins_over_the_months(contract, hass):
    entry, _ = await contract.setup(GAS, **TAG)
    calc = await history.async_calc(hass, entry, {**ALT, "abschlag_gezahlt": 2000.0}, ALT_ROWS)
    assert calc["values"]["abschlag_gezahlt"] == 2000.0


async def test_the_balance_of_an_old_term_follows_the_months(contract, hass):
    entry, _ = await contract.setup(GAS, **TAG)
    calc = await history.async_calc(hass, entry, {**ALT, "kosten": 2000.0}, ALT_ROWS)
    assert calc["values"]["saldo"] == pytest.approx(_alt_gezahlt() - 2000.0, abs=0.01)


async def test_saving_an_old_term_keeps_the_months_for_editing(frontend_env, contract, hass, hass_ws_client):  # noqa: F811
    client = await hass_ws_client()
    entry, _ = await contract.setup(GAS, **TAG)
    reply = await _call(client, "history_save", entry_id=entry.entry_id, values=ALT, rows=ALT_ROWS)
    assert reply["success"] is True
    term = entry.data["_historie"][0]
    assert term["abschlag_gezahlt"] == pytest.approx(_alt_gezahlt(), abs=0.01)
    assert term["abschlag"] == 215.0  # the instalment at the end of the term
    assert term["abschlag_verlauf"] == [
        {"ab": "2025-03-01", "betrag": 178.0}, {"ab": "2025-08-01", "betrag": 174.41}, {"ab": "2025-09-01", "betrag": 215.0},
    ]
    assert term["eigene"] == []  # nothing typed: the paid amount is worked out again when it is edited
    # the panel gets the stored months with the term
    from custom_components.tariffy import panel

    assert panel.contract_payload(hass, entry)["historie"][0]["abschlag_verlauf"][1]["betrag"] == 174.41
    assert entry.data["_abschlag_verlauf"] == VERLAUF and entry.data["abschlag"] == 215.0  # the running contract is untouched


async def test_a_term_without_months_is_as_before(frontend_env, contract, hass, hass_ws_client):  # noqa: F811
    client = await hass_ws_client()
    entry, _ = await contract.setup(GAS, **TAG)
    await _call(client, "history_save", entry_id=entry.entry_id, values={**ALT, "abschlag": 100.0})
    term = entry.data["_historie"][0]
    assert term["abschlag"] == 100.0 and "abschlag_verlauf" not in term
    assert term["abschlag_gezahlt"] == pytest.approx(100 * round(364 / 30.44, 2), abs=0.01)


@pytest.mark.parametrize(
    ("rows", "code"),
    [
        ([{"ab": "2026-03-01", "betrag": 200}], "invalid_dates"),  # after the end of the term
        ([{"ab": "kaputt", "betrag": 200}], "invalid_dates"),
        ([{"ab": "2025-03-01", "betrag": 100}, {"ab": "2025-03-01", "betrag": 120}], "invalid_dates"),
        ([{"ab": "2025-03-01", "betrag": 0}], "invalid_abschlag"),
        ([{"ab": "2025-03-01", "betrag": "abc"}], "invalid_abschlag"),
        ([{"ab": "2020-01-01", "betrag": 1}] * 61, "too_many"),
    ],
)
async def test_bad_months_of_an_old_term_are_refused(frontend_env, contract, hass, hass_ws_client, rows, code):  # noqa: F811
    client = await hass_ws_client()
    entry, _ = await contract.setup(GAS, **TAG)
    for kind in ("history_calc", "history_save"):
        reply = await _call(client, kind, entry_id=entry.entry_id, values=ALT, rows=rows)
        assert reply["success"] is False and reply["error"]["code"] == code, kind
    assert "_historie" not in entry.data


async def test_an_old_flat_term_counts_every_debit_with_its_amount(contract, hass):
    """Debits on the 1st from March 2025 to February 2026 (12): five of 178, one of 174.41, six of 215."""
    entry, _ = await contract.setup(INTERNET, **TAG)
    calc = await history.async_calc(hass, entry, ALT, ALT_ROWS)
    erwartet = 5 * 178 + 174.41 + 6 * 215
    assert calc["values"]["kosten"] == calc["values"]["abschlag_gezahlt"] == pytest.approx(erwartet, abs=0.01)


async def test_an_old_yearly_term_has_one_payment(contract, hass):
    data = {**INTERNET, "zahlweise": "yearly", "abschlag": 100.0, "_abschlag_verlauf": [{"ab": "2025-01-01", "betrag": 100.0}]}
    entry, _ = await contract.setup(data, **TAG)
    calc = await history.async_calc(hass, entry, ALT, [{"ab": "2025-03-01", "betrag": 1200}])
    assert calc["values"]["abschlag_gezahlt"] == 1200.0  # one debit of the year, not twelve months of 100 prorated


async def test_an_old_quarterly_term_counts_four_payments(contract, hass):
    data = {**INTERNET, "zahlweise": "quarterly", "abschlag": 100.0, "_abschlag_verlauf": [{"ab": "2025-01-01", "betrag": 100.0}]}
    entry, _ = await contract.setup(data, **TAG)
    rows = [{"ab": "2025-03-01", "betrag": 300}, {"ab": "2025-09-01", "betrag": 330}]  # debits 1 Mar, 1 Jun, 1 Sep, 1 Dec
    calc = await history.async_calc(hass, entry, ALT, rows)
    assert calc["values"]["abschlag_gezahlt"] == 2 * 300 + 2 * 330
