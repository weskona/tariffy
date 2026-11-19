🇩🇪 Deutsch · [🇬🇧 English](EN-Troubleshooting)

# Fehlerbehebung

Diese Seite ist nach Symptomen sortiert: Was Du siehst, woran es liegt und was Du tust. Am Ende steht, wie Du Protokolle (Logs) und Diagnose für einen Fehlerbericht sammelst. Kurze Antworten auf häufige Fragen stehen in der [FAQ](FAQ).

**Inhalt:**
- [Das Panel ist leer oder schwarz](#das-panel-ist-leer-oder-schwarz)
- [Verbrauch oder Kosten bleiben leer](#verbrauch-oder-kosten-bleiben-leer)
- [Statistik reicht nicht bis zum Vertragsbeginn](#statistik-reicht-nicht-bis-zum-vertragsbeginn)
- [Falsche Einheit](#falsche-einheit)
- [Prognosen wirken falsch](#prognosen-wirken-falsch)
- [Sensoren erscheinen nicht](#sensoren-erscheinen-nicht)
- [Tarifwechsel hat nicht stattgefunden](#tarifwechsel-hat-nicht-stattgefunden)
- [Erinnerungen und Warnungen kommen nicht](#erinnerungen-und-warnungen-kommen-nicht)
- [Benachrichtigung auf dem Handy bleibt aus](#benachrichtigung-auf-dem-handy-bleibt-aus)
- [Sicherung und Wiederherstellung](#sicherung-und-wiederherstellung)
- [Fehlermeldungen im Formular](#fehlermeldungen-im-formular)
- [Warnung zum Update-Listener](#warnung-zum-update-listener)
- [Debug-Protokoll einschalten](#debug-protokoll-einschalten)
- [Diagnose herunterladen](#diagnose-herunterladen)
- [Fehlerbericht erstellen](#fehlerbericht-erstellen)

## Das Panel ist leer oder schwarz

| Symptom | Ursache | Lösung |
|---|---|---|
| Meldung „Noch keine Verträge" | Es gibt keinen Vertrag. | Vertrag unter Einstellungen → Geräte & Dienste → Tariffy anlegen (Link „Vertrag anlegen"). Das Panel gibt es erst ab dem ersten Vertrag; wurde der letzte Vertrag gelöscht, legst Du zuerst einen neuen an. |
| Meldung „Das Panel konnte die Verträge nicht laden." | Das Panel hat die Vertragsdaten nicht bekommen. | Seite hart neu laden (Strg+F5). Dann das Home-Assistant-Protokoll nach `tariffy` filtern. |
| Schwarze oder leere Fläche | Nach einem Update liegt noch eine alte Version im Browser-Cache. | Seite hart neu laden (Strg+F5). Bei Version 1.31.0 oder älter: auf 1.32.0 aktualisieren, dort sind das schwarze Panel und das leere Panel nach dem Anlegen eines Vertrags behoben. |
| Kein Seitenleisten-Eintrag „Tariffy" | Das Panel konnte nicht eingerichtet werden (zum Beispiel fehlt ein Frontend- oder HTTP-Dienst). Die Integration läuft dann ohne Panel weiter. | Im Protokoll nach `Tariffy: panel could not be set up` suchen und Home Assistant neu starten. |
| Keine Buttons im Panel | Aktionen gibt es nur für Administratoren. | Mit einem Administrator-Konto anmelden. |

## Verbrauch oder Kosten bleiben leer

Kosten, Guthaben und Prognose brauchen einen konfigurierten Arbeitspreis. „Kosten (Bisher)", „Guthaben/Nachzahlung (Bisher)" und „Guthaben/Nachzahlung (Vertragsende)" brauchen zusätzlich einen Verbrauchssensor. Der Sensor muss Langzeitstatistiken (Long-Term Statistics) haben, siehe [Verbrauch messen](Verbrauch-Messen).

1. Prüfe unter Entwicklerwerkzeuge → Zustände, ob der Verbrauchssensor existiert und einen Wert hat.
2. Prüfe in den Attributen des Sensors, dass `state_class` gesetzt ist (`total_increasing` oder `total`).
3. Ist der Verbrauch weiter leer, steht im Protokoll eine Warnung wie `Tariffy '<Vertrag>': Verbrauch bisher ist unbekannt (Sensor ...)` mit Einzelheiten. Das Protokoll meldet nur den Wechsel auf „unbekannt" und später „wieder bekannt".
4. Lade die [Diagnose](#diagnose-herunterladen) herunter: Der Block `verbrauch` zeigt, was Tariffy beim Berechnen gefunden hat, `zaehler` den aktuellen Zustand Deines Sensors (`state` steht auf `fehlt`, wenn die Entität nicht existiert).

## Statistik reicht nicht bis zum Vertragsbeginn

Wurde der Sensor umbenannt oder neu angelegt, trage unter den Vertragsdaten einen manuellen **„Zählerstand bei Vertragsbeginn (optional)"** ein. Er hat Vorrang vor den automatischen Methoden.

## Falsche Einheit

Die Sensoren „Verbrauch (Bisher)" und „Verbrauch (Vertragslaufzeit hochgerechnet)" zeigen die rohe Zählerdifferenz in der Einheit Deines Sensors (meist m³). Nur für die Kostenberechnung wird intern über Brennwert × Zustandszahl in kWh umgerechnet. Zeigt ein Sensor trotzdem eine unerwartete Einheit, stammt sie vom Verbrauchssensor: Die Diagnose nennt sie im Block `zaehler` unter `unit`.

## Prognosen wirken falsch

- **Der Wert ist sehr hoch oder sehr niedrig:** Prüfe den Zählerstand bei Vertragsbeginn und die Einheit des Sensors (siehe oben). Ein falscher Startwert verfälscht Verbrauch, Kosten und Prognose.
- **Das Vorzeichen irritiert:** Guthaben/Nachzahlung ist positiv bei Guthaben, negativ bei Nachzahlung.
- **Der Abschlag hat sich geändert:** Trage unter **Gezahlte Abschläge** ein, was ab wann gezahlt wurde, siehe [Abschlagsverlauf und Einmalposten](Abschlagsverlauf-und-Einmalposten).
- **PV-Anlage:** Ohne [PV-Autarkie](PV-Autarkie) überschätzt die Prognose im Winter den Rest der Laufzeit und unterschätzt ihn im Sommer.

## Sensoren erscheinen nicht

Sensoren für Nachttarif, Staffelpreise und Zweizählertarif (HT/NT) gibt es nur, wenn die jeweilige Sparte oder Option genutzt wird. Kredit und Leasing haben eigene Sensoren, andere Sparten bekommen sie nicht. Die Liste steht in der [Sensoren-Referenz](Sensoren-Referenz).

## Tarifwechsel hat nicht stattgefunden

Der Wechsel wird täglich um 00:00:01 Uhr, alle 6 Stunden und nach dem Start von Home Assistant geprüft. Über den Button **Jetzt wechseln** lässt er sich sofort auslösen. Das Panel hat dafür keinen Button: Der Vertrag wechselt dort von selbst zum geplanten Datum. Mehr dazu unter [Vertragsende und Wechsel](Vertragsende-und-Wechsel).

## Erinnerungen und Warnungen kommen nicht

- **Kündigungs-Erinnerung:** Sie braucht ein eingetragenes Vertragsende und einen Erinnerungszeitraum, der erreicht ist. Mit eingetragener Kündigungsfrist bezieht sich die Erinnerung auf den letzten Kündigungstag, nicht auf das Vertragsende. Die Meldung erscheint als Dauerbenachrichtigung im Benachrichtigungscenter, bis Du sie mit dem Button **Kündigung bestätigen** quittierst.
- **Abschlag-Warnung:** Sie ist standardmäßig aus. Aktiviere im Vertragsformular „Warnen, wenn Abschlag zu niedrig ist". Sie gilt für Strom, Gas und Wasser mit Verbrauchssensor und feuert, wenn die Prognose zum Vertragsende eine Nachzahlung über der Schwelle (Standard 50 €) erwarten lässt. Mit **Abschlag-Warnung bestätigen** quittierst Du sie; verschlechtert sich die Prognose später erneut, meldet sie sich neu.
- **Archivierte Verträge:** Ihre Erinnerungen und Warnungen sind aus (siehe [Archiv und Historie](Archiv-und-Historie)).
- **Gelöschte Verträge:** Ihre offenen Meldungen werden beim Löschen entfernt.

## Benachrichtigung auf dem Handy bleibt aus

Die Push-Benachrichtigung geht an den Dienst, den Du im Feld „Benachrichtigungs-Ziel (notify-Dienst)" eingetragen hast, zum Beispiel `notify.mobile_app`. Ist er nicht erreichbar, schreibt Tariffy `notify.<Dienst> nicht erreichbar (...)` ins Protokoll. Prüfe den Namen unter Entwicklerwerkzeuge → Aktionen. Die Dauerbenachrichtigung im Benachrichtigungscenter erscheint unabhängig davon.

## Sicherung und Wiederherstellung

| Symptom | Ursache | Lösung |
|---|---|---|
| „Das ist keine gültige Tariffy-Sicherung." | Die Datei ist keine Tariffy-Sicherung oder wurde verändert. Tariffy prüft streng: nur bekannte Einstellungen, nur einfache Werte, höchstens 1 MB und 200 Verträge. | Die unveränderte Datei aus **Sicherung herunterladen** verwenden. |
| „Die Datei ist zu groß." | Die Datei überschreitet die Grenze. | Die Originaldatei verwenden, nichts von Hand ergänzen. |
| „Einen Vertrag mit diesem Namen und dieser Sparte gibt es schon." | Beim Zurückholen gibt es schon einen Vertrag mit gleichem Namen und gleicher Sparte. | Den vorhandenen Vertrag umbenennen oder löschen und erneut zurückholen. |
| „Diese Sicherung gibt es nicht mehr." | Der Eintrag des gelöschten Vertrags ist älter als 30 Tage oder wurde mit **Jetzt vergessen** entfernt. | Aus einer Sicherungsdatei oder einem Home-Assistant-Backup wiederherstellen. |
| „Das Wiederherstellen ist fehlgeschlagen." | Beim Anlegen ist etwas schiefgegangen. | Protokoll nach `tariffy` filtern und [Fehlerbericht](#fehlerbericht-erstellen) schreiben. |
| Verträge wurden beim Wiederherstellen übersprungen | Verträge mit gleichem Namen und gleicher Sparte werden nie verändert. | Das ist gewollt. |

Mehr zu den Funktionen steht unter [Panel: Sicherung](Panel-Sicherung) und [Sicherung und Umzug](Sicherung-und-Umzug).

## Fehlermeldungen im Formular

Diese Meldungen kommen aus dem Formular beim Anlegen oder Bearbeiten eines Vertrags:

| Meldung | Bedeutung und Lösung |
|---|---|
| „Keine gültige Zahl. Bitte Punkt oder Komma als Dezimaltrennzeichen verwenden (z.B. 11.2 oder 11,2)." | Ein Zahlenfeld enthält Text oder ein anderes Format. Nur Ziffern und Punkt oder Komma eingeben. |
| „Trage eine Kreditsumme über null ein." | Beim Kredit fehlt die Summe oder sie ist 0. |
| „Trage den Sollzins oder den effektiven Jahreszins ein." | Beim Kredit fehlen beide Zinsfelder. |
| „Trage einen Wert oder zwölf Werte zwischen 0 und 100 ein, getrennt durch Leerzeichen oder Semikolon." | Eigene PV-Autarkie-Werte sind kein Wert oder zwölf Werte zwischen 0 und 100, zum Beispiel `10 10 25 50 70 80 85 80 60 35 15 10`. |
| „Ohne Sensor ändert ein gleicher Wert für alle Monate nichts an der Prognose: Trage zwölf unterschiedliche Monatswerte (Januar bis Dezember) ein oder wähle einen Sensor." | Ein Wert allein ändert die Prognose nicht. Zwölf verschiedene Monatswerte eintragen oder einen Sensor wählen, siehe [PV-Autarkie](PV-Autarkie). |
| „Die Sicherung ist nicht gültig." | Tariffy hat beim Wiederherstellen einen Vertrag aus der Sicherung abgelehnt (Abbruch mit `invalid_backup`). Die Datei ist beschädigt oder verändert, siehe die Tabelle im Abschnitt Sicherung und Wiederherstellung. |

## Warnung zum Update-Listener

Die Home-Assistant-Warnung „update listener … should use it for scheduling a reload" ist in Tariffy 1.26.3 behoben ([Issue 2](https://github.com/weskona/tariffy/issues/2)). Aktualisiere Tariffy.

## Debug-Protokoll einschalten

Der Logger der Integration heißt `custom_components.tariffy`. Trage in der `configuration.yaml` ein:

```yaml
logger:
  logs:
    custom_components.tariffy: debug
```

Starte Home Assistant neu, stelle das Problem nach und öffne Einstellungen → System → Protokolle. Filtere nach `tariffy` und kopiere die passenden Zeilen. Entferne danach den Eintrag wieder, damit das Protokoll nicht unnötig anwächst.

## Diagnose herunterladen

Zu jedem Vertrag gibt es einen Diagnose-Download von Home Assistant (Einstellungen → Geräte & Dienste → Tariffy → beim Vertrag im Menü ⋮ den Eintrag zum Herunterladen der Diagnose). Die Datei enthält:

- `entry`: Titel, Vertragsdaten und Optionen
- `update`: ob die letzte Berechnung erfolgreich war, die letzte Ausnahme und das Intervall
- `verbrauch`: was Tariffy beim Ermitteln des Verbrauchs gefunden hat
- `zaehler` und `zaehler_nt`: Zustand, Einheit und `state_class` des Verbrauchssensors (und des Niedertarif-Sensors)
- `daten`: die berechneten Werte des Vertrags

**Geschwärzt** sind Kennzeichen, Kundennummer, Marktlokation, Benachrichtigungs-Ziel und Zählernummer(n). Nicht geschwärzt sind unter anderem Vertragsname, Anbieter, Tarif, Preise und die Entity-IDs. Schau die Datei trotzdem durch, bevor Du sie öffentlich anhängst.

## Fehlerbericht erstellen

Öffne ein [Issue mit dem Formular „Bug Report"](https://github.com/weskona/tariffy/issues/new/choose). Pflichtangaben sind die Tariffy-Version (HACS → Tariffy, oder `custom_components/tariffy/manifest.json`), die Home-Assistant-Version, die Installationsart (HACS oder manuell), was betroffen ist, die Sparte und eine Beschreibung des Problems mit den Schritten zum Nachstellen. Bei Verbrauchs- und Kostenproblemen helfen zusätzlich:

1. die Entity-ID des Verbrauchssensors (bei Zweizählertarif auch des Niedertarif-Sensors) und dessen `state_class`
2. das Vertragsbeginn-Datum
3. Protokollzeilen mit `tariffy` (am besten mit [Debug-Protokoll](#debug-protokoll-einschalten))
4. die [Diagnose](#diagnose-herunterladen)

Bei Beta-Versionen nenne die genaue Version, zum Beispiel `1.33.0-beta.1`. Das Formular verlangt, dass Du die neueste Version nutzt, vorhandene Issues durchsucht und persönliche Daten (Kundennummer, Zählernummer, Marktlokations-ID, Tokens) durch `xxx` ersetzt hast. Fragen zur Bedienung gehören in die [Discussions](https://github.com/weskona/tariffy/discussions), Ideen in das Formular „Feature Request".

> **Gut zu wissen:** Der Titel des Issues soll mit ein paar Worten beginnen statt mit `<short summary>`, zum Beispiel „Consumption (so far) too high".

## Siehe auch

- [FAQ](FAQ)
- [Verbrauch messen](Verbrauch-Messen)
- [Panel: Sicherung](Panel-Sicherung)
- [Releases und Beta](Releases-und-Beta)
- [Entwickler](Entwickler)
