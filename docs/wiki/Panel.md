# Panel (Beta)

Das **Tariffy-Panel** ist eine eigene Seite in der Seitenleiste von Home Assistant. Es zeigt alle Verträge auf einen Blick und lässt Administratoren Verträge direkt dort pflegen. Es ersetzt keine Funktion der Integration: Gespeichert wird immer über die vorhandenen Dialoge von Home Assistant, die Sensoren und Buttons bleiben unverändert.

> **Beta:** Das Panel gibt es seit `1.27.0-beta.1` und nur in Beta-Versionen. Die stabile Version (`1.26.x`) enthält es nicht. Wer keine Beta installiert hat, merkt nichts davon.

Screenshots: [docs/panel-preview](https://github.com/weskona/tariffy/tree/beta/docs/panel-preview)

## Beta installieren

1. HACS → Tariffy → ⋮ → **Neu herunterladen**, **Beta-Versionen anzeigen** einschalten.
2. Eine Version wie `1.27.0-beta.6` wählen und Home Assistant neu starten.
3. Browserseite einmal **hart neu laden** (Strg+F5, am Handy: Seite neu laden oder App-Cache leeren), damit die neue Panel-Datei geladen wird.

Zurück zur stabilen Version: in HACS wieder eine `1.26.x` wählen. Die Vertragsdaten ändern sich dadurch nicht.

## Öffnen

In der Seitenleiste erscheint der Eintrag **Tariffy** (Symbol `mdi:cash-multiple`), sobald mindestens ein Vertrag geladen ist. Das Panel sehen alle Benutzer. Wer ihn nicht in der Seitenleiste möchte, kann ihn im eigenen Profil ausblenden.

Das Panel folgt der Sprache von Home Assistant (Deutsch, sonst Englisch) und passt sich der Breite an: Auf dem Handy werden die Karten zu aufklappbaren Zeilen.

## Die drei Ansichten

| Ansicht | Inhalt |
|---|---|
| **Übersicht** | Oben die Summe der Abschläge pro Monat, die Prognose zum Vertragsende (nur Verträge mit Verbrauchsmessung) und der nächste Termin (Kündigungsfrist, Vertragsende oder Wechsel). Darunter zwei Gruppen mit je einer Karte pro Vertrag: **Verbrauchsverträge** (Strom, Gas, Wasser) und **Pauschalverträge** (Internet, Mobilfunk, Versicherung, Sonstiges). Die Karten sind nach dem Zustand getönt (grün Guthaben, rot Nachzahlung, orange Kündigung fällig). Eine Verbrauchskarte zeigt die Prognose zum Vertragsende als große Zahl neben dem Laufzeit-Ring, höchstens drei Zahlen (Kosten bisher, Saldo bisher, Verbrauch), die gezahlten Abschläge gegen die Kosten, die Restlaufzeit und Hinweise. Eine Pauschalkarte zeigt den Abschlag pro Monat, die Kosten bisher und das Vertragsende samt Laufzeit-Balken, ohne Ring und ohne Verbrauch. In der Übersicht gibt es keine Bearbeitungs-Aktionen. |
| **Kosten** | Zwei Tabellen wie in der Übersicht. **Verbrauchsverträge:** Kosten bisher, Saldo bisher, Saldo zum Vertragsende, Abschlag und empfohlener Abschlag. **Pauschalverträge:** Kosten bisher (die bis heute fälligen Abschläge), Abschlag, Vertragsende und Restlaufzeit; Saldo und Prognose gibt es dort nicht. Jede Tabelle hat eine Summenzeile, darunter steht die Gesamtsumme. |
| **Verträge** | In denselben zwei Gruppen pro Vertrag aufklappbare Details: Vertragsdaten, Preise, Verbrauch, Empfehlungen. Hier stehen auch **alle Aktionen, die einen Vertrag ändern**, als Symbole in jeder Zeile (Kalender: Folgevertrag planen oder bearbeiten, Stift: Vertrag bearbeiten) und oben der Button **Neuer Vertrag** (nur Administratoren). |

Vorzeichen: **Plus** ist Guthaben, **Minus** ist Nachzahlung. „Zum Vertragsende" ist aus dem bisherigen Verbrauch hochgerechnet. Deckt ein Guthaben die Kosten bis zum Vertragsende schon ab, steht beim empfohlenen Abschlag „0,00 €" mit dem Hinweis „Guthaben deckt die Kosten", nie ein negativer Betrag. Alle Werte sind dieselben wie bei den Sensoren und aktualisieren sich von selbst.

## Wer sieht und darf was

- **Alle Benutzer** sehen die Verträge, aber nur ausgewählte Werte. Kundennummer, Zählernummern, Marktlokations-ID, Benachrichtigungs-Ziel und interne Markierungen werden **nicht** ans Panel geschickt.
- **Nur Administratoren** sehen die Buttons und Dialoge zum Bestätigen, Bearbeiten, Anlegen und Löschen. Das prüft zusätzlich das Backend: Ein Nicht-Administrator kann die Aktionen auch über die Schnittstelle nicht auslösen.

## Bestätigen

Planen, Bearbeiten, Anlegen und Löschen findest du im Tab **Verträge** (Symbole in der Zeile, Button oben). Auf der Karte in der Übersicht erscheinen nur je nach Lage, direkt bei dem Hinweis, zu dem sie gehören:

- **Warnung bestätigen**: quittiert die Abschlag-Warnung (wie der Button „Abschlag-Warnung bestätigen"). Der Button erscheint nur, wenn die Warnung in den Vertragsdaten eingeschaltet ist und die Prognose die Schwelle unterschreitet.
- **Kündigung bestätigen**: quittiert die Kündigungs-Erinnerung (wie der Button „Kündigung bestätigen").

Beide fragen **ein zweites Mal** nach („Ja, bestätigen" / „Abbrechen"), damit nichts aus Versehen ausgelöst wird.

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
| Kein Eintrag „Tariffy" in der Seitenleiste | Nur Beta-Versionen haben das Panel. Version in HACS prüfen, Home Assistant neu starten, Seite hart neu laden. Im Profil prüfen, ob der Eintrag ausgeblendet ist. Im Log nach Meldungen „Tariffy: panel" suchen: Das Panel kann ausfallen, ohne die Verträge zu stören. |
| Panel zeigt alte Oberfläche oder fehlende Buttons | Seite hart neu laden, der Browser hat die alte Datei zwischengespeichert. |
| Keine Buttons zu sehen | Die Aktionen gibt es nur für Administratoren. |
| „Das Formular konnte nicht geladen werden" | Home Assistant war kurz nicht erreichbar oder der Vertrag ist gerade nicht geladen. Dialog schließen und neu öffnen. |
| Einen Fehler melden | Mit dem [Fehlerformular](https://github.com/weskona/tariffy/issues/new/choose) und der genauen Beta-Version. |

## Was das Panel nicht tut

- Es rechnet nichts selbst, sondern zeigt die Werte der Integration.
- Es schreibt nur über die Dialoge von Home Assistant. Diese bleiben unter Einstellungen → Integrationen → Tariffy unverändert verfügbar.
- Es gibt keine Funktion „Jetzt wechseln" (siehe oben).
