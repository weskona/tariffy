# Changelog

Alle nennenswerten Änderungen an Tariffy werden in dieser Datei festgehalten.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.1.0/),
das Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

## [Unreleased]

## [1.27.0-rc.6] - 2026-11-07

Sechster Release Candidate zum Testen des Seitenleisten-Panels. Bitte melde Probleme mit dem Bug-Formular und nenne diese genaue Version.

### Changed

- Das Status-Badge ("Guthaben", "Nachzahlung", "Nachzahlung droht") steht immer ganz rechts; weitere Badges ("Wechsel am ...", "Jetzt kündigen") stehen links daneben, damit der Status auf jeder Karte an derselben Stelle sitzt.
- Die Badges stehen auch in der Vertragsliste rechts: auf dem Handy neben dem Namen statt links in einer eigenen Zeile, und auf den Karten der Übersicht auf dem Handy rechtsbündig.

## [1.27.0-rc.5] - 2026-11-07

Fünfter Release Candidate zum Testen des Seitenleisten-Panels. Bitte melde Probleme mit dem Bug-Formular und nenne diese genaue Version.

### Changed

- Die zweite Zeile eines Vertrags im Panel zeigt nur noch Anbieter und Tarif. Die Sparte ("Strom", "Gas", ...) steht dort nicht mehr doppelt, das Symbol zeigt sie und der Name sagt es oft ohnehin.

## [1.27.0-rc.4] - 2026-11-07

Vierter Release Candidate zum Testen des Seitenleisten-Panels. Bitte melde Probleme mit dem Bug-Formular und nenne diese genaue Version.

### Changed

- Die Übersichtskarte erklärt, warum der Saldo heute und die Prognose auseinanderliegen (zum Beispiel "Heute 84,36 € im Rückstand, bis Vertragsende durch den Abschlag ausgeglichen."). Aus "Saldo bisher" wird im Panel "Saldo heute".

## [1.27.0-rc.3] - 2026-11-07

Dritter Release Candidate zum Testen des Seitenleisten-Panels. Bitte melde Probleme mit dem Bug-Formular und nenne diese genaue Version.

### Changed

- Die Badges einer Vertragskarte in der Übersicht ("Guthaben", "Wechsel am ...", ...) stehen oben rechts neben dem Namen, statt in einer eigenen Zeile darunter. Auf dem Handy bleibt die Karte unverändert.
- Die "Restlaufzeit" steht direkt unter den Kosten-Balken statt am unteren Rand der Karte, damit keine Lücke entsteht, wenn die Nachbarkarte höher ist.

## [1.27.0-rc.2] - 2026-11-06

Zweiter Release Candidate zum Testen des Seitenleisten-Panels. Das Panel nutzt die ganze Breite des Fensters, die Kopfzeile der Übersicht hat mehr Details, und die Kostentabellen stehen untereinander ausgerichtet. Bitte melde Probleme mit dem Bug-Formular und nenne diese genaue Version.

### Changed

- Die Kopfzeile der Übersicht hat vier Kacheln mit Details: die Abschläge pro Monat (mit Jahreswert und einem Balken, der Verbrauchs- und Pauschalverträge aufteilt), die Kosten bisher (mit den bis heute fälligen Abschlägen und dem Saldo), die Prognose zum Vertragsende (je Vertrag, die schlechteste zuerst) und die nächsten drei Termine.
- Die beiden Tabellen der Ansicht "Kosten" und die Gesamtzeile haben dasselbe Spaltenraster: "Kosten bisher" und "Abschlag" stehen untereinander, auch in der Gesamtzeile (Pauschal-Tabelle: Kosten bisher, Restlaufzeit, Vertragsende, Abschlag).
- Das Panel nutzt die ganze Breite des Fensters, statt bei 1280 px abgeschnitten und zentriert zu sein (die Grenze liegt jetzt bei 2400 px, nur für Ultrabreit-Monitore). Die Übersicht behält drei Verträge pro Zeile und bekommt bei einem sehr breiten Fenster (ab 1750 px) eine vierte Spalte.

## [1.27.0-rc.1] - 2026-11-06

Gleicher Inhalt wie 1.27.0-beta.10, unter neuem Namen noch einmal veröffentlicht: GitHub listet `beta.10` zwischen `beta.2` und `beta.1`, deshalb hat HACS es nicht angeboten. Bitte diese Version installieren (siehe "Beta-Versionen" in der Dokumentation; die Zählung geht jetzt mit `rc.2`, `rc.3`, ... weiter). Bitte melde Probleme mit dem Bug-Formular und nenne diese genaue Version.

### Changed

- Die Ansicht "Kosten" hat zwei Tabellen wie die Übersicht: **Verbrauchsverträge** (Kosten bisher, Saldo bisher, Saldo zum Vertragsende, Abschlag, empfohlener Abschlag) und **Pauschalverträge** (Kosten bisher, Abschlag, Vertragsende, Restlaufzeit), jede mit eigener Summenzeile und darunter die Gesamtsumme. Die Ansicht "Verträge" listet die Verträge in denselben zwei Gruppen.
- Auf einem breiten Bildschirm zeigt die Übersicht in beiden Gruppen drei Verträge pro Zeile. Der kleine Pfeil zum Aufklappen einer Zeile oder Karte ist jetzt ein Symbol im Stil der anderen Symbole und dreht sich beim Aufklappen.
- Release-Ablauf: Die Versionsnummern von Vorabversionen enden pro Serie bei 9 (`beta.1` ... `beta.9`, `rc.1` ... `rc.9`), weil GitHub Release-Tags als Text sortiert und HACS `beta.10` nicht anbieten würde. Ein Test prüft das.

## [1.27.0-beta.10] - 2026-11-06

Zehnte Beta zum Testen des Seitenleisten-Panels. Die Ansichten "Kosten" und "Verträge" sind jetzt wie die Übersicht getrennt. Bitte melde Probleme mit dem Bug-Formular und nenne diese genaue Version.

### Changed

- Beta: Die Ansicht "Kosten" hat zwei Tabellen wie die Übersicht: **Verbrauchsverträge** (Kosten bisher, Saldo bisher, Saldo zum Vertragsende, Abschlag, empfohlener Abschlag) und **Pauschalverträge** (Kosten bisher, Abschlag, Vertragsende, Restlaufzeit). Jede Tabelle hat eine eigene Summenzeile, darunter steht die Gesamtsumme. Pauschalverträge zeigen keine Zeilen voller Striche für Saldo und Prognose mehr.
- Beta: Die Ansicht "Verträge" listet die Verträge in denselben zwei Gruppen.
- Beta: Der kleine Pfeil zum Aufklappen einer Zeile oder Karte ist jetzt ein Symbol im Stil der anderen Symbole und dreht sich beim Aufklappen.
- Beta: Auf einem breiten Bildschirm zeigt die Übersicht in beiden Gruppen drei Verträge pro Zeile (vorher zwei Spalten bei vier Verbrauchsverträgen).

## [1.27.0-beta.9] - 2026-11-06

Neunte Beta zum Testen des Seitenleisten-Panels. Die Übersicht ist nach Vertragsart sortiert, Pauschalverträge bekommen eigene Karten, und alles, was einen Vertrag ändert, ist in den Tab "Verträge" gewandert. Bitte melde Probleme mit dem Bug-Formular und nenne diese genaue Version.

### Changed

- Beta: Die Übersicht hat zwei Gruppen: **Verbrauchsverträge** (Strom, Gas, Wasser) in großen Karten und **Pauschalverträge** (Internet, Mobilfunk, Versicherung, Sonstiges) in schlanken Karten. Die Karten stehen in Reihen gleicher Höhe; bei vier Verbrauchsverträgen entsteht 2 x 2, statt dass eine Karte allein in einer Reihe steht.
- Beta: Eine Pauschalkarte beginnt mit dem Abschlag pro Monat und zeigt die Kosten bisher, das Vertragsende und einen Laufzeit-Balken. Sie hat keinen Ring, keinen Verbrauch und keine leeren Zahlen; ein Vertrag ohne Vertragsende zeigt "Kein Vertragsende" statt eines Strichs oder einer angenommenen 12-Monats-Summe.
- Beta: Die Kostentabelle behandelt Pauschalverträge: Die Kosten bisher sind die bis heute fälligen Abschläge (auch in der Summe und in den Vertragsdetails). Saldo und Prognose bleiben leer, weil es keinen Verbrauch gibt.
- Beta: Die Übersicht hat keine Bearbeitungs-Aktionen mehr. Alles, was einen Vertrag ändert, steht im Tab "Verträge": Symbole in jeder Zeile (Folgevertrag planen oder bearbeiten, Vertrag bearbeiten) und oben der Button "Neuer Vertrag". Das Löschen bleibt im Bearbeiten-Dialog. "Warnung bestätigen" und "Kündigung bestätigen" bleiben auf der Karte bei ihrem Hinweis.

### Added

- Die Vertragsdaten enthalten jetzt die bis heute fälligen Abschläge (`abschlag_bisher_gezahlt`, endet am Vertragsende und berücksichtigt eine Abschlagsänderung). Das ist nur ein Wert für das Panel: kein neuer Sensor, bestehende Installationen bekommen also keine neuen Entitäten.

## [1.27.0-beta.8] - 2026-11-06

Achte Beta zum Testen des Seitenleisten-Panels. Neu: eine überarbeitete Übersicht. Bitte melde Probleme mit dem Bug-Formular und nenne diese genaue Version.

### Changed

- Beta: Die Übersicht wurde überarbeitet und orientiert sich stärker am Vorbild-Dashboard. Die Karten fließen jetzt ohne Lücken in Spalten statt in einem Raster mit Löchern, der Kopf einer Karte ist nach dem Zustand getönt (grün Guthaben, rot Nachzahlung, orange Kündigung fällig), Titel stehen in Kapitälchen, und die Kennzahl steht neben einem kleineren Fortschrittsring. Eine Karte zeigt höchstens drei Zahlen (Kosten bisher, Saldo bisher, Verbrauch) und eine Fußzeile mit der Restlaufzeit; weitere Zahlen stehen in den Ansichten "Kosten" und "Verträge".
- Beta: "Folgevertrag planen" und "Vertrag bearbeiten" sind in ein "…"-Menü im Kartenkopf gewandert (nur Administratoren). "Warnung bestätigen" und "Kündigung bestätigen" bleiben auf der Karte, bei dem Hinweis, zu dem sie gehören. Auf dem Handy bleiben die Buttons in der aufgeklappten Karte.
- Beta: Verträge ohne Beginn oder Ende zeigen keinen leeren Fortschrittsring mehr, und leere Kacheln entfallen.

### Fixed

- Beta: Am ersten Tag eines Vertrags mit Verbrauchssensor wird der Block "Verbrauch" in den Vertragsdetails gezeigt (Kosten und Verbrauch bisher gibt es schon, nur die Prognose fehlt noch). Bisher blieb er bis zum nächsten Tag ausgeblendet.
- Beta: Ein Menü auf einer Karte blieb nach der Auswahl eines Eintrags hinter dem Dialog offen.

## [1.27.0-beta.7] - 2026-11-06

Siebte Beta zum Testen des Seitenleisten-Panels. Sie behebt die Darstellung der Vertragsliste. Bitte melde Probleme mit dem Bug-Formular und nenne diese genaue Version.

### Fixed

- Beta: In der Ansicht "Verträge" waren die Zeilen zusammengequetscht: Name und Untertitel brachen Wort für Wort um, und der Betrag wurde über den Text gezeichnet. Die Zeilen zeigen jetzt Name, Status und Betrag in einer Zeile und brechen auf schmalen Bildschirmen um. Die Karten der Übersicht sind unverändert.

## [1.27.0-beta.6] - 2026-11-06

Sechste Beta zum Testen des Seitenleisten-Panels. Neu: Verträge direkt im Panel anlegen und löschen (nur Administratoren). Bitte melde Probleme mit dem Bug-Formular und nenne diese genaue Version.

### Added

- Beta: Das Panel kann jetzt Verträge anlegen ("Neuer Vertrag" in der oberen Leiste, nur Administratoren). Es startet den Einrichtungs-Dialog der Integration (erst Name und Sparte, dann die Daten der Sparte), Prüfung und Speicherung bleiben also unverändert, und der neue Vertrag erscheint von selbst im Panel.
- Beta: Das Panel kann jetzt einen Vertrag löschen ("Vertrag löschen" im Bearbeiten-Dialog, nur Administratoren). Weil das nicht rückgängig zu machen ist, muss vorher der Name des Vertrags eingetippt werden. Die Sensoren und Buttons des Vertrags werden entfernt; die Langzeit-Statistiken, die Home Assistant schon aufgezeichnet hat, bleiben in der Datenbank (der Dialog weist darauf hin).

### Fixed

- Beim Löschen eines Vertrags (im Panel oder in Home Assistant) werden jetzt auch seine offenen Benachrichtigungen zu Kündigung und zu niedrigem Abschlag entfernt. Bisher blieben sie dauerhaft in der Liste stehen.

## [1.27.0-beta.5] - 2026-11-06

Fünfte Beta zum Testen des Seitenleisten-Panels. Neu: einen Vertrag direkt im Panel bearbeiten (nur Administratoren). Bitte melde Probleme mit dem Bug-Formular und nenne diese genaue Version.

### Added

- Beta: Das Panel kann einen Vertrag jetzt bearbeiten ("Vertrag bearbeiten" auf der Vertragskarte, nur Administratoren). Es zeigt dieselben zwei Formulare wie der "Neu konfigurieren"-Dialog der Integration (allgemeine Daten, dann die Daten der Sparte) und speichert über diesen Dialog, Prüfung und Speicherung bleiben also unverändert. Der letzte Schritt fragt noch einmal nach, bevor die Vertragsdaten ersetzt werden. Ja/Nein-Einstellungen, Auswahllisten mit übersetzten Namen und Freitext mit Vorschlägen (Benachrichtigungs-Ziel) werden unterstützt.

### Fixed

- Beim Neukonfigurieren eines Vertrags gehen die Werte, die die Integration selbst führt, nicht mehr verloren. Bisher ersetzte der Dialog "Neu konfigurieren" die gespeicherten Daten durch das, was die Formulare enthalten: Eine bestätigte Kündigungs-Erinnerung oder Abschlag-Warnung kam wieder, eine schon gesendete Push-Nachricht konnte erneut gesendet werden, und der Verbrauch der letzten Laufzeit (Grundlage des empfohlenen Abschlags) ging verloren. Er bleibt jetzt erhalten. Die Kündigungs-Erinnerung beginnt nur dann neu, wenn sich Vertragsende oder Vorlaufzeit ändern.
- Die Auswahl "Kündigung erinnern" zeigt "3 Monate vorher" statt einer nackten "3" (die Texte gab es schon, sie waren nur nicht angebunden). Die gespeicherten Werte bleiben unverändert.

## [1.27.0-beta.4] - 2026-11-06

Vierte Beta zum Testen des Seitenleisten-Panels. Neu: Folgevertrag direkt im Panel planen, bearbeiten und entfernen (nur Administratoren). Die beiden Aktions-Buttons fragen jetzt eine zweite Stufe ab, und "Jetzt wechseln" gibt es im Panel nicht mehr, weil es den aktuellen Vertrag ersetzt hätte, bevor der neue beginnt. Bitte melde Probleme mit dem Bug-Formular und nenne diese genaue Version.

### Added

- Beta: Das Panel kann den Folgevertrag jetzt planen, bearbeiten und entfernen ("Folgevertrag planen" auf der Vertragskarte, nur Administratoren). Es zeigt dasselbe Formular wie der "Konfigurieren"-Dialog der Integration und speichert über diesen Dialog, Prüfung und Speicherung bleiben also unverändert. Ist die Kündigungserinnerung fällig, markiert ein Häkchen (standardmäßig an) die Kündigung im selben Schritt als erledigt.

### Changed

- Beta: Die beiden Aktions-Buttons im Panel (Warnung bestätigen, Kündigung bestätigen) fragen jetzt eine zweite Stufe ab, damit nichts versehentlich ausgelöst wird.
- Beta: Das Panel bietet "Jetzt wechseln" nicht mehr an. Der Klick hätte den aktuellen Vertrag sofort ersetzt, während der neue erst am geplanten Datum beginnt. Zum geplanten Datum wechselt der Vertrag von selbst; der Button in Home Assistant bleibt unverändert. Die ungenutzte Websocket-Aktion `switch_now` wurde mit entfernt.

## [1.27.0-beta.3] - 2026-11-06

Dritte Beta zum Testen des Seitenleisten-Panels. Neu: Warnung und Kündigungserinnerung bestätigen und auf einen geplanten Folgevertrag wechseln, direkt im Panel (nur Administratoren), sowie eine klarere Anzeige, wenn ein negativer Abschlag empfohlen wird. Bitte melde Probleme mit dem Bug-Formular und nenne diese genaue Version.

### Added

- Beta: Das Panel kann jetzt die Abschlag-Warnung bestätigen, die Kündigungserinnerung bestätigen und auf einen geplanten Folgevertrag wechseln, direkt in der Vertragskarte, mit Rückfrage vor dem Wechsel. Es sind dieselben Aktionen wie bei den drei Buttons, nur für Administratoren (neuer Websocket-Befehl `tariffy/action`, der dieselben Bedingungen wie die Buttons prüft). Alle anderen behalten die reine Leseansicht.

### Geändert

- Beta: Deckt das Guthaben die Kosten bis zum Vertragsende bereits ab, zeigt das Panel keinen negativen empfohlenen Abschlag mehr. Es zeigt 0,00 € mit dem Hinweis „Guthaben deckt die Kosten“. Der Sensor „Abschlag (Anpassung empfohlen)“ selbst bleibt unverändert.

## [1.27.0-beta.2] - 2026-11-06

Zweite Beta zum Testen des Seitenleisten-Panels. Sie enthält den Prognose-Fix aus 1.26.6, das Panel zeigt also nach einer Abschlagsänderung das korrigierte „Guthaben/Nachzahlung (Vertragsende)“. Das Panel selbst ist unverändert und nur lesend. Bitte melde Probleme mit dem Bug-Formular und nenne diese genaue Version.

### Behoben

- „Guthaben/Nachzahlung (Vertragsende)“ (und damit die Abschlag-Warnung) war nach einer Abschlagsänderung mitten im Vertrag zu optimistisch. Die Prognose rechnet jetzt mit den bisher tatsächlich gezahlten Abschlägen plus dem aktuellen Abschlag für die Restlaufzeit, siehe 1.26.6. Verträge, deren Abschlag nie geändert wurde, behalten exakt denselben Wert.

## [1.27.0-beta.1] - 2026-11-05

Beta zum Testen des neuen Seitenleisten-Panels. Das Panel liest nur, alles andere arbeitet wie in 1.26.5. Bitte melde Probleme mit dem Bug-Formular und nenne diese genaue Version. HACS bietet diese Version nur an, wenn „Beta-Versionen anzeigen“ aktiviert ist.

### Hinzugefügt

- Beta: Das Panel zeigt die Verträge jetzt in einem dunklen, kartenbasierten Design (Übersicht mit Zusammenfassung, Kostentabelle, Vertragsdetails) auf Deutsch und Englisch, auf dem Handy in einer kompakten, aufklappbaren Ansicht. Nur lesend. Die Seite wird von der Integration ausgeliefert, nutzt die System-Schrift und braucht keinen Build-Schritt.
- Beta: Backend für ein Tariffy-Seitenleisten-Panel. Es meldet das Panel „Tariffy“ an (für alle Benutzer sichtbar) und stellt zwei rein lesende Websocket-Befehle bereit, `tariffy/contracts` und `tariffy/subscribe`. Sie liefern die berechneten Werte aller Verträge, ohne Kundennummer, Zählernummern, MaLo-ID und Benachrichtigungsziel. Lässt sich das Panel nicht einrichten, wird nur eine Warnung geloggt, und die Integration arbeitet wie bisher. `manifest.json` führt `frontend`, `http`, `panel_custom` und `websocket_api` unter `after_dependencies`.

### Geändert

- CI: Der Release-Workflow läuft jetzt auch auf dem Branch `beta` und veröffentlicht Versionen wie `1.27.0-beta.1` als GitHub-Pre-Release (nie als „latest“). HACS bietet sie nur Nutzern an, die Beta-Versionen aktiviert haben. Stabile Releases aus `main` funktionieren wie bisher. Siehe `docs/beta-releases.md`.

## [1.26.6] - 2026-11-05

### Behoben

- **„Guthaben/Nachzahlung (Vertragsende)“ (und damit die Abschlag-Warnung) war nach einer Abschlagsänderung mitten im Vertrag zu optimistisch.** Die Prognose nahm den aktuellen Abschlag für die ganze Laufzeit an, obwohl „Guthaben/Nachzahlung (Bisher)“ und die Abschlag-Empfehlung den früheren, anderen Abschlag bis zum Änderungsdatum richtig mitzählten. Beispiel: Abschlag im Juli von 40 € auf 100 € erhöht, der Sensor zeigte zum Vertragsende ein Guthaben, obwohl der Saldo bisher negativ war. Die Prognose rechnet jetzt mit den bisher tatsächlich gezahlten Abschlägen plus dem aktuellen Abschlag für die Restlaufzeit. Bei Verträgen, deren Abschlag nie geändert wurde, ist der Wert exakt derselbe wie bisher. „Abschlag (Vertragslaufzeit)“ bleibt der reine Zahlungsplan (Abschlag × Laufzeit).

### Geändert

- CI: Der Release-Workflow läuft jetzt auch auf dem Branch `beta` und veröffentlicht Versionen wie `1.27.0-beta.1` als GitHub-Pre-Release (nie als „latest“). HACS bietet sie nur Nutzern an, die Beta-Versionen aktiviert haben. Stabile Releases aus `main` funktionieren wie bisher. Siehe `docs/beta-releases.md`.

## [1.26.5] - 2026-11-05

### Behoben

- Fiel ein Tarifwechsel in den ersten Refresh nach einem Home-Assistant-Start, wurde der Verbrauch der beendeten Laufzeit nicht eingefroren, der neue Vertrag hatte dann keinen „Verbrauch (Letzte Laufzeit)“ und keinen empfohlenen Abschlag. Der Zählerstand zum Vertragsbeginn wird nun auch in diesem Fall gelesen. Verträge mit manuell eingetragenem Startwert bleiben unverändert.
- Nach einem Tarifwechsel (automatisch zum Stichtag oder über den Button „Jetzt wechseln“) lädt die Integration wieder neu, wie vor 1.26.3. Seit 1.26.3 wurde der Sensorsatz (Nachttarif, Staffelpreise) nach einem Wechsel nicht mehr neu aufgebaut. Ein Folgevertrag mit anderen Merkmalen bekam seine Sensoren daher erst nach einem Neustart von Home Assistant.

### Geändert

- Automatisierte Tests für Kosten- und Prognoseberechnung, Tarifwechsel, Kündigungserinnerung und Abschlag-Warnung ergänzt, inklusive Regressionstest für die fehlenden Sensoren nach einem Tarifwechsel. Die CI führt sie bei jedem Push und Pull Request aus.

## [1.26.4] - 2026-11-05

### Geändert

- `manifest.json` deklariert jetzt `recorder` in `after_dependencies`, da die Integration die Long-Term Statistics liest.
- Der Coordinator übergibt seinen Config Entry nun an `DataUpdateCoordinator` (`config_entry=`), wie es neuere Home-Assistant-Versionen erwarten.
- Eine ungenutzte Variable und zwei ungenutzte Imports entfernt.
- CI: `ruff` (nur Korrektheitsregeln) und die offizielle `hassfest`-Prüfung ergänzt.

## [1.26.3] - 2026-11-05

### Behoben

- **HA-Core-Warnung „custom integration 'tariffy' has an update listener and should use it for scheduling a reload"** (funktioniert ab Home Assistant 2026.12.0 nicht mehr, [#2](https://github.com/weskona/tariffy/issues/2)): der manuelle Update-Listener wurde durch `OptionsFlowWithReload` ersetzt, das Speichern des Options-Flows lädt den Eintrag weiterhin neu. Interne Datenänderungen (manueller Wechsel, Bestätigen von Kündigung/Abschlag-Warnung) lösen nun einen Coordinator-Refresh statt eines vollständigen Reloads aus. Mindestversion von Home Assistant in `hacs.json` auf 2025.8.0 angehoben.

## [1.26.2] - 2026-08-25

### Behoben

- **Preisfelder haben ihre konfigurierte Schrittweite stillschweigend ignoriert**: der interne Helfer `_preis()`, den rund zwei Dutzend Preisfelder im Config Flow nutzen (Arbeitspreise, Grundpreis, Abschlag, Abschlag-Warnschwelle), nahm zwar einen `step`-Parameter entgegen, gab ihn aber nie an den zugrundeliegenden Zahlen-Selector weiter — jedes Preisfeld nutzte immer die generische Schrittweite `"any"`, unabhängig von der eigentlich vorgesehenen Genauigkeit (z. B. 0,0001 für Arbeitspreise, 0,01 für Grundpreis/Abschlag, 1,0 für die Warnschwelle). Nutzt jetzt die übergebene Schrittweite — mit einer Ausnahme: die acht Arbeitspreis-Felder mit gewünschter Schrittweite 0,0001 bleiben bei `"any"`, weil Home Assistants `NumberSelector` jede Schrittweite unter 0,001 hart ablehnt (wirft beim Aufbau des Formulars, rundet nicht einfach) — es gibt dafuer schlicht keinen gueltigen feineren Wert. Grundpreis/Abschlag/Warnschwelle (0,01/1,0) bekommen jetzt korrekt eine echte Schrittweite.
- **"Nächster Vertrag" hatte keine NT-Felder für Zweizählertarif-Verträge (HT/NT)**: der Options-Flow zum Planen eines kommenden Tarifwechsels zeigte nur ein einzelnes Feld "Arbeitspreis neu" — auch für die Zweizählertarif-Sparte, die Hoch- und Niedertarif unabhängig erfasst. Ein Tarifwechsel für das NT-Register liess sich damit nicht planen. Ergänzt: "Arbeitspreis neu, Niedertarif / NT", "Verbrauchssensor neu, Niedertarif / NT" und "Zählernummer neu, Niedertarif / NT" — nur bei HT/NT-Verträgen sichtbar, direkt nach dem bestehenden Arbeitspreis-Feld.
- **Englische Übersetzungen waren massiv unvollständig — 311 von 470 Keys fehlten**: `translations/en.json` wurde nie mit `strings.json` synchron gehalten (die deutsche Datei, `translations/de.json`, hatte vollständige Parität). Komplett gefehlt haben: die gesamten Einrichtungsschritte "Wasser" und "Strom (Zweizählertarif, HT/NT)", die meisten Feld-Beschriftungen für Staffelpreise und Tag/Nacht-Tarife, jede einzelne Feld-Beschreibung (`data_description`) in allen Schritten, sowie zwei Dropdown-Options-Texte (die HT/NT-Sparte selbst und alle drei Abwasser-Preismodell-Optionen) — all das zeigte statt lesbarem Text nur den rohen internen Key. Aus `strings.json` (der massgeblichen englischen Quelle) ergänzt, ohne die 159 bereits korrekten Keys anzufassen — beide Dateien haben jetzt identische Struktur und Key-Menge. Zusätzlich zwei verwaiste Übersetzungs-Keys (`prognose`, `geschaetzte_jahreskosten`) aus `strings.json` entfernt, die von keinem Sensor im Code mehr referenziert werden.

## [1.26.1] - 2026-08-07

### Hinzugefügt

- **Zweizählertarif-Sparte (HT/NT — Hochtarif/Niedertarif)**: neue Sparte „Strom (Zweizählertarif, Hoch-/Niedertarif)" für einen echten Zweiregister-Stromzähler. Fügt einen zweiten Arbeitspreis, zweiten Verbrauchssensor, zweiten manuellen Zählerstand-Override und zweite Zählernummer für das Niedertarif-Register hinzu — komplett unabhängig vom Hochtarif-Register erfasst (eigener Long-Term-Statistics-Offset, eigener manueller Override-Fallback). Die bestehenden kombinierten Sensoren (Kosten/Guthaben/Prognose Bisher usw.) funktionieren wie bei jedem anderen Stromvertrag weiter — der Verbrauch beider Register wird summiert, und der von allen nachgelagerten Formeln verwendete Arbeitspreis wird automatisch zu einem gewichteten Durchschnitt beider Tarife. Vier neue eigene Sensoren zeigen die Aufschlüsselung je Register: Verbrauch Hochtarif/Niedertarif (Bisher) und Kosten Hochtarif/Niedertarif (Bisher) — Letztere sind die reinen verbrauchsbasierten Kosten dieses Registers, ohne Grundpreis-Anteil.

## [1.25.1] - 2026-07-30

### Behoben

- **"Verbrauch (Bisher)" konnte durch eine Anomalie in Home Assistants eigener Recorder-
  `sum`-Langzeitstatistik plötzlich einen viel zu hohen Wert zeigen**, obwohl der rohe
  Zählerstand des Sensors durchgehend korrekt und unauffällig weiterlief (beobachtet: die
  `sum`-Statistik sprang nach einem HA-Neustart innerhalb einer Stunde auf etwa das Doppelte,
  während sich der tatsächliche Zählerstand im selben Zeitraum nur um 0,1 kWh änderte). Die
  Berechnung liest jetzt zusätzlich zur `sum`-Statistik auch den zugehörigen rohen `state`-Wert
  mit und vergleicht beide: bleibt der aktuelle Zählerstand seit Vertragsbeginn nicht unter den
  Anfangswert gefallen (der Normalfall, kein echter Reset), wird die einfache, robuste
  State-Differenz verwendet statt der potenziell fehleranfälligen `sum`-Statistik. Ein echter
  Zählerstand-Reset (z. B. bei manchen Gaszählern üblich) wird weiterhin korrekt über die
  reset-sichere `sum`-Statistik aufgefangen. Dadurch behebt sich das in Issue #1 gemeldete
  Problem jetzt auch automatisch, ganz ohne den in 1.25.0 hinzugefügten manuellen Zählerstand-
  Fallback eintragen zu müssen — dieser bleibt als Option für den selteneren Fall erhalten, dass
  die Statistik-Historie eines Sensors tatsächlich nicht bis zum Vertragsbeginn zurückreicht.

## [1.25.0] - 2026-07-26

### Hinzugefügt

- **Optionaler manueller Zählerstand bei Vertragsbeginn** (Strom/Gas/Wasser): neues Feld
  "Zählerstand bei Vertragsbeginn", das den automatisch über Home Assistants Recorder-
  Langzeitstatistik ermittelten Referenzwert überschreibt, sobald gesetzt. Deckt den Fall ab,
  dass die Statistik-Historie des Verbrauchssensors nicht bis zum Vertragsbeginn zurückreicht
  (z.B. weil der Sensor zwischenzeitlich umbenannt oder neu angelegt wurde, auch wenn die reine
  Zustands-Historie durchgehend aussieht) — bislang führte das zu einer falschen Berechnung
  ("Verbrauch (Bisher)" zeigte dann den vollen Zählerstand statt der Differenz seit
  Vertragsbeginn). Wird der manuelle Wert genutzt, rechnet Tariffy bewusst gegen den rohen
  aktuellen Zählerstand statt gegen die reset-sichere `sum`-Statistik, da beide unterschiedliche
  (unbekannte) Referenzpunkte haben und sich nicht mischen lassen.

## [1.24.4] - 2026-07-26

### Behoben

- **"Unable to remove unknown job listener" beim Neuladen der Integration** (z.B. nach einer
  Options-Änderung, oder manuell über "Neu laden"): der `_startup_refresh`-Listener auf
  `EVENT_HOMEASSISTANT_STARTED` wird registriert, unabhängig davon ob HA bereits vollständig
  gestartet ist. Feuert dieses Event vor dem Neuladen schon (der Normalfall bei jedem Reload,
  der nicht direkt beim HA-Start passiert), entfernt sich der Listener selbst — der
  `entry.async_on_unload()`-Aufruf beim nächsten Unload versuchte trotzdem noch, ihn zu
  entfernen, was zu diesem Fehler im Log führte. Prüft jetzt `hass.is_running`: läuft HA
  bereits, wird der Refresh direkt ausgeführt statt auf ein Event zu warten, das nicht mehr
  kommt.

## [1.24.3] - 2026-07-14

### Behoben

- **1.24.2s `zip_release` hat HACS' Fähigkeit, das Release überhaupt zu sehen/installieren, komplett kaputt gemacht**: Das Release-Zip hatte alles unter `custom_components/tariffy/` (plus `hacs.json`/`README.md`/`LICENSE` im Root) verpackt, aber HACS' `zip_release`-Modus erwartet die Integrationsdateien direkt im Zip-Root (Byte für Byte gegen HACS' eigenes `hacs.zip`-Release-Asset verifiziert, das `manifest.json` etc. direkt oben liegen hat, ohne `custom_components/hacs/`-Wrapper). Der Release-Workflow zippt jetzt den *Inhalt* von `custom_components/tariffy/` direkt.

## [1.24.2] - 2026-07-14

### Behoben

- **HACS-Download-Zähler stand immer auf 0**: `hacs.json` hatte kein `zip_release`/`filename` gesetzt, wodurch HACS bei jedem Release still auf das automatisch von GitHub generierte Quellcode-Archiv auswich statt auf das von unserem Release-Workflow hochgeladene `tariffy.zip` — und GitHub zählt Downloads nur für tatsächlich hochgeladene Release-Assets, nicht für Auto-Archive. `"zip_release": true, "filename": "tariffy.zip"` ergänzt, damit HACS das getrackte Asset lädt.

## [1.24.1] - 2026-07-14

### Behoben

- **Einheiten zeigten "€/kWh" statt "EUR/kWh"**: Der in 1.23.0 eingeführte Code-zu-Symbol-Fix (`hass.config.currency` → "€") war eine Fehlinterpretation und genau verkehrt herum — gewünscht war durchgehend der rohe ISO-4217-Code (z. B. "EUR/kWh"), nicht das Symbol. Die Symbol-Umwandlung wurde vollständig entfernt; alle Kosten-Sensoren zeigen die Einheit wieder als Code an.

## [1.24.0] - 2026-07-14

### Hinzugefügt

- **Dynamischer Tarif für Strom (Börsen-/Spotpreis)**: neue optionale Felder „Preissensor für dynamischen Tarif" und „Aufschlag dynamischer Tarif" bei Strom-Verträgen. Statt eines festen Arbeitspreises kann jetzt ein bestehender HA-Sensor referenziert werden, der einen live Spotpreis liefert (z. B. von Tibber, aWATTar, Nordpool) — der Arbeitspreis wird dann als Durchschnitt dieses Sensors über die bisherige Vertragslaufzeit (+ fester Aufschlag) berechnet und fließt automatisch in alle bestehenden Berechnungen ein (Kosten bisher, Guthaben/Nachzahlung, Abschlag-Anpassungsempfehlung, Abrechnungsprognose). Der manuell eingegebene Arbeitspreis bleibt als Fallback erhalten, solange für den Sensor noch keine ausreichende Statistik-Historie vorliegt. Der aktuelle Live-Preis (Sensor + Aufschlag) wird zusätzlich als Attribut `arbeitspreis_aktuell` am Sensor „Arbeitspreis" angezeigt, der bei aktivem dynamischen Tarif außerdem ein eigenes Icon erhält.

## [1.23.0] - 2026-07-14

### Hinzugefügt

- **Neuer Sensor „Abschlag (Anpassung empfohlen)"**: berechnet fortlaufend, was der Abschlag ab jetzt bis Vertragsende sein müsste, um exakt auszugleichen — im Unterschied zu „Abschlag (Empfohlen)" (nur nach Tarifwechsel, auf Basis der eingefrorenen letzten Laufzeit). Die Abschlag-Warnung-Benachrichtigung nennt jetzt zusätzlich diesen konkreten Empfehlungswert statt nur "Abschlag erhöhen".

### Behoben

- **Einheiten zeigten "EUR" statt "€"**: `hass.config.currency` liefert den ISO-4217-Code ("EUR"), kein Symbol. Alle Kosten-Sensoren (Arbeitspreis, Grundpreis, Abschlag, Kosten, Guthaben/Nachzahlung, ...) zeigten deshalb z. B. "EUR/kWh" statt "€/kWh". Wird jetzt für die gängigsten Währungen (EUR, USD, GBP, JPY, CNY, KRW, INR, RUB, BRL, TRY, ILS, MYR, NGN, PHP, THB, TWD, VND) in das jeweilige Symbol umgewandelt; unbekannte Codes zeigen weiterhin den rohen Code als Fallback.
- **Abschlags-Änderung wurde rückwirkend auf die gesamte bisherige Vertragslaufzeit angewendet**: Erhöhte/verringerte man den Abschlag mitten im Vertrag, rechneten „Guthaben/Nachzahlung (Bisher)" und „Abschlag (Anpassung empfohlen)" fälschlich so, als hätte der NEUE Abschlag schon seit Vertragsbeginn gegolten. Tariffy merkt sich jetzt automatisch Datum und vorherigen Wert bei jeder Abschlags-Änderung (`config_flow.py::_stamp_abschlag_change`) und wendet den alten Abschlag korrekt nur bis zum Änderungsdatum an, den neuen erst danach. Mehrere Korrekturen am selben Tag zählen als eine einzige Änderung (kein rückwirkender Zwischenstand).

## [1.22.0] - 2026-07-14

### Hinzugefügt

- **Optionale Abschlag-Warnung** (pro Vertrag, nur Energie/Wasser mit `verbrauch_sensor`): warnt per `persistent_notification` (+ optional `notify.*`), wenn die Prognose zum Vertragsende (`prognose_real`) eine Nachzahlung über einer einstellbaren Schwelle (Default 50 €) erwarten lässt. Neuer Button „Abschlag-Warnung bestätigen" zum Entfernen der Meldung — verschlechtert sich die Prognose danach erneut, wird automatisch wieder gewarnt (kein dauerhaftes Stummschalten). Rohzustand zusätzlich als Attribut `abschlag_warnung_aktiv` am Sensor „Guthaben/Nachzahlung (Vertragsende)".

## [1.21.0] - 2026-07-14

### Behoben

- **"Expected str"-Fehler bei Brennwert/Zustandszahl beim Bearbeiten eines bestehenden Gas-Vertrags**: Der Schema-Default für diese Felder war ein `float` (der bereits gespeicherte Wert), obwohl `TextSelector` zwingend einen String erwartet. Sendete das Formular den unveränderten Vorbelegungswert unverändert ab, kam ein roher Float statt eines Strings an, und die Validierung schlug fehl — noch bevor die eigentliche Komma/Punkt-Normalisierung überhaupt lief. Erst durch aktives Ändern des Werts (z. B. auf ein Komma) wurde ein echter String übermittelt, der dann funktionierte. Schema-Defaults werden jetzt immer als String deklariert.
- **Brennwert/Zustandszahl fehlten komplett beim Planen eines Nachfolgevertrags (Gas)**: Beim automatischen Tarifwechsel wurde dadurch stillschweigend der alte Brennwert/die alte Zustandszahl übernommen, ohne Möglichkeit zur Korrektur für den neuen Anbieter. Felder (inkl. Gas-Einheit) jetzt im Options-Flow für Gas-Verträge ergänzt.

## [1.20.0] - 2026-07-12

### Behoben

- **README.md des Standalone-Repos (die von HACS/GitHub angezeigte Version) hatte die "vier Kosten-Sensoren"-Erklärung gar nicht**: Das ausführliche 2×2-Raster mit Rechenbeispiel für `jahreskosten`/`kosten_bisher`/`guthaben_bisher`/`prognose_real` war bisher nur in dieser separaten Dokumentations-Kopie enthalten, nie im eigentlichen Top-Level-README des Standalone-Repos. Jetzt in beiden Sprachabschnitten (Englisch + Deutsch) dort ergänzt.

## [1.19.0] - 2026-07-12

### Behoben

- **README.md/CHANGELOG.md wurden von HACS immer wieder gelöscht**: Beide lagen im Standalone-Repo bisher nur auf oberster Ebene, nicht innerhalb von `custom_components/tariffy/`. HACS synct diesen Ordner 1:1 vom Repo und entfernte deshalb bei jedem Update lokale Dateien, die dort nicht Teil des offiziellen Pakets waren. Liegen jetzt zusätzlich innerhalb von `custom_components/tariffy/` im Standalone-Repo, damit sie als Teil des Pakets erhalten bleiben.

## [1.18.0] - 2026-07-12

### Behoben

- **Falsche Einheit bei "Verbrauch (Bisher)"/"Verbrauch (Vertragslaufzeit hochgerechnet)" bei Gas/Wasser**: Diese Sensoren zeigten die Anzeige-Einheit aus `gas_einheit`/`wasser_einheit` (die eigentlich nur die Einheit der manuell eingetragenen Jahresverbrauchs-Schätzung beschreibt), obwohl der angezeigte Wert der rohe Zählerstand-Delta des echten Verbrauchssensors ist — bei m³-Zählern mit `gas_einheit: kWh` stand fälschlich "kWh" über einem m³-Wert. Zeigt jetzt die tatsächliche Einheit des konfigurierten `verbrauch_sensor` an (Fallback auf das Config-Feld, falls der Sensor nicht verfügbar ist).

### Geändert

- README grundlegend überarbeitet: alle Sensor-Erklärungen jetzt mit durchgerechneten Beispielen aus echten Live-Verträgen (Strom, Gas) statt nur abstrakten Formeln; Wasser/Tag-Nacht/Staffelpreis mit klar gekennzeichneten Beispielzahlen (keine echten Verträge dieser Art vorhanden).

## [1.17.0] - 2026-07-12

### Geändert

- **Zwei Kosten-Sensoren umbenannt**, um das Zusammenspiel der vier Guthaben/Kosten-Sensoren klarer zu machen (nur Anzeigename, `entity_id`/`unique_id` unverändert):
  - „Kosten (Vertragslaufzeit)" → „Abschlag (Vertragslaufzeit)" (`jahreskosten`) — macht deutlich, dass es der reine Zahlungsplan ist, keine Kosten-Prognose auf Basis des echten Verbrauchs.
  - „Kosten (Guthaben/Nachzahlung)" → „Guthaben/Nachzahlung (Vertragsende)" (`prognose_real`) — parallele Benennung zu „Guthaben/Nachzahlung (Bisher)".
- README komplett neu strukturiert: 2×2-Raster (Bisher/Vertragsende × reiner Betrag/Bilanz) plus durchgerechnetes Zahlenbeispiel für alle vier Sensoren.

## [1.16.0] - 2026-07-12

### Behoben

- **Manueller "Jetzt wechseln"-Button fror den Verbrauch der endenden Laufzeit nicht ein**: Der Button rief `_switch_now()` ohne den real gemessenen Verbrauch auf, im Unterschied zum automatischen Datumswechsel — `verbrauch_letzte_laufzeit` blieb dadurch leer oder veraltet, was `empfohlener_abschlag` beim nächsten Wechsel verfälscht hätte. Beide Wege nutzen jetzt dieselbe Berechnung (`_verbrauch_letzte_laufzeit_jetzt()`).

## [1.15.0] - 2026-07-12

### Geändert

- **Tarifwechsel reagiert jetzt exakt auf Datumswechsel**: bisher wurde das Wechseldatum nur beim naechsten regulaeren 6-Stunden-Poll geprueft, wodurch der Wechsel bis zu knapp 6 Stunden zu spaet greifen konnte. Neuer taeglicher Trigger um 00:00:01 Uhr (`async_track_time_change`) prueft und schaltet den Vertrag exakt bei Datumswechsel um. Der bestehende 6h-Poll und der HA-Start-Refresh bleiben als Fallback erhalten.

## [1.14.0] - 2026-07-11

### Hinzugefügt

- **Neuer Sensor „Guthaben/Nachzahlung (Bisher)"** (`guthaben_bisher`): `abschlag × vergangene_monate − kosten_bisher`. Beantwortet "bin ich mit meinem Abschlag bis heute im Plus oder Minus?", ohne Hochrechnung auf die volle Vertragslaufzeit (im Unterschied zu `prognose_real`). Gleiches dynamisches 👍/👎-Icon wie bei `prognose_real`. Nur Energie-Sparten, benötigt `verbrauch_sensor`.

## [1.13.0] - 2026-07-11

### Geändert

- **`prognose_real`-Sensor umbenannt**: „Kosten (Prognose Real)" → „Kosten (Guthaben/Nachzahlung)" (nur Anzeigename, `entity_id`/`unique_id` unverändert) — klarer als der bisherige Name, was der Sensor eigentlich beantwortet.
- **Dynamisches Icon für `prognose_real`**: zeigt jetzt `mdi:thumb-up` bei Guthaben (Wert ≥ 0), `mdi:thumb-down` bei Nachzahlung (Wert < 0), Fallback `mdi:calculator-variant` wenn der Wert unbekannt ist (z. B. ohne konfigurierten `verbrauch_sensor`).
- README um eine Übersichtstabelle der drei Kosten-Sensoren (`jahreskosten`, `kosten_bisher`, `prognose_real`) ergänzt, die Formel und Zweck auf einen Blick gegenüberstellt.

## [1.12.0] - 2026-07-09

### Geändert

- **Hochrechnung auf Vertragslaufzeit statt Kalenderjahr**: `verbrauch_hochgerechnet` rechnete bisher immer auf ein festes 365-Tage-Jahr hoch, unabhängig von der tatsächlichen Vertragsdauer. Rechnet jetzt auf `(ende − beginn)` Tage hoch — wichtig bei Verträgen, die unterjährig wechseln. 365 Tage bleibt Fallback für Verträge ohne `ende`.
- **Empfohlener Abschlag** nutzt jetzt die tatsächliche Dauer der letzten Vertragslaufzeit (`verbrauch_letzte_laufzeit_monate`, neu beim Tarifwechsel eingefroren) statt pauschal 12 Monate anzunehmen.
- **Verbrauchssensor umbenannt**: „Jahresverbrauch (Hochgerechnet)" → „Verbrauch (Vertragslaufzeit hochgerechnet)", passend zum bestehenden „Verbrauch (Bisher)"-Schema.
- **Verbrauch-Tracking auf `sum`-Statistik umgestellt**: `verbrauch_bisher` und der Offset zum Vertragsbeginn nutzen jetzt die reset-sichere `sum`-Spalte der Recorder-Langzeitstatistik statt des rohen `state`-Werts. Betrifft `_get_historic_value`, den aktuellen Sensorwert-Read sowie das Einfrieren von „Verbrauch (Letzte Laufzeit)" beim Tarifwechsel. Notwendig für Sensoren mit `state_class: total_increasing`, die erlaubterweise periodisch zurücksetzen (z. B. manche ESP-basierte Zähler) — die alte State-Differenz ergab dabei teils negative Werte.
- Für Sensoren, die regelmäßig zurücksetzen, wo möglich einen echten, nie zurücksetzenden Zählerstand-Sensor als `verbrauch_sensor` konfigurieren (z. B. ein separates Utility-Meter mit `cycle: none`), statt sich allein auf die `sum`-Statistik zu verlassen.

### Behoben

- **Absturz (500 Internal Server Error) beim Anlegen/Bearbeiten eines Gas-Vertrags**: Ein erster Versuch, Dezimalkomma-Eingabe (`11,2`) für Brennwert/Zustandszahl zu erlauben, ließ sich nicht zu JSON serialisieren (`voluptuous_serialize` kann keine eigenen Funktionen in `vol.All` konvertieren). Brennwert/Zustandszahl sind jetzt reine Textfelder im Schema; die Komma/Punkt-Normalisierung passiert nach der Formularvalidierung in der jeweiligen Step-Funktion, mit sauberer Fehlermeldung statt Absturz bei ungültiger Eingabe.
- **Brennwert/Zustandszahl akzeptieren Dezimalkomma**: `11,2` und `11.2` funktionieren jetzt beide (Ursprungsmeldung: HTML5-Zahlenfeld verarbeitet Komma je nach Browser/Locale nicht zuverlässig).

## Vor 1.12.0

Keine strukturierte Changelog-Historie vor dieser Version.

[Unreleased]: https://github.com/weskona/tariffy/compare/v1.27.0-beta.3...HEAD
[1.27.0-beta.3]: https://github.com/weskona/tariffy/compare/v1.27.0-beta.2...v1.27.0-beta.3
[1.27.0-beta.2]: https://github.com/weskona/tariffy/compare/v1.27.0-beta.1...v1.27.0-beta.2
[1.27.0-beta.1]: https://github.com/weskona/tariffy/compare/v1.26.5...v1.27.0-beta.1
[1.26.6]: https://github.com/weskona/tariffy/compare/v1.26.5...v1.26.6
[1.26.5]: https://github.com/weskona/tariffy/compare/v1.26.4...v1.26.5
[1.26.4]: https://github.com/weskona/tariffy/compare/v1.26.3...v1.26.4
[1.26.3]: https://github.com/weskona/tariffy/compare/v1.26.2...v1.26.3
[1.26.2]: https://github.com/weskona/tariffy/compare/v1.26.1...v1.26.2
[1.26.1]: https://github.com/weskona/tariffy/compare/v1.25.1...v1.26.1
[1.25.1]: https://github.com/weskona/tariffy/compare/v1.25.0...v1.25.1
[1.25.0]: https://github.com/weskona/tariffy/compare/v1.24.4...v1.25.0
[1.24.4]: https://github.com/weskona/tariffy/compare/v1.24.3...v1.24.4
[1.24.3]: https://github.com/weskona/tariffy/compare/v1.24.2...v1.24.3
[1.24.2]: https://github.com/weskona/tariffy/compare/v1.24.1...v1.24.2
[1.24.1]: https://github.com/weskona/tariffy/compare/v1.24.0...v1.24.1
[1.24.0]: https://github.com/weskona/tariffy/compare/v1.23.0...v1.24.0
[1.23.0]: https://github.com/weskona/tariffy/compare/v1.22.0...v1.23.0
[1.22.0]: https://github.com/weskona/tariffy/compare/v1.21.0...v1.22.0
[1.21.0]: https://github.com/weskona/tariffy/compare/v1.20.0...v1.21.0
[1.20.0]: https://github.com/weskona/tariffy/compare/v1.19.0...v1.20.0
[1.19.0]: https://github.com/weskona/tariffy/compare/v1.18.0...v1.19.0
[1.18.0]: https://github.com/weskona/tariffy/compare/v1.17.0...v1.18.0
[1.17.0]: https://github.com/weskona/tariffy/compare/v1.16.0...v1.17.0
[1.16.0]: https://github.com/weskona/tariffy/compare/v1.15.0...v1.16.0
[1.15.0]: https://github.com/weskona/tariffy/compare/v1.14.0...v1.15.0
[1.14.0]: https://github.com/weskona/tariffy/compare/v1.13.0...v1.14.0
[1.13.0]: https://github.com/weskona/tariffy/compare/v1.12.0...v1.13.0
[1.12.0]: https://github.com/weskona/tariffy/releases/tag/v1.12.0
