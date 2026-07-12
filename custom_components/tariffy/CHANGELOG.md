# Changelog

Alle nennenswerten Änderungen an der Tariffy-Integration. Format angelehnt an [Keep a Changelog](https://keepachangelog.com/), Versionierung in `manifest.json`.

## [1.20.0] - 2026-07-12

### Behoben

- **README.md des Standalone-Repos (die von HACS/GitHub angezeigte Version) hatte die "vier Kosten-Sensoren"-Erklärung gar nicht**: Das ausführliche 2×2-Raster mit Rechenbeispiel für `jahreskosten`/`kosten_bisher`/`guthaben_bisher`/`prognose_real` war bisher nur in dieser separaten Dokumentations-Kopie enthalten, nie im eigentlichen Top-Level-README des Standalone-Repos. Jetzt in beiden Sprachabschnitten (Englisch + Deutsch) dort ergänzt.

## [1.19.0] - 2026-07-12

### Behoben

- **README.md/CHANGELOG.md wurden von HACS immer wieder gelöscht**: Beide lagen im Standalone-Repo bisher nur auf oberster Ebene, nicht innerhalb von `custom_components/tariffy/`. HACS synct diesen Ordner 1:1 vom Repo und entfernte deshalb bei jedem Update lokale Dateien, die dort nicht Teil des offiziellen Pakets waren. Liegen jetzt zusätzlich innerhalb von `custom_components/tariffy/` im Standalone-Repo, damit sie als Teil des Pakets erhalten bleiben.

## [1.18.0] - 2026-07-12

### Behoben

- **Falsche Einheit bei "Verbrauch (Bisher)"/"Verbrauch (Vertragslaufzeit hochgerechnet)" bei Gas/Wasser**: Diese Sensoren zeigten die Anzeige-Einheit aus `gas_einheit`/`wasser_einheit` (die eigentlich nur die Einheit der manuell eingetragenen Jahresverbrauchs-Schätzung beschreibt), obwohl der angezeigte Wert der rohe Zählerstand-Delta des echten Verbrauchssensors ist — bei m³-Zählern mit `gas_einheit: kWh` stand fälschlich "kWh" über einem m³-Wert. Zeigt jetzt die tatsächliche Einheit des konfigurierten `verbrauch_sensor` an (Fallback auf das Config-Feld, falls der Sensor nicht verfügbar ist).

### Geändert

- README grundlegend überarbeitet: alle Sensor-Erklärungen jetzt mit durchgerechneten Beispielen aus echten Live-Verträgen (Strom, Gas) statt nur abstrakten Formeln; Wasser/Tag-Nacht/Staffelpreis mit klar gekennzeichneten Beispielzahlen (keine echten Verträge dieser Art vorhanden).

## [1.17.0] - 2026-07-12

### Geändert

- **Zwei Kosten-Sensoren umbenannt**, um das Zusammenspiel der vier Guthaben/Kosten-Sensoren klarer zu machen (nur Anzeigename, `entity_id`/`unique_id` unverändert):
  - „Kosten (Vertragslaufzeit)" → „Abschlag (Vertragslaufzeit)" (`jahreskosten`) — macht deutlich, dass es der reine Zahlungsplan ist, keine Kosten-Prognose auf Basis des echten Verbrauchs.
  - „Kosten (Guthaben/Nachzahlung)" → „Guthaben/Nachzahlung (Vertragsende)" (`prognose_real`) — parallele Benennung zu „Guthaben/Nachzahlung (Bisher)".
- README komplett neu strukturiert: 2×2-Raster (Bisher/Vertragsende × reiner Betrag/Bilanz) plus durchgerechnetes Zahlenbeispiel für alle vier Sensoren.

## [1.16.0] - 2026-07-12

### Behoben

- **Manueller "Jetzt wechseln"-Button fror den Verbrauch der endenden Laufzeit nicht ein**: Der Button rief `_switch_now()` ohne den real gemessenen Verbrauch auf, im Unterschied zum automatischen Datumswechsel — `verbrauch_letzte_laufzeit` blieb dadurch leer oder veraltet, was `empfohlener_abschlag` beim nächsten Wechsel verfälscht hätte. Beide Wege nutzen jetzt dieselbe Berechnung (`_verbrauch_letzte_laufzeit_jetzt()`).

## [1.15.0] - 2026-07-12

### Geändert

- **Tarifwechsel reagiert jetzt exakt auf Datumswechsel**: bisher wurde das Wechseldatum nur beim naechsten regulaeren 6-Stunden-Poll geprueft, wodurch der Wechsel bis zu knapp 6 Stunden zu spaet greifen konnte. Neuer taeglicher Trigger um 00:00:01 Uhr (`async_track_time_change`) prueft und schaltet den Vertrag exakt bei Datumswechsel um. Der bestehende 6h-Poll und der HA-Start-Refresh bleiben als Fallback erhalten.

## [1.14.0] - 2026-07-11

### Hinzugefügt

- **Neuer Sensor „Guthaben/Nachzahlung (Bisher)"** (`guthaben_bisher`): `abschlag × vergangene_monate − kosten_bisher`. Beantwortet "bin ich mit meinem Abschlag bis heute im Plus oder Minus?", ohne Hochrechnung auf die volle Vertragslaufzeit (im Unterschied zu `prognose_real`). Gleiches dynamisches 👍/👎-Icon wie bei `prognose_real`. Nur Energie-Sparten, benötigt `verbrauch_sensor`.

## [1.13.0] - 2026-07-11

### Geändert

- **`prognose_real`-Sensor umbenannt**: „Kosten (Prognose Real)" → „Kosten (Guthaben/Nachzahlung)" (nur Anzeigename, `entity_id`/`unique_id` unverändert) — klarer als der bisherige Name, was der Sensor eigentlich beantwortet.
- **Dynamisches Icon für `prognose_real`**: zeigt jetzt `mdi:thumb-up` bei Guthaben (Wert ≥ 0), `mdi:thumb-down` bei Nachzahlung (Wert < 0), Fallback `mdi:calculator-variant` wenn der Wert unbekannt ist (z. B. ohne konfigurierten `verbrauch_sensor`).
- README um eine Übersichtstabelle der drei Kosten-Sensoren (`jahreskosten`, `kosten_bisher`, `prognose_real`) ergänzt, die Formel und Zweck auf einen Blick gegenüberstellt.

## [1.12.0] - 2026-07-09

### Geändert

- **Hochrechnung auf Vertragslaufzeit statt Kalenderjahr**: `verbrauch_hochgerechnet` rechnete bisher immer auf ein festes 365-Tage-Jahr hoch, unabhängig von der tatsächlichen Vertragsdauer. Rechnet jetzt auf `(ende − beginn)` Tage hoch — wichtig bei Verträgen, die unterjährig wechseln. 365 Tage bleibt Fallback für Verträge ohne `ende`.
- **Empfohlener Abschlag** nutzt jetzt die tatsächliche Dauer der letzten Vertragslaufzeit (`verbrauch_letzte_laufzeit_monate`, neu beim Tarifwechsel eingefroren) statt pauschal 12 Monate anzunehmen.
- **Verbrauchssensor umbenannt**: „Jahresverbrauch (Hochgerechnet)" → „Verbrauch (Vertragslaufzeit hochgerechnet)", passend zum bestehenden „Verbrauch (Bisher)"-Schema.
- **Verbrauch-Tracking auf `sum`-Statistik umgestellt**: `verbrauch_bisher` und der Offset zum Vertragsbeginn nutzen jetzt die reset-sichere `sum`-Spalte der Recorder-Langzeitstatistik statt des rohen `state`-Werts. Betrifft `_get_historic_value`, den aktuellen Sensorwert-Read sowie das Einfrieren von „Verbrauch (Letzte Laufzeit)" beim Tarifwechsel. Notwendig für Sensoren mit `state_class: total_increasing`, die erlaubterweise periodisch zurücksetzen (z. B. manche ESP-basierte Zähler) — die alte State-Differenz ergab dabei teils negative Werte.

### Behoben

- **Absturz (500 Internal Server Error) beim Anlegen/Bearbeiten eines Gas-Vertrags**: Ein erster Versuch, Dezimalkomma-Eingabe (`11,2`) für Brennwert/Zustandszahl zu erlauben, ließ sich nicht zu JSON serialisieren (`voluptuous_serialize` kann keine eigenen Funktionen in `vol.All` konvertieren). Brennwert/Zustandszahl sind jetzt reine Textfelder im Schema; die Komma/Punkt-Normalisierung passiert nach der Formularvalidierung in der jeweiligen Step-Funktion, mit sauberer Fehlermeldung statt Absturz bei ungültiger Eingabe.
- **Brennwert/Zustandszahl akzeptieren Dezimalkomma**: `11,2` und `11.2` funktionieren jetzt beide (Ursprungsmeldung: HTML5-Zahlenfeld verarbeitet Komma je nach Browser/Locale nicht zuverlässig).

### Empfohlen

- Für Sensoren, die regelmäßig zurücksetzen, wo möglich einen echten, nie zurücksetzenden Zählerstand-Sensor als `verbrauch_sensor` konfigurieren (z. B. ein separates Utility-Meter mit `cycle: none`), statt sich allein auf die `sum`-Statistik zu verlassen.

## Vor 1.12.0

Keine strukturierte Changelog-Historie vor dieser Version.
