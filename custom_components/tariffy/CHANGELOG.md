# Changelog

Alle nennenswerten Änderungen an Tariffy werden in dieser Datei festgehalten.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.1.0/),
das Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

## [Unreleased]

## [1.28.0-beta.7] - 2026-11-12

Siebte Beta zum Testen der Vertragshistorie und der Sicherung. Bitte melde Probleme mit dem Bug-Formular und nenne diese genaue Version.

### Added

- **Pauschalverträge verlängern.** Verträge ohne Verbrauch (Versicherung, Internet, Mobilfunk, Sonstiges) mit einem Vertragsende bekommen im Tab "Verträge" das Symbol "Vertrag verlängern" (nur Administratoren). Der Dialog schlägt als Beginn den Tag nach dem bisherigen Ende vor, als neues Ende ein Jahr später und den bisherigen Betrag und die Zahlweise, und zeigt, wie viel teurer oder günstiger der neue Betrag ist. Beim Verlängern wird die bisherige Laufzeit in der Historie gesichert, der Vertrag läuft mit neuem Beginn, Ende und Betrag weiter, und die Erinnerungen beginnen neu. Gedacht ist das für einen Beitrag, der jedes Jahr steigt, wie bei einer Kfz-Versicherung. Neuer Websocket-Befehl `tariffy/renew` (nur Administratoren) und das Vertragsdatum `verlaengerbar` für das Panel.

## [1.28.0-beta.6] - 2026-11-12

Sechste Beta zum Testen der Vertragshistorie und der Sicherung. Bitte melde Probleme mit dem Bug-Formular und nenne diese genaue Version.

### Added

- **Zahlweise und Jahreswerte für Pauschalverträge** (Internet, Mobilfunk, Versicherung, Sonstiges). Der Kosten-Schritt hat ein neues Feld "Zahlweise" (monatlich, vierteljährlich, halbjährlich, jährlich), und der Betrag wird pro Zahlung eingegeben, ein Versicherungs-Jahresbeitrag also so, wie er abgerechnet wird. Intern rechnet die Integration weiter mit dem Betrag pro Monat (600 € im Jahr werden als 50 € im Monat gespeichert, `abschlag` behält seine Bedeutung), **bestehende Verträge bleiben deshalb genau wie sie sind** (monatlich). Eine Änderung nur der Zahlweise gilt nicht als Abschlagsänderung. Das Panel zeigt den Jahres-Abschlag ("480 € / Jahr") auf der Karte, in der Kostentabelle und in den Vertragsdetails, dazu die Jahreskosten (Abschlag und Grundpreis) und, wenn nicht monatlich gezahlt wird, den Betrag pro Zahlung. Keine neuen Sensoren: Die Werte sind nur Daten für das Panel.

## [1.28.0-beta.5] - 2026-11-12

Fünfte Beta zum Testen der Vertragshistorie und der Sicherung. Bitte melde Probleme mit dem Bug-Formular und nenne diese genaue Version.

### Added

- **Der Name eines Vertrags lässt sich ändern.** Der erste Schritt von "Vertrag bearbeiten" (im Panel und in Home Assistant unter "Neu konfigurieren") beginnt jetzt mit dem Feld "Name", gefüllt mit dem aktuellen Namen. Beim Speichern wird er übernommen: Name des Vertrags und seines Geräts ändern sich, die Sensoren, ihre Entity-IDs und alle Vertragsdaten bleiben. Ein leerer Name behält den alten. Bisher ließ sich der Name nur beim Anlegen des Vertrags setzen.

## [1.28.0-beta.4] - 2026-11-12

Vierte Beta zum Testen der Vertragshistorie und der Sicherung. Bitte melde Probleme mit dem Bug-Formular und nenne diese genaue Version.

### Fixed

- **Die Auswahlliste eines Dropdowns in den Dialogen des Panels war in manchen Browsern unlesbar** (weiße Liste mit heller Schrift, zum Beispiel bei "Kündigung erinnern" oder der Sparte im Dialog für einen neuen Vertrag). Die Einträge haben jetzt die dunklen Farben des Panels, und das ganze Panel meldet dem Browser, dass es dunkel ist, damit auch die Datumsauswahl und andere eingebaute Elemente passen.

## [1.28.0-beta.3] - 2026-11-11

Dritte Beta zum Testen der Vertragshistorie und der Sicherung. Bitte melde Probleme mit dem Bug-Formular und nenne diese genaue Version.

### Added

- **Sicherung und Wiederherstellung.** Der neue Tab **Sicherung** des Seitenleisten-Panels (nur Administratoren) lädt alle Verträge als Datei herunter (Daten, Historie, Archiv, geplanter Folgevertrag, interner Zustand), stellt Verträge aus einer solchen Datei wieder her und holt gelöschte Verträge zurück. Beim Wiederherstellen siehst du zuerst, was passieren würde, und es werden nur Verträge angelegt, die es noch nicht gibt (gleicher Name und Sparte); vorhandene Verträge werden nie verändert. Die Datei wird streng geprüft, eine kaputte Datei legt nichts an. **Die Datei enthält persönliche Daten** (Kundennummer, Zählernummer, Marktlokations-ID, Benachrichtigungsziel); der Tab weist darauf hin. Neue Websocket-Befehle `tariffy/backup_export`, `tariffy/backup_preview`, `tariffy/backup_restore`, `tariffy/deleted_list`, `tariffy/deleted_restore` und `tariffy/deleted_discard` (nur Administratoren) und ein `import`-Schritt des Config-Flows, der einen Vertrag aus einer Sicherung anlegt.
- **Gelöschte Verträge lassen sich zurückholen.** Wird ein Vertrag gelöscht (im Panel oder in Home Assistant), bleibt er 30 Tage lang (höchstens die letzten 20) in Home Assistants Speicher (`.storage/tariffy.deleted`) erhalten und lässt sich im Tab Sicherung wiederherstellen. "Jetzt vergessen" entfernt eine solche Sicherung sofort. Das Löschen scheitert daran nie.

## [1.28.0-beta.2] - 2026-11-11

Zweite Beta zum Testen der Vertragshistorie. Bitte melde Probleme mit dem Bug-Formular und nenne diese genaue Version.

### Added

- **Alte Verträge von Hand hinzufügen.** In der Historie können Administratoren mit "Alten Vertrag hinzufügen" eine frühere Laufzeit eines Vertrags eintragen (zum Beispiel einen Vertrag von vor zwei Jahren) und sie mit dem Stift in der Zeile bearbeiten oder löschen. Beginn und Ende sind Pflicht; Anbieter, Tarif, Preis, Grundpreis und Abschlag sind optional. **Verbrauch, Kosten, gezahlte Abschläge und Saldo werden automatisch ermittelt**, soweit es geht: der Verbrauch aus den Langzeitstatistiken des Zählers des Vertrags, der Rest daraus und aus den Preisen (Gas mit Brennwert und Zustandszahl; bei Pauschalverträgen sind die Kosten die gezahlten Abschläge). Der Dialog zeigt die berechneten Werte und woher sie kommen, und jeder Wert lässt sich selbst eintragen und hat dann Vorrang. Neue Websocket-Befehle `tariffy/history_calc`, `tariffy/history_save` und `tariffy/history_delete` (nur Administratoren).

### Changed

- Die Historie speichert bis zu 50 Laufzeiten je Vertrag (vorher 20), weil Laufzeiten jetzt auch von Hand dazukommen können.

## [1.28.0-beta.1] - 2026-11-11

Beta-Version zum Testen der Vertragshistorie. Bitte melde Probleme mit dem Bug-Formular und nenne diese genaue Version. HACS bietet diese Version nur an, wenn "Beta-Versionen anzeigen" eingeschaltet ist.

### Added

- **Vertragshistorie.** Wenn der Folgevertrag am geplanten Datum übernimmt, wird die alte Laufzeit jetzt gesichert, bevor die Vertragsdaten ersetzt werden (Zeitraum, Anbieter, Tarif, Preise, Abschlag, Kosten bisher, Verbrauch und Saldo zum Ende; keine Kunden- oder Zählernummern, höchstens die letzten 20 Laufzeiten). Der neue Tab **Historie** des Seitenleisten-Panels zeigt sie unter dem jeweiligen Vertrag. Laufzeiten, die vor dieser Version endeten, gibt es nicht; die Historie beginnt mit dem nächsten Wechsel.
- **Abgelaufene Verträge archivieren.** Ein Vertrag, dessen Ende vorbei ist und für den kein Folgevertrag geplant ist, trägt in der Übersicht das Badge **Abgelaufen**. Administratoren können ihn im Tab "Verträge" archivieren (mit Rückfrage). Ein archivierter Vertrag verschwindet aus Übersicht, Kosten, Vertragsliste und Summen und steht in der Historie; seine Erinnerungen und Warnungen sind aus. Es wird nichts gelöscht, alle Sensoren und ihre Statistik bleiben, und **Zurückholen** holt den Vertrag wieder zurück. Nichts wird von allein archiviert: Bestehende Installationen sehen genauso aus wie vorher, bis jemand einen Vertrag archiviert.
- Beides liegt in internen Schlüsseln der Vertragsdaten (`_historie`, `_archiviert`): kein neuer Sensor, keine neue Entität. Beim Bearbeiten eines Vertrags bleiben sie erhalten.

## [1.27.3] - 2026-11-11

### Behoben

- **Das Seitenleisten-Panel war leer, wenn man nur Verträge einer Art hat** (zum Beispiel nur einen Strom-, Gas- oder Wasservertrag, oder nur Pauschalverträge wie Internet oder Mobilfunk). Die Übersicht brach mit „Failed to execute 'appendChild' on 'Node'" ab, weil sie eine Gruppe ohne Verträge einfügen wollte. Das Panel überspringt leere Gruppen jetzt. Gemeldet in #50.

## [1.27.2] - 2026-11-10

### Hinzugefügt

- **Diagnose-Download.** In Home Assistant unter Einstellungen > Geräte & Dienste > Tariffy > Menü des Vertrags > „Diagnose herunterladen" gibt es eine Datei mit den Einstellungen, den zuletzt berechneten Werten, ob das letzte Update geklappt hat, wie der Verbrauch ermittelt wurde (manueller Startwert oder Statistik, mit den Rohwerten) und dem Zustand des Zählersensors. Kundennummer, Zählernummer, Marktlokation (MaLo-ID) und Benachrichtigungsziel sind geschwärzt. Diese Datei bitte an eine Fehlermeldung anhängen.
- **Eine Zeile im Log, wenn der Verbrauch unbekannt wird.** Kann „Verbrauch (Bisher)" nicht berechnet werden, schreibt Tariffy eine Warnung mit dem Grund in das Home-Assistant-Protokoll (ohne Debug-Protokollierung), und eine Info-Zeile, sobald er wieder bekannt ist. Solange der Zustand gleich bleibt, wird nichts geloggt, das Protokoll läuft also nicht voll.

## [1.27.1] - 2026-11-10

### Behoben

- **Verbrauchs- und Guthaben-Sensoren fielen zeitweise auf "Unbekannt", wenn ein "Zählerstand bei Vertragsbeginn" eingetragen war und der Zähler kurz nicht verfügbar war** (Wasser, Gas, Strom, auch das Niedertarif-Register beim Zweizählertarif). Mit manuellem Startwert wurde nur der Live-Zustand des Zählers gelesen. Ist er `unavailable` oder `unknown`, wird jetzt der zuletzt aufgezeichnete Statistikwert verwendet. Ohne jeden Messwert bleiben die Sensoren wie bisher unbekannt. Gemeldet in #46.

## [1.27.0] - 2026-11-07

### Added

- **Seitenleisten-Panel "Tariffy".** Ein neuer Eintrag in der Seitenleiste zeigt alle Verträge auf einen Blick, mit Live-Werten, auf Deutsch und Englisch (dunkles, kartenbasiertes Design, kompakte aufklappbare Ansicht auf dem Handy). Es hat drei Ansichten: die **Übersicht** (vier Kopfkacheln mit den Abschlägen pro Monat, den Kosten bisher, der Prognose zum Vertragsende und den nächsten Terminen; darunter die Verbrauchsverträge und die Pauschalverträge mit je einer Karte), die **Kosten** (zwei Tabellen mit Summen) und die **Verträge** (Liste mit allen Details). Das Panel wird von der Integration mitgeliefert, nutzt die Systemschrift, braucht keinen Build-Schritt und keine zusätzlichen Entitäten. Alle, die Home Assistant benutzen dürfen, sehen die Werte; Kundennummern, Zählernummern, MaLo-ID und Benachrichtigungsziel werden nie an das Panel gesendet. Lässt sich das Panel nicht einrichten, steht eine Warnung im Log und die Integration arbeitet wie bisher. Siehe `docs/wiki/Panel.md` (deutsch) und `docs/wiki/English.md`.
- **Administratoren können Verträge im Panel bearbeiten**, im Tab "Verträge": die Abschlag-Warnung und die Kündigungs-Erinnerung bestätigen, den Folgevertrag planen, bearbeiten oder entfernen, einen Vertrag bearbeiten, einen neuen Vertrag anlegen und einen löschen. Alles läuft über die vorhandenen Dialoge von Home Assistant (Optionen, Neu konfigurieren, Einrichtung), Prüfung und Speicherung bleiben also unverändert, und jede Aktion fragt ein zweites Mal nach (zum Löschen muss der Vertragsname getippt werden). Ein "Jetzt wechseln" bietet das Panel nicht an: Der Vertrag wechselt am geplanten Datum von selbst. Benutzer ohne Administratorrechte sehen nur die Werte; das Backend prüft die Rechte zusätzlich.
- Die Vertragsdaten enthalten die bis heute fälligen Abschläge (`abschlag_bisher_gezahlt`; endet am Vertragsende und berücksichtigt eine Abschlagsänderung). Das ist nur ein Wert für das Panel: kein neuer Sensor, bestehende Installationen bekommen keine neuen Entitäten.

### Changed

- Deckt das Guthaben die Kosten bis zum Vertragsende schon ab, zeigt das Panel "Kein Abschlag nötig: Das Guthaben deckt die Kosten bis Vertragsende" statt einer negativen Empfehlung; sonst steht dort "Abschlag auf ... pro Monat erhöhen" oder "Abschlag könnte auf ... pro Monat sinken". Der Sensor "Abschlag-Anpassung (empfohlen)" selbst ist unverändert.
- Das Panel nennt "Saldo bisher" jetzt "Saldo heute" und erklärt, wenn der Saldo heute und die Prognose in verschiedene Richtungen gehen (zum Beispiel Rückstand heute, Guthaben am Ende).
- Pauschalverträge (Internet, Mobilfunk, Versicherung, Sonstiges) haben eigene Karten und eine eigene Tabelle. Ihre Kosten bisher sind die bis heute fälligen Abschläge.
- CI: Der Release-Workflow läuft auch auf dem Branch `beta` und veröffentlicht Vorabversionen wie `1.27.0-rc.1` (nie als "latest" markiert, damit HACS sie nur Nutzern anbietet, die Beta-Versionen eingeschaltet haben). Stabile Releases von `main` funktionieren wie bisher. Siehe `docs/beta-releases.md`.

### Fixed

- Beim Löschen eines Vertrags (im Panel oder in Home Assistant) werden jetzt auch seine offenen Kündigungs- und Abschlag-Benachrichtigungen entfernt. Bisher blieben sie dauerhaft in der Benachrichtigungsliste.
- Das Dropdown "Kündigungs-Erinnerung" zeigt "3 Monate vorher" statt einer nackten "3" (die Texte gab es schon, sie waren nur nicht verbunden). Die gespeicherten Werte bleiben unverändert.

## [1.26.7] - 2026-11-06

### Fixed

- **Beim Neukonfigurieren eines Vertrags gehen die Werte, die die Integration selbst führt, nicht mehr verloren.** Der Dialog "Neu konfigurieren" von Home Assistant ersetzt die gespeicherten Vertragsdaten durch das, was seine Formulare enthalten. Die Formulare enthalten die eigenen Werte der Integration nicht, deshalb kam nach jedem Neukonfigurieren eine bestätigte Kündigungs-Erinnerung oder Abschlag-Warnung wieder, eine schon gesendete Push-Nachricht konnte erneut gesendet werden, und der Verbrauch der letzten Laufzeit (Grundlage des empfohlenen Abschlags nach einem Tarifwechsel) ging verloren. Diese Werte bleiben jetzt erhalten. Die Kündigungs-Erinnerung beginnt nur dann neu, wenn sich Vertragsende oder Vorlaufzeit ändern. Sonst ändert sich nichts: Alle Felder der Formulare werden genau wie bisher gespeichert.

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

[Unreleased]: https://github.com/weskona/tariffy/compare/v1.27.0...HEAD
[1.27.0]: https://github.com/weskona/tariffy/compare/v1.26.7...v1.27.0
[1.26.7]: https://github.com/weskona/tariffy/compare/v1.26.6...v1.26.7
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
