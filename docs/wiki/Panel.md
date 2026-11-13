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
| **Kosten** | Oben die **Kostenaufteilung**: ein Ringdiagramm mit dem Anteil jedes Vertrags (umschaltbar zwischen **Kosten bisher** und **Pro Jahr**; die **Jahresauswahl** zeigt die Kosten eines Kalenderjahres für alle Jahre mit Daten, auch aus der Historie und von archivierten Verträgen, wobei eine Laufzeit über mehrere Jahre anteilig nach Tagen zählt) und ein Balken für die Aufteilung zwischen Verbrauchs- und Pauschalverträgen. Darunter zwei Tabellen wie in der Übersicht. **Verbrauchsverträge:** Kosten bisher, Saldo heute, Saldo zum Vertragsende, Abschlag und empfohlener Abschlag. **Pauschalverträge:** Kosten bisher (die bis heute fälligen Abschläge), Restlaufzeit, Vertragsende und Abschlag; Saldo und Prognose gibt es dort nicht. Beide Tabellen haben dasselbe Spaltenraster, „Kosten bisher“ und „Abschlag“ stehen also untereinander. Jede Tabelle hat eine Summenzeile, darunter steht die Gesamtsumme. |
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

## Pauschalvertrag verlängern

Bei Verträgen ohne Verbrauch (Versicherung, Internet, Mobilfunk, Sonstiges), die ein **Vertragsende** haben, steht in jeder Zeile des Tabs **Verträge** ein Symbol **Vertrag verlängern** (zwei Pfeile im Kreis, nur Administratoren). Der Dialog schlägt vor: Beginn am Tag nach dem bisherigen Ende, neues Ende ein Jahr später, Zahlweise und Betrag wie bisher. Du trägst zum Beispiel den neuen Beitrag ein, und der Dialog zeigt sofort, um wie viel Prozent der Vertrag teurer oder günstiger wird (verglichen pro Monat). Mit **Verlängern** passiert Folgendes:

- Die bisherige Laufzeit kommt in die **Historie** (Zeitraum, Anbieter, Tarif, Abschlag, gezahlte Abschläge). So entsteht pro Jahr ein Eintrag und man sieht, wie der Beitrag steigt.
- Der Vertrag läuft mit dem neuen Beginn, Ende und Betrag weiter. Anbieter, Tarif, Kundennummer und alles andere bleiben.
- Bestätigte Kündigungs-Erinnerungen und der Zeitpunkt einer früheren Abschlagsänderung gelten nur für die alte Laufzeit und beginnen neu; die Erinnerung richtet sich nach dem neuen Ende.

Verbrauchsverträge (Strom, Gas, Wasser) haben dafür den **Folgevertrag**, der am geplanten Datum von selbst übernimmt. Erhöhungen mitten in der Laufzeit trägst du über **Vertrag bearbeiten** ein (der neue Abschlag gilt ab dem Tag des Speicherns).

## Kosten bisher bei Pauschalverträgen

Bei Pauschalverträgen (Internet, Mobilfunk, Versicherung, Abos, ...) sind die **Kosten bisher** die **gebuchten Raten**: Bei monatlicher Zahlung zählt die Rate eines Monats **ab dem ersten Tag dieses Monats**, egal an welchem Tag abgebucht wird (Beginn 1. April, Rate 17,99 €: am 13. November sind es acht Raten = 143,92 €, auch wenn die Abbuchung am 27. ist). Bei quartalsweiser, halbjährlicher und jährlicher Zahlung zählt jede Abbuchung am Tag der Zahlung (mit dem Feld „Erste Abbuchung“ legst du ihren Tag fest). Eine Abschlagsänderung gilt für die Raten ab ihrem Datum.

## Gesamtkosten über alle Laufzeiten

Hat ein Vertrag eine **Historie** (zum Beispiel weil du ihn jährlich **verlängerst** oder weil der Folgevertrag übernommen hat), zeigt Tariffy die **Kosten gesamt** über alle Laufzeiten: die früheren Laufzeiten aus der Historie plus die laufende. Bei Pauschalverträgen ist das eine eigene Kachel auf der Karte, bei Verbrauchsverträgen eine Zeile unter der Restlaufzeit; dazu stehen sie in den Vertragsdetails und im Tab **Historie** unter den früheren Laufzeiten, jeweils mit „seit <Datum> · n Laufzeiten“. Für eine frühere Laufzeit zählen ihre Kosten, wenn es sie gibt, sonst die gezahlten Abschläge. Fehlt bei einer Laufzeit beides, steht „mindestens …“, weil die Summe dann nicht vollständig ist. Bei einem archivierten Vertrag steht seine letzte Laufzeit schon in der Historie und wird nicht doppelt gezählt. Ohne Historie und ohne Einmalposten gibt es keine zusätzliche Anzeige. Einmalposten (siehe unten) fließen in die Kosten gesamt ein.

## Einmalposten (Bonus und Rechnung)

Im Tab **Verträge** hat jeder Vertrag in den Details den Block **Einmalposten** (nur Administratoren können ihn ändern). Dort trägst du einmalige Beträge ein, die nicht zum Abschlag gehören, mit **Bezeichnung**, **Betrag** und **Datum**:

- ein **positiver** Betrag ist eine **Gutschrift**, zum Beispiel ein Wechselbonus,
- ein **negativer** Betrag ist eine **Rechnung**, zum Beispiel das Honorar eines Maklers, der sich um die Verträge kümmert.

Ein Posten zählt ab seinem Datum (ohne Datum sofort). Er verändert den **Saldo bisher** (der Posten gehört zur Laufzeit, in der sein Datum liegt) und die **Kosten gesamt** über alle Laufzeiten: ein Bonus senkt die Kosten, eine Rechnung erhöht sie. **Prognose zum Vertragsende und die Warnung bei zu niedrigem Abschlag hängen weiter nur vom Verbrauch ab.** Die Einmalposten gelten für jede Art von Vertrag, bleiben beim Verlängern und beim Tarifwechsel erhalten und stehen in der Sicherung. Das Feld **Neukundenbonus** im Vertragsformular bleibt wie es war und wird nur angezeigt.

## Folgevertrag planen

**Folgevertrag planen** (bzw. **Folgevertrag bearbeiten**, wenn schon einer eingetragen ist) öffnet dasselbe Formular wie „Konfigurieren" in Home Assistant. Felder, die du leer lässt, behalten den aktuellen Wert. Zum Wechseldatum übernimmt Home Assistant den Folgevertrag von selbst (siehe [Tarifwechsel und Erinnerungen](Tarifwechsel-und-Erinnerungen)).

- Ist eine Kündigungs-Erinnerung fällig, gibt es das Häkchen **Kündigung als erledigt markieren** (standardmäßig an). Es bestätigt die Kündigung im selben Schritt, in dem du den Folgevertrag speicherst.
- **Geplanten Vertrag entfernen** löscht nur den Plan, nicht den aktuellen Vertrag. Es fragt vorher nach.
- Einen Wechsel „jetzt" gibt es im Panel absichtlich nicht: Er würde den aktuellen Vertrag sofort ersetzen, obwohl der neue erst am geplanten Datum beginnt. Der Wechsel passiert zum Datum automatisch.

## Vertrag bearbeiten

**Vertrag bearbeiten** zeigt die zwei Formulare von „Neu konfigurieren": erst die allgemeinen Daten, dann die Daten der Sparte. Alles, was die Formulare enthalten, wird durch das ersetzt, was du speicherst. Vor dem Speichern fragt das Panel noch einmal nach.

- Bestätigte Erinnerungen, „Benachrichtigung gesendet" und der eingefrorene Verbrauch der letzten Laufzeit bleiben beim Bearbeiten erhalten. Die Kündigungs-Erinnerung beginnt nur dann neu, wenn sich das Vertragsende oder die Vorlaufzeit ändert.
- Ändert sich der Abschlag, merkt sich Tariffy wie bisher das Änderungsdatum, damit die Berechnung für die Zeit davor mit dem alten Abschlag weiterläuft.
- **Pauschalverträge (Internet, Mobilfunk, Versicherung, Sonstiges):** Im Kosten-Schritt wählst du die **Zahlweise** (monatlich, vierteljährlich, halbjährlich, jährlich) und trägst den **Betrag pro Zahlung** ein, bei einer Versicherung also zum Beispiel den Jahresbeitrag. Tariffy rechnet intern weiter mit dem Betrag pro Monat (600 € jährlich sind 50 € im Monat); bestehende Verträge sind monatlich und bleiben unverändert. Eine Änderung nur der Zahlweise gilt nicht als Preisänderung. Steigt der Beitrag, trägst du den neuen Betrag ein (gilt ab dem Tag des Speicherns) oder verlängerst den Vertrag.
- **Kosten bisher bei Zahlung im Voraus:** Wird nicht monatlich gezahlt (vierteljährlich, halbjährlich, jährlich), zählen die **Abbuchungen**, nicht ein monatlicher Anteil: Eine Versicherung, die kurz nach Beginn mit 896,63 € bezahlt wurde, zeigt 896,63 € bei „Kosten bisher“, nach einem Jahr die zweite Abbuchung dazu. Die erste Abbuchung nimmt Tariffy am **Vertragsbeginn** an; das tatsächliche Datum trägst du im Feld **Erste Abbuchung am** ein, die weiteren folgen im Abstand der Zahlweise. Die Vertragsdetails zeigen die erste und die **nächste Zahlung**. Abbuchungen nach dem Vertragsende gehören schon zur nächsten Laufzeit. Bei monatlicher Zahlweise bleibt alles wie bisher.
- **Der Name** des Vertrags steht als erstes Feld im ersten Schritt und lässt sich ändern (leer lassen = der Name bleibt). Er ändert den Namen des Vertrags und seines Geräts; Sensoren, Entity-IDs und Vertragsdaten bleiben.
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
