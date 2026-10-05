# Putzplan für Home Assistant

Wiederkehrende Putz- und Haushaltsaufgaben, gruppiert nach Räumen – mit Intervall, „zuletzt erledigt“, **ERLEDIGT**-/**ÜBERFÄLLIG**-Markierung und einer fertigen Dashboard-Karte.

## Was du bekommst

- Pro Aufgabe ein Sensor (`sensor.putzplan_...`) mit Status `ok`, `due_soon`, `overdue`, `as_needed` (bei Bedarf) oder `unknown` (noch nie erledigt)
- `sensor.putzplan_overdue`: Anzahl überfälliger Aufgaben (ideal für Benachrichtigungen)
- Die Karte `custom:putzplan-card` (wird automatisch geladen, keine Ressource nötig)
- Services zum Erledigen, Rückgängigmachen, Anlegen, Ändern und Löschen
- Beim Einrichten optional 98 Beispielaufgaben mit realistischen Intervallen (Küche, Bad, Wohnzimmer, Schlafzimmer, Kinderzimmer, Wintergarten, Balkon, Treppenhaus, Allgemein), z. B. Toilette alle 3 Tage, Bad wöchentlich, Backofen alle 3 Monate

## Installation (HACS)

1. HACS → Integrationen → ⋮ → **Benutzerdefinierte Repositories** → `https://github.com/patrickbrundiers-dev/putzplan`, Kategorie **Integration**
2. „Putzplan“ installieren, Home Assistant neu starten
3. Einstellungen → Geräte & Dienste → **Integration hinzufügen** → *Putzplan*

## Karte

```yaml
type: custom:putzplan-card
title: Putzplan        # optional
columns: 2             # optional, Standard 1
rooms:                 # optional: Reihenfolge und Filter
  - Küche
  - Bad
```

Antippen einer Aufgabe öffnet die Buttons **Heute erledigt**, **Gestern** und **Rückgängig**.

## Aufgaben verwalten

Entwicklerwerkzeuge → Aktionen (oder in Automationen/Skripten):

```yaml
action: putzplan.add_task
data:
  name: Fenster putzen
  room: Wohnzimmer
  icon: mdi:window-closed-variant
  interval_days: 90      # 0 oder weglassen = bei Bedarf
```

| Aktion | Zweck |
| --- | --- |
| `putzplan.mark_done` | `entity_id`, optional `date` (Standard heute) |
| `putzplan.undo_done` | stellt das vorherige Datum wieder her |
| `putzplan.add_task` | `name`, `room`, optional `icon`, `interval_days`, `last_done` |
| `putzplan.update_task` | `entity_id` plus beliebige Felder ändern |
| `putzplan.remove_task` | löscht Aufgabe und Sensor |

## Beispiel: tägliche Erinnerung

```yaml
automation:
  - alias: Putzplan Erinnerung
    triggers:
      - trigger: time
        at: "09:00:00"
    conditions:
      - condition: numeric_state
        entity_id: sensor.putzplan_overdue
        above: 0
    actions:
      - action: notify.notify
        data:
          title: Putzplan
          message: "{{ state_attr('sensor.putzplan_overdue', 'overdue_tasks') | join(', ') }}"
```

## Status-Regeln

- **Überfällig**: letzte Erledigung + Intervall liegt in der Vergangenheit
- **Bald**: fällig innerhalb von 3 Tagen
- **Bei Bedarf** (kein Intervall) und **unbekannt** (noch nie erledigt) werden nie als überfällig markiert

## Woher kommen die Intervalle?

Die Beispielwerte orientieren sich an gängigen Putzplänen ([selbermachen.de](https://selbermachen.de/wohnen/putzplan-wie-oft-sie-was-sauber-machen-sollten), [wohnglueck.de](https://wohnglueck.de/artikel/putzplan-zuhause-sauber-machen-wie-oft-41926), [alltagsfuchs.de](https://alltagsfuchs.de/haushalt/reinigung-ordnung/wie-oft-muss-man-was-putzen-was-ist-wirklich-realistisch/)) und an Herstellerangaben zur Gerätepflege ([Finish](https://www.finish.de/geschirrspuel-leitfaden/wartung-pflege/spuelmaschinenfilter/), [Bauknecht](https://www.bauknecht.de/magazin/waschen-trocknen/pflege-wartung/waschmaschine-reinigen), [BRITA](https://www.brita.de/wasser-wissen/wasserfilter-wechseln)), Rauchmelder-Wartung nach DIN 14676 ([rauchmelder-shop.de](https://www.rauchmelder-shop.de/rauchmelderpflicht/rauchmelder-testen-haeufigkeit-und-anleitung/)) sowie Ratgebern zu [Klobürste](https://utopia.de/ratgeber/klobuerste-wechseln-so-oft-solltest-du-es-tun_657931/), [Mülleimern](https://utopia.de/ratgeber/muelleimer-reinigen-wie-oft-und-mit-welchen-haus-mitteln_534796/) und [Fensterpflege](https://www.aroundhome.de/fenster/pflege-wartung/). Für Kinderzimmer: [Kinderbettwäsche](https://smartwood.de/blog/wie-oft-sollte-man-kinderbettwaesche-wechseln-ein-praxis-guide-fuer-eltern.html), [Milbenprävention (AAK)](https://www.aak.de/allergie-bei-kindern/welche-ausloeser-gibt-es/hausstaubmilben/sanierung-des-schlafbereiches/) und [Schulranzen-Pflege](https://ranzenkontor.de/blog/schulranzen-reinigen/); für Wintergarten und Balkon: [Leifheit](https://www.leifheit.de/de-de/ratgeber/reinigung/wintergarten-reinigen) und [Wohnglück](https://wohnglueck.de/artikel/balkon-und-terrasse-reinigen-37634); für das Treppenhaus: [GR Ferma](https://gr-ferma.de/aktuelles/reinigungsplan-treppenhaus/), [Immobilienwerk](https://www.immobilienwerk.net/wie-oft-sollten-treppenhaeuser-gereinigt-werden-eine-faustregel-fuer-hausverwalter/) und [Hausjournal](https://www.hausjournal.net/treppenhaus-reinigen). Wo Quellen keine Zahl nennen, sind die Werte Schätzungen. Es sind Richtwerte – passe sie über `putzplan.update_task` an deinen Haushalt an.
