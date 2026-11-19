🇩🇪 Deutsch · [🇬🇧 English](EN-FAQ)

# FAQ

Antworten auf die Fragen, die am häufigsten auftauchen. Wenn Du ein Problem hast, schau zuerst hier und danach in die [Fehlerbehebung](Fehlerbehebung).

**Inhalt:**
- [Das Panel ist leer oder schwarz](#das-panel-ist-leer-oder-schwarz)
- [Muss ich nach einem Update die Seite neu laden?](#muss-ich-nach-einem-update-die-seite-neu-laden)
- [Warum fehlen Verbrauch oder Kosten?](#warum-fehlen-verbrauch-oder-kosten)
- [Warum steht der Verbrauch nicht in kWh?](#warum-steht-der-verbrauch-nicht-in-kwh)
- [Folgevertrag oder Verlängern?](#folgevertrag-oder-verlängern)
- [Wo speichert Tariffy meine Daten?](#wo-speichert-tariffy-meine-daten)
- [Wer sieht persönliche Daten?](#wer-sieht-persönliche-daten)
- [Was passiert, wenn ich einen Vertrag lösche?](#was-passiert-wenn-ich-einen-vertrag-lösche)
- [Kann ich mehrere Verträge anlegen?](#kann-ich-mehrere-verträge-anlegen)
- [Wie oft rechnet Tariffy neu?](#wie-oft-rechnet-tariffy-neu)
- [Warum fehlt ein Sensor?](#warum-fehlt-ein-sensor)
- [Kann ich Beta-Versionen testen?](#kann-ich-beta-versionen-testen)

## Das Panel ist leer oder schwarz

Es gibt drei Fälle:

- **Die Meldung „Noch keine Verträge":** Das Panel zeigt sie, wenn es keinen Vertrag gibt. Lege einen unter Einstellungen → Geräte & Dienste → Tariffy an (Link „Vertrag anlegen"). Das Panel steht übrigens erst zur Verfügung, wenn mindestens ein Vertrag existiert.
- **Die Meldung „Das Panel konnte die Verträge nicht laden.":** Lade die Browserseite hart neu (Strg+F5). Bleibt der Fehler, schau in die [Fehlerbehebung](Fehlerbehebung#das-panel-ist-leer-oder-schwarz).
- **Schwarze Fläche ohne Meldung:** Das war ein Fehler bis Version 1.31.0 und ist in 1.32.0 behoben (das Panel blieb schwarz, bis ein anderes Dashboard geöffnet und wieder zurückgewechselt wurde). Aktualisiere und lade die Seite hart neu. Ein leeres Panel nach dem Anlegen oder Ändern eines Vertrags ist in 1.32.0 ebenfalls behoben.

## Muss ich nach einem Update die Seite neu laden?

Ja, einmal. Das Panel besteht aus mehreren Dateien, die der Browser lange zwischenspeichert. Nach einem Update lädst Du die Seite einmal hart neu (Strg+F5, am Mac Cmd+Shift+R), danach läuft die neue Version.

## Warum fehlen Verbrauch oder Kosten?

Kosten, Guthaben und Prognose brauchen einen eingetragenen **Arbeitspreis**. „Kosten (Bisher)", „Guthaben/Nachzahlung (Bisher)" und „Guthaben/Nachzahlung (Vertragsende)" brauchen zusätzlich einen **Verbrauchssensor** mit Langzeitstatistik (Long-Term Statistics). Wie Du den Sensor einrichtest, steht unter [Verbrauch messen](Verbrauch-Messen). Die Schritte zur Fehlersuche stehen in der [Fehlerbehebung](Fehlerbehebung#verbrauch-oder-kosten-bleiben-leer).

## Warum steht der Verbrauch nicht in kWh?

Die Sensoren „Verbrauch (Bisher)" und „Verbrauch (Vertragslaufzeit hochgerechnet)" zeigen die rohe Zählerdifferenz in der Einheit Deines Sensors, bei Gas und Wasser meist m³. Nur für die Kostenberechnung rechnet Tariffy intern bei Gas über Brennwert × Zustandszahl in kWh um. Es ist also kein Fehler, sondern Absicht.

Beispiel (Zahlen nur zur Veranschaulichung): 120 m³ Gas bei einem Brennwert von 10,0 kWh/m³ und einer Zustandszahl von 0,95 ergeben 120 × 10,0 × 0,95 = 1.140 kWh. Die Verbrauchssensoren zeigen weiter 120 m³, die Kosten rechnen mit 1.140 kWh.

## Folgevertrag oder Verlängern?

- **Folgevertrag planen**, wenn ein anderer Tarif oder ein anderer Anbieter zu einem Stichtag übernimmt. Tariffy wechselt am Wechseldatum von selbst.
- **Vertrag verlängern**, wenn derselbe Vertrag mit neuem Beginn, Ende und Betrag weiterläuft, etwa bei einer Beitragsanpassung. Das gibt es bei Verträgen ohne Verbrauch (Versicherung, Internet, Mobilfunk, Streaming, Sonstiges) und beim Kredit als Anschlussfinanzierung.

Der Unterschied mit allen Details steht unter [Folgevertrag oder Verlängern](Folgevertrag-oder-Verlaengern).

## Wo speichert Tariffy meine Daten?

Alles bleibt in Deinem Home Assistant:

- Die **Vertragsdaten** liegen in den Einstellungen des Vertrags in Home Assistant (jeder Vertrag ist ein eigener Eintrag der Integration).
- Der **Verbrauch** kommt aus den Langzeitstatistiken Deines Sensors; Tariffy liest sie nur.
- **Gelöschte Verträge** werden 30 Tage lang in Home Assistants Speicher unter `.storage/tariffy.deleted` aufbewahrt (höchstens die letzten 20).
- Die **Sicherungsdatei** aus dem Tab **Sicherung** liegt dort, wo Du sie speicherst. Sie enthält persönliche Daten, behandle sie entsprechend.
- Die Integration bringt keine zusätzlichen Python-Pakete mit (`requirements` in der `manifest.json` ist leer) und ist als `calculated` eingestuft, sie rechnet also nur mit Werten aus Home Assistant.

Die normalen Backups von Home Assistant sichern Tariffy mit. Mehr dazu unter [Sicherung und Umzug](Sicherung-und-Umzug).

## Wer sieht persönliche Daten?

**Kundennummer, Zählernummer(n) und Marktlokations-ID** schickt Tariffy nur an Administratoren. Sie stehen im Block **Vertrag** der Vertragsdetails (Tab **Verträge**); Browser anderer Benutzer bekommen sie nie. **Kennzeichen** und **Benachrichtigungs-Ziel** zeigt das Panel auch Administratoren nicht. Alle Aktionen, die etwas ändern, prüft zusätzlich das Backend, ein Nicht-Administrator kann sie auch über die Schnittstelle nicht auslösen. Die Einzelheiten stehen unter [Panel: Rechte und Design](Panel-Rechte-und-Design).

Zwei Stellen enthalten die persönlichen Daten trotzdem: die **Sicherungsdatei** und der **Eintrag eines gelöschten Vertrags** (30 Tage). Mit **Jetzt vergessen** im Tab **Sicherung** verschwindet ein gelöschter Vertrag samt seinen Daten sofort. Der **Diagnose-Download** schwärzt Kundennummer, Zählernummer(n), Marktlokation, Kennzeichen und Benachrichtigungs-Ziel (siehe [Fehlerbehebung](Fehlerbehebung#diagnose-herunterladen)).

## Was passiert, wenn ich einen Vertrag lösche?

- Offene Meldungen des Vertrags (Kündigungs-Erinnerung und Abschlag-Warnung) werden entfernt.
- Der Vertrag und seine Sensoren sind weg. Tariffy merkt sich den Vertrag aber **30 Tage lang** und bietet ihn im Tab **Sicherung** zum **Zurückholen** an. Das geht nicht, wenn es inzwischen einen Vertrag mit gleichem Namen und gleicher Sparte gibt.
- Ein zurückgeholter Vertrag ist ein neuer Vertrag mit neuen Sensoren. Die Statistik des alten Vertrags bleibt bei dessen Sensoren in Home Assistant.

Wenn Du den Vertrag nur aus der Übersicht haben willst, **archivierst** Du ihn besser: Dann wird nichts gelöscht. Siehe [Archiv und Historie](Archiv-und-Historie).

## Kann ich mehrere Verträge anlegen?

Ja. Jeder Vertrag wird als eigener Eintrag mit eigenem Gerät und eigenen Sensoren angelegt; die Integration kennt keine Obergrenze für Verträge, auch nicht für mehrere Verträge derselben Sparte. Du fügst weitere unter Einstellungen → Geräte & Dienste → Tariffy hinzu oder im Panel mit **Neuer Vertrag** (nur Administratoren). Mehr dazu unter [Verträge anlegen](Vertraege-Anlegen).

## Wie oft rechnet Tariffy neu?

Alle 6 Stunden und nach dem Start von Home Assistant, sobald die Langzeitstatistiken bereit sind. Ein geplanter Tarifwechsel wird zusätzlich täglich um 00:00:01 Uhr geprüft. Der Button **Jetzt wechseln** löst ihn sofort aus. Alles Weitere steht unter [Vertragsende und Wechsel](Vertragsende-und-Wechsel).

## Warum fehlt ein Sensor?

Sensoren für Nachttarif, Staffelpreise, Zweizählertarif (HT/NT), Leasing und Kredit gibt es nur, wenn die Sparte oder die Option genutzt wird. Die Liste steht in der [Sensoren-Referenz](Sensoren-Referenz).

## Kann ich Beta-Versionen testen?

Ja, über HACS, ohne dass andere davon etwas merken. Die Schritte stehen unter [Releases und Beta](Releases-und-Beta).

> **Gut zu wissen:** Nicht jede Frage steht hier. Findest Du Deine nicht, [eröffne ein Issue](https://github.com/weskona/tariffy/issues/new/choose) oder frag in den [Discussions](https://github.com/weskona/tariffy/discussions).

## Siehe auch

- [Fehlerbehebung](Fehlerbehebung)
- [Erste Schritte](Erste-Schritte)
- [Sensoren-Referenz](Sensoren-Referenz)
- [Releases und Beta](Releases-und-Beta)
