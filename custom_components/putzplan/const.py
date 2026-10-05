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
    ("Küche", "Kitchen", "Küchenboden wischen", "Mop kitchen floor", "mdi:mop", 2),
    ("Küche", "Kitchen", "Schranktürgriffe abwischen", "Wipe cabinet handles", "mdi:door", 7),
    ("Küche", "Kitchen", "Schwamm wechseln", "Change sponge", "mdi:sponge", 14),
    ("Küche", "Kitchen", "Mülleimer Küche reinigen", "Clean kitchen bin", "mdi:trash-can-outline", 14),
    ("Küche", "Kitchen", "Kühlschrank auswischen", "Clean fridge", "mdi:fridge-outline", 30),
    ("Küche", "Kitchen", "Spülmaschinen-Filter reinigen", "Clean dishwasher filter", "mdi:dishwasher", 30),
    ("Küche", "Kitchen", "Wasserkocher entkalken", "Descale kettle", "mdi:kettle", 30),
    ("Küche", "Kitchen", "Kaffeemaschine entkalken", "Descale coffee machine", "mdi:coffee-maker", 60),
    ("Küche", "Kitchen", "Dunstabzug: Fettfilter reinigen", "Clean hood grease filter", "mdi:range-hood", 60),
    ("Küche", "Kitchen", "Backofen reinigen", "Clean oven", "mdi:stove", 90),
    ("Küche", "Kitchen", "Spülmaschine tiefenreinigen", "Deep-clean dishwasher", "mdi:dishwasher", 90),
    ("Küche", "Kitchen", "Küchenschränke auswischen", "Wipe out kitchen cabinets", "mdi:cupboard-outline", 90),
    ("Küche", "Kitchen", "Papiermüll leeren", "Empty paper waste", "mdi:newspaper-variant-outline", 2),
    ("Küche", "Kitchen", "Biomüll leeren", "Empty organic waste", "mdi:food-apple-outline", 2),
    ("Küche", "Kitchen", "Plastikmüll leeren", "Empty plastic waste", "mdi:recycle", 2),
    ("Küche", "Kitchen", "Mikrowelle reinigen", "Clean microwave", "mdi:microwave", 14),
    ("Küche", "Kitchen", "Toaster: Krümelschublade leeren", "Toaster: empty crumb tray", "mdi:toaster", 14),
    ("Küche", "Kitchen", "Wasserfilter-Kartusche wechseln", "Change water filter cartridge", "mdi:water-check", 28),
    # Bad / Bathroom
    ("Bad", "Bathroom", "Toilette reinigen", "Clean toilet", "mdi:toilet", 3),
    ("Bad", "Bathroom", "Duschwand abziehen", "Squeegee shower", "mdi:shower-head", 2),
    ("Bad", "Bathroom", "Handtücher wechseln", "Change hand towels", "mdi:hand-wash-outline", 7),
    ("Bad", "Bathroom", "Badewanne/Dusche reinigen", "Clean bathtub/shower", "mdi:shower", 7),
    ("Bad", "Bathroom", "Waschbecken & Armaturen reinigen", "Clean basin & taps", "mdi:sink", 7),
    ("Bad", "Bathroom", "Spiegel reinigen", "Clean mirror", "mdi:mirror", 7),
    ("Bad", "Bathroom", "Badboden wischen", "Mop bathroom floor", "mdi:mop", 2),
    ("Bad", "Bathroom", "Waschmaschine: Gummidichtung auswischen", "Washer: wipe door seal", "mdi:washing-machine", 7),
    ("Bad", "Bathroom", "Badematte wechseln", "Change bath mat", "mdi:rug", 14),
    ("Bad", "Bathroom", "Abfluss reinigen", "Clean drain", "mdi:pipe", 30),
    ("Bad", "Bathroom", "Waschmaschine: Hygienewaschgang", "Washer: hygiene cycle", "mdi:washing-machine", 30),
    ("Bad", "Bathroom", "Waschmittelschublade reinigen", "Clean detergent drawer", "mdi:washing-machine", 30),
    ("Bad", "Bathroom", "Flusensieb reinigen", "Clean lint filter", "mdi:washing-machine", 90),
    ("Bad", "Bathroom", "Fugen & Silikon reinigen", "Clean grout & sealant", "mdi:wall", 90),
    ("Bad", "Bathroom", "Toilettenbürste reinigen", "Clean toilet brush", "mdi:toilet", 3),
    ("Bad", "Bathroom", "Mülleimer Bad leeren", "Empty bathroom bin", "mdi:trash-can-outline", 7),
    ("Bad", "Bathroom", "Duschkopf entkalken", "Descale shower head", "mdi:shower-head", 90),
    ("Bad", "Bathroom", "Perlatoren entkalken (Bad & Küche)", "Descale tap aerators", "mdi:faucet", 90),
    ("Bad", "Bathroom", "Toilettenbürste wechseln", "Replace toilet brush", "mdi:toilet", 180),
    # Wohnzimmer / Living room
    ("Wohnzimmer", "Living room", "Staubsaugen", "Vacuum", "mdi:robot-vacuum", 2),
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
    ("Schlafzimmer", "Bedroom", "Schlafzimmer saugen", "Vacuum bedroom", "mdi:robot-vacuum", 2),
    ("Schlafzimmer", "Bedroom", "Schlafzimmer wischen", "Mop bedroom", "mdi:mop", 14),
    ("Schlafzimmer", "Bedroom", "Schlafzimmer entstauben", "Dust bedroom", "mdi:spray-bottle", 14),
    ("Schlafzimmer", "Bedroom", "Fenster Schlafzimmer putzen", "Clean bedroom windows", "mdi:window-closed-variant", 90),
    ("Schlafzimmer", "Bedroom", "Matratze absaugen", "Vacuum mattress", "mdi:bed-empty", 180),
    ("Schlafzimmer", "Bedroom", "Kissen & Decken waschen", "Wash pillows & duvets", "mdi:bed-double-outline", 180),
    ("Schlafzimmer", "Bedroom", "Kleiderschrank auswischen", "Wipe out wardrobe", "mdi:wardrobe-outline", 365),
    # Kinderzimmer / Children's room (age: school children; see README for sources)
    ("Kinderzimmer", "Children's room", "Zimmer saugen", "Vacuum room", "mdi:robot-vacuum", 2),
    ("Kinderzimmer", "Children's room", "Bettwäsche wechseln", "Change bedding", "mdi:bed", 14),
    ("Kinderzimmer", "Children's room", "Boden wischen", "Mop floor", "mdi:mop", 14),
    ("Kinderzimmer", "Children's room", "Staub wischen", "Dust surfaces", "mdi:spray-bottle", 14),
    ("Kinderzimmer", "Children's room", "Schulranzen ausleeren & auswischen", "Empty & wipe school bag", "mdi:bag-personal-outline", 30),
    ("Kinderzimmer", "Children's room", "Kuscheltiere waschen", "Wash stuffed animals", "mdi:teddy-bear", 60),
    ("Kinderzimmer", "Children's room", "Fenster putzen", "Clean windows", "mdi:window-closed-variant", 90),
    ("Kinderzimmer", "Children's room", "Kissen & Decken waschen", "Wash pillows & duvets", "mdi:bed-double-outline", 90),
    ("Kinderzimmer", "Children's room", "Matratze absaugen", "Vacuum mattress", "mdi:bed-empty", 90),
    # Wintergarten / Conservatory
    ("Wintergarten", "Conservatory", "Boden saugen", "Vacuum floor", "mdi:robot-vacuum", 7),
    ("Wintergarten", "Conservatory", "Staub wischen", "Dust surfaces", "mdi:spray-bottle", 14),
    ("Wintergarten", "Conservatory", "Möbel abwischen", "Wipe furniture", "mdi:sofa", 30),
    ("Wintergarten", "Conservatory", "Glas innen & außen reinigen", "Clean glass inside & out", "mdi:window-closed-variant", 180),
    ("Wintergarten", "Conservatory", "Rahmen & Dichtungen reinigen", "Clean frames & seals", "mdi:window-frame", 365),
    # Balkon / Balcony
    ("Balkon", "Balcony", "Balkon fegen", "Sweep balcony", "mdi:broom", 14),
    ("Balkon", "Balcony", "Balkonmöbel & Geländer abwischen", "Wipe balcony furniture & railing", "mdi:table-furniture", 90),
    ("Balkon", "Balcony", "Balkontür-Schiene reinigen", "Clean balcony door track", "mdi:door-sliding", 90),
    ("Balkon", "Balcony", "Balkonboden gründlich reinigen", "Deep-clean balcony floor", "mdi:spray-bottle", 180),
    # Allgemein / General
    ("Allgemein", "General", "Türklinken & Lichtschalter abwischen", "Wipe door handles & switches", "mdi:light-switch", 3),
    ("Allgemein", "General", "Eingangsbereich saugen", "Vacuum entrance", "mdi:shoe-print", 2),
    ("Allgemein", "General", "Flur wischen", "Mop hallway", "mdi:mop", 7),
    ("Allgemein", "General", "Türen abwischen", "Wipe doors", "mdi:door", 90),
    ("Allgemein", "General", "Fußmatten waschen", "Wash door mats", "mdi:rug", 28),
    ("Allgemein", "General", "Fensterbänke abwischen", "Wipe window sills", "mdi:window-closed-variant", 30),
    ("Allgemein", "General", "Mülltonnen draußen reinigen", "Clean outdoor bins", "mdi:trash-can", 30),
    ("Allgemein", "General", "Schuhschrank & Garderobe auswischen", "Wipe shoe cabinet & wardrobe", "mdi:shoe-formal", 90),
    ("Allgemein", "General", "Fensterrahmen & Dichtungen reinigen", "Clean window frames & seals", "mdi:window-frame", 365),
    ("Allgemein", "General", "Fensterbeschläge ölen", "Oil window hinges", "mdi:oil", 365),
    ("Allgemein", "General", "Rauchmelder testen & entstauben", "Test & dust smoke detectors", "mdi:smoke-detector-variant", 365),
    ("Treppenhaus", "Stairwell", "Treppe saugen", "Vacuum stairs", "mdi:vacuum", 3),
    ("Treppenhaus", "Stairwell", "Treppe wischen", "Mop stairs", "mdi:mop", 7),
    ("Treppenhaus", "Stairwell", "Handlauf abwischen", "Wipe handrail", "mdi:stairs", 7),
    ("Treppenhaus", "Stairwell", "Geländer gründlich entfetten", "Degrease railing thoroughly", "mdi:spray-bottle", 30),
    ("Treppenhaus", "Stairwell", "Lichtschalter & Türklinken abwischen", "Wipe light switches & door handles", "mdi:light-switch", 7),
    ("Treppenhaus", "Stairwell", "Lampen abstauben", "Dust lamps", "mdi:lamp", 30),
    ("Treppenhaus", "Stairwell", "Fußmatte ausschütteln", "Shake out door mat", "mdi:rug", 7),
    ("Treppenhaus", "Stairwell", "Spinnweben entfernen", "Remove cobwebs", "mdi:spider-web", 14),
    ("Treppenhaus", "Stairwell", "Treppenhausfenster putzen", "Clean stairwell window", "mdi:window-closed-variant", 30),
    ("Treppenhaus", "Stairwell", "Fußleisten & Stufenkanten abwischen", "Wipe skirting & stair edges", "mdi:broom", 30),
]
