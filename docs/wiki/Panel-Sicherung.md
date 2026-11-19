🇩🇪 Deutsch · [🇬🇧 English](EN-Panel-Backup)

# Panel: Sicherung

Der Tab **Sicherung** ist nur für Administratoren sichtbar. Er hat drei Bereiche: eine Sicherung nur für Tariffy herunterladen, aus einer Sicherungsdatei wiederherstellen und **gelöschte Verträge der letzten 30 Tage zurückholen**.

**Inhalt:**
- [Die drei Bereiche](#die-drei-bereiche)
- [Sicherung herunterladen](#sicherung-herunterladen)
- [Aus Datei wiederherstellen](#aus-datei-wiederherstellen)
- [Gelöschte Verträge](#gelöschte-verträge)
- [Beispiel: Strom 2023 zurückholen](#beispiel-strom-2023-zurückholen)
- [Grenzen](#grenzen)
- [Auf dem Handy](#auf-dem-handy)
- [Siehe auch](#siehe-auch)

## Die drei Bereiche

Die normalen Backups von Home Assistant sichern Tariffy schon vollständig mit. Der Tab ergänzt das um eine Sicherung nur für Tariffy (mehr dazu in [Sicherung-und-Umzug](Sicherung-und-Umzug)).

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/desktop-backup.png"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/desktop-backup-light.png" alt="Tab Sicherung mit den Bereichen Sicherung erstellen mit dem Button Sicherung herunterladen, Aus Datei wiederherstellen mit der Dateiauswahl und Gelöschte Verträge mit dem Eintrag Strom 2023 und den Buttons Zurückholen und Jetzt vergessen" width="100%"></picture></p>

*Abbildung: Der Tab Sicherung (Beispieldaten vom 12.07.2026). Das Feld „Choose File" kommt vom Browser und ist in der Sprache des Browsers beschriftet.*

| Bereich | Button | Zweck |
|---|---|---|
| **Sicherung erstellen** | **Sicherung herunterladen** | Speichert alle Verträge in einer Datei. |
| **Aus Datei wiederherstellen** | Dateiauswahl, dann **Wiederherstellen (n)** | Legt fehlende Verträge aus einer Sicherungsdatei an. |
| **Gelöschte Verträge** | **Zurückholen**, **Jetzt vergessen** | Holt einen gelöschten Vertrag zurück oder vergisst ihn sofort. |

## Sicherung herunterladen

Der Button **Sicherung herunterladen** speichert alle Verträge in einer Datei `tariffy-backup-<Datum>.json`: Vertragsdaten, Historie, archivierte Verträge, geplanten Folgevertrag und den internen Zustand (zum Beispiel bestätigte Erinnerungen). Danach meldet das Panel „Sicherung heruntergeladen: n Verträge."

> **Gut zu wissen:** **Die Datei enthält persönliche Daten** (Kundennummer, Zählernummer, Marktlokations-ID, Benachrichtigungsziel). Bewahre sie sicher auf und gib sie nicht weiter.

## Aus Datei wiederherstellen

1. Du wählst die Sicherungsdatei.
2. Das Panel zeigt Dir, was passieren würde: Verträge, die es noch nicht gibt, werden **angelegt** („wird angelegt"), Verträge mit gleichem Namen und gleicher Sparte werden **übersprungen** („übersprungen: gibt es schon") und nie verändert. Gibt es nichts anzulegen, steht „Nichts wiederherzustellen: die Verträge dieser Datei gibt es schon."
3. Mit **Wiederherstellen (n)** und einer Rückfrage („n fehlende(n) Vertrag/Verträge aus dieser Datei anlegen? Vorhandene Verträge werden nicht verändert." mit **Ja, wiederherstellen**) werden die fehlenden Verträge angelegt. Danach steht „Wiederhergestellt: n angelegt, m übersprungen."

- Die Datei wird streng geprüft (nur bekannte Einstellungen, nur einfache Werte, höchstens 1 MB und 200 Verträge); eine kaputte Datei legt nichts an. Das Panel meldet dann „Das ist keine gültige Tariffy-Sicherung." oder, bei einer zu großen Datei, „Die Datei ist zu groß."
- Wiederhergestellte Verträge sind **neue Verträge mit neuen Sensoren**; die Statistiken des alten Vertrags bleiben bei dessen Sensoren in Home Assistant.

## Gelöschte Verträge

Wird ein Vertrag gelöscht (im Panel oder in Home Assistant), merkt sich Tariffy ihn **30 Tage lang** (höchstens die letzten 20) und bietet ihn hier an. Jeder Eintrag zeigt Name, Sparte und das Löschdatum („Strom · gelöscht am 01.07.2026").

- **Zurückholen** legt den Vertrag wieder an, nach einer Rückfrage („Strom 2023" zurückholen?, **Ja, zurückholen**). Das geht nicht, wenn es inzwischen einen Vertrag mit gleichem Namen und gleicher Sparte gibt („Einen Vertrag mit diesem Namen und dieser Sparte gibt es schon.").
- **Jetzt vergessen** entfernt einen Eintrag sofort, auch seine persönlichen Daten, nach einer Rückfrage („endgültig vergessen? Danach lässt er sich nicht mehr zurückholen.", **Ja, vergessen**).
- Die Daten liegen in Home Assistants Speicher (`.storage/tariffy.deleted`) und werden nach 30 Tagen entfernt.
- Gibt es nichts zurückzuholen, steht „Keine gelöschten Verträge."

## Beispiel: Strom 2023 zurückholen

In den Beispieldaten wurde der Vertrag **Strom 2023** (Sparte Strom) am 01.07.2026 gelöscht. Heute ist der 12.07.2026, er ist also elf Tage alt und noch zurückzuholen.

1. Tab **Sicherung** öffnen, Bereich **Gelöschte Verträge**.
2. Bei „Strom 2023" auf **Zurückholen** klicken.
3. Die Rückfrage mit **Ja, zurückholen** beantworten.
4. Oben auf der Seite erscheint die Meldung `„Strom 2023“ ist wieder da.` in Grün, und der Vertrag steht wieder in der Übersicht.

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/desktop-backup-actions.png" alt="Tab Sicherung nach dem Zurückholen: oben in Grün die Meldung Strom 2023 ist wieder da, darunter unverändert die drei Bereiche" width="100%"></p>

*Abbildung: Die grüne Meldung oben bestätigt das Zurückholen.*

Wäre der Vertrag länger als 30 Tage gelöscht, wäre der Eintrag schon verschwunden.

## Grenzen

- **Das Panel gibt es erst, wenn mindestens ein Vertrag existiert.** Wurde der letzte Vertrag gelöscht, legst Du zuerst irgendeinen neuen Vertrag an (Einstellungen → Geräte & Dienste → Tariffy → Hinzufügen), dann steht das Panel wieder zur Verfügung, und Du kannst den gelöschten Vertrag im Tab Sicherung zurückholen.
- Nicht-Administratoren sehen den Tab nicht, und das Backend lehnt die Aktionen auch über die Schnittstelle ab ([Panel-Rechte-und-Design](Panel-Rechte-und-Design)).
- Die Sicherungsdatei ersetzt kein Backup von Home Assistant: Sie enthält die Verträge, aber nicht die Langzeit-Statistiken.

## Auf dem Handy

Auf dem Handy stehen die drei Bereiche untereinander.

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-backup.png"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-backup-light.png" alt="Tab Sicherung auf dem Handy: die drei Bereiche untereinander" width="300"></picture></p>

*Abbildung: Der Tab Sicherung auf dem Handy.*

## Siehe auch

- [Sicherung-und-Umzug](Sicherung-und-Umzug): Sicherung, Umzug auf eine andere Installation, Wiederherstellung im Zusammenhang.
- [Panel-Vertraege](Panel-Vertraege): Vertrag löschen.
- [Panel-Historie](Panel-Historie): archivierte Verträge zurückholen.
- [Panel-Rechte-und-Design](Panel-Rechte-und-Design): wer den Tab sieht.
