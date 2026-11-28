🇩🇪 Deutsch · [🇬🇧 English](EN-Sensor-Reference)

# Sensoren-Referenz

Diese Seite listet alle Sensoren und Buttons, die Tariffy für einen Vertrag anlegt: Name, Einheit, Bedeutung und Attribute, geordnet nach Sparte. Sie ist zum Nachschlagen gedacht, zum Beispiel beim Bau eines Dashboards oder einer Automation.

**Inhalt:**
- [Gerät und Entitäten](#gerät-und-entitäten)
- [Sensoren für alle Verträge](#sensoren-für-alle-verträge)
- [Strom](#strom)
- [Strom (Zweizählertarif)](#strom-zweizählertarif)
- [Gas](#gas)
- [Wasser](#wasser)
- [Versicherung](#versicherung)
- [Leasing](#leasing)
- [Kredit](#kredit)
- [Pauschalverträge](#pauschalverträge)
- [Buttons](#buttons)
- [Beispiel](#beispiel)
- [Siehe auch](#siehe-auch)

## Gerät und Entitäten

- Jeder Vertrag ist **ein Gerät** in Home Assistant. Name des Geräts ist der Vertragsname, **Hersteller** ist der Anbieter, **Modell** die Sparte (zum Beispiel `Electricity`, `Electricity (HT/NT)`, `Gas`, `Water`).
- Sensoren und Buttons des Vertrags gehören zu diesem Gerät. Ihre **Entity-ID** besteht aus dem Gerätenamen und dem Namen der Entität, zum Beispiel `sensor.strom_haus_kosten_bisher`. Das ist **ein Beispiel**: Die ID hängt vom Vertragsnamen und von der Sprache ab, in der Home Assistant die Entität angelegt hat. Prüfe die echte ID in den Einstellungen der Entität.
- Die **Spalte Schlüssel** in den Tabellen ist die Endung der `unique_id` (`<Eintrags-ID>_<Schlüssel>`). Sie bleibt gleich, auch wenn Du die Entität umbenennst.
- Die **Namen** stammen aus den Übersetzungen der Integration. Die Tabellen nennen sie genau so, wie sie im deutschen Home Assistant stehen.
- **Währung:** Betragssensoren tragen die Währung aus der Home-Assistant-Konfiguration als Einheit, zum Beispiel `EUR`, `EUR/kWh`, `EUR/Monat`. In den Tabellen steht dafür `Währung`. Das Wort `Monat` in der Einheit ist in allen Sprachen gleich.
- **Aktualisierung:** nach dem Start von Home Assistant, alle 6 Stunden und täglich um 00:00:01 Uhr.
- **Daten:** Die Sensoren **Vertragsbeginn**, **Vertragsende**, **Nächster Wechsel** und **Kündigungs-Erinnerung** liefern ein Datum als **Text** im Format `TT.MM.JJJJ`, kein Datum-Objekt von Home Assistant.
- Ein Sensor ohne Wert zeigt `unbekannt` (`unknown`). Das ist normal, solange Voraussetzungen fehlen, zum Beispiel der Verbrauchssensor.
- Welche Sensoren es gibt, wird beim Laden des Vertrags festgelegt. Schaltest Du Nachttarif, Staffelpreise oder einen Außenzähler erst später ein, erscheinen die Sensoren nach dem Neuladen des Vertrags.

> **Gut zu wissen:** Der Sensor **Arbeitspreis** trägt unter anderem die Attribute `kundennummer` und `marktlokation`. Bedenke das, wenn Du Dashboards, Screenshots oder Zustandsdaten teilst.

## Sensoren für alle Verträge

Diese Sensoren bekommt jeder Vertrag, unabhängig von der Sparte. Die vier Sensoren mit Verbrauch und Prognose haben nur dann einen Wert, wenn ein **Verbrauchssensor** eingetragen ist (siehe [Verbrauch-Messen](Verbrauch-Messen)).

| Name | Schlüssel | Einheit | Bedeutung | Attribute |
|---|---|---|---|---|
| Abschlag | `abschlag` | Währung/Monat | monatlicher Abschlag (bei nicht monatlicher Zahlweise der Betrag pro Monat) | – |
| Abschlag (Vertragslaufzeit) | `jahreskosten` | Währung | Abschlag × Laufzeit in Monaten, nur der Zahlungsplan, **keine** Kostenprognose | – |
| Restlaufzeit | `restlaufzeit` | Tage | Tage bis zum Vertragsende (nach dem Ende negativ), leer ohne Vertragsende | – |
| Vertragsbeginn | `beginn` | Text `TT.MM.JJJJ` | Startdatum des Vertrags | – |
| Vertragsende | `ende` | Text `TT.MM.JJJJ` | Ende des aktuellen Vertrags | – |
| Anbieter | `anbieter` | – | Name des Anbieters (Kategorie Diagnose) | – |
| Kundennummer | `kundennummer` | – | Kundennummer (Kategorie Diagnose) | – |
| Tarif | `tarif` | – | Tarifbezeichnung (Kategorie Diagnose) | – |
| Nächster Wechsel | `naechster_wechsel` | Text `TT.MM.JJJJ` | Datum des geplanten Folgevertrags, leer ohne Folgevertrag | `anbieter`, `tarif`, `kundennummer`, `arbeitspreis`, `grundpreis`, `abschlag`, `jahresverbrauch`, `ende` des geplanten Vertrags |
| Kündigungs-Erinnerung | `kuendigung_erinnerung` | Text `TT.MM.JJJJ` | Datum, ab dem erinnert wird (bezogen auf den letzten Kündigungstag, wenn eine Kündigungsfrist eingetragen ist) | `aktiv`, `bestaetigt`, `monate_vorher`, `kuendigungsfrist_monate`, `kuendigung_bis` |
| Verbrauch (Bisher) | `verbrauch_bisher` | kWh bei Strom; bei Gas und Wasser die Einheit des Zählers (Wh und MWh als kWh) | gemessener Verbrauch seit Vertragsbeginn | `verbrauch_hochgerechnet`, `verbrauch_bisher_ht`, `verbrauch_bisher_nt` |
| Verbrauch (Vertragslaufzeit hochgerechnet) | `verbrauch_hochgerechnet` | wie oben | Verbrauch auf die tatsächliche Vertragslaufzeit hochgerechnet | – |
| Guthaben/Nachzahlung (Vertragsende) | `prognose_real` | Währung | Prognose: Abschläge über die Laufzeit minus geschätzte Kosten. Positiv Guthaben, negativ Nachzahlung. Symbol: Daumen hoch oder runter | `tendenz` (`Guthaben` oder `Nachzahlung`), `verbrauch_hochgerechnet`, `abschlag_warnung_aktiv`; mit PV-Autarkie zusätzlich `autarkie_variante`, `autarkie_monatswerte`, `autarkie_bisher`, `autarkie_bisher_nt`, `autarkie_naeherung`, `prognose_ohne_autarkie`; mit Gesamtverbrauchs-Sensor außerdem `verbrauch_gesamt_bisher`, `verbrauch_gesamt_hochgerechnet`, `verbrauch_pv_gedeckt_bisher`, `verbrauch_pv_gedeckt_hochgerechnet` |
| Abschlag (Anpassung empfohlen) | `abschlag_anpassung_empfohlen` | Währung/Monat | Abschlag, der von heute bis Vertragsende genau ausgleicht. Symbol: Daumen runter bei empfohlener Erhöhung. Unter 2 Restmonaten ist der Wert ein einzelner Monatsbetrag für die ganze Rest-Nachzahlung, dann passt eher `abschlag_naechste_laufzeit` | `aktueller_abschlag`, `differenz`, `kurz_vor_ende`, `abschlag_naechste_laufzeit` |

Die Werte des Attributs `tendenz` sind in jeder Sprache die deutschen Wörter `Guthaben` und `Nachzahlung`. Der Rechenweg dieser Werte steht in [Abschlaege-und-Kosten](Abschlaege-und-Kosten), die Attribute der Autarkie in [PV-Autarkie](PV-Autarkie).

## Strom

Zusätzlich zu den Sensoren für alle Verträge:

| Name | Schlüssel | Einheit | Bedeutung | Attribute |
|---|---|---|---|---|
| Arbeitspreis | `arbeitspreis` | Währung/kWh | Preis je kWh. Bei dynamischem Tarif der Statistik-Mittelwert des Preissensors seit Vertragsbeginn plus Aufschlag | `anbieter`, `tarif`, `kundennummer`, `sparte`, `jahresverbrauch`, `marktlokation`, `oekostrom`, `bonus`, `preisgarantie_bis`, `dynamischer_tarif` (ob ein Preissensor gesetzt ist), `arbeitspreis_aktuell` (aktueller Preis des Preissensors plus Aufschlag) |
| Grundpreis | `grundpreis` | Währung/Monat | monatlicher Grundpreis | – |
| Kosten (Bisher) | `kosten_bisher` | Währung | Verbrauch bisher × Arbeitspreis + Grundpreis × vergangene Monate | `verbrauch_bisher`, `kosten_ht_bisher`, `kosten_nt_bisher` |
| Guthaben/Nachzahlung (Bisher) | `guthaben_bisher` | Währung | gezahlte Abschläge minus Kosten bisher, plus Einmalposten der laufenden Laufzeit. Symbol: Daumen hoch oder runter | `tendenz` (`Guthaben` oder `Nachzahlung`), `kosten_bisher` |
| Verbrauch (Letzte Laufzeit) | `verbrauch_letzte_laufzeit` | kWh | beim Tarifwechsel eingefrorener Verbrauch der letzten Laufzeit | – |
| Abschlag (Empfohlen) | `empfohlener_abschlag` | Währung/Monat | Empfehlung nach einem Tarifwechsel, aus dem Verbrauch der letzten Laufzeit | `verbrauch_letzte_laufzeit`, `verbrauch_letzte_laufzeit_monate`, `aktueller_abschlag`, `differenz` |
| Zählernummer | `zaehlernummer` | – | Zählernummer (Kategorie Diagnose) | – |
| Einspeisevergütung | `einspeiseverguetung` | Währung/kWh | eingetragene Vergütung je eingespeister kWh, nur der Eingabewert | – |

Nur wenn die Option genutzt wird, erscheinen außerdem:

| Name | Schlüssel | Einheit | Bedeutung | Attribute |
|---|---|---|---|---|
| Arbeitspreis (Nacht) | `arbeitspreis_nacht` | Währung/kWh | Nachtpreis (Economy 7, TOU). Erscheint, wenn Nachtpreis, Jahresverbrauch Tag und Nacht sowie Arbeitspreis eingetragen sind | `verbrauch_tag`, `verbrauch_nacht`, `tou_jahreskosten` |
| Arbeitspreis (Effektiv) | `effektiver_arbeitspreis` | Währung/kWh | durchschnittlicher Preis bei Staffelpreisen | `tier_limits`, `tier_prices`, `tiered_jahreskosten`, `aktiv` |

Mehr zum Vertrag in [Vertrag-Strom](Vertrag-Strom).

## Strom (Zweizählertarif)

Alle Sensoren von **Strom** (mit dem Hochtarif-Register als Hauptzähler) und zusätzlich:

| Name | Schlüssel | Einheit | Bedeutung | Attribute |
|---|---|---|---|---|
| Arbeitspreis (Niedertarif / NT) | `arbeitspreis_nt` | Währung/kWh | Preis des Niedertarifs, wie eingetragen | – |
| Zählernummer (Niedertarif / NT) | `zaehlernummer_nt` | – | Zählernummer des Niedertarif-Registers (Kategorie Diagnose) | – |
| Verbrauch Hochtarif (Bisher) | `verbrauch_ht_bisher` | kWh | gemessener Verbrauch des Hochtarif-Registers seit Vertragsbeginn | – |
| Verbrauch Niedertarif (Bisher) | `verbrauch_nt_bisher` | kWh | gemessener Verbrauch des Niedertarif-Registers seit Vertragsbeginn | – |
| Kosten Hochtarif (Bisher) | `kosten_ht_bisher` | Währung | Verbrauchskosten des Hochtarifs ohne Grundpreis | `verbrauch_bisher_ht` |
| Kosten Niedertarif (Bisher) | `kosten_nt_bisher` | Währung | Verbrauchskosten des Niedertarifs ohne Grundpreis | `verbrauch_bisher_nt` |

**Verbrauch (Bisher)**, **Kosten (Bisher)** und die Prognose gelten für beide Register zusammen. Sobald beide Register einen Verbrauch haben, zeigt der Sensor **Arbeitspreis** den nach Verbrauch gewichteten Durchschnittspreis beider Register, vorher den Hochtarif-Preis. Mehr dazu in [Vertrag-Strom](Vertrag-Strom).

## Gas

Dieselben Sensoren wie bei **Strom**, ohne **Einspeisevergütung**, und zusätzlich:

| Name | Schlüssel | Einheit | Bedeutung | Attribute |
|---|---|---|---|---|
| Jahresverbrauch (kWh) | `verbrauch_kwh` | kWh | der eingetragene Jahresverbrauch, umgerechnet in kWh (Brennwert × Zustandszahl bei m³, CCF und ft³; Therm und MBtu mit festem Faktor) | `jahresverbrauch_m3` (der eingetragene Wert in der Einheit der Vertragsdaten), `brennwert`, `zustandszahl` |

**Verbrauch (Bisher)** und **Verbrauch (Vertragslaufzeit hochgerechnet)** zeigen bei Gas die Einheit des Zählers, meist m³. **Kosten (Bisher)** und die Prognose rechnen mit Brennwert × Zustandszahl in kWh. Die Sensoren für Nachttarif und Staffelpreise sind auch bei Gas möglich. Mehr in [Vertrag-Gas](Vertrag-Gas).

## Wasser

Zusätzlich zu den Sensoren für alle Verträge:

| Name | Schlüssel | Einheit | Bedeutung | Attribute |
|---|---|---|---|---|
| Arbeitspreis (Abwasser) | `arbeitspreis_abwasser` | Währung/Wassereinheit | Abwasserpreis (bei Angabe in Prozent der berechnete Preis, bei einer Monatspauschale der eingetragene Betrag) | `typ`, `pauschal_monat` |
| Wasserpreis (Gesamt) | `arbeitspreis_gesamt_wasser` | Währung/Wassereinheit | Frischwasser plus Abwasser. Mit Außenzähler der gewichtete Preis des Hauptzählers (siehe [Vertrag-Wasser](Vertrag-Wasser#außenzähler)) | – |

Nur mit mindestens einem **Außenzähler** (Garten, Pool) erscheinen außerdem:

| Name | Schlüssel | Einheit | Bedeutung | Attribute |
|---|---|---|---|---|
| Gartenwasser (Verbrauch) | `garten_verbrauch` | Einheit des Zählers | Verbrauch der Außenzähler, nicht abwasserpflichtig | – |
| Gartenwasser (Kosten) | `garten_kosten` | Währung | Kosten dieses Verbrauchs ohne Abwasser | – |
| Abwasserpflichtiger Verbrauch | `abwasserpflichtiger_verbrauch` | Einheit des Zählers | Hauptzähler minus Außenzähler | – |
| Abwasserkosten | `abwasser_kosten` | Währung | Abwasseranteil der Kosten | – |

> **Gut zu wissen:** Bei Wasser legt Tariffy die Sensoren **Arbeitspreis**, **Grundpreis**, **Kosten (Bisher)**, **Guthaben/Nachzahlung (Bisher)**, **Verbrauch (Letzte Laufzeit)**, **Abschlag (Empfohlen)** und **Zählernummer** nicht an. Im Panel stehen die Kosten bisher und der Saldo heute trotzdem, denn sie kommen aus den Vertragsdaten. Die Prognose zum Vertragsende gibt es als Sensor. Mehr in [Vertrag-Wasser](Vertrag-Wasser).

## Versicherung

Zusätzlich zu den Sensoren für alle Verträge. Die Fahrzeugsensoren haben nur bei einer Kfz-Versicherung einen Wert.

| Name | Schlüssel | Einheit | Bedeutung | Attribute |
|---|---|---|---|---|
| Art der Versicherung | `versicherungsart` | – | Auswahl: Auto (Kfz), Gebäude / Haus, Hausrat, Haftpflicht, Kranken, Leben, Rechtsschutz, Unfall, Sonstige | – |
| Kennzeichen | `kennzeichen` | – | Kennzeichen des Fahrzeugs (Kategorie Diagnose) | – |
| Kilometerstand bei Vertragsbeginn | `km_start` | km | Kilometerstand bei Beginn | – |
| Erlaubte Kilometer pro Jahr | `km_pro_jahr` | km | vereinbarte Kilometer pro Jahr | – |

Mehr in [Vertrag-Versicherung](Vertrag-Versicherung).

## Leasing

Zusätzlich zu den Sensoren für alle Verträge bekommt ein Leasingvertrag die Fahrzeugsensoren **Kennzeichen**, **Kilometerstand bei Vertragsbeginn** und **Erlaubte Kilometer pro Jahr** (wie bei der Versicherung) und drei Sensoren für die Kilometer:

| Name | Schlüssel | Einheit | Bedeutung | Attribute |
|---|---|---|---|---|
| Gefahrene Kilometer | `leasing_km_gefahren` | km | Kilometerstand minus Stand bei Beginn | `km_stand`, `km_erlaubt`, `km_soll`, `abweichung_soll`, `km_rest`, `km_rest_je_tag`, `km_je_tag`, `prozent_der_erlaubten` |
| Kilometer bei Rückgabe (Hochrechnung) | `leasing_km_hochgerechnet` | km | Hochrechnung der Kilometer bis zur Rückgabe | `abweichung_ende`, `mehr_km`, `minder_km` |
| Erwartete Mehr-/Minderkilometer-Kosten | `leasing_km_kosten` | Währung | erwartete Nachzahlung oder Gutschrift bei Rückgabe | `nachzahlung`, `gutschrift`, `mehr_km`, `minder_km` |

Mehr in [Vertrag-Leasing](Vertrag-Leasing).

## Kredit

Zusätzlich zu den Sensoren für alle Verträge (bei einem Kredit ohne Verbrauch) vier Sensoren:

| Name | Schlüssel | Einheit | Bedeutung | Attribute |
|---|---|---|---|---|
| Restschuld | `kredit_restschuld` | Währung | verbleibende Schuld | `tilgung_prozent`, `rate`, `naechste_zahlung`, `zins_anteil`, `tilgung_anteil` |
| Gezahlt bisher | `kredit_gezahlt` | Währung | bisher gezahlte Raten | `zinsen`, `tilgung`, `zahlungen` |
| Restsumme | `kredit_restsumme` | Währung | noch zu zahlende Summe | `zahlungen_offen` |
| Zinsen bisher | `kredit_zinsen_bisher` | Währung | bisher gezahlte Zinsen | `zinsen_gesamt` |

Mehr in [Vertrag-Kredit](Vertrag-Kredit).

## Pauschalverträge

**Internet**, **Mobilfunk**, **Streaming**, **Hauskosten** und **Sonstiges** haben nur die Sensoren für alle Verträge. **Abschlag** ist dort der Betrag pro Monat, **Abschlag (Vertragslaufzeit)** der Gesamtbetrag der Laufzeit. Die vier Sensoren für Verbrauch und Prognose bleiben ohne Verbrauchssensor leer. Kosten bisher gibt es für diese Verträge nur im Panel, als die bis heute fälligen Abschläge.

## Buttons

Jeder Vertrag hat drei Buttons am selben Gerät. Ein Button ist nur **verfügbar**, solange seine Aktion Sinn hat.

| Name | Schlüssel | Verfügbar, wenn | Was er tut |
|---|---|---|---|
| Jetzt wechseln | `jetzt_wechseln` | ein Folgevertrag geplant ist | übernimmt den geplanten Folgevertrag sofort, ohne das Datum abzuwarten, und friert den Verbrauch der endenden Laufzeit wie beim automatischen Wechsel ein |
| Kündigung bestätigen | `kuendigung_bestaetigen` | die Kündigungs-Erinnerung aktiv ist | quittiert die Erinnerung und entfernt die Dauerbenachrichtigung |
| Abschlag-Warnung bestätigen | `abschlag_warnung_bestaetigen` | die Abschlag-Warnung offen und noch nicht bestätigt ist | quittiert die Warnung. Verschlechtert sich die Prognose später erneut, meldet sich Tariffy wieder |

Eine **Entity-ID** wie `button.strom_haus_jetzt_wechseln` ist wieder ein Beispiel. Im Panel heißen die Aktionen **Warnung bestätigen** und **Kündigung bestätigen**. Mehr in [Vertragsende-und-Wechsel](Vertragsende-und-Wechsel).

## Beispiel

Die Sensoren des Vertrags **Strom Haus** aus den Beispieldaten des Panels, Stichtag 12.07.2026 (Vertrag 01.01. bis 31.12.2026, Abschlag 40 €):

| Name | Wert |
|---|---|
| Abschlag | 40 EUR/Monat |
| Abschlag (Vertragslaufzeit) | 478,32 EUR |
| Arbeitspreis | 0,2977 EUR/kWh |
| Grundpreis | 11,51 EUR/Monat |
| Verbrauch (Bisher) | 1.481,17 kWh |
| Verbrauch (Vertragslaufzeit hochgerechnet) | 2.808,1 kWh |
| Kosten (Bisher) | 513,54 EUR |
| Guthaben/Nachzahlung (Bisher) | −206,24 EUR (mit Einmalposten +55 EUR) |
| Guthaben/Nachzahlung (Vertragsende) | −495,29 EUR, Attribut `tendenz`: `Nachzahlung` |
| Abschlag (Anpassung empfohlen) | 127,66 EUR/Monat |
| Restlaufzeit | 172 Tage |
| Vertragsbeginn | 01.01.2026 |
| Vertragsende | 31.12.2026 |

Wie diese Zahlen zusammenhängen, rechnet [Abschlaege-und-Kosten](Abschlaege-und-Kosten) vor.

## Siehe auch

- [Dashboard-Beispiele](Dashboard-Beispiele): Karten mit diesen Sensoren
- [Automationen](Automationen): Sensoren und Buttons in Automationen
- [Verbrauch-Messen](Verbrauch-Messen) und [Abschlaege-und-Kosten](Abschlaege-und-Kosten): wie die Werte entstehen
- [PV-Autarkie](PV-Autarkie): Attribute zur Autarkie
- [Panel-Uebersicht](Panel-Uebersicht): dieselben Werte im Panel
