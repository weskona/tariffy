"""Folgevertrag der Sparte Streaming: Beginn nach dem Vertragsende, Zahlweise und ein Betrag je Zahlung."""

from __future__ import annotations

import pytest
from homeassistant.data_entry_flow import FlowResultType

from .test_coordinator import STROM
from .test_panel import GOLDEN, frontend_env  # noqa: F401  (fixture)

STREAMING = {
    "sparte": "streaming", "anbieter": "Netflix", "tarif": "Standard", "abschlag": 9.99, "zahlweise": "monthly",
    "beginn": "2026-04-01", "ende": "2027-03-31", "erinnerung_monate": "0", "kundennummer": "K-1",
}
JAEHRLICH = {**STREAMING, "abschlag": 10.0, "zahlweise": "yearly"}  # 120 euro a year


async def _form(hass, entry):
    result = await hass.config_entries.options.async_init(entry.entry_id)
    assert result["type"] is FlowResultType.FORM
    return result


def _names(result):
    return [str(key) for key in result["data_schema"].schema]


def _suggested(result):
    return {
        str(key): key.description["suggested_value"]
        for key in result["data_schema"].schema
        if key.description and "suggested_value" in key.description
    }


def _defaults(result):
    return {str(key): key.default() for key in result["data_schema"].schema if hasattr(key, "default") and key.default is not vol_missing()}


def vol_missing():
    import voluptuous as vol

    return vol.UNDEFINED


async def test_the_form_asks_for_what_a_flat_contract_changes(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await contract.setup(STREAMING, **GOLDEN)
    result = await _form(hass, entry)
    assert result["step_id"] == "init_streaming"
    assert _names(result) == ["next_beginn", "next_tarif", "next_zahlweise", "next_abschlag", "next_ende"]


async def test_the_start_is_the_day_after_the_contract_end(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await contract.setup(STREAMING, **GOLDEN)
    assert _suggested(await _form(hass, entry))["next_beginn"] == "2027-04-01"
    entry2, _ = await contract.setup({**STREAMING, "ende": "2026-12-31"}, **GOLDEN)
    assert _suggested(await _form(hass, entry2))["next_beginn"] == "2027-01-01"  # over the new year
    entry3, _ = await contract.setup({k: v for k, v in STREAMING.items() if k != "ende"}, **GOLDEN)
    assert "next_beginn" not in _suggested(await _form(hass, entry3))  # no end: nothing to suggest


async def test_a_planned_start_is_not_replaced_by_the_suggestion(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await contract.setup(STREAMING, **GOLDEN, options={"next_beginn": "2027-06-01"})
    assert _suggested(await _form(hass, entry))["next_beginn"] == "2027-06-01"


async def test_the_payment_interval_defaults_to_the_current_one(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await contract.setup(JAEHRLICH, **GOLDEN)
    zahlweise = next(k for k in (await _form(hass, entry))["data_schema"].schema if str(k) == "next_zahlweise")
    assert zahlweise.default() == "yearly"


async def test_the_amount_per_payment_is_stored_per_month(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await contract.setup(JAEHRLICH, **GOLDEN)
    result = await _form(hass, entry)
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {"next_beginn": "2027-04-01", "next_zahlweise": "monthly", "next_abschlag": 12.99, "next_tarif": "Monatsabo"},
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    assert entry.options == {"next_beginn": "2027-04-01", "next_zahlweise": "monthly", "next_abschlag": 12.99, "next_tarif": "Monatsabo"}
    # yearly 120: stored as 10 a month, and shown again as 120 a payment
    result = await _form(hass, entry)
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], {"next_beginn": "2027-04-01", "next_zahlweise": "yearly", "next_abschlag": 120}
    )
    await hass.async_block_till_done()
    assert entry.options["next_abschlag"] == 10.0 and entry.options["next_zahlweise"] == "yearly"
    assert _suggested(await _form(hass, entry))["next_abschlag"] == 120.0


async def test_an_empty_start_removes_the_plan(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await contract.setup(STREAMING, **GOLDEN, options={"next_beginn": "2027-04-01", "next_abschlag": 5.0})
    result = await _form(hass, entry)
    result = await hass.config_entries.options.async_configure(result["flow_id"], {"next_zahlweise": "monthly"})
    await hass.async_block_till_done()
    assert result["type"] is FlowResultType.CREATE_ENTRY and entry.options == {}


async def test_a_plan_with_a_provider_or_a_base_price_keeps_those_fields(frontend_env, contract, hass):  # noqa: F811
    plan = {"next_beginn": "2027-04-01", "next_anbieter": "Neu AG", "next_kundennummer": "K-9", "next_grundpreis": 2.0}
    entry, _ = await contract.setup(STREAMING, **GOLDEN, options=plan)
    result = await _form(hass, entry)
    assert {"next_anbieter", "next_kundennummer", "next_grundpreis"} <= set(_names(result))
    result = await hass.config_entries.options.async_configure(result["flow_id"], dict(plan))
    await hass.async_block_till_done()
    assert entry.options["next_anbieter"] == "Neu AG" and entry.options["next_grundpreis"] == 2.0


@pytest.mark.parametrize("sparte", ["electricity", "gas", "water", "internet", "mobile", "insurance", "leasing", "other"])
async def test_the_other_categories_keep_their_form(frontend_env, contract, hass, sparte):  # noqa: F811
    """Only streaming has the short form: everything else is asked as before."""
    data = {**STROM, "sparte": sparte} if sparte in ("electricity", "gas", "water") else {**STREAMING, "sparte": sparte}
    entry, _ = await contract.setup(data, **GOLDEN)
    result = await _form(hass, entry)
    assert result["step_id"] == "init"
    assert {"next_anbieter", "next_kundennummer", "next_grundpreis", "next_abschlag", "next_ende"} <= set(_names(result))
    assert "next_zahlweise" not in _names(result)


# ------------------------------------------------------------- the switch itself
async def test_the_switch_takes_over_the_new_interval_and_amount(contract):
    options = {"next_beginn": "2027-04-01", "next_ende": "2028-03-31", "next_zahlweise": "monthly", "next_abschlag": 12.99}
    entry, _ = await contract.setup(JAEHRLICH, options=options, **{**GOLDEN, "today": "2027-04-02"})
    new = entry.data
    assert new["beginn"] == "2027-04-01" and new["zahlweise"] == "monthly" and new["abschlag"] == 12.99
    assert new["anbieter"] == "Netflix" and new["tarif"] == "Standard"  # not asked for: kept
    assert "erste_zahlung" not in new  # the new term starts with its first payment


async def test_the_switch_keeps_the_interval_when_it_is_not_changed(contract):
    entry, _ = await contract.setup(JAEHRLICH, options={"next_beginn": "2027-04-01", "next_ende": "2028-03-31"}, **{**GOLDEN, "today": "2027-04-02"})
    assert entry.data["zahlweise"] == "yearly" and entry.data["abschlag"] == 10.0  # it used to fall back to monthly


async def test_a_metered_switch_gets_no_payment_interval(contract):
    options = {"next_beginn": "2026-07-01", "next_ende": "2027-06-30", "next_abschlag": 55.0}
    entry, _ = await contract.setup(STROM, options=options, **GOLDEN)
    assert entry.data["abschlag"] == 55.0 and "zahlweise" not in entry.data


async def test_the_plan_survives_a_backup():
    from custom_components.tariffy import backup

    data = backup.sanitize_contract({"title": "Netflix", "data": STREAMING, "options": {"next_beginn": "2027-04-01", "next_zahlweise": "yearly", "next_abschlag": 10.0}})
    assert data["options"] == {"next_beginn": "2027-04-01", "next_zahlweise": "yearly", "next_abschlag": 10.0}
