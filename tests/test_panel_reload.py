"""Issue 102: after a contract was created or changed the open panel stayed empty until another contract was reloaded.

A panel that is open is told about the contracts every time `SIGNAL_CONTRACTS` fires (`tariffy/subscribe`). These tests
record what such a panel would have been shown at every signal."""

from __future__ import annotations

import pytest
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from custom_components.tariffy.panel import SIGNAL_CONTRACTS, async_contracts

from .test_coordinator import STROM
from .test_panel import GOLDEN, frontend_env  # noqa: F401  (fixture)


@pytest.fixture
def shown(hass):
    """The list of entry ids the open panel was shown, one item per signal."""
    seen: list[list[str]] = []

    @callback
    def record() -> None:  # a @callback like the push of tariffy/subscribe: it runs at once, inside the signal
        seen.append([c["entry_id"] for c in async_contracts(hass)])

    unsub = async_dispatcher_connect(hass, SIGNAL_CONTRACTS, record)
    yield seen
    unsub()


async def test_the_panel_shows_the_contract_again_after_it_was_reloaded(frontend_env, contract, hass, shown):  # noqa: F811
    entry, _ = await contract.setup(STROM, **GOLDEN)
    shown.clear()
    assert await hass.config_entries.async_reload(entry.entry_id)  # what saving a changed contract does
    await hass.async_block_till_done()
    assert shown, "the panel was told nothing after the reload"
    assert shown[-1] == [entry.entry_id], f"the last thing the panel was shown is {shown[-1]}, the signals were {shown}"


async def test_a_new_contract_shows_up_in_the_open_panel(frontend_env, contract, hass, shown):  # noqa: F811
    entry, _ = await contract.setup(STROM, **GOLDEN)
    shown.clear()
    second, _ = await contract.setup({**STROM, "anbieter": "Zweiter"}, **GOLDEN)
    await hass.async_block_till_done()
    assert shown and set(shown[-1]) == {entry.entry_id, second.entry_id}, shown


async def test_a_contract_that_is_being_unloaded_is_not_listed(frontend_env, contract, hass, shown):  # noqa: F811
    entry, _ = await contract.setup(STROM, **GOLDEN)
    shown.clear()
    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()
    assert shown[-1] == []  # unloaded: nothing to show


async def test_every_signal_during_a_reload_of_one_of_two_contracts_keeps_the_other(frontend_env, contract, hass, shown):  # noqa: F811
    first, _ = await contract.setup(STROM, **GOLDEN)
    second, _ = await contract.setup({**STROM, "anbieter": "Zweiter"}, **GOLDEN)
    shown.clear()
    assert await hass.config_entries.async_reload(second.entry_id)
    await hass.async_block_till_done()
    assert all(first.entry_id in listed for listed in shown), shown
    assert set(shown[-1]) == {first.entry_id, second.entry_id}
