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
# Intervals follow common German cleaning guides (e.g. selbermachen.de, wohnglueck.de,
# alltagsfuchs.de) and manufacturer advice (Finish, Bauknecht) for appliance care.
DEFAULT_TASKS: list[tuple[str, str, str, str, str, int | None]] = [
    # Küche / Kitchen
    ("Küche", "Kitchen", "Arbeitsplatte abwischen", "Wipe counter", "mdi:countertop", 1),
    ("Küche", "Kitchen", "Spüle & Armatur reinigen", "Clean sink & tap", "mdi:faucet", 3),
    ("Küche", "Kitchen", "Küchentücher & Spüllappen wechseln", "Change dish towels & cloths", "mdi:hand-wash-outline", 3),
    ("Küche", "Kitchen", "Herd & Kochfeld reinigen", "Clean stove & hob", "mdi:stove", 7),
    ("Küche", "Kitchen", "Küchenboden wischen", "Mop kitchen floor", "mdi:mop", 7),
    ("Küche", "Kitchen", "Schranktürgriffe abwischen", "Wipe cabinet handles", "mdi:door", 7),
    ("Küche", "Kitchen", "Schwamm wechseln", "Change sponge", "mdi:sponge", 14),
    ("Küche", "Kitchen", "Mülleimer Küche reinigen", "Clean kitchen bin", "mdi:trash-can-outline", 30),
    ("Küche", "Kitchen", "Kühlschrank auswischen", "Clean fridge", "mdi:fridge-outline", 30),
    ("Küche", "Kitchen", "Spülmaschinen-Filter reinigen", "Clean dishwasher filter", "mdi:dishwasher", 30),
    ("Küche", "Kitchen", "Wasserkocher entkalken", "Descale kettle", "mdi:kettle", 30),
    ("Küche", "Kitchen", "Kaffeemaschine entkalken", "Descale coffee machine", "mdi:coffee-maker", 60),
    ("Küche", "Kitchen", "Dunstabzug: Fettfilter reinigen", "Clean hood grease filter", "mdi:range-hood", 60),
    ("Küche", "Kitchen", "Backofen reinigen", "Clean oven", "mdi:stove", 90),
    ("Küche", "Kitchen", "Spülmaschine tiefenreinigen", "Deep-clean dishwasher", "mdi:dishwasher", 90),
    ("Küche", "Kitchen", "Küchenschränke auswischen", "Wipe out kitchen cabinets", "mdi:cupboard-outline", 90),
    ("Küche", "Kitchen", "Gefrierschrank abtauen", "Defrost freezer", "mdi:snowflake", 365),
    # Bad / Bathroom
    ("Bad", "Bathroom", "Toilette reinigen", "Clean toilet", "mdi:toilet", 3),
    ("Bad", "Bathroom", "Duschwand abziehen", "Squeegee shower", "mdi:shower-head", 2),
    ("Bad", "Bathroom", "Handtücher wechseln", "Change hand towels", "mdi:hand-wash-outline", 7),
    ("Bad", "Bathroom", "Badewanne/Dusche reinigen", "Clean bathtub/shower", "mdi:shower", 7),
    ("Bad", "Bathroom", "Waschbecken & Armaturen reinigen", "Clean basin & taps", "mdi:sink", 7),
    ("Bad", "Bathroom", "Spiegel reinigen", "Clean mirror", "mdi:mirror", 7),
    ("Bad", "Bathroom", "Badboden wischen", "Mop bathroom floor", "mdi:mop", 7),
    ("Bad", "Bathroom", "Waschmaschine: Gummidichtung auswischen", "Washer: wipe door seal", "mdi:washing-machine", 7),
    ("Bad", "Bathroom", "Badematte wechseln", "Change bath mat", "mdi:rug", 14),
    ("Bad", "Bathroom", "Abfluss reinigen", "Clean drain", "mdi:pipe", 30),
    ("Bad", "Bathroom", "Waschmaschine: Hygienewaschgang", "Washer: hygiene cycle", "mdi:washing-machine", 30),
    ("Bad", "Bathroom", "Waschmittelschublade reinigen", "Clean detergent drawer", "mdi:washing-machine", 30),
    ("Bad", "Bathroom", "Flusensieb reinigen", "Clean lint filter", "mdi:washing-machine", 90),
    ("Bad", "Bathroom", "Duschvorhang waschen", "Wash shower curtain", "mdi:curtains", 90),
    ("Bad", "Bathroom", "Fugen & Silikon reinigen", "Clean grout & sealant", "mdi:wall", 90),
    # Wohnzimmer / Living room
    ("Wohnzimmer", "Living room", "Staubsaugen", "Vacuum", "mdi:robot-vacuum", 3),
    ("Wohnzimmer", "Living room", "Boden wischen", "Mop floor", "mdi:mop", 7),
    ("Wohnzimmer", "Living room", "Staub wischen", "Dust surfaces", "mdi:spray-bottle", 7),
    ("Wohnzimmer", "Living room", "Polstermöbel absaugen", "Vacuum upholstery", "mdi:sofa", 30),
    ("Wohnzimmer", "Living room", "Teppich gründlich saugen", "Deep-vacuum rug", "mdi:rug", 30),
    ("Wohnzimmer", "Living room", "Fenster putzen", "Clean windows", "mdi:window-closed-variant", 90),
    ("Wohnzimmer", "Living room", "Heizkörper reinigen", "Clean radiators", "mdi:radiator", 90),
    ("Wohnzimmer", "Living room", "Sofakissen waschen", "Wash sofa cushions", "mdi:sofa", 90),
    ("Wohnzimmer", "Living room", "Schrankoberseiten abstauben", "Dust top of cabinets", "mdi:spray-bottle", 90),
    ("Wohnzimmer", "Living room", "Gardinen & Vorhänge waschen", "Wash curtains", "mdi:curtains", 365),
    # Schlafzimmer / Bedroom
    ("Schlafzimmer", "Bedroom", "Bettwäsche wechseln", "Change bedding", "mdi:bed", 14),
    ("Schlafzimmer", "Bedroom", "Schlafzimmer saugen", "Vacuum bedroom", "mdi:robot-vacuum", 7),
    ("Schlafzimmer", "Bedroom", "Schlafzimmer wischen", "Mop bedroom", "mdi:mop", 14),
    ("Schlafzimmer", "Bedroom", "Schlafzimmer entstauben", "Dust bedroom", "mdi:spray-bottle", 14),
    ("Schlafzimmer", "Bedroom", "Fenster Schlafzimmer putzen", "Clean bedroom windows", "mdi:window-closed-variant", 90),
    ("Schlafzimmer", "Bedroom", "Matratze absaugen", "Vacuum mattress", "mdi:bed-empty", 180),
    ("Schlafzimmer", "Bedroom", "Kissen & Decken waschen", "Wash pillows & duvets", "mdi:bed-double-outline", 180),
    ("Schlafzimmer", "Bedroom", "Kleiderschrank auswischen", "Wipe out wardrobe", "mdi:wardrobe-outline", 365),
    # Allgemein / General
    ("Allgemein", "General", "Türklinken & Lichtschalter abwischen", "Wipe door handles & switches", "mdi:light-switch", 3),
    ("Allgemein", "General", "Eingangsbereich saugen", "Vacuum entrance", "mdi:shoe-print", 3),
    ("Allgemein", "General", "Flur wischen", "Mop hallway", "mdi:mop", 7),
    ("Allgemein", "General", "Staubsaugerfilter reinigen", "Clean vacuum filter", "mdi:air-filter", 30),
    ("Allgemein", "General", "Türen abwischen", "Wipe doors", "mdi:door", 90),
]
