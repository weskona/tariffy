🇩🇪 Deutsch · [🇬🇧 English](EN-Panel-Permissions-and-Design)

# Panel: Rechte und Design

Diese Seite erklärt, **wer im Tariffy-Panel was sieht und darf** (Administratoren und andere Benutzer), wie das **helle und dunkle Design** und die **Handy-Ansicht** funktionieren, was Du siehst, wenn es **keine Verträge** gibt oder das **Laden fehlschlägt**, und was das Panel bewusst **nicht** tut.

**Inhalt:**
- [Administratoren und andere Benutzer](#administratoren-und-andere-benutzer)
- [Persönliche Daten](#persönliche-daten)
- [Helles und dunkles Design](#helles-und-dunkles-design)
- [Handy-Ansicht](#handy-ansicht)
- [Leerer Zustand und Fehlerzustand](#leerer-zustand-und-fehlerzustand)
- [Beispiel: derselbe Vertrag mit zwei Benutzern](#beispiel-derselbe-vertrag-mit-zwei-benutzern)
- [Was das Panel nicht tut](#was-das-panel-nicht-tut)
- [Fehlerbehebung](#fehlerbehebung)
- [Siehe auch](#siehe-auch)

## Administratoren und andere Benutzer

Das Panel sehen **alle Benutzer** von Home Assistant, aber nicht alle dürfen alles. Entscheidend ist, ob das Benutzerkonto in Home Assistant Administrator ist.

| | Alle Benutzer | Nur Administratoren |
|---|---|---|
| Tabs **Übersicht**, **Kosten**, **Verträge**, **Historie** ansehen | ja | ja |
| Tab **Sicherung** | nicht sichtbar | ja ([Panel-Sicherung](Panel-Sicherung)) |
| Vertragsdetails mit ausgewählten Werten | ja | ja |
| Kundennummer, Zählernummer(n), Marktlokations-ID mit Kopieren-Symbol | nein | ja |
| Symbole in der Vertragsliste (Stift, Kalender, Verlängern) und **"Neuer Vertrag"** | nein | ja |
| **"Warnung bestätigen"**, **"Kündigung bestätigen"**, Archivieren, Zurückholen | nein | ja |
| **Alten Vertrag hinzufügen**, Laufzeiten bearbeiten | nein | ja |
| Einmalposten, gezahlte Abschläge und Außenzähler ändern | nein | ja |
| Vertrag bearbeiten, löschen, verlängern, Folgevertrag planen | nein | ja |

Die Prüfung gibt es doppelt: Das Panel blendet die Buttons und Dialoge für andere Benutzer aus, und das **Backend prüft es zusätzlich**. Ein Nicht-Administrator kann die Aktionen auch über die Schnittstelle nicht auslösen. Für andere Benutzer ist der Block **Einmalposten** (und ähnlich die Blöcke Gezahlte Abschläge und Außenzähler) nur sichtbar, wenn es Einträge gibt.

> **Gut zu wissen:** Siehst Du keine Buttons, bist Du wahrscheinlich nicht als Administrator angemeldet. Das ist Absicht und kein Fehler.

## Persönliche Daten

Persönliche Angaben werden nur an Administratoren geschickt:

- **Alle Benutzer** bekommen **nicht**: Kundennummer, Zählernummern, Marktlokations-ID, Kennzeichen, Benachrichtigungs-Ziel und interne Markierungen. Sie werden gar nicht erst ans Panel gesendet, andere Browser bekommen sie nie.
- **Administratoren** sehen zusätzlich **Kundennummer, Zählernummer(n) und Marktlokations-ID** im Block **Vertrag** der Vertragsdetails (Tab **Verträge**), jeweils mit einem Symbol zum **Kopieren** („Kopiert" bestätigt es). **Kennzeichen** und **Benachrichtigungs-Ziel** bleiben auch für sie verborgen.
- Die **Sicherungsdatei** enthält persönliche Daten, siehe [Panel-Sicherung](Panel-Sicherung).

## Helles und dunkles Design

Das Panel folgt dem **Design von Home Assistant**: Ist Home Assistant (nach Profil, automatischer Umschaltung oder Systemeinstellung) im **hellen** Modus, zeigt Tariffy helle Farben, sonst dunkle. Meldet Home Assistant keinen Modus, entscheidet die Systemeinstellung des Browsers. Es gibt dafür keine eigene Einstellung in Tariffy. Ein Wechsel in Home Assistant gilt sofort, ohne die Seite neu zu laden. Die Farben für Guthaben, Nachzahlung und Warnungen sind im hellen Modus dunkler, damit sie lesbar bleiben.

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/desktop-costs.png" alt="Tab Kosten im dunklen Design: dunkler Hintergrund, helle Schrift, rote und grüne Beträge" width="100%"></p>

*Abbildung: Der Tab Kosten im dunklen Design.*

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/desktop-costs-light.png" alt="Tab Kosten im hellen Design: heller Hintergrund, dunkle Schrift, abgedunkelte rote und grüne Beträge" width="100%"></p>

*Abbildung: Derselbe Tab im hellen Design. Die Beträge für Guthaben und Nachzahlung sind dunkler getönt.*

## Handy-Ansicht

Das Panel passt sich der Breite an, nicht dem Gerät: Ist es höchstens etwa 760 Pixel breit (Handy, schmales Fenster), stehen die Kacheln untereinander und die Vertragskarten werden **aufklappbare Zeilen**, die Tabellen werden Karten mit einer Zeile je Spalte. Auf dem Handy erscheint bei schmalem Home Assistant oben links der Menü-Knopf. Auf einem breiten Bildschirm stehen mehr Karten nebeneinander.

<table align="center"><tr><td align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-overview.png" alt="Übersicht auf dem Handy: Kacheln untereinander und Verträge als zugeklappte Zeilen (dunkles Design)" width="300"><br><sub>Dunkel</sub></td><td align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/mobile-overview-light.png" alt="Übersicht auf dem Handy: Kacheln untereinander und Verträge als zugeklappte Zeilen (helles Design)" width="300"><br><sub>Hell</sub></td></tr></table>

*Abbildung: Die Übersicht in schmaler Ansicht.*

Die einzelnen Tabs in der Handy-Ansicht siehst Du auf den Seiten [Panel-Uebersicht](Panel-Uebersicht), [Panel-Kosten](Panel-Kosten), [Panel-Vertraege](Panel-Vertraege), [Panel-Historie](Panel-Historie) und [Panel-Sicherung](Panel-Sicherung).

## Leerer Zustand und Fehlerzustand

Während das Panel lädt, steht „Verträge werden geladen ...". Zwei Zustände zeigen, dass etwas fehlt:

- **Noch keine Verträge:** Es gibt keinen Vertrag. Das Panel zeigt „Noch keine Verträge", den Text „Lege einen Vertrag unter Einstellungen → Geräte & Dienste → Tariffy an." und den Link **Vertrag anlegen**.
- **Fehler beim Laden:** Das Panel zeigt „Das Panel konnte die Verträge nicht laden." und darunter die technische Meldung von Home Assistant.

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/state-empty.png" alt="Panel ohne Verträge: Tab-Leiste, darunter die Überschrift Noch keine Verträge, der Text zum Anlegen eines Vertrags und der Link Vertrag anlegen" width="100%"></p>

*Abbildung: Der leere Zustand.*

<p align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/state-error.png" alt="Panel im Fehlerzustand: die Überschrift Das Panel konnte die Verträge nicht laden und darunter die Meldung Unknown command" width="100%"></p>

*Abbildung: Der Fehlerzustand. Im Screenshot steht darunter „Unknown command." (ein Beispieltext aus der Testumgebung); in Deinem Home Assistant steht dort die Meldung, die Home Assistant liefert.*

Was Du tun kannst, steht im Abschnitt [Fehlerbehebung](#fehlerbehebung).

## Beispiel: derselbe Vertrag mit zwei Benutzern

Der Vertrag **Strom Haus** zeigt in der Übersicht für alle dasselbe: −495 € Prognose, Badge **Nachzahlung droht**. Im Tab **Verträge** unterscheiden sich die Konten:

| Was | Administrator | Anderer Benutzer |
|---|---|---|
| Zeile Strom Haus | Symbole Kalender und Stift vor dem Pfeil | nur der Pfeil |
| Aufgeklappt, Block **Vertrag** | zusätzlich Kundennummer und Zählernummer mit Kopieren-Symbol | nur Anbieter, Tarif, Beginn, Ende, Restlaufzeit, Erinnerung ab |
| Block **Einmalposten** | Posten, Stifte und **Posten hinzufügen** | nur die Posten (Wechselbonus +80,00 €, Honorar Makler −25,00 €) |
| Unter **Empfehlungen** | **"Warnung bestätigen"** | nur der Hinweis „Abschlag auf 127,66 € pro Monat erhöhen" |
| Tabs | Übersicht, Kosten, Verträge, Historie, **Sicherung** | Übersicht, Kosten, Verträge, Historie |

## Was das Panel nicht tut

- Es rechnet nichts selbst, sondern zeigt die Werte der Integration. Alle Werte sind dieselben wie bei den Sensoren ([Sensoren-Referenz](Sensoren-Referenz)).
- Es schreibt nur über die Dialoge von Home Assistant. Diese bleiben unter Einstellungen → Geräte & Dienste → Tariffy unverändert verfügbar; die Sensoren und Buttons der Integration bleiben unverändert.
- Es gibt keine Funktion „Jetzt wechseln": Der Wechsel zum Folgevertrag passiert zum geplanten Datum automatisch ([Panel-Vertraege](Panel-Vertraege)).
- Es archiviert und löscht nichts von allein.
- Es schickt Kundennummer, Zählernummern, Marktlokations-ID, Kennzeichen und Benachrichtigungs-Ziel nicht an Nicht-Administratoren.
- Es hat keine eigene Design-Einstellung: Hell oder dunkel kommt von Home Assistant.
- Es gibt das Panel erst, wenn mindestens ein Vertrag existiert.

## Fehlerbehebung

| Problem | Lösung |
|---|---|
| Kein Eintrag „Tariffy" in der Seitenleiste | Version in HACS prüfen (ab 1.27.0 gibt es das Panel), Home Assistant neu starten, Seite hart neu laden (Strg+F5). Im Profil prüfen, ob der Eintrag ausgeblendet ist. Im Log nach Meldungen „Tariffy: panel" suchen: Das Panel kann ausfallen, ohne die Verträge zu stören. |
| Panel schwarz oder leer | Seite hart neu laden (Strg+F5, am Handy: Seite neu laden oder App-Cache leeren). Hilft das nicht: Home Assistant neu starten und im Log nach „Tariffy: panel" suchen. |
| Panel zeigt alte Oberfläche oder fehlende Buttons | Seite hart neu laden, der Browser hat die alte Datei zwischengespeichert. |
| Keine Buttons zu sehen | Die Aktionen gibt es nur für Administratoren. |
| „Das Formular konnte nicht geladen werden" | Home Assistant war kurz nicht erreichbar oder der Vertrag ist gerade nicht geladen. Dialog schließen und neu öffnen. |
| „Das Panel konnte die Verträge nicht laden." | Seite neu laden, bei Dauerfehler im Log nach „Tariffy: panel" suchen und einen Fehler melden. |
| Einen Fehler melden | Mit dem [Fehlerformular](https://github.com/weskona/tariffy/issues/new/choose) und der genauen Version. |

Mehr Hilfe in [Fehlerbehebung](Fehlerbehebung) und [FAQ](FAQ).

## Siehe auch

- [Panel-Uebersicht](Panel-Uebersicht): der Einstieg ins Panel.
- [Panel-Vertraege](Panel-Vertraege): alle Aktionen für Administratoren.
- [Panel-Sicherung](Panel-Sicherung): der Tab nur für Administratoren.
- [Fehlerbehebung](Fehlerbehebung): allgemeine Hilfe.
