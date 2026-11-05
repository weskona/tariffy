"""Shared fixtures for the Tariffy tests."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any
from unittest.mock import patch

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.tariffy.const import DOMAIN

COORDINATOR = "custom_components.tariffy.coordinator"


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Let Home Assistant load custom_components/tariffy in every test."""


@pytest.fixture(autouse=True)
async def _notifications(hass: HomeAssistant):
    """Coordinator creates/dismisses persistent notifications."""
    assert await async_setup_component(hass, "persistent_notification", {})


class Contract:
    """Sets up a Tariffy entry with the recorder queries replaced.

    `latest` is the (sum, state) pair read for the consumption sensor now,
    `offset` the pair at contract start. The replacements stay active for the
    whole test, so `refresh()` and entry reloads use them as well.
    """

    def __init__(self, hass: HomeAssistant, freezer) -> None:
        self.hass = hass
        self.freezer = freezer
        self.entry: MockConfigEntry | None = None
        self.values: dict[str, Any] = {}

    async def _latest(self, _hass, entity_id):
        if entity_id == self.values.get("nt_id"):
            return self.values["latest_nt"]
        return self.values["latest"]

    async def _offset(self, _hass, entity_id, _at_date):
        if entity_id == self.values.get("nt_id"):
            return self.values["offset_nt"]
        return self.values["offset"]

    async def _average(self, *_args, **_kwargs):
        return self.values["average_price"]

    async def setup(
        self,
        data: dict[str, Any],
        *,
        today: str = "2026-07-12",
        options: dict[str, Any] | None = None,
        latest: tuple[float | None, float | None] = (None, None),
        offset: tuple[float | None, float | None] = (None, None),
        latest_nt: tuple[float | None, float | None] = (None, None),
        offset_nt: tuple[float | None, float | None] = (None, None),
        average_price: float | None = None,
        sensor_states: dict[str, str] | None = None,
    ):
        self.values = {
            "latest": latest,
            "offset": offset,
            "latest_nt": latest_nt,
            "offset_nt": offset_nt,
            "average_price": average_price,
            "nt_id": data.get("verbrauch_sensor_nt"),
        }
        self.freezer.move_to(f"{today} 12:00:00")
        for entity_id, state in (sensor_states or {}).items():
            self.hass.states.async_set(entity_id, state)

        self.entry = MockConfigEntry(
            domain=DOMAIN, title="Test", data=data, options=options or {}
        )
        self.entry.add_to_hass(self.hass)
        assert await self.hass.config_entries.async_setup(self.entry.entry_id)
        await self.hass.async_block_till_done()
        return self.entry, self.entry.runtime_data.data

    async def advance_to(self, day: str):
        """Move the clock and run a coordinator refresh, like the 6 h poll."""
        self.freezer.move_to(f"{day} 12:00:00")
        await self.entry.runtime_data.async_refresh()
        await self.hass.async_block_till_done()
        return self.entry.runtime_data.data


@pytest.fixture
def contract(hass: HomeAssistant, freezer):
    c = Contract(hass, freezer)
    with (
        patch(f"{COORDINATOR}._get_latest_sum", c._latest),
        patch(f"{COORDINATOR}._get_historic_value", c._offset),
        patch(f"{COORDINATOR}._get_average_price", c._average),
    ):
        yield c


@pytest.fixture
def setup_contract(contract: Contract) -> Callable[..., Any]:
    return contract.setup
