# Putzplan für Home Assistant

Wiederkehrende Putz- und Haushaltsaufgaben, gruppiert nach Räumen – mit Intervall, „zuletzt erledigt“, **ERLEDIGT**-/**ÜBERFÄLLIG**-Markierung und einer fertigen Dashboard-Karte.

## Was du bekommst

- Pro Aufgabe ein Sensor (`sensor.putzplan_...`) mit Status `ok`, `due_soon`, `overdue`, `as_needed` (bei Bedarf) oder `unknown` (noch nie erledigt)
- `sensor.putzplan_overdue`: Anzahl überfälliger Aufgaben (ideal für Benachrichtigungen)
- Die Karte `custom:putzplan-card` (wird automatisch geladen, keine Ressource nötig)
- Services zum Erledigen, Rückgängigmachen, Anlegen, Ändern und Löschen
- Beim Einrichten optional 22 Beispielaufgaben (Küche, Bad, Wohnzimmer, Schlafzimmer, Allgemein)

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
