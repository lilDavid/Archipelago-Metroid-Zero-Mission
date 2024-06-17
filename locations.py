"""
Classes and functions related to AP locations for Metroid: Zero Mission
"""
from BaseClasses import Location
from .items import AP_MZM_ID_BASE


class MZMLocation(Location):
    game: str = "Metroid Zero Mission"


# Location numbers/order and some names from Biospark's MZM Randomizer.
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
    "Brinstar Acid near Varia": AP_MZM_ID_BASE + 10,
    "Brinstar First Missile": AP_MZM_ID_BASE + 11,
    "Brinstar Behind Hive": AP_MZM_ID_BASE + 12,
    "Brinstar Under Bridge": AP_MZM_ID_BASE + 13,
    "Brinstar Post-Hive Missile": AP_MZM_ID_BASE + 14,
    "Brinstar Upper Pillar Missile": AP_MZM_ID_BASE + 15,
    "Brinstar Behind Bombs": AP_MZM_ID_BASE + 16,
    "Brinstar Bomb": AP_MZM_ID_BASE + 17,
    "Brinstar Post-Hive E-Tank": AP_MZM_ID_BASE + 18,
}

kraid_location_table = {
    "Kraid Giant Hoppers Missile": AP_MZM_ID_BASE + 19,
    "Kraid Save Room Missile": AP_MZM_ID_BASE + 20,
    "Kraid Crumble Block Missile": AP_MZM_ID_BASE + 21,
    "Kraid Quad Ball Cannon Room": AP_MZM_ID_BASE + 22,
    "Kraid Space Jump/Unknown Item 2": AP_MZM_ID_BASE + 23,
    "Kraid Acid Ballspark": AP_MZM_ID_BASE + 24,
    "Kraid Speed Booster": AP_MZM_ID_BASE + 25,
    "Kraid Worm Missile": AP_MZM_ID_BASE + 26,
    "Kraid Pillar Missile": AP_MZM_ID_BASE + 27,
    "Kraid Acid Fall": AP_MZM_ID_BASE + 28,
    "Kraid Worm E-Tank": AP_MZM_ID_BASE + 29,
    "Kraid Speed Jump": AP_MZM_ID_BASE + 30,
    "Kraid Upper Right Morph Ball Cannon": AP_MZM_ID_BASE + 31,
    "Kraid Defeated": None
}

norfair_location_table = {
    "Norfair Lava Power Bomb": AP_MZM_ID_BASE + 32,
    "Norfair Lava Missile": AP_MZM_ID_BASE + 33,
    "Norfair Screw Attack": AP_MZM_ID_BASE + 34,
    "Norfair Screw Attack Missile": AP_MZM_ID_BASE + 35,
    "Norfair Power Grip Missile": AP_MZM_ID_BASE + 36,
    "Norfair Under Crateria Elevator": AP_MZM_ID_BASE + 37,
    "Norfair Wave Beam": AP_MZM_ID_BASE + 38,
    "Norfair Bomb Trap": AP_MZM_ID_BASE + 39,
    "Norfair Bottom Heated Room First": AP_MZM_ID_BASE + 40,  #TODO: maybe rename
    "Norfair Bottom Heated Room Second": AP_MZM_ID_BASE + 41,  #TODO and this one
    "Norfair Heated Room Under Brinstar Elevator": AP_MZM_ID_BASE + 42,
    "Norfair Space Boost Missile": AP_MZM_ID_BASE + 43,  # TODO maybe rename
    "Norfair Space Boost Super Missile": AP_MZM_ID_BASE + 44,  # TODO and this one
    "Norfair Ice Beam": AP_MZM_ID_BASE + 45,
    "Norfair Heated Room above Ice Beam": AP_MZM_ID_BASE + 46,
    "Norfair Hi-Jump": AP_MZM_ID_BASE + 47,
    "Norfair Big Room": AP_MZM_ID_BASE + 48,
    "Norfair Behind Top Chozo Statue": AP_MZM_ID_BASE + 49,
    "Norfair Larva Ceiling E-tank": AP_MZM_ID_BASE + 50,
    "Norfair Right Shaft Lower": AP_MZM_ID_BASE + 51,
    "Norfair Right Shaft Bottom": AP_MZM_ID_BASE + 52
}

ridley_location_table = {
    "Ridley Southwest Puzzle Top": AP_MZM_ID_BASE + 53,
    "Ridley Southwest Puzzle Bottom": AP_MZM_ID_BASE + 54,
    "Ridley West Pillar": AP_MZM_ID_BASE + 55,
    "Ridley E-Tank behind Gravity": AP_MZM_ID_BASE + 56,
    "Ridley Gravity Suit/Unknown Item 3": AP_MZM_ID_BASE + 57,
    "Ridley Fake Floor E-Tank": AP_MZM_ID_BASE + 58,
    "Ridley Upper Ball Cannon Puzzle": AP_MZM_ID_BASE + 59,
    "Ridley Lower Ball Cannon Puzzle": AP_MZM_ID_BASE + 60,
    "Ridley Imago Super Missile": AP_MZM_ID_BASE + 61,
    "Ridley After Sidehopper Hall Upper": AP_MZM_ID_BASE + 62,
    "Ridley After Sidehopper Hall Lower": AP_MZM_ID_BASE + 63,
    "Ridley Long Hall": AP_MZM_ID_BASE + 64,
    "Ridley Center Pillar Missile": AP_MZM_ID_BASE + 65,
    "Ridley Ball Room Missile": AP_MZM_ID_BASE + 66,
    "Ridley Ball Room Super": AP_MZM_ID_BASE + 67,
    "Ridley Fake Lava Missile": AP_MZM_ID_BASE + 68,
    "Ridley Owl E-Tank": AP_MZM_ID_BASE + 69,
    "Ridley Northeast corner Missile": AP_MZM_ID_BASE + 70,
    "Ridley Bomb Puzzle": AP_MZM_ID_BASE + 71,
    "Ridley Speed Jump": AP_MZM_ID_BASE + 72,
    "Ridley Defeated": None
}

tourian_location_table = {
    "Tourian Left of Mother Brain": AP_MZM_ID_BASE + 73,
    "Tourian Under Mother Brain ": AP_MZM_ID_BASE + 74,
    "Mother Brain Defeated": None
}

crateria_location_table = {
    "Crateria Landing Site Ballspark": AP_MZM_ID_BASE + 75,
    "Crateria Power Grip": AP_MZM_ID_BASE + 76,
    "Crateria Moat": AP_MZM_ID_BASE + 77,
    "Crateria Statue Water": AP_MZM_ID_BASE + 78,
    "Crateria Plasma Beam/Unknown Item 1": AP_MZM_ID_BASE + 79,
    "Crateria East Ballspark": AP_MZM_ID_BASE + 80,
    "Crateria Northeast Corner": AP_MZM_ID_BASE + 81
}

chozodia_location_table = {
    "Chozodia Upper Crateria Door": AP_MZM_ID_BASE + 82,
    "Chozodia Bomb Maze": AP_MZM_ID_BASE + 83,
    "Chozodia Zoomer Maze": AP_MZM_ID_BASE + 84,
    "Chozodia Ruins Near Upper Crateria Door": AP_MZM_ID_BASE + 85,
    "Chozodia Chozo Ghost Area Morph Tunnel Above Water": AP_MZM_ID_BASE + 86,
    "Chozodia Chozo Ghost Area Underwater": AP_MZM_ID_BASE + 87,
    "Chozodia Under Chozo Ghost Area Water": AP_MZM_ID_BASE + 88,
    "Chozodia Glass Tube E-Tank": AP_MZM_ID_BASE + 89,
    "Chozodia Lava Super": AP_MZM_ID_BASE + 90,
    "Chozodia Original Power Bomb": AP_MZM_ID_BASE + 91,
    "Chozodia Next to Original Power Bomb": AP_MZM_ID_BASE + 92,
    "Chozodia Glass Tube Power Bomb": AP_MZM_ID_BASE + 93,
    "Chozodia Chozo Ghost Area Long Shinespark": AP_MZM_ID_BASE + 94,
    "Chozodia Shortcut Super": AP_MZM_ID_BASE + 95,
    "Chozodia Workbot Super": AP_MZM_ID_BASE + 96,
    "Chozodia Mothership Ceiling Near ZSS Start": AP_MZM_ID_BASE + 97,
    "Chozodia Under Mecha Ridley Hallway": AP_MZM_ID_BASE + 98,
    "Chozodia Southeast Corner In Hull": AP_MZM_ID_BASE + 99,
    "Chozo Ghost Defeated": None,
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
