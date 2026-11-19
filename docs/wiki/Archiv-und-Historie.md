🇩🇪 Deutsch · [🇬🇧 English](EN-Archive-and-History)

# Archiv und Historie

Hier erfährst Du, was mit einem Vertrag nach seinem Ende passiert: Du kannst ihn **archivieren**, ohne etwas zu löschen, Du siehst im Tab **Historie** alle **früheren Laufzeiten**, und Du kannst alte Verträge, die Du nie eingetragen hast, **nachtragen**. Die Seite ist für alle, die ihre Kosten über mehrere Jahre im Blick behalten wollen.

**Inhalt:**

- [Abgelaufene Verträge archivieren](#abgelaufene-verträge-archivieren)
- [Der Tab Historie](#der-tab-historie)
- [Frühere Laufzeiten](#frühere-laufzeiten)
- [Beispiel mit Zahlen](#beispiel-mit-zahlen)

## Abgelaufene Verträge archivieren

Archivieren räumt einen beendeten Vertrag aus dem Alltag, ohne ihn zu löschen. Das Archivieren geschieht nie von selbst.

### Wann ein Vertrag archivierbar ist

Ein Vertrag lässt sich archivieren, wenn alle drei Punkte stimmen:

- Das **Vertragsende ist vorbei** (der Tag des Vertragsendes selbst zählt noch nicht).
- Es ist **kein Folgevertrag geplant**.
- Er ist noch nicht archiviert.

Ein Vertrag ohne Vertragsende läuft nie ab und lässt sich deshalb nicht archivieren. Ein abgelaufener Vertrag bekommt in der Übersicht die Marke **Abgelaufen** und in den Vertragsdetails den Hinweis, dass Du ihn archivieren kannst.

### Archivieren und Zurückholen

1. Öffne im Panel den Tab **Verträge** und klappe die Details des abgelaufenen Vertrags auf.
2. Klicke auf **Archivieren**. Es folgt eine Rückfrage („Diesen Vertrag archivieren? …"), die Du mit **Ja, archivieren** bestätigst. Nur Administratoren sehen die Schaltfläche.
3. Der Vertrag verschwindet aus Übersicht, Kosten, Verträgen und den Summen und steht im Tab **Historie** in der Gruppe **Archivierte Verträge**.
4. Zum Zurückholen klickst Du dort auf **Zurückholen** und bestätigst mit **Ja, zurückholen**.

Das passiert beim Archivieren:

- Die **letzte Laufzeit** kommt als Eintrag in die Historie des Vertrags (mit Markierung „archiviert").
- Erinnerung und Abschlag-Warnung sind aus, offene Dauerbenachrichtigungen werden entfernt.
- **Nichts wird gelöscht.** Die Sensoren, Buttons und ihre Statistiken bleiben bestehen.

Beim **Zurückholen** wird genau dieser eine Eintrag wieder entfernt, alle früheren Laufzeiten bleiben. Der Vertrag ist dann wieder normal da, und eine Erinnerung, die vorher aktiv war, meldet sich wieder.

> **Gut zu wissen:** Archivieren und Löschen sind verschiedene Dinge. Ein gelöschter Vertrag verliert seine Sensoren und bleibt nur 30 Tage zurückholbar (siehe [Sicherung-und-Umzug](Sicherung-und-Umzug)). Ein archivierter bleibt unbegrenzt erhalten.

## Der Tab Historie

Der Tab **Historie** zeigt zwei Gruppen, jeweils mit einem Block pro Vertrag:

- **Archivierte Verträge** mit der Marke „Archiviert" und der Schaltfläche **Zurückholen**.
- **Frühere Laufzeiten** der Verträge, die noch laufen.

Jede Zeile ist eine Laufzeit mit **Laufzeit** (Zeitraum, darunter Anbieter und Tarif), **Abschlag**, **Kosten**, **Verbrauch** und **Saldo**; die neueste steht oben. Unter dem Block stehen die **Kosten gesamt** über alle Laufzeiten mit „seit <Datum>" und der Zahl der Laufzeiten. Bei einer früheren Laufzeit zählen ihre Kosten, und sind keine eingetragen, die gezahlten Abschläge. Fehlt beides, steht „mindestens …", weil die Summe dann unvollständig ist. Bei einem archivierten Vertrag steht die letzte Laufzeit schon in der Historie und wird nicht doppelt gezählt.

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/desktop-history.png"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/desktop-history-light.png" alt="Der Tab Historie mit der Gruppe Archivierte Verträge (Strom Altvertrag, zwei Laufzeiten, Schaltfläche Zurückholen) und der Gruppe Frühere Laufzeiten (Strom Haus, zwei Laufzeiten), oben rechts die Schaltfläche Alten Vertrag hinzufügen" width="100%"></picture></p>

*Abbildung: Der Tab „Historie" mit Mock-Daten vom 12.07.2026: ein archivierter Vertrag und die früheren Laufzeiten eines laufenden Vertrags.*

Alle Benutzer sehen die Historie, nur Administratoren sehen **Alten Vertrag hinzufügen**, die Stifte zum Bearbeiten und die Aktionen. Alles Weitere zum Aufbau des Tabs steht unter [Panel-Historie](Panel-Historie).

## Frühere Laufzeiten

### Wie sie entstehen

Eine Laufzeit kommt auf drei Wegen in die Historie:

- **Automatisch**, wenn ein Folgevertrag übernimmt oder wenn Du einen Pauschalvertrag verlängerst (siehe [Vertragsende-und-Wechsel](Vertragsende-und-Wechsel)).
- **Beim Archivieren** als letzte Laufzeit des Vertrags.
- **Von Hand**, wenn Du einen älteren Vertrag nachträgst (siehe unten).

Gespeichert wird nur, was das Panel ohnehin zeigt: Zeitraum, Anbieter, Tarif, Arbeitspreis, Grundpreis, Abschlag, Kosten, gezahlte Abschläge, Saldo und Verbrauch, bei einem Kredit zusätzlich Kreditsumme, Zinsen und Restschuld. **Kunden-, Zähler- und Marktlokationsnummern sind nicht dabei.** Pro Vertrag bleiben höchstens **50 Laufzeiten**; ist die Historie voll, fällt beim automatischen Eintrag die älteste heraus, und beim Nachtragen kommt die Meldung „Die Historie ist voll (50 Laufzeiten)." Die Historie hat keine eigene Entität in Home Assistant; sie steht im Panel und in der Sicherung.

### Eine frühere Laufzeit nachtragen

Du hast einen Vertrag, der vor Tariffy lief? Trage ihn nach, dann stimmen auch die Gesamtkosten.

1. Öffne den Tab **Historie** und klicke auf **Alten Vertrag hinzufügen** (nur Administratoren).
2. Wähle bei **Vertrag**, zu welchem Vertrag die Laufzeit gehört. Zähler und Sparte kommen von ihm.
3. Trage **Beginn** und **Ende** ein. Das Ende darf nicht vor dem Beginn liegen.
4. Trage, soweit bekannt, **Anbieter**, **Tarif**, **Arbeitspreis je Einheit (€)**, **Grundpreis pro Monat (€)** und **Abschlag pro Monat (€)** ein.
5. Lass die grau hinterlegten Felder **Verbrauch**, **Kosten (€)**, **Gezahlte Abschläge (€)** und **Saldo (€)** leer. Sie werden berechnet; darunter steht jeweils, woher der Wert kommt.
6. Klicke auf **Speichern**. Vorher wird nichts gespeichert.

![Der Dialog Alten Vertrag hinzufügen für den Vertrag Strom Haus, Zeitraum 2024, mit eingetragenem Verbrauch 3000 und berechneten Feldern Kosten, Gezahlte Abschläge und Saldo](https://raw.githubusercontent.com/wiki/weskona/tariffy/images/term-dialog.png)

*Abbildung: Der Dialog „Alten Vertrag hinzufügen" mit Mock-Daten. Der Verbrauch ist von Hand eingetragen („Von dir eingetragen"), die anderen drei Werte sind berechnet („Berechnet").*

### Was automatisch berechnet wird

In jedes Feld kannst Du selbst einen Wert schreiben; er hat dann Vorrang, und der Rest richtet sich danach. Berechnet wird so:

| Wert | Berechnung |
|------|------------|
| Verbrauch | Aus den Langzeitstatistiken des Zählers zwischen Beginn und Ende; beim Zweizählertarif werden beide Register addiert. Gibt es für die Zeit keine Statistik, trägst Du ihn selbst ein. Pauschalverträge haben keinen Verbrauch. |
| Gezahlte Abschläge | Abschlag pro Monat mal Dauer in Monaten (Tage geteilt durch 30,44). Hast Du unter **Abschläge nach Zahlungen (freiwillig)** die tatsächlichen Zahlungen eingetragen, zählen diese. |
| Kosten | Verbrauch mal Arbeitspreis plus Grundpreis mal Monate; bei Gas wird der Verbrauch mit Brennwert und Zustandszahl des Vertrags in kWh umgerechnet. Bei Pauschalverträgen sind die Kosten das, was gezahlt wurde. |
| Saldo | Gezahlte Abschläge minus Kosten (nur bei Verträgen mit Verbrauch). Positiv ist Guthaben, negativ Nachzahlung. |

> **Gut zu wissen:** Staffelpreise, dynamische Preise und getrennte Preise für Hoch- und Niedertarif werden hier nicht gerechnet. Trage in dem Fall die Kosten selbst ein.

### Bearbeiten und löschen

Der Stift in der Zeile öffnet **Laufzeit bearbeiten**. Werte, die Du selbst eingetragen hast, bleiben stehen; berechnete werden neu berechnet. Von Hand eingetragene Laufzeiten sind mit „von Hand eingetragen" markiert. Mit **Laufzeit löschen** (Rückfrage „Diese Laufzeit aus der Historie löschen?") entfernst Du eine Zeile. Bearbeitest Du die Laufzeit, die das Archivieren angelegt hat, bleibt ihre Archiv-Markierung erhalten, damit **Zurückholen** sie wieder findet.

## Beispiel mit Zahlen

Beispiel (die Werte aus dem Screenshot oben): Du trägst für den Vertrag „Strom Haus" die Laufzeit 01.01.2024 bis 31.12.2024 nach, Arbeitspreis 0,30 €/kWh, Grundpreis 10 €/Monat, Abschlag 90 €/Monat und einen Verbrauch von 3000 kWh.

1. Dauer: 365 Tage / 30,44 = 11,99 Monate.
2. **Gezahlte Abschläge** = 90 € × 11,99 = 1.079,10 €.
3. **Kosten** = 3000 × 0,30 € + 10 € × 11,99 = 1.019,90 €.
4. **Saldo** = 1.079,10 € − 1.019,90 € = +59,20 €, also ein Guthaben.

Hättest Du den Verbrauch leer gelassen, würde Tariffy ihn aus den Statistiken des Zählers holen und alles daraus rechnen. In den Tests ergeben Zählerstände von 1000 und 4200 kWh am Anfang und am Tag nach dem Ende einen Verbrauch von 3200 kWh.

## Siehe auch

- [Panel-Historie](Panel-Historie): Der Tab Historie im Panel
- [Vertragsende-und-Wechsel](Vertragsende-und-Wechsel): Wann Laufzeiten automatisch in die Historie kommen
- [Folgevertrag-oder-Verlaengern](Folgevertrag-oder-Verlaengern): Folgevertrag oder Verlängern
- [Sicherung-und-Umzug](Sicherung-und-Umzug): Historie und Archiv sind in der Sicherung enthalten
- [Abschlaege-und-Kosten](Abschlaege-und-Kosten): Gesamtkosten über alle Laufzeiten
