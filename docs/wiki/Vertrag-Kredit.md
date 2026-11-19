🇩🇪 Deutsch · [🇬🇧 English](EN-Contract-Loan)

# Vertrag: Kredit und Finanzierung

Die Sparte **Kredit / Finanzierung** ist für Annuitätendarlehen (Baufinanzierung), Ratenkredite und Autofinanzierungen. Tariffy erstellt aus Summe, Zins, Laufzeit und Zahlweise einen Tilgungsplan und zeigt dir die Restschuld, die gezahlten Zinsen und die nächste Rate.

**Inhalt:**
- [Kredite laufen getrennt](#kredite-laufen-getrennt)
- [Schritt für Schritt](#schritt-für-schritt)
- [Felder im Überblick](#felder-im-überblick)
- [So rechnet Tariffy](#so-rechnet-tariffy)
- [Was Tariffy anzeigt](#was-tariffy-anzeigt)
- [Anschlussfinanzierung: Kredit verlängern](#anschlussfinanzierung-kredit-verlängern)
- [Rechenbeispiel](#rechenbeispiel)
- [Typische Fehler](#typische-fehler)
- [Siehe auch](#siehe-auch)

## Kredite laufen getrennt

Der Kredit hat im Panel eine **eigene Gruppe** (**Kredite / Finanzierungen**) und zählt **nicht** in die Summen der Verträge (Abschläge pro Monat, Kosten bisher, Kostenaufteilung). Das Panel weist darauf hin: „Kredite laufen getrennt: Sie zählen nicht in die Summen der Verträge.“ Ein Leasingvertrag steht in derselben Gruppe, zählt aber in den Summen mit, siehe [Vertrag: Leasing](Vertrag-Leasing).

## Schritt für Schritt

1. Im Panel im Tab **Verträge** auf **Neuer Vertrag** klicken. Die allgemeinen Schritte stehen auf [Verträge anlegen](Vertraege-Anlegen).
2. **Schritt 1, allgemeine Daten:** Bezeichnung (zum Beispiel „Baufinanzierung“), Sparte **Kredit / Finanzierung**, Anbieter und **Vertragsbeginn**. Das Vertragsende musst du hier nicht eintragen: Es ergibt sich aus dem Beginn und der Laufzeit.
3. **Schritt „Kredit / Finanzierung“:** die Daten so eintragen, wie sie im Kreditvertrag stehen (siehe Tabelle unten). Die Rate ist freiwillig.
4. Speichern. Es gibt keinen weiteren Kosten-Schritt.

Nachträglich änderst du alles mit **Vertrag bearbeiten**.

## Felder im Überblick

Schritt 1 ist auf [Vertrag: Internet und Mobilfunk](Vertrag-Internet-und-Mobilfunk#felder-im-überblick) beschrieben. Der Schritt **Kredit / Finanzierung**:

| Feld | Pflicht | Bedeutung | Standard |
|------|---------|-----------|----------|
| Kreditsumme (€) | ja | Der geliehene Betrag laut Vertrag. Muss über null liegen | 0 |
| Sollzins (% pro Jahr) | nein | Nominalzins pro Jahr. Mit ihm rechnen die Banken die Rate. Bleibt er leer, wird der effektive Jahreszins genommen | leer |
| Effektiver Jahreszins (%) | nein | Zur Information und als Ersatz, wenn es keinen Sollzins gibt. **Einer der beiden Zinssätze ist nötig** | leer |
| Laufzeit (Monate) | ja | Monate ab Vertragsbeginn bis zum Ende; 1 bis 600 | 12 |
| Zahlweise | ja | Monatlich, Vierteljährlich, Halbjährlich oder Jährlich | Monatlich |
| Rate je Zahlung (€) | nein | Die Rate aus deinem Vertrag. **Leer = Tariffy rechnet die Annuität aus** | leer |
| Schlussrate / Restwert (€) | nein | Ein Betrag, der am Ende noch offen ist und mit der letzten Rate gezahlt wird (Autofinanzierung) | leer |
| Datum der ersten Rate | nein | Leer = ein Zahlungsintervall nach dem Beginn (bei monatlicher Zahlung: Ende des ersten Monats) | leer |

## So rechnet Tariffy

- **Zins je Zahlung** = Sollzins geteilt durch die Zahlungen pro Jahr (monatlich: 5 % ergeben 5 / 12 % je Rate). Ohne Sollzins wird der Satz aus dem effektiven Jahreszins abgeleitet.
- **Anzahl der Raten** = Laufzeit geteilt durch das Zahlungsintervall in Monaten (24 Monate vierteljährlich sind 8 Raten).
- **Jede Rate** besteht aus Zinsen auf die Restschuld und Tilgung; der Zinsanteil sinkt von Rate zu Rate.
- **Annuität:** Ohne eingetragene Rate rechnet Tariffy die gleichbleibende Rate aus, die die Summe bis auf die Schlussrate tilgt. Ohne Zins (Zins 0) wird gleichmäßig getilgt.
- **Eingetragene Rate:** Sie hat Vorrang vor der berechneten. Weicht sie um **mehr als 1 %** von der Rate ab, die der Zins ergibt, meldet Tariffy das und zeigt die berechnete Rate.
- **Schlussrate / Restwert:** Wird mit der **letzten Rate** gezahlt. Ist eine eingetragene Rate zu niedrig, bleibt am Ende ein Rest, der ebenfalls mit der letzten Rate gezahlt wird.
- **Eine Rate zählt ab ihrem Datum**, die Rate des Tages zählt mit.
- **Nicht enthalten:** Sondertilgungen und ein Zins, der sich innerhalb der Laufzeit ändert.

Fehlen Summe, Laufzeit, Beginn oder ein Zinssatz, lässt sich der Kredit noch nicht berechnen.

## Was Tariffy anzeigt

- **Im Panel**, Block **Kredit**: **Restschuld**, **Gezahlt bisher** (Zinsen und Tilgung), **Restsumme** (noch zu zahlen bis zum Ende), die **Nächste Rate** mit der Aufteilung „Zinsen … · Tilgung …“, der Fortschritt **Getilgt** und die **Raten gezahlt**. In den Details kommen dazu: Kreditsumme, Sollzins, Effektiver Jahreszins, Laufzeit, Rate, Rate laut Zins, Schlussrate am Ende, Zinsen bisher, Getilgt bisher, Zinsen über die Laufzeit, Summe aller Zahlungen und Erste Rate.
- **Hinweise:** „Der Kredit lässt sich noch nicht berechnen: Summe, Laufzeit, Beginn und ein Zinssatz werden gebraucht.“ und, wenn deine Rate abweicht: „Deine Rate weicht um … % von der ab, die der Zins ergibt (…).“
- **Sensoren:** Jeder Kredit hat vier: **Restschuld**, **Gezahlt bisher**, **Restsumme** und **Zinsen bisher**. Die Attribute und Entity-IDs stehen in der [Sensoren-Referenz](Sensoren-Referenz).

## Anschlussfinanzierung: Kredit verlängern

Läuft die Zinsbindung oder der Kredit aus, geht es mit einem neuen Kredit weiter. Im Tab **Verträge** hat der Kredit dafür das Symbol **Vertrag verlängern** (nur Administratoren). Es öffnet den Dialog **Anschlussfinanzierung**. Ein Kredit hat **kein** Symbol für einen Folgevertrag.

![Dialog Anschlussfinanzierung für den Kredit Baufinanzierung mit Beginn, neuer Kreditsumme, Sollzins, effektivem Jahreszins, Laufzeit, Zahlweise, Rate, Schlussrate und erster Abbuchung](https://raw.githubusercontent.com/wiki/weskona/tariffy/images/loan-renew-dialog.png)

*Abbildung: Der Dialog „Anschlussfinanzierung“ für eine Baufinanzierung (Beispieldaten).*

Der Dialog schlägt vor:

| Feld | Vorschlag |
|------|-----------|
| Beginn | das bisherige Vertragsende |
| Neue Kreditsumme (€) | die **Restschuld** |
| Sollzins (% pro Jahr), Effektiver Jahreszins (%) | die bisherigen Werte |
| Laufzeit (Monate) | die bisherige Laufzeit |
| Zahlweise | die bisherige Zahlweise |
| Rate je Zahlung (freiwillig), Schlussrate (freiwillig), Erste Abbuchung (optional) | leer |

Du passt Summe, Zins und Laufzeit an die neuen Konditionen an. Mit **Verlängern** kommt die bisherige Laufzeit in die **Historie** (mit Summe, Zins und Kosten), und der Kredit läuft mit den neuen Werten weiter. Rate, Schlussrate und Effektivzins der alten Laufzeit übernimmt Tariffy nicht, was du leer lässt, gilt für den neuen Kredit als nicht gesetzt.

## Rechenbeispiel

Werte aus den Tests: Kredit über **10 000 €**, **5 % Sollzins**, **12 Monate**, monatlich, Beginn **15. Januar 2026**, keine Rate eingetragen. Stichtag **20. Juni 2026**.

```
Rate (Annuität):          856,07 €
Erste Rate:               15.02.2026   →  bis zum 20.06. sind 5 Raten fällig (Feb bis Juni)
Zins der 1. Rate:         10 000 × 5 % / 12 = 41,67 €  (Tilgung 814,40 €)

Zinsen bisher:            174,26 €
Getilgt bisher:           4 106,12 €
Gezahlt bisher:           4 280,37 €   (Zinsen plus Tilgung)
Restschuld:               10 000 − 4 106,12 = 5 893,88 €
Restsumme:                5 992,52 €     (noch zu zahlen bis zum 15.01.2027)
Zinsen über die Laufzeit: 272,90 €
Summe aller Zahlungen:    10 272,90 €
Nächste Rate:             15.07.2026, 856,07 € (24,56 € Zinsen · 831,52 € Tilgung)
Fortschritt:              41,1 % getilgt
```

Gezahlt bisher plus Restsumme ergeben (bis auf Cent-Rundung) die Summe aller Zahlungen. Trägst du statt der berechneten Rate 900 € ein, zeigt Tariffy die Abweichung von 5,13 % und weist darauf hin, weil sie über 1 % liegt.

## Typische Fehler

- **Kreditsumme 0.** Das Formular lehnt es ab: „Trage eine Kreditsumme über null ein.“
- **Kein Zinssatz.** Das Formular lehnt es ab: „Trage den Sollzins oder den effektiven Jahreszins ein.“ Trage mindestens einen der beiden ein.
- **Kein Vertragsbeginn.** Ohne Beginn kann Tariffy keinen Plan rechnen; trage ihn in Schritt 1 ein.
- **Effektivzins statt Sollzins für die Rate erwartet.** Die Bank rechnet die Rate mit dem Sollzins. Trägst du nur den Effektivzins ein, leitet Tariffy daraus einen Satz ab. Trage deshalb möglichst den Sollzins ein oder die Rate aus dem Vertrag.
- **Rate und Zins passen nicht.** Weicht deine Rate um mehr als 1 % ab, zeigt Tariffy beide Werte. Prüfe Zins, Zahlweise und Schlussrate.
- **Sondertilgung erwartet.** Sondertilgungen rechnet Tariffy nicht ein, die Restschuld kann deshalb von der Bank abweichen.
- **Falsche Zahlweise.** Bei vierteljährlicher Zahlung ist die Rate je Zahlung der Quartalsbetrag, nicht der Monatsbetrag.
- **Anschlussfinanzierung mit alter Rate.** Im Dialog bleiben Rate und Schlussrate leer; lass sie leer, wenn Tariffy die neue Rate ausrechnen soll.

> **Gut zu wissen:** Der Block „Gezahlte Abschläge“ gibt es für den Kredit nicht, seine Zahlungen kommen aus dem Tilgungsplan. Einmalposten lassen sich bei jeder Vertragsart eintragen.

## Siehe auch

- [Vertrag: Leasing](Vertrag-Leasing)
- [Vertrag: Sonstiges](Vertrag-Sonstiges)
- [Folgevertrag oder Verlängern](Folgevertrag-oder-Verlaengern)
- [Archiv und Historie](Archiv-und-Historie)
- [Sensoren-Referenz](Sensoren-Referenz)
