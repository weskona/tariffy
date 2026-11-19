🇩🇪 Deutsch · [🇬🇧 English](EN-Contract-Electricity)

# Vertrag Strom

Diese Seite erklärt alle Felder eines Stromvertrags (Sparte **Strom** und **Strom (Zweizählertarif, Hoch-/Niedertarif)**), wie Tariffy daraus Kosten, Saldo und Prognose rechnet, und was bei Zweizählertarif, Nachttarif, dynamischem Tarif, Einspeisevergütung und Staffelpreisen gilt.

**Inhalt:**

- [So rechnet Tariffy](#so-rechnet-tariffy)
- [Die Formularfelder](#die-formularfelder)
- [Zähler-Sensor und Einheiten](#zähler-sensor-und-einheiten)
- [Zweizählertarif HT/NT](#zweizählertarif-htnt)
- [Tag-/Nachttarif](#tag-nachttarif)
- [Dynamischer Tarif](#dynamischer-tarif)
- [Einspeisevergütung](#einspeisevergütung)
- [Staffelpreise](#staffelpreise)
- [Rechenbeispiel](#rechenbeispiel)
- [Typische Fehler](#typische-fehler)

## So rechnet Tariffy

Mit einem **Verbrauchssensor** misst Tariffy den Verbrauch seit Vertragsbeginn und rechnet daraus (ein Monat zählt dabei 30,44 Tage):

```
Verbrauch (Bisher)   = aktueller Zählerstand − Zählerstand am Vertragsbeginn
Kosten (Bisher)      = Verbrauch bisher × Arbeitspreis + Grundpreis × vergangene Monate
Guthaben/Nachzahlung (Bisher) = bis heute fällige Abschläge − Kosten (Bisher)
Verbrauch hochgerechnet       = Verbrauch bisher ÷ vergangene Tage × Tage der Vertragslaufzeit
```

Die Vertragslaufzeit ist Vertragsende minus Vertragsbeginn in Tagen (365 Tage, wenn kein Vertragsende eingetragen ist). Die Prognose zum Vertragsende rechnet die hochgerechneten Kosten gegen die Abschläge der ganzen Laufzeit. **Plus ist Guthaben, Minus ist Nachzahlung.** Alle vier Kosten-Sensoren erklärt [Sensoren Referenz](Sensoren-Referenz), das Messen selbst [Verbrauch messen](Verbrauch-Messen), den Abschlag [Abschläge und Kosten](Abschlaege-und-Kosten).

## Die Formularfelder

Das zweite Formular heißt **Strom-Details** („Preise, Verbrauch und Zählerdaten.“). Beim Zweizählertarif heißt es **Strom-Details (Zweizählertarif, Hoch-/Niedertarif)**.

| Feld | Pflicht | Beschreibung |
|---|---|---|
| Arbeitspreis (€/kWh) | ja | Preis pro verbrauchter kWh, steht auf Deiner Rechnung. Dient auch als Ersatz, solange für den Preissensor noch keine Statistik vorliegt. Beim Zweizählertarif heißt das Feld **Arbeitspreis Hochtarif / HT (€/kWh)**. |
| Preissensor für dynamischen Tarif (optional) | nein | Sensor mit dem Börsen- oder Spotpreis, siehe [Dynamischer Tarif](#dynamischer-tarif). |
| Aufschlag dynamischer Tarif (€/kWh) | nein | Fester Aufschlag auf den Preis des Preissensors. |
| Grundpreis (€/Monat) | ja | Monatlicher Festbetrag unabhängig vom Verbrauch. |
| Monatlicher Abschlag (€/Monat) | ja | Monatliche Vorauszahlung an den Anbieter. |
| Geschätzter Jahresverbrauch (kWh) | nein | Schätzung in kWh. Sie dient als Eingabe für die Anzeige bei Staffelpreisen und Nachttarif und erscheint als Attribut am Sensor **Arbeitspreis**. Kosten bisher und Prognose rechnen mit dem gemessenen Verbrauch, nicht mit dieser Schätzung. |
| Verbrauchssensor (optional) | nein | Sensor Deines Stromzählers; ermöglicht die echte Verbrauchsmessung. Beim Zweizählertarif ist das das Hochtarif-Register. |
| Zählerstand bei Vertragsbeginn (optional) | nein | Dein genauer Zählerstand am Vertragsbeginn, falls Du ihn kennst (zum Beispiel von der Abrechnung). Hat Vorrang vor der automatischen Erkennung. Hilft, wenn die Statistik des Sensors nicht bis zum Vertragsbeginn reicht. |
| Warnen, wenn Abschlag zu niedrig ist | nein | Aus nach der Voreinstellung. Ist die Option an und liegt die Prognose zum Vertragsende mehr als die Schwelle im Minus, meldet Tariffy das als Benachrichtigung in Home Assistant (und über das Benachrichtigungs-Ziel, falls eingetragen), bis Du sie mit **Abschlag-Warnung bestätigen** quittierst. |
| Warnschwelle (€ Nachzahlung) | nein | Voreinstellung 50. |
| PV-Autarkie in der Prognose berücksichtigen | nein | Freiwillig, nur für die Restlaufzeit. Dazu **Gesamtverbrauch des Hauses (Sensor)**, **Autarkie-Sensor (%)** oder **Autarkie, eigene Werte (%)**. Beim Zweizählertarif zusätzlich **Gesamtverbrauch Niedertarif-Zeit (Sensor)**. Alles dazu unter [PV-Autarkie](PV-Autarkie). |
| Einspeisevergütung (€/kWh, optional) | nein | Siehe [Einspeisevergütung](#einspeisevergütung). |
| Neukundenbonus / Sofortbonus (€) | nein | Einmaliger Bonus des Anbieters. Der Wert wird gespeichert und als Attribut `bonus` am Sensor **Arbeitspreis** gezeigt, fließt aber nicht in die Kosten ein. Für einen Bonus, der den Saldo ändern soll, nutzt Du einen Einmalposten, siehe [Abschlagsverlauf und Einmalposten](Abschlagsverlauf-und-Einmalposten). |
| Ökostrom | ja | Ja oder Nein, nur zur Dokumentation (Attribut `oekostrom`). |
| Zählernummer | nein | Zur Dokumentation. Beim Zweizählertarif ist das das Hochtarif-Register. |
| Marktlokation (MaLo-ID) / Zählpunkt | nein | Zur Dokumentation. |
| Preisgarantie bis | nein | Datum, bis zu dem der Arbeitspreis garantiert ist (Attribut `preisgarantie_bis`). |

Nur beim Zweizählertarif kommen diese Felder dazu (siehe unten): **Arbeitspreis Niedertarif / NT (€/kWh)**, **Verbrauchssensor Niedertarif / NT (optional)**, **Zählerstand bei Vertragsbeginn, NT (optional)** und **Zählernummer Niedertarif / NT**.

Je nach dem in Home Assistant eingestellten Land erscheinen außerdem **Staffelpreise aktivieren** mit den Blöcken und, bei Strom (nicht beim Zweizählertarif), der **Nachttarif**. Beides steht in den eigenen Abschnitten unten.

> **Gut zu wissen:** Preise, Abschlag und Grundpreis sind Zahlenfelder. Die Einheit der Preise ist die Währung Deiner Home-Assistant-Installation je kWh.

## Zähler-Sensor und Einheiten

- Der **Verbrauchssensor** muss ein Sensor mit Langzeitstatistik sein, der die kumulierte Summe führt (ein Zählersensor, wie ihn das Energie-Dashboard nutzt). Tariffy liest daraus den Stand zu Vertragsbeginn und den aktuellen Stand.
- Meldet der Sensor in **Wh** oder **MWh**, rechnet Tariffy den Verbrauch in **kWh** um (Wh × 0,001, MWh × 1000). Andere Einheiten bleiben unverändert. Ein manueller **Zählerstand bei Vertragsbeginn** wird in der Einheit des Zählers eingegeben.
- Der Sensor **Verbrauch (Bisher)** zeigt bei Strom immer kWh.
- Ist der Sensor kurz nicht verfügbar, benutzt Tariffy beim manuellen Zählerstand den zuletzt aufgezeichneten Statistikwert, damit die Sensoren nicht auf „unbekannt“ fallen.

Mehr zu den Zählerstand-Methoden und Zählerresets steht unter [Verbrauch messen](Verbrauch-Messen).

## Zweizählertarif HT/NT

Die Sparte **Strom (Zweizählertarif, Hoch-/Niedertarif)** ist für einen Zähler mit zwei Registern: Hochtarif (HT) und Niedertarif (NT). Jedes Register hat einen eigenen Arbeitspreis, einen eigenen Verbrauchssensor, einen eigenen manuellen Startwert und eine eigene Zählernummer.

- Tariffy rechnet beide Register getrennt: **Verbrauch Hochtarif (Bisher)** und **Verbrauch Niedertarif (Bisher)** in kWh, dazu **Kosten Hochtarif (Bisher)** und **Kosten Niedertarif (Bisher)** (ohne Grundpreis-Anteil).
- Für die übrigen Sensoren (Kosten, Saldo, Prognose, empfohlener Abschlag) verwendet Tariffy einen **gewichteten Durchschnittspreis** aus beiden Registern, gewichtet mit dem gemessenen Verbrauch. **Verbrauch (Bisher)** ist die Summe beider Register.
- Fehlt der Niedertarif-Sensor oder ist er noch ohne Wert, rechnet Tariffy nur mit dem Hochtarif-Preis.
- Zusätzliche Sensoren gibt es nur bei dieser Sparte: **Arbeitspreis (Niedertarif / NT)**, **Zählernummer (Niedertarif / NT)** und die vier Hochtarif-/Niedertarif-Sensoren für Verbrauch und Kosten.
- Der Nachttarif (Economy 7) gehört zu **Strom**, nicht zum Zweizählertarif.

## Tag-/Nachttarif

Für Länder mit Tag-/Nachttarifen (Economy 7, Time of Use) zeigt das Formular drei Felder: **Nachttarif (z.B. Economy 7, TOU Nebenzeit)**, **Jahresverbrauch Tag** und **Jahresverbrauch Nacht**. Sie erscheinen, wenn in Home Assistant eines dieser Länder eingestellt ist: GB, US, CA, AU, NZ, IE. Der **Arbeitspreis** ist dann der Tagpreis.

Sind alle drei Felder ausgefüllt, gibt es den Sensor **Arbeitspreis (Nacht)**. Seine Attribute zeigen die Jahresverbräuche und `tou_jahreskosten`, das ist Tagverbrauch × Arbeitspreis + Nachtverbrauch × Nachtpreis. Diese Zahl ist eine Anzeige. Die **Kosten (Bisher)** rechnen weiter mit dem gemessenen Verbrauch und dem einen Arbeitspreis.

Hast Du in Deutschland einen Zähler mit zwei Registern, nimm den [Zweizählertarif](#zweizählertarif-htnt).

## Dynamischer Tarif

Bei einem dynamischen Tarif (Tibber, aWATTar, Nordpool und ähnliche) trägst Du statt eines festen Preises einen Preissensor ein:

1. Wähle im Feld **Preissensor für dynamischen Tarif (optional)** den Sensor mit dem aktuellen Börsen- oder Spotpreis.
2. Trage bei **Aufschlag dynamischer Tarif (€/kWh)** Deinen festen Aufschlag ein (zum Beispiel die Marge des Anbieters).
3. Lass den **Arbeitspreis** als Ersatzwert stehen.

Tariffy ersetzt dann den Arbeitspreis durch den **Durchschnitt des Preissensors seit Vertragsbeginn** (aus den Langzeitstatistiken, Mittelwerte je Stunde) **plus Aufschlag**. Liegt noch keine Statistik vor, bleibt der eingetragene Arbeitspreis. Der Sensor **Arbeitspreis** zeigt diesen Durchschnittspreis, bekommt das Symbol `mdi:chart-line` und hat zwei Attribute: `arbeitspreis_aktuell` (aktueller Live-Preis plus Aufschlag) und `dynamischer_tarif`.

> **Gut zu wissen:** Der Durchschnitt ist ein einfacher Mittelwert der Stundenwerte, nicht nach Deinem Verbrauch gewichtet. Tariffy rechnet den Sensorwert nicht um; er muss den Preis in der Währung je kWh liefern, wie der Aufschlag.

## Einspeisevergütung

Das Feld **Einspeisevergütung (€/kWh, optional)** speichert die Vergütung für eingespeisten Strom (zum Beispiel bei Photovoltaik). Sie ist überall verfügbar und wird als Sensor **Einspeisevergütung** angezeigt. Tariffy rechnet damit **nichts**: Es gibt keine Erlös-Rechnung und die Kosten ändern sich nicht.

## Staffelpreise

Gestaffelte Preise (Blöcke mit steigendem Preis) gibt es nur für die Länder US, CA, AU, NZ, ES, PT, IT, GR, IL, IN, BR, MX, ZA, CN, JP, KR. Dort erscheinen **Staffelpreise aktivieren** und bis zu fünf Blöcke mit **Block 1 Obergrenze** und **Block 1 Preis** bis **Block 5 Obergrenze** und **Block 5 Preis**. Lässt Du die Obergrenze eines Blocks leer, gilt dieser Block für den ganzen Rest. Ein Block ohne Preis beendet die Liste.

Tariffy rechnet damit die Jahreskosten für Deinen **Geschätzten Jahresverbrauch (kWh)** und zeigt sie mit dem durchschnittlichen Preis im Sensor **Arbeitspreis (Effektiv)**. Beispiel aus den Tests: Block 1 bis 1.000 kWh zu 0,10 €, Block 2 darüber zu 0,20 €, Jahresverbrauch 1.500 kWh. Das ergibt 1.000 × 0,10 + 500 × 0,20 = 200 €, also 0,1333 €/kWh effektiv. Auch das ist eine Anzeige; **Kosten (Bisher)** und die Prognose bleiben beim Arbeitspreis.

## Rechenbeispiel

Der Beispiel-Vertrag „Strom Haus“: Abschlag 40 €/Monat, Arbeitspreis 0,2977 €/kWh, Grundpreis 11,51 €/Monat, Laufzeit 01.01. bis 31.12.2026 (364 Tage, 11,958 Monate). Heute ist der 12.07.2026, also Tag 192 (6,3075 Monate). Der Zähler stand bei Vertragsbeginn bei 1.000 kWh und steht jetzt bei 2.481,17 kWh. Die Zahlen sind die des Testfalls in `tests/test_coordinator.py`; es sind Mock-Daten.

```
Verbrauch (Bisher)                    = 2.481,17 − 1.000                      = 1.481,17 kWh
Kosten (Bisher)                       = 1.481,17 × 0,2977 + 11,51 × 6,3075    =   513,54 €
Abschläge bisher fällig               = 40 × 6,3075                           =   252,30 €
→ Guthaben/Nachzahlung (Bisher)       = 252,30 − 513,54                       =  −261,24 €  (Nachzahlung)

Verbrauch hochgerechnet               = 1.481,17 ÷ 192 × 364                  = 2.808,1 kWh
Abschlag (Vertragslaufzeit)           = 40 × 11,958                           =   478,32 €
Geschätzte Kosten zum Vertragsende    = 2.808,1 × 0,2977 + 11,51 × 11,958    =   973,61 €
→ Guthaben/Nachzahlung (Vertragsende) = 478,32 − 973,61                       =  −495,29 €  (Nachzahlung, Prognose)
```

(Die Monate sind Tage ÷ 30,44: 192 ÷ 30,44 = 6,3075 und 364 ÷ 30,44 = 11,958.)

Der Verbrauch liegt deutlich über dem, was der Abschlag deckt: Die Nachzahlung wächst von −261 € heute auf prognostizierte −495 € zum Vertragsende. Das Panel zeigt dieselben Werte in der Karte „Strom Haus“.

### Beispiel Zweizählertarif

Ein Vertrag mit Hochtarif zu 0,30 €/kWh und Niedertarif zu 0,20 €/kWh, Grundpreis 11,51 €/Monat, Abschlag 40 €/Monat, gleiche Laufzeit und gleicher Tag wie oben. Seit Beginn wurden im Hochtarif 300 kWh und im Niedertarif 300 kWh gemessen (Zahlen aus den Tests):

```
Kosten Hochtarif (Bisher)   = 300 × 0,30                                  =  90,00 €
Kosten Niedertarif (Bisher) = 300 × 0,20                                  =  60,00 €
Verbrauch (Bisher)          = 300 + 300                                   = 600 kWh
Gewichteter Arbeitspreis    = (300 × 0,30 + 300 × 0,20) ÷ 600             = 0,25 €/kWh
Kosten (Bisher)             = 600 × 0,25 + 11,51 × 6,3075                 = 222,60 €
```

Die Abschläge bisher (252,30 €) ergeben hier ein Guthaben von etwa +29,70 €.

## Typische Fehler

| Problem | Ursache und Lösung |
|---|---|
| **Kosten (Bisher)**, Saldo und Prognose bleiben leer | Es fehlt der Verbrauchssensor oder der Vertragsbeginn. Siehe [Fehlerbehebung](Fehlerbehebung). |
| Der Verbrauch ist unbekannt | Die Statistik des Sensors reicht nicht bis zum Vertragsbeginn. Trage den **Zählerstand bei Vertragsbeginn (optional)** ein. |
| Der Verbrauch ist um den Faktor 1.000 zu klein oder zu groß | Tariffy rechnet nur Wh und MWh in kWh um. Meldet der Sensor in einer anderen Einheit, wird der Wert unverändert übernommen. |
| Die Kosten stimmen nicht mit der Rechnung überein | Prüfe Arbeitspreis, Grundpreis, Vertragsbeginn und Abschlag. Tariffy rechnet die Monate tagesgenau (ein Monat sind 30,44 Tage), die Rechnung des Versorgers kann anders abgrenzen. |
| Nachttarif oder Staffelpreise fehlen im Formular | Sie erscheinen nur, wenn in Home Assistant eines der oben genannten Länder eingestellt ist. |
| Sensor **Arbeitspreis (Nacht)** oder **Arbeitspreis (Effektiv)** fehlt | **Arbeitspreis (Nacht)** gibt es nur, wenn Arbeitspreis, Nachttarif und beide Jahresverbräuche eingetragen sind. **Arbeitspreis (Effektiv)** gibt es nur bei aktivierten Staffelpreisen und hat einen Wert mit Blockpreis und Jahresverbrauch. |
| Dynamischer Tarif: Preis wirkt viel zu hoch | Der Preissensor liefert zum Beispiel ct/kWh statt €/kWh. Tariffy rechnet nicht um. |

## Siehe auch

- [Verträge anlegen](Vertraege-Anlegen)
- [Verbrauch messen](Verbrauch-Messen)
- [PV-Autarkie](PV-Autarkie)
- [Abschläge und Kosten](Abschlaege-und-Kosten)
- [Sensoren Referenz](Sensoren-Referenz)
- [Folgevertrag oder Verlängern](Folgevertrag-oder-Verlaengern)
- [Fehlerbehebung](Fehlerbehebung)
