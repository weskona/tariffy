🇩🇪 Deutsch · [🇬🇧 English](EN-Panel-Overview)

# Panel: Übersicht

Das **Tariffy-Panel** ist eine eigene Seite in der Seitenleiste von Home Assistant. Diese Seite erklärt, wie das Panel aufgebaut ist und was der Tab **Übersicht** zeigt: vier Kacheln mit den Summen und darunter eine Karte pro Vertrag. Sie ist für alle gedacht, die das Panel zum ersten Mal öffnen.

**Inhalt:**
- [Panel öffnen](#panel-öffnen)
- [Die fünf Tabs](#die-fünf-tabs)
- [Die vier Kacheln oben](#die-vier-kacheln-oben)
- [Die Vertragskarten](#die-vertragskarten)
- [Vorzeichen und Farben](#vorzeichen-und-farben)
- [Beispiel: die Karte Strom Haus](#beispiel-die-karte-strom-haus)
- [Auf dem Handy](#auf-dem-handy)
- [Wenn etwas nicht stimmt](#wenn-etwas-nicht-stimmt)
- [Siehe auch](#siehe-auch)

## Panel öffnen

In der Seitenleiste erscheint der Eintrag **Tariffy** (Symbol `mdi:cash-multiple`), sobald mindestens ein Vertrag geladen ist. Es gibt nichts zu installieren oder einzurichten: Das Panel gehört seit Version `1.27.0` zur Integration. Wer den Eintrag nicht in der Seitenleiste möchte, kann ihn im eigenen Profil ausblenden.

Nach einem Update startest Du Home Assistant neu und lädst die Browserseite einmal **hart neu** (Strg+F5, am Handy: Seite neu laden oder den App-Cache leeren). Sonst zeigt der Browser noch die alte Panel-Datei.

Das Panel folgt der **Sprache** von Home Assistant (Deutsch, sonst Englisch) und dem **Design** (hell oder dunkel, siehe [Panel-Rechte-und-Design](Panel-Rechte-und-Design)). Das Panel merkt sich im Browser, welchen Tab Du zuletzt geöffnet hattest.

Alle Beispiele auf den Seiten zum Panel stammen aus Beispieldaten mit dem Stichtag 12.07.2026. Die Zahlen in Deinem Panel sehen anders aus.

## Die fünf Tabs

Oben in der Mitte steht die Tab-Leiste. Der Tab **Sicherung** erscheint nur für Administratoren.

| Tab | Wofür | Seite |
|---|---|---|
| **Übersicht** | Vier Kacheln mit den Summen, darunter eine Karte pro Vertrag. Nur zum Ansehen, ohne Bearbeiten-Aktionen. | diese Seite |
| **Kosten** | Kostenaufteilung als Ringdiagramm und je eine Tabelle für Verbrauchs- und Pauschalverträge. | [Panel-Kosten](Panel-Kosten) |
| **Verträge** | Aufklappbare Details pro Vertrag und alle Aktionen, die einen Vertrag ändern. | [Panel-Vertraege](Panel-Vertraege) |
| **Historie** | Frühere Laufzeiten und archivierte Verträge. | [Panel-Historie](Panel-Historie) |
| **Sicherung** | Sicherung herunterladen, aus Datei wiederherstellen, gelöschte Verträge zurückholen (nur Administratoren). | [Panel-Sicherung](Panel-Sicherung) |

<table align="center"><tr><td align="center" width="50%"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/desktop-overview.png" alt="Tab Übersicht auf dem Desktop: oben die Tab-Leiste mit Übersicht, Kosten, Verträge, Historie und Sicherung, darunter vier Kacheln, dann die Gruppen Verbrauchsverträge, Pauschalverträge und Kredite / Finanzierungen mit je einer Karte pro Vertrag (dunkles Design)" width="100%"><br><sub>Dunkel</sub></td><td align="center" width="50%"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/desktop-overview-light.png" alt="Tab Übersicht auf dem Desktop: oben die Tab-Leiste mit Übersicht, Kosten, Verträge, Historie und Sicherung, darunter vier Kacheln, dann die Gruppen Verbrauchsverträge, Pauschalverträge und Kredite / Finanzierungen mit je einer Karte pro Vertrag (helles Design)" width="100%"><br><sub>Hell</sub></td></tr></table>

*Abbildung: Der Tab Übersicht auf dem Desktop (Beispieldaten vom 12.07.2026).*

## Die vier Kacheln oben

Die Kacheln fassen alle Verträge zusammen. Kredite zählen nicht mit (siehe unten).

| Kachel | Das steht darin |
|---|---|
| **Abschläge pro Monat** | Die Summe aller monatlichen Abschläge (im Beispiel 322,98 €), darunter der Jahreswert („≈ 3.876 € / Jahr") und ein Balken, der **Verbrauch** und **Pauschal** aufteilt (263,00 € und 59,98 €). |
| **Kosten bisher** | Die Kosten aller Verträge bis heute (2.791,24 €), dazu „Fällige Abschläge bisher" (2.859 €) und der **Saldo heute** (+67,50 €). |
| **Prognose zum Vertragsende** | Die Summe der Prognosen (−378 €) und je Vertrag die Prognose, die schlechteste zuerst. Es zählen nur Verträge mit Verbrauchsmessung; die Zeile darunter sagt es („4 von 6 Verträgen mit Verbrauchsmessung"). |
| **Nächste Termine** | Der nächste Termin groß (31.08.2026, Vertragsende von Gas Heizung, „in 50 Tagen"), darunter die weiteren: Kündigungsfrist („Jetzt kündigen"), Wechsel und Vertragsende. Ohne Termine steht „Nichts geplant". |

> **Gut zu wissen:** Alle Werte sind dieselben wie bei den Sensoren (siehe [Sensoren-Referenz](Sensoren-Referenz)) und aktualisieren sich von selbst. Das Panel rechnet nichts selbst.

## Die Vertragskarten

Unter den Kacheln stehen die Verträge in Gruppen, je eine Karte pro Vertrag:

- **Verbrauchsverträge** (Strom, Gas, Wasser),
- **Pauschalverträge** (Internet, Mobilfunk, Versicherung, Streaming, Sonstiges),
- **Hauskosten** (Abfallgebühren, Straßenreinigung und Ähnliches; sie zählen in den Summen mit),
- **Kredite / Finanzierungen** (getrennt von den anderen, ihre Beträge zählen nicht in die Summen der Verträge).

Die Karten sind nach dem Zustand getönt: grün bei Guthaben, rot bei Nachzahlung, orange wenn die Kündigung fällig ist. Oben rechts auf der Karte steht eine Kennzeichnung (Badge), zum Beispiel **Guthaben**, **Nachzahlung**, **Nachzahlung droht** (die Prognose liegt unter der Warnschwelle), **Jetzt kündigen**, **Wechsel am 01.01.2027** (ein Folgevertrag ist geplant) oder **Abgelaufen** (das Vertragsende ist vorbei, siehe [Panel-Historie](Panel-Historie)).

**Verbrauchskarte** (Strom, Gas, Wasser):

- Die **Prognose zum Vertragsende** als große Zahl, daneben der **Laufzeit-Ring** (Prozent der Laufzeit, die schon vorbei sind).
- Darunter der Abschlag pro Monat und der Hinweis zum Abschlag: „Abschlag auf 127,66 € pro Monat erhöhen", „Abschlag könnte auf 25,33 € pro Monat sinken" oder „Kein Abschlag nötig: Das Guthaben deckt die Kosten bis Vertragsende".
- Höchstens drei Zahlen: **Kosten bisher**, **Saldo heute** und **Verbrauch** (mit der Hochrechnung auf die Laufzeit).
- Zwei Balken: **Abschläge gezahlt** gegen **Kosten**.
- Die **Restlaufzeit** und, wenn der Vertrag eine Historie hat, **Kosten gesamt** über alle Laufzeiten („seit 01.01.2024 · 3 Laufzeiten").
- Ein Hinweiskasten, zum Beispiel zur Nachzahlung oder zur laufenden Kündigungsfrist. Zeigen **Saldo heute** und Prognose in verschiedene Richtungen (heute im Rückstand, am Ende Guthaben oder umgekehrt), steht darunter, warum.

**Pauschalkarte** (Internet, Mobilfunk, ...): der **Abschlag pro Monat** groß, darunter der Jahreswert und der Betrag über die Laufzeit, dazu die Kacheln **Kosten bisher** und **Vertragsende**, ein **Laufzeit-Balken**, die Restlaufzeit und die **Erinnerung**. Es gibt keinen Ring, keinen Verbrauch und keinen Saldo. Hat der Vertrag eine Historie, kommt eine Kachel **Kosten gesamt** dazu.

**Kreditkarte:** die **Restschuld** groß, darunter Monatsrate, Sollzins und effektiver Zins, die Kacheln **Gezahlt bisher**, **Restsumme** und **Nächste Rate**, ein Balken **Getilgt**, Restlaufzeit, gezahlte Raten und die Aufteilung der nächsten Rate in Zinsen und Tilgung. Mehr dazu in [Vertrag-Kredit](Vertrag-Kredit).

> **Gut zu wissen:** Bei Pauschalverträgen sind die **Kosten bisher** die bis heute gebuchten Raten, nicht ein Tagesanteil. Wie Tariffy sie zählt, steht in [Abschlaege-und-Kosten](Abschlaege-und-Kosten). Eine Zeile **Kosten gesamt** erscheint nur, wenn es eine Historie oder Einmalposten gibt ([Abschlagsverlauf-und-Einmalposten](Abschlagsverlauf-und-Einmalposten)).

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/wide-overview.png" alt="Übersicht auf einem breiten Bildschirm: die vier Kacheln nebeneinander, darunter vier Verbrauchskarten in einer Reihe" width="100%"></p>

*Abbildung: Auf einem breiten Bildschirm stehen mehr Karten nebeneinander.*

## Vorzeichen und Farben

- **Plus** ist Guthaben, **Minus** ist Nachzahlung.
- „Zum Vertragsende" ist aus dem bisherigen Verbrauch hochgerechnet.
- Deckt ein Guthaben die Kosten bis zum Vertragsende schon ab, steht beim empfohlenen Abschlag „0,00 €" mit dem Hinweis „Guthaben deckt die Kosten", nie ein negativer Betrag.

Grün steht für Guthaben, Rot für Nachzahlung, Orange für eine fällige Kündigung und Blau für einen geplanten Wechsel.

## Beispiel: die Karte Strom Haus

In den Beispieldaten hat der Vertrag **Strom Haus** (Stadtwerke Nord, Tarif Öko Fix 12, Abschlag 40,00 € im Monat) diese Werte:

| Anzeige | Wert | Bedeutung |
|---|---|---|
| Prognose zum Vertragsende | −495 € | Bis 31.12.2026 wird eine Nachzahlung von etwa 495 € erwartet. |
| Saldo heute | −206,24 € | Heute liegen die Kosten (513,54 €) um diesen Betrag über den gezahlten Abschlägen. |
| Abschläge gezahlt | 307 € | 252,30 € Abschläge plus 55,00 € aus den Einmalposten (Wechselbonus +80,00 €, Honorar Makler −25,00 €). |
| Hinweis zum Abschlag | „Abschlag auf 127,66 € pro Monat erhöhen" | Mit diesem Abschlag wäre die Prognose bis zum Vertragsende ausgeglichen. |
| Laufzeit-Ring | 53 % | 172 Tage Restlaufzeit bis 31.12.2026. |

Die Karte ist rot getönt und trägt das Badge **Nachzahlung droht**. Zur Gegenprobe: Der **Saldo heute** ist 252,30 € + 55,00 € − 513,54 € = −206,24 €. Daneben steht **Gas Heizung** mit **Guthaben** (+524 € zum Vertragsende): Dort steht beim Hinweis „Kein Abschlag nötig: Das Guthaben deckt die Kosten bis Vertragsende".

Die Übersicht hat keine Buttons. Wie Du den Abschlag änderst oder die Warnung bestätigst, steht in [Panel-Vertraege](Panel-Vertraege).

## Auf dem Handy

Ist das Panel schmal (bis etwa 760 Pixel Breite), stehen die Kacheln untereinander und jede Karte ist eine **aufklappbare Zeile**: Name, Anbieter und Tarif, die Prognose als Zahl und das Badge. Mit dem Pfeil rechts klappst Du die Karte auf und siehst dieselben Angaben wie auf dem Desktop. Oben links erscheint in der Home-Assistant-App der Menü-Knopf.

<table align="center"><tr><td align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-overview.png" alt="Übersicht auf dem Handy: vier Kacheln untereinander, darunter die Verträge als zugeklappte Zeilen mit Prognose und Badge (dunkles Design)" width="300"><br><sub>Dunkel</sub></td><td align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-overview-light.png" alt="Übersicht auf dem Handy: vier Kacheln untereinander, darunter die Verträge als zugeklappte Zeilen mit Prognose und Badge (helles Design)" width="300"><br><sub>Hell</sub></td></tr></table>

*Abbildung: Die Übersicht auf dem Handy, alle Karten zugeklappt.*

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-overview-open.png" alt="Übersicht auf dem Handy mit aufgeklappten Karten für Strom Haus, Strom Wohnung und Internet" width="300"></p>

*Abbildung: Mit dem Pfeil aufgeklappte Karten zeigen alle Angaben, nur untereinander.*

## Wenn etwas nicht stimmt

| Problem | Lösung |
|---|---|
| Kein Eintrag „Tariffy" in der Seitenleiste | Version in HACS prüfen (ab 1.27.0 gibt es das Panel), Home Assistant neu starten, Seite hart neu laden. Im Profil prüfen, ob der Eintrag ausgeblendet ist. Im Log nach Meldungen „Tariffy: panel" suchen: Das Panel kann ausfallen, ohne die Verträge zu stören. |
| Panel zeigt die alte Oberfläche oder es fehlen Buttons | Seite hart neu laden (Strg+F5), der Browser hat die alte Datei zwischengespeichert. |
| Seite schwarz oder leer | Seite hart neu laden. Hilft das nicht, Home Assistant neu starten und im Log nach „Tariffy: panel" suchen. Siehe auch [Panel-Rechte-und-Design](Panel-Rechte-und-Design) zu den Meldungen „Noch keine Verträge" und „Das Panel konnte die Verträge nicht laden." |
| Keine Buttons zu sehen | Die Aktionen gibt es nur für Administratoren. |

Weitere Hilfe: [Fehlerbehebung](Fehlerbehebung). Einen Fehler meldest Du mit dem [Fehlerformular](https://github.com/weskona/tariffy/issues/new/choose) und der genauen Version.

## Siehe auch

- [Panel-Kosten](Panel-Kosten): die Kostenaufteilung und die Tabellen.
- [Panel-Vertraege](Panel-Vertraege): Vertragsdetails und alle Aktionen.
- [Panel-Historie](Panel-Historie): frühere Laufzeiten und Archiv.
- [Panel-Sicherung](Panel-Sicherung): Sicherung und gelöschte Verträge.
- [Panel-Rechte-und-Design](Panel-Rechte-und-Design): Administratoren, helles und dunkles Design.
- [Sensoren-Referenz](Sensoren-Referenz): dieselben Werte als Sensoren.
