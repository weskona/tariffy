"""Payment interval of flat-rate contracts: the amount per payment is converted to the monthly amount."""

from __future__ import annotations

import pytest
from homeassistant.data_entry_flow import FlowResultType

from custom_components.tariffy.const import DOMAIN

from .test_coordinator import STROM
from .test_panel import GOLDEN, frontend_env  # noqa: F401  (fixture)
from .test_reconfigure import _form_defaults, _reconfigure

INSURANCE = {
    "sparte": "insurance",
    "anbieter": "Versicherung AG",
    "abschlag": 50.0,
    "beginn": "2026-01-01",
    "ende": "2026-12-31",
    "erinnerung_monate": "3",
}


async def _create(hass, zahlweise, betrag):
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": "user"})
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"name": "Kfz", "sparte": "insurance", "anbieter": "Versicherung AG", "erinnerung_monate": "0"},
    )
    if result["step_id"] == "versicherung":  # an insurance first asks what it covers
        result = await hass.config_entries.flow.async_configure(result["flow_id"], {})
    assert result["step_id"] == "pauschal"
    names = [str(key) for key in result["data_schema"].schema]
    assert names[:2] == ["zahlweise", "abschlag"]  # the interval comes before the amount
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {"zahlweise": zahlweise, "abschlag": betrag}
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    return result["result"]


@pytest.mark.parametrize(
    ("zahlweise", "betrag", "monthly"),
    [("monthly", 50.0, 50.0), ("quarterly", 150.0, 50.0), ("halfyearly", 300.0, 50.0), ("yearly", 600.0, 50.0), ("yearly", 599.99, 49.999167)],
)
async def test_a_new_contract_stores_the_monthly_amount(hass, contract, zahlweise, betrag, monthly):
    entry = await _create(hass, zahlweise, betrag)
    assert entry.data["zahlweise"] == zahlweise
    assert entry.data["abschlag"] == pytest.approx(monthly, abs=1e-6)


async def test_the_form_shows_the_amount_per_payment(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await contract.setup({**INSURANCE, "zahlweise": "yearly", "abschlag": 49.999167}, **GOLDEN)
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "reconfigure", "entry_id": entry.entry_id}
    )
    result = await hass.config_entries.flow.async_configure(result["flow_id"], _form_defaults(result))
    while result["step_id"].startswith("reconfigure_versicherung"):
        result = await hass.config_entries.flow.async_configure(result["flow_id"], _form_defaults(result))
    assert result["step_id"] == "reconfigure_pauschal"
    defaults = _form_defaults(result)
    assert defaults["zahlweise"] == "yearly"
    assert defaults["abschlag"] == 599.99  # not 49.999167


async def test_saving_unchanged_changes_nothing_and_stamps_nothing(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await contract.setup({**INSURANCE, "zahlweise": "yearly", "abschlag": 49.999167}, **GOLDEN)
    data = await _reconfigure(hass, entry)
    assert data["abschlag"] == pytest.approx(49.999167, abs=1e-6)
    assert data["zahlweise"] == "yearly"
    assert "_abschlag_ab_datum" not in data  # no change of the instalment


async def test_an_older_contract_stays_exactly_as_it_was(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await contract.setup(dict(INSURANCE), **GOLDEN)  # no interval stored
    data = await _reconfigure(hass, entry)
    assert data["abschlag"] == 50.0
    assert data["zahlweise"] == "monthly"
    assert "_abschlag_ab_datum" not in data


async def test_a_dearer_premium_is_stamped_like_any_instalment_change(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await contract.setup({**INSURANCE, "zahlweise": "yearly"}, **GOLDEN)
    data = await _reconfigure(hass, entry, second={"abschlag": 660.0})
    assert data["abschlag"] == 55.0
    assert data["_abschlag_vorheriger_wert"] == 50.0
    assert data["_abschlag_ab_datum"] == "2026-07-12"


async def test_changing_only_the_interval_keeps_the_monthly_amount(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await contract.setup(dict(INSURANCE), **GOLDEN)  # 50 a month
    data = await _reconfigure(hass, entry, second={"zahlweise": "yearly", "abschlag": 600.0})
    assert data["abschlag"] == 50.0 and data["zahlweise"] == "yearly"
    assert "_abschlag_ab_datum" not in data  # the cost did not change, only how it is paid


async def test_energy_contracts_have_no_interval(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await contract.setup(dict(STROM), **GOLDEN)
    data = await _reconfigure(hass, entry)
    assert "zahlweise" not in data


async def test_filling_in_the_amount_later_is_no_price_change(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await contract.setup({**INSURANCE, "abschlag": 0.0}, **GOLDEN)  # 0 is the default when creating
    data = await _reconfigure(hass, entry, second={"abschlag": 50.0})
    assert data["abschlag"] == 50.0
    assert "_abschlag_ab_datum" not in data and "_abschlag_vorheriger_wert" not in data


async def test_the_date_of_the_first_debit_is_stored_and_can_be_removed(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await contract.setup({**INSURANCE, "zahlweise": "yearly"}, **GOLDEN)
    data = await _reconfigure(hass, entry, second={"erste_zahlung": "2026-02-10"})
    assert data["erste_zahlung"] == "2026-02-10"
    assert entry.runtime_data.data["erste_zahlung"].isoformat() == "2026-02-10"
    data = await _reconfigure(hass, entry, drop=("erste_zahlung",))
    assert "erste_zahlung" not in data


async def test_the_form_has_the_field_for_the_first_debit(frontend_env, contract, hass):  # noqa: F811
    entry, _ = await contract.setup(dict(INSURANCE), **GOLDEN)
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "reconfigure", "entry_id": entry.entry_id}
    )
    result = await hass.config_entries.flow.async_configure(result["flow_id"], _form_defaults(result))
    while result["step_id"].startswith("reconfigure_versicherung"):
        result = await hass.config_entries.flow.async_configure(result["flow_id"], _form_defaults(result))
    names = [str(key) for key in result["data_schema"].schema]
    assert names.index("abschlag") < names.index("erste_zahlung") < names.index("grundpreis")
