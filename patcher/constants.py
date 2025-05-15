from enum import IntEnum


class Area(IntEnum):
    BRINSTAR = 0
    KRAID = 1
    NORFAIR = 2
    RIDLEY = 3
    TOURIAN = 4
    CRATERIA = 5
    CHOZODIA = 6


class ItemType(IntEnum):
    NONE = 0
    ENERGY_TANK = 1
    MISSILE_TANK = 2
    SUPER_MISSILE_TANK = 3
    POWER_BOMB_TANK = 4
    BEAM = 5
    MAJOR = 6
    CUSTOM = 7


PIXEL_SIZE = 4


RC_COUNT = 101
