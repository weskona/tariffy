"""Coordinator: Berechnung, Tarifwechsel und Kündigungs-Erinnerung."""

from __future__ import annotations

import calendar
from datetime import date, timedelta
import logging
from typing import TYPE_CHECKING, Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .const import (
    BASIS_FELDER,
    CONF_ABSCHLAG,
    CONF_ANBIETER,
    CONF_ARBEITSPREIS,
    CONF_BEGINN,
    CONF_BONUS,
    CONF_BRENNWERT,
    CONF_ENDE,
    CONF_ERINNERUNG_MONATE,
    CONF_GRUNDPREIS,
    CONF_JAHRESVERBRAUCH,
    CONF_KUENDIGUNG_BESTAETIGT,
    CONF_KUNDENNUMMER,
    CONF_MARKTLOKATION,
    CONF_NOTIFY_GESENDET,
    CONF_NOTIFY_TARGET,
    CONF_OEKOSTROM,
    CONF_PREISGARANTIE,
    CONF_SPARTE,
    CONF_TARIF,
    CONF_ZAEHLERNUMMER,
    CONF_ZUSTANDSZAHL,
    GAS_SPARTE,
    NEXT_PREFIX,
    NOTIFY_ID_PREFIX,
)

if TYPE_CHECKING:
    from . import VertraegeConfigEntry

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(hours=6)


def _parse_date(value: Any) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(str(value))
    except (ValueError, TypeError):
        return None


def _f(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def _minus_months(d: date, months: int) -> date:
    if not months:
        return d
    index = (d.month - 1) - months
    year = d.year + index // 12
    month = index % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


class VertraegeCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Hält Vertragsdaten aktuell, schaltet Tarife und erinnert an Kündigungen."""

    def __init__(self, hass: HomeAssistant, entry: "VertraegeConfigEntry") -> None:
        super().__init__(
            hass, _LOGGER, name=entry.title, update_interval=SCAN_INTERVAL
        )
        self.entry = entry

    @property
    def _notification_id(self) -> str:
        return f"{NOTIFY_ID_PREFIX}{self.entry.entry_id}"

    # -------------------------------------------------------------- Wechsel
    def _switch_now(self) -> None:
        nxt = dict(self.entry.options)
        if not nxt:
            return
        new_data: dict[str, Any] = {
            CONF_SPARTE: self.entry.data.get(CONF_SPARTE),
            CONF_ERINNERUNG_MONATE: self.entry.data.get(CONF_ERINNERUNG_MONATE, "0"),
            CONF_NOTIFY_TARGET: self.entry.data.get(CONF_NOTIFY_TARGET),
        }
        for feld in BASIS_FELDER:
            wert = nxt.get(NEXT_PREFIX + feld)
            # Nicht angegebene Felder behalten den aktuellen Wert (z. B. Zähler).
            new_data[feld] = wert if wert not in (None, "") else self.entry.data.get(feld)
        _LOGGER.info(
            "Vertrag '%s': automatischer Wechsel zu '%s' (%s)",
            self.entry.title,
            new_data.get(CONF_ANBIETER),
            new_data.get(CONF_TARIF),
        )
        self.hass.config_entries.async_update_entry(
            self.entry, data=new_data, options={}
        )

    async def async_force_switch(self) -> None:
        self._switch_now()

    # ------------------------------------------------------------ Kündigung
    async def async_confirm_kuendigung(self) -> None:
        await self.hass.services.async_call(
            "persistent_notification",
            "dismiss",
            {"notification_id": self._notification_id},
            blocking=True,
        )
        self.hass.config_entries.async_update_entry(
            self.entry,
            data={**self.entry.data, CONF_KUENDIGUNG_BESTAETIGT: True},
        )

    async def _send_notify(self, title: str, message: str) -> None:
        target = self.entry.data.get(CONF_NOTIFY_TARGET)
        if not target:
            return
        try:
            await self.hass.services.async_call(
                "notify", target, {"title": title, "message": message}
            )
        except Exception as err:  # noqa: BLE001
            _LOGGER.warning("notify.%s nicht erreichbar (%s)", target, err)

    async def _handle_reminder(
        self, aktiv: bool, ende: date | None, data: dict[str, Any]
    ) -> None:
        if not aktiv:
            return
        title = f"Kündigung: {self.entry.title}"
        ende_str = ende.isoformat() if ende else "?"
        message = (
            f"Vertrag **{data.get(CONF_ANBIETER) or ''}** "
            f"({data.get(CONF_TARIF) or ''}) läuft am **{ende_str}** aus.\n\n"
            f"Erinnerung {data.get(CONF_ERINNERUNG_MONATE)} Monat(e) vorher. "
            "Bitte rechtzeitig kündigen oder den Folgevertrag eintragen.\n\n"
            "_Diese Meldung bleibt bestehen, bis du sie über den Button "
            "'Kündigung bestätigen' quittierst._"
        )
        await self.hass.services.async_call(
            "persistent_notification",
            "create",
            {
                "notification_id": self._notification_id,
                "title": title,
                "message": message,
            },
        )
        if not data.get(CONF_NOTIFY_GESENDET):
            await self._send_notify(title, message)
            self.hass.config_entries.async_update_entry(
                self.entry, data={**self.entry.data, CONF_NOTIFY_GESENDET: True}
            )

    # --------------------------------------------------------------- Update
    async def _async_update_data(self) -> dict[str, Any]:
        heute = dt_util.now().date()

        nxt = dict(self.entry.options)
        wechsel = _parse_date(nxt.get(NEXT_PREFIX + CONF_BEGINN)) if nxt else None
        if wechsel is not None and wechsel <= heute:
            self._switch_now()
            nxt = {}

        data = dict(self.entry.data)
        ende = _parse_date(data.get(CONF_ENDE))
        restlaufzeit = (ende - heute).days if ende is not None else None

        arbeitspreis = _f(data.get(CONF_ARBEITSPREIS))
        grundpreis = _f(data.get(CONF_GRUNDPREIS))
        abschlag = _f(data.get(CONF_ABSCHLAG))
        verbrauch = _f(data.get(CONF_JAHRESVERBRAUCH))
        brennwert = _f(data.get(CONF_BRENNWERT))
        zustandszahl = _f(data.get(CONF_ZUSTANDSZAHL))
        sparte = data.get(CONF_SPARTE)

        # Bei Gas: m³ -> kWh (kWh = m³ × Brennwert × Zustandszahl). Sonst kWh direkt.
        if sparte == GAS_SPARTE:
            verbrauch_kwh = (
                round(verbrauch * brennwert * zustandszahl, 1)
                if (verbrauch and brennwert and zustandszahl)
                else None
            )
        else:
            verbrauch_kwh = verbrauch

        abschlagssumme = round(abschlag * 12, 2) if abschlag is not None else None
        geschaetzte_kosten = (
            round(verbrauch_kwh * arbeitspreis + (grundpreis or 0) * 12, 2)
            if (verbrauch_kwh and arbeitspreis is not None)
            else None
        )
        prognose = (
            round(abschlagssumme - geschaetzte_kosten, 2)
            if (abschlagssumme is not None and geschaetzte_kosten is not None)
            else None
        )

        monate = int(data.get(CONF_ERINNERUNG_MONATE) or 0)
        bestaetigt = bool(data.get(CONF_KUENDIGUNG_BESTAETIGT))
        erinnerung_datum = (
            _minus_months(ende, monate) if (ende is not None and monate) else None
        )
        aktiv = bool(
            erinnerung_datum is not None
            and ende is not None
            and erinnerung_datum <= heute <= ende
            and not bestaetigt
        )
        await self._handle_reminder(aktiv, ende, data)

        return {
            CONF_SPARTE: data.get(CONF_SPARTE),
            CONF_ANBIETER: data.get(CONF_ANBIETER),
            CONF_KUNDENNUMMER: data.get(CONF_KUNDENNUMMER),
            CONF_TARIF: data.get(CONF_TARIF),
            CONF_ARBEITSPREIS: arbeitspreis,
            CONF_GRUNDPREIS: grundpreis,
            CONF_ABSCHLAG: abschlag,
            CONF_JAHRESVERBRAUCH: verbrauch,
            CONF_BRENNWERT: brennwert,
            CONF_ZUSTANDSZAHL: zustandszahl,
            "verbrauch_kwh": verbrauch_kwh,
            CONF_ZAEHLERNUMMER: data.get(CONF_ZAEHLERNUMMER),
            CONF_MARKTLOKATION: data.get(CONF_MARKTLOKATION),
            CONF_PREISGARANTIE: _parse_date(data.get(CONF_PREISGARANTIE)),
            CONF_BONUS: _f(data.get(CONF_BONUS)),
            CONF_OEKOSTROM: bool(data.get(CONF_OEKOSTROM)),
            CONF_BEGINN: _parse_date(data.get(CONF_BEGINN)),
            CONF_ENDE: ende,
            "restlaufzeit": restlaufzeit,
            "jahreskosten": abschlagssumme,
            "geschaetzte_jahreskosten": geschaetzte_kosten,
            "prognose": prognose,
            "erinnerung_datum": erinnerung_datum,
            "erinnerung_aktiv": aktiv,
            "erinnerung_bestaetigt": bestaetigt,
            "erinnerung_monate": monate,
            "wechsel": _parse_date(nxt.get(NEXT_PREFIX + CONF_BEGINN)) if nxt else None,
            "next": nxt,
        }
