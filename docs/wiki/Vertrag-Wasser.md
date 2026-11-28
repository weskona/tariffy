🇩🇪 Deutsch · [🇬🇧 English](EN-Contract-Water)

# Vertrag Wasser

Hier findest Du alle Felder eines Wasservertrags, die drei Arten, das Abwasser abzurechnen, und die Außenzähler für Garten, Pool und Bewässerung. Wasser ist wie Strom und Gas ein Verbrauchsvertrag: Mit einem Zähler-Sensor rechnet Tariffy echte Kosten, Saldo und Prognose.

**Inhalt:**

- [So rechnet Tariffy bei Wasser](#so-rechnet-tariffy-bei-wasser)
- [Die Formularfelder](#die-formularfelder)
- [Frischwasser und Abwasser](#frischwasser-und-abwasser)
- [Außenzähler](#außenzähler)
- [Rechenbeispiel](#rechenbeispiel)
- [Typische Fehler](#typische-fehler)

## So rechnet Tariffy bei Wasser

```
Verbrauch (Bisher)        = aktueller Zählerstand − Zählerstand am Vertragsbeginn
Wasserpreis (Gesamt)      = Frischwasserpreis + Abwasserpreis (je nach Abwasser-Typ)
Kosten (Bisher)           = Verbrauch bisher × Wasserpreis (Gesamt) + Grundpreis × vergangene Monate
```

Ein Monat zählt 30,44 Tage. Saldo und Prognose rechnen wie bei Strom, die Formeln stehen auf [Vertrag Strom](Vertrag-Strom#so-rechnet-tariffy). Die Verbrauchs-Sensoren zeigen die Einheit des Zählersensors (zum Beispiel m³); hat er keine, gilt die gewählte **Wassereinheit**. Es gibt keine Umrechnung in kWh.

## Die Formularfelder

Das zweite Formular heißt **Wasservertrag Details**.

| Feld | Pflicht | Beschreibung |
|---|---|---|
| Wassereinheit | ja | Abrechnungseinheit laut Wasserrechnung: `m³`, `L`, `gal`, `ft³` oder `CCF` (Voreinstellung `m³`). |
| Frischwasserpreis (pro Einheit) | ja | Preis pro Einheit Frischwasser. |
| Grundpreis (pro Monat) | ja | Monatlicher Festbetrag unabhängig vom Verbrauch. |
| Monatlicher Abschlag | ja | Monatliche Vorauszahlung an den Anbieter. |
| Abwasser-Abrechnungstyp | ja | Art der Abwasserberechnung, siehe [Frischwasser und Abwasser](#frischwasser-und-abwasser). |
| Abwassergebühr | nein | Betrag pro Einheit, Prozentsatz oder Monatspauschale, je nach gewähltem Typ. |
| Jahresverbrauch | nein | Geschätzter Jahresverbrauch. Kosten bisher und Prognose rechnen mit dem gemessenen Verbrauch. |
| Verbrauchssensor (optional) | nein | Sensor Deines Wasserzählers; ermöglicht die echte Verbrauchsmessung. |
| Zählerstand bei Vertragsbeginn (optional) | nein | Dein genauer Zählerstand am Vertragsbeginn, falls Du ihn kennst. Hat Vorrang vor der automatischen Erkennung. |
| Warnen, wenn Abschlag zu niedrig ist | nein | Aus nach der Voreinstellung. Wirkt wie bei [Vertrag Strom](Vertrag-Strom#die-formularfelder) beschrieben. |
| Warnschwelle (€ Nachzahlung) | nein | Voreinstellung 50. |
| Zählernummer | nein | Zur Dokumentation. |

Je nach dem in Home Assistant eingestellten Land erscheinen zusätzlich **Staffelpreise aktivieren** und die Blöcke; sie funktionieren wie bei [Vertrag Strom](Vertrag-Strom#staffelpreise). Die Außenzähler trägst Du nicht im Formular ein, sondern im Panel (siehe unten).

## Frischwasser und Abwasser

Bei **Abwasser-Abrechnungstyp** wählst Du eine von drei Arten. Welche vorausgewählt ist, hängt vom Land in Home Assistant ab (Prozentsatz in US, CA, AU, NZ, GB, IE; Monatspauschale in FR, BE, LU; sonst fester Preis).

| Typ | Bedeutung von **Abwassergebühr** | Wirkung auf den Wasserpreis (Gesamt) |
|---|---|---|
| Fixer Preis pro Einheit (z.B. DE, AT, CH) | Preis pro Einheit | Frischwasserpreis + Abwassergebühr |
| Prozentsatz des Frischwasserpreises (z.B. US, UK, AU) | Prozent, zum Beispiel 80 für 80 % | Frischwasserpreis + Frischwasserpreis × Prozent ÷ 100 |
| Monatliche Pauschale (z.B. FR, BE) | Euro pro Monat | Frischwasserpreis unverändert |

Daraus entstehen die Sensoren **Arbeitspreis (Abwasser)** und **Wasserpreis (Gesamt)** in „Währung pro Wassereinheit“. Beim Prozentsatz zeigt **Arbeitspreis (Abwasser)** den berechneten Preis; sein Attribut `typ` nennt den Abwasser-Typ.

> **Gut zu wissen:** Die **Monatliche Pauschale** steht nur als Attribut `pauschal_monat` am Sensor **Arbeitspreis (Abwasser)**. Tariffy rechnet sie **nicht** in die Kosten ein. Soll sie im Saldo erscheinen, addierst Du sie zum **Grundpreis (pro Monat)**.

## Außenzähler

Wasser aus dem Garten, dem Pool oder der Bewässerung läuft nicht in die Kanalisation und wird deshalb nicht als Abwasser berechnet. Dafür gibt es Außenzähler: Unterzähler, deren Verbrauch **schon im Hauptzähler enthalten** ist. Du trägst sie im Panel ein, im Tab **Verträge** in den Details des Wasservertrags, im Block **Außenzähler**. Das geht nur als Administrator und für höchstens zehn Zähler.

![Die Details eines Wasservertrags im Tab Verträge: Blöcke Vertrag, Preise, Einmalposten und Verbrauch mit Gartenwasser und Abwasserkosten, darunter der Block Außenzähler mit zehn Zählern](https://raw.githubusercontent.com/wiki/weskona/tariffy/images/outdoor-meters-layout.png)

*Abbildung: Der Block „Außenzähler“ unter den Details des Wasservertrags, hier mit zehn Zählern (Mock-Daten, Datum 12.07.2026). Im Block „Verbrauch“ stehen „Gartenwasser“, „Abwasserpflichtiger Verbrauch“, „Gartenwasser-Kosten“ und „Abwasserkosten“.*

### Außenzähler eintragen

1. Öffne im Panel den Tab **Verträge** und klappe den Wasservertrag auf.
2. Klicke im Block **Außenzähler** auf **Außenzähler hinzufügen**. Zum Ändern nutzt Du den Stift am Zähler.
3. Fülle den Dialog aus und klicke auf **Speichern**.

![Der Dialog Außenzähler hinzufügen mit den Feldern Name, Verbrauchssensor, Startwert und Eigener Preis je Einheit](https://raw.githubusercontent.com/wiki/weskona/tariffy/images/aussen-dialog.png)

*Abbildung: Der Dialog „Außenzähler hinzufügen“ mit dem Beispiel „Pool“.*

| Feld | Pflicht | Beschreibung |
|---|---|---|
| Name | ja | Name des Zählers, zum Beispiel „Pool“. |
| Verbrauchssensor | ja | Sensor des Außenzählers. Er darf nicht der Hauptzähler des Vertrags sein. |
| Startwert (optional) | nein | Zählerstand am Vertragsbeginn, in der Einheit des Zählers. Ohne Startwert liest Tariffy den Stand aus den Langzeitstatistiken. |
| Eigener Preis je Einheit, ohne Abwasser (optional) | nein | Preis, mit dem das Wasser dieses Zählers gerechnet wird, **nur das Frischwasser, ohne Abwasser** (Gartenwasser läuft nicht in die Kanalisation). Das Feld ist mit dem **Frischwasserpreis des Vertrags vorbelegt**; ändere ihn, wenn dieses Wasser etwas anderes kostet. Lässt Du ihn unverändert, folgt der Zähler dem Preis des Vertrags (zum Beispiel nach einem Tarifwechsel). |

Löschen kannst Du einen Zähler im Bearbeiten-Dialog mit **Zähler löschen** (mit Rückfrage „Diesen Außenzähler löschen?“ und **Ja, löschen**). Wenn Du den ersten Außenzähler anlegst, lädt Home Assistant den Vertrag neu, weil er dafür zusätzliche Sensoren bekommt.

### Wie Tariffy die Außenzähler rechnet

- **Abwasserpflichtiger Verbrauch = Hauptzähler − Summe der Außenzähler** (nie unter 0). Zählen die Außenzähler zusammen mehr als der Hauptzähler, wird ihr Anteil auf den Hauptzähler begrenzt.
- Das Außenwasser kostet den **Frischwasserpreis** oder den eigenen Preis des Zählers, das übrige Wasser den vollen **Wasserpreis (Gesamt)** aus Frischwasser und Abwasser.
- Die **Kosten (Bisher)**, die Prognose und der empfohlene Abschlag rechnen mit dem daraus **gewichteten Preis** des Hauptzählers, wie beim Zweizählertarif bei Strom.
- Im Panel zeigt der Block **Preise** dann zwei Zeilen: **Wasserpreis inkl. Abwasser** ist der **volle Preis** (Frischwasser plus Abwasser, zum Beispiel 5,51 €/m³), **Mischpreis (mit Gartenwasser)** ist der **gewichtete Preis** des Hauptzählers, mit dem die Kosten gerechnet werden. Der Sensor **Wasserpreis (Gesamt)** enthält den gewichteten Preis.
- Ein Zähler in Litern wird in die Einheit des Hauptzählers (m³) umgerechnet. Ein Startwert gilt in der Einheit des Zählers.
- Bei einer **Monatlichen Pauschale** fürs Abwasser ändern Außenzähler an den Kosten nichts; **Abwasserkosten** sind dann 0.
- Für einen Vertrag mit Außenzähler gibt es vier zusätzliche Sensoren: **Gartenwasser (Verbrauch)**, **Gartenwasser (Kosten)**, **Abwasserpflichtiger Verbrauch** und **Abwasserkosten**. Die Gesamtkosten stehen wie immer in **Kosten (Bisher)**. Ohne Außenzähler ändert sich nichts.

> **Gut zu wissen:** Bei einem automatischen Wechsel zum Folgevertrag bleiben die Außenzähler verbunden; ihre Startwerte entfallen, weil sie zur alten Laufzeit gehörten. Außenzähler sind auch in der [Sicherung](Panel-Sicherung) enthalten.

## Rechenbeispiel

Ein Wasservertrag mit Frischwasserpreis 2,00 €/m³, Abwasser als fester Preis 3,00 €/m³ (Wasserpreis (Gesamt) also 5,00 €/m³), Grundpreis 5,00 €/Monat, Abschlag 30 €/Monat. Laufzeit 01.01. bis 31.12.2026, heute der 12.07.2026 (6,3075 Monate). Der Hauptzähler zeigt seit Beginn 150 m³ Verbrauch. Die Zahlen stammen aus den Tests (`tests/test_coordinator.py` und `tests/test_aussen.py`); es sind Beispielwerte.

**Ohne Außenzähler:**

```
Kosten (Bisher)                 = 150 × 5,00 + 5,00 × 6,3075            =   781,54 €
Abschläge bisher fällig         = 30 × 6,3075                           =   189,22 €
→ Guthaben/Nachzahlung (Bisher) = 189,22 − 781,54                       =  −592,32 €  (Nachzahlung)
```

### Mit einem Außenzähler

Der Garten-Zähler zeigt seit Beginn 40 m³ (ohne eigenen Preis):

```
Gartenwasser (Verbrauch)        = 40 m³
Abwasserpflichtiger Verbrauch   = 150 − 40                              = 110 m³
Gartenwasser (Kosten)           = 40 × 2,00                             =    80,00 €
Abwasserkosten                  = 110 × 3,00                            =   330,00 €
Kosten (Bisher)                 = 110 × 5,00 + 40 × 2,00 + 5,00 × 6,3075 =  661,54 €
Gewichteter Preis des Hauptzählers = (110 × 5,00 + 80) ÷ 150            =     4,20 €/m³
→ Guthaben/Nachzahlung (Bisher) = 189,22 − 661,54                       =  −472,32 €  (Nachzahlung)
```

Der Außenzähler spart hier gegenüber der Rechnung ohne Außenzähler 120 € Abwasser (40 m³ × 3,00 €). Die Prognose zum Vertragsende folgt dem gewichteten Preis und fällt dadurch besser aus als ohne Außenzähler.

Wird als Abwasser-Typ der Prozentsatz gewählt (Frischwasser 2,00 €/m³, Abwassergebühr 80), ergibt das einen Abwasserpreis von 1,60 €/m³ und einen Wasserpreis (Gesamt) von 3,60 €/m³.

## Typische Fehler

| Problem | Ursache und Lösung |
|---|---|
| Die Abwasser-Pauschale taucht in den Kosten nicht auf | Die **Monatliche Pauschale** fließt nicht in die Rechnung ein. Addiere sie zum **Grundpreis (pro Monat)**. |
| Falscher Abwasserpreis | Der **Abwasser-Abrechnungstyp** passt nicht zu Deiner Rechnung. Bei „Prozentsatz“ trägst Du in **Abwassergebühr** den Prozentwert ein (80 für 80 %), nicht den Preis. |
| Die vier Außenzähler-Sensoren fehlen | Sie entstehen erst mit dem ersten Außenzähler; der Vertrag lädt dann neu. Ein Außenzähler lässt sich nur bei einem Wasservertrag anlegen. |
| Der Außenzähler wird abgelehnt | Trage einen Namen ein, wähle einen Sensor und nimm nicht den Hauptzähler des Vertrags („Das ist der Hauptzähler des Vertrags.“). Der Preis darf nicht negativ sein. |
| Es gibt keine Außenzähler-Kosten | Die Aufteilung braucht den Verbrauch des Hauptzählers: Ohne Verbrauchssensor am Wasservertrag bleiben die Werte leer. |
| Der Außenzähler zählt in Litern, der Hauptzähler in m³ | Das geht: Tariffy rechnet Liter in m³ um (nur diese zwei Einheiten). |
| Verbrauch unbekannt | Die Statistik des Sensors reicht nicht bis zum Vertragsbeginn zurück. Trage den **Zählerstand bei Vertragsbeginn (optional)** ein. |

## Siehe auch

- [Verträge anlegen](Vertraege-Anlegen)
- [Vertrag Strom](Vertrag-Strom)
- [Verbrauch messen](Verbrauch-Messen)
- [Panel Verträge](Panel-Vertraege)
- [Abschläge und Kosten](Abschlaege-und-Kosten)
- [Sensoren Referenz](Sensoren-Referenz)
- [Fehlerbehebung](Fehlerbehebung)
