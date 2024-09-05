"""
Logic rule definitions for Metroid: Zero Mission.

Logic based on MZM Randomizer, by Biospark and dragonfangs.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from .logic import *
from worlds.generic.Rules import add_rule

if TYPE_CHECKING:
    from . import MZMWorld


brinstar_start = {
        "Brinstar Morph Ball": None,
        "Brinstar Morph Ball Cannon": CanBallCannon,
        "Brinstar Ceiling E-Tank": any(
            all(
                IceBeam,
                RidleyBoss
            ),
            CanFly,
            all(
                MorphBall,
                CanTrickySparks
            )
        ),
    }

brinstar_main = {
        "Brinstar Long Beam": all(
            MorphBall,
            any(
                CanLongBeam,
                LayoutPatches,
            )
        ),
        "Brinstar Main Shaft Left Alcove": all(
            CanSingleBombBlock,
            any(
                CanFlyWall,
                IceBeam,
                CanHiGrip
            )
        ),
        "Brinstar Ballspark": CanBallspark,
        "Brinstar Ripper Climb": any(
            all(
                CanEnterHighMorphTunnel,
                any(
                    IceBeam,
                    CanFlyWall
                )
            ),
            CanIBJ,
            all(
                CanBallspark,
                CanTrickySparks,
                CanWallJump,
                AdvancedLogic
            )
        ),
        "Brinstar Speed Booster Shortcut": all(
            any(
                CanBallspark,
                all(
                    AdvancedLogic,
                    CanBallJump
                )
            ),
            CanBombTunnelBlock,
            CanVerticalWall,
        ),
        "Brinstar Worm drop": all(
            MorphBall,
            Missiles
        ),
        "Brinstar First Missile": MorphBall,
        "Brinstar Behind Hive": all(
            MorphBall,
            Missiles),
        "Brinstar Under Bridge": all(
            Missiles,
            CanSingleBombBlock
        ),
    }

brinstar_top = {
        "Brinstar Varia Suit": all(
            any(
                SpaceJump,
                CanHorizontalIBJ,
                CanHiGrip,
                CanTrickySparks
            ),
            CanBallJump,
            any(
                CanIBJ,
                PowerGrip,
                all(
                    HiJump,
                    any(
                        CanWallJump,
                        GravitySuit
                    )
                )
            ),
            CanBombTunnelBlock
        ),
        "Brinstar Acid near Varia": all(
            any(
                SpaceJump,
                CanHorizontalIBJ,
                CanHiGrip,
                CanTrickySparks
            ),
            CanBallJump,
            CanLongBeam,
            any(
                VariaSuit,
                GravitySuit,
                Hellrun(2),
            )
        ),
        "Brinstar Upper Pillar": None
    }

brinstar_pasthives = {
        "Brinstar Post-Hive In Wall": None,
        "Brinstar Behind Bombs": all(
            CanBombTunnelBlock,
            CanBallJump
        ),
        "Brinstar Bomb": None,
        "Brinstar Post-Hive Pillar": None
    }


kraid_main = {
        "Kraid Save Room Tunnel": CanBombTunnelBlock,
        "Kraid Zipline Morph Jump": all(
            Ziplines,
            CanBallJump
        ),
        "Kraid Acid Ballspark": all(
            any(
                CanIBJ,
                HiJump,
                PowerGrip
            ),
            CanBombTunnelBlock,
            CanBallJump,
            GravitySuit,
            CanBallspark
        ),
        "Kraid Right Hall Pillar": Missiles,
        "Kraid Speed Jump": all(
            Missiles,
            SpeedBooster
        ),
        "Kraid Upper Right Morph Ball Cannon": all(
            Missiles,
            CanBallCannon
        )
    }

kraid_acidworm_area = {
        "Kraid Under Acid Worm": all(
            MissileCount(20),
            CanSingleBombBlock,
            CanVerticalWall
        ),
        "Kraid Zipline Activator Room": None
    }

# past acid worm skip
kraid_left_shaft = {
        "Kraid Behind Giant Hoppers": CanEnterHighMorphTunnel,
        "Kraid Quad Ball Cannon Room": all(
            CanBombTunnelBlock,
            Ziplines,
            Missiles
        ),  # there are some other seriously degen ways too
        "Kraid Unknown Item Statue": all(
            any(
                Bomb,
                PowerBombCount(2)
            ),
            any(
                PowerGrip,
                HiJump,
                CanIBJ,
                all(
                    IceBeam,
                    Bomb
                )
            ),
            Missiles  # required for escape - covers both cases of only hijump or only grip
        )
    }

# req either unknown 2 or norfair backdoor
# 3 locations: Unknown 2 + Speed + Kraid + Acid Fall
# Connects back to Kraid main and Norfair
kraid_bottom = {
        "Kraid Speed Booster": any(
            KraidBoss,
            SpeedBooster
        ),
        "Kraid Acid Fall": None,
        "Kraid": all(
            any(
                UnknownItem2,
                SpeedBooster
            ),
            any(
                all(
                    MissileCount(20),
                    EnergyTanks(1),
                ),
                all(
                    AdvancedLogic,
                    MissileTanks(1)
                )
            ),
            any(
                SpeedBooster,
                CanHiGrip,
                CanFlyWall
            )  # to escape, or to get to the upper door if you take the speed booster exit into the room
        )
    }

norfair_main = {
        "Norfair Hallway to Crateria": any(
            PowerGrip,
            CanIBJ,
            all(
                IceBeam,
                CanEnterMediumMorphTunnel
            )
        ),
        "Norfair Under Crateria Elevator": all(
            any(
                CanLongBeam,
                CanBallspark
            ),
            CanEnterHighMorphTunnel
        )
    }

norfair_right_shaft = {
        "Norfair Big Room": any(
            SpeedBooster,
            CanFly,
            all(
                IceBeam,
                CanVerticalWall
            ),
            all(  # this method requires some jump extends
                AdvancedLogic,
                CanHiGrip,
                CanWallJump
            )
        )
    }

norfair_upper_right = {
        "Norfair Ice Beam": None,
        "Norfair Heated Room above Ice Beam": any(
            VariaSuit,
            Hellrun(1)
        )
    }

norfair_behind_ice = {
        "Norfair Behind Top Chozo Statue": None,
    }

norfair_lowerrightshaft = {
        "Norfair Bomb Trap": all(
            any(
                Bomb,
                all(
                    SpaceJump,
                    PowerBombs
                )
            ),
            CanReachLocation("Norfair Heated Room Under Brinstar Elevator")
        ),
        "Norfair Heated Room Under Brinstar Elevator": all(
            SuperMissiles,
            any(
                VariaSuit,
                Hellrun(4),
                all(
                    SpeedBooster,
                    Hellrun(1)
                )
            )
        ),
        "Norfair Hi-Jump": Missiles,
        "Norfair Right Shaft Near Hi-Jump": all(
            CanEnterHighMorphTunnel,
            any(
                HiJump,
                CanWallJump
            )
        )
    }

lower_norfair = {
        "Norfair Lava Dive Left": all(
            MissileCount(7),
            GravitySuit,
            CanFly
        ),
        "Norfair Lava Dive Right": all(
            MissileCount(5),
            any(
                GravitySuit,
                all(
                    VariaSuit,
                    Hellrun(5)
                ),
                Hellrun(9)
            ),
            any(
                CanBombTunnelBlock,
                WaveBeam
            ),
            CanVerticalWall,
        ),
        "Norfair Wave Beam": MissileCount(4),
        "Norfair Heated Room Below Wave - Left": all(
            CanVerticalWall,
            any(
                VariaSuit,
                Hellrun(2)
            ),
            any(
                CanIBJ,
                HiJump,
                PowerGrip,
                all(
                    IceBeam,
                    Bomb
                )
            )
        ),
        "Norfair Heated Room Below Wave - Right": all(
            CanVerticalWall,
            any(
                VariaSuit,
                Hellrun(2)
            )
        ),
    }

norfair_screwattack = {
        "Norfair Screw Attack": None,
        "Norfair Next to Screw Attack": ScrewAttack,
    }

norfair_behind_superdoor = {
        "Norfair Behind Lower Super Missile Door - Left": all(
            any(
                all(
                    CanIBJ,
                    GravitySuit
                ),
                all(
                    SpaceJump,
                    PowerGrip
                ),
                all(
                    IceBeam,
                    any(
                        CanEnterMediumMorphTunnel,
                        Bomb
                    ),
                    CanReachLocation("Norfair Behind Lower Super Missile Door - Right"),
                )
            ),
            any(
                SpeedBooster,
                CanBallJump
            )
        ),
        "Norfair Behind Lower Super Missile Door - Right": any(
            CanFly,
            all(
                HiJump,
                any(
                    IceBeam,
                    all(
                        GravitySuit,
                        CanWallJump
                    )
                )
            )
        )
    }

norfair_bottom = {
        "Norfair Larva Ceiling": CanReachEntrance("Lower Norfair -> Bottom"),
        "Norfair Right Shaft Bottom": all(
            any(
                CanVerticalWall,
                IceBeam
            ),
            CanBallJump
        )
    }

ridley_main = {
        "Ridley Imago Super Missile": all(
            CanVerticalWall,
            any(
                MissileCount(20),
                all(
                    AdvancedLogic,
                    MissileTanks(1)  # Imago does not drop super refills
                ),
                ChargeBeam
            )
        )
    }

ridley_left_shaft = {
        "Ridley West Pillar": None,
        "Ridley Fake Floor": None,
        "Ridley Long Hall": None
    }

ridley_sw_puzzle = {
        "Ridley Southwest Puzzle Top": all(
            MissileCount(5),
            any(
                CanWallJump,
                PowerGrip,
                SpaceJump
            )
        ),
        "Ridley Southwest Puzzle Bottom": None
    }

ridley_right_shaft = {
        "Ridley Northeast Corner": any(
            CanFly,
            all(
                AdvancedLogic,
                CanWallJump,
                HiJump  # disable hi-jump mid walljump to get this, might be possible without
            ),
            all(
                IceBeam,
                any(
                    CanWallJump,
                    CanHiGrip
                )
            )
        )
    }

ridley_right_speed_puzzles = {
        "Ridley Bomb Puzzle": all(
            Bomb,
            PowerGrip,
            any(
                CanWallJump,
                SpaceJump
            )
        ),
        "Ridley Speed Jump": WaveBeam
    }

ridley_central = {
        "Ridley Upper Ball Cannon Puzzle": all(
            any(
                HiJump,
                all(
                    CanWallJump,
                    any(
                        PowerGrip,
                        SpaceJump
                    )
                )
            ),
            any(
                CanBallCannon,
                LayoutPatches
            )
        ),
        "Ridley Lower Ball Cannon Puzzle": all(
            any(
                PowerBombs,
                PowerGrip,
                all(
                    WaveBeam,
                    any(
                        CanWallJump,
                        SpaceJump
                    )
                )
            ),
            any(
                CanBallCannon,
                all(
                    LayoutPatches,
                    any(
                        HiJump,
                        SpaceJump,
                        CanWallJump
                    )
                )
            )
        ),
        "Ridley After Sidehopper Hall Upper": None,
        "Ridley After Sidehopper Hall Lower": None,
        "Ridley Center Pillar": None,
        "Ridley Ball Room Lower": None,
        "Ridley Ball Room Upper": all(
            SuperMissiles,
            any(
                CanFlyWall,
                CanHiGrip
            )
        ),
        "Ridley Fake Lava Under Floor": all(
            any(
                WaveBeam,
                CanBombTunnelBlock
            ),
            CanEnterHighMorphTunnel
        ),
        "Ridley Under Owls": None,
    }

ridley_room = {
        "Ridley Behind Unknown Statue": UnknownItem3,
        "Ridley Unknown Item Statue": None,
        "Ridley": UnknownItem3,
    }

tourian = {
        "Tourian Left of Mother Brain": all(
            ChozoGhostBoss,
            MotherBrainBoss,
            SpeedBooster,
            any(
                SpaceJump,
                CanTrickySparks
            )
        ),
        "Tourian Under Mother Brain": all(
            MotherBrainBoss,
            SuperMissiles,
            CanEnterMediumMorphTunnel  # to escape
        ),
        "Mother Brain": all(
            IceBeam,
            CanRegularBomb,  # only bomb can unlatch metroids
            any(
                AdvancedLogic,
                all(
                    MissileCount(40),
                    EnergyTanks(4),
                )
            ),
            CanVertical,  # to get through escape shaft
            any(  # to get to ship
                SpeedBooster,
                CanFly,
                all(
                    HiJump,
                    CanWallJump
                )
            )
        )
    }

crateria_main = {
        "Crateria Landing Site Ballspark": all(
            ChozoGhostBoss,
            MotherBrainBoss,
            CanBallspark,
            CanBallJump,
            any(
                GravitySuit,
                CanReachEntrance("Brinstar -> Crateria Ballcannon")
            )
        ),
        "Crateria Moat": None
    }

crateria_upper = {
        "Crateria Power Grip": any(
            all(
                CanVertical,
                LayoutPatches
            ),
            PowerGrip,
            CanIBJ
        ),
        "Crateria Statue Water": UnknownItem1,
        "Crateria Unknown Item Statue": None,
        "Crateria East Ballspark": all(
            CanBallspark,
            any(
                CanReachEntrance("Crateria -> Chozodia Upper Door"),
                CanReachLocation("Crateria Northeast Corner")
            )
        ),
        "Crateria Northeast Corner": all(
            SpeedBooster,
            any(
                SpaceJump,
                CanWallJump,
                CanTrickySparks
            )
        )
    }

chozodia_ruins_crateria_entrance = {
        "Chozodia Upper Crateria Door":
            CanReachEntrance("Crateria -> Chozodia Upper Door"),  # Specifically need to access this entrance, not just the region as it's one-way
        "Chozodia Ruins East of Upper Crateria Door": Missiles,
        "Chozodia Triple Crawling Pirates": all(  # Rename to Triple Crawling Pirates
            any(
                Bomb,
                PowerBombCount(2)
            ),
            any(
                CanHiGrip,
                CanFlyWall
            ),
            any(
                AdvancedLogic,
                ChozodiaCombat
            )
        ),
    }

chozodia_ruins_test = {
        "Chozodia Chozo Ghost Area Morph Tunnel Above Water": all(
            ChozoGhostBoss,  # The room leading to this item is inaccessible until the Chozo Ghost is defeated
            Missiles,
            CanBallJump
        ),
        "Chozodia Chozo Ghost Area Underwater": all(
            ChozoGhostBoss,  # This item is fake until the Chozo Ghost is defeated
            SpeedBooster,
            GravitySuit
        ),
        "Chozodia Chozo Ghost Area Long Shinespark": all(
            ChozoGhostBoss,  # The room leading to this item is inaccessible until the Chozo Ghost is defeated
            SpeedBooster,
            GravitySuit
        ),
        "Chozodia Lava Dive": all(  # TODO split this lavadive into regular/advanced? current values are close to bare minimum
            ChozoGhostBoss,
            any(
                GravitySuit,
                all(
                    Hellrun(4),
                    VariaSuit,
                    CanHiGrip
                ),
                all(
                    AdvancedLogic,
                    Hellrun(6),
                    CanHiGrip
                )
            ),
            CanEnterHighMorphTunnel,
            CanBallJump,
            any(
                CanWallJump,
                all(
                    GravitySuit,
                    CanFly
                )
            )
        ),
        "Chozo Ghost": None  # Regional access requirements should cover what is needed
    }

chozodia_under_tube = {
        "Chozodia Bomb Maze": all(
            MorphBall,
            any(
                CanIBJ,
                all(
                    CanBallspark,
                    CanTrickySparks
                ),
                all(
                    PowerGrip,
                    any(
                        CanWallJump,
                        SpaceJump
                    )
                )
            ),
            any(
                Bomb,
                PowerBombCount(3)
            ),
            CanBallJump
        ),
        "Chozodia Zoomer Maze": any(
            CanIBJ,
            all(
                PowerGrip,
                CanBallJump
            ),
            all(
                CanBallspark,
                CanTrickySparks
            )
        ),
        "Chozodia Left of Glass Tube": all(
            SpeedBooster,
            CanReachEntrance("Chozodia Glass Tube -> Chozo Ruins") # Required to access a save station after collecting to warp if necessary
        ),
        "Chozodia Right of Glass Tube": all(
            PowerBombs,
            CanFly
        )
    }

chozodia_mothership = {
        "Chozodia Pirate Pitfall Trap": all(
            Missiles,
            SuperMissiles,
            any(
                ScrewAttack,
                MissileCount(5)
            ),
            any(
                all(
                    CanBombTunnelBlock,
                    CanFlyWall
                ),
                all(
                    AdvancedLogic,  # doable without falling down using screw, but can get softlocked without infinite vertical
                    CanSingleBombBlock
                )
            )
        ),
        "Chozodia Behind Workbot": MissileCount(5),
        "Chozodia Ceiling Near Map Station": all(
            Missiles,
            any(
                PowerBombs,
                ScrewAttack,
                MissileCount(6)
            )
        ),
        "Chozodia Southeast Corner In Hull": PowerBombs
    }

chozodia_pb_area = {
        "Chozodia Original Power Bomb": None,
        "Chozodia Next to Original Power Bomb": all(
            PowerBombs,
            CanFly
        )
    }

chozodia_mecha_ridley_hall = {
    "Chozodia Under Mecha Ridley Hallway": SpeedBooster,
        "Mecha Ridley": all(
            PlasmaBeam,
            any(
                MissileCount(40),
                all(
                    AdvancedLogic,
                    Missiles,
                    any(
                        HiJump,
                        CanWallJump
                    )
                )
            ),
            CanEnterHighMorphTunnel,  # To escape
            ReachedGoal
        ),
        "Chozodia Space Pirate's Ship": MechaRidleyBoss
}

access_rules = {
        **brinstar_start,
        **brinstar_main,
        **brinstar_top,
        **brinstar_pasthives,
        **kraid_main,
        **kraid_acidworm_area,
        **kraid_left_shaft,
        **kraid_bottom,
        **norfair_main,
        **norfair_right_shaft,
        **norfair_upper_right,
        **norfair_behind_ice,
        **norfair_lowerrightshaft,
        **lower_norfair,
        **norfair_screwattack,
        **norfair_behind_superdoor,
        **norfair_bottom,
        **ridley_main,
        **ridley_left_shaft,
        **ridley_sw_puzzle,
        **ridley_right_shaft,
        **ridley_right_speed_puzzles,
        **ridley_central,
        **ridley_room,
        **tourian,
        **crateria_main,
        **crateria_upper,
        **chozodia_ruins_crateria_entrance,
        **chozodia_ruins_test,
        **chozodia_under_tube,
        **chozodia_mothership,
        **chozodia_pb_area,
        **chozodia_mecha_ridley_hall
    }


def set_rules(world: MZMWorld, locations):
    player = world.player

    for i in locations:
        location = world.multiworld.get_location(i, player)

        try:
            if access_rules[i]:
                add_rule(location, access_rules[i].create_rule(world))
        except KeyError:
            continue
