🇩🇪 Deutsch · [🇬🇧 English](EN-Contract-Internet-and-Mobile)

# Vertrag: Internet und Mobilfunk

Internet- und Mobilfunkverträge sind **Pauschalverträge**: Du zahlst einen festen Betrag, es gibt keinen Zähler und keinen Verbrauch. Diese Seite zeigt, welche Felder Tariffy dafür abfragt, wie die Kosten gezählt werden und was du bei Preisänderungen und Kündigung beachten solltest.

**Inhalt:**
- [Was Tariffy für Pauschalverträge rechnet](#was-tariffy-für-pauschalverträge-rechnet)
- [Schritt für Schritt](#schritt-für-schritt)
- [Felder im Überblick](#felder-im-überblick)
- [Laufzeit, Mindestlaufzeit und Kündigung](#laufzeit-mindestlaufzeit-und-kündigung)
- [Preisänderung und Aktionspreis](#preisänderung-und-aktionspreis)
- [Rechenbeispiel](#rechenbeispiel)
- [Typische Fehler](#typische-fehler)
- [Siehe auch](#siehe-auch)

## Was Tariffy für Pauschalverträge rechnet

Die Sparten **Internet** und **Mobilfunk** gehören (wie Streaming, Versicherung und Sonstiges) zu den Pauschalverträgen. Du wählst die **Zahlweise** (monatlich, vierteljährlich, halbjährlich, jährlich) und trägst den **Betrag pro Zahlung** ein. Intern rechnet Tariffy mit dem Betrag pro Monat (600 € jährlich sind 50 € im Monat).

Die **Kosten bisher** sind die **gebuchten Raten**, es gibt keine Prognose aus einem Verbrauch:

- **Monatliche Zahlung:** Die Rate eines Monats zählt **ab dem ersten Tag dieses Monats**, egal an welchem Tag abgebucht wird.
- **Vierteljährlich, halbjährlich, jährlich:** Jede Abbuchung zählt am Tag der Zahlung. Mit dem Feld **Erste Abbuchung am** legst du ihren Tag fest; die weiteren folgen im Abstand der Zahlweise.
- Abbuchungen nach dem Vertragsende gehören schon zur nächsten Laufzeit.

Mehr dazu auf [Abschläge und Kosten](Abschlaege-und-Kosten).

## Schritt für Schritt

1. Im Panel im Tab **Verträge** auf **Neuer Vertrag** klicken (oder in Home Assistant unter Einstellungen → Integrationen → Tariffy eine Integration hinzufügen). Die allgemeinen Schritte sind auf [Verträge anlegen](Vertraege-Anlegen) beschrieben.
2. **Schritt 1, allgemeine Daten:** Bezeichnung, **Sparte** (Internet oder Mobilfunk), Anbieter, Vertragsbeginn, Vertragsende, Mindestlaufzeit, Kündigungsfrist und Erinnerung eintragen.
3. **Schritt 2, Kosten:** **Zahlweise** wählen, **Betrag pro Zahlung** eintragen und, wenn du nicht monatlich zahlst, **Erste Abbuchung am** setzen.
4. Speichern. Der Vertrag erscheint von selbst im Panel.

Nachträglich änderst du alles mit **Vertrag bearbeiten**: Das Panel zeigt dieselben zwei Formulare und fragt vor dem Speichern noch einmal nach.

## Felder im Überblick

**Schritt 1, allgemeine Daten** (gilt für alle Sparten):

| Feld | Pflicht | Bedeutung | Standard |
|------|---------|-----------|----------|
| Bezeichnung (z. B. Strom Haus) | ja | Anzeigename, erscheint im Gerätenamen (zum Beispiel „Internet Zuhause“) | – |
| Sparte | ja | **Internet** oder **Mobilfunk** | Strom |
| Anbieter | ja | Name des Anbieters | – |
| Kundennummer | nein | Deine Kundennummer; gilt als persönlich und ist nur für Administratoren im Panel sichtbar | – |
| Tarifname | nein | Bezeichnung des Tarifs | – |
| Icon | nein | Eigenes Icon, zum Beispiel `mdi:router-wireless`; leer = Icon der Sparte | leer |
| Vertragsbeginn | nein | Tag, ab dem der Vertrag gilt; die erste Rate nimmt Tariffy an diesem Tag an | – |
| Vertragsende / Laufzeit bis | nein | Letzter Gültigkeitstag des Vertrags | – |
| Mindestlaufzeit (Monate) | nein | Das Panel zeigt, bis wann der Vertrag mindestens läuft (Beginn plus Mindestlaufzeit) | – |
| Kündigungsfrist (Monate) | nein | Monate vor Vertragsende, bis zu denen die Kündigung vorliegen muss | – |
| Kündigung erinnern | ja | „Keine Erinnerung“ oder 1 bis 4 Monate vorher | 3 Monate vorher |
| Benachrichtigungs-Ziel (notify-Dienst) | nein | Dienst für die Erinnerung, zum Beispiel `mobile_app_iphone`; das Feld erscheint nur, wenn es notify-Dienste gibt | – |

**Schritt 2, Kosten:**

| Feld | Pflicht | Bedeutung | Standard |
|------|---------|-----------|----------|
| Zahlweise | ja | Monatlich, Vierteljährlich, Halbjährlich oder Jährlich | Monatlich |
| Betrag pro Zahlung (€) | ja | Der Betrag einer Zahlung in der gewählten Zahlweise | 0 |
| Erste Abbuchung am | nein | Tag der ersten Abbuchung; leer = Vertragsbeginn. Die weiteren folgen im Abstand der Zahlweise | leer |

Das frühere Feld **Grundpreis (€/Monat)** gibt es bei neuen Pauschalverträgen nicht mehr. Es erscheint nur noch beim Bearbeiten eines Vertrags, der schon einen Grundpreis hat; dort lässt sich der Wert leeren.

## Laufzeit, Mindestlaufzeit und Kündigung

- **Mindestlaufzeit** ist nur eine Anzeige im Panel („bis …“). Sie löst keine Erinnerung aus.
- **Kündigungsfrist:** Wenn du sie einträgst, bezieht sich die Erinnerung auf den **letzten Kündigungstag** (Vertragsende minus Frist) statt auf das Vertragsende.
- **Kündigung erinnern** bestimmt, wie viele Monate vor diesem Termin Tariffy meldet: eine Dauerbenachrichtigung in Home Assistant und, wenn eingetragen, eine Push-Meldung über das **Benachrichtigungs-Ziel**. Mit dem Button „Kündigung bestätigen“ quittierst du die Erinnerung.
- Beispiel: Vertragsende 31.12., Kündigungsfrist 3 Monate, Erinnerung „3 Monate vorher“. Die Kündigung muss bis 30.09. vorliegen, die Meldung kommt am 30.06.

Alle Einzelheiten stehen auf [Vertragsende und Wechsel](Vertragsende-und-Wechsel).

## Preisänderung und Aktionspreis

Tariffy kennt für Pauschalverträge **keine Preisphasen** (zum Beispiel „die ersten 12 Monate günstiger“). Es gibt einen Betrag pro Zahlung. Das kannst du tun, wenn sich der Preis ändert:

- **Der Betrag steigt oder sinkt mitten in der Laufzeit:** Trage im Vertrag den neuen Betrag ein. Er gilt ab dem Tag des Speicherns, davor rechnet Tariffy mit dem alten. Eine Änderung nur der Zahlweise zählt nicht als Preisänderung.
- **Die Laufzeit endet und der Preis ändert sich:** Nutze das Symbol **Vertrag verlängern** (zwei Pfeile im Kreis, nur Administratoren) im Tab **Verträge**. Die bisherige Laufzeit kommt in die Historie, der Vertrag läuft mit neuem Beginn, Ende und Betrag weiter. Das Panel zeigt sofort, um wie viel Prozent der Vertrag teurer oder günstiger wird (verglichen pro Monat). Der Dialog ist auf [Folgevertrag oder Verlängern](Folgevertrag-oder-Verlaengern) beschrieben.
- **Du kennst den Wechseltermin schon:** Plane einen Folgevertrag (Symbol **Folgevertrag planen**); am Wechseldatum übernimmt Home Assistant ihn automatisch. Das Formular fragt den Betrag pro Monat („Abschlag neu (€/Monat)“), nicht pro Zahlung.
- **Du willst zurückliegende Beträge korrigieren:** Im Block **Gezahlte Abschläge** der Vertragsdetails (Dialog **Abschläge bearbeiten**) trägst du ein, was wirklich gezahlt wurde. Siehe [Abschlagsverlauf und Einmalposten](Abschlagsverlauf-und-Einmalposten).
- **Wechselbonus oder Anschlusskosten:** Das Feld „Neukundenbonus“ gibt es nur bei Strom. Für Internet und Mobilfunk trägst du einen **Einmalposten** ein: ein positiver Betrag ist eine Gutschrift, ein negativer eine Rechnung.

## Rechenbeispiel

Beispielwerte (nicht aus einem echten Vertrag): Mobilfunkvertrag „Handy Anna“, Beginn 1. April, monatliche Zahlung von 17,99 €, Abbuchung jeweils am 27.

Am 13. November sind acht Raten gezählt (April bis November), obwohl die Novemberrate erst am 27. abgebucht wird:

```
8 Raten × 17,99 € = 143,92 €   (Kosten bisher)
```

Später wird der Vertrag zum Ende der Laufzeit verlängert. Im Verlängern-Dialog stehen bei einem Internetvertrag, der bisher 39,99 € im Monat kostet, die Zahlweise „jährlich“ und der Betrag 432 € pro Zahlung. Darunter zeigt der Dialog:

```
432 € / 12 = 36,00 € im Monat  →  10,0 % günstiger (36,00 € statt 39,99 € pro Monat)
```

![Dialog Vertrag verlängern für einen Internetvertrag mit Zahlweise jährlich, Betrag 432 und dem Hinweis 10,0 % günstiger](https://raw.githubusercontent.com/wiki/weskona/tariffy/images/renew-dialog.png)

*Abbildung: Der Dialog „Vertrag verlängern“ für einen Internetvertrag (Beispieldaten). Unter dem Betrag steht der Vergleich pro Monat.*

Mit **Verlängern** kommt die alte Laufzeit in die Historie, und der Vertrag läuft mit dem neuen Betrag weiter.

## Typische Fehler

- **Jahresbetrag bei „Monatlich“ eingetragen.** Der Betrag gilt pro Zahlung. Zahlst du jährlich 432 €, wähle die Zahlweise **Jährlich** und trage 432 ein, nicht 36.
- **Kein Vertragsbeginn.** Die erste Rate nimmt Tariffy am Vertragsbeginn an, trage ihn deshalb ein.
- **Die erste Abbuchung weicht vom Vertragsbeginn ab.** Bei nicht monatlicher Zahlung setzt du **Erste Abbuchung am**, sonst zählt Tariffy die Abbuchungen ab dem Vertragsbeginn.
- **Preis erhöht, aber nur das Vertragsende geändert.** Trage den neuen Betrag ein oder verlängere den Vertrag, sonst rechnet Tariffy weiter mit dem alten Preis.
- **Keine Erinnerung.** „Kündigung erinnern“ steht auf „Keine Erinnerung“, oder es ist kein Vertragsende eingetragen.
- **Kündigung vergessen zu bestätigen.** Die Dauerbenachrichtigung bleibt bestehen, bis du „Kündigung bestätigen“ drückst.

> **Gut zu wissen:** Der Name des Vertrags lässt sich beim Bearbeiten im ersten Feld ändern; Sensoren und Entity-IDs bleiben dabei bestehen.

## Siehe auch

- [Verträge anlegen](Vertraege-Anlegen)
- [Abschläge und Kosten](Abschlaege-und-Kosten)
- [Abschlagsverlauf und Einmalposten](Abschlagsverlauf-und-Einmalposten)
- [Vertragsende und Wechsel](Vertragsende-und-Wechsel)
- [Folgevertrag oder Verlängern](Folgevertrag-oder-Verlaengern)
- [Vertrag: Streaming](Vertrag-Streaming)
- [Sensoren-Referenz](Sensoren-Referenz)
