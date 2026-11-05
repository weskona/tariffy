# Sensoren

## Sensoren pro Vertrag

| Sensor | Einheit | Sparte | Beschreibung |
|--------|---------|--------|-------------|
| Arbeitspreis | €/kWh | Energie | Verbrauchsabhängiger Preis. Bei dynamischem Tarif (Preissensor konfiguriert) der Statistik-Durchschnitt über die bisherige Vertragslaufzeit + Aufschlag; Attribut `arbeitspreis_aktuell` zeigt den aktuellen Live-Preis, `dynamischer_tarif` ob ein Preissensor gesetzt ist |
| Arbeitspreis (Nacht) | €/kWh | Energie | Nachttarif (TOU/Economy 7) |
| Arbeitspreis (Niedertarif/NT) | €/kWh | Strom (Zweizählertarif) | Niedertarif-Preis, wie im Config Flow eingetragen |
| Arbeitspreis (Effektiv) | €/kWh | Energie | Effektiver Ø-Preis bei Staffeltarif |
| Arbeitspreis (Abwasser) | €/m³ | Wasser | Abwassergebühr |
| Wasserpreis (Gesamt) | €/m³ | Wasser | Frischwasser + Abwasser kombiniert |
| Grundpreis | €/Monat | Energie | Monatliche Grundgebühr |
| Abschlag | €/Monat | Alle | Monatlicher Abschlag |
| Abschlag (Empfohlen) | €/Monat | Energie | Basiert auf realem Verbrauch der letzten Laufzeit × aktuelle Preise |
| Abschlag (Anpassung empfohlen) | €/Monat | Energie+Wasser | Was der Abschlag ab jetzt bis Vertragsende sein müsste, um exakt auszugleichen — im Unterschied zu „Abschlag (Empfohlen)" (erst nach Tarifwechsel) läuft dieser fortlaufend während des aktuellen Vertrags mit |
| Abschlag (Vertragslaufzeit) | € | Alle | Abschlag × Laufzeit in Monaten (reiner Zahlungsplan, keine Kosten-Prognose) |
| Kosten (Bisher) | € | Energie+Wasser | Tatsächlich angefallene Kosten seit Vertragsbeginn (Echte Messung) |
| Guthaben/Nachzahlung (Bisher) | € | Energie | Abschlag bisher gezahlt − Kosten (Bisher), Stand von heute (keine Hochrechnung). Icon zeigt 👍/👎 je nach Vorzeichen |
| Einspeisevergütung | €/kWh | Strom | Eingetragene Vergütung pro kWh |
| Jahresverbrauch (kWh) | kWh | Gas | m³ umgerechnet via Brennwert & Zustandszahl |
| Verbrauch (Bisher) | Einheit des Verbrauchssensors (meist m³) | Energie+Wasser | Gemessener Verbrauch seit Vertragsbeginn — roher Zählerstand-Delta, **nicht** automatisch in kWh umgerechnet |
| Verbrauch (Vertragslaufzeit hochgerechnet) | Einheit des Verbrauchssensors | Energie+Wasser | Aktueller Verbrauch auf die tatsächliche Vertragslaufzeit hochgerechnet (kein festes Kalenderjahr) |
| Verbrauch (Letzte Laufzeit) | Einheit des Verbrauchssensors | Energie | Eingefroren beim Tarifwechsel |
| Verbrauch Hochtarif/Niedertarif (Bisher) | kWh | Strom (Zweizählertarif) | Gemessener Verbrauch je Register seit Vertragsbeginn |
| Kosten Hochtarif/Niedertarif (Bisher) | € | Strom (Zweizählertarif) | Verbrauchskosten je Register (ohne Grundpreis-Anteil) seit Vertragsbeginn |
| Guthaben/Nachzahlung (Vertragsende) | € | Energie+Wasser | Prognose auf Basis des echten Verbrauchs. Icon zeigt 👍/👎 je nach Vorzeichen |
| Restlaufzeit | Tage | Alle | Tage bis Vertragsende |
| Vertragsbeginn | Datum | Alle | Startdatum des Vertrags |
| Vertragsende | Datum | Alle | Ende des aktuellen Vertrags |
| Nächster Wechsel | Datum | Alle | Datum des geplanten Tarifwechsels |
| Kündigungs-Erinnerung | Datum | Alle | Datum ab dem erinnert wird |
| Anbieter | – | Alle | Name des Anbieters (Diagnose) |
| Tarif | – | Alle | Tarifbezeichnung (Diagnose) |
| Kundennummer | – | Alle | Kundennummer (Diagnose) |
| Zählernummer | – | Energie | Zählernummer (Diagnose) |
| Zählernummer (Niedertarif/NT) | – | Strom (Zweizählertarif) | Zählernummer des Niedertarif-Registers (Diagnose) |

> Sensoren für **Nachttarif** (Economy 7 / TOU), **Staffelpreise** und **Zweizählertarif (HT/NT)** erscheinen nur wenn die entsprechende Sparte/Option genutzt wird.


## Die vier Kosten-Sensoren im Überblick

Tariffy hat vier Sensoren mit Währungseinheit. Dahinter stecken zwei unabhängige Fragen:

- **Wann?** – der Stand **bis heute** (Ist) oder die Prognose fürs **Vertragsende** (hochgerechnet)?
- **Was?** – ein **reiner Betrag** (Abschlag-Soll oder echte Kosten) oder die **Bilanz** daraus (Abschlag minus Kosten = Guthaben/Nachzahlung)?

|  | **reiner Betrag** | **Bilanz (Abschlag − Kosten)** |
|---|---|---|
| **Bisher** | Kosten (Bisher) `kosten_bisher` | Guthaben/Nachzahlung (Bisher) `guthaben_bisher` |
| **Vertragsende** (hochgerechnet) | Abschlag (Vertragslaufzeit) `jahreskosten` | Guthaben/Nachzahlung (Vertragsende) `prognose_real` |

Wichtig: **Abschlag (Vertragslaufzeit)** ist *keine* Kosten-Prognose — es ist einfach `abschlag × laufzeit_monate`, also nur der Zahlungsplan, unabhängig vom tatsächlichen Verbrauch. Die beiden Bilanz-Sensoren (`guthaben_bisher`, `prognose_real`) sind positiv bei Guthaben, negativ bei Nachzahlung (siehe `tendenz`-Attribut und Icon 👍/👎).

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
