from typing import NamedTuple

from .constants import ItemType
from .sprites import Sprite
from .symbols import get_symbol


class ItemData(NamedTuple):
    type: ItemType  # used for determining the memory address to write bits to as each go somewhere different
    acquisition: int
    bits: int
    sprite: Sprite
    message: int | str  # Address of vanilla message if int; custom message text if str
    sound: int


SOUND_ARMING_WEAPON = 0x84


item_data_table = {
    "Nothing":            ItemData(ItemType.CUSTOM,              0,      0, Sprite.Nothing,          "Nothing acquired.",                                         SOUND_ARMING_WEAPON),

    "Energy Tank":        ItemData(ItemType.ENERGY_TANK,         1,      1, Sprite.EnergyTank,       get_symbol("sEnglishText_Message_EnergyTankAcquired"),                      0x87),
    "Missile Tank":       ItemData(ItemType.MISSILE_TANK,        3,      1, Sprite.MissileTank,      get_symbol("sEnglishText_Message_MissileTankAcquired"),      SOUND_ARMING_WEAPON),
    "Super Missile Tank": ItemData(ItemType.SUPER_MISSILE_TANK,  5,      1, Sprite.SuperMissileTank, get_symbol("sEnglishText_Message_SuperMissileTankAcquired"), SOUND_ARMING_WEAPON),
    "Power Bomb Tank":    ItemData(ItemType.POWER_BOMB_TANK,     7,      1, Sprite.PowerBombTank,    "Power Bomb Tank acquired.",                                 SOUND_ARMING_WEAPON),  # PBs don't say "acquired" in vanilla for some reason

    "Long Beam":          ItemData(ItemType.BEAM,                8, 1 << 0, Sprite.LongBeam,         get_symbol("sEnglishText_Message_LongBeam"),                                0xC9),
    "Charge Beam":        ItemData(ItemType.BEAM,                9, 1 << 4, Sprite.ChargeBeam,       get_symbol("sEnglishText_Message_ChargeBeam"),                              0xF0),
    "Ice Beam":           ItemData(ItemType.BEAM,               10, 1 << 1, Sprite.IceBeam,          get_symbol("sEnglishText_Message_IceBeam"),                                 0xCA),
    "Wave Beam":          ItemData(ItemType.BEAM,               11, 1 << 2, Sprite.WaveBeam,         get_symbol("sEnglishText_Message_WaveBeam"),                                0xCC),
    "Plasma Beam":        ItemData(ItemType.BEAM,               12, 1 << 3, Sprite.PlasmaBeam,       "Plasma Beam",                                                              0xD0),
    "Bomb":               ItemData(ItemType.BEAM,               13, 1 << 7, Sprite.Bomb,             get_symbol("sEnglishText_Message_Bomb"),                                    0xFF),

    "Varia Suit":         ItemData(ItemType.MAJOR,              14, 1 << 4, Sprite.VariaSuit,        get_symbol("sEnglishText_Message_VariaSuit"),                               0x7D),
    "Gravity Suit":       ItemData(ItemType.MAJOR,              15, 1 << 5, Sprite.GravitySuit,      "Gravity Suit",                                                             0x75),
    "Morph Ball":         ItemData(ItemType.MAJOR,              16, 1 << 6, Sprite.MorphBall,        get_symbol("sEnglishText_Message_MorphBall"),                               0x77),
    "Speed Booster":      ItemData(ItemType.MAJOR,              17, 1 << 1, Sprite.SpeedBooster,     get_symbol("sEnglishText_Message_SpeedBooster"),                            0x8D),
    "Hi-Jump":            ItemData(ItemType.MAJOR,              18, 1 << 0, Sprite.HiJump,           get_symbol("sEnglishText_Message_HighJump"),                                0x6A),
    "Screw Attack":       ItemData(ItemType.MAJOR,              19, 1 << 3, Sprite.ScrewAttack,      get_symbol("sEnglishText_Message_ScrewAttack"),                             0x6C),
    "Space Jump":         ItemData(ItemType.MAJOR,              20, 1 << 2, Sprite.SpaceJump,        "Space Jump",                                                               0x6B),
    "Power Grip":         ItemData(ItemType.MAJOR,              21, 1 << 7, Sprite.PowerGrip,        get_symbol("sEnglishText_Message_PowerGrip"),                               0x7B),

    "Fully Powered Suit": ItemData(ItemType.CUSTOM,              0, 1 << 7, Sprite.GravitySuit,      get_symbol("sEnglishText_Message_FullyPoweredSuit"),                       0x1D3),  # TODO: Custom sprite
    "Wall Jump":          ItemData(ItemType.CUSTOM,              0, 1 << 0, Sprite.WallJump,         "Wall Jump",                                                                0x76),
    "Spring Ball":        ItemData(ItemType.CUSTOM,              0, 1 << 1, Sprite.SpringBall,       "Spring Ball",                                                              0x70),
}
