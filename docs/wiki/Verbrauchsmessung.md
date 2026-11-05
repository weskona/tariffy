# Verbrauchsmessung

## Echte Verbrauchsmessung

Wenn ein **Verbrauchssensor** eingetragen ist, liest Tariffy beim Vertragsbeginn den historischen Zählerstand aus den **Long-Term Statistics** und berechnet:

```
Verbrauch (Bisher)                          = aktueller Zählerstand − Zählerstand am Vertragsbeginn
Verbrauch (Vertragslaufzeit hochgerechnet)  = Verbrauch bisher ÷ vergangene Tage × Vertragslaufzeit (Tage)
Kosten (Bisher)                             = Verbrauch bisher × Arbeitspreis + Grundpreis × vergangene Monate
Guthaben/Nachzahlung (Bisher)                = Abschlag × vergangene Monate − Kosten (Bisher)
Guthaben/Nachzahlung (Vertragsende)           = Abschlag (Vertragslaufzeit) − hochgerechnete Kosten über Laufzeit
```

**Positiv** = Guthaben · **Negativ** = Nachzahlung

Die für die Hochrechnung verwendete Vertragslaufzeit ist `Vertragsende − Vertragsbeginn` in Tagen (Fallback 365 ohne Enddatum) — ein Vertrag über z. B. 6 Monate wird auf diese 6 Monate hochgerechnet, nicht auf ein volles Kalenderjahr.

Sowohl der aktuelle Zählerstand als auch der historische Wert zum Vertragsbeginn werden primär aus der kumulierten **`sum`-Statistik** des Recorders gelesen, nicht aus dem rohen Sensor-Zustand. Das macht die Berechnung robust gegenüber Sensoren mit `state_class: total_increasing`, die erlaubterweise periodisch zurücksetzen (manche Smart-Meter-Integrationen setzen ihren Rohzähler bei jedem Ablesezyklus zurück) — die `sum`-Statistik des Recorders berücksichtigt solche Resets bereits. Zusätzlich liest Tariffy aber auch den rohen `state`-Wert mit: ist der aktuelle Zählerstand nicht unter den Wert bei Vertragsbeginn gefallen (kein echter Reset), wird stattdessen die einfachere State-Differenz verwendet — das schützt vor seltenen Anomalien direkt in der `sum`-Statistik selbst (beobachtet z. B. nach einem HA-Neustart: die Statistik sprang plötzlich auf einen unplausiblen Wert, während der Zählerstand durchgehend korrekt blieb).

> Der Sensor muss Long-Term Statistics aktiviert haben. Reicht dessen Statistik-Historie trotzdem
> nicht bis zum Vertragsbeginn zurück (z. B. weil der Sensor zwischenzeitlich umbenannt oder neu
> angelegt wurde), kannst du optional einen **manuellen "Zählerstand bei Vertragsbeginn"**
> eintragen — der hat dann Vorrang vor beiden automatischen Methoden.


## Verbrauch letzte Laufzeit & empfohlener Abschlag

Beim Tarifwechsel friert Tariffy den Gesamtverbrauch der ablaufenden Vertragslaufzeit ein:

```
Verbrauch (Letzte Laufzeit) = Zählerstand am Wechseltag − Zählerstand am Vertragsbeginn
Abschlag (Empfohlen)        = (Letzte Laufzeit × neuer Arbeitspreis + neuer Grundpreis × Monate) / Monate
```

`Monate` ist die **tatsächliche Dauer der ablaufenden Vertragslaufzeit** in Monaten (eingefroren im Moment des Wechsels), nicht pauschal 12 — relevant, wenn der vorherige Vertrag kürzer oder länger als ein Jahr lief. Fallback auf 12, wenn die Laufzeit vor Einführung dieser Berechnung eingefroren wurde.

So erhält man eine datenbasierte Empfehlung für den monatlichen Abschlag im neuen Vertrag.
