🇩🇪 Deutsch · [🇬🇧 English](EN-Creating-Contracts)

# Verträge anlegen

Hier findest Du den Überblick über alle Sparten, die allgemeinen Felder des ersten Formulars, die Wege zum Bearbeiten und Löschen eines Vertrags und typische Fehler. Die Felder der einzelnen Sparten stehen auf den jeweiligen Sparten-Seiten.

**Inhalt:**

- [Wo legst Du einen Vertrag an?](#wo-legst-du-einen-vertrag-an)
- [Alle Sparten im Überblick](#alle-sparten-im-überblick)
- [Die allgemeinen Felder (Schritt 1)](#die-allgemeinen-felder-schritt-1)
- [Vertrag bearbeiten](#vertrag-bearbeiten)
- [Vertrag löschen](#vertrag-löschen)
- [Typische Fehler](#typische-fehler)

## Wo legst Du einen Vertrag an?

Es gibt zwei Wege, die zum selben Formular führen:

1. **Im Panel:** Tab **Verträge**, Button **Neuer Vertrag** (nur Administratoren).
2. **In Home Assistant:** **Einstellungen → Geräte & Dienste → Integration hinzufügen → Tariffy**.

Das erste Formular heißt **Neuen Vertrag anlegen** („Allgemeine Vertragsdaten.“) und ist für alle Sparten gleich. Mit der **Sparte** entscheidest Du, welches Formular danach folgt. Im Panel erscheinen die Formulare in einem Dialog; die Schaltfläche heißt auf allen Schritten außer dem letzten **Weiter**, auf dem letzten **Speichern**. Jeder Vertrag wird ein eigenes Gerät, wie in [Erste Schritte](Erste-Schritte) beschrieben.

![Der Dialog Neuer Vertrag im Panel, hier der Schritt Gas-Details mit Gaseinheit, Arbeitspreis, Grundpreis, Monatlichem Abschlag, Brennwert und Zustandszahl](https://raw.githubusercontent.com/wiki/weskona/tariffy/images/new-contract-dialog.png)

*Abbildung: Der Dialog „Neuer Vertrag“ im Panel, hier der zweite Schritt einer Gas-Sparte mit den Buttons „Speichern“ und „Abbrechen“.*

## Alle Sparten im Überblick

Die Auswahl **Sparte** bietet diese Einträge in dieser Reihenfolge an:

| Sparte | Abrechnung | Formulare nach Schritt 1 | Seite |
|---|---|---|---|
| Strom | nach Verbrauch | **Strom-Details** | [Vertrag Strom](Vertrag-Strom) |
| Strom (Zweizählertarif, Hoch-/Niedertarif) | nach Verbrauch, zwei Zähler-Register | **Strom-Details (Zweizählertarif, Hoch-/Niedertarif)** | [Vertrag Strom](Vertrag-Strom#zweizählertarif-htnt) |
| Gas | nach Verbrauch | **Gas-Details** | [Vertrag Gas](Vertrag-Gas) |
| Wasser | nach Verbrauch | **Wasservertrag Details** | [Vertrag Wasser](Vertrag-Wasser) |
| Internet | Pauschale | **Kosten** | [Vertrag Internet und Mobilfunk](Vertrag-Internet-und-Mobilfunk) |
| Mobilfunk | Pauschale | **Kosten** | [Vertrag Internet und Mobilfunk](Vertrag-Internet-und-Mobilfunk) |
| Streaming | Pauschale | **Kosten** | [Vertrag Streaming](Vertrag-Streaming) |
| Kredit / Finanzierung | eigener Tilgungsplan, zählt nicht in die Summen der Verträge | **Kredit / Finanzierung** | [Vertrag Kredit](Vertrag-Kredit) |
| Leasing | Pauschale plus Kilometer | **Leasing**, dann **Kosten** | [Vertrag Leasing](Vertrag-Leasing) |
| Versicherung | Pauschale | **Versicherung**, bei Kfz **Kfz-Versicherung**, dann **Kosten** | [Vertrag Versicherung](Vertrag-Versicherung) |
| Sonstiges | Pauschale | **Kosten** | [Vertrag Sonstiges](Vertrag-Sonstiges) |

**Verbrauchsverträge** (Strom, Strom HT/NT, Gas, Wasser) rechnen mit einem Zähler-Sensor echte Kosten, Saldo und Prognose aus. **Pauschalverträge** haben einen Betrag pro Zahlung und eine Zahlweise (monatlich, vierteljährlich, halbjährlich, jährlich). Im Panel stehen Kredit und Leasing in der Gruppe **Kredite / Finanzierungen**.

> **Gut zu wissen:** Die Sparte bestimmt, welche Sensoren ein Vertrag bekommt. Sie lässt sich später im Bearbeiten-Formular zwar auswählen, aber lege den Vertrag lieber gleich mit der richtigen Sparte an. Welche Sensoren es wo gibt, steht in der [Sensoren Referenz](Sensoren-Referenz).

## Die allgemeinen Felder (Schritt 1)

| Feld | Pflicht | Beschreibung |
|---|---|---|
| Bezeichnung (z. B. Strom Haus) | ja | Kurzer Name; er erscheint im Gerätenamen und im Panel. Beim Bearbeiten heißt das Feld **Name**. |
| Sparte | ja | Siehe die Tabelle oben. |
| Anbieter | ja | Name des Energieversorgers oder Anbieters. |
| Kundennummer | nein | Deine Kundennummer aus den Vertragsunterlagen. |
| Tarifname | nein | Bezeichnung des Tarifs, zum Beispiel „Ökostrom Plus“. |
| Icon | nein | Eigenes Icon des Vertrags, zum Beispiel `mdi:car`. Gilt im Panel und für die Sensoren des Vertrags (Sensoren mit Statussymbol wie Guthaben/Nachzahlung behalten ihres). Leer = das Icon der Sparte. |
| Vertragsbeginn | nein | Datum, ab dem der Vertrag gilt. Ohne Beginn gibt es keine Verbrauchsmessung. |
| Vertragsende / Laufzeit bis | nein | Letzter Gültigkeitstag des Vertrags. |
| Mindestlaufzeit (Monate) | nein | Das Panel zeigt, bis wann der Vertrag mindestens läuft (Beginn plus Mindestlaufzeit). |
| Kündigungsfrist (Monate) | nein | Monate vor Vertragsende, bis zu denen die Kündigung vorliegen muss. Wenn eingetragen, bezieht sich die Erinnerung auf diese Frist statt auf das Vertragsende. |
| Kündigung erinnern | ja | **Keine Erinnerung**, **1 Monat vorher** bis **4 Monate vorher** (Voreinstellung: 3 Monate). Bezieht sich auf das Vertragsende, mit eingetragener Kündigungsfrist auf deren Ablauf. |
| Benachrichtigungs-Ziel (notify-Dienst) | nein | Home-Assistant-Benachrichtigungsdienst für die Erinnerung, zum Beispiel `mobile_app_iphone`. Das Feld erscheint nur, wenn Home Assistant mindestens einen notify-Dienst kennt; eigene Werte sind möglich. |

Ein Datumsfeld ist ein normaler Datumswähler, die Felder für Monate sind Zahlenfelder. Wie die Erinnerung genau abläuft, beschreibt [Vertragsende und Wechsel](Vertragsende-und-Wechsel).

> **Gut zu wissen:** Ohne **Vertragsende** gibt es keine Kündigungs-Erinnerung, weil sich das Datum aus dem Vertragsende berechnet.

## Vertrag bearbeiten

So änderst Du einen bestehenden Vertrag:

1. Öffne im Panel den Tab **Verträge** und klicke in der Zeile des Vertrags auf den Stift **Vertrag bearbeiten** (nur Administratoren). Alternativ nutzt Du in Home Assistant das Menü des Tariffy-Eintrags (Neu konfigurieren, englisch Reconfigure).
2. Es öffnet sich dasselbe Formular wie beim Anlegen, aber mit den gespeicherten Werten und dem Titel **Vertrag bearbeiten · Strom Haus** (mit dem Namen Deines Vertrags).
3. Ändere die Werte und klicke auf **Weiter** beziehungsweise im letzten Schritt auf **Speichern**.
4. Im Panel fragt Tariffy ein letztes Mal nach: „Änderungen speichern? Die Vertragsdaten werden durch das ersetzt, was das Formular zeigt.“ Bestätige mit **Ja, speichern**.
5. Home Assistant lädt den Vertrag neu und rechnet mit den neuen Werten.

![Der Dialog Vertrag bearbeiten für Strom Haus mit den Feldern der Strom-Details und den Buttons Speichern, Abbrechen und Vertrag löschen](https://raw.githubusercontent.com/wiki/weskona/tariffy/images/edit-contract-dialog.png)

*Abbildung: Der Dialog „Vertrag bearbeiten · Strom Haus“ (Strom-Details) mit den Buttons „Speichern“, „Abbrechen“ und „Vertrag löschen“.*

Was beim Bearbeiten erhalten bleibt und was sich ändert:

- **Erhalten bleiben** der Verlauf und die Merkzettel von Tariffy: Historie, Einmalposten, Abschlagsverlauf, Außenzähler, der Verbrauch der letzten Laufzeit und archivierte Verträge.
- **Neu beginnt die Kündigungs-Erinnerung**, wenn Du Vertragsende, **Kündigung erinnern** oder **Kündigungsfrist (Monate)** änderst: Eine schon bestätigte Erinnerung ist dann wieder offen.
- **Ändert sich der Abschlag**, merkt sich Tariffy das Datum der Änderung. Der neue Betrag gilt dann erst ab heute, damit „Guthaben/Nachzahlung (Bisher)“ nicht rückwirkend neu gerechnet wird. Ein Abschlag, den Du zum ersten Mal von 0 auf einen Betrag setzt, gilt dagegen für die ganze Laufzeit. Hat der Versorger den Abschlag selbst geändert, trägst Du den Verlauf ein, siehe [Abschlagsverlauf und Einmalposten](Abschlagsverlauf-und-Einmalposten).
- Lässt Du das Feld **Name** leer, bleibt der bisherige Name.

Für einen geplanten Tarifwechsel gibt es nicht dieses Formular, sondern den Folgevertrag: [Folgevertrag oder Verlängern](Folgevertrag-oder-Verlaengern).

## Vertrag löschen

Im Dialog **Vertrag bearbeiten** gibt es den roten Button **Vertrag löschen**. Danach fragt Tariffy: „Den Vertrag "Strom Haus" endgültig löschen? Das lässt sich nicht rückgängig machen. Zur Bestätigung den Namen eintippen.“ Der Button **Endgültig löschen** bleibt gesperrt, bis Du den Namen des Vertrags genau eingetippt hast.

![Die Rückfrage zum Löschen im Dialog Vertrag bearbeiten: ein Eingabefeld für den Namen, daneben die Buttons Endgültig löschen und Abbrechen](https://raw.githubusercontent.com/wiki/weskona/tariffy/images/delete-contract-dialog.png)

*Abbildung: Die Rückfrage beim Löschen. Der Button „Endgültig löschen“ ist gesperrt, solange der eingetippte Name nicht stimmt (im Bild steht erst „Strom“ statt „Strom Haus“).*

Nach dem Löschen:

- Die Sensoren und Buttons des Vertrags sind weg. Die Langzeitstatistiken, die Home Assistant schon aufgezeichnet hat, bleiben in der Datenbank.
- Tariffy merkt sich den Vertrag **30 Tage lang** (die letzten 20), auch wenn Du ihn direkt in Home Assistant gelöscht hast. Im Tab **Sicherung** kannst Du ihn mit **Zurückholen** wiederherstellen. Das geht nicht, wenn es inzwischen einen Vertrag mit gleichem Namen und gleicher Sparte gibt. Alles dazu steht unter [Panel Sicherung](Panel-Sicherung).

> **Gut zu wissen:** Läuft ein Vertrag nur aus, musst Du ihn nicht löschen: Ein abgelaufener Vertrag lässt sich archivieren und bleibt dann in der Historie, siehe [Archiv und Historie](Archiv-und-Historie).

## Typische Fehler

| Problem | Ursache und Lösung |
|---|---|
| Kosten, Saldo und Prognose bleiben leer | Es fehlt der **Verbrauchssensor**, der **Vertragsbeginn** oder der **Arbeitspreis**. Verbrauchsmessung braucht Sensor und Beginn. |
| Der Verbrauch ist unbekannt, obwohl ein Sensor eingetragen ist | Die Langzeitstatistik des Sensors reicht nicht bis zum Vertragsbeginn zurück (zum Beispiel nach Umbenennen oder Neuanlegen). Trage den **Zählerstand bei Vertragsbeginn (optional)** ein, er hat Vorrang. Siehe [Verbrauch messen](Verbrauch-Messen). |
| Keine Kündigungs-Erinnerung | **Vertragsende** fehlt oder **Kündigung erinnern** steht auf **Keine Erinnerung**. |
| „Keine gültige Zahl.“ bei Brennwert oder Zustandszahl | Diese zwei Felder sind Textfelder. Erlaubt sind Punkt oder Komma (`11.2` oder `11,2`), sonst nichts. |
| Der Saldo wirkt falsch, weil der Abschlag fehlt | Der **Monatliche Abschlag** ist ein Pflichtfeld mit Voreinstellung 0. Trage den echten Betrag ein. |
| Falsche Sensoren oder fehlende Sensoren | Die **Sparte** passt nicht, zum Beispiel Strom statt Strom (Zweizählertarif, Hoch-/Niedertarif). Staffelpreise und Nachttarif erscheinen nur, wenn in Home Assistant ein passendes Land eingestellt ist, siehe die Sparten-Seiten. |
| Das Panel fehlt in der Seitenleiste | Das Panel erscheint erst, wenn mindestens ein Vertrag geladen ist. Danach Browserseite hart neu laden (Strg+F5). |

Weitere Hilfe bietet die [Fehlerbehebung](Fehlerbehebung).

## Siehe auch

- [Erste Schritte](Erste-Schritte)
- [Vertrag Strom](Vertrag-Strom), [Vertrag Gas](Vertrag-Gas), [Vertrag Wasser](Vertrag-Wasser)
- [Panel Verträge](Panel-Vertraege)
- [Panel Sicherung](Panel-Sicherung)
- [Abschläge und Kosten](Abschlaege-und-Kosten)
- [Fehlerbehebung](Fehlerbehebung)
