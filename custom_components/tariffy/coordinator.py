"""Coordinator: Berechnung, Tarifwechsel und Kündigungs-Erinnerung."""

from __future__ import annotations

import calendar
from datetime import date, datetime, timedelta
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
    CONF_VERBRAUCH_SENSOR,
    CONF_ZAEHLERNUMMER,
    CONF_ZUSTANDSZAHL,
    GAS_SPARTE,
    NEXT_PREFIX,
    NOTIFY_ID_PREFIX,
)

if TYPE_CHECKING:
    from . import TariffyConfigEntry

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


async def _get_historic_value(
    hass: HomeAssistant, entity_id: str, at_date: date
) -> float | None:
    """Liest den Sensorwert zum Zeitpunkt des Vertragsbeginns aus dem Recorder."""
    try:
        from homeassistant.components.recorder import get_instance
        from homeassistant.components.recorder.history import get_last_state_changes

        start_dt = datetime.combine(at_date, datetime.min.time()).replace(
            tzinfo=dt_util.get_default_time_zone()
        )
        end_dt = start_dt + timedelta(days=1)

        instance = get_instance(hass)
        states = await instance.async_add_executor_job(
            lambda: _fetch_states(hass, entity_id, start_dt, end_dt)
        )

        if states:
            for state in reversed(states):
                val = _f(state.state)
                if val is not None:
                    return val
    except Exception as err:  # noqa: BLE001
        _LOGGER.debug(
            "History-Abfrage für %s fehlgeschlagen: %s", entity_id, err
        )
    return None


def _fetch_states(hass: HomeAssistant, entity_id: str, start: datetime, end: datetime):
    """Synchroner Abruf der States aus dem Recorder."""
    try:
        from homeassistant.components.recorder.history import state_changes_during_period
        return state_changes_during_period(
            hass, start, end, entity_id, include_start_time_state=True
        ).get(entity_id, [])
    except Exception:  # noqa: BLE001
        return []


class TariffyCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Hält Vertragsdaten aktuell, schaltet Tarife und erinnert an Kündigungen."""

    def __init__(self, hass: HomeAssistant, entry: "TariffyConfigEntry") -> None:
        super().__init__(
            hass, _LOGGER, name=entry.title, update_interval=SCAN_INTERVAL
        )
        self.entry = entry
        self._verbrauch_offset: float | None = None
        self._verbrauch_offset_date: date | None = None

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
            new_data[feld] = wert if wert not in (None, "") else self.entry.data.get(feld)
        _LOGGER.info(
            "Tariffy '%s': automatischer Wechsel zu '%s' (%s)",
            self.entry.title,
            new_data.get(CONF_ANBIETER),
            new_data.get(CONF_TARIF),
        )
        # Offset zurücksetzen — neuer Vertrag, neuer Startpunkt
        self._verbrauch_offset = None
        self._verbrauch_offset_date = None
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

    # ------------------------------------------------- Verbrauch Hochrechnung
    async def _get_verbrauch_offset(
        self, entity_id: str, beginn: date
    ) -> float | None:
        """Holt den Zählerstand zum Vertragsbeginn (einmalig, dann gecacht)."""
        if (
            self._verbrauch_offset is not None
            and self._verbrauch_offset_date == beginn
        ):
            return self._verbrauch_offset

        val = await _get_historic_value(self.hass, entity_id, beginn)
        if val is not None:
            self._verbrauch_offset = val
            self._verbrauch_offset_date = beginn
            _LOGGER.debug(
                "Tariffy '%s': Verbrauch-Offset zum %s = %.2f",
                self.entry.title, beginn, val,
            )
        return val

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
        beginn = _parse_date(data.get(CONF_BEGINN))
        restlaufzeit = (ende - heute).days if ende is not None else None

        arbeitspreis = _f(data.get(CONF_ARBEITSPREIS))
        grundpreis = _f(data.get(CONF_GRUNDPREIS))
        abschlag = _f(data.get(CONF_ABSCHLAG))
        verbrauch = _f(data.get(CONF_JAHRESVERBRAUCH))
        brennwert = _f(data.get(CONF_BRENNWERT))
        zustandszahl = _f(data.get(CONF_ZUSTANDSZAHL))
        sparte = data.get(CONF_SPARTE)

        # Bei Gas: m³ -> kWh
        if sparte == GAS_SPARTE:
            verbrauch_kwh = (
                round(verbrauch * brennwert * zustandszahl, 1)
                if (verbrauch and brennwert and zustandszahl)
                else None
            )
        else:
            verbrauch_kwh = verbrauch

        abschlagssumme = round(abschlag * 12, 2) if abschlag is not None else None

        # ---- Echte Verbrauchsmessung via Sensor ----
        verbrauch_sensor = data.get(CONF_VERBRAUCH_SENSOR)
        verbrauch_bisher: float | None = None
        verbrauch_hochgerechnet: float | None = None
        prognose_real: float | None = None

        if verbrauch_sensor and beginn:
            # Aktuellen Sensorwert lesen
            state = self.hass.states.get(verbrauch_sensor)
            aktuell = _f(state.state) if state else None

            if aktuell is not None:
                # Offset zum Vertragsbeginn holen
                offset = await self._get_verbrauch_offset(verbrauch_sensor, beginn)

                if offset is not None:
                    verbrauch_bisher = round(aktuell - offset, 2)
                else:
                    # Fallback: kein History-Eintrag → gesamten aktuellen Wert nehmen
                    _LOGGER.debug(
                        "Tariffy '%s': kein History-Offset gefunden, "
                        "Fallback auf Schätzverbrauch",
                        self.entry.title,
                    )

                if verbrauch_bisher is not None and verbrauch_bisher > 0:
                    vergangene_tage = (heute - beginn).days
                    if vergangene_tage > 0:
                        verbrauch_hochgerechnet = round(
                            verbrauch_bisher / vergangene_tage * 365, 1
                        )
                        # Bei Gas: m³ hochgerechnet → kWh
                        if sparte == GAS_SPARTE and brennwert and zustandszahl:
                            verbrauch_kwh_real = round(
                                verbrauch_hochgerechnet * brennwert * zustandszahl, 1
                            )
                        else:
                            verbrauch_kwh_real = verbrauch_hochgerechnet

                        if arbeitspreis is not None:
                            geschaetzte_kosten_real = round(
                                verbrauch_kwh_real * arbeitspreis
                                + (grundpreis or 0) * 12,
                                2,
                            )
                            if abschlagssumme is not None:
                                prognose_real = round(
                                    abschlagssumme - geschaetzte_kosten_real, 2
                                )

        # Geschätzte Kosten (aus eingetragenem Jahresverbrauch)
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
            CONF_SPARTE: sparte,
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
            CONF_BEGINN: beginn,
            CONF_ENDE: ende,
            "restlaufzeit": restlaufzeit,
            "jahreskosten": abschlagssumme,
            "geschaetzte_jahreskosten": geschaetzte_kosten,
            "prognose": prognose,
            "verbrauch_bisher": verbrauch_bisher,
            "verbrauch_hochgerechnet": verbrauch_hochgerechnet,
            "prognose_real": prognose_real,
            "erinnerung_datum": erinnerung_datum,
            "erinnerung_aktiv": aktiv,
            "erinnerung_bestaetigt": bestaetigt,
            "erinnerung_monate": monate,
            "wechsel": _parse_date(nxt.get(NEXT_PREFIX + CONF_BEGINN)) if nxt else None,
            "next": nxt,
        }
