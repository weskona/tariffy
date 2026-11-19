🇩🇪 Deutsch · [🇬🇧 English](EN-Contract-Streaming)

# Vertrag: Streaming

Die Sparte **Streaming** ist für Abos wie Video-, Musik- oder Spieldienste. Sie ist ein **Pauschalvertrag** mit einem Preis pro Zahlung und hat ein eigenes, kurzes Formular für den **Folgevertrag**.

**Inhalt:**
- [Was anders ist als bei anderen Pauschalverträgen](#was-anders-ist-als-bei-anderen-pauschalverträgen)
- [Schritt für Schritt](#schritt-für-schritt)
- [Felder im Überblick](#felder-im-überblick)
- [Der Folgevertrag im Kurzformular](#der-folgevertrag-im-kurzformular)
- [Rechenbeispiel](#rechenbeispiel)
- [Typische Fehler](#typische-fehler)
- [Siehe auch](#siehe-auch)

## Was anders ist als bei anderen Pauschalverträgen

Die Kosten werden wie bei [Internet und Mobilfunk](Vertrag-Internet-und-Mobilfunk) gezählt: Zahlweise, Betrag pro Zahlung, Kosten bisher als gebuchte Raten. Bei Streaming gibt es drei Unterschiede:

- **Der Betrag heißt im Panel „Preis“** statt „Abschlag“ (zum Beispiel **Preis / Monat**). Der Dialog zum Korrigieren zurückliegender Zahlungen heißt **Beträge bearbeiten**, der Block **Gezahlte Beträge**.
- **Der Block „Einmalposten“ fehlt**, solange der Vertrag keine hat; ein Abo braucht ihn meist nicht. Hat ein Streaming-Vertrag schon Einmalposten, bleibt der Block mit ihnen sichtbar.
- **Die Zeile „Abschlag / Jahr“ wird nicht doppelt gezeigt.**

Der Folgevertrag hat ein kürzeres Formular, siehe [unten](#der-folgevertrag-im-kurzformular).

## Schritt für Schritt

1. Im Panel im Tab **Verträge** auf **Neuer Vertrag** klicken. Die allgemeinen Schritte stehen auf [Verträge anlegen](Vertraege-Anlegen).
2. **Schritt 1:** Bezeichnung, Sparte **Streaming**, Anbieter, Tarifname (zum Beispiel „Standard“), Vertragsbeginn und, wenn das Abo eine feste Laufzeit hat, das Vertragsende eintragen.
3. **Schritt 2, Kosten:** **Zahlweise** wählen und **Betrag pro Zahlung (€)** eintragen. Wird nicht monatlich gezahlt, setzt du **Erste Abbuchung am**.
4. Speichern.
5. Optional später: im Tab **Verträge** das Symbol **Folgevertrag planen** wählen, wenn der Preis oder die Zahlweise zu einem bekannten Datum wechselt.

## Felder im Überblick

Schritt 1 (allgemeine Daten) ist für alle Sparten gleich und auf [Vertrag: Internet und Mobilfunk](Vertrag-Internet-und-Mobilfunk#felder-im-überblick) beschrieben. Schritt 2:

| Feld | Pflicht | Bedeutung | Standard |
|------|---------|-----------|----------|
| Zahlweise | ja | Monatlich, Vierteljährlich, Halbjährlich oder Jährlich | Monatlich |
| Betrag pro Zahlung (€) | ja | Der Betrag einer Zahlung in der gewählten Zahlweise | 0 |
| Erste Abbuchung am | nein | Tag der ersten Abbuchung; leer = Vertragsbeginn | leer |

Tariffy speichert den Betrag pro Monat (120 € jährlich werden als 10 € im Monat gespeichert) und zeigt beim Bearbeiten wieder den Betrag pro Zahlung.

## Der Folgevertrag im Kurzformular

Das Symbol **Folgevertrag planen** öffnet bei Streaming das Formular **Folgevertrag planen** mit nur fünf Feldern. Zum Beginn übernimmt Home Assistant die neue Laufzeit automatisch (geprüft täglich um 00:00:01 Uhr, zusätzlich beim regulären Abruf und beim Start von Home Assistant).

| Feld | Pflicht | Bedeutung |
|------|---------|-----------|
| Beginn der neuen Laufzeit | nein | Vorgeschlagen wird der **Tag nach dem Vertragsende**, auch über den Jahreswechsel. Ohne Vertragsende gibt es keinen Vorschlag. Ein schon geplanter Beginn wird nicht durch den Vorschlag ersetzt. **Leer lassen entfernt einen geplanten Vertrag.** |
| Tarifname (neu) | nein | Neuer Tarifname |
| Zahlweise (neu) | nein | Standard ist die aktuelle Zahlweise; so wechselst du zum Beispiel von jährlich auf monatlich |
| Betrag pro Zahlung (neu, €) | nein | Betrag je Zahlung in der gewählten Zahlweise; gespeichert wird der Betrag pro Monat |
| Ende der neuen Laufzeit / gültig bis | nein | Ende der neuen Laufzeit |

Drei weitere Felder erscheinen nur, wenn der geplante Vertrag sie schon hat: **Anbieter (neu)**, **Kundennummer (neu)** und **Grundpreis neu (€/Monat)**.

So verhält sich der Wechsel:

- **Nicht ausgefüllte Felder behalten den aktuellen Wert**, auch die Zahlweise (sie fällt nicht auf „monatlich“ zurück).
- **Die erste Abbuchung der neuen Laufzeit ist ihr Beginn.** Eine alte Angabe bei „Erste Abbuchung am“ entfällt.
- Alle anderen Sparten behalten ihr bisheriges Formular. Strom, Gas, Wasser, Internet, Mobilfunk, Versicherung, Leasing und Sonstiges fragen weiter nach Anbieter, Kundennummer, Grundpreis und so weiter.
- Der geplante Folgevertrag steckt auch in der Tariffy-Sicherung.

Das Formular für Strom, Gas, Wasser und die übrigen Sparten ist auf [Folgevertrag oder Verlängern](Folgevertrag-oder-Verlaengern) beschrieben.

## Rechenbeispiel

Beispielwerte aus den Tests: Streaming-Abo „Standard“ von Netflix, Beginn 1. April 2026, Ende 31. März 2027, Zahlweise **Jährlich**, 10 € im Monat, also **120 € pro Zahlung**.

Du planst den Wechsel auf ein Monatsabo: Im Formular **Folgevertrag planen** steht schon der Beginn **01.04.2027** (Tag nach dem Ende). Du trägst ein:

| Feld | Eingabe |
|------|---------|
| Zahlweise (neu) | Monatlich |
| Betrag pro Zahlung (neu, €) | 12,99 |
| Tarifname (neu) | Monatsabo |

Am 1. April 2027 gilt der neue Vertrag mit Zahlweise monatlich, 12,99 € und dem Tarifnamen „Monatsabo“. Der Anbieter („Netflix“) bleibt, weil du ihn nicht geändert hast.

Die Umrechnung läuft in beide Richtungen: Wählst du bei „Zahlweise (neu)“ **Jährlich** und trägst 120 ein, speichert Tariffy 10 € pro Monat und zeigt beim nächsten Öffnen des Formulars wieder 120.

## Typische Fehler

- **Beginn leer gelassen.** Ohne **Beginn der neuen Laufzeit** wird nichts geplant, und ein vorhandener Plan wird entfernt. Der Beginn ist Pflicht für den Plan.
- **Monatsbetrag statt Betrag pro Zahlung.** Bei Zahlweise „Jährlich“ trägst du den Jahresbetrag ein.
- **Kein Vertragsende, kein Beginn-Vorschlag.** Dann musst du den Beginn selbst eintragen.
- **Anbieter oder Kundennummer ändern wollen.** Diese Felder zeigt das Kurzformular nur, wenn der Plan sie schon hat. Änderst du Anbieter oder Kundennummer, bearbeite den Vertrag nach dem Wechsel mit **Vertrag bearbeiten**.
- **Erinnerung vergessen.** Auch ein Abo braucht für eine Kündigungs-Erinnerung ein Vertragsende, siehe [Vertragsende und Wechsel](Vertragsende-und-Wechsel).

> **Gut zu wissen:** Für ein Abo ohne festes Ende nutzt du bei einer Preiserhöhung das Symbol **Vertrag verlängern** mit leerem Ende oder trägst den neuen Betrag direkt im Vertrag ein; er gilt ab dem Tag des Speicherns.

## Siehe auch

- [Vertrag: Internet und Mobilfunk](Vertrag-Internet-und-Mobilfunk)
- [Folgevertrag oder Verlängern](Folgevertrag-oder-Verlaengern)
- [Vertragsende und Wechsel](Vertragsende-und-Wechsel)
- [Abschlagsverlauf und Einmalposten](Abschlagsverlauf-und-Einmalposten)
- [Abschläge und Kosten](Abschlaege-und-Kosten)
