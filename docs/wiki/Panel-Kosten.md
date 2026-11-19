🇩🇪 Deutsch · [🇬🇧 English](EN-Panel-Costs)

# Panel: Kosten

Der Tab **Kosten** zeigt oben, wie sich Deine Kosten auf Sparten und Verträge verteilen, und darunter je eine Tabelle für Verbrauchs- und Pauschalverträge mit Summen. Er ist nur zum Ansehen: Bearbeiten kannst Du im Tab [Panel-Vertraege](Panel-Vertraege).

**Inhalt:**
- [Kostenaufteilung](#kostenaufteilung)
- [Die Tabellen](#die-tabellen)
- [Kredite](#kredite)
- [Beispiel: Anteil von Gas](#beispiel-anteil-von-gas)
- [Auf dem Handy](#auf-dem-handy)
- [Siehe auch](#siehe-auch)

<table align="center"><tr><td align="center" width="50%"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/desktop-costs.png" alt="Tab Kosten: oben die Kostenaufteilung mit Ringdiagramm und Legende, darunter die Tabellen Verbrauchsverträge, Pauschalverträge und Kredite / Finanzierungen (dunkles Design)" width="100%"><br><sub>Dunkel</sub></td><td align="center" width="50%"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/desktop-costs-light.png" alt="Tab Kosten: oben die Kostenaufteilung mit Ringdiagramm und Legende, darunter die Tabellen Verbrauchsverträge, Pauschalverträge und Kredite / Finanzierungen (helles Design)" width="100%"><br><sub>Hell</sub></td></tr></table>

*Abbildung: Der Tab Kosten auf dem Desktop (Beispieldaten vom 12.07.2026).*

## Kostenaufteilung

Oben steht die **Kostenaufteilung**: ein **Ringdiagramm** mit der Gesamtsumme in der Mitte (2.791 €) und daneben eine Legende mit Betrag und Anteil je Eintrag. Darunter zeigt ein Balken die Aufteilung zwischen **Verbrauchsverträgen** (77,1 %) und **Pauschalverträgen** (22,9 %). Drei Umschalter steuern das Diagramm:

| Umschalter | Auswahl | Wirkung |
|---|---|---|
| Zeitraum | **Kosten bisher** / **Pro Jahr** | „Kosten bisher" zählt, was bis heute angefallen ist. „Pro Jahr" rechnet den Abschlag auf ein Jahr hoch (zum Beispiel Gas Heizung 140,00 € × 12 = 1.680,00 €). |
| **Jahr** | **Aktuell** oder ein Kalenderjahr | Zeigt die Kosten eines Kalenderjahres, für alle Jahre mit Daten, auch aus der Historie und von archivierten Verträgen. Eine Laufzeit über mehrere Jahre zählt anteilig nach Tagen in jedem Jahr. Dazu steht der Hinweis „Die Kosten dieses Kalenderjahres; frühere Laufzeiten zählen anteilig für ihre Tage darin." |
| Gruppierung | **Je Sparte** / **Je Vertrag** | „Je Sparte" zählt Verträge gleicher Sparte zusammen (zwei Internet-Verträge werden zu „Internet (2)"). „Je Vertrag" zeigt jeden einzeln. |

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/cost-chart-sparte.png" alt="Kostenaufteilung je Sparte für Kosten bisher: Gas, Internet (2), Strom, Strom HT/NT, Mobilfunk und Wasser mit Betrag und Prozent" width="100%"></p>

*Abbildung: „Je Sparte" und „Kosten bisher": Verträge der gleichen Sparte werden zusammengezählt, hier Internet (2). Andere Beispieldaten mit einem zweiten Internet-Vertrag.*

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/cost-chart.png" alt="Kostenaufteilung je Vertrag für Pro Jahr: Gas Heizung 1.680 Euro, Strom Wohnung 660 Euro, Strom Haus 480 Euro und weitere Verträge" width="100%"></p>

*Abbildung: „Je Vertrag" und „Pro Jahr": jeder Vertrag einzeln, hochgerechnet auf ein Jahr.*

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/cost-chart-year.png" alt="Kostenaufteilung je Vertrag für das Jahr 2025 mit dem Hinweis, dass frühere Laufzeiten anteilig für ihre Tage zählen" width="100%"></p>

*Abbildung: Die Jahresauswahl zeigt die Kosten eines Kalenderjahres, hier 2025, auch von früheren Laufzeiten und dem archivierten Vertrag Strom Altvertrag.*

Sind noch keine Werte da, steht „Noch nichts darzustellen."

## Die Tabellen

Unter dem Diagramm stehen zwei Tabellen wie in der Übersicht. Beide haben dasselbe Spaltenraster, „Kosten bisher" und „Abschlag" stehen also genau untereinander.

**Verbrauchsverträge:**

| Spalte | Bedeutung |
|---|---|
| **Vertrag** | Name und Anbieter. |
| **Kosten bisher** | Die Kosten bis heute, aus dem gemessenen Verbrauch. |
| **Saldo heute** | Guthaben (plus) oder Nachzahlung (minus) bis heute. |
| **Zum Vertragsende** | Die Prognose zum Vertragsende, aus dem bisherigen Verbrauch hochgerechnet. |
| **Abschlag** | Der aktuelle Abschlag pro Monat. |
| **Empfohlen** | Der empfohlene Abschlag. Deckt ein Guthaben die Kosten schon ab, steht „0,00 €" mit „Guthaben deckt die Kosten". |

Bei einem Zweitarifzähler (Strom HT/NT) stehen unter dem Vertrag zwei Zeilen, **Hochtarif** und **Niedertarif**, mit Verbrauch und Kosten (900 kWh = 288,00 € und 600 kWh = 126,00 €).

**Pauschalverträge:** **Kosten bisher** (die bis heute gebuchten Raten), **Restlaufzeit**, **Vertragsende** und **Abschlag** (mit dem Jahreswert darunter, zum Beispiel „480 € / Jahr"). Saldo und Prognose gibt es dort nicht.

Jede Tabelle hat eine Zeile **Summe**, darunter steht die Zeile **Gesamt** mit der Gesamtsumme. Unter den Tabellen erinnert ein Hinweis an die Vorzeichen: „Positiv = Guthaben, negativ = Nachzahlung. „Zum Vertragsende" ist aus dem bisherigen Verbrauch hochgerechnet. Bei Pauschalverträgen sind die Kosten bisher die bis heute fälligen Abschläge."

> **Gut zu wissen:** Wie die Kosten bei Pauschalverträgen mit Zahlung im Voraus (vierteljährlich, halbjährlich, jährlich) gezählt werden, steht in [Abschlaege-und-Kosten](Abschlaege-und-Kosten). Einmalposten fließen in die Kosten gesamt ein, nicht in die Prognose ([Abschlagsverlauf-und-Einmalposten](Abschlagsverlauf-und-Einmalposten)).

## Kredite

Kredite stehen in einer **eigenen Tabelle** „Kredite / Finanzierungen" mit den Spalten **Gezahlt bisher**, **Restschuld**, **Restsumme**, **Abschlag** und **Zinsen über die Laufzeit**. Der Hinweis darunter sagt: „Kredite laufen getrennt: Sie zählen nicht in die Summen der Verträge." Mehr zum Kredit in [Vertrag-Kredit](Vertrag-Kredit).

## Beispiel: Anteil von Gas

In den Beispieldaten ist die Summe der **Kosten bisher** 2.791,24 € (Verbrauchsverträge 2.151,46 € plus Pauschalverträge 639,78 €). Der Gasvertrag **Gas Heizung** hat 991,76 € Kosten bisher:

1. Du öffnest den Tab **Kosten**.
2. Du lässt **Kosten bisher** und **Je Sparte** gewählt.
3. In der Legende steht „Gas 991,76 € 35,5 %". Das ist 991,76 € ÷ 2.791,24 € = 35,5 %.

Mit **Je Vertrag** und **Pro Jahr** siehst Du dagegen den Abschlag auf ein Jahr gerechnet: Gas Heizung kostet bei 140,00 € im Monat 1.680,00 € im Jahr.

## Auf dem Handy

Auf schmalen Bildschirmen steht die Legende unter dem Ring, und jeder Vertrag der Tabellen wird zu einer Karte mit einer Zeile je Spalte (Kosten bisher, Saldo heute, Zum Vertragsende, Abschlag, Empfohlen). Die Summen stehen als eigene Karten darunter.

<table align="center"><tr><td align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-costs.png" alt="Tab Kosten auf dem Handy: Kostenaufteilung und Tabellen untereinander (dunkles Design)" width="300"><br><sub>Dunkel</sub></td><td align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-costs-light.png" alt="Tab Kosten auf dem Handy: Kostenaufteilung und Tabellen untereinander (helles Design)" width="300"><br><sub>Hell</sub></td></tr></table>

*Abbildung: Der Tab Kosten auf dem Handy.*

## Siehe auch

- [Panel-Uebersicht](Panel-Uebersicht): die Kacheln und Karten.
- [Panel-Vertraege](Panel-Vertraege): Details und Aktionen.
- [Abschlaege-und-Kosten](Abschlaege-und-Kosten): wie die Kosten gezählt werden.
- [Sensoren-Referenz](Sensoren-Referenz): dieselben Werte als Sensoren.
