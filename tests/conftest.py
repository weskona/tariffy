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


@pytest.fixture
def setup_contract(hass: HomeAssistant, freezer) -> Callable[..., Any]:
    """Create a Tariffy entry and return (entry, coordinator data).

    Recorder access is replaced: `latest` is the (sum, state) pair read for the
    consumption sensor now, `offset` the pair at contract start.
    """

    async def _setup(
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
        freezer.move_to(f"{today} 12:00:00")
        for entity_id, state in (sensor_states or {}).items():
            hass.states.async_set(entity_id, state)

        nt_id = data.get("verbrauch_sensor_nt")

        async def fake_latest(_hass, entity_id):
            return latest_nt if entity_id == nt_id else latest

        async def fake_offset(_hass, entity_id, _at_date):
            return offset_nt if entity_id == nt_id else offset

        async def fake_average(*_args, **_kwargs):
            return average_price

        entry = MockConfigEntry(
            domain=DOMAIN, title="Test", data=data, options=options or {}
        )
        entry.add_to_hass(hass)
        with (
            patch(f"{COORDINATOR}._get_latest_sum", fake_latest),
            patch(f"{COORDINATOR}._get_historic_value", fake_offset),
            patch(f"{COORDINATOR}._get_average_price", fake_average),
        ):
            assert await hass.config_entries.async_setup(entry.entry_id)
            await hass.async_block_till_done()
        return entry, entry.runtime_data.data

    return _setup
