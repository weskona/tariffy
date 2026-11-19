🇩🇪 Deutsch · [🇬🇧 English](EN-Development)

# Entwickler

Diese Seite ist für alle, die an Tariffy mitarbeiten oder die Dokumentation pflegen: Projektaufbau, Tests, die Vorschau des Panels, Screenshots, den Dokumentations-Check und das Wiki.

**Inhalt:**
- [Projektstruktur](#projektstruktur)
- [Tests und Lint](#tests-und-lint)
- [Vorschau des Panels](#vorschau-des-panels)
- [Screenshots neu erzeugen](#screenshots-neu-erzeugen)
- [Dokumentation prüfen](#dokumentation-prüfen)
- [Wiki veröffentlichen](#wiki-veröffentlichen)
- [Fehler melden](#fehler-melden)

## Projektstruktur

Alles, was Home Assistant lädt, liegt in `custom_components/tariffy/`:

| Datei | Aufgabe |
|---|---|
| `__init__.py` | Einrichten und Entladen eines Vertrags, richtet das Panel ein, räumt beim Löschen Meldungen auf und merkt sich den gelöschten Vertrag |
| `manifest.json` | Domain, Version, Abhängigkeiten (`after_dependencies`) und Links |
| `const.py` | Konstanten: Domain, Plattformen, Sparten, Namen der Einstellungsfelder |
| `config_flow.py` | Einrichten, Bearbeiten (Reconfigure) und Optionen (Folgevertrag), je nach Sparte |
| `coordinator.py` | Berechnung aller Werte, Tarifwechsel, Kündigungs-Erinnerung, Abschlag-Warnung |
| `sensor.py` | Die Sensoren eines Vertrags |
| `button.py` | Die Buttons „Jetzt wechseln", „Kündigung bestätigen" und „Abschlag-Warnung bestätigen" |
| `panel.py` | Seitenleisten-Panel, Datenschnittstelle (WebSocket) und Rechteprüfung |
| `backup.py` | Sicherung, Wiederherstellung und die 30 Tage für gelöschte Verträge |
| `history.py` | Alte Laufzeiten von Hand in die Historie eintragen |
| `autarkie.py` | Rechnung der PV-Autarkie in der Prognose |
| `leasing.py` | Rechnung für Leasing (Kilometer) |
| `loan.py` | Tilgungsplan für Kredite |
| `diagnostics.py` | Diagnose-Download mit Schwärzung persönlicher Daten |
| `strings.json` | Texte des Formulars (Englisch, Grundlage der Übersetzungen) |
| `translations/de.json`, `translations/en.json` | Deutsche und englische Texte |
| `frontend/tariffy-panel.js` | Code des Panels |
| `frontend/tariffy-i18n.js` | Texte des Panels (Deutsch und Englisch) |
| `frontend/tariffy-icons.js` | Symbole des Panels |
| `frontend/tariffy-style.js` | Stile des Panels |
| `brand/icon.png` | Symbol der Integration |
| `CHANGELOG.md`, `README.md` | Eigene Fassungen für die Integration; beide Changelogs werden gepflegt (siehe [Releases und Beta](Releases-und-Beta#regeln-für-mitwirkende)) |

Weitere Verzeichnisse im Repository:

| Pfad | Inhalt |
|---|---|
| `tests/` | Alle Tests (`test_*.py`) und die Panel-Vorschau in `tests/frontend/` |
| `docs/wiki/` | Quellen des Wikis (diese Seiten) und `docs/wiki/images/` mit den Bildern |
| `docs/beta-releases.md` | Beschreibung des Beta-Wegs |
| `scripts/check_wiki.py` | Prüfung der Wiki-Seiten |
| `.github/` | Workflows (`release.yml`, `validate.yml`), Release-Skripte und die Issue-Formulare |
| `hacs.json`, `pytest.ini`, `requirements_test.txt`, `ruff.toml` | Einstellungen für HACS, Tests und Lint |

Das Panel baut auf den vier Dateien in `frontend/` auf; der Code lädt die anderen drei mit einer eigenen `?v=`-Version, weil der statische Pfad lange zwischengespeichert wird.

## Tests und Lint

Die Tests nutzen `pytest-homeassistant-custom-component`. In `pytest.ini` stehen `asyncio_mode = auto`, `testpaths = tests` und `pythonpath = .`. Die CI nutzt Python 3.13.

```bash
pip install -r requirements_test.txt
pytest
```

Lint mit Ruff, wie in der CI (nur Korrektheitsregeln `E9` und `F`, Ziel `py312`):

```bash
ruff check custom_components
```

Die Release-Skripte haben eigene Tests:

```bash
.github/scripts/test-release-notes.sh
.github/scripts/test-release-plan.sh
```

Ein einzelner Test, zum Beispiel für die Issue-Formulare:

```bash
pytest tests/test_issue_templates.py
```

> **Gut zu wissen:** Lass vor jedem Push die volle Suite und Ruff laufen. Die CI (`validate.yml`) prüft zusätzlich HACS und Hassfest.

## Vorschau des Panels

Das Verzeichnis `tests/frontend/` enthält Beispieldaten und eine Vorschau des Panels:

- `fixtures.json`: Das, was `tariffy/contracts` für sechs realistische Verträge liefert, erzeugt vom **echten Backend**. `tests/test_panel_fixtures.py` schlägt fehl, wenn die Datei veraltet ist.
- `preview.html`: Lädt das Panel mit einem Mock-`hass`.

Neu erzeugen:

```bash
UPDATE_FIXTURES=1 pytest tests/test_panel_fixtures.py
```

Vorschau öffnen: Starte im Hauptverzeichnis des Repositorys einen Webserver und öffne die Seite.

```bash
python -m http.server
```

Dann `/tests/frontend/preview.html?lang=de` im Browser öffnen. Parameter: `lang=de|en`, `state=loading|empty|error`, `narrow=1` und `theme=light|dark`.

## Screenshots neu erzeugen

Zwei Skripte rendern die Vorschau im Headless-Chromium mit dem Datum 2026-07-12 und schreiben Screenshots:

- `tests/frontend/screenshots.mjs`: alle Screenshots im dunklen Design
- `tests/frontend/screenshots-light.mjs`: die Hauptscreenshots (deutsch am Desktop und Handy, englisch bei 960 px, alle fünf Tabs) im hellen Design, als `*-light.png` neben den dunklen

```bash
node tests/frontend/screenshots.mjs [Zielordner]
node tests/frontend/screenshots-light.mjs [Zielordner]
```

Beide brauchen Playwright mit einem Chromium-Browser und sind **nicht Teil der CI**. Ohne Zielordner schreibt `screenshots.mjs` nach `docs/panel-preview/`; für das Wiki gibst Du `docs/wiki/images` an. Das Wiki nutzt zu den Bildern mit Hell-Variante ein `<picture>`-Element, das je nach Farbschema des Besuchers die helle oder dunkle Datei zeigt.

## Dokumentation prüfen

```bash
python3 scripts/check_wiki.py
```

Das Skript prüft die Seiten in `docs/wiki/`: Links und Anker, Bilder (Datei vorhanden, höchstens 500 KB), Mermaid-Blöcke und ob zu jeder deutschen Seite die englische Seite mit gleichem Aufbau existiert. Bei einem Problem endet es mit dem Exit-Code 1. Zusätzlich prüft `tests/test_docs.py` in der Test-Suite, dass die Dokumentation nicht auf Dinge verweist, die es nicht gibt.

## Wiki veröffentlichen

Das GitHub-Wiki ist ein eigenes Repository (`weskona/tariffy.wiki`). Die Quellen liegen in `docs/wiki/` und werden hineinkopiert:

1. Wiki-Repository klonen: `git clone https://github.com/weskona/tariffy.wiki.git`
2. Alle `*.md`-Dateien aus `docs/wiki/` hineinkopieren.
3. Den Ordner `docs/wiki/images/` als `images/` hineinkopieren.
4. Committen und pushen.

```bash
cp docs/wiki/*.md ../tariffy.wiki/
cp -r docs/wiki/images ../tariffy.wiki/
```

Die Bilder verweisen auf `https://raw.githubusercontent.com/wiki/weskona/tariffy/images/<Datei>`, also genau auf den Ort, an dem sie nach dem Kopieren liegen. Deshalb müssen die Pfade im Wiki-Repository `images/<Datei>` lauten.

## Fehler melden

Nutze das Formular „Bug Report" unter [Issues](https://github.com/weskona/tariffy/issues/new/choose) und gib an:

1. die **Version** von Tariffy und von Home Assistant
2. das **Protokoll** mit `tariffy` gefiltert, am besten mit Debug-Stufe (siehe [Fehlerbehebung](Fehlerbehebung#debug-protokoll-einschalten))
3. die **Schritte**, mit denen sich das Problem nachstellen lässt

Entferne persönliche Daten wie Kundennummer, Zählernummer und Marktlokations-ID. Die Diagnose ([Fehlerbehebung](Fehlerbehebung#diagnose-herunterladen)) schwärzt sie schon. Die Issue-Formulare werden von `tests/test_issue_templates.py` geprüft.

## Siehe auch

- [Releases und Beta](Releases-und-Beta)
- [Fehlerbehebung](Fehlerbehebung)
- [Sensoren-Referenz](Sensoren-Referenz)
