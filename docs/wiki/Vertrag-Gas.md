🇩🇪 Deutsch · [🇬🇧 English](EN-Contract-Gas)

# Vertrag Gas

Hier findest Du alle Felder eines Gasvertrags und die Umrechnung von Kubikmetern in Kilowattstunden über Brennwert und Zustandszahl. Du brauchst beide Werte von Deiner Gasrechnung.

**Inhalt:**

- [So rechnet Tariffy bei Gas](#so-rechnet-tariffy-bei-gas)
- [Die Formularfelder](#die-formularfelder)
- [Umrechnung von Kubikmeter in kWh](#umrechnung-von-kubikmeter-in-kwh)
- [Zähler-Sensor und Einheiten](#zähler-sensor-und-einheiten)
- [Rechenbeispiel](#rechenbeispiel)
- [Typische Fehler](#typische-fehler)

## So rechnet Tariffy bei Gas

Der **Arbeitspreis** eines Gasvertrags gilt pro **kWh**, Dein Zähler zählt aber meist in **m³**. Tariffy misst den Verbrauch in der Einheit des Zählers und rechnet nur für die Kosten in kWh um:

```
Verbrauch (Bisher)        = aktueller Zählerstand − Zählerstand am Vertragsbeginn   (in m³)
Verbrauch in kWh          = Verbrauch (Bisher) × Brennwert × Zustandszahl
Kosten (Bisher)           = Verbrauch in kWh × Arbeitspreis + Grundpreis × vergangene Monate
```

Saldo und Prognose rechnen genauso wie bei Strom (ein Monat zählt 30,44 Tage); die Formeln stehen auf [Vertrag Strom](Vertrag-Strom#so-rechnet-tariffy). Der Sensor **Verbrauch (Bisher)** zeigt weiterhin die Zählerdifferenz in m³, nicht in kWh.

## Die Formularfelder

Das zweite Formular heißt **Gas-Details** („Preise, Verbrauch (m³) und Umrechnung auf kWh über Brennwert und Zustandszahl.“).

| Feld | Pflicht | Beschreibung |
|---|---|---|
| Gaseinheit | ja | Abrechnungseinheit laut Gasrechnung: `m³`, `CCF`, `therm`, `ft³`, `MBtu` oder `kWh` (Voreinstellung `m³`). |
| Arbeitspreis (€/kWh) | ja | Preis pro kWh Gas, steht auf Deiner Gasrechnung. |
| Grundpreis (€/Monat) | ja | Monatlicher Festbetrag unabhängig vom Verbrauch. |
| Monatlicher Abschlag (€/Monat) | ja | Monatliche Vorauszahlung an den Anbieter. |
| Geschätzter Jahresverbrauch (m³) | nein | Schätzung in der gewählten Einheit. Daraus entsteht der Sensor **Jahresverbrauch (kWh)**. Kosten bisher und Prognose rechnen mit dem gemessenen Verbrauch. |
| Verbrauchssensor (optional) | nein | Sensor Deines Gaszählers; ermöglicht die echte Verbrauchsmessung. |
| Zählerstand bei Vertragsbeginn (optional) | nein | Dein genauer Zählerstand am Vertragsbeginn, falls Du ihn kennst. Hat Vorrang vor der automatischen Erkennung. |
| Brennwert (kWh/m³) | ja | Brennwert Hs in kWh pro Einheit, steht auf der Gasrechnung (Voreinstellung 11,0). |
| Zustandszahl | ja | Zustandszahl Z für die Gasvolumenumrechnung, steht auf der Gasrechnung (meist 0,9 bis 1,0; Voreinstellung 0,95). |
| Warnen, wenn Abschlag zu niedrig ist | nein | Aus nach der Voreinstellung. Wirkt wie bei [Vertrag Strom](Vertrag-Strom#die-formularfelder) beschrieben. |
| Warnschwelle (€ Nachzahlung) | nein | Voreinstellung 50. |
| Neukundenbonus / Sofortbonus (€) | nein | Wird gespeichert, fließt aber nicht in die Kosten ein. Für einen Bonus im Saldo nutzt Du einen Einmalposten. |
| Ökostrom | ja | Ja oder Nein, nur zur Dokumentation (das Feld heißt auch bei Gas so). |
| Zählernummer | nein | Zur Dokumentation. |
| Marktlokation (MaLo-ID) / Zählpunkt | nein | Zur Dokumentation. |
| Preisgarantie bis | nein | Datum, bis zu dem der Arbeitspreis garantiert ist. |

Je nach dem in Home Assistant eingestellten Land kommen die Felder für **Staffelpreise** und den **Nachttarif** dazu. Sie funktionieren wie bei Strom und stehen auf [Vertrag Strom](Vertrag-Strom#staffelpreise). Dynamischer Tarif, Einspeisevergütung, PV-Autarkie und Zweizählertarif gibt es bei Gas nicht.

> **Gut zu wissen:** **Brennwert** und **Zustandszahl** sind Textfelder. Du kannst sie mit Dezimalpunkt (`11.2`) oder Dezimalkomma (`11,2`) eintragen. Alles andere meldet „Keine gültige Zahl. Bitte Punkt oder Komma als Dezimaltrennzeichen verwenden (z.B. 11.2 oder 11,2).“

## Umrechnung von Kubikmeter in kWh

Für die Einheiten `m³`, `CCF` und `ft³` gilt:

```
kWh = Menge × Brennwert × Zustandszahl
```

- Der **Brennwert** (Hs) sagt, wie viel Energie in einer Einheit Gas steckt (ungefähr 10 bis 12 kWh pro m³).
- Die **Zustandszahl** (Z) rechnet das Gasvolumen auf den Normzustand um (ungefähr 0,95).

Für `therm`, `MBtu` und `kWh` rechnet Tariffy die **Jahresverbrauch-Schätzung** mit festen Faktoren um und braucht dafür keinen Brennwert: 1 therm = 29,3071 kWh, 1 MBtu = 293,071 kWh, 1 kWh = 1 kWh.

Die Umrechnung der Schätzung zeigt der Sensor **Jahresverbrauch (kWh)** (Symbol `mdi:fire`). Seine Attribute nennen die Schätzung in m³, den Brennwert und die Zustandszahl.

> **Gut zu wissen:** Die Kostenrechnung aus dem Zählerverbrauch (**Kosten (Bisher)**, Prognose, empfohlener Abschlag) multipliziert immer mit **Brennwert × Zustandszahl**, sobald beide eingetragen sind, auch bei `therm`, `MBtu` und `kWh`. Beide Felder sind im Formular Pflicht. Meldet Dein Zähler schon in kWh, trägst Du daher Brennwert 1 und Zustandszahl 1 ein, damit die Umrechnung nichts verändert.

## Zähler-Sensor und Einheiten

- Der **Verbrauchssensor** liefert den Zählerstand, zum Beispiel in m³. Tariffy liest daraus den Stand zum Vertragsbeginn und den aktuellen Stand, wie bei [Verbrauch messen](Verbrauch-Messen) beschrieben. Auch Gaszähler, die zwischendurch zurückspringen, kommen damit zurecht.
- Die Sensoren **Verbrauch (Bisher)**, **Verbrauch (Vertragslaufzeit hochgerechnet)** und **Verbrauch (Letzte Laufzeit)** zeigen die Einheit des Zählersensors, falls er eine hat, sonst die gewählte **Gaseinheit**. Meldet der Zähler in Wh oder MWh, steht dort kWh.
- Der **Arbeitspreis** hat die Einheit „Währung pro kWh“.

## Rechenbeispiel

Ein Gasvertrag mit Arbeitspreis 0,10 €/kWh, Grundpreis 10,00 €/Monat, Abschlag 80 €/Monat, Gaseinheit m³, Brennwert 11,2, Zustandszahl 0,95. Laufzeit 01.01. bis 31.12.2026, heute der 12.07.2026 (Tag 192, also 6,3075 Monate). Der Zähler stand bei Vertragsbeginn bei 1.000 m³ und steht jetzt bei 1.100 m³. Die Zahlen stammen aus den Tests (`tests/test_coordinator.py`); es sind Beispielwerte.

```
Verbrauch (Bisher)              = 1.100 − 1.000                         = 100 m³
Verbrauch in kWh                = 100 × 11,2 × 0,95                     = 1.064 kWh
Kosten (Bisher)                 = 1.064 × 0,10 + 10,00 × 6,3075         =   169,47 €
Abschläge bisher fällig         = 80 × 6,3075                           =   504,60 €
→ Guthaben/Nachzahlung (Bisher) ≈ 504,60 − 169,47                       =  +335,12 €  (Guthaben)
```

Und die Hochrechnung auf die Laufzeit (364 Tage, 11,958 Monate):

```
Verbrauch hochgerechnet         = 100 ÷ 192 × 364                       = 189,6 m³
Verbrauch hochgerechnet in kWh  = 189,6 × 11,2 × 0,95                   = 2.017,3 kWh
Geschätzte Kosten zum Ende      = 2.017,3 × 0,10 + 10,00 × 11,958       =   321,31 €
Abschläge der ganzen Laufzeit   = 80 × 11,958                           =   956,64 €
→ Guthaben/Nachzahlung (Vertragsende) ≈ 956,64 − 321,31                 =  +635,32 €
```

Der Abschlag im Beispiel ist also deutlich zu hoch. Der Test prüft die Kosten bisher; die Prognose folgt derselben Formel wie bei Strom.

Die Schätzung im Formular rechnet genauso: 1.000 m³ Jahresverbrauch × 11,2 × 0,95 ergeben im Sensor **Jahresverbrauch (kWh)** 10.640 kWh.

## Typische Fehler

| Problem | Ursache und Lösung |
|---|---|
| Der Verbrauch ist in m³, die Kosten sind in kWh gerechnet | Das ist so gewollt: **Verbrauch (Bisher)** zeigt die Zählerdifferenz, nur die Kosten laufen über Brennwert × Zustandszahl. |
| „Keine gültige Zahl.“ beim Speichern | Brennwert oder Zustandszahl enthalten etwas anderes als Ziffern mit Punkt oder Komma. |
| Die Kosten sind etwa zehnmal zu hoch bei einem kWh-Zähler | Brennwert und Zustandszahl multiplizieren auch dann. Trage für einen Zähler in kWh beide Werte als 1 ein. |
| Die Kosten stimmen nicht mit der Rechnung überein | Brennwert und Zustandszahl ändern sich beim Versorger mit der Zeit. Trage die Werte Deiner aktuellen Rechnung ein. Für einen neuen Vertrag mit anderen Werten legst Du einen [Folgevertrag](Folgevertrag-oder-Verlaengern) mit **Brennwert neu** und **Zustandszahl neu** an. |
| Der Verbrauch ist unbekannt | Die Statistik des Sensors reicht nicht bis zum Vertragsbeginn zurück. Trage den **Zählerstand bei Vertragsbeginn (optional)** ein. |
| Kein Sensor **Jahresverbrauch (kWh)** mit Wert | Er braucht den **Geschätzten Jahresverbrauch (m³)** und bei m³, CCF und ft³ den Brennwert. |

## Siehe auch

- [Verträge anlegen](Vertraege-Anlegen)
- [Vertrag Strom](Vertrag-Strom)
- [Verbrauch messen](Verbrauch-Messen)
- [Abschläge und Kosten](Abschlaege-und-Kosten)
- [Folgevertrag oder Verlängern](Folgevertrag-oder-Verlaengern)
- [Sensoren Referenz](Sensoren-Referenz)
- [Fehlerbehebung](Fehlerbehebung)
