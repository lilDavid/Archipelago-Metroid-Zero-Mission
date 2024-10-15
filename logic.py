"""
Functions used to describe Metroid: Zero Mission logic rules
"""

from __future__ import annotations

import builtins
import functools
from typing import TYPE_CHECKING, Any, Callable, NamedTuple
from BaseClasses import CollectionState

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
CanReachLocation = lambda n: Requirement.location(n)
CanReachEntrance = lambda n: Requirement.entrance(n)

UnknownItem1 = Requirement.location("Crateria Unknown Item Statue")
UnknownItem2 = Requirement.location("Kraid Unknown Item Statue")
UnknownItem3 = Requirement.location("Ridley Unknown Item Statue")

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
    # TODO: account for Hard
    lambda world, state:
    5 * state.count("Missile Tank", world.player) + 2 * state.count("Super Missile Tank", world.player) >= n
)
SuperMissiles = SuperMissileTanks(1)
PowerBombs = PowerBombTanks(1)
PowerBombCount = lambda n: PowerBombTanks(n // 2)  # TODO: account for Hard

# Various morph/bomb rules
CanRegularBomb = all(
    MorphBall,
    Bomb
)
# Morph tunnels or bomb chains--any block that Screw Attack can't break
CanBombTunnelBlock = all(
    MorphBall,
    any(
        Bomb,
        PowerBombTanks(1),
    ),
)
CanSingleBombBlock = any(
    CanBombTunnelBlock,
    ScrewAttack
)
CanBallCannon = CanRegularBomb
CanBallspark = all(
    MorphBall,
    SpeedBooster,
    HiJump,
)
CanBallJump = all(
    MorphBall,
    any(
        Bomb,
        HiJump
    )
)
CanLongBeam = any(
    LongBeam,
    MissileCount(1),
    CanBombTunnelBlock,
)

# Logic option rules
AdvancedLogic = Requirement.setting_atleast("logic_difficulty", 1)
CanIBJ = all(
    Requirement.setting_atleast("ibj_in_logic", 1),
    CanRegularBomb,
)
CanHorizontalIBJ = all(
    CanIBJ,
    Requirement.setting_atleast("ibj_in_logic", 2)
)
CanWallJump = Requirement.setting_atleast("walljumps_in_logic", 1)
CanTrickySparks = all(
    Requirement.setting_enabled("tricky_shinesparks"),
    SpeedBooster,
)
Hellrun = lambda n: all(
    Requirement.setting_enabled("heatruns_lavadives"),
    EnergyTanks(n),
)

# Miscellaneous rules
CanFly = any(  # infinite vertical
    CanIBJ,
    SpaceJump
)
CanFlyWall = any(  # infinite vertical with a usable wall
    CanFly,
    CanWallJump
)
CanVertical = any(  # fka can_hj_sj_ibj_or_grip
    HiJump,
    PowerGrip,
    CanFly
)
CanVerticalWall = any(
    CanVertical,
    CanWallJump
)
CanHiGrip = all(
    HiJump,
    PowerGrip
)
CanEnterHighMorphTunnel = any(
    CanIBJ,
    all(
        MorphBall,
        PowerGrip
    )
)
CanEnterMediumMorphTunnel = any(
    CanEnterHighMorphTunnel,
    all(
        MorphBall,
        HiJump
    )
)
# Kraid ziplines
Ziplines = CanReachEntrance("Kraid Main -> Acid Worm Area")
ChozodiaCombat = all(
    any(
        IceBeam,
        PlasmaBeam
    ),
    EnergyTanks(4)
)
RuinsTestEscape = all(
    any(
            all(
                AdvancedLogic,
                CanHiGrip,
                CanWallJump
            ),
            CanIBJ,
            Requirement.item("Space Jump")  # Need SJ to escape, but it doesn't need to be active yet
    ),
    CanEnterMediumMorphTunnel
)

# Goal
ReachedGoal = any(
    all(
        Requirement.setting_is("goal", 0)
    ),
    all(
        Requirement.setting_is("goal", 1),
        MotherBrainBoss,
        ChozoGhostBoss
    ),
)


# Regional connection requirements

# brinstar main to past-hives, top to past-hives is different
def brinstar_past_hives():
    return all(
        MorphBall,
        Missiles,
        any(
            AdvancedLogic,
            MissileCount(10),
            SuperMissiles,
            LongBeam,
            IceBeam,
            WaveBeam,
            PlasmaBeam,
            ScrewAttack
        )
    )


def brinstar_main_to_brinstar_top():
    return any(
        all(
            CanSingleBombBlock,
            CanBallJump
        ),
        all(
            AdvancedLogic,
            IceBeam,
            CanWallJump,
            PowerBombs
        )  # truly cursed strat
    )


def brinstar_pasthives_to_brinstar_top():
    return all(
        any(
            CanFly,
            all(
                HiJump,
                IceBeam,
                CanWallJump
            )
        ),
        CanBallJump
    )

# this works for now. it's kind of tricky, cause all you need just to get there is PBs and bombs,
# but to actually do anything (including get to ship) you need IBJ/speed/sj. it only checks for speed
# for now since the only thing you'd potentially need this entrance for is Landing Site Ballspark
# (this assumption changes if/when entrance/elevator rando happens)
def brinstar_crateria_ballcannon():
    return all(
         PowerBombs,
         CanBallCannon,
         CanVertical,
         SpeedBooster
     )


# used for the items in this area as well as determining whether the ziplines can be activated
def kraid_upper_right():
    return all(
        Missiles,
        CanBallCannon,
        any(
            CanHorizontalIBJ,
            PowerGrip,
            all(
                IceBeam,
                CanBallJump
            )
        )
    )


# access to lower kraid
def kraid_left_shaft_access():
    return all(
        any(
            CanHorizontalIBJ,
            PowerGrip,
            HiJump
        ),
        CanBallJump,
        CanBombTunnelBlock,
        any(
            Ziplines,
            SpaceJump,
            all(
                GravitySuit,
                any(
                    CanTrickySparks,
                    CanIBJ
                )
            ),
            all(  # Acid Worm Skip
                AdvancedLogic,
                PowerGrip
            )
        )
    )


def kraid_left_shaft_to_bottom():
    return UnknownItem2


def kraid_bottom_to_lower_norfair():
    return all(
        ScrewAttack,
        PowerBombs,
        Missiles,
        MorphBall
    )


def norfair_main_to_crateria():
    return all(
        MorphBall,
        any(
            CanLongBeam,
            CanBallspark
        ),
        any(
            LayoutPatches,
            CanEnterMediumMorphTunnel
        )
    )


def norfair_right_shaft_access():
    return any(
        CanVertical,
        SpeedBooster
    )


def norfair_upper_right_shaft():
    return any(
        CanVerticalWall,
        IceBeam
    )


def norfair_behind_ice_beam():
    return all(
        any(
            CanLongBeam,
            WaveBeam
        ),
        MorphBall,
        any(
            all(
                PowerGrip,
                any(
                    CanWallJump,
                    SpaceJump,
                    IceBeam
                )
            ),
            CanIBJ,
            all(
                IceBeam,
                HiJump
            )
        )
    )


def norfair_behind_ice_to_bottom():
    return all(
        Missiles,
        CanBombTunnelBlock,
        any(
            PowerGrip,
            CanHorizontalIBJ,
            all(
                IceBeam,
                CanBallJump
            )
        ),
        any(
            all(
                AdvancedLogic,
                PowerBombs,
                HiJump
            ),
            all(
                PowerGrip,
                any(
                    CanWallJump,
                    SpaceJump
                )
            )
        )
    )


def norfair_lower_right_shaft():
    return any(
        ScrewAttack,
        all(
            SpeedBooster,
            any(
                CanBallCannon,
                # TODO: This does nothing. Figure out a way to make it do what you intended
                CanReachEntrance("Norfair Right Shaft -> Lower Norfair")
            )
        )
    )


def norfair_lower_right_shaft_to_lower_norfair():
    return all(
        Missiles,
        CanBombTunnelBlock,
        any(
            SpaceJump,
            CanWallJump,
            all(
                Bomb,
                any(
                    PowerGrip,
                    CanHorizontalIBJ,
                    all(
                        AdvancedLogic,
                        SuperMissiles,
                        IceBeam
                    )
                )
            ),
        ),
        any(
            VariaSuit,
            Hellrun(6)
        ),
        any(
            SpaceJump,
            CanHorizontalIBJ,
            all(
                CanSingleBombBlock,
                SpeedBooster
            )
        )
    )


def lower_norfair_to_screwattack():
    return any(
        CanTrickySparks,
        all(
            ScrewAttack,
            any(
                CanWallJump,
                SpaceJump
            )
        ),
        all(
            MissileCount(5),
            any(
                CanFlyWall,
                all(
                    AdvancedLogic,
                    IceBeam,
                    HiJump
                )
            )
        )
    )


def screw_to_lower_norfair():
    return any(
        MissileCount(4),
        ScrewAttack
    )


def lower_norfair_to_kraid():
    return all(
        ScrewAttack,
        PowerBombs,
        Missiles,
        any(
            CanIBJ,
            PowerGrip,
            all(
                HiJump,
                IceBeam
            ),
            all(
                CanTrickySparks,
                CanBallspark
            )
        )
    )


# The two items in Lower Norfair behind the Super Missile door right under the Screw Attack area
def lower_norfair_to_spaceboost_room():
    return all(
        SuperMissiles,
        any(
            SpeedBooster,
            Bomb,
            PowerBombCount(2),
            all(
                WaveBeam,
                LongBeam,
                any(
                    PowerGrip,
                    all(
                        GravitySuit,
                        HiJump
                    )
                )
            )
        ),
        CanVertical
    )


def lower_norfair_to_bottom_norfair():
    return all(
        MissileCount(2),
        SpeedBooster,
        any(
            VariaSuit,
            Hellrun(1)
        ),
        any(
            WaveBeam,
            CanTrickySparks
        ),
        CanEnterMediumMorphTunnel
    )


def bottom_norfair_to_ridley():
    return any(
        all(
            MissileCount(6),  # Covers the case where you only have Supers; 1 normal missile is enough from drops
            any(
                IceBeam,
                AdvancedLogic
            )
        ),
        PowerBombs
    )


def bottom_norfair_to_screw():
    return all(
        RidleyBoss,
        SpeedBooster,
        any(
            CanBallCannon,
            CanTrickySparks,
            AdvancedLogic
        ),
        any(
            IceBeam,
            CanVerticalWall
        )
    )


def ridley_main_to_left_shaft():
    return all(
        SuperMissiles,
        any(
            CanVerticalWall,
            IceBeam
        ),
        any(
            VariaSuit,
            Hellrun(1),
            all(
                CanFly,
                CanBombTunnelBlock
            )
        ),
        MorphBall
    )


# shortcut to the right of elevator
def ridley_main_to_right_shaft():
    return all(
        Missiles,
        any(
            CanIBJ,
            all(
                PowerGrip,
                CanBombTunnelBlock,
                any(
                    SpaceJump,
                    HiJump,
                    IceBeam
                )
            )
        )
    )


def ridley_left_shaft_to_sw_puzzle():
    return all(
        SpeedBooster,
        any(
            PowerGrip,
            SpaceJump
        ),
        any(
            PowerGrip,
            PowerBombs,
            all(
                LongBeam,
                WaveBeam
            )
        )
    )


# The alcove to the right of the right shaft
def ridley_speed_puzzles_access():
    return all(
        SpeedBooster,
        any(
            CanVerticalWall,
            IceBeam
        )
    )


# getting into the gap at the start of "ball room" and subsequently into the general area of ridley himself
def ridley_right_shaft_to_central():
    return CanEnterMediumMorphTunnel


# Ridley, Unknown 3, and the item behind Unknown 3
def ridley_central_to_ridley_room():
    return all(
        any(
            AdvancedLogic,
            all(
              MissileCount(40),
              EnergyTanks(3),
            )
        ),
        any(
            CanFly,
            all(
                IceBeam,
                CanVerticalWall
            )
        )
    )


def tourian_to_chozodia():
    return all(
        MotherBrainBoss,
        RuinsTestEscape
    )


# Getting to Unknown 1 and everything above
def crateria_main_to_crateria_upper():
    return any(
        CanBallJump,
        all(
            LayoutPatches,
            CanFly
        ),
        all(
            AdvancedLogic,
            ScrewAttack,
            any(
                SpaceJump,
                all(
                    PowerBombs,
                    CanTrickySparks,
                    CanWallJump
                )
            )
        )
    )


# Upper Crateria door to Ruins, the two items right by it, and the Triple Crawling Pirates
def crateria_upper_to_chozo_ruins():
    return all(
        PowerBombs,
        MorphBall,
        Missiles,
        any(
            CanFly,
            CanReachLocation("Crateria Northeast Corner")
        ),
        any(
            MotherBrainBoss,
            Requirement.setting_is("chozodia_access", 0)
        )
    )

# Ruins to Chozo Ghost, the three items in that general area, and the lava dive item
def chozo_ruins_to_ruins_test():
    return all(
        MorphBall,
        PowerBombs,
        any(
            Bomb,
            PowerBombCount(3)
        ),
        any(
            AdvancedLogic,
            ChozodiaCombat
        ),
        RuinsTestEscape
    )


def chozo_ruins_to_chozodia_tube():
    return any(
        all(  # Getting up to the tube is doable with just walljumps but tricky enough to be advanced imo
            AdvancedLogic,
            CanWallJump
        ),
        CanFly
    )


# Specifically getting to the room with Crateria Upper Door location. Might need another empty region for region rando
def chozodia_tube_to_chozo_ruins():
    return all(
        any(
            CanFlyWall,
            CanHiGrip
        ),
        CanBombTunnelBlock
    )


def crateria_to_under_tube():
    return all(
        PowerBombs,
        MorphBall,
        any(  # To get to the save station and warp out
            SpeedBooster,
            CanFlyWall,
            CanHiGrip
        ),
        any(
            MotherBrainBoss,
            Requirement.setting_is("chozodia_access", 0)
        )
    )


def under_tube_to_tube():
    return any(
        SpeedBooster,
        all(
            CanFly,
            PowerBombs,
            ChozoGhostBoss  # Change if basepatch makes the tube breakable before Charlie
        )
    )


def under_tube_to_crateria():
    return any(
        CanIBJ,
        all(
            PowerGrip,
            CanFlyWall
        ),
        all(
            CanTrickySparks,
            CanBallspark
        )
    )


def tube_to_under_tube():
    return all(
        ChozoGhostBoss,
        PowerBombs
    )


def chozodia_tube_to_mothership_central():
    return all(
        any(
            AdvancedLogic,
            ChozodiaCombat
        ),
        any(
            CanFly,
            all(
                CanWallJump,
                HiJump
            )
        )
    )


def mothership_central_to_cockpit():
    return all(
        any(
            Bomb,
            PowerBombCount(2)
        ),
        any(
            ScrewAttack,
            MissileCount(5)
        ),
        any(
            SuperMissiles,
            PowerGrip,
            CanFly
        ),
        any(
            AdvancedLogic,
            EnergyTanks(6)
        )
    )


def cockpit_to_original_pb():
    return all(
        any(
            CanWallJump,
            HiJump,
            PowerGrip,
            SpaceJump
        ),  # cannot IBJ to escape to cockpit
        any(
            CanIBJ,
            all(
                PowerGrip,
                any(
                    CanFlyWall,
                    HiJump
                )
            ),
            all(
                AdvancedLogic,
                IceBeam,
                CanBallJump
            )
        )
    )


def cockpit_to_mecha_ridley():
    return all(
        CanBombTunnelBlock,
        any(
            CanIBJ,
            PowerGrip,
            all(
                AdvancedLogic,
                IceBeam,
                HiJump
            )
        ),
        CanBallJump,
        any(
            PowerBombCount(2),
            all(
                Bomb,
                PowerBombs
            ),
            all(
                AdvancedLogic,
                any(
                    CanIBJ,
                    all(
                        PowerGrip,
                        any(
                            HiJump,
                            SpaceJump,
                            CanWallJump
                        )
                    )
                )
            )
        )
    )
