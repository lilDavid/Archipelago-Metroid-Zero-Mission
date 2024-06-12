from typing import Mapping

from BaseClasses import Item


compatible_games: Mapping[str, Mapping[str, int]] = {
    "Super Metroid": {
        "Energy Tank": 0,
        "Missile": 1,
        "Super Missile": 2,
        "Power Bomb": 3,
        "Bomb": 9,
        "Charge Beam": 5,
        "Ice Beam": 6,
        "Hi-Jump Boots": 14,
        "Speed Booster": 13,
        "Wave Beam": 7,
        # "Spazer Beam":
        # "Spring Ball":
        "Varia Suit": 10,
        "Plasma Beam": 8,
        # "Grappling Beam":
        "Morph Ball": 12,
        # "Reserve Tank":
        "Gravity Suit": 11,
        # "X-Ray Scope":
        "Space Jump": 16,
        "Screw Attack": 15,
    },
    "SMZ3": {
        "Missile": 1,
        "Super": 2,
        "PowerBomb": 3,
        # "Grapple":
        # "XRay":
        "ETank": 0,
        # "ReserveTank":
        "Charge": 5,
        "Ice": 6,
        "Wave": 7,
        # "Spazer":
        "Plasma": 8,
        "Varia": 10,
        "Gravity": 11,
        "Morph": 12,
        "Bombs": 9,
        # "SpringBall":
        "ScrewAttack": 15,
        "HiJump": 14,
        "SpaceJump": 16,
        "SpeedBooster": 13,
    },
}


def get_zero_mission_sprite(item: Item):
    if item.game not in compatible_games:
        return None

    return compatible_games[item.game].get(item.code)
