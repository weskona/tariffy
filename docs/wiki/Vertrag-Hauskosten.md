🇩🇪 Deutsch · [🇬🇧 English](EN-Contract-House-Costs)

# Vertrag: Hauskosten

Die Sparte **Hauskosten** ist für die laufenden Kosten rund ums Haus, die keinen Zähler haben und in festen Beträgen kommen: Abfallgebühren, Straßenreinigung, Niederschlagswasser (Regenwassergebühr), Grundsteuer, Schornsteinfeger, Winterdienst und Ähnliches. Sie ist ein **Pauschalvertrag** mit einer zusätzlichen **Art**, die Du aus einer Liste wählst oder frei eintippst.

**Inhalt:**
- [Was Hauskosten können](#was-hauskosten-können)
- [Schritt für Schritt](#schritt-für-schritt)
- [Felder im Überblick](#felder-im-überblick)
- [So sieht es im Panel aus](#so-sieht-es-im-panel-aus)
- [Betrag ändert sich und Folgevertrag](#betrag-ändert-sich-und-folgevertrag)
- [Rechenbeispiel](#rechenbeispiel)
- [Typische Fehler](#typische-fehler)
- [Siehe auch](#siehe-auch)

## Was Hauskosten können

- **Art:** Wähle aus der Liste **Abfallgebühren**, **Straßenreinigung**, **Niederschlagswasser (Regenwassergebühr)**, **Grundsteuer**, **Schornsteinfeger**, **Winterdienst** oder **Hausmeister / Gebäudeservice**, oder tippe eine eigene Art ein (zum Beispiel „Gartenabfall“). Die Art ist freiwillig und dient der Übersicht.
- **Kosten:** wie bei [Sonstiges](Vertrag-Sonstiges) und [Internet und Mobilfunk](Vertrag-Internet-und-Mobilfunk): Zahlweise (monatlich, vierteljährlich, halbjährlich, jährlich), Betrag pro Zahlung und Kosten bisher als gebuchte Raten.
- **In den Summen:** Hauskosten **zählen mit**, in den Abschlägen pro Monat, in Kosten bisher und in den Jahressummen, wie jeder Pauschalvertrag. In der Kostenaufteilung erscheinen sie als eigene Kategorie **Hauskosten**.
- **Eigene Gruppe:** Im Panel stehen Hauskosten in einer eigenen Gruppe **Hauskosten** (nach den Pauschalverträgen und vor den Krediten).
- **Wortwahl:** Das Panel spricht bei Hauskosten von **Betrag**, nicht von „Abschlag“ („Betrag / Monat“, „Gezahlte Beträge“).
- **Kündigung und Verlängern:** Vertragsende (auch leer), Kündigungsfrist und Erinnerung wie bei jeder Sparte. **Vertrag verlängern** geht auch ohne Vertragsende, zum Beispiel wenn sich eine Gebühr ändert (Ende im Dialog leer lassen).
- **Eigenes Icon:** Mit dem Feld **Icon** bekommt der Vertrag ein eigenes Symbol; leer = das Haus-Symbol der Sparte.
- **Was fehlt:** Es gibt keinen Zähler und keine Prognose. Für Wasser mit Zähler nimm [Wasser](Vertrag-Wasser), für die Gebäudeversicherung [Versicherung](Vertrag-Versicherung).

## Schritt für Schritt

1. Im Panel im Tab **Verträge** auf **Neuer Vertrag** klicken. Die allgemeinen Schritte stehen auf [Verträge anlegen](Vertraege-Anlegen).
2. **Schritt 1:** Bezeichnung (zum Beispiel „Abfallgebühren“), Sparte **Hauskosten**, Anbieter (zum Beispiel die Stadt oder Gemeinde), Vertragsbeginn und, falls vorhanden, Vertragsende und Erinnerung eintragen.
3. **Schritt 2, Art:** **Art der Hauskosten** aus der Liste wählen oder eintippen. Leer lassen geht auch.
4. **Schritt 3, Kosten:** **Zahlweise** wählen, **Betrag pro Zahlung (€)** eintragen und bei nicht monatlicher Zahlung **Erste Abbuchung am** setzen.
5. Speichern.

## Felder im Überblick

Schritt 1 ist auf [Vertrag: Internet und Mobilfunk](Vertrag-Internet-und-Mobilfunk#felder-im-überblick) beschrieben. Die weiteren Schritte:

| Feld | Schritt | Pflicht | Bedeutung | Standard |
|------|---------|---------|-----------|----------|
| Art der Hauskosten | 2 | nein | Aus der Liste gewählt oder frei eingetippt | leer |
| Zahlweise | 3 | ja | Monatlich, Vierteljährlich, Halbjährlich oder Jährlich | Monatlich |
| Betrag pro Zahlung (€) | 3 | ja | Der Betrag einer Zahlung in der gewählten Zahlweise (zum Beispiel eine Quartalsrate) | 0 |
| Erste Abbuchung am | 3 | nein | Tag der ersten Abbuchung; leer = Vertragsbeginn | leer |

Das Feld **Grundpreis (€/Monat)** erscheint nur beim Bearbeiten eines Vertrags, der schon einen hat.

## So sieht es im Panel aus

Die Karte in der Gruppe **Hauskosten** zeigt vorn die Art, dann den Anbieter und den Tarif, darunter **Betrag / Monat**, die Zahlung je Rate und **Kosten bisher**.

<table align="center"><tr><td align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/house-costs-card.png" alt="Karte Abfallgebühren in der Gruppe Hauskosten: Betrag pro Monat 31 Euro, 93 Euro vierteljährlich, Kosten bisher 279 Euro (dunkles Design)" width="380"><br><sub>Dunkel</sub></td><td align="center"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/house-costs-card-light.png" alt="Karte Abfallgebühren in der Gruppe Hauskosten: Betrag pro Monat 31 Euro, 93 Euro vierteljährlich, Kosten bisher 279 Euro (helles Design)" width="380"><br><sub>Hell</sub></td></tr></table>

*Abbildung: Karte in der Übersicht (Mock-Daten, Datum 12.07.2026).*

Im Tab **Verträge** stehen die Details: die Art unter **Vertrag**, die Zahlung und die nächste Zahlung unter **Preise** und rechts die **Gezahlten Beträge**.

<table align="center"><tr><td align="center" width="50%"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/house-costs-details.png" alt="Details des Vertrags Abfallgebühren mit Art der Hauskosten, Preisen, Einmalposten und gezahlten Beträgen (dunkles Design)" width="100%"><br><sub>Dunkel</sub></td><td align="center" width="50%"><img src="https://raw.githubusercontent.com/wiki/weskona/tariffy/images/house-costs-details-light.png" alt="Details des Vertrags Abfallgebühren mit Art der Hauskosten, Preisen, Einmalposten und gezahlten Beträgen (helles Design)" width="100%"><br><sub>Hell</sub></td></tr></table>

*Abbildung: Details im Tab Verträge (Mock-Daten).*

## Betrag ändert sich und Folgevertrag

Gebühren ändern sich oft zum Jahreswechsel. Du hast drei Wege, wie bei [Sonstiges](Vertrag-Sonstiges#preisänderung-und-folgevertrag):

- **Mitten in der Laufzeit:** Trage den neuen Betrag im Vertrag ein; er gilt ab dem Tag des Speicherns. Hat der Versorger rückwirkend andere Beträge abgebucht, korrigierst Du sie unter **Gezahlte Beträge eintragen** ([Abschlagsverlauf und Einmalposten](Abschlagsverlauf-und-Einmalposten)).
- **Zum Ende der Laufzeit:** **Vertrag verlängern**, auch ohne Vertragsende ([Folgevertrag oder Verlängern](Folgevertrag-oder-Verlaengern)).
- **Bekannter Wechsel:** **Folgevertrag planen** mit dem Formular der Pauschalverträge (Wechseldatum, Anbieter, Tarifname, Betrag pro Monat und so weiter).

## Rechenbeispiel

Beispielwerte (nicht aus einem echten Vertrag): „Abfallgebühren“ mit Sparte **Hauskosten**, Art **Abfallgebühren**, Beginn 1. Januar 2026, Zahlweise **Vierteljährlich**, **93 €** pro Zahlung.

```
Gespeichert wird der Monatsbetrag:  93 € / 3 = 31,00 € im Monat
Kosten pro Jahr:                    31,00 € × 12 = 372,00 €
Kosten bisher am 12.07.2026:        279,00 €   (drei Abbuchungen: 01.01., 01.04., 01.07.)
Nächste Zahlung:                    01.10.2026
```

## Typische Fehler

- **Monatsbetrag statt Betrag pro Zahlung.** Bei Zahlweise „Vierteljährlich“ gehört die Quartalsrate (93 €) ins Feld, nicht der Monatsbetrag (31 €).
- **Hauskosten gewählt, obwohl ein Zähler mitläuft.** Wasser mit Zähler gehört in [Wasser](Vertrag-Wasser); dort rechnet Tariffy mit dem Verbrauch.
- **Erste Abbuchung nicht gesetzt.** Ohne Angabe nimmt Tariffy die erste Rate am Vertragsbeginn an; liegt die erste echte Abbuchung später, trage das Datum ein.
- **Die Art muss nicht „stimmen“.** Sie dient nur der Übersicht und ändert nichts an der Rechnung. Eine eigene Art zeigt das Panel genau so an, wie Du sie getippt hast.

> **Gut zu wissen:** Die Sparte lässt sich beim Bearbeiten ändern. Prüfe danach die Felder des neuen Schritts, weil jede Sparte eigene Felder hat.

## Siehe auch

- [Vertrag: Sonstiges](Vertrag-Sonstiges)
- [Vertrag: Internet und Mobilfunk](Vertrag-Internet-und-Mobilfunk)
- [Abschläge und Kosten](Abschlaege-und-Kosten)
- [Folgevertrag oder Verlängern](Folgevertrag-oder-Verlaengern)
- [Verträge anlegen](Vertraege-Anlegen)
