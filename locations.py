"""
Classes and functions related to AP locations for Metroid: Zero Mission
"""

from .items import AP_MZM_ID_BASE


class LocationData:
    region: str
    code: int

    def __init__(self, reg, id):
        self.region = reg
        self.code = id


# Location numbers/order and some names from Biospark's MZM Randomizer.
# Events in any region must be at the end of its table for the client to work correctly

brinstar_location_table = {
    "Brinstar Morph Ball": LocationData("Brinstar Start", AP_MZM_ID_BASE + 0),
    "Brinstar Morph Ball Cannon": LocationData("Brinstar Start", AP_MZM_ID_BASE + 1),
    "Brinstar Long Beam": LocationData("Brinstar Main", AP_MZM_ID_BASE + 2),
    "Brinstar Ceiling E-Tank": LocationData("Brinstar Start", AP_MZM_ID_BASE + 3),
    "Brinstar Main Shaft Left Alcove": LocationData("Brinstar Main", AP_MZM_ID_BASE + 4),
    "Brinstar Ballspark": LocationData("Brinstar Main", AP_MZM_ID_BASE + 5),
    "Brinstar Ripper Climb": LocationData("Brinstar Main", AP_MZM_ID_BASE + 6),
    "Brinstar Speed Booster Shortcut": LocationData("Brinstar Main", AP_MZM_ID_BASE + 7),
    "Brinstar Varia Suit": LocationData("Brinstar Top", AP_MZM_ID_BASE + 8),
    "Brinstar Worm Drop": LocationData("Brinstar Main", AP_MZM_ID_BASE + 9),
    "Brinstar Acid Near Varia": LocationData("Brinstar Top", AP_MZM_ID_BASE + 10),
    "Brinstar First Missile": LocationData("Brinstar Main", AP_MZM_ID_BASE + 11),
    "Brinstar Behind Hive": LocationData("Brinstar Main", AP_MZM_ID_BASE + 12),
    "Brinstar Under Bridge": LocationData("Brinstar Main", AP_MZM_ID_BASE + 13),
    "Brinstar Post-Hive in Wall": LocationData("Brinstar Past Hives", AP_MZM_ID_BASE + 14),
    "Brinstar Upper Pillar": LocationData("Brinstar Top", AP_MZM_ID_BASE + 15),
    "Brinstar Behind Bombs": LocationData("Brinstar Past Hives", AP_MZM_ID_BASE + 16),
    "Brinstar Bomb": LocationData("Brinstar Past Hives", AP_MZM_ID_BASE + 17),
    "Brinstar Post-Hive Pillar": LocationData("Brinstar Past Hives", AP_MZM_ID_BASE + 18)
}

kraid_location_table = {
    "Kraid Behind Giant Hoppers": LocationData("Kraid Left Shaft", AP_MZM_ID_BASE + 19),
    "Kraid Save Room Tunnel": LocationData("Kraid Main", AP_MZM_ID_BASE + 20),
    "Kraid Zipline Morph Jump": LocationData("Kraid Main", AP_MZM_ID_BASE + 21),
    "Kraid Quad Ball Cannon Room": LocationData("Kraid Left Shaft", AP_MZM_ID_BASE + 22),
    "Kraid Unknown Item Statue": LocationData("Kraid Left Shaft", AP_MZM_ID_BASE + 23),
    "Kraid Acid Ballspark": LocationData("Kraid Main", AP_MZM_ID_BASE + 24),
    "Kraid Speed Booster": LocationData("Kraid Bottom", AP_MZM_ID_BASE + 25),
    "Kraid Under Acid Worm": LocationData("Kraid Acid Worm Area", AP_MZM_ID_BASE + 26),
    "Kraid Right Hall Pillar": LocationData("Kraid Main", AP_MZM_ID_BASE + 27),
    "Kraid Acid Fall": LocationData("Kraid Bottom", AP_MZM_ID_BASE + 28),
    "Kraid Zipline Activator Room": LocationData("Kraid Acid Worm Area", AP_MZM_ID_BASE + 29),
    "Kraid Speed Jump": LocationData("Kraid Main", AP_MZM_ID_BASE + 30),
    "Kraid Upper Right Morph Ball Cannon": LocationData("Kraid Main", AP_MZM_ID_BASE + 31),
    "Kraid Zipline Activator": LocationData("Kraid Acid Worm Area", None),
    "Kraid": LocationData("Kraid Bottom", None)
}

norfair_location_table = {
    "Norfair Lava Dive Left": LocationData("Lower Norfair", AP_MZM_ID_BASE + 32),
    "Norfair Lava Dive Right": LocationData("Lower Norfair", AP_MZM_ID_BASE + 33),
    "Norfair Screw Attack": LocationData("Norfair Screw Attack Area", AP_MZM_ID_BASE + 34),
    "Norfair Next to Screw Attack": LocationData("Norfair Screw Attack Area", AP_MZM_ID_BASE + 35),
    "Norfair Hallway to Crateria": LocationData("Norfair Main", AP_MZM_ID_BASE + 36),
    "Norfair Under Crateria Elevator": LocationData("Norfair Main", AP_MZM_ID_BASE + 37),
    "Norfair Wave Beam": LocationData("Lower Norfair", AP_MZM_ID_BASE + 38),
    "Norfair Bomb Trap": LocationData("Norfair Under Brinstar Elevator", AP_MZM_ID_BASE + 39),
    "Norfair Heated Room Below Wave - Left": LocationData("Lower Norfair", AP_MZM_ID_BASE + 40),
    "Norfair Heated Room Below Wave - Right": LocationData("Lower Norfair", AP_MZM_ID_BASE + 41),
    "Norfair Heated Room Under Brinstar Elevator": LocationData("Norfair Under Brinstar Elevator", AP_MZM_ID_BASE + 42),
    "Norfair Behind Lower Super Missile Door - Left": LocationData("Norfair Behind Super Door", AP_MZM_ID_BASE + 43),
    "Norfair Behind Lower Super Missile Door - Right": LocationData("Norfair Behind Super Door", AP_MZM_ID_BASE + 44),
    "Norfair Ice Beam": LocationData("Norfair Upper Right Shaft", AP_MZM_ID_BASE + 45),
    "Norfair Heated Room Above Ice Beam": LocationData("Norfair Upper Right Shaft", AP_MZM_ID_BASE + 46),
    "Norfair Hi-Jump": LocationData("Norfair Lower Right Shaft", AP_MZM_ID_BASE + 47),
    "Norfair Big Room": LocationData("Norfair Right Shaft", AP_MZM_ID_BASE + 48),
    "Norfair Behind Top Chozo Statue": LocationData("Norfair Behind Ice Beam", AP_MZM_ID_BASE + 49),
    "Norfair Larva Ceiling": LocationData("Norfair Bottom", AP_MZM_ID_BASE + 50),
    "Norfair Right Shaft Near Hi-Jump": LocationData("Norfair Lower Right Shaft", AP_MZM_ID_BASE + 51),
    "Norfair Right Shaft Bottom": LocationData("Norfair Bottom", AP_MZM_ID_BASE + 52)
}

ridley_location_table = {
    "Ridley Southwest Puzzle Top": LocationData("Ridley SW Puzzle", AP_MZM_ID_BASE + 53),
    "Ridley Southwest Puzzle Bottom": LocationData("Ridley SW Puzzle", AP_MZM_ID_BASE + 54),
    "Ridley West Pillar": LocationData("Ridley Left Shaft", AP_MZM_ID_BASE + 55),
    "Ridley Behind Unknown Statue": LocationData("Ridley Room", AP_MZM_ID_BASE + 56),
    "Ridley Unknown Item Statue": LocationData("Ridley Room", AP_MZM_ID_BASE + 57),
    "Ridley Fake Floor": LocationData("Ridley Left Shaft", AP_MZM_ID_BASE + 58),
    "Ridley Upper Ball Cannon Puzzle": LocationData("Central Ridley", AP_MZM_ID_BASE + 59),
    "Ridley Lower Ball Cannon Puzzle": LocationData("Central Ridley", AP_MZM_ID_BASE + 60),
    "Ridley Imago Super Missile": LocationData("Ridley Main", AP_MZM_ID_BASE + 61),
    "Ridley After Sidehopper Hall Upper": LocationData("Central Ridley", AP_MZM_ID_BASE + 62),
    "Ridley After Sidehopper Hall Lower": LocationData("Central Ridley", AP_MZM_ID_BASE + 63),
    "Ridley Long Hall": LocationData("Ridley Right Shaft", AP_MZM_ID_BASE + 64),
    "Ridley Center Pillar": LocationData("Central Ridley", AP_MZM_ID_BASE + 65),
    "Ridley Ball Room Lower": LocationData("Central Ridley", AP_MZM_ID_BASE + 66),
    "Ridley Ball Room Upper": LocationData("Central Ridley", AP_MZM_ID_BASE + 67),
    "Ridley Fake Lava Under Floor": LocationData("Ridley Right Shaft", AP_MZM_ID_BASE + 68),
    "Ridley Under Owls": LocationData("Central Ridley", AP_MZM_ID_BASE + 69),
    "Ridley Northeast Corner": LocationData("Ridley Right Shaft", AP_MZM_ID_BASE + 70),
    "Ridley Bomb Puzzle": LocationData("Ridley Speed Puzzles", AP_MZM_ID_BASE + 71),
    "Ridley Speed Jump": LocationData("Ridley Speed Puzzles", AP_MZM_ID_BASE + 72),
    "Ridley": LocationData("Ridley Room", None)
}

tourian_location_table = {
    "Tourian Left of Mother Brain": LocationData("Tourian", AP_MZM_ID_BASE + 73),
    "Tourian Under Mother Brain": LocationData("Tourian", AP_MZM_ID_BASE + 74),
    "Mother Brain": LocationData("Tourian", None)
}

crateria_location_table = {
    "Crateria Landing Site Ballspark": LocationData("Crateria", AP_MZM_ID_BASE + 75),
    "Crateria Power Grip": LocationData("Upper Crateria", AP_MZM_ID_BASE + 76),
    "Crateria Moat": LocationData("Crateria", AP_MZM_ID_BASE + 77),
    "Crateria Statue Water": LocationData("Upper Crateria", AP_MZM_ID_BASE + 78),
    "Crateria Unknown Item Statue": LocationData("Upper Crateria", AP_MZM_ID_BASE + 79),
    "Crateria East Ballspark": LocationData("Upper Crateria", AP_MZM_ID_BASE + 80),
    "Crateria Northeast Corner": LocationData("Upper Crateria", AP_MZM_ID_BASE + 81)
}

chozodia_location_table = {
    "Chozodia Upper Crateria Door": LocationData("Chozodia Ruins", AP_MZM_ID_BASE + 82),
    "Chozodia Bomb Maze": LocationData("Chozodia Under Tube", AP_MZM_ID_BASE + 83),
    "Chozodia Zoomer Maze": LocationData("Chozodia Under Tube", AP_MZM_ID_BASE + 84),
    "Chozodia Ruins East of Upper Crateria Door": LocationData("Chozodia Ruins", AP_MZM_ID_BASE + 85),
    "Chozodia Chozo Ghost Area Morph Tunnel Above Water": LocationData("Chozodia Ruins Test Area", AP_MZM_ID_BASE + 86),
    "Chozodia Chozo Ghost Area Underwater": LocationData("Chozodia Ruins Test Area", AP_MZM_ID_BASE + 87),
    "Chozodia Triple Crawling Pirates": LocationData("Chozodia Ruins", AP_MZM_ID_BASE + 88),
    "Chozodia Left of Glass Tube": LocationData("Chozodia Under Tube", AP_MZM_ID_BASE + 89),
    "Chozodia Lava Dive": LocationData("Chozodia Ruins Test Area", AP_MZM_ID_BASE + 90),
    "Chozodia Original Power Bomb": LocationData("Chozodia Original Power Bomb Room", AP_MZM_ID_BASE + 91),
    "Chozodia Next to Original Power Bomb": LocationData("Chozodia Original Power Bomb Room", AP_MZM_ID_BASE + 92),
    "Chozodia Right of Glass Tube": LocationData("Chozodia Under Tube", AP_MZM_ID_BASE + 93),
    "Chozodia Chozo Ghost Area Long Shinespark": LocationData("Chozodia Ruins Test Area", AP_MZM_ID_BASE + 94),
    "Chozodia Pirate Pitfall Trap": LocationData("Chozodia Mothership Upper", AP_MZM_ID_BASE + 95),
    "Chozodia Behind Workbot": LocationData("Chozodia Mothership Upper", AP_MZM_ID_BASE + 96),
    "Chozodia Ceiling Near Map Station": LocationData("Chozodia Mothership Lower", AP_MZM_ID_BASE + 97),
    "Chozodia Under Mecha Ridley Hallway": LocationData("Chozodia Mecha Ridley Hallway", AP_MZM_ID_BASE + 98),
    "Chozodia Southeast Corner in Hull": LocationData("Chozodia Mothership Lower", AP_MZM_ID_BASE + 99),
    "Chozo Ghost": LocationData("Chozodia Ruins Test Area", None),
    "Mecha Ridley": LocationData("Chozodia Mecha Ridley Hallway", None),
    "Chozodia Space Pirate's Ship": LocationData("Chozodia Mecha Ridley Hallway", None)
}

full_location_table = {
    **brinstar_location_table,
    **kraid_location_table,
    **norfair_location_table,
    **ridley_location_table,
    **tourian_location_table,
    **crateria_location_table,
    **chozodia_location_table
}

mzm_location_name_groups = {
    "Brinstar": {name for name, id in brinstar_location_table.items() if id.code is not None},
    "Kraid": {name for name, id in kraid_location_table.items() if id.code is not None},
    "Upper Norfair": {
        "Norfair Hallway to Crateria",
        "Norfair Under Crateria Elevator",
        "Norfair Bomb Trap",
        "Norfair Heated Room Under Brinstar Elevator",
        "Norfair Ice Beam",
        "Norfair Heated Room Above Ice Beam",
        "Norfair Hi-Jump",
        "Norfair Big Room",
        "Norfair Behind Top Chozo Statue",
        "Norfair Right Shaft Near Hi-Jump",
    },
    "Lower Norfair": {
        "Norfair Lava Dive Left",
        "Norfair Lava Dive Right",
        "Norfair Screw Attack",
        "Norfair Next to Screw Attack",
        "Norfair Wave Beam",
        "Norfair Heated Room Below Wave - Right",
        "Norfair Heated Room Below Wave - Left",
        "Norfair Behind Lower Super Missile Door - Right",
        "Norfair Behind Lower Super Missile Door - Left",
        "Norfair Larva Ceiling",
        "Norfair Right Shaft Bottom",
    },
    "Ridley": {name for name, id in ridley_location_table.items() if id.code is not None},
    "Tourian": {name for name, id in tourian_location_table.items() if id.code is not None},
    "Crateria": {name for name, id in crateria_location_table.items() if id.code is not None},
    "Chozo Ruins": {
        "Chozodia Upper Crateria Door",
        "Chozodia Ruins East of Upper Crateria Door",
        "Chozodia Chozo Ghost Area Morph Tunnel Above Water",
        "Chozodia Chozo Ghost Area Underwater",
        "Chozodia Triple Crawling Pirates",
        "Chozodia Lava Dive",
    },
    "Mother Ship": {
        "Chozodia Bomb Maze",
        "Chozodia Zoomer Maze",
        "Chozodia Left of Glass Tube",
        "Chozodia Original Power Bomb",
        "Chozodia Next to Original Power Bomb",
        "Chozodia Right of Glass Tube",
        "Chozodia Chozo Ghost Area Long Shinespark",
        "Chozodia Pirate Pitfall Trap",
        "Chozodia Behind Workbot",
        "Chozodia Ceiling Near Map Station",
        "Chozodia Under Mecha Ridley Hallway",
        "Chozodia Southeast Corner in Hull",
    },
    "Chozo Statues": {
        "Brinstar Long Beam",
        "Brinstar Varia Suit",
        "Brinstar Bomb",
        "Kraid Unknown Item Statue",
        "Kraid Speed Booster",
        "Norfair Screw Attack",
        "Norfair Wave Beam",
        "Norfair Ice Beam",
        "Norfair Hi-Jump",
        "Ridley Unknown Item Statue",
        "Crateria Unknown Item Statue",
    },
    "Freestanding Items": {
        "Brinstar Morph Ball",
        "Brinstar Worm Drop",
        "Crateria Power Grip",
    },
    "Energy Tanks": {
        "Brinstar Ceiling E-Tank",
        "Brinstar Post-Hive Pillar",
        "Brinstar Acid Near Varia",
        "Kraid Zipline Activator Room",
        "Kraid Speed Jump",
        "Norfair Larva Ceiling",
        "Ridley Behind Unknown Statue",
        "Ridley Fake Floor",
        "Ridley Under Owls",
        "Chozodia Left of Glass Tube",
        "Chozodia Chozo Ghost Area Long Shinespark",
        "Chozodia Under Mecha Ridley Hallway",
    },
}
