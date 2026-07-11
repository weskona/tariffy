"""Coordinator: Berechnung, Tarifwechsel und Kündigungs-Erinnerung."""

from __future__ import annotations

import calendar
from datetime import date, datetime, timedelta
import logging
from typing import TYPE_CHECKING, Any

from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_change
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
    CONF_GAS_EINHEIT,
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
    CONF_VERBRAUCH_LETZTE_LAUFZEIT,
    CONF_VERBRAUCH_LETZTE_LAUFZEIT_MONATE,
    CONF_VERBRAUCH_SENSOR,
    CONF_ZAEHLERNUMMER,
    CONF_ZUSTANDSZAHL,
    ABWASSER_TYP_PAUSCHAL,
    ABWASSER_TYP_PROZENT,
    ABWASSER_TYP_PREIS,
    CONF_ABWASSER_TYP,
    CONF_ARBEITSPREIS_ABWASSER,
    CONF_ARBEITSPREIS_NACHT,
    CONF_EINSPEISEVERGUETUNG,
    CONF_JAHRESVERBRAUCH_NACHT,
    CONF_JAHRESVERBRAUCH_TAG,
    CONF_TIER_LIMITS,
    CONF_TIER_PRICES,
    CONF_TIERED,
    CONF_WASSER_EINHEIT,
    MAX_TIERS,
    ENERGIE_SPARTEN_MIT_WASSER,
    GAS_SPARTE,
    WASSER_SPARTE,
    NEXT_PREFIX,
    NOTIFY_ID_PREFIX,
    SPARTEN_MIGRATION,
)

if TYPE_CHECKING:
    from . import TariffyConfigEntry

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(hours=6)


def _tiered_cost(verbrauch: float, limits: list, prices: list) -> float | None:
    """Berechnet gestaffelte Kosten für gegebenen Jahresverbrauch.

    limits: Obergrenzen je Block (letzter Block = unbegrenzt wenn None)
    prices: Preis je Block
    Beispiel: limits=[5,10], prices=[0.5,0.8,1.2]
    → Block1: 0-5, Block2: 5-10, Block3: >10
    """
    if not limits or not prices:
        return None
    total = 0.0
    remaining = verbrauch
    prev = 0.0
    for i, price in enumerate(prices):
        if remaining <= 0:
            break
        if i < len(limits) and limits[i] is not None:
            block_size = min(remaining, limits[i] - prev)
            total += block_size * price
            remaining -= block_size
            prev = limits[i]
        else:
            # Letzter Block: unbegrenzt
            total += remaining * price
            remaining = 0
    return round(total, 2)


def _extract_tiers(data: dict) -> tuple[list, list]:
    """Extrahiert Tier-Listen aus entry.data (tier_limit_0..N, tier_price_0..N)."""
    limits = []
    prices = []
    # Zuerst prüfen ob alte Listen-Form vorhanden
    if data.get(CONF_TIER_LIMITS):
        return list(data[CONF_TIER_LIMITS]), list(data[CONF_TIER_PRICES] or [])
    # Neue Form: einzelne Felder
    for i in range(MAX_TIERS):
        lim = _f(data.get(f"tier_limit_{i}"))
        prc = _f(data.get(f"tier_price_{i}"))
        if prc is None:
            break
        limits.append(lim)  # None = unbegrenzt
        prices.append(prc)
    return limits, prices


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
    """Liest den kumulierten 'sum'-Wert zum Vertragsbeginn aus den Long-Term
    Statistics.

    Wichtig: 'sum' statt 'state' — 'state' ist der rohe Momentanwert des
    Sensors und bei state_class total_increasing NICHT reset-sicher (z.B.
    Gaszähler-Sensoren, die regelmäßig auf 0 zurückspringen). 'sum' rechnet
    solche Resets bereits korrekt zusammen.
    """
    try:
        from homeassistant.components.recorder import get_instance
        from homeassistant.components.recorder.statistics import statistics_during_period

        tz = dt_util.get_default_time_zone()
        # Suche ab dem Vortag bis 3 Tage danach um den nächsten verfügbaren Wert zu finden
        start_dt = datetime.combine(at_date - timedelta(days=1), datetime.min.time()).replace(tzinfo=tz)
        end_dt = datetime.combine(at_date + timedelta(days=3), datetime.min.time()).replace(tzinfo=tz)

        instance = get_instance(hass)
        stats = await instance.async_add_executor_job(
            lambda: statistics_during_period(
                hass,
                start_dt,
                end_dt,
                statistic_ids={entity_id},
                period="hour",
                units={},
                types={"sum"},
            )
        )

        entries = stats.get(entity_id, [])
        if entries:
            # Ersten Eintrag am oder nach dem Vertragsbeginn nehmen
            # In HA 2026+ liefert statistics_during_period den start-Wert als
            # Unix-Timestamp (float), nicht als datetime — beide Fälle abdecken
            at_ts = datetime.combine(at_date, datetime.min.time()).replace(tzinfo=tz).timestamp()
            for entry in entries:
                entry_start = entry.get("start")
                if entry_start is None:
                    continue
                # Normalisieren: float (Unix-ts) oder datetime → float
                if isinstance(entry_start, (int, float)):
                    entry_ts = float(entry_start)
                else:
                    entry_ts = entry_start.timestamp()
                if entry_ts >= at_ts:
                    val = entry.get("sum")
                    if val is not None:
                        _LOGGER.debug(
                            "Tariffy: LTS-Offset (sum) für %s am %s = %.3f",
                            entity_id, at_date, val,
                        )
                        return float(val)
            # Fallback: letzten Eintrag vor Vertragsbeginn nehmen
            for entry in reversed(entries):
                val = entry.get("sum")
                if val is not None:
                    _LOGGER.debug(
                        "Tariffy: LTS-Offset (sum, vor Beginn) für %s = %.3f",
                        entity_id, val,
                    )
                    return float(val)

        # Kein Eintrag im Suchfenster — frühesten verfügbaren LTS-Wert suchen
        # 730 Tage = 2 Jahre, deckt Sensoren ab die erst lange nach Vertragsbeginn
        # existierten (z.B. neu eingerichtete Zähler)
        stats_all = await instance.async_add_executor_job(
            lambda: statistics_during_period(
                hass,
                end_dt,
                end_dt + timedelta(days=730),
                statistic_ids={entity_id},
                period="hour",
                units={},
                types={"sum"},
            )
        )
        early_entries = stats_all.get(entity_id, [])
        for entry in early_entries:
            val = entry.get("sum")
            if val is not None:
                _LOGGER.debug(
                    "Tariffy: Frühester LTS-Offset (sum) für %s = %.3f (Sensor existierte "
                    "noch nicht am Vertragsbeginn)",
                    entity_id, val,
                )
                return float(val)

    except Exception as err:  # noqa: BLE001
        _LOGGER.warning("Tariffy: LTS-Abfrage für %s fehlgeschlagen: %s", entity_id, err)
    return None


async def _get_latest_sum(hass: HomeAssistant, entity_id: str) -> float | None:
    """Liest den neuesten verfügbaren kumulierten 'sum'-Wert aus den Long-Term
    Statistics — reset-sicheres Gegenstück zum rohen Live-Sensorwert.
    """
    try:
        from homeassistant.components.recorder import get_instance
        from homeassistant.components.recorder.statistics import statistics_during_period

        instance = get_instance(hass)
        end_dt = dt_util.now()
        start_dt = end_dt - timedelta(days=3)
        stats = await instance.async_add_executor_job(
            lambda: statistics_during_period(
                hass,
                start_dt,
                end_dt,
                statistic_ids={entity_id},
                period="hour",
                units={},
                types={"sum"},
            )
        )
        entries = stats.get(entity_id, [])
        for entry in reversed(entries):
            val = entry.get("sum")
            if val is not None:
                return float(val)
    except Exception as err:  # noqa: BLE001
        _LOGGER.warning("Tariffy: aktueller Sum-Wert für %s fehlgeschlagen: %s", entity_id, err)
    return None


class TariffyCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Hält Vertragsdaten aktuell, schaltet Tarife und erinnert an Kündigungen."""

    def __init__(self, hass: HomeAssistant, entry: "TariffyConfigEntry") -> None:
        super().__init__(
            hass, _LOGGER, name=entry.title, update_interval=SCAN_INTERVAL
        )
        self.entry = entry
        self._verbrauch_offset: float | None = None
        self._verbrauch_offset_date: date | None = None

        async def _startup_refresh(_event: Any) -> None:
            """Refresh nach HA-Start, damit LTS-Daten verfügbar sind."""
            if entry.data.get(CONF_VERBRAUCH_SENSOR):
                await self.async_refresh()

        entry.async_on_unload(
            hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, _startup_refresh)
        )

        async def _midnight_refresh(_now: Any) -> None:
            """Prueft den Tarifwechsel exakt bei Datumswechsel, nicht erst
            beim naechsten 6h-Poll."""
            await self.async_refresh()

        entry.async_on_unload(
            async_track_time_change(hass, _midnight_refresh, hour=0, minute=0, second=1)
        )

    @property
    def _notification_id(self) -> str:
        return f"{NOTIFY_ID_PREFIX}{self.entry.entry_id}"

    # -------------------------------------------------------------- Wechsel
    def _switch_now(self, verbrauch_letzte: float | None = None) -> None:
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
        # Verbrauch der letzten Laufzeit einfrieren — inkl. ihrer tatsächlichen
        # Dauer in Monaten, damit empfohlener_abschlag nicht von einem festen
        # 12-Monats-Jahr ausgehen muss.
        alte_laufzeit_monate: float | None = None
        alte_beginn = _parse_date(self.entry.data.get(CONF_BEGINN))
        if alte_beginn is not None:
            heute = dt_util.now().date()
            alte_laufzeit_monate = round((heute - alte_beginn).days / 30.44, 2)
        if verbrauch_letzte is not None:
            new_data[CONF_VERBRAUCH_LETZTE_LAUFZEIT] = verbrauch_letzte
            if alte_laufzeit_monate is not None:
                new_data[CONF_VERBRAUCH_LETZTE_LAUFZEIT_MONATE] = alte_laufzeit_monate
        elif self.entry.data.get(CONF_VERBRAUCH_LETZTE_LAUFZEIT) is not None:
            new_data[CONF_VERBRAUCH_LETZTE_LAUFZEIT] = self.entry.data[CONF_VERBRAUCH_LETZTE_LAUFZEIT]
            if self.entry.data.get(CONF_VERBRAUCH_LETZTE_LAUFZEIT_MONATE) is not None:
                new_data[CONF_VERBRAUCH_LETZTE_LAUFZEIT_MONATE] = self.entry.data[CONF_VERBRAUCH_LETZTE_LAUFZEIT_MONATE]
        _LOGGER.info(
            "Tariffy '%s': automatischer Wechsel zu '%s' (%s) — Verbrauch letzte Laufzeit: %s",
            self.entry.title,
            new_data.get(CONF_ANBIETER),
            new_data.get(CONF_TARIF),
            verbrauch_letzte,
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
            # Verbrauch der letzten Laufzeit vor dem Wechsel einfrieren
            _vll: float | None = None
            _sensor_id = self.entry.data.get(CONF_VERBRAUCH_SENSOR)
            if _sensor_id and self._verbrauch_offset is not None:
                _aktuell = await _get_latest_sum(self.hass, _sensor_id)
                if _aktuell is None:
                    _state = self.hass.states.get(_sensor_id)
                    _aktuell = _f(_state.state) if _state else None
                if _aktuell is not None:
                    _vll = round(_aktuell - self._verbrauch_offset, 2)
            self._switch_now(_vll)
            nxt = {}

        data = dict(self.entry.data)

        # Rueckwaertskompatibilitaet: alte Sparten-Werte migrieren
        if data.get(CONF_SPARTE) in SPARTEN_MIGRATION:
            migrated_sparte = SPARTEN_MIGRATION[data[CONF_SPARTE]]
            _LOGGER.debug(
                "Tariffy '%s': Sparte migriert von '%s' zu '%s'",
                self.entry.title, data[CONF_SPARTE], migrated_sparte,
            )
            data = {**data, CONF_SPARTE: migrated_sparte}
            # Entry dauerhaft aktualisieren
            self.hass.config_entries.async_update_entry(
                self.entry, data=data
            )

        ende = _parse_date(data.get(CONF_ENDE))
        beginn = _parse_date(data.get(CONF_BEGINN))
        restlaufzeit = (ende - heute).days if ende is not None else None
        laufzeit_monate = (ende - beginn).days / 30.44 if (beginn and ende) else 12.0

        arbeitspreis = _f(data.get(CONF_ARBEITSPREIS))
        grundpreis = _f(data.get(CONF_GRUNDPREIS))
        abschlag = _f(data.get(CONF_ABSCHLAG))
        verbrauch = _f(data.get(CONF_JAHRESVERBRAUCH))
        brennwert = _f(data.get(CONF_BRENNWERT))
        zustandszahl = _f(data.get(CONF_ZUSTANDSZAHL))
        sparte = data.get(CONF_SPARTE)

        # Gasverbrauch -> kWh (einheitenabhängig)
        gas_einheit = data.get(CONF_GAS_EINHEIT, "m³")
        # Umrechnungsfaktoren zu kWh (ohne Brennwert)
        # Therm und MBtu haben festen kWh-Wert, m³/CCF/ft³ brauchen Brennwert
        GAS_KWH_FAKTOR = {
            "therm": 29.3071,   # 1 therm = 29.3071 kWh
            "MBtu": 293.071,    # 1 MBtu = 293.071 kWh
            "kWh": 1.0,
        }
        # Wasser direkt in Einheit (keine kWh-Umrechnung nötig)
        if sparte == WASSER_SPARTE:
            verbrauch_kwh = verbrauch  # bleibt in Wasser-Einheit (m³, L, gal, …)
        elif sparte == GAS_SPARTE:
            if gas_einheit in GAS_KWH_FAKTOR:
                verbrauch_kwh = (
                    round(verbrauch * GAS_KWH_FAKTOR[gas_einheit], 1)
                    if verbrauch else None
                )
            else:
                # m³, CCF, ft³ → brauchen Brennwert × Zustandszahl
                verbrauch_kwh = (
                    round(verbrauch * brennwert * (zustandszahl or 1.0), 1)
                    if (verbrauch and brennwert)
                    else None
                )
        else:
            verbrauch_kwh = verbrauch

        # Währung aus HA-Konfiguration
        currency = self.hass.config.currency or "€"

        # Wasser: Abwasser-Berechnung je nach Typ
        arbeitspreis_abwasser_raw = _f(data.get(CONF_ARBEITSPREIS_ABWASSER))
        abwasser_typ = data.get(CONF_ABWASSER_TYP, ABWASSER_TYP_PREIS)
        wasser_einheit = data.get(CONF_WASSER_EINHEIT, "m³")
        arbeitspreis_abwasser = arbeitspreis_abwasser_raw
        arbeitspreis_gesamt_wasser: float | None = None
        abwasser_pauschal_monat: float | None = None

        if sparte == WASSER_SPARTE and arbeitspreis is not None:
            if abwasser_typ == ABWASSER_TYP_PREIS and arbeitspreis_abwasser_raw is not None:
                # Fixer Preis/Einheit (DE/AT/CH): einfach addieren
                arbeitspreis_gesamt_wasser = round(arbeitspreis + arbeitspreis_abwasser_raw, 6)

            elif abwasser_typ == ABWASSER_TYP_PROZENT and arbeitspreis_abwasser_raw is not None:
                # % des Frischwasserpreises (US/UK/AU)
                # arbeitspreis_abwasser_raw = Prozentsatz (z.B. 80 = 80%)
                abwasser_preis_berechnet = round(arbeitspreis * arbeitspreis_abwasser_raw / 100, 6)
                arbeitspreis_gesamt_wasser = round(arbeitspreis + abwasser_preis_berechnet, 6)
                arbeitspreis_abwasser = abwasser_preis_berechnet  # für Sensor-Anzeige

            elif abwasser_typ == ABWASSER_TYP_PAUSCHAL and arbeitspreis_abwasser_raw is not None:
                # Pauschal pro Monat (FR/BE)
                abwasser_pauschal_monat = arbeitspreis_abwasser_raw
                arbeitspreis_gesamt_wasser = arbeitspreis  # Arbeitspreis bleibt gleich

        abschlagssumme = round(abschlag * laufzeit_monate, 2) if abschlag is not None else None

        # ---- Echte Verbrauchsmessung via Sensor ----
        verbrauch_sensor = data.get(CONF_VERBRAUCH_SENSOR)
        verbrauch_bisher: float | None = None
        verbrauch_hochgerechnet: float | None = None
        prognose_real: float | None = None

        if verbrauch_sensor and beginn:
            # Aktuellen kumulierten Wert lesen (reset-sicher über 'sum', s.o.).
            # Fallback auf den rohen Live-Zustand, falls die Statistik (noch)
            # keinen Sum-Wert liefert (z.B. brandneuer Sensor).
            aktuell = await _get_latest_sum(self.hass, verbrauch_sensor)
            if aktuell is None:
                state = self.hass.states.get(verbrauch_sensor)
                aktuell = _f(state.state) if state else None
            if aktuell is not None:
                # Offset zum Vertragsbeginn holen
                offset = await self._get_verbrauch_offset(verbrauch_sensor, beginn)

                if offset is not None:
                    verbrauch_bisher = round(aktuell - offset, 2)
                else:
                    # LTS für Vertragsbeginn nicht verfügbar — Sensor bleibt unbekannt.
                    # Kein Fallback-Offset setzen: beim nächsten Refresh erneut abfragen.
                    _LOGGER.debug(
                        "Tariffy '%s': Kein LTS-Offset für %s am %s — "
                        "verbrauch_bisher unbekannt.",
                        self.entry.title, verbrauch_sensor, beginn,
                    )

                if verbrauch_bisher is not None and verbrauch_bisher > 0:
                    vergangene_tage = (heute - beginn).days
                    if vergangene_tage > 0:
                        # Hochrechnung auf die tatsächliche Vertragslaufzeit,
                        # nicht auf ein festes Kalenderjahr — ein Vertrag kann
                        # auch mitten im Jahr beginnen/enden.
                        vertrag_gesamttage = (ende - beginn).days if ende is not None else 365
                        verbrauch_hochgerechnet = round(
                            verbrauch_bisher / vergangene_tage * vertrag_gesamttage, 1
                        )
                        # Bei Gas: m³ hochgerechnet → kWh
                        if sparte == GAS_SPARTE and brennwert and zustandszahl:
                            verbrauch_kwh_real = round(
                                verbrauch_hochgerechnet * brennwert * zustandszahl, 1
                            )
                        else:
                            verbrauch_kwh_real = verbrauch_hochgerechnet

                        ap_real = (
                            arbeitspreis_gesamt_wasser
                            if sparte == WASSER_SPARTE and arbeitspreis_gesamt_wasser is not None
                            else arbeitspreis
                        )
                        if ap_real is not None:
                            # verbrauch_kwh_real ist bereits auf die gesamte
                            # Vertragslaufzeit hochgerechnet (s.o.), braucht
                            # hier keinen weiteren laufzeit_faktor mehr.
                            geschaetzte_kosten_real = round(
                                verbrauch_kwh_real * ap_real
                                + (grundpreis or 0) * laufzeit_monate,
                                2,
                            )
                            if abschlagssumme is not None:
                                prognose_real = round(
                                    abschlagssumme - geschaetzte_kosten_real, 2
                                )

        # Tatsächliche Kosten bisher (auf Basis realer Messung)
        kosten_bisher: float | None = None
        guthaben_bisher: float | None = None
        if verbrauch_bisher is not None and beginn is not None:
            _vergangene_tage_kb = (heute - beginn).days
            if _vergangene_tage_kb >= 0:
                _vergangene_monate_kb = _vergangene_tage_kb / 30.44
                if sparte == GAS_SPARTE and brennwert and zustandszahl:
                    _vb_abr = verbrauch_bisher * brennwert * zustandszahl
                else:
                    _vb_abr = verbrauch_bisher
                _ap_kb = (
                    arbeitspreis_gesamt_wasser
                    if sparte == WASSER_SPARTE and arbeitspreis_gesamt_wasser is not None
                    else arbeitspreis
                )
                if _ap_kb is not None:
                    kosten_bisher = round(
                        _vb_abr * _ap_kb + (grundpreis or 0) * _vergangene_monate_kb,
                        2,
                    )
                    # Guthaben/Nachzahlung bisher: Abschlag, der bis heute
                    # tatsaechlich faellig war, gegen die echten Kosten bisher —
                    # anders als prognose_real KEINE Hochrechnung auf die
                    # gesamte Vertragslaufzeit, sondern der Stand von heute.
                    if abschlag is not None:
                        guthaben_bisher = round(
                            abschlag * _vergangene_monate_kb - kosten_bisher, 2
                        )

        # Tag/Nacht-Tarif (Economy 7 / TOU)
        arbeitspreis_nacht = _f(data.get(CONF_ARBEITSPREIS_NACHT))
        verbrauch_tag = _f(data.get(CONF_JAHRESVERBRAUCH_TAG))
        verbrauch_nacht = _f(data.get(CONF_JAHRESVERBRAUCH_NACHT))
        hat_tag_nacht = (
            arbeitspreis_nacht is not None
            and arbeitspreis is not None
            and verbrauch_tag is not None
            and verbrauch_nacht is not None
        )
        if hat_tag_nacht:
            tou_jahreskosten: float | None = round(
                verbrauch_tag * arbeitspreis + verbrauch_nacht * arbeitspreis_nacht, 2
            )
            # Effektiver Durchschnittspreis
            gesamt_verbrauch = (verbrauch_tag or 0) + (verbrauch_nacht or 0)
            if gesamt_verbrauch > 0:
                verbrauch_kwh = gesamt_verbrauch
        else:
            tou_jahreskosten = None

        # Tiered / Staffelpreise
        ist_tiered = bool(data.get(CONF_TIERED))
        tier_limits, tier_prices = _extract_tiers(data)
        tiered_jahreskosten: float | None = None
        effektiver_arbeitspreis: float | None = None  # Durchschnittspreis für Anzeige

        if ist_tiered and tier_prices and verbrauch_kwh:
            tiered_jahreskosten = _tiered_cost(verbrauch_kwh, tier_limits, tier_prices)
            if tiered_jahreskosten is not None and verbrauch_kwh > 0:
                effektiver_arbeitspreis = round(tiered_jahreskosten / verbrauch_kwh, 6)

        # Einspeiseverguetung — nur als Eingabewert gespeichert, keine Berechnung
        einspeiseverguetung = _f(data.get(CONF_EINSPEISEVERGUETUNG))

        # Verbrauch letzte Laufzeit (eingefroren beim Tarifwechsel)
        verbrauch_letzte_laufzeit = _f(data.get(CONF_VERBRAUCH_LETZTE_LAUFZEIT))
        verbrauch_letzte_laufzeit_monate = _f(data.get(CONF_VERBRAUCH_LETZTE_LAUFZEIT_MONATE))

        # Empfohlener Abschlag auf Basis der letzten Vertragslaufzeit
        empfohlener_abschlag: float | None = None
        if verbrauch_letzte_laufzeit is not None and verbrauch_letzte_laufzeit > 0:
            # Gas: m³ → kWh
            if sparte == GAS_SPARTE and brennwert and zustandszahl:
                _vll_kwh = verbrauch_letzte_laufzeit * brennwert * zustandszahl
            else:
                _vll_kwh = verbrauch_letzte_laufzeit
            _ap = (
                arbeitspreis_gesamt_wasser
                if sparte == WASSER_SPARTE and arbeitspreis_gesamt_wasser is not None
                else arbeitspreis
            )
            # Tatsächliche Dauer der letzten Laufzeit verwenden, nicht fest 12
            # Monate — nur als Fallback für vor diesem Fix eingefrorene Werte.
            _monate_alt = (
                verbrauch_letzte_laufzeit_monate
                if verbrauch_letzte_laufzeit_monate and verbrauch_letzte_laufzeit_monate > 0
                else 12.0
            )
            if _ap is not None:
                empfohlener_abschlag = round(
                    (_vll_kwh * _ap + (grundpreis or 0) * _monate_alt) / _monate_alt, 2
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
            "currency": currency,
            "gas_einheit": gas_einheit,
            "wasser_einheit": wasser_einheit,
            CONF_ARBEITSPREIS_ABWASSER: arbeitspreis_abwasser,
            CONF_ABWASSER_TYP: abwasser_typ,
            "arbeitspreis_gesamt_wasser": arbeitspreis_gesamt_wasser,
            "abwasser_pauschal_monat": abwasser_pauschal_monat,
            "hat_tag_nacht": hat_tag_nacht,
            CONF_EINSPEISEVERGUETUNG: einspeiseverguetung,
            CONF_ARBEITSPREIS_NACHT: arbeitspreis_nacht,
            CONF_JAHRESVERBRAUCH_TAG: verbrauch_tag,
            CONF_JAHRESVERBRAUCH_NACHT: verbrauch_nacht,
            "tou_jahreskosten": tou_jahreskosten,
            "ist_tiered": ist_tiered,
            "tier_limits": tier_limits,
            "tier_prices": tier_prices,
            "tiered_jahreskosten": tiered_jahreskosten,
            "effektiver_arbeitspreis": effektiver_arbeitspreis,
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
            "verbrauch_bisher": verbrauch_bisher,
            "verbrauch_hochgerechnet": verbrauch_hochgerechnet,
            "prognose_real": prognose_real,
            "kosten_bisher": kosten_bisher,
            "guthaben_bisher": guthaben_bisher,
            "verbrauch_letzte_laufzeit": verbrauch_letzte_laufzeit,
            "verbrauch_letzte_laufzeit_monate": verbrauch_letzte_laufzeit_monate,
            "empfohlener_abschlag": empfohlener_abschlag,
            "erinnerung_datum": erinnerung_datum,
            "erinnerung_aktiv": aktiv,
            "erinnerung_bestaetigt": bestaetigt,
            "erinnerung_monate": monate,
            "wechsel": _parse_date(nxt.get(NEXT_PREFIX + CONF_BEGINN)) if nxt else None,
            "next": nxt,
        }
