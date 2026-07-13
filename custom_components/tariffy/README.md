# Tariffy

Home-Assistant-Integration für Energie-/Wasser-/sonstige Vertragskosten: legt pro Vertrag ein Gerät mit mehreren Sensoren an, verfolgt echten Verbrauch über einen verknüpften Sensor, rechnet Prognosen und erinnert an Kündigungsfristen. Unterstützt automatischen Tarifwechsel zu einem geplanten Datum.

## Unterstützte Sparten

- `electricity` (Strom)
- `gas`
- `water` (Wasser)
- `internet`, `mobile`, `insurance`, `other` (Pauschalverträge ohne Verbrauchsmessung)

## Die vier Kosten-Sensoren im Überblick

Tariffy hat vier Sensoren mit Währungseinheit. Dahinter stecken zwei unabhängige Fragen:

- **Wann?** – der Stand **bis heute** (Ist) oder die Prognose fürs **Vertragsende** (hochgerechnet)?
- **Was?** – ein **reiner Betrag** (Abschlag-Soll oder echte Kosten) oder die **Bilanz** daraus (Abschlag minus Kosten = Guthaben/Nachzahlung)?

|  | **reiner Betrag** | **Bilanz (Abschlag − Kosten)** |
|---|---|---|
| **Bisher** | Kosten (Bisher) `kosten_bisher` | Guthaben/Nachzahlung (Bisher) `guthaben_bisher` |
| **Vertragsende** (hochgerechnet) | Abschlag (Vertragslaufzeit) `jahreskosten` | Guthaben/Nachzahlung (Vertragsende) `prognose_real` |

Wichtig: **Abschlag (Vertragslaufzeit)** ist *keine* Kosten-Prognose — es ist einfach `abschlag × laufzeit_monate`, also nur der Zahlungsplan, unabhängig vom tatsächlichen Verbrauch. Die beiden Bilanz-Sensoren (`guthaben_bisher`, `prognose_real`) sind positiv bei Guthaben, negativ bei Nachzahlung (siehe `tendenz`-Attribut und Icon 👍/👎).

**Formeln:**

| Sensor | Formel |
|---|---|
| Kosten (Bisher) | `verbrauch_bisher_kwh × arbeitspreis + grundpreis × vergangene_monate` |
| Guthaben/Nachzahlung (Bisher) | `abschlag × vergangene_monate − Kosten (Bisher)` |
| Abschlag (Vertragslaufzeit) | `abschlag × laufzeit_monate` |
| Guthaben/Nachzahlung (Vertragsende) | `Abschlag (Vertragslaufzeit) − geschaetzte_kosten_real`, wobei `geschaetzte_kosten_real` der auf die volle Laufzeit hochgerechnete reale Verbrauch × Arbeitspreis (+ Grundpreis) ist |

**Echtes Beispiel** (Stromvertrag: Abschlag 40 €/Monat, Arbeitspreis 0,2977 €/kWh, Grundpreis 11,51 €/Monat, Laufzeit 01.01.–31.12.2026 ≈ 11,96 Monate; Stand heute nach 6,31 Monaten: 1.481,17 kWh verbraucht):

```
Kosten (Bisher)                       = 1.481,17 kWh × 0,2977 €  + 11,51 € × 6,31 Monate  =    513,54 €
Abschlag bisher gezahlt (intern)      = 40 € × 6,31 Monate                                =    252,40 €
→ Guthaben/Nachzahlung (Bisher)       = 252,40 € − 513,54 €                               =   −261,24 €  (Nachzahlung)

Hochgerechnet auf die volle Laufzeit: 1.481,17 kWh / 192 Tage × 364 Tage ≈ 2.808,1 kWh

Abschlag (Vertragslaufzeit)           = 40 € × 11,96 Monate                               =    478,32 €
Geschaetzte Kosten real (intern)      = 2.808,1 kWh × 0,2977 € + 11,51 € × 11,96 Monate    =    973,61 €
→ Guthaben/Nachzahlung (Vertragsende)  = 478,32 € − 973,61 €                               =   −495,29 €  (Nachzahlung, prognostiziert)
```

Alle vier Werte entsprechen exakt den live angezeigten Sensoren dieses Vertrags. Man sieht: der Verbrauch liegt deutlich über dem, was der Abschlag deckt — die Nachzahlung wächst von −261 € (heute) auf prognostizierte −495 € (Vertragsende), fast im gleichen Verhältnis wie die Zeit fortschreitet (6,31 → 11,96 Monate, fast Faktor 2). Das zeigt den Unterschied zwischen den beiden Bilanz-Sensoren: einer ist der **aktuelle** Stand, der andere die **Prognose** zum Vertragsende, unter der Annahme dass der Verbrauch im gleichen Tempo weitergeht.

Alle vier benötigen `arbeitspreis`; `kosten_bisher`, `guthaben_bisher` und `prognose_real` zusätzlich einen konfigurierten `verbrauch_sensor`.

## Sensoren und ihre Berechnung

Alle Formeln beziehen sich auf `coordinator.py::_async_update_data`. `heute` = aktuelles Datum, `beginn`/`ende` = Vertragslaufzeit.

### Grunddaten (direkte Eingabewerte, keine Berechnung)

Keine Formel — das sind einfach die Werte, die du im Config-Flow eingetragen hast.

| Sensor | Bedeutung | Beispiel (Strom-Vertrag) |
|---|---|---|
| Arbeitspreis | €/kWh (bzw. €/Einheit bei Wasser) laut Vertrag | 0,2977 €/kWh |
| Grundpreis | €/Monat | 11,51 €/Monat |
| Abschlag | monatliche Abschlagszahlung | 40 €/Monat |
| Anbieter, Kundennummer, Zählernummer, Tarif, Marktlokation | reine Anzeige/Diagnose | — |
| Einspeisevergütung (nur Strom) | reiner Eingabewert, keine Berechnung | 0,0811 €/kWh |

### Vertragslaufzeit

Beispielvertrag: Beginn 01.01.2026, Ende 31.12.2026, heute 12.07.2026, Kündigungsfrist 3 Monate vorher.

- **Restlaufzeit** = `(ende − heute).days` → `(31.12.2026 − 12.07.2026).days` = **172 Tage**
- **Laufzeit (Monate)**, intern verwendet = `(ende − beginn).days / 30.44` → `364 / 30,44` = **11,96 Monate** (Fallback `12.0` ohne `ende`/`beginn`)
- **Abschlag (Vertragslaufzeit)** (`jahreskosten`) = `abschlag × laufzeit_monate` → `40 € × 11,96` = **478,32 €**
- **Kündigungs-Erinnerung** = `ende − erinnerung_monate Monate` → `31.12.2026 − 3 Monate` = **30.09.2026**. Aktiv, wenn `erinnerung_datum ≤ heute ≤ ende` und noch nicht bestätigt. Löst eine `persistent_notification` und optional eine `notify.*`-Nachricht aus.
- **Nächster Wechsel**: Startdatum aus den geplanten „Next"-Feldern (Options-Flow), falls ein Nachfolgevertrag hinterlegt ist — sonst `unknown`. Erreicht der Wechseltermin `heute`, schaltet die Integration automatisch um (`_switch_now`, siehe „Automatischer Tarifwechsel" unten) und friert dabei den Verbrauch der endenden Laufzeit ein.

### Echte Verbrauchsmessung (`verbrauch_sensor` konfiguriert)

Die Basis ist immer der **`sum`-Wert der Langzeitstatistik** (Recorder), nicht der rohe Live-Zustand des Sensors — das macht die Berechnung robust gegenüber Sensoren, die bei `state_class: total_increasing` erlaubterweise periodisch zurücksetzen (z. B. manche ESP-basierte Zähler). Ein echter, nie zurücksetzender Zählerstand-Sensor ist trotzdem vorzuziehen, wo verfügbar.

Weiter mit dem Strom-Beispiel (Verbrauchssensor zeigt seit Vertragsbeginn insgesamt 1.481,17 kWh mehr an):

- **Verbrauch (Bisher)** = `sum(jetzt) − sum(vertragsbeginn)` = **1.481,17 kWh**. Der Offset zum Vertragsbeginn wird einmalig per LTS-Abfrage ermittelt und danach gecacht.
- **Verbrauch (Vertragslaufzeit hochgerechnet)** = `verbrauch_bisher / vergangene_tage × vertrag_gesamttage` → `1.481,17 / 192 Tage × 364 Tage` = **2.808,1 kWh**. `vertrag_gesamttage = (ende − beginn).days` (Fallback `365` ohne `ende`). Rechnet also auf die **tatsächliche Vertragsdauer** hoch, nicht auf ein festes Kalenderjahr — wichtig bei unterjährigem Vertragswechsel.
- **Kosten (Bisher)** (nur Energie-Sparten) = `verbrauch_bisher_kwh × arbeitspreis + grundpreis × vergangene_monate`, `vergangene_monate = (heute − beginn).days / 30.44 = 6,31` → `1.481,17 × 0,2977 € + 11,51 € × 6,31` = **513,54 €**
- **Guthaben/Nachzahlung (Bisher)** (nur Energie-Sparten) = `abschlag_bisher_gezahlt − kosten_bisher` → `252,40 € − 513,54 €` = **−261,24 €** (Nachzahlung). Anders als `prognose_real` KEINE Hochrechnung auf die volle Vertragslaufzeit, sondern der exakte Stand zum heutigen Tag. `abschlag_bisher_gezahlt` berücksichtigt automatisch eine zwischenzeitliche Abschlags-Änderung, siehe „Abschlag (Anpassung empfohlen)" unten.
- **Guthaben/Nachzahlung (Vertragsende)**: `geschaetzte_kosten_real = verbrauch_kwh_real × arbeitspreis + grundpreis × laufzeit_monate` → `2.808,1 × 0,2977 € + 11,51 € × 11,96` = `973,61 €`; `prognose_real = abschlag_vertragslaufzeit − geschaetzte_kosten_real` → `478,32 € − 973,61 €` = **−495,29 €** (Nachzahlung, prognostiziert). `verbrauch_kwh_real` ist bei Gas bereits in kWh umgerechnet (siehe unten).
- **Abschlag (Anpassung empfohlen)**: was der Abschlag ab **jetzt bis Vertragsende** sein müsste, um exakt auszugleichen — im Unterschied zu „Abschlag (Empfohlen)" unten (der ist erst NACH einem Tarifwechsel verfügbar und nutzt den eingefrorenen Verbrauch der LETZTEN Laufzeit). Formel: `(geschaetzte_kosten_real − abschlag_bisher_gezahlt) / restlaufzeit_monate`. Mit den Werten oben: `(973,61 € − 252,40 €) / 5,65` = **127,64 €/Monat** (aktueller Abschlag 40 €/Monat, `differenz`-Attribut zeigt `+87,64 €`). Steht auch in der Abschlag-Warnung-Benachrichtigung (siehe unten), sofern berechenbar.
  - **Wichtig — keine rückwirkende Neuberechnung bei Abschlags-Änderung**: `abschlag_bisher_gezahlt` ist NICHT einfach `abschlag × vergangene_monate` mit dem aktuellen Wert. Tariffy merkt sich beim Ändern des Abschlags automatisch Datum und vorherigen Wert (intern, keine eigenen Sensoren) und rechnet den alten Abschlag korrekt nur bis zum Änderungsdatum, den neuen erst danach. Ändert man z. B. mitten im Vertrag von 40 € auf 127 €, bleibt „Guthaben/Nachzahlung (Bisher)" direkt nach der Änderung nahezu unverändert (nicht rückwirkend höher/niedriger), da ja bisher tatsächlich nur 40 € gezahlt wurden. Mehrere Korrekturen am selben Tag zählen als eine Änderung.
- **Verbrauch (Letzte Laufzeit)**: bei jedem Tarifwechsel eingefroren = `sum(zum Wechselzeitpunkt) − sum(alter Vertragsbeginn)` — egal ob automatisch (Datumswechsel) oder manuell per „Jetzt wechseln"-Button ausgelöst, identische Berechnung. Zusätzlich wird die tatsächliche Dauer dieser abgelaufenen Laufzeit in Monaten mit eingefroren (intern, kein eigener Sensor). Beispiel aus einem echten Testwechsel: Vertrag lief 6,31 Monate, `verbrauch_letzte_laufzeit` wurde auf **1.481,17 kWh** eingefroren.
- **Abschlag (Empfohlen)** (nur Energie-Sparten) = `(verbrauch_letzte_laufzeit_kwh × arbeitspreis_neu + grundpreis_neu × monate_letzte_laufzeit) / monate_letzte_laufzeit`. Nutzt die tatsächliche Dauer der letzten Laufzeit, nicht pauschal 12 Monate. Mit den Werten oben und einem neuen Tarif (Arbeitspreis 0,8754 €/kWh, Grundpreis 45,80 €/Monat): `(1.481,17 × 0,8754 + 45,80 × 6,31) / 6,31` = **251,29 €/Monat** empfohlen (bisheriger Abschlag war 100,78 €/Monat — das `differenz`-Attribut zeigt `+150,51 €`).

### Gas-spezifisch

⚠️ **Wichtig:** `Verbrauch (Bisher)` und `Verbrauch (Vertragslaufzeit hochgerechnet)` zeigen bei Gas den **rohen Zählerstand-Delta in der tatsächlichen Einheit deines Verbrauchssensors** (meist m³, je nachdem was dein Gaszähler liefert) — **nicht** automatisch in kWh, auch wenn `gas_einheit` auf „kWh" steht. `gas_einheit` beschreibt nur die Einheit deiner manuell eingetragenen Jahresverbrauchs-**Schätzung**, nicht die Einheit deines echten Verbrauchssensors. Verwechsle die beiden nicht!

Beispiel (Gas-Vertrag: Arbeitspreis 0,096402 €/kWh, Grundpreis 11,71 €/Monat, Brennwert 12,45, Zustandszahl 1,47, Verbrauchssensor liefert m³):

- **Verbrauch (Bisher)** zeigt **1.037,09 m³** (nicht kWh!) — das ist der rohe Zählerstand-Delta.
- Für **alle Kostenberechnungen** (Kosten Bisher, Guthaben/Nachzahlung, Prognose) wird intern in kWh umgerechnet: `verbrauch_kwh_real = verbrauch × brennwert × zustandszahl` → `1.037,09 m³ × 12,45 × 1,47` = **18.980,3 kWh**. Das ergibt `Kosten (Bisher) = 18.980,3 kWh × 0,096402 € + 11,71 € × 6,31 Monate` = **1.903,6 €** — exakt der live angezeigte Wert.
- **Verbrauch (kWh)** (`verbrauch_kwh`, eigener Sensor): Umrechnung des **manuell eingetragenen** Jahresverbrauchs (nicht des echten Verbrauchssensors!) in kWh, abhängig von `gas_einheit`:
  - `therm` → `× 29.3071`, `MBtu` → `× 293.071`, `kWh` → unverändert
  - `m³` / `CCF` / `ft³` → `verbrauch × brennwert × zustandszahl` (Zustandszahl-Default `1.0`, falls leer)
  - Beispiel: Jahresverbrauch-Schätzung 1.700 (Einheit `kWh` gewählt) → **1.700 kWh** direkt, keine Umrechnung nötig.
- **Brennwert** und **Zustandszahl** akzeptieren sowohl Dezimalpunkt (`11.2`) als auch Dezimalkomma (`11,2`) — Eingabe als Text, serverseitig normalisiert (siehe `config_flow.py::_parse_dezimal`), da das native HTML5-Zahlenfeld Kommas je nach Browser/Locale nicht zuverlässig verarbeitet.

### Wasser-spezifisch

Wie bei Gas gilt: `Verbrauch (Bisher)`/`Verbrauch (Vertragslaufzeit hochgerechnet)` zeigen die tatsächliche Einheit deines Verbrauchssensors (typischerweise m³), nicht zwangsläufig `wasser_einheit`.

Abwasser-Berechnung je nach `abwasser_typ` (Beispiel: Arbeitspreis Frischwasser 2,10 €/m³):

| Typ | Rechnung | Beispiel | Typische Region |
|---|---|---|---|
| `price_per_unit` | `arbeitspreis_gesamt = arbeitspreis + abwasserpreis` (fixer Preis/Einheit) | 2,10 € + 1,80 € = **3,90 €/m³** | DE/AT/CH |
| `percentage` | `abwasser = arbeitspreis × prozentsatz / 100`; `arbeitspreis_gesamt = arbeitspreis + abwasser` | 80 % von 2,10 € = 1,68 €; gesamt **3,78 €/m³** | US/UK/AU |
| `flat_rate` | Abwasser als Pauschale/Monat separat, `arbeitspreis_gesamt = arbeitspreis` (unverändert) | Frischwasser bleibt **2,10 €/m³**, dazu z. B. 15 €/Monat Pauschale | FR/BE |

### Tag/Nacht-Tarif (Economy 7 / TOU)

Aktiv, wenn `arbeitspreis_nacht`, `arbeitspreis`, `verbrauch_tag` und `verbrauch_nacht` alle gesetzt sind (Länder wie GB, US, CA, AU, NZ, IE). Beispiel: Tagpreis 0,32 €/kWh, Nachtpreis 0,18 €/kWh, 2.000 kWh Tag- und 1.500 kWh Nachtverbrauch pro Jahr:

- **Tou-Jahreskosten** = `verbrauch_tag × arbeitspreis + verbrauch_nacht × arbeitspreis_nacht` → `2.000 × 0,32 € + 1.500 × 0,18 €` = `640 € + 270 €` = **910 €**
- Der allgemeine `verbrauch_kwh` wird in diesem Fall durch `verbrauch_tag + verbrauch_nacht` (hier 3.500 kWh) ersetzt.

### Staffelpreise (Tiered)

Aktiv für Länder wie US, CA, AU, ES, PT, IT u. a. Blockweise Berechnung über `tier_limits`/`tier_prices`. Beispiel: erste 1.000 kWh zu 0,25 €, Rest zu 0,35 €, Jahresverbrauch 3.500 kWh:

- Block 1: 0–1.000 kWh × 0,25 € = 250 €; Block 2 (kein Limit mehr): restliche 2.500 kWh × 0,35 € = 875 € → **Tiered-Jahreskosten = 1.125 €**
- **Effektiver Arbeitspreis** = `tiered_jahreskosten / verbrauch_kwh` → `1.125 € / 3.500 kWh` = **0,3214 €/kWh** (Durchschnittspreis über alle Blöcke, nur zur Anzeige).

## Automatischer Tarifwechsel

Im Options-Flow lässt sich ein Nachfolgevertrag mit Startdatum hinterlegen. Der Wechsel wird exakt bei Datumswechsel geprüft (täglich um 00:00:01 Uhr via `async_track_time_change`), zusätzlich bei jedem regulären 6-Stunden-Poll und beim HA-Start als Fallback. Sobald das Wechseldatum erreicht ist: neue Vertragsdaten werden aktiv, der Verbrauch der endenden Laufzeit wird eingefroren (siehe „Verbrauch (Letzte Laufzeit)“ oben), und die Options werden geleert.

## Abschlag-Warnung (optional)

Pro Vertrag zuschaltbar (nur Energie/Wasser, benötigt einen konfigurierten `verbrauch_sensor`): warnt per `persistent_notification` (+ optional `notify.*`), wenn die Prognose zum Vertragsende (`prognose_real`, siehe „Guthaben/Nachzahlung (Vertragsende)“ oben) eine Nachzahlung über der eingestellten Schwelle erwarten lässt.

- **Aktivieren**: Checkbox „Warnen, wenn Abschlag zu niedrig ist" im Config-/Reconfigure-Flow des jeweiligen Vertrags. Standardmäßig aus.
- **Warnschwelle** (€ Nachzahlung, Default 50 €): Warnung feuert, wenn `prognose_real < -Schwelle`.
- **Bestätigen**: Button „Abschlag-Warnung bestätigen" entfernt die Dauerbenachrichtigung für die aktuelle Episode. Verbessert sich die Prognose danach wieder über die Schwelle (z. B. durch einen höheren Abschlag oder geringeren Verbrauch) und verschlechtert sie sich später erneut, wird automatisch wieder gewarnt — die Bestätigung ist also keine dauerhafte Stummschaltung, sondern gilt nur für die aktuelle Verschlechterung.
- Der rohe Zustand (unabhängig vom Bestätigt-Status) steht als Attribut `abschlag_warnung_aktiv` am Sensor „Guthaben/Nachzahlung (Vertragsende)".

## Bekannte Einschränkungen

- Die Umrechnung „vergangene Tage → Monate“ nutzt überall den Faktor `30.44` (Durchschnittsmonatslänge), keine kalendergenaue Monatsrechnung.
- `empfohlener_abschlag` fällt auf eine 12-Monats-Annahme zurück, wenn die Dauer der letzten Laufzeit nicht bekannt ist (z. B. bei Verträgen, die vor Einführung dieses Felds gewechselt haben).
- Ohne konfigurierten `verbrauch_sensor` bleiben alle "echten" Verbrauchssensoren (`verbrauch_bisher`, `verbrauch_hochgerechnet`, `prognose_real`, `kosten_bisher`) auf `unknown` — nur die eingetragenen Vertragsdaten (Preise, Restlaufzeit, Kosten laut Abschlag) sind dann verfügbar.
