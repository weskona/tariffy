"""Diagnostics download and the log lines for an unknown consumption."""

from __future__ import annotations

import json
import logging

from custom_components.tariffy.diagnostics import async_get_config_entry_diagnostics

SENSOR = "sensor.wasserzaehler"

WASSER = {
    "sparte": "water",
    "arbeitspreis": 1.89,
    "grundpreis": 14.68,
    "abschlag": 26.0,
    "beginn": "2026-01-01",
    "ende": "2026-12-31",
    "verbrauch_sensor": SENSOR,
    "verbrauch_start_wert": 148.0,
    "kundennummer": "K-123456",
    "zaehlernummer": "Z-987654",
    "marktlokation": "DE000MALO",
    "notify_target": "notify.handy",
    "erinnerung_monate": "0",
}


async def test_download_is_redacted_and_serializable(hass, setup_contract):
    entry, _ = await setup_contract(
        dict(WASSER),
        latest=(211.5, 211.5),
        offset=(1.0, 1.0),
        sensor_states={SENSOR: "211.5663"},
    )
    result = await async_get_config_entry_diagnostics(hass, entry)
    text = json.dumps(result)  # must be JSON serialisable

    for secret in ("K-123456", "Z-987654", "DE000MALO", "notify.handy"):
        assert secret not in text
    assert result["entry"]["data"]["kundennummer"] == "**REDACTED**"
    assert result["update"]["last_update_success"] is True
    assert result["zaehler"]["state"] == "211.5663"
    assert result["verbrauch"]["pfad"] == "manueller_startwert"
    assert result["verbrauch"]["ergebnis"] == 63.57
    assert result["daten"]["verbrauch_bisher"] == 63.57


async def test_warning_once_when_unknown_and_info_on_recovery(
    hass, setup_contract, contract, caplog
):
    caplog.set_level(logging.INFO, logger="custom_components.tariffy")
    entry, d = await setup_contract(
        dict(WASSER), sensor_states={SENSOR: "unavailable"}
    )
    assert d["verbrauch_bisher"] is None
    def warnings():
        return [
            r for r in caplog.records
            if r.levelno == logging.WARNING and r.name == "custom_components.tariffy.coordinator"
        ]

    assert len(warnings()) == 1
    assert "unbekannt" in warnings()[0].getMessage()
    assert "unavailable" in warnings()[0].getMessage()

    # still unknown on the next refresh: no second warning
    await contract.advance_to("2026-07-13")
    assert len(warnings()) == 1

    # the meter is back: one info line
    contract.values["latest"] = (211.5, 211.5)
    hass.states.async_set(SENSOR, "211.5663")
    d = await contract.advance_to("2026-07-14")
    assert d["verbrauch_bisher"] == 63.57
    assert any("wieder bekannt" in r.getMessage() for r in caplog.records)
