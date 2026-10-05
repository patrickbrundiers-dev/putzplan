"""Constants for the Putzplan integration."""

from __future__ import annotations

DOMAIN = "putzplan"
VERSION = "1.0.0"

STORAGE_KEY = "putzplan.tasks"
STORAGE_VERSION = 1

SIGNAL_UPDATED = "putzplan_updated"

FRONTEND_URL_BASE = "/putzplan_static"
FRONTEND_CARD_FILE = "putzplan-card.js"

CONF_SEED = "seed"

DEFAULT_ICON = "mdi:broom"
DUE_SOON_DAYS = 3

STATUS_OK = "ok"
STATUS_DUE_SOON = "due_soon"
STATUS_OVERDUE = "overdue"
STATUS_AS_NEEDED = "as_needed"
STATUS_UNKNOWN = "unknown"

# (room_de, room_en, name_de, name_en, icon, interval_days or None = as needed)
DEFAULT_TASKS: list[tuple[str, str, str, str, str, int | None]] = [
    ("Küche", "Kitchen", "Spüle reinigen", "Clean sink", "mdi:faucet", 30),
    ("Küche", "Kitchen", "Arbeitsplatte reinigen", "Clean counter", "mdi:countertop", None),
    ("Küche", "Kitchen", "Herd reinigen", "Clean stove", "mdi:stove", 30),
    ("Küche", "Kitchen", "Griffe abwischen", "Wipe handles", "mdi:door", 30),
    ("Küche", "Kitchen", "Dunstabzugshaube reinigen", "Clean exhaust hood", "mdi:range-hood", 120),
    ("Küche", "Kitchen", "Schwamm wechseln", "Change sponge", "mdi:sponge", 45),
    ("Küche", "Kitchen", "Kühlschrank auswischen", "Clean fridge", "mdi:fridge-outline", 60),
    ("Küche", "Kitchen", "Spülmaschinen-Filter reinigen", "Clean dishwasher filter", "mdi:dishwasher", 30),
    ("Bad", "Bathroom", "Boden wischen", "Mop floor", "mdi:mop", 14),
    ("Bad", "Bathroom", "Badewanne/Dusche reinigen", "Clean bathtub/shower", "mdi:shower", 30),
    ("Bad", "Bathroom", "Toilette reinigen", "Clean toilet", "mdi:toilet", 14),
    ("Bad", "Bathroom", "Handtücher wechseln", "Change hand towels", "mdi:hand-wash-outline", 7),
    ("Bad", "Bathroom", "Badematte wechseln", "Change bath mat", "mdi:rug", 14),
    ("Bad", "Bathroom", "Waschmaschine reinigen", "Clean washing machine", "mdi:washing-machine", 60),
    ("Wohnzimmer", "Living room", "Staubsaugen", "Vacuum", "mdi:robot-vacuum", 7),
    ("Wohnzimmer", "Living room", "Staub wischen", "Dust surfaces", "mdi:spray-bottle", 14),
    ("Wohnzimmer", "Living room", "Fenster putzen", "Clean windows", "mdi:window-closed-variant", 90),
    ("Schlafzimmer", "Bedroom", "Bettwäsche wechseln", "Change bedding", "mdi:bed", 14),
    ("Schlafzimmer", "Bedroom", "Staubsaugen", "Vacuum", "mdi:robot-vacuum", 7),
    ("Schlafzimmer", "Bedroom", "Matratze absaugen", "Vacuum mattress", "mdi:bed-empty", 90),
    ("Allgemein", "General", "Staubsaugerfilter reinigen", "Clean vacuum filter", "mdi:air-filter", 60),
    ("Allgemein", "General", "Kaffeemaschine entkalken", "Descale coffee machine", "mdi:coffee-maker", 60),
]
