🇩🇪 Deutsch · [🇬🇧 English](EN-Panel-Contracts)

# Panel: Verträge

Der Tab **Verträge** ist die Arbeitsfläche des Panels: Hier klappst Du die Details jedes Vertrags auf, und hier stehen **alle Aktionen, die einen Vertrag ändern**: anlegen, bearbeiten, Folgevertrag planen, verlängern, archivieren, löschen. Ansehen dürfen den Tab alle Benutzer, ändern nur Administratoren.

**Inhalt:**
- [Die Vertragsliste](#die-vertragsliste)
- [Die Vertragsdetails](#die-vertragsdetails)
- [Schaltflächen](#schaltflächen)
- [Bestätigen: Warnung und Kündigung](#bestätigen-warnung-und-kündigung)
- [Neuer Vertrag](#neuer-vertrag)
- [Vertrag bearbeiten](#vertrag-bearbeiten)
- [Folgevertrag planen](#folgevertrag-planen)
- [Pauschalvertrag verlängern](#pauschalvertrag-verlängern)
- [Gezahlte Abschläge](#gezahlte-abschläge)
- [Einmalposten](#einmalposten)
- [Archivieren](#archivieren)
- [Vertrag löschen](#vertrag-löschen)
- [Beispiel: Einmalposten eintragen](#beispiel-einmalposten-eintragen)
- [Auf dem Handy](#auf-dem-handy)
- [Fehler und Hinweise](#fehler-und-hinweise)
- [Siehe auch](#siehe-auch)

## Die Vertragsliste

Die Verträge stehen in denselben Gruppen wie in der Übersicht: **Verbrauchsverträge**, **Pauschalverträge** und **Kredite / Finanzierungen**. Jede Zeile zeigt Symbol, Name, Anbieter und Tarif, die Kennzeichnung (zum Beispiel **Nachzahlung droht**, **Guthaben**, **Jetzt kündigen**, **Wechsel am 01.01.2027**) und rechts den Saldo zum Vertragsende (Verbrauch) oder den Betrag „39,99 € / Monat" (Pauschal). Ein Klick auf die Zeile klappt die Details auf (Pfeil ganz rechts).

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/list-1280.png" alt="Tab Verträge auf einem Bildschirm mit 1280 Pixel Breite: oben rechts der Button Neuer Vertrag, darunter die Verträge als zugeklappte Zeilen mit Kennzeichnung, Saldo und Symbolen" width="100%"></p>

*Abbildung: Der Tab Verträge mit zugeklappten Zeilen (Beispieldaten vom 12.07.2026).*

Als **Administrator** siehst Du in jeder Zeile Symbole vor dem Pfeil, von rechts nach links:

| Symbol | Name | Wo |
|---|---|---|
| Stift | Vertrag bearbeiten | jeder Vertrag |
| Kalender | Folgevertrag planen (oder Folgevertrag bearbeiten, wenn schon einer eingetragen ist) | jeder Vertrag außer Krediten |
| zwei Pfeile im Kreis | Vertrag verlängern (bei Krediten: Anschlussfinanzierung) | Pauschalverträge und Kredite, die sich verlängern lassen |

Oben rechts steht der Button **Neuer Vertrag**. Andere Benutzer sehen die Liste ohne Symbole und ohne diesen Button.

## Die Vertragsdetails

Aufgeklappt zeigt ein Verbrauchsvertrag mehrere Blöcke nebeneinander (auf schmalen Bildschirmen untereinander):

| Block | Inhalt |
|---|---|
| **Vertrag** | Anbieter, Tarif, Beginn, Ende, Restlaufzeit, Erinnerung ab; bei Bedarf Mindestlaufzeit, Kündigungsfrist und „Kündigen bis". **Nur Administratoren** sehen hier zusätzlich Kundennummer, Zählernummer(n) und Marktlokations-ID, jeweils mit einem Symbol zum Kopieren. |
| **Preise** | Arbeitspreis, Grundpreis, Abschlag pro Monat und pro Jahr, bei Verträgen mit Historie **Kosten gesamt** („seit 01.01.2024 · 3 Laufzeiten"). |
| **Einmalposten** | Gutschriften und Rechnungen, siehe [Einmalposten](#einmalposten). Für andere Benutzer nur sichtbar, wenn es Posten gibt. |
| **Verbrauch** | Bisher, hochgerechnet auf die Laufzeit, Kosten bisher, Guthaben/Nachzahlung bisher und zum Vertragsende. Mit Gesamtverbrauchs-Sensor kommen das Raster **Gesamtverbrauch**, **Durch PV gedeckt** und **Netzbezug (abgerechnet)** dazu, mit PV-Autarkie die Prognose ohne Autarkie ([PV-Autarkie](PV-Autarkie)). |
| **Empfehlungen** | Die **Abschlag-Anpassung** (empfohlener Abschlag) und, je nach Lage, die Buttons zum Bestätigen. |
| **Folgevertrag** | Erscheint, wenn ein Folgevertrag eingetragen ist: Beginn, Ende, Anbieter, Tarif, Preis, Abschlag. |
| **Gezahlte Abschläge** | Der Verlauf der wirklich gezahlten Beträge, siehe [Gezahlte Abschläge](#gezahlte-abschläge). Kredite haben ihn nicht. |

Bei Pauschalverträgen heißen die Blöcke ähnlich, es gibt keinen Verbrauch; bei Streaming heißt der Abschlag „Preis / Monat". Weitere Blöcke gibt es nur bei bestimmten Sparten: **Außenzähler** beim Wasser ([Vertrag-Wasser](Vertrag-Wasser)), **Leasing-Kilometer** beim Leasing ([Vertrag-Leasing](Vertrag-Leasing)) und **Kredit** mit allen Kreditwerten ([Vertrag-Kredit](Vertrag-Kredit)).

<table align="center"><tr><td align="center" width="50%"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/desktop-contracts.png" alt="Tab Verträge mit aufgeklappten Details für Strom Haus und Gas Heizung: Blöcke Vertrag, Preise, Einmalposten und Verbrauch, darunter Empfehlungen und der Button Warnung bestätigen (dunkles Design)" width="100%"><br><sub>Dunkel</sub></td><td align="center" width="50%"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/desktop-contracts-light.png" alt="Tab Verträge mit aufgeklappten Details für Strom Haus und Gas Heizung: Blöcke Vertrag, Preise, Einmalposten und Verbrauch, darunter Empfehlungen und der Button Warnung bestätigen (helles Design)" width="100%"><br><sub>Hell</sub></td></tr></table>

*Abbildung: Aufgeklappte Details. Bei Strom Haus steht unter Empfehlungen der Button „Warnung bestätigen".*

## Schaltflächen

Das sind alle Schaltflächen, die Verträge ändern, mit ihrem genauen Namen im Panel. Alle gibt es nur für Administratoren.

| Schaltfläche | Wo | Was sie tut | Nachfrage |
|---|---|---|---|
| "Neuer Vertrag" | oben im Tab Verträge | Startet den Einrichtungs-Dialog von Home Assistant, der Vertrag erscheint danach von selbst im Panel. | nein, der Dialog selbst ist der Schritt |
| "Vertrag bearbeiten" | Stift in der Zeile | Öffnet die zwei Formulare von „Neu konfigurieren": erst die allgemeinen Daten, dann die der Sparte. | ja, vor dem Speichern |
| "Folgevertrag planen" | Kalender in der Zeile | Trägt einen künftigen Tarif ein, der am Wechseldatum von selbst übernimmt. | nein |
| "Folgevertrag bearbeiten" | Kalender in der Zeile, wenn schon einer eingetragen ist | Ändert den geplanten Folgevertrag. | nein |
| "Warnung bestätigen" | Details, Block Empfehlungen | Quittiert die Abschlag-Warnung. | ja |
| "Kündigung bestätigen" | Details, Block Empfehlungen | Quittiert die Kündigungs-Erinnerung. | ja |
| "Vertrag löschen" | im Bearbeiten-Dialog | Löscht den Vertrag. | ja, der Name muss getippt werden |
| "Endgültig löschen" | in der Löschabfrage | Führt das Löschen aus, erst aktiv, wenn der Name stimmt. | siehe oben |
| "Geplanten Vertrag entfernen" | im Folgevertrag-Dialog | Löscht nur den Plan, nicht den aktuellen Vertrag. | ja |
| "Kündigung als erledigt markieren" | Häkchen im Folgevertrag-Dialog (nur wenn eine Kündigungs-Erinnerung fällig ist) | Bestätigt die Kündigung im selben Schritt wie das Speichern des Folgevertrags. | nein |

Weitere Schaltflächen mit Namen: **Vertrag verlängern** (Symbol, [siehe unten](#pauschalvertrag-verlängern)), **Archivieren** (nur wenn der Vertrag abgelaufen ist, [siehe unten](#archivieren)), **Abschläge bearbeiten** und **Posten hinzufügen**.

## Bestätigen: Warnung und Kündigung

Die Karte in der Übersicht zeigt nur den Hinweis mit dem Grund. Bestätigen kannst Du in den aufgeklappten Details im Block **Empfehlungen**, je nach Lage:

- **"Warnung bestätigen"** quittiert die Abschlag-Warnung (wie der Button „Abschlag-Warnung bestätigen"). Der Button erscheint nur, wenn die Warnung in den Vertragsdaten eingeschaltet ist und die Prognose die Schwelle unterschreitet.
- **"Kündigung bestätigen"** quittiert die Kündigungs-Erinnerung (wie der Button „Kündigung bestätigen"). Er erscheint, solange die Erinnerung aktiv ist.

Beide fragen **ein zweites Mal** nach, damit nichts aus Versehen ausgelöst wird: Beim Warnungs-Button lautet die Frage „Abschlag-Warnung bestätigen? Sie wird für diesen Vertrag erst wieder gemeldet, wenn sich die Prognose zwischendurch erholt hat.", beim Kündigungs-Button „Kündigungs-Erinnerung bestätigen? Die Erinnerung wird für diesen Vertrag ausgeblendet." Du antwortest mit **Ja, bestätigen** oder **Abbrechen**. Mehr zur Erinnerung in [Vertragsende-und-Wechsel](Vertragsende-und-Wechsel).

## Neuer Vertrag

Der Button **"Neuer Vertrag"** (oben im Tab Verträge) startet den Einrichtungs-Dialog von Home Assistant im Panel: erst Name, Sparte und Anbieter, dann die Daten der Sparte. Das Bild zeigt den zweiten Schritt für eine Gas-Sparte (Gaseinheit, Arbeitspreis, Brennwert, Zustandszahl und weitere Felder). Mit **Speichern** legst Du den Vertrag an, er erscheint von selbst im Panel. Die Felder sind dieselben wie bei der Einrichtung unter Einstellungen → Geräte & Dienste, siehe [Vertraege-Anlegen](Vertraege-Anlegen).

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/new-contract-dialog.png" alt="Dialog Neuer Vertrag, zweiter Schritt für Gas: Gaseinheit, Arbeitspreis, Grundpreis, monatlicher Abschlag, Brennwert, Zustandszahl, Warnschwelle und weitere Felder, unten die Buttons Speichern und Abbrechen" width="520"></p>

*Abbildung: Der Dialog „Neuer Vertrag", hier die Daten der Sparte Gas.*

## Vertrag bearbeiten

**"Vertrag bearbeiten"** (Stift) zeigt die zwei Formulare von „Neu konfigurieren": erst die allgemeinen Daten (mit Weiter), dann die Daten der Sparte. Alles, was die Formulare enthalten, wird durch das ersetzt, was Du speicherst. Vor dem Speichern fragt das Panel noch einmal nach („Änderungen speichern? Die Vertragsdaten werden durch das ersetzt, was das Formular zeigt." mit **Ja, speichern**).

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/edit-contract-dialog.png" alt="Dialog Vertrag bearbeiten für Strom Haus, Schritt mit Preisen und Verbrauch: Arbeitspreis, Grundpreis, monatlicher Abschlag, Verbrauchssensor, Warnschwelle und weitere Felder, unten Speichern, Abbrechen und Vertrag löschen" width="520"></p>

*Abbildung: Der Dialog „Vertrag bearbeiten" für Strom Haus mit den Daten der Sparte. Unten stehen Speichern, Abbrechen und „Vertrag löschen".*

- Bestätigte Erinnerungen, „Benachrichtigung gesendet" und der eingefrorene Verbrauch der letzten Laufzeit bleiben erhalten. Die Kündigungs-Erinnerung beginnt nur dann neu, wenn sich das Vertragsende oder die Vorlaufzeit ändert.
- Ändert sich der Abschlag, merkt sich Tariffy das Änderungsdatum, damit die Berechnung für die Zeit davor mit dem alten Abschlag weiterläuft.
- Ein leeres optionales Feld entfernt den Wert.
- **Der Name** des Vertrags steht als erstes Feld im ersten Schritt und lässt sich ändern (leer lassen = der Name bleibt). Er ändert den Namen des Vertrags und seines Geräts; Sensoren, Entity-IDs und Vertragsdaten bleiben.
- **Pauschalverträge** (Internet, Mobilfunk, Streaming, Versicherung, Sonstiges): Im Kosten-Schritt wählst Du die **Zahlweise** (monatlich, vierteljährlich, halbjährlich, jährlich) und trägst den **Betrag pro Zahlung** ein, bei einer Versicherung also zum Beispiel den Jahresbeitrag. Tariffy rechnet intern weiter mit dem Betrag pro Monat (600 € jährlich sind 50 € im Monat); bestehende Verträge sind monatlich und bleiben unverändert. Eine Änderung nur der Zahlweise gilt nicht als Preisänderung. Steigt der Beitrag, trägst Du den neuen Betrag ein (gilt ab dem Tag des Speicherns) oder verlängerst den Vertrag.
- **Kosten bisher bei Zahlung im Voraus:** Wird nicht monatlich gezahlt, zählen die **Abbuchungen**, nicht ein monatlicher Anteil: Eine Versicherung, die kurz nach Beginn mit 896,63 € bezahlt wurde, zeigt 896,63 € bei „Kosten bisher", nach einem Jahr kommt die zweite Abbuchung dazu. Die erste Abbuchung nimmt Tariffy am **Vertragsbeginn** an; das tatsächliche Datum trägst Du im Feld **Erste Abbuchung am** ein. Die Vertragsdetails zeigen die erste und die **nächste Zahlung**. Abbuchungen nach dem Vertragsende gehören schon zur nächsten Laufzeit. Bei monatlicher Zahlweise bleibt alles wie bisher. Details: [Abschlaege-und-Kosten](Abschlaege-und-Kosten).
- Erhöhungen mitten in der Laufzeit eines Verbrauchsvertrags trägst Du hier ein (der neue Abschlag gilt ab dem Tag des Speicherns).

## Folgevertrag planen

**"Folgevertrag planen"** (Kalender-Symbol; **"Folgevertrag bearbeiten"**, wenn schon einer eingetragen ist) öffnet dasselbe Formular wie „Konfigurieren" in Home Assistant, mit dem Titel „Folgevertrag · Name". Du trägst Wechseldatum und die neuen Werte ein (Anbieter, Kundennummer, Tarifname, Abschlag, Grundpreis, Vertragsende). Felder, die Du leer lässt, behalten den aktuellen Wert. Zum Wechseldatum übernimmt Home Assistant den Folgevertrag von selbst (siehe [Vertragsende-und-Wechsel](Vertragsende-und-Wechsel) und [Folgevertrag-oder-Verlaengern](Folgevertrag-oder-Verlaengern)).

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/next-contract-dialog.png" alt="Dialog Folgevertrag für Internet: Wechseldatum, Anbieter neu, Kundennummer, Tarifname, Abschlag neu, Grundpreis neu, Vertragsende neu und das Häkchen Kündigung als erledigt markieren" width="520"></p>

*Abbildung: Der Dialog „Folgevertrag" für den Vertrag Internet, mit dem Häkchen „Kündigung als erledigt markieren".*

- Ist eine Kündigungs-Erinnerung fällig, gibt es das Häkchen **"Kündigung als erledigt markieren"** (standardmäßig an). Es bestätigt die Kündigung im selben Schritt, in dem Du den Folgevertrag speicherst. Schlägt das fehl, steht dort der Hinweis, stattdessen „Kündigung bestätigen" zu benutzen.
- **"Geplanten Vertrag entfernen"** löscht nur den Plan, nicht den aktuellen Vertrag. Es fragt vorher nach („Den geplanten Folgevertrag entfernen? Der aktuelle Vertrag bleibt unverändert." mit **Ja, entfernen**).
- Einen Wechsel „jetzt" gibt es im Panel absichtlich nicht: Er würde den aktuellen Vertrag sofort ersetzen, obwohl der neue erst am geplanten Datum beginnt. Der Wechsel passiert zum Datum automatisch.

## Pauschalvertrag verlängern

Bei Verträgen ohne Verbrauch (Versicherung, Internet, Mobilfunk, Streaming, Sonstiges) steht in der Zeile ein Symbol **Vertrag verlängern** (zwei Pfeile im Kreis). Der Dialog schlägt vor: Beginn am Tag nach dem bisherigen Ende, neues Ende ein Jahr später (bei einem Vertrag **ohne Ende**: Beginn heute, Ende leer; der Vertrag läuft nach einer Preisanpassung ohne Ende weiter), Zahlweise und Betrag wie bisher. Du trägst zum Beispiel den neuen Beitrag ein, und der Dialog zeigt sofort, um wie viel Prozent der Vertrag teurer oder günstiger wird (verglichen pro Monat). Mit **Verlängern** passiert Folgendes:

- Die bisherige Laufzeit kommt in die **Historie** (Zeitraum, Anbieter, Tarif, Abschlag, gezahlte Abschläge). So entsteht pro Jahr ein Eintrag und man sieht, wie der Beitrag steigt.
- Der Vertrag läuft mit dem neuen Beginn, Ende und Betrag weiter. Anbieter, Tarif, Kundennummer und alles andere bleiben.
- Bestätigte Kündigungs-Erinnerungen und der Zeitpunkt einer früheren Abschlagsänderung gelten nur für die alte Laufzeit und beginnen neu; die Erinnerung richtet sich nach dem neuen Ende.

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/renew-dialog.png" alt="Dialog Vertrag verlängern für Internet: Beginn, Ende, Zahlweise jährlich, Betrag pro Zahlung 432 mit dem Hinweis 10,0 Prozent günstiger, Erste Abbuchung optional" width="520"></p>

*Abbildung: „Vertrag verlängern": Bei jährlicher Zahlung von 432 € zeigt der Dialog „10,0 % günstiger (36,00 € statt 39,99 € pro Monat)".*

Verbrauchsverträge (Strom, Gas, Wasser) haben dafür den **Folgevertrag**, der am geplanten Datum von selbst übernimmt. Kredite haben statt des Verlängerns die **Anschlussfinanzierung** ([Vertrag-Kredit](Vertrag-Kredit)).

## Gezahlte Abschläge

Ändert der Versorger den Abschlag von sich aus, rechnet Tariffy mit dem neuen Betrag rückwirkend, solange Du nichts einträgst. Jeder Vertrag mit Abschlag (nicht der Kredit) hat deshalb den Block **Gezahlte Abschläge**. Dort trägst Du ein, **was ab wann gezahlt wurde**, zum Beispiel bei Gas Monat 1–7 178 €, Monat 8 174,41 €, Monat 9–11 215 €:

| Monat | Abschlag |
|-------|----------|
| März bis Juli | 178,00 € |
| August | 174,41 € |
| September bis heute | 215,00 € |

- Der Dialog **Abschläge bearbeiten** hat **ein Feld je Zahlung der Laufzeit**, passend zur **Zahlweise**: bei monatlicher Zahlung ein Feld je Monat, bei vierteljährlicher vier im Jahr, bei halbjährlicher zwei, bei jährlicher eines. Bei Zahlungen, die nicht monatlich sind, steht das Datum der Abbuchung vor dem Feld, und Du gibst den Betrag **je Zahlung** ein. Zahlungen, die **noch nicht fällig waren, sind gesperrt** und zeigen den aktuellen Abschlag. Hat der Vertrag kein Ende, stehen die Zahlungen bis heute da. Speichern gilt für alle Zahlungen zusammen.
- Eine Änderung gilt **auch für die folgenden Zahlungen, die noch denselben Betrag haben**: Du trägst 178 im März ein, 174,41 im August und 215 im September; mehr ist nicht zu tun. Ein leeres Feld übernimmt den Betrag der Zahlung davor.
- Die **letzte Zahlung ist der aktuelle Abschlag**: Tariffy übernimmt ihren Betrag als Abschlag des Vertrags. Der Vertrag braucht einen Beginn.
- Gespeichert werden nur die Zahlungen, bei denen sich der Betrag ändert (höchstens 60).
- Mit dem Verlauf rechnen **Gezahlt bisher**, **Guthaben/Nachzahlung bisher**, die **Prognose zum Vertragsende** und der **empfohlene Abschlag** mit den Beträgen, die wirklich galten. Ohne Zeilen gilt wie bisher der aktuelle Abschlag.
- Beim **Verlängern** eines Pauschalvertrags und bei einem **Tarifwechsel** beginnt die neue Laufzeit ohne den alten Verlauf; die alte Laufzeit steht mit ihren Werten in der Historie.

Die Rechenregeln stehen in [Abschlagsverlauf-und-Einmalposten](Abschlagsverlauf-und-Einmalposten).

## Einmalposten

Jeder Vertrag hat in den Details den Block **Einmalposten**. Dort trägst Du einmalige Beträge ein, die nicht zum Abschlag gehören, mit **Bezeichnung**, **Betrag** und **Datum**:

- ein **positiver** Betrag ist eine **Gutschrift**, zum Beispiel ein Wechselbonus,
- ein **negativer** Betrag ist eine **Rechnung**, zum Beispiel das Honorar eines Maklers.

Mit **Posten hinzufügen** legst Du einen Posten an, der Stift in der Zeile bearbeitet ihn (dort lässt er sich auch löschen). Die Zeile **Saldo** unter den Posten zeigt die Summe. Ein Posten zählt ab seinem Datum (ohne Datum sofort). Er verändert den **Saldo bisher** und die **Kosten gesamt** über alle Laufzeiten: ein Bonus senkt die Kosten, eine Rechnung erhöht sie. **Prognose zum Vertragsende und die Warnung bei zu niedrigem Abschlag hängen weiter nur vom Verbrauch ab.** Die Einmalposten gelten für jede Art von Vertrag, bleiben beim Verlängern und beim Tarifwechsel erhalten und stehen in der Sicherung. Bei der Sparte Streaming erscheint der Block nicht, solange der Vertrag keine Einmalposten hat. Das Feld **Neukundenbonus** im Vertragsformular bleibt wie es war und wird nur angezeigt.

## Archivieren

Ein Vertrag, dessen Ende vorbei ist und für den kein Folgevertrag geplant ist, bekommt in der Übersicht das Badge **Abgelaufen** und den Hinweis, dass er sich archivieren lässt. In den Details steht der Button **Archivieren** (mit Rückfrage „Ja, archivieren"). Danach verschwindet der Vertrag aus Übersicht, Kosten und Verträgen und aus den Summen, steht in der **Historie**, und seine Erinnerungen und Warnungen sind aus. Es wird nichts gelöscht; mit **Zurückholen** in der Historie ist er wieder da. Nichts wird von allein archiviert. Mehr in [Panel-Historie](Panel-Historie) und [Archiv-und-Historie](Archiv-und-Historie).

## Vertrag löschen

**"Vertrag löschen"** steht im Bearbeiten-Dialog. Weil das nicht rückgängig zu machen ist, öffnet sich die Frage „Den Vertrag ... endgültig löschen? Das lässt sich nicht rückgängig machen. Zur Bestätigung den Namen eintippen." Der Button **"Endgültig löschen"** wird erst aktiv, wenn Du den **Namen des Vertrags** eintippst.

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/delete-contract-dialog.png" alt="Löschabfrage im Dialog Vertrag bearbeiten für Strom Haus: Hinweis zum endgültigen Löschen, Eingabefeld für den Namen mit rotem Rand, weil erst Strom getippt ist, und der noch ausgegraute Button Endgültig löschen" width="520"></p>

*Abbildung: Die Löschabfrage. Solange der Name nicht stimmt (hier erst „Strom" statt „Strom Haus"), bleibt „Endgültig löschen" gesperrt.*

- Sensoren, Buttons und Gerät des Vertrags werden entfernt, ebenso offene Benachrichtigungen zu Kündigung und Abschlag. Dazu heißt es im Panel: „Seine Sensoren und Buttons werden entfernt. Die Langzeit-Statistiken, die Home Assistant schon aufgezeichnet hat, bleiben in der Datenbank." Sie lassen sich in den Entwicklerwerkzeugen unter Statistiken entfernen.
- Tariffy merkt sich den gelöschten Vertrag **30 Tage** und bietet ihn im Tab **Sicherung** zum Zurückholen an ([Panel-Sicherung](Panel-Sicherung)).
- Löschst Du den **letzten** Vertrag, verschwindet das Panel aus der Seitenleiste. Einen neuen Vertrag legst Du dann unter Einstellungen → Geräte & Dienste → Tariffy → Hinzufügen an.

## Beispiel: Einmalposten eintragen

Du hast beim Vertrag **Strom Haus** noch eine Gebühr von 12,50 € zu verbuchen. In den Beispieldaten stehen dort schon der Wechselbonus (+80,00 €, 15.01.2026) und das Honorar Makler (−25,00 €, 20.01.2026), die Zeile **Saldo** zeigt +55,00 €.

1. Tab **Verträge**, Zeile **Strom Haus** aufklappen.
2. Im Block **Einmalposten** auf **Posten hinzufügen** klicken.
3. Im Dialog „Einmalposten hinzufügen" bei **Bezeichnung** „Gebühr" eintragen, bei **Betrag (+ Gutschrift, − Rechnung)** „-12,5", das **Datum** nach Wunsch.
4. **Speichern**.

Danach steht der Posten in der Liste, und **Saldo** zeigt +42,50 € (55,00 € − 12,50 €). Rechnerisch sinkt auch das **Guthaben / Nachzahlung bisher** von −206,24 € auf −218,74 €, denn der Posten zählt ab seinem Datum im Saldo. Die **Prognose zum Vertragsende** (−495 €) und der empfohlene Abschlag (127,66 €) ändern sich nicht, weil sie nur vom Verbrauch abhängen.

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/once-dialog.png" alt="Dialog Einmalposten hinzufügen für Strom Haus: Bezeichnung Gebühr, Betrag minus 12,5, Datum leer, Buttons Speichern und Abbrechen" width="520"></p>

*Abbildung: Der Dialog „Einmalposten hinzufügen" mit dem Beispiel „Gebühr", −12,5.*

## Auf dem Handy

Auf dem Handy stehen die Symbole in der Zeile unter dem Namen, und die Details-Blöcke klappen untereinander auf. Alles andere funktioniert wie am Desktop.

<table align="center"><tr><td align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-contracts.png" alt="Tab Verträge auf dem Handy: oben der Button Neuer Vertrag, darunter die Verträge als Karten mit Symbolen für Folgevertrag und Bearbeiten (dunkles Design)" width="300"><br><sub>Dunkel</sub></td><td align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-contracts-light.png" alt="Tab Verträge auf dem Handy: oben der Button Neuer Vertrag, darunter die Verträge als Karten mit Symbolen für Folgevertrag und Bearbeiten (helles Design)" width="300"><br><sub>Hell</sub></td></tr></table>

*Abbildung: Der Tab Verträge auf dem Handy.*

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/list-390.png" alt="Tab Verträge bei 390 Pixel Breite: Neuer Vertrag oben, jede Karte mit Kennzeichnung, Saldo und den Symbolen Verlängern, Folgevertrag, Bearbeiten und Pfeil" width="300"></p>

*Abbildung: Dieselbe Liste bei 390 Pixel Breite.*

## Fehler und Hinweise

Schlägt eine Aktion fehl, erscheint die Meldung „Aktion fehlgeschlagen: ..." in Rot unter dem Button. Beim Löschen heißt sie „Löschen fehlgeschlagen: ...", beim Speichern „Speichern fehlgeschlagen: ...".

| Meldung oder Problem | Lösung |
|---|---|
| „Das Formular konnte nicht geladen werden" | Home Assistant war kurz nicht erreichbar oder der Vertrag ist gerade nicht geladen. Dialog schließen und neu öffnen. |
| „Dieses Formular enthält Felder, die das Panel noch nicht anzeigen kann. Bitte die Einrichtung von Home Assistant benutzen." | Den Vertrag unter Einstellungen → Geräte & Dienste → Tariffy bearbeiten. |
| Keine Buttons oder Symbole zu sehen | Die Aktionen gibt es nur für Administratoren ([Panel-Rechte-und-Design](Panel-Rechte-und-Design)). |
| Alte Oberfläche, Buttons fehlen | Seite hart neu laden (Strg+F5). |

## Siehe auch

- [Panel-Uebersicht](Panel-Uebersicht) und [Panel-Kosten](Panel-Kosten): die Ansichten ohne Aktionen.
- [Panel-Historie](Panel-Historie): frühere Laufzeiten, Archiv, alte Verträge von Hand eintragen.
- [Panel-Sicherung](Panel-Sicherung): gelöschte Verträge zurückholen.
- [Vertraege-Anlegen](Vertraege-Anlegen): die Felder beim Anlegen.
- [Abschlaege-und-Kosten](Abschlaege-und-Kosten), [Abschlagsverlauf-und-Einmalposten](Abschlagsverlauf-und-Einmalposten), [Vertragsende-und-Wechsel](Vertragsende-und-Wechsel), [Folgevertrag-oder-Verlaengern](Folgevertrag-oder-Verlaengern): die Hintergründe zu den Aktionen.
