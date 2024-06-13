"""
Classes and functions related to AP locations for Metroid: Zero Mission
"""
from BaseClasses import Location
from .items import AP_MZM_ID_BASE


class MZMLocation(Location):
    game: str = "Metroid Zero Mission"


# room numbers lifted from Biospark's MZM Randomizer don't blame me
# probably need to add more to this i.e. room #, clipdata addr and bg1data addr from mzmr

# Events in any region must be at the end of its table for the client to work correctly

brinstar_location_table = {
    "Brinstar Morph Ball": AP_MZM_ID_BASE + 0,
    "Brinstar Morph Ball Cannon": AP_MZM_ID_BASE + 1,
    "Brinstar Long Beam": AP_MZM_ID_BASE + 2,
    "Brinstar Ceiling E-Tank": AP_MZM_ID_BASE + 3,
    "Brinstar Missile Above Super": AP_MZM_ID_BASE + 4,
    "Brinstar Super Missile": AP_MZM_ID_BASE + 5,
    "Brinstar Top Missile": AP_MZM_ID_BASE + 6,
    "Brinstar Speed Booster Shortcut Missile": AP_MZM_ID_BASE + 7,
    "Brinstar Varia Suit": AP_MZM_ID_BASE + 8,
    "Brinstar Worm drop": AP_MZM_ID_BASE + 9,
    "Brinstar Varia E-Tank": AP_MZM_ID_BASE + 10,
    "Brinstar First Missile": AP_MZM_ID_BASE + 11,
    "Brinstar Hive Missile": AP_MZM_ID_BASE + 12,
    "Brinstar Under Bridge": AP_MZM_ID_BASE + 13,
    "Brinstar Post-Hive Missile": AP_MZM_ID_BASE + 14,
    "Brinstar Upper Pillar Missile": AP_MZM_ID_BASE + 15,
    "Brinstar Missile Behind Bombs": AP_MZM_ID_BASE + 16,
    "Brinstar Bomb": AP_MZM_ID_BASE + 17,
    "Brinstar Post-Hive E-Tank": AP_MZM_ID_BASE + 18,
}

kraid_location_table = {
    "Kraid Giant Hoppers Room Missile": AP_MZM_ID_BASE + 19,
    "Kraid Save Room Missile": AP_MZM_ID_BASE + 20,
    "Kraid Crumble Block Missile": AP_MZM_ID_BASE + 21,
    "Kraid Boring Room": AP_MZM_ID_BASE + 22,  #TODO: rename this one
    "Kraid Space Jump/Unknown Item 2": AP_MZM_ID_BASE + 23,
    "Kraid Lava Missile": AP_MZM_ID_BASE + 24,
    "Kraid Speed Booster": AP_MZM_ID_BASE + 25,
    "Kraid Worm Missile": AP_MZM_ID_BASE + 26,
    "Kraid Pillar Missile": AP_MZM_ID_BASE + 27,
    "Kraid Lava Fall": AP_MZM_ID_BASE + 28,
    "Kraid Worm E-Tank": AP_MZM_ID_BASE + 29,
    "Kraid Speed Jump": AP_MZM_ID_BASE + 30,
    "Kraid Ball Cannon": AP_MZM_ID_BASE + 31
}

norfair_location_table = {
    "Norfair Power Bomb": AP_MZM_ID_BASE + 32,
    "Norfair Lava Missile": AP_MZM_ID_BASE + 33,
    "Norfair Screw Attack": AP_MZM_ID_BASE + 34,
    "Norfair Screw Attack Missile": AP_MZM_ID_BASE + 35,
    "Norfair Power Grip Missile": AP_MZM_ID_BASE + 36,
    "Norfair Under Elevator": AP_MZM_ID_BASE + 37,
    "Norfair Wave Beam": AP_MZM_ID_BASE + 38,
    "Norfair Bomb Super Missile": AP_MZM_ID_BASE + 39,
    "Norfair Bottom Heated First": AP_MZM_ID_BASE + 40,  #TODO: rename this one
    "Norfair Bottom Heated Second": AP_MZM_ID_BASE + 41,  #TODO and also this one
    "Norfair Heated Room hidden Missile": AP_MZM_ID_BASE + 42,
    "Norfair Space Boost Missile": AP_MZM_ID_BASE + 43,  # TODO probably need to rename
    "Norfair Space Boost Super Missile": AP_MZM_ID_BASE + 44,  # TODO and this one
    "Norfair Ice Beam": AP_MZM_ID_BASE + 45,
    "Norfair Heated Room under Ice Beam": AP_MZM_ID_BASE + 46,
    "Norfair Hi-Jump": AP_MZM_ID_BASE + 47,
    "Norfair Big Room": AP_MZM_ID_BASE + 48,
    "Norfair Behind Top Chozo Statue": AP_MZM_ID_BASE + 49,
    "Norfair Larva E-tank": AP_MZM_ID_BASE + 50,
    "Norfair Main Shaft Ball Cannon": AP_MZM_ID_BASE + 51,
    "Norfair Main Shaft Bottom": AP_MZM_ID_BASE + 52
}

ridley_location_table = {
    "Ridley SW Puzzle Top": AP_MZM_ID_BASE + 53,  # TODO: maybe rename
    "Ridley SW Puzzle Bottom": AP_MZM_ID_BASE + 54,
    "Ridley West Pillar": AP_MZM_ID_BASE + 55, # req hijump or grip
    "Ridley E-Tank behind Gravity": AP_MZM_ID_BASE + 56,
    "Ridley Gravity Suit/Unknown Item 3": AP_MZM_ID_BASE + 57,
    "Ridley Fake Floor E-Tank": AP_MZM_ID_BASE + 58,
    "Ridley Upper Ball Cannon": AP_MZM_ID_BASE + 59,
    "Ridley Lower Ball Cannon": AP_MZM_ID_BASE + 60,
    "Ridley Imago Super Missile": AP_MZM_ID_BASE + 61,
    "Ridley Missile Above Sidehoppers": AP_MZM_ID_BASE + 62,
    "Ridley Sidehopper Super": AP_MZM_ID_BASE + 63,
    "Ridley Long Hall": AP_MZM_ID_BASE + 64,
    "Ridley Pillar Missile": AP_MZM_ID_BASE + 65,
    "Ridley Ball Missile": AP_MZM_ID_BASE + 66,  # TODO rename?
    "Ridley Ball Super": AP_MZM_ID_BASE + 67,  # TODO rename?
    "Ridley Sidehopper Missile": AP_MZM_ID_BASE + 68,  #TODO rename?
    "Ridley Owl E-Tank": AP_MZM_ID_BASE + 69,
    "Ridley Upper Right corner Missile": AP_MZM_ID_BASE + 70,  # MZMR calls it jumpy jumpy
    "Ridley Bomb Puzzle": AP_MZM_ID_BASE + 71,
    "Ridley Speed Jump": AP_MZM_ID_BASE + 72
}

tourian_location_table = {
    "Tourian Left of Mother Brain": AP_MZM_ID_BASE + 73,
    "Tourian Under Mother Brain ": AP_MZM_ID_BASE + 74
}

crateria_location_table = {
    "Crateria Power Bomb": AP_MZM_ID_BASE + 75,
    "Crateria Power Grip": AP_MZM_ID_BASE + 76,
    "Crateria Moat": AP_MZM_ID_BASE + 77,
    "Crateria Statue Water": AP_MZM_ID_BASE + 78,
    "Crateria Plasma Beam/Unknown Item 1": AP_MZM_ID_BASE + 79,
    "Crateria Ball Spark": AP_MZM_ID_BASE + 80,
    "Crateria Upper Right corner": AP_MZM_ID_BASE + 81
}

chozodia_location_table = {
    "Chozodia Crateria Power Bomb": AP_MZM_ID_BASE + 82,
    "Chozodia Bomb Maze": AP_MZM_ID_BASE + 83,
    "Chozodia Zoomer Maze": AP_MZM_ID_BASE + 84,
    "Chozodia First Ruin Super": AP_MZM_ID_BASE + 85,  # TODO rename?
    "Chozodia Charlie Spark Missile": AP_MZM_ID_BASE + 86,  # TODO rename
    "Chozodia Charlie Spark Super": AP_MZM_ID_BASE + 87,  # TODO rename
    "Chozodia Out of the Way": AP_MZM_ID_BASE + 88,  # TODO rename
    "Chozodia Glass Tube E-Tank": AP_MZM_ID_BASE + 89,
    "Chozodia Lava Super": AP_MZM_ID_BASE + 90,
    "Chozodia Original Power Bomb": AP_MZM_ID_BASE + 91,
    "Chozodia Second Power Bomb": AP_MZM_ID_BASE + 92,  # TODO rename
    "Chozodia Glass Tube Power Bomb": AP_MZM_ID_BASE + 93,
    "Chozodia Charlie Spark": AP_MZM_ID_BASE + 94,  # TODO rename
    "Chozodia Shortcut Super": AP_MZM_ID_BASE + 95,
    "Chozodia Workbot Super": AP_MZM_ID_BASE + 96,
    "Chozodia Ship Hull Super": AP_MZM_ID_BASE + 97,
    "Chozodia Space Jump E-Tank": AP_MZM_ID_BASE + 98,
    "Chozodia Hull Power Bomb": AP_MZM_ID_BASE + 99,
    "Chozodia Space Pirate's Ship": None
}

full_location_table: dict[str, int] = {
    **brinstar_location_table,
    **kraid_location_table,
    **norfair_location_table,
    **ridley_location_table,
    **tourian_location_table,
    **crateria_location_table,
    **chozodia_location_table
}
