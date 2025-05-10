"""
Classes and functions related to AP items for Metroid: Zero Mission
"""

from enum import IntEnum, IntFlag
from BaseClasses import Item, ItemClassification
from typing import Dict, NamedTuple

from .data import get_symbol

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


class MZMItem(Item):
    game: str = "Metroid Zero Mission"


class ItemData(NamedTuple):
    progression: ItemClassification
    type: ItemType  # used for determining the memory address to write bits to as each go somewhere different
    bits: int
    appearance_data: tuple[str, int, int | str, int]  # Sprite name, acquisition number, message, sound number

    @property
    def code(self):
        return AP_MZM_ID_BASE + (self.type << 8 | self.bits)

    @property
    def sprite(self):
        return self.appearance_data[0]

    @property
    def acquisition(self):
        return self.appearance_data[1]

    @property
    def message(self):
        """
        - int: Address of message data
        - str: Message to be injected into ROM
        """
        return self.appearance_data[2]

    @property
    def sound(self):
        return self.appearance_data[3]


SOUND_ARMING_WEAPON = 0x84


tank_data_table = {
    "Energy Tank":        ItemData(progression, ItemType.ENERGY_TANK,        1, (Sprite.EnergyTank,       1, get_symbol("sEnglishText_Message_EnergyTankAcquired"),                      0x87)),
    "Missile Tank":       ItemData(progression, ItemType.MISSILE_TANK,       1, (Sprite.MissileTank,      3, get_symbol("sEnglishText_Message_MissileTankAcquired"),      SOUND_ARMING_WEAPON)),
    "Super Missile Tank": ItemData(progression, ItemType.SUPER_MISSILE_TANK, 1, (Sprite.SuperMissileTank, 5, get_symbol("sEnglishText_Message_SuperMissileTankAcquired"), SOUND_ARMING_WEAPON)),
    "Power Bomb Tank":    ItemData(progression, ItemType.POWER_BOMB_TANK,    1, (Sprite.PowerBombTank,    7, "Power Bomb Tank acquired.",                                 SOUND_ARMING_WEAPON)),  # PBs don't say "acquired" in vanilla for some reason
}

major_item_data_table = {
    "Long Beam":          ItemData(progression, ItemType.BEAM,   1 << 0, (Sprite.LongBeam,      8, get_symbol("sEnglishText_Message_LongBeam"),         0xC9)),
    "Charge Beam":        ItemData(progression, ItemType.BEAM,   1 << 4, (Sprite.ChargeBeam,    9, get_symbol("sEnglishText_Message_ChargeBeam"),       0xF0)),
    "Ice Beam":           ItemData(progression, ItemType.BEAM,   1 << 1, (Sprite.IceBeam,      10, get_symbol("sEnglishText_Message_IceBeam"),          0xCA)),
    "Wave Beam":          ItemData(progression, ItemType.BEAM,   1 << 2, (Sprite.WaveBeam,     11, get_symbol("sEnglishText_Message_WaveBeam"),         0xCC)),
    "Plasma Beam":        ItemData(progression, ItemType.BEAM,   1 << 3, (Sprite.PlasmaBeam,   12, "Plasma Beam",                                       0xD0)),
    "Bomb":               ItemData(progression, ItemType.BEAM,   1 << 7, (Sprite.Bomb,         13, get_symbol("sEnglishText_Message_Bomb"),             0xFF)),

    "Varia Suit":         ItemData(progression, ItemType.MAJOR,  1 << 4, (Sprite.VariaSuit,    14, get_symbol("sEnglishText_Message_VariaSuit"),        0x7D)),
    "Gravity Suit":       ItemData(progression, ItemType.MAJOR,  1 << 5, (Sprite.GravitySuit,  15, "Gravity Suit",                                      0x75)),
    "Morph Ball":         ItemData(progression, ItemType.MAJOR,  1 << 6, (Sprite.MorphBall,    16, get_symbol("sEnglishText_Message_MorphBall"),        0x77)),
    "Speed Booster":      ItemData(progression, ItemType.MAJOR,  1 << 1, (Sprite.SpeedBooster, 17, get_symbol("sEnglishText_Message_SpeedBooster"),     0x8D)),
    "Hi-Jump":            ItemData(progression, ItemType.MAJOR,  1 << 0, (Sprite.HiJump,       18, get_symbol("sEnglishText_Message_HighJump"),         0x6A)),
    "Screw Attack":       ItemData(progression, ItemType.MAJOR,  1 << 3, (Sprite.ScrewAttack,  19, get_symbol("sEnglishText_Message_ScrewAttack"),      0x6C)),
    "Space Jump":         ItemData(progression, ItemType.MAJOR,  1 << 2, (Sprite.SpaceJump,    20, "Space Jump",                                        0x6B)),
    "Power Grip":         ItemData(progression, ItemType.MAJOR,  1 << 7, (Sprite.PowerGrip,    21, get_symbol("sEnglishText_Message_PowerGrip"),        0x7B)),

    "Fully Powered Suit": ItemData(progression, ItemType.CUSTOM, 1 << 7, (Sprite.GravitySuit,   0, get_symbol("sEnglishText_Message_FullyPoweredSuit"), 0x1D3)),  # TODO: Custom sprite
    "Wall Jump Boots":    ItemData(progression, ItemType.CUSTOM, 1 << 6, (Sprite.WallJump,      0, "Wall Jump Boots",                                   0x76)),
}

extra_item_data_table = {
    "Nothing": ItemData(filler, ItemType.CUSTOM, 0, (Sprite.Nothing, 0, "Nothing acquired.", SOUND_ARMING_WEAPON)),
}

item_data_table: Dict[str, ItemData] = {
    **tank_data_table,
    **major_item_data_table,
    **extra_item_data_table,
}

mzm_item_name_groups = {
    "Beams": {name for name in major_item_data_table.keys() if name != "Bomb"},
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
