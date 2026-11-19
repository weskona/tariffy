🇩🇪 Deutsch · [🇬🇧 English](EN-Contract-Leasing)

# Vertrag: Leasing

Die Sparte **Leasing** ist für einen Auto-Leasingvertrag. Die Rate läuft wie ein Pauschalvertrag und zählt in den Summen mit. Dazu behält Tariffy die **Kilometer** im Blick: Du siehst, wie viel du schon gefahren bist, ob du im Soll liegst und was die Rückgabe voraussichtlich kostet oder bringt.

**Inhalt:**
- [Wie Leasing in Tariffy aufgebaut ist](#wie-leasing-in-tariffy-aufgebaut-ist)
- [Schritt für Schritt](#schritt-für-schritt)
- [Felder im Überblick](#felder-im-überblick)
- [So rechnet Tariffy die Kilometer](#so-rechnet-tariffy-die-kilometer)
- [Was Tariffy anzeigt](#was-tariffy-anzeigt)
- [Rechenbeispiel](#rechenbeispiel)
- [Typische Fehler](#typische-fehler)
- [Siehe auch](#siehe-auch)

## Wie Leasing in Tariffy aufgebaut ist

Das Formular hat drei Schritte:

1. **Allgemeine Daten** (wie bei allen Sparten): **Vertragsbeginn** ist der Beginn des Leasings, **Vertragsende / Laufzeit bis** das **Rückgabedatum**.
2. **Leasing:** die Kilometer des Vertrags. Alles ist freiwillig.
3. **Kosten:** die Rate, wie bei jedem Pauschalvertrag (Zahlweise, Betrag pro Zahlung, Erste Abbuchung am).

Im Panel steht ein Leasingvertrag in der Gruppe **Kredite / Finanzierungen**. Die **Kilometerkosten zählen nicht** in die Summen des Vertrags: Sie sind eine Schätzung für die Rückgabe, kein bezahlter Betrag.

## Schritt für Schritt

1. Im Panel im Tab **Verträge** auf **Neuer Vertrag** klicken. Die allgemeinen Schritte stehen auf [Verträge anlegen](Vertraege-Anlegen).
2. **Schritt 1:** Bezeichnung, Sparte **Leasing**, Anbieter (zum Beispiel die Leasingbank), **Vertragsbeginn** und **Vertragsende / Laufzeit bis** (Rückgabedatum) eintragen. Ohne diese beiden Daten kann Tariffy keine Kilometer auf die Laufzeit verteilen.
3. **Schritt Leasing:** Entweder einen **Kilometerzähler-Sensor** wählen oder den **Aktuellen Kilometerstand (km)** von Hand eintragen; dazu **Kilometerstand bei Vertragsbeginn (km)**, die erlaubten Kilometer, die Toleranzen und die Preise je Kilometer.
4. **Kosten:** **Zahlweise** und **Betrag pro Zahlung (€)** der Leasingrate eintragen.
5. Speichern. Ohne Sensor aktualisierst du den Kilometerstand ab und zu mit **Vertrag bearbeiten**.

## Felder im Überblick

Schritt 1 und der Kosten-Schritt sind auf [Vertrag: Internet und Mobilfunk](Vertrag-Internet-und-Mobilfunk#felder-im-überblick) beschrieben. Der Schritt **Leasing**:

| Feld | Pflicht | Bedeutung | Standard |
|------|---------|-----------|----------|
| Kennzeichen | nein | Gilt als persönlich: wird im Seitenpanel nicht angezeigt | leer |
| Kilometerzähler-Sensor | nein | Sensor des Fahrzeugs mit dem Kilometerstand in km (Meilen werden umgerechnet). Er hat Vorrang vor dem von Hand eingetragenen Wert. Fehlt er oder ist er nicht verfügbar, gilt der eingetragene Stand | leer |
| Aktueller Kilometerstand (km) | nein | Nur wenn du keinen Sensor hast: von Hand eintragen und ab und zu aktualisieren (Vertrag bearbeiten) | leer |
| Kilometerstand bei Vertragsbeginn (km) | nein | Kilometerstand zu Beginn des Leasings | leer = 0 |
| Erlaubte Kilometer pro Jahr (km) | nein | Im Vertrag vereinbarte Kilometer pro Jahr | leer |
| Erlaubte Kilometer über die ganze Laufzeit (km) | nein | Die Summe der ganzen Laufzeit. Der Wert hat Vorrang vor „pro Jahr“ | leer = Kilometer pro Jahr mal Laufzeit |
| Toleranz nach oben (km) | nein | Mehrkilometer bis zu diesem Wert werden nicht berechnet | leer = 0 |
| Toleranz nach unten (km) | nein | Minderkilometer bis zu diesem Wert werden nicht gutgeschrieben | leer = 0 |
| Preis je Mehrkilometer (€) | nein | Wird für jeden Mehrkilometer über der Toleranz berechnet | leer |
| Gutschrift je Minderkilometer (€) | nein | Wird für jeden Minderkilometer über der Toleranz gutgeschrieben | leer |

## So rechnet Tariffy die Kilometer

1. **Gefahren** = Kilometerstand minus Stand bei Vertragsbeginn. Der Kilometerstand kommt aus dem Sensor, sonst aus dem eingetragenen Wert.
2. **Erlaubt insgesamt** = der Gesamtwert, sonst Kilometer pro Jahr mal Laufzeit in Tagen geteilt durch 365,25.
3. **Soll bis heute** = erlaubte Kilometer gleichmäßig auf die Laufzeit verteilt, bis heute gezählt.
4. **Noch übrig** = erlaubt minus gefahren; **Erlaubt pro Tag ab jetzt** = Rest geteilt durch die Resttage.
5. **Hochrechnung bei Rückgabe** = bisheriger Schnitt je Tag, bis zum Rückgabedatum fortgeschrieben. Sie gibt es **erst ab 14 Tagen Fahrt**; vorher stehen nur die einfachen Werte.
6. **Abweichung** = Hochrechnung minus erlaubt. **Mehrkilometer** sind, was die Abweichung über die Toleranz nach oben hinaus übersteigt. **Minderkilometer** sind, was nach unten die Toleranz übersteigt.
7. **Erwartete Nachzahlung** = Mehrkilometer mal Preis je Mehrkilometer; **erwartete Gutschrift** = Minderkilometer mal Gutschrift je Minderkilometer. Der **Saldo** ist Nachzahlung minus Gutschrift, eine Gutschrift ist also negativ. Ohne Preise gibt es keinen Geldbetrag.
8. **Nach dem Rückgabedatum** sind die gefahrenen Kilometer das Ergebnis.

Ohne verwertbaren Kilometerstand (kein Sensor, kein Wert, oder ein Stand unter dem Startwert) zeigt Tariffy keine Kilometerwerte.

## Was Tariffy anzeigt

- **In der Vertragskarte** steht eine Zeile mit den gefahrenen Kilometern und was das Tempo bei Rückgabe bedeutet.
- **In den Details** gibt es den Block **Leasing-Kilometer**: Kilometerstand, Bisher gefahren, Erlaubt insgesamt, Soll bis heute, Gegenüber dem Soll, Noch übrig, Erlaubt pro Tag ab jetzt, Dein Schnitt pro Tag, Hochrechnung bei Rückgabe, Gegenüber der Erlaubnis bei Rückgabe, Toleranzen, Mehr- und Minderkilometer, die Preise und der Geldbetrag (**Erwartete Nachzahlung**, **Erwartete Gutschrift**, **Erwartet bei Rückgabe**).
- **Hinweise im Block:**
  - „Noch kein Kilometerstand: Wähle einen Sensor oder trage den Stand im Vertrag ein.“
  - „Die Hochrechnung braucht mindestens zwei Wochen Fahrt.“
  - „In diesem Tempo liegst du bei Rückgabe etwa … km über der Erlaubnis“, „… unter der Erlaubnis“ oder „In diesem Tempo bleibst du bei Rückgabe innerhalb der Erlaubnis.“
- **Sensoren:** **Gefahrene Kilometer** (in km, mit den Attributen `km_stand`, `km_erlaubt`, `km_soll`, `abweichung_soll`, `km_rest`, `km_rest_je_tag`, `km_je_tag`, `prozent_der_erlaubten`), **Kilometer bei Rückgabe (Hochrechnung)** und **Erwartete Mehr-/Minderkilometer-Kosten**. Dazu die Fahrzeug-Sensoren der Versicherung: **Kennzeichen**, **Kilometerstand bei Vertragsbeginn**, **Erlaubte Kilometer pro Jahr**. Die Sensoren gibt es nur bei Leasing; die Namen der Sensoren und ihre Entity-IDs findest du in der [Sensoren-Referenz](Sensoren-Referenz).

## Rechenbeispiel

Werte aus den Tests: Leasing bei „Autobank“, Rate 299 € im Monat, Beginn **1. Januar 2026**, Rückgabe **1. Januar 2027** (365 Tage), Kilometerstand bei Vertragsbeginn **20 000 km**, erlaubt über die ganze Laufzeit **12 000 km**, keine Toleranz, **0,10 €** je Mehrkilometer, **0,05 €** Gutschrift je Minderkilometer. Der Kilometerzähler-Sensor steht am **1. Juli 2026** (Tag 181) auf **26 000 km**.

```
Gefahren:                26 000 − 20 000 = 6 000 km
Soll bis heute:          12 000 × 181 / 365 ≈ 5 951 km   → 49 km über dem Soll
Noch übrig:              12 000 − 6 000 = 6 000 km  (rund 32,6 km pro Tag bei 184 Resttagen)
Dein Schnitt:            6 000 / 181 ≈ 33,1 km pro Tag
Hochrechnung:            6 000 / 181 × 365 ≈ 12 099 km
Mehrkilometer:           12 099 − 12 000 ≈ 99 km
Erwartete Nachzahlung:   99,45 km × 0,10 € ≈ 9,94 €
```

Mit einer **Toleranz nach oben** von 500 km würden diese 99 km nicht berechnet: Mehrkilometer 0, Nachzahlung 0 €.

Für Minderkilometer: Steht der Zähler am 1. Juli nur bei 22 000 km (2 000 km gefahren), ergibt die Hochrechnung rund 4 033 km, also knapp 7 967 km unter der Erlaubnis. Mit **1 000 km Toleranz nach unten** zählen rund 6 967 Minderkilometer, die Gutschrift beträgt etwa 348 € und der Saldo bei Rückgabe ist etwa −348 € (negativ = Gutschrift).

## Typische Fehler

- **Kilometerstand bei Vertragsbeginn leer.** Dann zählt Tariffy ab 0, und die „gefahrenen“ Kilometer sind der ganze Zählerstand des Autos. Trage den Stand bei Übernahme ein.
- **Kein Rückgabedatum oder kein Beginn.** Ohne beide fehlen Soll, Hochrechnung und Resttage. Nur die gefahrenen Kilometer erscheinen, wenn es einen Kilometerstand gibt.
- **Kilometerstand unter dem Startwert.** Dann zeigt Tariffy gar keine Kilometerwerte. Das passiert zum Beispiel, wenn ein Sensor ein anderes Fahrzeug oder einen Tageszähler liefert.
- **Die Hochrechnung fehlt.** In den ersten 14 Tagen gibt es sie nicht, das ist gewollt.
- **Kein Geldbetrag.** Es sind weder Preis je Mehrkilometer noch Gutschrift je Minderkilometer eingetragen.
- **Sensor und Hand-Wert gleichzeitig.** Der Sensor hat Vorrang. Ist er „nicht verfügbar“, nimmt Tariffy den von Hand eingetragenen Stand; den hast du dann hoffentlich aktuell gehalten.
- **Toleranz verwechselt.** „Nach oben“ entlastet Mehrkilometer, „nach unten“ nur die Gutschrift für Minderkilometer.

> **Gut zu wissen:** Ein **Tarifwechsel** oder ein geplanter Folgevertrag behält Fahrzeug, Sensor und Kilometerregeln; Kilometerstand bei Beginn und der von Hand eingetragene Stand gehören zur alten Laufzeit und entfallen. Bei **Vertrag verlängern** bleiben die Angaben, wie sie sind: Prüfe bei einem anderen Fahrzeug unter **Vertrag bearbeiten** den Stand bei Beginn und die Erlaubnis.

## Siehe auch

- [Vertrag: Kredit](Vertrag-Kredit)
- [Vertrag: Versicherung](Vertrag-Versicherung)
- [Vertrag: Internet und Mobilfunk](Vertrag-Internet-und-Mobilfunk)
- [Folgevertrag oder Verlängern](Folgevertrag-oder-Verlaengern)
- [Sensoren-Referenz](Sensoren-Referenz)
- [Panel: Verträge](Panel-Vertraege)
