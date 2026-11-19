🇩🇪 Deutsch · [🇬🇧 English](EN-Home)

# Tariffy – Vertragsverwaltung für Home Assistant

Tariffy verwaltet Deine Energie- und Dienstleistungsverträge in Home Assistant: Strom, Gas, Wasser, Internet, Mobilfunk, Streaming, Versicherung, Kredit, Leasing und Sonstiges. Dieses Wiki erklärt Schritt für Schritt, wie Du Tariffy einrichtest und nutzt.

## Was Tariffy für Dich tut

- Jeder Vertrag wird ein eigenes Home-Assistant-Gerät mit Sensoren (Kosten, Saldo, Prognose und mehr).
- Mit einem Zähler-Sensor misst Tariffy den echten Verbrauch und rechnet Prognose und empfohlenen Abschlag daraus.
- Tariffy erinnert Dich rechtzeitig vor dem Ende der Kündigungsfrist und kann den Folgetarif am Wechseldatum automatisch übernehmen.
- Das Panel in der Seitenleiste zeigt alle Verträge, Kosten und die Historie, auch auf dem Handy, in hellem und dunklem Design.
- Sicherung und Wiederherstellung sind eingebaut; gelöschte Verträge bleiben 30 Tage wiederherstellbar.

<table align="center"><tr><td align="center" width="50%"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/desktop-overview.png" alt="Das Tariffy-Panel, Übersicht: Verträge, Kosten und Hinweise auf einen Blick (dunkles Design)" width="100%"><br><sub>Dunkel</sub></td><td align="center" width="50%"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/desktop-overview-light.png" alt="Das Tariffy-Panel, Übersicht: Verträge, Kosten und Hinweise auf einen Blick (helles Design)" width="100%"><br><sub>Hell</sub></td></tr></table>

*Abbildung: Übersicht im Panel (Mock-Daten, Datum 12.07.2026).*

## Schnellstart

1. [Erste Schritte](Erste-Schritte) – installieren, Integration anlegen, ersten Vertrag in fünf Minuten.
2. [Verträge anlegen](Vertraege-Anlegen) – alle Sparten und ihre Formularfelder.
3. [Verbrauch messen](Verbrauch-Messen) – Zähler-Sensor wählen, damit Prognosen echt werden.
4. [Das Panel](Panel-Uebersicht) – die fünf Ansichten.

## Alle Seiten

| Thema | Seiten |
|---|---|
| Start | [Erste Schritte](Erste-Schritte) · [Verträge anlegen](Vertraege-Anlegen) |
| Verträge je Sparte | [Strom](Vertrag-Strom) · [Gas](Vertrag-Gas) · [Wasser](Vertrag-Wasser) · [Internet und Mobilfunk](Vertrag-Internet-und-Mobilfunk) · [Streaming](Vertrag-Streaming) · [Versicherung](Vertrag-Versicherung) · [Leasing](Vertrag-Leasing) · [Kredit](Vertrag-Kredit) · [Sonstiges](Vertrag-Sonstiges) |
| Verbrauch | [Verbrauch messen](Verbrauch-Messen) · [PV-Autarkie](PV-Autarkie) |
| Abschläge und Kosten | [Abschläge und Kosten](Abschlaege-und-Kosten) · [Abschlagsverlauf und Einmalposten](Abschlagsverlauf-und-Einmalposten) |
| Vertragsende und Wechsel | [Vertragsende und Wechsel](Vertragsende-und-Wechsel) · [Folgevertrag oder Verlängern](Folgevertrag-oder-Verlaengern) · [Archiv und Historie](Archiv-und-Historie) |
| Panel | [Übersicht](Panel-Uebersicht) · [Kosten](Panel-Kosten) · [Verträge](Panel-Vertraege) · [Historie](Panel-Historie) · [Sicherung](Panel-Sicherung) · [Rechte und Design](Panel-Rechte-und-Design) |
| Referenz | [Sensoren](Sensoren-Referenz) · [Dashboard-Beispiele](Dashboard-Beispiele) · [Automationen](Automationen) |
| Betrieb | [Sicherung und Umzug](Sicherung-und-Umzug) · [FAQ](FAQ) · [Fehlerbehebung](Fehlerbehebung) |
| Projekt | [Releases und Beta](Releases-und-Beta) · [Für Entwickler](Entwickler) |

## Version und Status

Dieses Wiki beschreibt Tariffy **1.32.0** (Stable). Das Panel in der Seitenleiste gibt es seit 1.27. Neue Funktionen kommen zuerst als Beta-Version, siehe [Releases und Beta](Releases-und-Beta).

Quellcode, Releases und Changelog: [weskona/tariffy](https://github.com/weskona/tariffy) · [Changelog](https://github.com/weskona/tariffy/blob/main/CHANGELOG.md) · [Fehler melden](https://github.com/weskona/tariffy/issues)
