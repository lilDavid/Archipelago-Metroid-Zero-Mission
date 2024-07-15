"""
Functions used to describe Metroid: Zero Mission logic rules in rules.py
"""

from __future__ import annotations

import builtins
import functools
from typing import TYPE_CHECKING, Any, Callable, NamedTuple
from BaseClasses import CollectionState

from .options import MZMOptions

if TYPE_CHECKING:
    from . import MZMWorld


class Requirement(NamedTuple):
    rule: Callable[[MZMWorld, CollectionState], bool]

    def create_rule(self, world: MZMWorld):
        return functools.partial(self.rule, world)

    @classmethod
    def item(cls, item: str, count: int = 1):
        return cls(lambda world, state: state.has(item, world.player, count))

    @classmethod
    def location(cls, location: str):
        return cls(lambda world, state: state.can_reach_location(location, world.player))

    @classmethod
    def entrance(cls, entrance: str):
        return cls(lambda world, state: state.can_reach_entrance(entrance, world.player))

    @classmethod
    def setting_enabled(cls, setting: str):
        return cls(lambda world, _: getattr(world.options, setting))

    @classmethod
    def setting_is(cls, setting: str, value: Any):
        return cls(lambda world, _: getattr(world.options, setting) == value)

    @classmethod
    def setting_atleast(cls, setting: str, value: int):
        return cls(lambda world, _: getattr(world.options, setting) >= value)


def all(*args: Requirement):
    return Requirement(lambda world, state: builtins.all(req.rule(world, state) for req in args))

def any(*args: Requirement):
    return Requirement(lambda world, state: builtins.any(req.rule(world, state) for req in args))


KraidBoss = Requirement.item("Kraid Defeated")
RidleyBoss = Requirement.item("Ridley Defeated")
MotherBrainBoss = Requirement.item("Mother Brain Defeated")
ChozoGhostBoss = Requirement.item("Chozo Ghost Defeated")
MechaRidleyBoss = Requirement.item("Mecha Ridley Defeated")

UnknownItem1 = Requirement.location("Crateria Plasma Beam/Unknown Item 1")
UnknownItem2 = Requirement.location("Kraid Space Jump/Unknown Item 2")
UnknownItem3 = Requirement.location("Ridley Gravity Suit/Unknown Item 3")

CanUseUnknownItems = any(
    Requirement.setting_enabled("unknown_items_always_usable"),
    ChozoGhostBoss,
)
LayoutPatches = Requirement.setting_enabled("layout_patches")

EnergyTanks = lambda n: Requirement.item("Energy Tank", n)
MissileTanks = lambda n: Requirement.item("Missile Tank", n)
SuperMissileTanks = lambda n: Requirement.item("Super Missile Tank", n)
PowerBombTanks = lambda n: Requirement.item("Power Bomb Tank", n)
LongBeam = Requirement.item("Long Beam")
ChargeBeam = Requirement.item("Charge Beam")
IceBeam = Requirement.item("Ice Beam")
WaveBeam = Requirement.item("Wave Beam")
PlasmaBeam = all(
    Requirement.item("Plasma Beam"),
    CanUseUnknownItems,
)
Bomb = Requirement.item("Bomb")
VariaSuit = Requirement.item("Varia Suit")
GravitySuit = all(
    Requirement.item("Gravity Suit"),
    CanUseUnknownItems
)
MorphBall = Requirement.item("Morph Ball")
SpeedBooster = Requirement.item("Speed Booster")
HiJump = Requirement.item("Hi-Jump")
ScrewAttack = Requirement.item("Screw Attack")
SpaceJump = all(
    Requirement.item("Space Jump"),
    CanUseUnknownItems
)
PowerGrip = Requirement.item("Power Grip")

Missiles = any(
    MissileTanks(1),
    SuperMissileTanks(1),
)
MissileCount = lambda n: Requirement(
    lambda world, state:
        5 * state.count("Missile Tank", world.player) + 2 * state.count("Super Missile Tank", world.player)
        >= n
)
SuperMissiles = SuperMissileTanks(1)
PowerBombs = PowerBombTanks(1)
PowerBombCount = lambda n: PowerBombTanks(n // 2)

CanRegularBomb = all(
    MorphBall,
    Bomb,
)
CanIBJ = all(
    Requirement.setting_enabled("ibj_in_logic"),
    CanRegularBomb,
)
CanHiJump = any(
    HiJump,
    SpaceJump,
    CanIBJ,
)
CanHjSjIbjOrGrip = any(  # This name is even more cursed in Pascal case
    CanHiJump,
    PowerGrip,
)
CanWallJump = Requirement.setting_enabled("walljumps_in_logic")
CanTrickySparks = all(
    lambda world, state: False,
    SpeedBooster,
)

CanBombBlock = all(
    MorphBall,
    any(
        Bomb,
        PowerBombTanks(1),
    ),
)
CanBallCannon = CanRegularBomb
CanBallspark = all(
    MorphBall,
    SpeedBooster,
    HiJump,
)

CanLongBeam = any(
    LongBeam,
    MissileCount(1),
    CanBombBlock,
)

CanTraverseHeat = VariaSuit
Hellrun = lambda n: all(
    Requirement.setting_enabled("heatruns_lavadives"),
    EnergyTanks(n),
)

# TODO: Add missing logic options
# TODO: Fine tune boss logic

def _get_options(state: CollectionState, player: int) -> MZMOptions:
    return state.multiworld.worlds[player].options


def has_missiles(state: CollectionState, player: int) -> bool:
    return state.has_any({"Missile Tank", "Super Missile Tank"}, player)


def has_missile_count(state: CollectionState, player: int, required_missiles: int) -> int:
    # TODO: somehow account for Hard mode
    missilecount = (state.count("Missile Tank", player) * 5) + (state.count("Super Missile Tank", player) * 2)
    return missilecount >= required_missiles


def has_super_missiles(state: CollectionState, player: int) -> bool:
    return state.has("Super Missile Tank", player)


def has_power_bombs(state: CollectionState, player: int):
    return state.has("Power Bomb Tank", player)


def power_bomb_count(state: CollectionState, player: int, required_pbs: int):
    pbcount = (state.count("Power Bomb Tank", player) * 2)
    return pbcount >= required_pbs


def can_regular_bomb(state: CollectionState, player: int):
    return state.has_all({"Morph Ball", "Bomb"}, player)


# this may be different from can_regular_bomb later and also just reads easier in some rules
def can_ballcannon(state: CollectionState, player: int):
    return state.has_all({"Morph Ball", "Bomb"}, player)


def can_bomb_block(state: CollectionState, player: int) -> bool:
    return (state.has("Morph Ball", player)
            and state.has_any({"Bomb", "Power Bomb Tank"}, player))


# checked for ability to clear blocks that would require long beam to hit
def can_long_beam(state: CollectionState, player: int) -> bool:
    return (state.has("Long Beam", player)
            or has_missile_count(state, player, 3)
            or can_bomb_block(state, player))


def can_hi_jump(state: CollectionState, player: int) -> bool:
    return state.has("Hi-Jump", player) or can_space_jump(state, player) or can_ibj(state, player)


# this particular combination is extremely common
def can_hj_sj_ibj_or_grip(state: CollectionState, player: int) -> bool:
    return can_hi_jump(state, player) or state.has("Power Grip", player)


def can_ballspark(state: CollectionState, player: int) -> bool:
    return state.has_all({"Morph Ball", "Hi-Jump", "Speed Booster"}, player)


def can_space_jump(state: CollectionState, player: int) -> bool:
    return (state.has("Space Jump", player)
            and (state.has("Chozo Ghost Defeated", player)
                 or _get_options(state, player).unknown_items_always_usable.value)
            )


def can_traverse_heat(state: CollectionState, player: int) -> bool:
    return state.has("Varia Suit", player)


def can_gravity_suit(state: CollectionState, player: int) -> bool:
    return (state.has("Gravity Suit", player)
            and (state.has("Chozo Ghost Defeated", player)
                 or _get_options(state, player).unknown_items_always_usable.value)
            )


# currently used for both heated rooms AND lava dives
def hellrun(state: CollectionState, player: int, required_etanks: int) -> bool:
    return (_get_options(state, player).heatruns_lavadives.value
            and (state.count("Energy Tank", player) >= required_etanks))


def can_ibj(state: CollectionState, player: int) -> bool:
    return _get_options(state, player).ibj_in_logic.value and can_regular_bomb(state, player)


def can_walljump(state: CollectionState, player: int) -> bool:
    return _get_options(state, player).walljumps_in_logic.value


def can_tricky_sparks(state: CollectionState, player: int) -> bool:
    return False and state.has("Speed Booster", player)  # TODO: add option


def brinstar_past_hives(state: CollectionState, player: int) -> bool:
    return (state.has("Morph Ball", player)
            and (has_missile_count(state, player, 10)
                 or state.has("Super Missile Tank", player)
                 or state.has_any({"Long Beam", "Ice Beam", "Wave Beam", "Plasma Beam", "Screw Attack"}, player)))


# used for the items in this area as well as determining whether the ziplines can be activated
# it's technically possible to do the climb after ballcannon with just hi-jump using tight morph jumps
# TODO: add solo hi-jump logic once an option for advanced tricks is added
def kraid_upper_right(state: CollectionState, player: int) -> bool:
    return (has_missiles(state, player)
            and can_ballcannon(state, player)
            and (can_ibj(state, player)
                 or can_walljump(state, player)
                 or can_space_jump(state, player)
                 or state.has("Power Grip", player))
            ) and (can_ibj(state, player)
                   or state.has("Power Grip", player)
                   or (state.has_all({"Ice Beam", "Hi-Jump"}, player)))


# access to lower kraid via left shaft
# TODO: add logic for acid worm skip
def kraid_left_shaft_access(state: CollectionState, player: int) -> bool:
    return ((can_ibj(state, player) or state.has_any({"Power Grip", "Hi-Jump"}, player))
            and can_bomb_block(state, player)
            and (can_regular_bomb(state, player) or state.has("Hi-Jump", player))
            and (kraid_upper_right(state, player)
                 or can_space_jump(state, player)
                 or (can_gravity_suit(state, player) and can_tricky_sparks(state, player))
                 )
            )


def norfair_right_shaft_access(state: CollectionState, player: int) -> bool:
    return can_hj_sj_ibj_or_grip(state, player) or state.has("Speed Booster", player)


def norfair_upper_right_shaft(state: CollectionState, player: int) -> bool:
    return (norfair_right_shaft_access(state, player)
            and (can_hj_sj_ibj_or_grip(state, player)
                 or state.has("Ice Beam", player)
                 or can_walljump(state, player))
            )


# used for one item and the ridley shortcut
def norfair_behind_ice_beam(state: CollectionState, player: int) -> bool:
    return (norfair_upper_right_shaft(state, player)
            and (can_long_beam(state, player) or state.has("Wave Beam", player))
            and ((state.has("Ice Beam", player) and state.has_any({"Hi-Jump", "Power Grip"},
                                                                  player))  # to get up the rippers
                 or can_ibj(state, player)
                 or (can_walljump(state, player) and state.has("Power Grip", player)))
            )


def norfair_lower_right_shaft(state: CollectionState, player: int) -> bool:
    return (norfair_right_shaft_access(state, player)
            and (state.has("Screw Attack", player)
                 or (state.has("Speed Booster", player) and can_ballcannon(state, player)))
            )


def norfair_to_save_behind_hijump(state: CollectionState, player: int) -> bool:
    return (norfair_lower_right_shaft(state, player)
            and has_missiles(state, player)
            and can_bomb_block(state, player)
            and (can_ibj(state, player)
                 or (has_power_bombs(state, player) and state.has("Hi-Jump", player))
                 or (state.has("Bomb", player) and state.has_any({"Hi-Jump", "Power Grip"}, player))
                 )
            and (can_hj_sj_ibj_or_grip(state, player) or can_walljump(state, player)
                 or state.has("Ice Beam", player))
            and (can_traverse_heat(state, player)
                 or hellrun(state, player, 6))
            and (can_ibj(state, player)
                 or can_space_jump(state, player)
                 or (state.has("Speed Booster", player)
                     and (can_bomb_block(state, player) or state.has("Screw Attack", player))
                     )
                 )
            )


def norfair_shortcut(state: CollectionState, player: int) -> bool:
    return (norfair_behind_ice_beam(state, player)
            and has_missiles(state, player)
            and (can_ibj(state, player)
                 or (state.has("Power Grip", player)
                     and (can_space_jump(state, player) or can_walljump(state, player))
                     and can_bomb_block(state, player)))
            )


def norfair_bottom_right_shaft(state: CollectionState, player: int) -> bool:
    return ((norfair_to_save_behind_hijump(state, player)
             and has_missile_count(state, player, 4)
             and state.has_all({"Wave Beam", "Speed Booster"}, player)
             )
            or (norfair_shortcut(state, player)))


def ridley_left_shaft_access(state: CollectionState, player: int) -> bool:
    return (has_super_missiles(state, player)
            and (can_hj_sj_ibj_or_grip(state, player) or can_walljump(state, player)
                 or state.has("Ice Beam", player) or can_bomb_block(state, player))
            and (can_traverse_heat(state, player) or hellrun(state, player, 1)
                 or (can_space_jump(state, player) and can_bomb_block(state, player)))
            )


# going the "intended" way, to the left of the elevator, down, and back to the right to get to the right shaft
def ridley_longway_right_shaft_access(state: CollectionState, player: int) -> bool:
    return (ridley_left_shaft_access(state, player)
            and (state.has("Power Grip", player)
                 and (can_hj_sj_ibj_or_grip(state, player) or can_walljump(state, player)))
            )


# taking the shortcut, to the right of the elevator and up the hole
def ridley_shortcut_right_shaft_access(state: CollectionState, player: int) -> bool:
    return (has_missiles(state, player)
            and (can_ibj(state, player)
                 or (state.has("Power Grip", player)
                     and can_bomb_block(state, player)
                     and (state.has_any({"Ice Beam", "Hi-Jump"}, player)
                          or can_space_jump(state, player)))
                 )
            )


# getting into the gap at the start of "ball room" and subsequently into the general area of ridley himself
def ridley_central_access(state: CollectionState, player: int) -> bool:
    return (
            (ridley_shortcut_right_shaft_access(state, player) or ridley_longway_right_shaft_access(state, player))
            and (can_ibj(state, player) or state.has_any({"Hi-Jump", "Power Grip"}, player))
    )


# ice/plasma beam makes dealing with the pirates a ton easier. etanks keeps you from needing to go too deep before you have
# a decent chance to survive. the rest is the strictest requirement to get in and back out of the chozo ghost area
def chozodia_ghost_from_upper_crateria_door(state: CollectionState, player: int) -> bool:
    return (
            state.has_any({"Ice Beam", "Plasma Beam"}, player) and (state.count("Energy Tank", player) >= 4)
            and has_missiles(state, player)
            and (can_walljump(state, player) or can_ibj(state, player)
                 or can_space_jump(state, player))
            and state.count("Power Bomb Tank", player) >= 2
    )


def chozodia_glass_tube_from_crateria_door(state: CollectionState, player: int) -> bool:
    return (
        # from upper door
            (state.has_any({"Ice Beam", "Plasma Beam"}, player)
             and state.count("Energy Tank", player) >= 2
             and has_missiles(state, player)
             and has_power_bombs(state, player)
             and (can_space_jump(state, player) or can_ibj(state, player)))
            # from lower door
            or (state.has_any({"Ice Beam", "Plasma Beam"}, player)
                and state.count("Energy Tank", player) >= 2
                and (can_ibj(state, player)
                     or can_space_jump(state, player)
                     or has_power_bombs(state, player)
                     )
                and has_missile_count(state, player, 6)
                and has_power_bombs(state, player)
                )
    )


# from the ruins to the save station next to the big room with all the tripwires
def chozodia_tube_to_mothership_central(state: CollectionState, player: int) -> bool:
    return (chozodia_glass_tube_from_crateria_door(state, player)
            and state.count("Energy Tank", player) >= 6
            and (can_ibj(state, player)
                 or can_space_jump(state, player)
                 or (state.has("Hi-Jump", player)
                     and (can_walljump(state, player) or state.has("Power Grip", player)))
                 )
            )


def chozodia_to_cockpit(state: CollectionState, player: int) -> bool:
    return (chozodia_tube_to_mothership_central(state, player)
            and (can_space_jump(state, player)
                 or can_ibj(state, player)
                 or (can_walljump(state, player) and state.has("Hi-Jump", player))
            )
            and (state.has("Bomb", player) or state.count("Power Bomb Tank", player) >= 2)
            )
