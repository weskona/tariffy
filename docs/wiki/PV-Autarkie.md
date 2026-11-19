🇩🇪 Deutsch · [🇬🇧 English](EN-PV-Self-Sufficiency)

# PV-Autarkie

Mit einer Photovoltaikanlage (auch mit Batterie) schwankt der Strom, den Du aus dem Netz beziehst, stark mit der Jahreszeit. Die PV-Autarkie sorgt dafür, dass die Prognose zum Vertragsende das berücksichtigt. Diese Seite ist für alle mit einem Stromvertrag und einer PV-Anlage.

**Inhalt:**
- [Wofür die PV-Autarkie gut ist](#wofür-die-pv-autarkie-gut-ist)
- [Einschalten](#einschalten)
- [Die drei Quellen](#die-drei-quellen)
- [So rechnet Tariffy](#so-rechnet-tariffy)
- [Gesamtverbrauch und Durch PV gedeckt](#gesamtverbrauch-und-durch-pv-gedeckt)
- [Wie die Autarkie in die Prognose eingeht](#wie-die-autarkie-in-die-prognose-eingeht)
- [Was Du am Sensor und im Panel siehst](#was-du-am-sensor-und-im-panel-siehst)
- [Beispiel](#beispiel)
- [Wann nichts passiert](#wann-nichts-passiert)
- [Siehe auch](#siehe-auch)

## Wofür die PV-Autarkie gut ist

Der Verbrauchssensor Deines Vertrags misst den **Netzbezug**. Wer im Winter auf die Prognose schaut, hat viel Netzbezug gemessen und rechnet damit fürs ganze Jahr: Die Prognose ist zu hoch. Wer im Sommer schaut, hat wenig gemessen: Sie ist zu niedrig.

Die **Autarkie** eines Monats ist der Anteil des Hausverbrauchs, den die Anlage deckt:

```
Autarkie = 1 − Netzbezug ÷ Gesamtverbrauch      (begrenzt auf 0 bis 100 %)
```

Mit der Option vergleicht Tariffy für jeden Restmonat der Laufzeit die Autarkie des **gleichen Monats im Vorjahr** mit der Autarkie im bisher gemessenen Zeitraum und passt den erwarteten Netzbezug entsprechend an.

- Die Option gilt **nur für die Restlaufzeit**. Der bisher gemessene Verbrauch und die Kosten bisher bleiben, wie sie sind.
- Es gibt sie nur bei **Strom** und **Strom (Zweizählertarif)**. Gas und Wasser bieten sie nicht an.
- Sie ist **standardmäßig aus**. Ohne die Option ändert sich nichts.

## Einschalten

1. Öffne den Stromvertrag zum Bearbeiten (im Panel **Vertrag bearbeiten**, siehe [Vertrag-Strom](Vertrag-Strom)).
2. Schalte **PV-Autarkie in der Prognose berücksichtigen** ein.
3. Gib die Quelle der Autarkie an, mindestens eine der drei unter [Die drei Quellen](#die-drei-quellen).
4. Der **Verbrauchssensor** des Vertrags muss den **Netzbezug** messen. Ohne Verbrauchssensor gibt es keine Prognose, an der sich etwas ändern ließe. Wie er funktioniert, steht in [Verbrauch-Messen](Verbrauch-Messen).
5. Speichere. Nach dem Neuladen rechnet Tariffy die Prognose mit der Autarkie.

## Die drei Quellen

Die Quellen gelten in dieser Reihenfolge: Ist Quelle 1 angegeben, bestimmt sie die Autarkie, sonst Quelle 2, sonst Quelle 3. Fehlt für einen Monat der Wert der Quelle 1 oder 2, gilt für diesen Monat Quelle 3 (falls eingetragen), sonst gibt es für den Monat keine Anpassung.

| Nr. | Feld im Formular | Was Du einträgst | Was Tariffy daraus macht |
|---|---|---|---|
| 1 | **Gesamtverbrauch des Hauses (Sensor)** | Sensor in kWh mit Langzeitstatistik (`total_increasing`), zum Beispiel der Hausverbrauch aus dem Energie-Dashboard | Autarkie je Monat aus den Energiesummen des Vorjahres: `1 − Netzbezug ÷ Gesamtverbrauch`. Die genaueste Quelle, funktioniert auch mit Batterie |
| 2 | **Autarkie-Sensor (%)** | Sensor mit dem Autarkiegrad in % und Statistik (`state_class` measurement), zum Beispiel die Autarkie der Fronius-Integration | Monatsmittelwert dieses Sensors im Vorjahr. Wird nicht benutzt, wenn Quelle 1 angegeben ist |
| 3 | **Autarkie, eigene Werte (%)** | Zwölf Werte für Januar bis Dezember, getrennt durch Leerzeichen oder Semikolon, zum Beispiel `10 10 25 50 70 80 85 80 60 35 15 10`, oder ein Wert für alle Monate | Der Wert des Monats. Gilt für Monate ohne Daten und reicht allein, zum Beispiel im ersten Jahr einer PV-Anlage ohne Historie |

Regeln für die eigenen Werte:

- Erlaubt sind ein Wert oder zwölf Werte zwischen 0 und 100, mit Komma oder Punkt als Dezimaltrennzeichen. Alles andere weist das Formular ab.
- **Ein einziger Wert für alle Monate ändert allein nichts.** Die Prognose vergleicht die Autarkie jedes Restmonats mit der des gemessenen Zeitraums, und ein einzelner Wert ist in jedem Monat gleich. Darum verlangt das Formular ohne Sensor zwölf **unterschiedliche** Monatswerte. Ein Wert für alle Monate ist nur als Ersatz für Monate ohne Daten **neben einem Sensor** sinnvoll.

**Zweizählertarif:** Zu Quelle 1 gibt es ein zweites Feld **Gesamtverbrauch Niedertarif-Zeit (Sensor)**. Ist es gefüllt, rechnet Tariffy je Tarif. Ohne das zweite Feld wird die Autarkie über beide Tarife zusammen berechnet und auf beide angewendet. Das ist eine Näherung und steht im Attribut `autarkie_naeherung`. Quelle 2 und 3 gelten für beide Tarife gleich.

## So rechnet Tariffy

Für jeden Kalendermonat der Restlaufzeit, mit den Tagen ab heute:

1. **Autarkie des Monats** `a_Monat`: bei Quelle 1 aus den Langzeitstatistiken des **gleichen Monats im Vorjahr** (Netzbezug und Gesamtverbrauch dieses Monats), bei Quelle 2 der Monatsmittelwert des Vorjahres, bei Quelle 3 Dein Wert. Immer auf 0 bis 100 % begrenzt.
2. **Autarkie bisher** `a_bisher`: aus derselben Quelle für den Zeitraum seit Vertragsbeginn. Bei Quelle 3 sind es Deine Werte der schon gemessenen Monate, nach Tagen gewichtet.
3. **Faktor** des Monats: `(1 − a_Monat) ÷ (1 − a_bisher)`.
4. **Netzbezug des Monats**: `Netzbezug je Tag bisher × Tage des Monats × Faktor`.

Die Summe aus dem Verbrauch bisher und diesen Monatswerten ist der hochgerechnete Netzbezug für die ganze Laufzeit.

Der Faktor hat Grenzen:

| Fall | Faktor |
|---|---|
| kein Wert für den Monat oder für den gemessenen Zeitraum | 1 (lineare Hochrechnung wie ohne Option) |
| Autarkie bisher fast 100 % (Netzanteil unter 5 %) | 1, denn die Rechnung wäre nicht belastbar |
| Monat voll autark (Autarkie 100 %) | 0 (kein Netzbezug) |
| Monat viel dunkler als der gemessene Zeitraum | höchstens 4 |

Beim Zweizählertarif wird je Tarif gerechnet. Dabei verschiebt sich auch der Mischpreis aus Hoch- und Niedertarif mit der Jahreszeit.

> **Gut zu wissen:** Für Quelle 1 braucht Tariffy Statistik des **Vorjahres** für den Gesamtverbrauch **und** für den Verbrauchssensor des Vertrags. Fehlt sie für einen Monat, bleibt dieser Monat bei der linearen Hochrechnung. Fehlt jede Historie, ändert sich nichts und es gibt keinen Fehler.

## Gesamtverbrauch und Durch PV gedeckt

Mit Quelle 1 kennt Tariffy auch den **Gesamtverbrauch** Deines Hauses. Im Panel erscheint dann im Block **Verbrauch** der Vertragsdetails (Tab **Verträge**) ein kleines Raster mit den Spalten **Bisher** und **Hochgerechnet**:

| Zeile im Panel | Bedeutung |
|---|---|
| **Gesamtverbrauch** | Gesamtverbrauch des Hauses in kWh |
| **Durch PV gedeckt** | Gesamtverbrauch minus Netzbezug, nie negativ |
| **Netzbezug (abgerechnet)** | der Verbrauch, den Dein Versorger abrechnet, also der Verbrauchssensor des Vertrags |

- Der Gesamtverbrauch wird **linear** fortgeschrieben: Die Jahreszeit steckt nur im Netzbezug.
- Beim Zweizählertarif werden beide Tarife addiert. Gibt es nur einen Gesamtverbrauchs-Sensor, zählt er einmal.
- Mit einem Autarkie-Sensor in % (Quelle 2) oder eigenen Werten (Quelle 3) gibt es keinen Gesamtverbrauch, das Raster erscheint dann nicht.
- Der Netzbezug und alle Kosten bleiben, wie sie sind. Das Raster zeigt nur zusätzliche Zahlen.

## Wie die Autarkie in die Prognose eingeht

Der angepasste Netzbezug ersetzt in der Prognose die lineare Hochrechnung:

- **Verbrauch (Vertragslaufzeit hochgerechnet)** zeigt den angepassten Wert.
- **Guthaben/Nachzahlung (Vertragsende)** rechnet mit den geschätzten Kosten aus diesem Verbrauch. Beim Zweizählertarif gilt dafür der gewichtete Mischpreis der Jahreszeit.
- **Abschlag (Anpassung empfohlen)** folgt derselben geschätzten Kostensumme.
- Die **Abschlag-Warnung** richtet sich nach der Prognose und damit auch nach der Autarkie.
- **Unverändert** bleiben **Verbrauch (Bisher)**, **Kosten (Bisher)** und **Guthaben/Nachzahlung (Bisher)**.

Den Rechenweg der Prognose zeigt [Abschlaege-und-Kosten](Abschlaege-und-Kosten).

## Was Du am Sensor und im Panel siehst

Der Sensor **Guthaben/Nachzahlung (Vertragsende)** bekommt zusätzliche Attribute, **nur wenn die Autarkie die Prognose wirklich bestimmt**. Ist die Option aus oder fehlt die Historie, sehen die Attribute aus wie immer.

| Attribut | Inhalt |
|---|---|
| `autarkie_variante` | die Quelle: `gesamtverbrauch`, `entitaet` oder `manuell` |
| `autarkie_monatswerte` | eine Zeile je Restmonat: `monat`, `tage`, `autarkie` (in %), `faktor`, `quelle` (`statistik` oder `manuell`); beim Zweizählertarif auch `autarkie_nt` und `faktor_nt` |
| `autarkie_bisher` | Autarkie im gemessenen Zeitraum in % |
| `autarkie_bisher_nt` | dasselbe für den Niedertarif (nur Zweizählertarif) |
| `autarkie_naeherung` | `true`, wenn bei zwei Tarifen nur ein Gesamtverbrauchs-Sensor die Autarkie für beide bestimmt |
| `prognose_ohne_autarkie` | die Prognose zum Vertragsende mit linearer Hochrechnung |

Nur mit einem Gesamtverbrauchs-Sensor (Quelle 1) kommen dazu: `verbrauch_gesamt_bisher`, `verbrauch_gesamt_hochgerechnet`, `verbrauch_pv_gedeckt_bisher` und `verbrauch_pv_gedeckt_hochgerechnet`.

Im Panel zeigen die Vertragsdetails im Block **Verbrauch** zusätzlich **Prognose zum Vertragsende ohne PV-Autarkie**, **PV-Autarkie bisher** (beim Zweizählertarif mit dem Niedertarif-Wert) und **Quelle der Autarkie** (**Gesamtverbrauch des Hauses**, **Autarkie-Sensor** oder **Eigene Werte**). Bei der Näherung steht außerdem die Zeile **Autarkie über beide Tarife (Näherung)**.

## Beispiel

Das Beispiel stammt aus den Tests von Tariffy (Beispieldaten, nicht Dein Vertrag).

- Vertrag 01.01. bis 31.12.2026 (364 Tage), Arbeitspreis 0,30 €/kWh, Grundpreis 10 €/Monat, Abschlag 100 €/Monat.
- Stichtag 01.07.2026, nach **181 Tagen**: Netzbezug bisher **1.800 kWh**, Gesamtverbrauch des Hauses bisher **3.600 kWh**. Die Autarkie bisher ist damit `1 − 1.800 ÷ 3.600 = 50 %`.
- Im Vorjahr betrug der Gesamtverbrauch jeden Monat 300 kWh. Der Netzbezug im Vorjahr war von Juli bis Dezember 50, 50, 100, 150, 200 und 250 kWh.

| Monat | Tage | Autarkie im Vorjahr | Faktor `(1 − a) ÷ 0,5` |
|---|---|---|---|
| Juli | 31 | 83,3 % | 0,333 |
| August | 31 | 83,3 % | 0,333 |
| September | 30 | 66,7 % | 0,667 |
| Oktober | 31 | 50,0 % | 1,000 |
| November | 30 | 33,3 % | 1,333 |
| Dezember | 30 | 16,7 % | 1,667 |

```
Netzbezug je Tag bisher      = 1.800 kWh ÷ 181 Tage                        = 9,945 kWh
Netzbezug der Restlaufzeit   = 9,945 × (31×0,333 + 31×0,333 + 30×0,667 + 31×1 + 30×1,333 + 30×1,667)
                             = 9,945 × 161,67                               = 1.607,7 kWh
Hochgerechnet mit Autarkie   = 1.800 + 1.607,7                              = 3.407,7 kWh
Hochgerechnet linear         = 1.800 ÷ 181 × 364                            = 3.619,9 kWh
```

Die Faktoren unter 1 (Juli bis September) senken den erwarteten Netzbezug, die über 1 (November und Dezember) erhöhen ihn. Insgesamt liegt die angepasste Hochrechnung unter der linearen.

```
Abschläge über die Laufzeit  = 100 € × 11,958 Monate                       = 1.195,80 €
Kosten mit Autarkie          = 3.407,7 kWh × 0,30 € + 10 € × 11,958         = 1.141,90 €
Kosten linear                = 3.619,9 kWh × 0,30 € + 10 € × 11,958         = 1.205,55 €

Guthaben/Nachzahlung (Vertragsende)  mit Autarkie   = 1.195,80 € − 1.141,90 € = +53,90 €
prognose_ohne_autarkie                              = 1.195,80 € − 1.205,55 € =  −9,75 €
```

Die lineare Rechnung hätte eine kleine Nachzahlung vorhergesagt, mit der Autarkie ist es ein Guthaben. Der Gesamtverbrauch des Hauses wäre linear `3.600 ÷ 181 × 364 = 7.239,8 kWh`; **Durch PV gedeckt** sind bisher 1.800 kWh und hochgerechnet `7.239,8 − 3.407,7 = 3.832,0 kWh`.

## Wann nichts passiert

Die Option bleibt wirkungslos, ohne Fehlermeldung, wenn:

- kein Verbrauchssensor im Vertrag steht oder noch kein Verbrauch größer als null gemessen ist,
- keine der drei Quellen angegeben ist (Option an, aber alles leer),
- die Statistik des Vorjahres für Gesamtverbrauch oder Netzbezug fehlt und keine eigenen Werte da sind,
- die Autarkie bisher nicht berechenbar ist, etwa weil der Gesamtverbrauch null ist,
- der Vertrag nicht Strom oder Strom (Zweizählertarif) ist.

Ein Verbrauchssensor, der den **Gesamtverbrauch** statt des Netzbezugs misst, passt nicht zu dieser Option.

## Siehe auch

- [Verbrauch-Messen](Verbrauch-Messen): wie der Verbrauch bisher entsteht
- [Abschlaege-und-Kosten](Abschlaege-und-Kosten): Prognose und empfohlener Abschlag
- [Vertrag-Strom](Vertrag-Strom): das Stromformular mit den Feldern zur Autarkie
- [Sensoren-Referenz](Sensoren-Referenz): Attribute des Sensors Guthaben/Nachzahlung (Vertragsende)
- [Dashboard-Beispiele](Dashboard-Beispiele): die Autarkie-Werte auf dem Dashboard
