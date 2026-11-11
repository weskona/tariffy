# Panel

Das **Tariffy-Panel** ist eine eigene Seite in der Seitenleiste von Home Assistant. Es zeigt alle Verträge auf einen Blick und lässt Administratoren Verträge direkt dort pflegen. Es ersetzt keine Funktion der Integration: Gespeichert wird immer über die vorhandenen Dialoge von Home Assistant, die Sensoren und Buttons bleiben unverändert.

Screenshots: [docs/panel-preview](https://github.com/weskona/tariffy/tree/main/docs/panel-preview)

## Nach dem Update

Das Panel gehört seit `1.27.0` zur Integration, es gibt nichts zu installieren oder einzurichten. Nach dem Update Home Assistant neu starten und die Browserseite einmal **hart neu laden** (Strg+F5, am Handy: Seite neu laden oder App-Cache leeren), damit die neue Panel-Datei geladen wird.

## Öffnen

In der Seitenleiste erscheint der Eintrag **Tariffy** (Symbol `mdi:cash-multiple`), sobald mindestens ein Vertrag geladen ist. Das Panel sehen alle Benutzer. Wer ihn nicht in der Seitenleiste möchte, kann ihn im eigenen Profil ausblenden.

Das Panel folgt der Sprache von Home Assistant (Deutsch, sonst Englisch) und passt sich der Breite an: Auf dem Handy werden die Karten zu aufklappbaren Zeilen.

## Die fünf Ansichten

| Ansicht | Inhalt |
|---|---|
| **Übersicht** | Oben vier Kacheln: die **Abschläge pro Monat** (mit Jahreswert und einem Balken, der Verbrauchs- und Pauschalverträge aufteilt), die **Kosten bisher** (mit den bis heute fälligen Abschlägen und dem Saldo), die **Prognose zum Vertragsende** (mit der Prognose je Vertrag, die schlechteste zuerst; nur Verträge mit Verbrauchsmessung) und die **nächsten Termine** (Kündigungsfrist, Wechsel, Vertragsende). Darunter zwei Gruppen mit je einer Karte pro Vertrag: **Verbrauchsverträge** (Strom, Gas, Wasser) und **Pauschalverträge** (Internet, Mobilfunk, Versicherung, Sonstiges). Die Karten sind nach dem Zustand getönt (grün Guthaben, rot Nachzahlung, orange Kündigung fällig). Eine Verbrauchskarte zeigt die Prognose zum Vertragsende als große Zahl neben dem Laufzeit-Ring, höchstens drei Zahlen (Kosten bisher, Saldo heute, Verbrauch), die gezahlten Abschläge gegen die Kosten, die Restlaufzeit und Hinweise. Zeigen der Saldo heute und die Prognose in verschiedene Richtungen (Rückstand heute, Guthaben zum Vertragsende), steht darunter, warum. Eine Pauschalkarte zeigt den Abschlag pro Monat, die Kosten bisher und das Vertragsende samt Laufzeit-Balken, ohne Ring und ohne Verbrauch. In der Übersicht gibt es keine Bearbeitungs-Aktionen. |
| **Kosten** | Zwei Tabellen wie in der Übersicht. **Verbrauchsverträge:** Kosten bisher, Saldo heute, Saldo zum Vertragsende, Abschlag und empfohlener Abschlag. **Pauschalverträge:** Kosten bisher (die bis heute fälligen Abschläge), Restlaufzeit, Vertragsende und Abschlag; Saldo und Prognose gibt es dort nicht. Beide Tabellen haben dasselbe Spaltenraster, „Kosten bisher“ und „Abschlag“ stehen also untereinander. Jede Tabelle hat eine Summenzeile, darunter steht die Gesamtsumme. |
| **Verträge** | In denselben zwei Gruppen pro Vertrag aufklappbare Details: Vertragsdaten, Preise, Verbrauch, Empfehlungen. Hier stehen auch **alle Aktionen, die einen Vertrag ändern**, als Symbole in jeder Zeile (Kalender: Folgevertrag planen oder bearbeiten, Stift: Vertrag bearbeiten) und oben der Button **Neuer Vertrag** (nur Administratoren). |
| **Historie** | Die **früheren Laufzeiten** jedes Vertrags (Zeitraum, Anbieter, Tarif, Abschlag, Kosten, Verbrauch und Saldo am Ende) und die **archivierten Verträge**. Wer keinen Folgevertrag hatte und keinen Vertrag archiviert hat, sieht hier zunächst nur einen kurzen Hinweis. |
| **Sicherung** | Nur für Administratoren: **Sicherung herunterladen**, **aus Datei wiederherstellen** und die **gelöschten Verträge** der letzten 30 Tage zurückholen (siehe unten). |

Vorzeichen: **Plus** ist Guthaben, **Minus** ist Nachzahlung. „Zum Vertragsende" ist aus dem bisherigen Verbrauch hochgerechnet. Deckt ein Guthaben die Kosten bis zum Vertragsende schon ab, steht beim empfohlenen Abschlag „0,00 €" mit dem Hinweis „Guthaben deckt die Kosten", nie ein negativer Betrag. Alle Werte sind dieselben wie bei den Sensoren und aktualisieren sich von selbst.

## Wer sieht und darf was

- **Alle Benutzer** sehen die Verträge, aber nur ausgewählte Werte. Kundennummer, Zählernummern, Marktlokations-ID, Benachrichtigungs-Ziel und interne Markierungen werden **nicht** ans Panel geschickt.
- **Nur Administratoren** sehen die Buttons und Dialoge zum Bestätigen, Bearbeiten, Anlegen und Löschen. Das prüft zusätzlich das Backend: Ein Nicht-Administrator kann die Aktionen auch über die Schnittstelle nicht auslösen.

## Bestätigen

Die Übersicht ist nur zum Ansehen und hat keine Buttons. Planen, Bearbeiten, Anlegen und Löschen findest du im Tab **Verträge** (Symbole in der Zeile, Button oben). Die beiden Bestätigungen stehen dort in den aufgeklappten Details des Vertrags, je nach Lage; die Karte in der Übersicht zeigt weiter den Hinweis mit dem Grund:

- **Warnung bestätigen**: quittiert die Abschlag-Warnung (wie der Button „Abschlag-Warnung bestätigen"). Der Button erscheint nur, wenn die Warnung in den Vertragsdaten eingeschaltet ist und die Prognose die Schwelle unterschreitet.
- **Kündigung bestätigen**: quittiert die Kündigungs-Erinnerung (wie der Button „Kündigung bestätigen").

Beide fragen **ein zweites Mal** nach („Ja, bestätigen" / „Abbrechen"), damit nichts aus Versehen ausgelöst wird.

## Historie und Archiv

- **Frühere Laufzeiten:** Wenn der Folgevertrag am geplanten Datum übernimmt, überschreibt Tariffy die Vertragsdaten (das war schon immer so). Neu: Die alte Laufzeit wird vorher als Eintrag gesichert, mit Zeitraum, Anbieter, Tarif, Preisen, Abschlag, den Kosten, dem Verbrauch und dem Saldo zum Ende. Sie steht dann im Tab **Historie** unter dem Vertrag. Für Laufzeiten, die schon vorbei sind, gibt es keine Einträge; die Historie beginnt mit dem ersten Wechsel nach dem Update. Es werden höchstens 50 Laufzeiten je Vertrag gespeichert. Kunden- und Zählernummern stehen nicht darin.
- **Alte Verträge von Hand eintragen:** Im Tab **Historie** (nur Administratoren) legt der Button **Alten Vertrag hinzufügen** eine frühere Laufzeit an, zum Beispiel einen Vertrag von vor zwei Jahren, und der Stift in der Zeile bearbeitet sie (dort lässt sie sich auch löschen). Du wählst den Vertrag, zu dem die Laufzeit gehört (Zähler und Sparte kommen von ihm), und trägst Beginn und Ende ein, dazu nach Wunsch Anbieter, Tarif, Arbeitspreis je Einheit, Grundpreis, Abschlag. **Verbrauch, Kosten, gezahlte Abschläge und Saldo werden automatisch ermittelt**, soweit es geht: der Verbrauch aus den Langzeitstatistiken des Zählers von Home Assistant (zwischen Beginn und Ende; gibt es für den Zeitraum keine Statistik, trägst du ihn selbst ein), die Kosten aus Verbrauch, Arbeitspreis und Grundpreis (Gas mit Brennwert und Zustandszahl des Vertrags), die gezahlten Abschläge aus Abschlag und Dauer, der Saldo aus beidem. Bei Pauschalverträgen sind die Kosten die gezahlten Abschläge. Die grau hinterlegten Felder zeigen den berechneten Wert und woher er kommt; **in jedes Feld kannst du selbst einen Wert eintragen**, er hat dann Vorrang und der Rest richtet sich danach. Beim Bearbeiten werden die Werte, die du nicht selbst eingetragen hast, neu berechnet. Der Dialog speichert nichts, bis du auf **Speichern** klickst. Heißt der Tarif im alten Vertrag anders oder waren die Preise andere, trägst du sie einfach ein; Staffelpreise, dynamische Preise und getrennte Preise für Hoch- und Niedertarif werden nicht berechnet (dort trägst du die Kosten selbst ein).
- **Archivieren:** Ein Vertrag, dessen Ende vorbei ist und für den kein Folgevertrag geplant ist, bekommt in der Übersicht das Badge **Abgelaufen** und den Hinweis, dass er sich archivieren lässt. Im Tab **Verträge** steht in den Details der Button **Archivieren** (mit Rückfrage, nur Administratoren). Danach verschwindet der Vertrag aus Übersicht, Kosten und Verträgen und aus den Summen, steht in der **Historie**, und seine Erinnerungen und Warnungen sind aus. Es wird nichts gelöscht: Die Sensoren und ihre Statistik bleiben, der Vertrag lässt sich in der Historie mit **Zurückholen** wieder in die Übersicht holen. Nichts wird von allein archiviert.

## Sicherung und Wiederherstellung

Die normalen Backups von Home Assistant sichern Tariffy schon vollständig mit. Der Tab **Sicherung** (nur Administratoren) ergänzt das um eine Sicherung nur für Tariffy:

- **Sicherung herunterladen:** Speichert alle Verträge in einer Datei `tariffy-backup-<Datum>.json`: Vertragsdaten, Historie, archivierte Verträge, geplanten Folgevertrag und den internen Zustand (zum Beispiel bestätigte Erinnerungen). **Die Datei enthält persönliche Daten** (Kundennummer, Zählernummer, Marktlokations-ID, Benachrichtigungsziel). Bewahre sie sicher auf und gib sie nicht weiter.
- **Aus Datei wiederherstellen:** Du wählst die Datei und siehst zuerst, was passieren würde: Verträge, die es noch nicht gibt, werden **angelegt**, Verträge mit gleichem Namen und gleicher Sparte werden **übersprungen** und nie verändert. Erst nach einer Rückfrage wird angelegt. Die Datei wird streng geprüft (nur bekannte Einstellungen, nur einfache Werte, höchstens 1 MB und 200 Verträge); eine kaputte Datei legt nichts an. Wiederhergestellte Verträge sind neue Verträge mit neuen Sensoren; Statistiken des alten Vertrags bleiben bei dessen Sensoren in Home Assistant.
- **Gelöschte Verträge:** Wird ein Vertrag gelöscht (im Panel oder in Home Assistant), merkt sich Tariffy ihn **30 Tage lang** (höchstens die letzten 20) und bietet ihn im Tab **Sicherung** zum **Zurückholen** an, mit Rückfrage. Das geht nicht, wenn es inzwischen einen Vertrag mit gleichem Namen und gleicher Sparte gibt. Die Daten liegen in Home Assistants Speicher (`.storage/tariffy.deleted`) und werden nach 30 Tagen entfernt; mit **Jetzt vergessen** (mit Rückfrage) verschwindet ein Eintrag sofort, auch seine persönlichen Daten.
- **Grenze:** Das Panel gibt es erst, wenn mindestens ein Vertrag existiert. Wurde der letzte Vertrag gelöscht, legst du zuerst irgendeinen neuen Vertrag an, dann steht das Panel wieder zur Verfügung.

## Folgevertrag planen

**Folgevertrag planen** (bzw. **Folgevertrag bearbeiten**, wenn schon einer eingetragen ist) öffnet dasselbe Formular wie „Konfigurieren" in Home Assistant. Felder, die du leer lässt, behalten den aktuellen Wert. Zum Wechseldatum übernimmt Home Assistant den Folgevertrag von selbst (siehe [Tarifwechsel und Erinnerungen](Tarifwechsel-und-Erinnerungen)).

- Ist eine Kündigungs-Erinnerung fällig, gibt es das Häkchen **Kündigung als erledigt markieren** (standardmäßig an). Es bestätigt die Kündigung im selben Schritt, in dem du den Folgevertrag speicherst.
- **Geplanten Vertrag entfernen** löscht nur den Plan, nicht den aktuellen Vertrag. Es fragt vorher nach.
- Einen Wechsel „jetzt" gibt es im Panel absichtlich nicht: Er würde den aktuellen Vertrag sofort ersetzen, obwohl der neue erst am geplanten Datum beginnt. Der Wechsel passiert zum Datum automatisch.

## Vertrag bearbeiten

**Vertrag bearbeiten** zeigt die zwei Formulare von „Neu konfigurieren": erst die allgemeinen Daten, dann die Daten der Sparte. Alles, was die Formulare enthalten, wird durch das ersetzt, was du speicherst. Vor dem Speichern fragt das Panel noch einmal nach.

- Bestätigte Erinnerungen, „Benachrichtigung gesendet" und der eingefrorene Verbrauch der letzten Laufzeit bleiben beim Bearbeiten erhalten. Die Kündigungs-Erinnerung beginnt nur dann neu, wenn sich das Vertragsende oder die Vorlaufzeit ändert.
- Ändert sich der Abschlag, merkt sich Tariffy wie bisher das Änderungsdatum, damit die Berechnung für die Zeit davor mit dem alten Abschlag weiterläuft.
- Ein leeres optionales Feld entfernt den Wert.

## Neuer Vertrag

**Neuer Vertrag** (oben im Tab Verträge) startet den Einrichtungs-Dialog von Home Assistant: erst Bezeichnung, Sparte und Anbieter, dann die Daten der Sparte. Der Vertrag erscheint danach von selbst im Panel. Die Felder sind dieselben wie bei der Einrichtung unter Einstellungen → Integrationen, siehe [Konfiguration](Konfiguration).

## Vertrag löschen

**Vertrag löschen** steht im Bearbeiten-Dialog. Weil das nicht rückgängig zu machen ist, wird der Button **Endgültig löschen** erst aktiv, wenn du den **Namen des Vertrags** eintippst.

- Sensoren, Buttons und Gerät des Vertrags werden entfernt, ebenso offene Benachrichtigungen zu Kündigung und Abschlag.
- Die **Langzeit-Statistiken**, die Home Assistant schon aufgezeichnet hat, bleiben in der Datenbank. Sie lassen sich in den Entwicklerwerkzeugen unter Statistiken entfernen.
- Löschst du den **letzten** Vertrag, verschwindet das Panel aus der Seitenleiste. Einen neuen Vertrag legst du dann unter Einstellungen → Integrationen → Tariffy → Hinzufügen an.

## Fehlerbehebung

| Problem | Lösung |
|---|---|
| Kein Eintrag „Tariffy" in der Seitenleiste | Version in HACS prüfen (ab 1.27.0 gibt es das Panel), Home Assistant neu starten, Seite hart neu laden. Im Profil prüfen, ob der Eintrag ausgeblendet ist. Im Log nach Meldungen „Tariffy: panel" suchen: Das Panel kann ausfallen, ohne die Verträge zu stören. |
| Panel zeigt alte Oberfläche oder fehlende Buttons | Seite hart neu laden, der Browser hat die alte Datei zwischengespeichert. |
| Keine Buttons zu sehen | Die Aktionen gibt es nur für Administratoren. |
| „Das Formular konnte nicht geladen werden" | Home Assistant war kurz nicht erreichbar oder der Vertrag ist gerade nicht geladen. Dialog schließen und neu öffnen. |
| Einen Fehler melden | Mit dem [Fehlerformular](https://github.com/weskona/tariffy/issues/new/choose) und der genauen Version. |

## Was das Panel nicht tut

- Es rechnet nichts selbst, sondern zeigt die Werte der Integration.
- Es schreibt nur über die Dialoge von Home Assistant. Diese bleiben unter Einstellungen → Integrationen → Tariffy unverändert verfügbar.
- Es gibt keine Funktion „Jetzt wechseln" (siehe oben).
