🇩🇪 Deutsch · [🇬🇧 English](EN-Backup-and-Migration)

# Sicherung und Umzug

Diese Seite zeigt, wie Du Deine Verträge in eine Datei sichern, aus ihr wiederherstellen und auf eine neue Home-Assistant-Installation mitnehmen kannst, und wie Du einen versehentlich gelöschten Vertrag zurückholst. Sie ist für alle, die ihre Vertragsdaten nicht verlieren wollen. Alles hier ist nur für Administratoren.

**Inhalt:**

- [Welche Sicherungen es gibt](#welche-sicherungen-es-gibt)
- [Sicherung erstellen](#sicherung-erstellen)
- [Aus einer Sicherung wiederherstellen](#aus-einer-sicherung-wiederherstellen)
- [Was in der Sicherung ist und was nicht](#was-in-der-sicherung-ist-und-was-nicht)
- [Umzug auf eine neue Home-Assistant-Instanz](#umzug-auf-eine-neue-home-assistant-instanz)
- [Gelöschte Verträge: 30 Tage Zeit](#gelöschte-verträge-30-tage-zeit)
- [Beispiel mit Zahlen](#beispiel-mit-zahlen)

## Welche Sicherungen es gibt

- **Das normale Home-Assistant-Backup** enthält Tariffy mit: Die Verträge liegen im Speicher von Home Assistant. Das ist der Weg, wenn Du Home Assistant als Ganzes wiederherstellst.
- **Die Tariffy-Sicherung** im Tab **Sicherung** des Panels ist eine einzelne Datei nur mit Deinen Verträgen. Sie hilft, wenn Du nur die Verträge brauchst, wenn Du auf eine frische Installation umziehst oder wenn Du vor einer größeren Änderung eine Kopie ziehen willst.
- **Gelöschte Verträge** merkt sich Tariffy 30 Tage lang selbst, ohne dass Du etwas tun musst.

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/desktop-backup.png"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/desktop-backup-light.png" alt="Der Tab Sicherung mit den drei Blöcken Sicherung erstellen, Aus Datei wiederherstellen und Gelöschte Verträge, im letzten ein Vertrag Strom 2023 mit den Schaltflächen Zurückholen und Jetzt vergessen" width="100%"></picture></p>

*Abbildung: Der Tab „Sicherung" mit Mock-Daten vom 12.07.2026. Mehr zum Tab steht unter [Panel-Sicherung](Panel-Sicherung).*

## Sicherung erstellen

1. Öffne im Panel den Tab **Sicherung**.
2. Klicke unter **Sicherung erstellen** auf **Sicherung herunterladen**.
3. Dein Browser speichert die Datei `tariffy-backup-<Datum>.json`. Tariffy meldet „Sicherung heruntergeladen: n Verträge."

> **Wichtig:** Die Datei enthält **persönliche Daten** (Kundennummer, Zählernummer, Marktlokation, Benachrichtigungsziel). Bewahre sie sicher auf und gib sie nicht weiter.

## Aus einer Sicherung wiederherstellen

1. Öffne den Tab **Sicherung** und wähle unter **Aus Datei wiederherstellen** Deine Datei.
2. Tariffy zeigt Dir vorher, was passieren würde: Verträge, die es noch nicht gibt, stehen als „wird angelegt", Verträge, die es schon gibt, als „übersprungen: gibt es schon". Bis hierhin wurde nichts angelegt.
3. Klicke auf **Wiederherstellen (n)** und bestätige mit **Ja, wiederherstellen**.
4. Tariffy meldet „Wiederhergestellt: x angelegt, y übersprungen."

Die Regeln dahinter:

- **Es werden nur fehlende Verträge angelegt.** „Vorhanden" heißt: gleicher **Name** und gleiche **Sparte**. Vorhandene Verträge werden **nie verändert**, auch nicht, wenn sich die Werte unterscheiden.
- Kommt derselbe Vertrag zweimal in der Datei vor, wird er einmal angelegt.
- Die Datei wird streng geprüft: nur bekannte Einstellungen, nur einfache Werte, höchstens 200 Verträge, jeder Text höchstens 2000 Zeichen. Das Panel nimmt Dateien bis 1 MB an („Die Datei ist zu groß." darüber). Ist die Datei kaputt („Das ist keine gültige Tariffy-Sicherung."), wird **nichts** angelegt, auch nicht die gültigen Verträge davor.
- Ein wiederhergestellter Vertrag ist ein **neuer Vertrag** mit neuen Sensoren und Buttons, aber denselben Daten wie vorher.

## Was in der Sicherung ist und was nicht

**In der Sicherung** ist alles, was zum Vertrag gehört:

- der Vertragsname und alle Einstellungen aus dem Vertragsformular, auch Kundennummer, Zählernummer, Marktlokation und Benachrichtigungsziel,
- die Historie, ein eventueller Archiv-Vermerk, Einmalposten, der Abschlagsverlauf und die Außenzähler,
- der geplante Folgevertrag,
- der interne Zustand, zum Beispiel bestätigte Erinnerungen und der eingefrorene Verbrauch der letzten Laufzeit.

**Nicht in der Sicherung** ist alles, was nicht Tariffy gehört:

- die Langzeitstatistiken Deiner Zähler und die Zähler-Sensoren selbst (Du verweist beim Vertrag nur auf ihre Entitäten-ID),
- die Sensoren und Buttons des Vertrags und ihre eigenen Statistiken; sie entstehen beim Wiederherstellen neu,
- Dashboard-Karten und Automationen, die Deine Vertrags-Entitäten verwenden,
- notify-Dienste, auf die das Benachrichtigungsziel zeigt,
- die Liste der gelöschten Verträge (siehe unten).

## Umzug auf eine neue Home-Assistant-Instanz

1. **Alte Instanz:** Lade im Tab **Sicherung** die Sicherung herunter.
2. **Neue Instanz:** Installiere Tariffy (siehe [Erste-Schritte](Erste-Schritte)) und starte Home Assistant neu.
3. Richte auf der neuen Instanz zuerst Deine **Zähler-Sensoren** ein, mit **denselben Entitäten-IDs** wie vorher (zum Beispiel `sensor.zaehler_strom`). Die Sicherung enthält nur die ID, die der Vertrag verwendet. Auch den notify-Dienst für das Benachrichtigungsziel brauchst Du dort wieder.
4. Lege einen **beliebigen Vertrag** an, zum Beispiel einen Platzhalter mit einem anderen Namen. Das Panel gibt es erst, wenn mindestens ein Vertrag existiert; ohne Panel gibt es den Tab **Sicherung** nicht.
5. Öffne im Panel den Tab **Sicherung**, wähle die Datei, prüfe die Vorschau und klicke auf **Wiederherstellen (n)**.
6. Kontrolliere die Verträge im Panel und die neuen Sensoren. Ändere Dashboard-Karten und Automationen auf die neuen Entitäten-IDs.
7. Lösche den Platzhalter-Vertrag. Er bleibt 30 Tage in der Liste der gelöschten Verträge; mit **Jetzt vergessen** entfernst Du ihn sofort.

> **Gut zu wissen:** Weil die Statistiken Deiner Zähler nicht in der Sicherung stehen, hängt Tariffy auf der neuen Instanz von den dortigen Langzeitstatistiken ab. Reichen sie nicht bis zum Vertragsbeginn zurück, trage beim Vertrag im Feld **Zählerstand bei Vertragsbeginn (optional)** einen Wert ein, der hat Vorrang vor den automatischen Methoden (siehe [Verbrauch-Messen](Verbrauch-Messen)).

> **Gut zu wissen:** Heißt auf der neuen Instanz schon ein Sensor so wie ein neuer, hängt Home Assistant an die ID ein `_2` an. Prüfe die IDs in **Einstellungen → Geräte & Dienste → Entitäten**, bevor Du Automationen anpasst (siehe [Automationen](Automationen)).

## Gelöschte Verträge: 30 Tage Zeit

Löschst Du einen Vertrag, im Panel oder in Home Assistant, behält Tariffy eine Kopie für **30 Tage**, höchstens die **letzten 20**. Du findest sie im Tab **Sicherung** unter **Gelöschte Verträge** mit „gelöscht am <Datum>".

![Der Dialog zum endgültigen Löschen eines Vertrags: Zur Bestätigung muss der Name Strom Haus eingetippt werden, darunter die Schaltflächen Endgültig löschen und Abbrechen](https://raw.githubusercontent.com/wiki/weskona/tariffy/images/delete-contract-dialog.png)

*Abbildung: Der Löschen-Dialog mit Mock-Daten: Der Vertragsname muss zur Bestätigung eingetippt werden.*

- **Zurückholen** (mit Rückfrage „<Name> zurückholen?") legt den Vertrag wieder an, mit neuen Sensoren. Das geht nicht, wenn es inzwischen einen Vertrag mit gleichem Namen und gleicher Sparte gibt („Einen Vertrag mit diesem Namen und dieser Sparte gibt es schon.").
- **Jetzt vergessen** (mit Rückfrage) entfernt den Eintrag sofort und endgültig, samt persönlicher Daten.
- Nach 30 Tagen verschwindet ein Eintrag von selbst. Die Kopie liegt im Speicher von Home Assistant (`.storage/tariffy.deleted`).
- Das Löschen scheitert nie an der Kopie: Lässt sie sich nicht anlegen, wird der Vertrag trotzdem gelöscht.

> **Gut zu wissen:** Die Langzeitstatistiken, die Home Assistant schon aufgezeichnet hat, bleiben beim Löschen in der Datenbank, die Sensoren und Buttons des Vertrags werden entfernt. Wer nur ablegen will, ohne zu löschen, nimmt besser das Archiv (siehe [Archiv-und-Historie](Archiv-und-Historie)).

## Beispiel mit Zahlen

Beispiel (nach den Tests der Integration): Du hast die Verträge „Strom Haus" (Abschlag 40 €) und „Wasser" und lädst die Sicherung herunter. Danach löschst Du „Wasser" und änderst bei „Strom Haus" den Abschlag auf 99 €.

1. Du wählst die Datei. Die Vorschau zeigt: „Strom Haus", übersprungen (gibt es schon); „Wasser", wird angelegt.
2. Nach **Wiederherstellen (1)** meldet Tariffy: „Wiederhergestellt: 1 angelegt, 1 übersprungen."
3. „Wasser" ist mit seinen alten Daten zurück, mit neuen Sensoren. „Strom Haus" hat weiter den Abschlag 99 €, die Sicherung hat ihn nicht überschrieben.
4. Eine zweite Wiederherstellung mit derselben Datei legt nichts mehr an: 0 angelegt, 2 übersprungen.

## Siehe auch

- [Panel-Sicherung](Panel-Sicherung): Der Tab Sicherung im Panel
- [Archiv-und-Historie](Archiv-und-Historie): Verträge archivieren statt löschen
- [Vertraege-Anlegen](Vertraege-Anlegen): Einen Vertrag neu anlegen
- [Verbrauch-Messen](Verbrauch-Messen): Zähler, Statistiken und Zählerstand bei Vertragsbeginn
- [Erste-Schritte](Erste-Schritte): Tariffy installieren und den ersten Vertrag anlegen
- [Fehlerbehebung](Fehlerbehebung): Wenn etwas nicht klappt
