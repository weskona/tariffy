🇩🇪 Deutsch · [🇬🇧 English](EN-Contract-Other)

# Vertrag: Sonstiges

Die Sparte **Sonstiges** ist für alles, was zu keiner anderen Sparte passt und einen festen Betrag kostet, zum Beispiel ein Fitnessstudio, ein Vereinsbeitrag, eine Zeitung oder ein Wartungsvertrag. Sie ist ein ganz normaler **Pauschalvertrag** ohne Sonderfelder.

**Inhalt:**
- [Was Sonstiges kann](#was-sonstiges-kann)
- [Schritt für Schritt](#schritt-für-schritt)
- [Felder im Überblick](#felder-im-überblick)
- [Preisänderung und Folgevertrag](#preisänderung-und-folgevertrag)
- [Rechenbeispiel](#rechenbeispiel)
- [Typische Fehler](#typische-fehler)
- [Siehe auch](#siehe-auch)

## Was Sonstiges kann

- **Kosten:** wie bei [Internet und Mobilfunk](Vertrag-Internet-und-Mobilfunk): Zahlweise, Betrag pro Zahlung, Kosten bisher als gebuchte Raten.
- **Kündigung:** Vertragsende, Kündigungsfrist, Mindestlaufzeit und Erinnerung wie bei jeder Sparte.
- **Verlängern:** Das Symbol **Vertrag verlängern** gibt es auch bei Sonstiges. Du kannst es auch bei einem Vertrag **ohne Vertragsende** nutzen, zum Beispiel bei einer Preisanpassung (Ende im Dialog leer lassen).
- **Eigenes Icon:** Mit dem Feld **Icon** (zum Beispiel `mdi:dumbbell`) bekommt der Vertrag ein eigenes Symbol im Panel und bei den Sensoren; leer = das Icon der Sparte.
- **Was fehlt:** Es gibt keine Versicherungs-, Kilometer- oder Kreditfelder. Brauchst du die, wähle [Versicherung](Vertrag-Versicherung), [Leasing](Vertrag-Leasing) oder [Kredit](Vertrag-Kredit).

## Schritt für Schritt

1. Im Panel im Tab **Verträge** auf **Neuer Vertrag** klicken. Die allgemeinen Schritte stehen auf [Verträge anlegen](Vertraege-Anlegen).
2. **Schritt 1:** Bezeichnung, Sparte **Sonstiges**, Anbieter, Vertragsbeginn und, falls vorhanden, Vertragsende, Kündigungsfrist und Erinnerung eintragen.
3. **Schritt 2, Kosten:** **Zahlweise** wählen, **Betrag pro Zahlung (€)** eintragen und bei nicht monatlicher Zahlung **Erste Abbuchung am** setzen.
4. Speichern.

## Felder im Überblick

Schritt 1 ist auf [Vertrag: Internet und Mobilfunk](Vertrag-Internet-und-Mobilfunk#felder-im-überblick) beschrieben. Schritt 2:

| Feld | Pflicht | Bedeutung | Standard |
|------|---------|-----------|----------|
| Zahlweise | ja | Monatlich, Vierteljährlich, Halbjährlich oder Jährlich | Monatlich |
| Betrag pro Zahlung (€) | ja | Der Betrag einer Zahlung in der gewählten Zahlweise (zum Beispiel der Jahresbeitrag) | 0 |
| Erste Abbuchung am | nein | Tag der ersten Abbuchung; leer = Vertragsbeginn | leer |

Das Feld **Grundpreis (€/Monat)** erscheint nur noch beim Bearbeiten eines Vertrags, der schon einen hat.

## Preisänderung und Folgevertrag

- **Der Betrag ändert sich mitten in der Laufzeit:** Trage den neuen Betrag im Vertrag ein; er gilt ab dem Tag des Speicherns.
- **Zum Ende der Laufzeit:** **Vertrag verlängern** (Historie mit einem Eintrag pro Laufzeit, siehe [Folgevertrag oder Verlängern](Folgevertrag-oder-Verlaengern)).
- **Bekannter Wechsel:** **Folgevertrag planen** öffnet ein Formular, das fragt: **Wechseldatum (Beginn neuer Vertrag)**, **Anbieter (neu)**, **Kundennummer (neu)**, **Tarifname (neu)**, **Abschlag neu (€/Monat)**, **Grundpreis neu (€/Monat)** und **Vertragsende neu / Laufzeit bis**. Anders als bei [Streaming](Vertrag-Streaming) gibt es hier keine Zahlweise im Formular, und der Betrag ist der **Betrag pro Monat**. Nicht ausgefüllte Felder behalten den aktuellen Wert, ein leeres **Wechseldatum** entfernt den geplanten Wechsel.

## Rechenbeispiel

Beispielwerte (nicht aus einem echten Vertrag): Vertrag „Fitnessstudio“ mit Sparte **Sonstiges**, Beginn 15. März 2026, Zahlweise **Jährlich**, **249 €** pro Zahlung, Erste Abbuchung am 15. März 2026.

```
Gespeichert wird der Monatsbetrag:  249 € / 12 = 20,75 € im Monat
Kosten bisher am 20.11.2026:         249,00 €   (eine Abbuchung)
Kosten bisher ab 15.03.2027:         498,00 €   (zwei Abbuchungen, wenn der Vertrag dann noch läuft)
```

Hätte der Vertrag ein Ende am 14. März 2027, gehörte die Abbuchung vom 15. März 2027 schon zur nächsten Laufzeit.

## Typische Fehler

- **Betrag pro Monat statt pro Zahlung.** Bei Zahlweise „Jährlich“ gehört der Jahresbetrag ins Feld, nicht der Monatsbetrag.
- **Sonstiges gewählt, obwohl eine Spezialsparte passt.** Für Strom, Gas und Wasser (mit Zähler), Streaming, Versicherung, Leasing und Kredit gibt es eigene Sparten mit passenden Feldern.
- **Vertragsbeginn fehlt.** Die erste Rate nimmt Tariffy am Vertragsbeginn an.
- **Im Folgevertrag-Formular eine Zahlweise gesucht.** Sie gibt es nur bei Streaming; bei Sonstiges planst du den Betrag pro Monat.

> **Gut zu wissen:** Die Sparte lässt sich beim Bearbeiten ändern. Prüfe danach die Felder des neuen Schritts, weil jede Sparte eigene Felder hat.

## Siehe auch

- [Vertrag: Internet und Mobilfunk](Vertrag-Internet-und-Mobilfunk)
- [Vertrag: Streaming](Vertrag-Streaming)
- [Folgevertrag oder Verlängern](Folgevertrag-oder-Verlaengern)
- [Abschläge und Kosten](Abschlaege-und-Kosten)
- [Verträge anlegen](Vertraege-Anlegen)
