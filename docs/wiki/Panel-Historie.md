🇩🇪 Deutsch · [🇬🇧 English](EN-Panel-History)

# Panel: Historie

Der Tab **Historie** zeigt, was früher war: die **früheren Laufzeiten** jedes Vertrags und die **archivierten Verträge**. Hier trägst Du als Administrator auch einen alten Vertrag von Hand nach. Ansehen dürfen den Tab alle Benutzer.

**Inhalt:**
- [Was der Tab zeigt](#was-der-tab-zeigt)
- [Frühere Laufzeiten](#frühere-laufzeiten)
- [Archivierte Verträge](#archivierte-verträge)
- [Alten Vertrag hinzufügen](#alten-vertrag-hinzufügen)
- [Kosten gesamt](#kosten-gesamt)
- [Beispiel: Strom Haus](#beispiel-strom-haus)
- [Wenn die Historie leer ist](#wenn-die-historie-leer-ist)
- [Auf dem Handy](#auf-dem-handy)
- [Siehe auch](#siehe-auch)

## Was der Tab zeigt

Oben rechts steht für Administratoren der Button **Alten Vertrag hinzufügen**. Darunter stehen zwei Gruppen: **Archivierte Verträge** und **Frühere Laufzeiten**. Jede Gruppe hat pro Vertrag eine Tabelle mit den Spalten **Laufzeit** (mit Anbieter und Tarif darunter), **Abschlag**, **Kosten**, **Verbrauch** und **Saldo**. Administratoren sehen am Zeilenende einen Stift zum Bearbeiten.

<table align="center"><tr><td align="center" width="50%"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/desktop-history.png" alt="Tab Historie: oben rechts der Button Alten Vertrag hinzufügen, darunter der archivierte Vertrag Strom Altvertrag mit zwei Laufzeiten und der Button Zurückholen, dann die früheren Laufzeiten von Strom Haus (dunkles Design)" width="100%"><br><sub>Dunkel</sub></td><td align="center" width="50%"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/desktop-history-light.png" alt="Tab Historie: oben rechts der Button Alten Vertrag hinzufügen, darunter der archivierte Vertrag Strom Altvertrag mit zwei Laufzeiten und der Button Zurückholen, dann die früheren Laufzeiten von Strom Haus (helles Design)" width="100%"><br><sub>Hell</sub></td></tr></table>

*Abbildung: Der Tab Historie (Beispieldaten vom 12.07.2026).*

## Frühere Laufzeiten

Wenn der Folgevertrag am geplanten Datum übernimmt, überschreibt Tariffy die Vertragsdaten. Die alte Laufzeit wird vorher als Eintrag gesichert, mit Zeitraum, Anbieter, Tarif, Preisen, Abschlag, den Kosten, dem Verbrauch und dem Saldo zum Ende, und steht dann hier unter dem Vertrag. Auch **Vertrag verlängern** bei Pauschalverträgen legt pro Verlängerung einen Eintrag an (Zeitraum, Anbieter, Tarif, Abschlag, gezahlte Abschläge), so siehst Du, wie der Beitrag steigt.

- Für Laufzeiten, die schon vorbei sind, gibt es keine Einträge; die Historie beginnt mit dem ersten Wechsel nach dem Update.
- Es werden höchstens 50 Laufzeiten je Vertrag gespeichert.
- Kunden- und Zählernummern stehen nicht darin.
- Die Farbe beim **Saldo** zeigt die Richtung: grün ist Guthaben (+37,50 €), rot ist Nachzahlung (−146,20 €).

## Archivierte Verträge

Ein Vertrag, dessen Ende vorbei ist und für den kein Folgevertrag geplant ist, bekommt in der Übersicht das Badge **Abgelaufen**. Im Tab [Panel-Vertraege](Panel-Vertraege) archivierst Du ihn mit dem Button **Archivieren** (Administratoren, mit Rückfrage). Danach steht er hier unter **Archivierte Verträge** mit dem Badge **Archiviert**; seine letzte Laufzeit steht schon in der Tabelle und wird nicht doppelt gezählt.

- Aus Übersicht, Kosten, Verträgen und den Summen verschwindet er; seine Erinnerungen und Warnungen sind aus.
- Es wird nichts gelöscht: Die Sensoren und ihre Statistik bleiben.
- Mit **Zurückholen** (Administratoren, mit Rückfrage „Diesen Vertrag wieder in die Übersicht holen?" und **Ja, zurückholen**) ist der Vertrag wieder in der Übersicht.
- Nichts wird von allein archiviert. Sind alle Verträge archiviert, steht in der Übersicht: „Alle Verträge sind archiviert. Du findest sie im Tab Historie."

Hintergründe in [Archiv-und-Historie](Archiv-und-Historie).

## Alten Vertrag hinzufügen

Mit dem Button **Alten Vertrag hinzufügen** (nur Administratoren) legst Du eine frühere Laufzeit an, zum Beispiel einen Vertrag von vor zwei Jahren. Der Stift in der Zeile bearbeitet sie; dort lässt sie sich auch löschen („Diese Laufzeit aus der Historie löschen?" mit **Ja, löschen**).

Du wählst den **Vertrag**, zu dem die Laufzeit gehört (Zähler und Sparte kommen von ihm), und trägst **Beginn** und **Ende** ein, dazu nach Wunsch **Anbieter**, **Tarif**, **Arbeitspreis je Einheit (€)**, **Grundpreis pro Monat (€)** und **Abschlag pro Monat (€)**. **Verbrauch, Kosten, gezahlte Abschläge und Saldo werden automatisch ermittelt**, soweit es geht:

| Wert | Woher er kommt |
|---|---|
| **Verbrauch** | Aus den Langzeitstatistiken des Zählers in Home Assistant, zwischen Beginn und Ende. Gibt es für den Zeitraum keine Statistik, trägst Du ihn selbst ein. |
| **Kosten (€)** | Aus Verbrauch, Arbeitspreis und Grundpreis (Gas mit Brennwert und Zustandszahl des Vertrags). Bei Pauschalverträgen sind die Kosten die gezahlten Abschläge. |
| **Gezahlte Abschläge (€)** | Aus Abschlag und Dauer. |
| **Saldo (€)** | Aus gezahlten Abschlägen und Kosten. |

Die grau hinterlegten Felder zeigen den berechneten Wert und woher er kommt („Automatisch aus den Statistiken von ...", „Berechnet", „Von dir eingetragen", „Keine Statistik für diese Laufzeit, bitte eintragen"). **In jedes Feld kannst Du selbst einen Wert eintragen**, er hat dann Vorrang und der Rest richtet sich danach. Beim Bearbeiten werden die Werte, die Du nicht selbst eingetragen hast, neu berechnet. Der Dialog speichert nichts, bis Du auf **Speichern** klickst.

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/term-dialog.png" alt="Dialog Alten Vertrag hinzufügen für Strom Haus: Beginn 01.01.2024, Ende 31.12.2024, Arbeitspreis 0,30, Grundpreis 10, Abschlag 90, Verbrauch 3000 von Hand eingetragen, Kosten 1.019,90, Gezahlte Abschläge 1.079,10 und Saldo 59,20 als berechnete graue Felder" width="520"></p>

*Abbildung: Der Dialog „Alten Vertrag hinzufügen". Der Verbrauch (3000) ist von Hand eingetragen, Kosten, gezahlte Abschläge und Saldo sind berechnet.*

- Hatte der alte Vertrag einen anderen Tarifnamen oder andere Preise, trägst Du sie einfach ein.
- Staffelpreise, dynamische Preise und getrennte Preise für Hoch- und Niedertarif werden nicht berechnet; dort trägst Du die Kosten selbst ein.
- Unter den Feldern gibt es den Bereich **Abschläge nach Zahlungen (freiwillig)** mit einem Feld je Zahlung der Laufzeit (aus Beginn, Ende und der Zahlweise des Vertrags). Trägst Du dort etwas ein, werden **Gezahlt** und der **Saldo** der Laufzeit daraus berechnet (bei Verbrauchsverträgen anteilig nach Tagen, bei Pauschalverträgen Zahlung für Zahlung); ein selbst eingetragener Wert bei „Gezahlte Abschläge" hat Vorrang. Die Beträge bleiben gespeichert und erscheinen beim Bearbeiten wieder. Bleibt der Bereich leer, rechnet die Laufzeit mit dem einzelnen Abschlag. Mehr in [Abschlagsverlauf-und-Einmalposten](Abschlagsverlauf-und-Einmalposten).
- Mögliche Meldungen: „Das Ende darf nicht vor dem Beginn liegen.", „Die Historie ist voll (50 Laufzeiten).", „Diese Laufzeit gibt es nicht mehr.", „Eine der Zahlen ist nicht gültig."

## Kosten gesamt

Hat ein Vertrag eine Historie (weil Du ihn verlängert hast, der Folgevertrag übernommen hat oder Du alte Laufzeiten eingetragen hast), zeigt Tariffy die **Kosten gesamt** über alle Laufzeiten: die früheren Laufzeiten plus die laufende. Im Tab Historie steht die Zeile unter der Tabelle, jeweils mit „seit <Datum> · n Laufzeiten"; dazu steht sie in der Übersicht und in den Vertragsdetails.

- Für eine frühere Laufzeit zählen ihre Kosten, wenn es sie gibt, sonst die gezahlten Abschläge.
- Fehlt bei einer Laufzeit beides, steht „mindestens ...", weil die Summe dann nicht vollständig ist.
- Bei einem archivierten Vertrag steht seine letzte Laufzeit schon in der Historie und wird nicht doppelt gezählt.
- Einmalposten (Bonus, Rechnung) fließen in die Kosten gesamt ein.
- Ohne Historie und ohne Einmalposten gibt es keine zusätzliche Anzeige.

## Beispiel: Strom Haus

In den Beispieldaten hat **Strom Haus** zwei frühere Laufzeiten. Die Tabelle zeigt:

| Laufzeit | Abschlag | Kosten | Verbrauch | Saldo |
|---|---|---|---|---|
| 01.01.2025 – 31.12.2025 | 85,00 € | 1.166,20 € | 3.340 kWh | −146,20 € |
| 01.01.2024 – 31.12.2024 | 90,00 € | 1.042,50 € | 3.210 kWh | +37,50 € |

Der Saldo ist gezahlte Abschläge minus Kosten: 12 × 85,00 € = 1.020,00 € gezahlt gegen 1.166,20 € Kosten ergibt −146,20 €; 12 × 90,00 € = 1.080,00 € gegen 1.042,50 € ergibt +37,50 €. Unter der Tabelle steht „Kosten gesamt 2.667,24 € · seit 01.01.2024 · 3 Laufzeiten". Das sind die beiden früheren Laufzeiten (1.166,20 € + 1.042,50 €) plus die laufende (513,54 €), abzüglich der Einmalposten dieses Vertrags (netto +55,00 €, also eine Gutschrift): 2.208,70 € + 513,54 € − 55,00 € = 2.667,24 €.

Der archivierte Vertrag **Strom Altvertrag** (Stadtwerke Süd) hat ebenso zwei Laufzeiten, zusammen 1.725,40 € („seit 01.01.2022 · 2 Laufzeiten"), und den Button **Zurückholen**.

## Wenn die Historie leer ist

Wer noch keinen Folgevertrag hatte und keinen Vertrag archiviert hat, sieht „Noch keine Historie" mit dem Text „Die früheren Laufzeiten eines Vertrags erscheinen hier, sobald der Folgevertrag übernimmt. Archivierte Verträge erscheinen hier ebenfalls." Administratoren können trotzdem mit **Alten Vertrag hinzufügen** Laufzeiten nachtragen.

## Auf dem Handy

Auf dem Handy stehen die Zeilen der Tabellen als Karten untereinander, die Buttons bleiben am Platz.

<table align="center"><tr><td align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-history.png" alt="Tab Historie auf dem Handy: archivierter Vertrag und frühere Laufzeiten untereinander (dunkles Design)" width="300"><br><sub>Dunkel</sub></td><td align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-history-light.png" alt="Tab Historie auf dem Handy: archivierter Vertrag und frühere Laufzeiten untereinander (helles Design)" width="300"><br><sub>Hell</sub></td></tr></table>

*Abbildung: Der Tab Historie auf dem Handy.*

## Siehe auch

- [Panel-Vertraege](Panel-Vertraege): Archivieren, Verlängern und Folgevertrag planen.
- [Archiv-und-Historie](Archiv-und-Historie): Archiv und Historie im Zusammenhang.
- [Folgevertrag-oder-Verlaengern](Folgevertrag-oder-Verlaengern): wann eine Laufzeit in die Historie kommt.
- [Abschlagsverlauf-und-Einmalposten](Abschlagsverlauf-und-Einmalposten): Abschläge nach Zahlungen und Einmalposten.
- [Panel-Sicherung](Panel-Sicherung): die Historie steckt auch in der Sicherung.
