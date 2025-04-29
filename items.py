"""
Classes and functions related to AP items for Metroid: Zero Mission
"""
import typing
from enum import IntEnum, IntFlag, StrEnum
from BaseClasses import Item, ItemClassification
from typing import Dict

from .item_sprites import Sprite

AP_MZM_ID_BASE = 261300

progression = ItemClassification.progression
filler = ItemClassification.filler
useful = ItemClassification.useful
trap = ItemClassification.trap


class ItemType(IntEnum):
    NONE = 0
    ENERGY_TANK = 1
    MISSILE_TANK = 2
    SUPER_MISSILE_TANK = 3
    POWER_BOMB_TANK = 4
    BEAM = 5
    MAJOR = 6
    CUSTOM = 7


class BeamFlags(IntFlag):
    LONG_BEAM = 1 << 0
    ICE_BEAM = 1 << 1
    WAVE_BEAM = 1 << 2
    PLASMA_BEAM = 1 << 3
    CHARGE_BEAM = 1 << 4
    BOMB = 1 << 7


class MajorFlags(IntFlag):
    HI_JUMP = 1 << 0
    SPEED_BOOSTER = 1 << 1
    SPACE_JUMP = 1 << 2
    SCREW_ATTACK = 1 << 3
    VARIA_SUIT = 1 << 4
    GRAVITY_SUIT = 1 << 5
    MORPH_BALL = 1 << 6
    POWER_GRIP = 1 << 7


class ItemAcquisition(IntEnum):
    DUMMY = 0
    ENERGY_TANK = 1
    MISSILES = 3
    SUPER_MISSILES = 5
    POWER_BOMBS = 7
    LONG_BEAM = 8
    CHARGE_BEAM = 9
    ICE_BEAM = 10
    WAVE_BEAM = 11
    PLASMA_BEAM = 12
    BOMBS = 13
    VARIA = 14
    GRAVITY = 15
    MORPH_BALL = 16
    SPEEDBOOSTER = 17
    HIGH_JUMP = 18
    SCREW_ATTACK = 19
    SPACE_JUMP = 20
    POWER_GRIP = 21


class MZMItem(Item):
    game: str = "Metroid Zero Mission"


class ItemData:
    code: int
    progression: ItemClassification
    type: ItemType  # used for determining the memory address to write bits to as each go somewhere different
    bits: int
    sprite: int
    acquisition: int

    def __init__(self, progression: ItemClassification, type: ItemType, bits: int, sprite: int, acquisition: int):
        self.code = AP_MZM_ID_BASE + (type << 8 | bits)
        self.progression = progression
        self.type = type
        self.bits = bits
        self.sprite = sprite
        self.acquisition = acquisition


tank_data_table = {
    "Energy Tank": ItemData(progression, ItemType.ENERGY_TANK, 1, Sprite.EnergyTank, ItemAcquisition.ENERGY_TANK),
    "Missile Tank": ItemData(progression, ItemType.MISSILE_TANK, 1, Sprite.MissileTank, ItemAcquisition.MISSILES),
    "Super Missile Tank": ItemData(progression, ItemType.SUPER_MISSILE_TANK, 1, Sprite.SuperMissileTank, ItemAcquisition.SUPER_MISSILES),
    "Power Bomb Tank": ItemData(progression, ItemType.POWER_BOMB_TANK, 1, Sprite.PowerBombTank, ItemAcquisition.POWER_BOMBS),
}

major_item_data_table = {
    "Long Beam": ItemData(progression, ItemType.BEAM, BeamFlags.LONG_BEAM, Sprite.LongBeam, ItemAcquisition.LONG_BEAM),
    "Charge Beam": ItemData(progression, ItemType.BEAM, BeamFlags.CHARGE_BEAM, Sprite.ChargeBeam, ItemAcquisition.CHARGE_BEAM),
    "Ice Beam": ItemData(progression, ItemType.BEAM, BeamFlags.ICE_BEAM, Sprite.IceBeam, ItemAcquisition.ICE_BEAM),
    "Wave Beam": ItemData(progression, ItemType.BEAM, BeamFlags.WAVE_BEAM, Sprite.WaveBeam, ItemAcquisition.WAVE_BEAM),
    "Plasma Beam": ItemData(progression, ItemType.BEAM, BeamFlags.PLASMA_BEAM, Sprite.PlasmaBeam, ItemAcquisition.PLASMA_BEAM),
    "Bomb": ItemData(progression, ItemType.BEAM, BeamFlags.BOMB, Sprite.Bomb, ItemAcquisition.BOMBS),
    "Varia Suit": ItemData(progression, ItemType.MAJOR, MajorFlags.VARIA_SUIT, Sprite.VariaSuit, ItemAcquisition.VARIA),
    "Gravity Suit": ItemData(progression, ItemType.MAJOR, MajorFlags.GRAVITY_SUIT, Sprite.GravitySuit, ItemAcquisition.GRAVITY),
    "Morph Ball": ItemData(progression, ItemType.MAJOR, MajorFlags.MORPH_BALL, Sprite.MorphBall, ItemAcquisition.MORPH_BALL),
    "Speed Booster": ItemData(progression, ItemType.MAJOR, MajorFlags.SPEED_BOOSTER, Sprite.SpeedBooster, ItemAcquisition.SPEEDBOOSTER),
    "Hi-Jump": ItemData(progression, ItemType.MAJOR, MajorFlags.HI_JUMP, Sprite.HiJump, ItemAcquisition.HIGH_JUMP),
    "Screw Attack": ItemData(progression, ItemType.MAJOR, MajorFlags.SCREW_ATTACK, Sprite.ScrewAttack, ItemAcquisition.SCREW_ATTACK),
    "Space Jump": ItemData(progression, ItemType.MAJOR, MajorFlags.SPACE_JUMP, Sprite.SpaceJump, ItemAcquisition.SPACE_JUMP),
    "Power Grip": ItemData(progression, ItemType.MAJOR, MajorFlags.POWER_GRIP, Sprite.PowerGrip, ItemAcquisition.POWER_GRIP),
}

extra_item_data_table = {
    "Nothing": ItemData(filler, ItemType.CUSTOM, 0, Sprite.Nothing, ItemAcquisition.DUMMY),
}

item_data_table: Dict[str, ItemData] = {
    **tank_data_table,
    **major_item_data_table,
    **extra_item_data_table,
}

mzm_item_name_groups = {
    "Beams": {name for name, data in major_item_data_table.items() if data.type == ItemType.BEAM and data.bits != BeamFlags.BOMB},
    "Upgrades": {
        "Bomb",
        *(name for name, data in major_item_data_table.items() if data.type == ItemType.MAJOR)
    },
    "Major Items": set(major_item_data_table.keys()),
    "Missiles": {
        "Missile Tank",
        "Super Missile Tank",
    },
}
