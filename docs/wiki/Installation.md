# Installation

## Installation via HACS

1. HACS → Integrationen → ⋮ → **Benutzerdefinierte Repositories**
2. URL: `https://github.com/weskona/tariffy` – Kategorie: **Integration**
3. Tariffy installieren → HA neu starten
4. Einstellungen → Integrationen → **Tariffy** → Hinzufügen

## Panel

Ab Version 1.27.0 bringt die Integration ein Seitenleisten-Panel mit. Es braucht keine Einrichtung, nach dem Update die Browserseite einmal hart neu laden (Strg+F5). Mehr dazu unter [Panel](Panel).

## Manuelle Installation

```bash
cp -r custom_components/tariffy /config/custom_components/
```
HA neu starten.

## Anforderungen

- Home Assistant 2026.6 oder neuer

