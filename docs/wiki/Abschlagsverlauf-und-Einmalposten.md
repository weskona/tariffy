🇩🇪 Deutsch · [🇬🇧 English](EN-Payment-History-and-One-off-Items)

# Abschlagsverlauf und Einmalposten

Diese Seite erklärt zwei Werkzeuge im Panel, mit denen Du die Zahlen eines Vertrags der Wirklichkeit anpasst: den **Abschlagsverlauf** („Abschläge bearbeiten“), wenn Dein Anbieter den Abschlag mitten in der Laufzeit geändert hat, und **Einmalposten**, zum Beispiel einen Wechselbonus oder eine Maklerrechnung. Beide gibt es im Tab **Verträge** und nur für Administratoren.

**Inhalt:**
- [Wann Du den Abschlagsverlauf brauchst](#wann-du-den-abschlagsverlauf-brauchst)
- [Gezahlte Abschläge eintragen](#gezahlte-abschläge-eintragen)
- [Wie Tariffy den Verlauf rechnet](#wie-tariffy-den-verlauf-rechnet)
- [Frühere Laufzeiten](#frühere-laufzeiten)
- [Einmalposten](#einmalposten)
- [Beispiel](#beispiel)
- [Siehe auch](#siehe-auch)

## Wann Du den Abschlagsverlauf brauchst

Tariffy rechnet **Gezahlt bisher** standardmäßig mit dem aktuellen Abschlag für die ganze bisherige Laufzeit. Hat Dein Anbieter den Abschlag in der Zwischenzeit geändert, stimmt das nicht: Saldo und Prognose wären zu optimistisch oder zu pessimistisch.

- Änderst Du den Abschlag im Vertragsformular, merkt sich Tariffy das Datum und den alten Wert und rechnet den alten Betrag nur bis dahin. Mehrere Änderungen am selben Tag zählen als eine.
- Wenn der Anbieter den Abschlag öfter geändert hat, oder Du das genaue Datum nicht mehr weißt, trägst Du im **Abschlagsverlauf** ein, **was Du für jede Zahlung wirklich gezahlt hast**. Er ersetzt dann die einzelne Änderung.

Ohne Eintrag bleibt alles wie bisher. Kredite haben keinen Abschlagsverlauf.

## Gezahlte Abschläge eintragen

1. Öffne im Tab **Verträge** die Details des Vertrags (Pfeil in der Zeile).
2. Im Block **Gezahlte Abschläge** steht, was schon erfasst ist, jeweils mit **Ab** und dem Datum. Der letzte Eintrag trägt das Wort **aktuell**. Ohne Eintrag steht dort **Noch kein Verlauf: Der aktuelle Abschlag gilt für die ganze Laufzeit.**
3. Klicke auf **Gezahlte Abschläge eintragen** (noch kein Verlauf) oder **Abschläge bearbeiten** (es gibt schon einen).
4. Es öffnet sich der Dialog **Gezahlte Abschläge** mit **einem Feld je Zahlung**:
   - bei monatlicher Zahlweise ein Feld je Monat (Spalten **Monat** und **Abschlag (€)**),
   - bei vierteljährlicher vier Felder im Jahr, bei halbjährlicher zwei, bei jährlicher eines (Spalten **Zahlung** und **Betrag je Zahlung (€)**), jeweils zum Tag der Abbuchung.
5. Trage in jedes Feld ein, was für diese Zahlung gezahlt wurde. **Eine Änderung gilt auch für die folgenden Zahlungen, die noch denselben Betrag haben.** Ändere also nur die Felder, die abweichen. Komma oder Punkt sind als Dezimaltrennzeichen möglich.
6. **Zahlungen, die noch nicht fällig waren**, sind gesperrt und zeigen den aktuellen Abschlag. **Die letzte fällige Zahlung ist der aktuelle Abschlag** des Vertrags.
7. Klicke auf **Speichern**.

**Eine Zahlung ist ausgefallen?** Trage für diese Zahlung **0** ein (zum Beispiel für September, wenn der Versorger den Abschlag nicht abgebucht hat), und danach beim nächsten Monat wieder den normalen Betrag, denn eine Änderung gilt auch für die folgenden Zahlungen mit demselben Betrag. Eine **0 in der letzten Zahlung** geht nicht, denn die letzte Zahlung ist der aktuelle Abschlag, der weiterläuft. Die ausgefallene Zahlung zählt dann bei **Gezahlt bisher** als nichts gezahlt.

Ein leeres Feld übernimmt den Betrag der Zahlung davor, nur das erste Feld muss gefüllt sein. Sonst meldet der Dialog **Trage einen Betrag für den ersten Monat ein.**

Fehlermeldungen des Dialogs:

| Meldung | Ursache |
|---|---|
| **Ein Datum ist ungültig (nicht in der Zukunft, jeder Monat einmal).** | ein Datum in der Zukunft oder doppelt |
| **Ein Betrag darf nicht negativ sein.** | ein Betrag ist negativ oder keine Zahl |
| **Der letzte Monat ist der aktuelle Betrag, der weiterläuft, und muss über null liegen. Nur eine frühere Zahlung darf 0 sein.** | im letzten Feld steht 0 |
| **Zu viele Änderungen (höchstens 60).** | mehr als 60 Änderungen im Verlauf |
| **Dieser Vertrag hat keine Abschläge.** | der Vertrag ist ein Kredit |
| **Der Vertrag braucht einen Beginn, bevor sich die Abschläge nach Monaten eintragen lassen.** | im Vertrag fehlt der Beginn |

Gespeichert werden nur die Zahlungen, bei denen sich der Betrag ändert. Jeder Eintrag besteht aus dem Datum (**Ab**) und dem Betrag **pro Monat**. Bei vierteljährlicher Zahlung teilt Tariffy den eingetragenen Betrag durch 3, bei halbjährlicher durch 6, bei jährlicher durch 12. Ein leerer Verlauf löscht ihn, der Abschlag des Vertrags bleibt.

> **Gut zu wissen:** Ändert sich der Abschlag später im Vertragsformular und es gibt schon einen Verlauf, hängt Tariffy einen neuen Eintrag mit dem heutigen Datum an. Bei einer Änderung am selben Tag ersetzt sie den letzten Eintrag.

## Wie Tariffy den Verlauf rechnet

- **Verbrauchsverträge:** Jeder Betrag gilt für die Monate zwischen seinem Datum und dem nächsten Eintrag (Tage ÷ 30,44). Vor dem ersten Eintrag gilt dessen Betrag. Ab dem letzten Eintrag gilt der aktuelle Abschlag. Einträge, die noch nicht erreicht sind, zählen nicht.
- **Pauschalverträge:** Jede Abbuchung zählt mit dem Betrag, der an ihrem Tag galt.
- Es verändert sich **Gezahlt bisher** und damit **Guthaben/Nachzahlung (Bisher)**, die Prognose **Guthaben/Nachzahlung (Vertragsende)** und **Abschlag (Anpassung empfohlen)**. **Kosten (Bisher)** hängen nicht vom Abschlag ab.
- Der Verlauf **ersetzt** die einzelne Änderung mit Datum und altem Wert.
- Der Rechenweg steht in [Abschlaege-und-Kosten](Abschlaege-und-Kosten).

## Frühere Laufzeiten

Auch beim Eintragen eines alten Vertrags im Tab **Historie** (Button **Alten Vertrag hinzufügen**) gibt es diese Eingabe. Im Dialog steht unter den Feldern der aufklappbare Bereich **Abschläge nach Zahlungen (freiwillig)** mit demselben Raster, im Screenshot nicht zu sehen. Aus den Zahlungen berechnet Tariffy das grau hinterlegte Feld **Gezahlte Abschläge (€)** und den **Saldo (€)**. Bleibt der Bereich leer, gilt der einzelne **Abschlag pro Monat**.

![Dialog Alten Vertrag hinzufügen mit Vertrag Strom Haus, Laufzeit 2024 und den grau hinterlegten berechneten Feldern Kosten, Gezahlte Abschläge und Saldo](https://raw.githubusercontent.com/wiki/weskona/tariffy/images/term-dialog.png)

*Abbildung: Der Dialog Alten Vertrag hinzufügen. Die grauen Felder zeigen den berechneten Wert mit dem Hinweis Berechnet. Beispieldaten.*

Mehr zur Historie steht in [Archiv-und-Historie](Archiv-und-Historie) und [Panel-Historie](Panel-Historie).

## Einmalposten

Ein **Einmalposten** ist ein Betrag, der nicht zum monatlichen Abschlag gehört: ein **Wechselbonus** oder **Neukundenbonus** (positiv) oder zum Beispiel das **Honorar für einen Makler** (negativ).

1. Öffne im Tab **Verträge** die Details des Vertrags.
2. Im Block **Einmalposten** klickst Du auf **Posten hinzufügen**.
3. Im Dialog **Einmalposten hinzufügen** füllst Du aus:
   - **Bezeichnung** (höchstens 100 Zeichen),
   - **Betrag (+ Gutschrift, − Rechnung)**: positiv für eine Gutschrift, negativ für eine Rechnung, nicht null,
   - **Datum** (freiwillig).
4. Klicke auf **Speichern**.

Mit dem Stift in der Zeile (**Posten bearbeiten**) änderst Du einen Posten, im Dialog gibt es dazu **Posten löschen** mit der Rückfrage **Diesen Posten löschen?** und **Ja, löschen**. Pro Vertrag sind bis zu 50 Posten möglich.

![Dialog Einmalposten hinzufügen mit der Bezeichnung Gebühr und dem Betrag minus 12,5](https://raw.githubusercontent.com/wiki/weskona/tariffy/images/once-dialog.png)

*Abbildung: Der Dialog Einmalposten hinzufügen, hier mit einer Rechnung (negativer Betrag). Beispieldaten.*

Das **Datum** entscheidet, ab wann ein Posten zählt:

- **Mit Datum in der Vergangenheit oder heute:** Er zählt sofort.
- **Mit Datum in der Zukunft:** Er zählt erst ab diesem Tag.
- **Ohne Datum:** Er zählt sofort und gehört zur laufenden Laufzeit.
- Ein Posten mit Datum vor dem Vertragsbeginn gehört nicht mehr zur laufenden Laufzeit, zählt aber in den **Kosten gesamt**.

Was ein Einmalposten verändert:

| Wert | Wirkung |
|---|---|
| **Guthaben/Nachzahlung (Bisher)** (Saldo heute) | plus die Summe der Posten der laufenden Laufzeit |
| **Kosten gesamt** (im Panel) | minus die Summe aller Posten: ein Bonus senkt, eine Rechnung erhöht die Gesamtkosten |
| **Kosten (Bisher)** | unverändert |
| **Guthaben/Nachzahlung (Vertragsende)** und Abschlag-Warnung | unverändert: Sie bleiben reine Verbrauchsrechnung |

Einmalposten gehören zum **Vertrag**, nicht zu einer Laufzeit. Bei einem Tarifwechsel bleiben sie erhalten. Bei mehr als einem Posten zeigt der Block eine Zeile **Saldo** mit der Summe. Ein Streaming-Vertrag zeigt den Block erst, wenn er schon Posten hat.

## Beispiel

Der Vertrag Strom Haus aus den Beispieldaten des Panels (Stichtag 12.07.2026) hat zwei Einmalposten.

<table align="center"><tr><td align="center" width="50%"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/desktop-contracts.png" alt="Tab Verträge mit dem Vertrag Strom Haus: im Block Einmalposten stehen Wechselbonus plus 80 Euro und Honorar Makler minus 25 Euro, Saldo plus 55 Euro (dunkles Design)" width="100%"><br><sub>Dunkel</sub></td><td align="center" width="50%"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/desktop-contracts-light.png" alt="Tab Verträge mit dem Vertrag Strom Haus: im Block Einmalposten stehen Wechselbonus plus 80 Euro und Honorar Makler minus 25 Euro, Saldo plus 55 Euro (helles Design)" width="100%"><br><sub>Hell</sub></td></tr></table>

*Abbildung: Tab Verträge mit den Details von Strom Haus. Im Block Einmalposten stehen die beiden Posten und ihr Saldo.*

| Posten | Datum | Betrag |
|---|---|---|
| Wechselbonus | 15.01.2026 | +80,00 € |
| Honorar Makler | 20.01.2026 | −25,00 € |
| **Saldo** | | **+55,00 €** |

```
Gezahlt bisher                            =  252,30 €
Kosten (Bisher)                           =  513,54 €     (unverändert)
Saldo ohne Posten                         = 252,30 € − 513,54 € = −261,24 €
Guthaben/Nachzahlung (Bisher)             = −261,24 € + 55,00 €  = −206,24 €
Kosten gesamt                             = 1.042,50 € + 1.166,20 € + 513,54 € − 55,00 € = 2.667,24 €
Guthaben/Nachzahlung (Vertragsende)       = −495,29 €     (unverändert)
```

Für den Abschlagsverlauf stammt das Beispiel aus den Tests von Tariffy: Ein Gasvertrag läuft seit 01.01.2026, heute ist der 18.11.2026 (321 Tage). Der Abschlag war von Januar bis Juli **178 €**, im August **174,41 €**, seit September **215 €** (der aktuelle). Im Dialog stehen also drei Änderungen: **178** im Januar, **174,41** im August, **215** im September.

```
Gezahlt bisher mit Verlauf = 178 € × 6,96 Monate + 174,41 € × 1,02 Monate + 215 € × 2,56 Monate ≈ 1.968,20 €
Gezahlt bisher ohne Verlauf = 215 € × 321 ÷ 30,44                                              ≈ 2.267,25 €
```

Ohne Verlauf würde Tariffy rund 299 € mehr gezahlt annehmen, als Du wirklich gezahlt hast. Mit dem Verlauf fallen **Guthaben/Nachzahlung (Bisher)** und die Prognose **Guthaben/Nachzahlung (Vertragsende)** entsprechend niedriger aus, und die Empfehlung **Abschlag (Anpassung empfohlen)** steigt.

## Siehe auch

- [Abschlaege-und-Kosten](Abschlaege-und-Kosten): wie Kosten, Saldo und Prognose entstehen
- [Panel-Vertraege](Panel-Vertraege): der Tab Verträge im Panel
- [Panel-Historie](Panel-Historie): frühere Laufzeiten und alte Verträge von Hand eintragen
- [Archiv-und-Historie](Archiv-und-Historie)
- [Sensoren-Referenz](Sensoren-Referenz)
