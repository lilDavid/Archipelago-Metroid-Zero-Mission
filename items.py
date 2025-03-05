"""
Classes and functions related to AP items for Metroid: Zero Mission
"""
import typing
from enum import IntEnum
from BaseClasses import Item, ItemClassification
from typing import Dict

AP_MZM_ID_BASE = 261300

progression = ItemClassification.progression
filler = ItemClassification.filler
useful = ItemClassification.useful
trap = ItemClassification.trap


class ItemType(IntEnum):
    tank = 0
    major = 1
    beam = 2


class MZMItem(Item):
    game: str = "Metroid Zero Mission"


class ItemData:
    code: int
    id: int
    progression: ItemClassification
    type: ItemType  # used for determining the memory address to write bits to as each go somewhere different
    bits: typing.Optional[int]  # bit to flip when adding this item to Samus' equipment

    def __init__(self, id: int, progression: ItemClassification, type: ItemType, bits: int) -> None:
        self.id = id
        self.code = id + AP_MZM_ID_BASE
        self.progression = progression
        self.type = type
        self.bits = bits


# Assignments lifted from BioSpark's MZM Randomizer

class ItemID(IntEnum):
    EnergyTank = 0
    MissileTank = 1
    SuperMissileTank = 2
    PowerBombTank = 3
    LongBeam = 4
    ChargeBeam = 5
    IceBeam = 6
    WaveBeam = 7
    PlasmaBeam = 8
    Bomb = 9
    VariaSuit = 10
    GravitySuit = 11
    MorphBall = 12
    SpeedBooster = 13
    HiJump = 14
    ScrewAttack = 15
    SpaceJump = 16
    PowerGrip = 17
    Nothing = 18

    # Other games' items
    APItemFiller = 19
    APItemProgression = 20
    APItemUseful = 21
    SpazerBeam = 22
    GrappleBeam = 23
    SpringBall = 24
    XRayScope = 25
    ReserveTank = 26
    WallJump = 27
    PowerBeam = 28
    SpiderBall = 29


tank_data_table = {
    "Energy Tank": ItemData(ItemID.EnergyTank, progression, ItemType.tank, None),
    "Missile Tank": ItemData(ItemID.MissileTank, progression, ItemType.tank, None),
    "Super Missile Tank": ItemData(ItemID.SuperMissileTank, progression, ItemType.tank, None),
    "Power Bomb Tank": ItemData(ItemID.PowerBombTank, progression, ItemType.tank, None),
}

major_item_data_table = {
    "Long Beam": ItemData(ItemID.LongBeam, progression, ItemType.beam, 0x1),
    "Charge Beam": ItemData(ItemID.ChargeBeam, progression, ItemType.beam, 0x10),
    "Ice Beam": ItemData(ItemID.IceBeam, progression, ItemType.beam, 0x2),
    "Wave Beam": ItemData(ItemID.WaveBeam, progression, ItemType.beam, 0x4),
    "Plasma Beam": ItemData(ItemID.PlasmaBeam, progression, ItemType.beam, 0x8),
    "Bomb": ItemData(ItemID.Bomb, progression, ItemType.beam, 0x80),  # regular bomb is stored with beams
    "Varia Suit": ItemData(ItemID.VariaSuit, progression, ItemType.major, 0x10),
    "Gravity Suit": ItemData(ItemID.GravitySuit, progression, ItemType.major, 0x20),
    "Morph Ball": ItemData(ItemID.MorphBall, progression, ItemType.major, 0x40),
    "Speed Booster": ItemData(ItemID.SpeedBooster, progression, ItemType.major, 0x2),
    "Hi-Jump": ItemData(ItemID.HiJump, progression, ItemType.major, 0x1),
    "Screw Attack": ItemData(ItemID.ScrewAttack, progression, ItemType.major, 0x8),
    "Space Jump": ItemData(ItemID.SpaceJump, progression, ItemType.major, 0x4),
    "Power Grip": ItemData(ItemID.PowerGrip, progression, ItemType.major, 0x80),
}

extra_item_data_table = {
    "Nothing": ItemData(ItemID.Nothing, filler, None, None),
}

item_data_table: Dict[str, ItemData] = {
    **tank_data_table,
    **major_item_data_table,
    **extra_item_data_table,
}

mzm_item_name_groups = {
    "Beams": {name for name, data in major_item_data_table.items() if data.type == ItemType.beam and data.id != ItemID.Bomb},
    "Upgrades": {
        "Bomb",
        *(name for name, data in major_item_data_table.items() if data.type == ItemType.major)
    },
    "Major Items": set(major_item_data_table.keys()),
    "Missiles": {
        "Missile Tank",
        "Super Missile Tank",
    },
}
