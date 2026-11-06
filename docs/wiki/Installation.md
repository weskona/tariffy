# Installation

## Installation via HACS

1. HACS → Integrationen → ⋮ → **Benutzerdefinierte Repositories**
2. URL: `https://github.com/weskona/tariffy` – Kategorie: **Integration**
3. Tariffy installieren → HA neu starten
4. Einstellungen → Integrationen → **Tariffy** → Hinzufügen

## Beta-Versionen (Panel)

Das Seitenleisten-Panel gibt es nur in Beta-Versionen. In HACS → Tariffy → ⋮ → **Neu herunterladen** die Option **Beta-Versionen anzeigen** einschalten und eine Version wie `1.27.0-beta.6` wählen. Mehr dazu unter [Panel (Beta)](Panel).

## Manuelle Installation

```bash
cp -r custom_components/tariffy /config/custom_components/
```
HA neu starten.

## Anforderungen

- Home Assistant 2026.6 oder neuer

