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
                any(
                    RidleyBoss,
                    HardMode
                )
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
                CanLongBeam(2),
                LayoutPatches("brinstar_long_beam_hall"),
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
        "Brinstar Ballspark": all(
            CanBallspark,
            CanBombTunnelBlock
        ),
        "Brinstar Ripper Climb": any(
            all(
                PowerGrip,
                any(
                    all(
                        IceBeam,
                        NormalMode  # On Hard, one Ripper is missing
                    ),
                    CanFlyWall
                ),
                any(
                    CanBallJump,
                    CanSingleBombBlock,
                    LayoutPatches("brinstar_top")
                )
            ),
            CanIBJ,
            all(  # Dislodging a zoomer and then freezing it along the wall to grip, springball, or bomb jump up
                AdvancedLogic,
                IceBeam,
                SuperMissiles,
                any(
                    PowerGrip,
                    all(
                        CanBallJump,
                        any(
                            NormalMode,
                            CanVerticalWall  # On Hard, one ripper is missing, so need vertical
                        )
                    )
                )
            ),
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
                    NormalLogic,
                    CanBallJump
                )
            ),
            CanBombTunnelBlock,
            CanVerticalWall,
        ),
        "Brinstar Worm Drop": all(
            MorphBall,
            Missiles
        ),
        "Brinstar First Missile": MorphBall,
        "Brinstar Behind Hive": all(
            MorphBall,
            Missiles
        ),
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
                all(
                    IceBeam,
                    NormalLogic,
                    any(
                        CanVertical,
                        CanTrickySparks
                    )
                )
            ),
            CanBallJump,
            any(
                CanHorizontalIBJ,
                PowerGrip,
                all(
                    GravitySuit,
                    CanVerticalWall
                ),
                all(
                    any(
                        Hellrun(199),
                        VariaSuit
                    ),
                    CanHiWallJump,
                    any(
                        SpaceJump,
                        AdvancedLogic
                    )
                ),
            ),
            any(
                Bomb,
                all(
                    PowerBombs,
                    NormalLogic
                )
            ),
            Missiles
        ),
        "Brinstar Acid Near Varia": all(
            any(
                SpaceJump,
                CanHorizontalIBJ,
                CanHiGrip,
                all(
                    IceBeam,
                    NormalLogic,
                    any(
                        CanVertical,
                        CanTrickySparks
                    )
                )
            ),
            CanBallJump,
            any(
                CanLongBeam(5),
                WaveBeam
            ),
            any(
                VariaSuit,
                GravitySuit,
                Hellrun(199),
            )
        ),
        "Brinstar Upper Pillar": None
    }

brinstar_pasthives = {
        "Brinstar Post-Hive in Wall": None,
        "Brinstar Behind Bombs": all(
            Missiles,
            CanBombTunnelBlock,
            CanBallJump
        ),
        "Brinstar Bomb": Missiles,
        "Brinstar Post-Hive Pillar": None
    }


kraid_main = {
        "Kraid Save Room Tunnel": CanBombTunnelBlock,
        "Kraid Zipline Morph Jump": any(
            all(
                Ziplines,
                CanBallJump
            ),
            all(  # Frame-perfect crumble shenanigans
                AdvancedLogic,
                PowerGrip,
                any(
                    HiJump,
                    SpaceJump
                )
            )
        ),
        "Kraid Acid Ballspark": all(
            any(
                CanHorizontalIBJ,
                PowerGrip,
                all(
                    HiJump,
                    NormalLogic
                )
            ),
            CanBombTunnelBlock,
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
            Missiles,
            any(
                NormalCombat,
                all(
                    MissileTanks(5),
                    EnergyTanks(1)
                )
            ),
            CanSingleBombBlock,
            CanVerticalWall
        ),
        "Kraid Zipline Activator Room": None,
        "Kraid Zipline Activator": None
    }

# past the long acid pool
kraid_left_shaft = {
        "Kraid Behind Giant Hoppers": CanEnterHighMorphTunnel,
        "Kraid Quad Ball Cannon Room": any(
            all(
                CanBombTunnelBlock,
                Ziplines,
                Missiles
            ),
            all(
                NormalLogic,
                Missiles,
                Ziplines,
                SpeedBooster,
                HiJump
            ),
            all(
                AdvancedLogic,
                Missiles,
                PowerGrip,  # Quick jumps and gripping the crumble blocks prevents them from reforming
                any(
                    HiJump,
                    SpaceJump
                )
            )
        ),
        "Kraid Unknown Item Statue": all(
            any(
                Bomb,
                PowerBombCount(4),  # nowhere good to refill PBs between elevator shaft and here
                ScrewAttack,
                all(   # space boosting to break one of the bomb blocks in the floor
                    AdvancedLogic,
                    SpeedBooster,
                    SpaceJump,
                    PowerBombCount(3)
                ),
                all(  # going past, through the "T room" with the short zipline to refill your 2 PBs, then come back
                    AdvancedLogic,
                    Missiles,
                    any(
                        all(
                            Ziplines,
                            CanBallJump
                        ),
                        PowerGrip,  # crumble shenanigans
                    )
                )
            ),
            any(  # To enter the morph tunnel to leave after getting the item on the statue
                PowerGrip,
                HiJump,
                CanIBJ,
                all(
                    IceBeam,
                    Bomb
                )
            ),
        )
    }

kraid_bottom = {
        "Kraid Speed Booster": any(
            KraidBoss,
            all(
                NormalLogic,
                SpeedBooster
            )
        ),
        "Kraid Acid Fall": None,
        "Kraid": all(
            any(
                UnknownItem2,
                all(
                    NormalLogic,
                    SpeedBooster
                )
            ),
            Missiles,
            KraidCombat,
            any(  # to escape, or to get to the upper door if you take the speed booster exit into the room
                SpeedBooster,
                CanHiGrip,
                CanFlyWall
            ),
            any(  # to escape via the bottom right shaft
                LayoutPatches("kraid_right_shaft"),
                SpeedBooster,
                CanFly,
                all(
                    NormalLogic,
                    IceBeam,
                    any(
                        CanWallJump,
                        PowerGrip
                    )
                ),
                all(
                    AdvancedLogic,
                    CanHiWallJump
                )
            )
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
                CanLongBeam(1),
                CanBallspark
            ),
            any(
                CanEnterHighMorphTunnel,
                all(
                    NormalLogic,
                    IceBeam,
                    any(
                        HiJump,
                        all(
                            Bomb,
                            CanWallJump
                        )
                    )
                )
            )
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
            all(
                NormalLogic,
                CanHiGrip,
                CanWallJump
            )
        )
    }

norfair_upper_right = {
        "Norfair Ice Beam": any(
            CanFlyWall,
            PowerGrip,
            all(
                IceBeam,
                HardMode
            ),
            all(
                HiJump,
                AdvancedLogic
            )
        ),
        "Norfair Heated Room Above Ice Beam": any(
            VariaSuit,
            Hellrun(199)
        )
    }

norfair_behind_ice = {
        "Norfair Behind Top Chozo Statue": None,
    }

norfair_under_brinstar_elevator = {
        "Norfair Bomb Trap": all(
            any(
                Bomb,
                all(
                    PowerBombs,
                    any(
                        SpaceJump,
                        NormalLogic  # Placing a PB in a specific place by the door hits only the top bomb chain
                    )
                )
            ),
            CanReachLocation("Norfair Heated Room Under Brinstar Elevator")
        ),
        "Norfair Heated Room Under Brinstar Elevator": all(
            SuperMissiles,
            any(  # TODO: Redo this hellrun; Hard mode has extra considerations
                VariaSuit,
                Hellrun(499),
                all(
                    SpeedBooster,
                    Hellrun(199)
                )
            )
        ),
}

norfair_lowerrightshaft = {
        "Norfair Hi-Jump": Missiles,
        "Norfair Right Shaft Near Hi-Jump": any(
            CanIBJ,
            CanHiGrip,
            all(
                SpaceJump,
                PowerGrip
            ),
            all(
                PowerGrip,
                CanWallJump,
                NormalLogic
            ),
            CanReachEntrance("Norfair Bottom -> Norfair Lower Right Shaft")
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
                    Hellrun(599)
                ),
                Hellrun(999)
            ),
            any(
                CanBombTunnelBlock,
                WaveBeam
            ),
            any(
                all(
                    GravitySuit,
                    CanVerticalWall
                ),
                PowerGrip,
                CanHiWallJump
            )
        ),
        "Norfair Wave Beam": MissileCount(4),
        "Norfair Heated Room Below Wave - Left": all(
            CanVerticalWall,
            any(
                VariaSuit,
                Hellrun(299)
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
                Hellrun(299)
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
                    any(
                        GravitySuit,
                        all(
                            NormalLogic,
                            HiJump
                        )
                    )
                ),
                all(
                    SpaceJump,
                    PowerGrip
                ),
                all(
                    NormalLogic,
                    IceBeam,
                    any(
                        CanEnterMediumMorphTunnel,
                        Bomb
                    ),
                    CanReachLocation("Norfair Behind Lower Super Missile Door - Right"),
                ),
                all(
                    NormalLogic,
                    GravitySuit,
                    CanHiGrip,
                    CanWallJump
                )
            ),
            any(  # To get out
                LayoutPatches("norfair_behind_superdoor"),
                SpeedBooster,
                CanBallJump
            )
        ),
        "Norfair Behind Lower Super Missile Door - Right": any(
            SpaceJump,
            CanHorizontalIBJ,
            all(
                GravitySuit,
                CanIBJ
            ),
            all(
                IceBeam,
                CanWallJump
            ),
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
        "Norfair Right Shaft Bottom": any(
            # going from the right "stairs"
            all(
                any(
                    CanVerticalWall,
                    IceBeam
                ),
                CanBallJump
            ),
            # using the shot blocks to the left
            all(
                NormalLogic,
                Missiles,
                PowerGrip,
                any(
                    CanFlyWall,
                    IceBeam
                )
            )
        )
    }

ridley_main = {
        "Ridley Imago Super Missile": all(
            CanVerticalWall,
            any(
                all(
                    MissileTanks(7),
                    EnergyTanks(1)
                ),
                all(
                    NormalCombat,
                    MissileTanks(4),
                ),
                all(
                    MinimalCombat,
                    any(
                        MissileTanks(1),
                        SuperMissileCount(8)
                    )
                ),
                ChargeBeam
            )
        )
    }

ridley_left_shaft = {
        "Ridley West Pillar": None,
        "Ridley Fake Floor": any(
            CanBombTunnelBlock,  # the long way
            CanFly,  # the short way
            all(
                AdvancedLogic,
                any(
                    CanWallJump,
                    PowerGrip
                )
            )
        ),
    }

ridley_sw_puzzle = {
        "Ridley Southwest Puzzle Top": all(
            CanReachLocation("Ridley Southwest Puzzle Bottom"),
            MissileCount(5),
            any(
                CanWallJump,
                PowerGrip,
                SpaceJump
            )
        ),
        "Ridley Southwest Puzzle Bottom": all(
            SpeedBooster,
            MorphBall,
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
            ),
            Missiles,
            any(
                PowerGrip,
                all(
                    AdvancedLogic,
                    any(
                        SpaceJump,
                        CanWallJump
                    )
                )
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
    }

ridley_right_shaft = {
        "Ridley Long Hall": None,
        "Ridley Northeast Corner": any(
            CanFly,
            all(
                AdvancedLogic,
                CanHiWallJump  # disable hi-jump mid walljump to get this, might be possible without
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
            any(
                PowerGrip,
                all(
                    AdvancedLogic,
                    HiJump,
                    CanHorizontalIBJ
                )
            ),
            any(
                all(
                    Bomb,
                    any(
                        CanWallJump,
                        SpaceJump
                    )
                ),
                all(
                    AdvancedLogic,
                    PowerBombCount(2),
                    HiJump
                )
            )
        ),
        "Ridley Speed Jump": WaveBeam
    }

ridley_central = {
        "Ridley Upper Ball Cannon Puzzle": all(
            any(
                HiJump,
                CanIBJ,
                all(
                    PowerGrip,
                    any(
                        CanWallJump,
                        SpaceJump,
                        all(  # A well-placed bomb and well-timed unmorph will grab the ledge
                            NormalLogic,
                            Bomb
                        )
                    )
                )
            ),
            any(
                CanBallCannon,
                LayoutPatches("ridley_ballcannon")
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
                    LayoutPatches("ridley_ballcannon"),
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
            ),
            any(
                Bomb,
                PowerBombCount(3)
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
                NormalLogic
            )
        ),
        "Tourian Under Mother Brain": all(
            ChozoGhostBoss,
            MotherBrainBoss,
            SuperMissiles,
            CanEnterMediumMorphTunnel  # to escape
        ),
        "Mother Brain": all(
            IceBeam,
            any(
                Bomb,  # only bomb can unlatch metroids
                NormalCombat  # or just don't get hit!
            ),
            MotherBrainCombat,
            any(  # to get through the tunnel right before Mother Brain
                CanEnterHighMorphTunnel,
                all(
                    CanWallJump,
                    NormalLogic,
                ),
                AdvancedLogic  # it is possible to freeze Rinkas in such a way that you don't need grip IBJ or walljumps
            ),
            any(  # to get through escape shaft
                all(
                    NormalMode,
                    CanVertical,
                ),
                any(  # Hard mode escape; much tighter time so IBJs alone don't cut it
                    SpaceJump,
                    HiJump,
                    all(
                        PowerGrip,
                        CanWallJump
                    ),
                    all(
                        AdvancedLogic,
                        CanIBJ,
                        CanWallJump
                    )
                ),
                all(
                    AdvancedLogic,  # running into MB after the final hit to get a speed boost
                    SpeedBooster,
                    CanWallJump
                )
            ),
            any(  # to get to ship
                SpeedBooster,
                CanFly,
                all(
                    NormalLogic,
                    CanHiWallJump
                )
            )
        )
    }

crateria_main = {
        "Crateria Landing Site Ballspark": all(
            CanBallspark,
            PowerBombs,
            any(
                all(
                    GravitySuit,
                    ChozoGhostBoss
                ),
                CanReachEntrance("Brinstar -> Crateria Ballcannon")
            )
        ),
        "Crateria Moat": None
    }

crateria_upper = {
        "Crateria Power Grip": all(
            CanBallJump,
            any(
                all(
                    CanVertical,
                    LayoutPatches("crateria_left_of_grip")
                ),
                CanEnterHighMorphTunnel
            )
        ),
        "Crateria Statue Water": UnknownItem1,
        "Crateria Unknown Item Statue": CanBallJump,
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
        "Chozodia Triple Crawling Pirates": all(
            Missiles,
            PowerBombCount(2),  # 2 PBs ALWAYS required at minimum, but you may need many more
            any(
                all(
                    Bomb,
                    any(
                        NormalMode,
                        PowerBombCount(3)  # on Hard a save room is disabled, so you cannot refill PBs, requiring more
                    )
                ),
                PowerBombCount(7),  # Hard, no refills, only PBs, no ability to skip any bomb chains
                all(
                    NormalMode,
                    PowerBombCount(5),  # no skipping bomb reqs, but with refills
                ),
                all(  # Skips one PB on either the slow-crumble morph tunnel or the bomb chain after
                    any(
                        PowerBombCount(6),
                        all(
                            NormalMode,
                            PowerBombCount(4)
                        )
                    ),
                    any(
                        ScrewAttack,
                        WaveBeam,
                        CanFlyWall
                    ),
                    NormalLogic
                ),
                all(  # Skips both but still only PBs
                    any(
                        ScrewAttack,
                        WaveBeam
                    ),
                    CanFlyWall,
                    NormalLogic,
                    any(
                        PowerBombCount(5),
                        all(
                            NormalMode,
                            PowerBombCount(3)
                        )
                    )
                ),
            ),
            any(
                CanHiGrip,
                CanFlyWall,
                all(
                    NormalLogic,
                    IceBeam
                )
            ),
            ChozodiaCombat
        )
    }

chozodia_ruins_test = {
        "Chozodia Chozo Ghost Area Morph Tunnel Above Water": all(
            MissileCount(3),
            CanBallJump,
            any(
                all(  # Going up through the water
                    any(
                        CanWallJump,
                        all(
                            GravitySuit,
                            CanFly
                        ),
                    ),
                    any(
                        ScrewAttack,
                        NormalLogic  # Skipping the screw attack wall with the missile tunnel
                    )
                ),
                all(  # Going up from the Triple Crawling Pirates room
                    NormalLogic,
                    CanFlyWall
                )
            )
        ),
        "Chozodia Chozo Ghost Area Underwater": all(
            Missiles,
            SpeedBooster,
            GravitySuit
        ),
        "Chozodia Chozo Ghost Area Long Shinespark": all(
            Missiles,
            SpeedBooster,
            GravitySuit,
            any(  # IBJ is too slow to keep charge
                SpaceJump,
                CanWallJump
            ),
            any(
                ScrewAttack,
                all(
                    AdvancedLogic,  # You need to be very fast to keep the charge going this way
                    MissileCount(3)
                )
            )
        ),
        "Chozodia Lava Dive": all(  # TODO redo this whole lava dive
            any(
                ScrewAttack,
                all(
                    Missiles,
                    any(
                        Bomb,
                        PowerBombCount(2)
                    )
                )
            ),
            any(
                GravitySuit,
                all(
                    Hellrun(499),
                    VariaSuit,
                    CanHiGrip
                ),
                all(
                    AdvancedLogic,
                    Hellrun(699),
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
        "Chozo Ghost": all(
            MotherBrainBoss,
            RuinsTestEscape
        )
    }

chozodia_under_tube = {
        "Chozodia Bomb Maze": all(
            MorphBall,
            any(
                CanIBJ,
                all(
                    CanBallspark,
                    NormalLogic
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
                NormalLogic
            )
        ),
        "Chozodia Left of Glass Tube": all(
            SpeedBooster,
            CanReachEntrance("Chozodia Glass Tube -> Chozo Ruins") # Required to access a save station after collecting to warp if necessary
        ),
        "Chozodia Right of Glass Tube": all(
            PowerBombs,
            any(
                CanFly,
                all(
                    NormalLogic,
                    SpeedBooster,
                    CanVerticalWall
                )
            )
        )
    }

chozodia_upper_mothership = {
        "Chozodia Pirate Pitfall Trap": all(
            Missiles,
            any(
                SuperMissiles,
                all(
                    CanReachEntrance("Chozodia Upper Mothership -> Deep Mothership"),
                    PowerBombs
                )
            ),
            any(
                all(
                    CanBombTunnelBlock,
                    CanFlyWall
                ),
                all(
                    NormalLogic,  # doable without falling down using screw or by leaving the room then returning
                    CanSingleBombBlock
                )
            )
        ),
        "Chozodia Behind Workbot": all(
            Missiles,
            any(
                CanFly,
                CanHiGrip,
                CanHiWallJump
            )
        )
    }

chozodia_lower_mothership = {
        "Chozodia Ceiling Near Map Station": Missiles,
        "Chozodia Southeast Corner in Hull": all(
            any(
                SuperMissiles,
                any(
                    Bomb,
                    PowerBombCount(2)
                ),
            ),
            CanVerticalWall,
            PowerBombs
        )
}

chozodia_pb_area = {
        "Chozodia Original Power Bomb": None,
        "Chozodia Next to Original Power Bomb": all(
            any(
                Bomb,
                PowerBombCount(3)
            ),
            CanFly
        )
    }

chozodia_mecha_ridley_hall = {
        "Chozodia Under Mecha Ridley Hallway": SpeedBooster,
        "Mecha Ridley": all(
            MechaRidleyCombat,
            CanEnterHighMorphTunnel,
            CanBallJump,
            PlasmaBeam,  # To defeat black pirates
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
        **norfair_under_brinstar_elevator,
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
        **chozodia_upper_mothership,
        **chozodia_lower_mothership,
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


# Regional connection requirements

# brinstar main to past-hives, top to past-hives is different
def brinstar_past_hives():
    return all(
        MorphBall,
        Missiles,
        any(
            NormalCombat,
            MissileCount(10),
            SuperMissiles,
            LongBeam,
            ChargeBeam,
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
        )
    )


def brinstar_pasthives_to_brinstar_top():
    return all(
        any(
            CanFly,
            all(
                IceBeam,
                CanHiWallJump
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
         CanVerticalWall,
         SpeedBooster
     )


# used for the items in this area as well as determining whether the ziplines can be activated
def kraid_upper_right():
    return all(
        Missiles,
        CanBallCannon,
        any(  # Getting to the top of the right shaft
            CanFlyWall,
            PowerGrip,
            all(
                AdvancedLogic,
                HiJump  # Balljumps can get you up there using the crevices, but it's pretty tight
            )
        ),
        any(  # Getting up to the top door of the right shaft
            CanVertical,
            all(  # Freezing a zeela to get just enough height to WJ up. You might have to wait a while for it though
                NormalLogic,
                IceBeam,
                CanWallJump
            )
        ),
        any(  # Getting through the hole in the next room
            CanHorizontalIBJ,
            PowerGrip,
            all(
                IceBeam,
                CanBallJump
            ),
            all(
                GravitySuit,
                CanIBJ
            ),
            all(
                NormalLogic,
                any(
                    Hellrun(99),
                    VariaSuit
                ),
                HiJump,
                CanIBJ
            )
        )
    )


# access to lower kraid
def kraid_left_shaft_access():
    return all(
        any(
            CanHorizontalIBJ,
            PowerGrip,
            all(
                GravitySuit,
                CanIBJ
            ),
            all(
                NormalLogic,
                HiJump
            ),
            all(  # weird, tight rising midair morph
                SpaceJump,
                AdvancedLogic
            )
        ),
        CanBallJump,
        CanBombTunnelBlock,
        any(
            Ziplines,
            SpaceJump,
            all(
                GravitySuit,
                any(
                    CanIBJ,
                    all(
                        CanTrickySparks,
                        any(
                            HiJump,
                            CanWallJump
                        )
                    )
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
        NormalLogic,
        ScrewAttack,
        PowerBombs,
        Missiles,
        MorphBall
    )


def norfair_main_to_crateria():
    return all(
        MorphBall,
        any(
            CanLongBeam(1),
            CanBallspark
        ),
        any(
            LayoutPatches("crateria_water_speedway"),
            CanEnterMediumMorphTunnel
        )
    )


def norfair_right_shaft_access():
    return any(
        CanVertical,
        SpeedBooster,
        all(
            SuperMissiles,
            IceBeam,
            CanWallJump,
            AdvancedLogic
        )
    )


def norfair_upper_right_shaft():
    return any(
        CanVerticalWall,
        IceBeam
    )


def norfair_behind_ice_beam():
    return all(
        CanReachLocation("Norfair Ice Beam"),
        any(
            CanLongBeam(1),
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
                HiJump,
                any(
                    NormalMode,
                    CanWallJump,
                    AdvancedLogic  # Finicky enemy freeze to get up the triple ripper room with just HJ on Hard
                )
            )
        )
    )


def norfair_behind_ice_to_bottom():
    return all(
        NormalLogic,
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
            CanIBJ,
            all(
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


def norfair_shaft_to_under_elevator():
    return any(
        SpeedBooster,
        all(
            ScrewAttack,
            any(
                CanFlyWall,
                CanHiGrip
            )
        )
    )


# under elevator to lower right shaft
def norfair_lower_right_shaft():
    RightShaftNearHiJumpRule = norfair_lowerrightshaft.get("Norfair Right Shaft Near Hi-Jump")
    LowerNorfairAccess = norfair_lower_right_shaft_to_lower_norfair()
    return any(
        all(
            ScrewAttack,
            any(
                CanFlyWall,
                CanHiGrip
            )
        ),
        all(
            SpeedBooster,
            any(  # escape
                all(
                    RightShaftNearHiJumpRule,  # shorthand for accessing that area of the room
                    any(
                        Missiles,
                        CanVertical
                    ),
                    CanBallCannon,
                ),
                # to reach a save station and warp out
                LowerNorfairAccess
            )
        )
    )


def norfair_lower_shaft_to_under_elevator():
    return all(
        ScrewAttack,
        any(
            CanFlyWall,
            CanHiGrip
        )
    )


def norfair_lower_right_shaft_to_lower_norfair():
    return all(
        Missiles,
        CanBombTunnelBlock,
        any(
            SpaceJump,
            CanWallJump,
            CanHorizontalIBJ,
            all(
                GravitySuit,
                CanHiGrip
            ),
            all(
                any(
                    HiJump,
                    PowerGrip,
                    CanIBJ
                ),
                any(
                    PowerGrip,
                    CanHorizontalIBJ,
                    all(
                        AdvancedLogic,
                        IceBeam
                    )
                )
            ),
        ),
        any(
            VariaSuit,
            Hellrun(699)
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
        all(
            ScrewAttack,
            any(
                CanWallJump,
                SpaceJump
            )
        ),
        all(
            NormalLogic,
            MissileCount(5),
            any(
                CanFlyWall,
                all(
                    AdvancedLogic,
                    IceBeam,
                    HiJump
                )
            )
        ),
        all(
            NormalLogic,
            SpeedBooster
        )
    )


# This is necessary if your only way to the Screw Attack region is the ballcannon near the Ridley elevator
def screw_to_lower_norfair():
    return any(
        MissileCount(4),
        ScrewAttack
    )


def lower_norfair_to_kraid():
    return all(
        NormalLogic,
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
                AdvancedLogic,
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
            Hellrun(199)
        ),
        any(
            WaveBeam,
            all(
                CanTrickySparks,
                any(
                    NormalMode,
                    ScrewAttack  # Hard mode adds extra enemies to the hardest room for this spark
                )
            ),
        ),
        CanEnterMediumMorphTunnel,
        any(  # defeating the larvae
            PowerBombCount(2),
            all(
                PowerBombs,
                any(
                    PlasmaBeam,
                    Bomb
                )
            ),
            all(
                WaveBeam,
                any(
                    CanBallJump,
                    LayoutPatches("norfair_larvae_room")
                ),
                any(
                    PlasmaBeam,
                    CanBombTunnelBlock
                )
            ),
            all(
                AdvancedLogic,
                Missiles,  # you can defeat the first larva by jumping and shooting 2 missiles up against the ceiling
                any(
                    CanBallJump,
                    LayoutPatches("norfair_larvae_room")
                ),
                any(
                    PlasmaBeam,
                    CanBombTunnelBlock
                ),
            )
        )
    )


# Needed for Kraid -> Norfair shortcut, so this rule is for getting to Hi-Jump location from that entrance
def lower_norfair_to_lower_right_shaft():
    return all(
        CanVerticalWall,
        CanBombTunnelBlock,
        any(
            VariaSuit,
            Hellrun(299)  # TODO: may be possible with even just 1
        )
    )


def bottom_norfair_to_lower_shaft():
    BottomShaftLocationRule = norfair_bottom.get("Norfair Right Shaft Bottom")
    return any(
        all(
            Missiles,
            BottomShaftLocationRule,
            any(
                CanBombTunnelBlock,
                WaveBeam
            ),
            CanFlyWall,
            any(
                PowerGrip,
                CanIBJ
            )
        ),
        all(
            SpeedBooster,
            NormalLogic
        ),
    )


def bottom_norfair_to_ridley():
    return any(
        all(
            any(
                MissileCount(20),
                SuperMissileCount(8),
                all(
                    NormalCombat,
                    any(
                        MissileTanks(1),
                        SuperMissileCount(6),
                    )
                )
            ),
            any(
                IceBeam,
                SpaceJump,
                NormalLogic
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
            NormalLogic
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
            Hellrun(199),
            all(
                CanFly,
                CanBombTunnelBlock
            )
        ),
        MorphBall,
        any(
            NormalCombat,
            EnergyTanks(2),
            VariaSuit,
            GravitySuit
        )
    )


# shortcut to the right of elevator
def ridley_main_to_right_shaft():
    return all(
        NormalLogic,
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
        ),
        any(
            NormalCombat,
            EnergyTanks(2),
            VariaSuit,
            GravitySuit
        )
    )


def ridley_left_shaft_to_sw_puzzle():
    return all(
        SpeedBooster,
        any(
            CanVerticalWall,
            IceBeam
        )
    )


# The alcove to the right of the right shaft
def ridley_speed_puzzles_access():
    return all(
        SpeedBooster,
        CanVerticalWall
    )


# getting into the gap at the start of "ball room" and subsequently into the general area of ridley himself
def ridley_right_shaft_to_central():
    return CanEnterMediumMorphTunnel


def ridley_right_shaft_to_left_shaft():
    return any(
        CanIBJ,
        all(
            SpaceJump,
            PowerGrip
        ),
        all(
            PowerGrip,
            CanWallJump,
            CanTrickySparks
        )
    )


# Ridley, Unknown 3, and the item behind Unknown 3
def ridley_central_to_ridley_room():
    return all(
        any(
            Missiles,
            ChargeBeam  # Fun fact! you can kill the eye door with charge beam
        ),
        RidleyCombat,
        any(
            CanFly,
            all(
                IceBeam,
                CanVerticalWall
            )
        )
    )


# TODO: What to do about this only being one-time? It may matter in very rare cases
def tourian_to_chozodia():
    return all(
        MotherBrainBoss,
        RuinsTestEscape
    )


# Getting above the Unknown Item block
def crateria_main_to_crateria_upper():
    return any(
        CanBallJump,
        all(
            CanFly,
            any(
                all(
                    PowerBombs,
                    SpeedBooster,
                    GravitySuit
                ),
                all(
                    NormalLogic,  # not in Simple level logic because this requires meta knowledge of the rando
                    LayoutPatches("crateria_water_speedway")
                )
            ),
            any(
                LayoutPatches("crateria_left_of_grip"),
                CanEnterHighMorphTunnel
            )
        ),
        all(  # Shinespark up landing site
            any(
                PowerBombs,
                LayoutPatches("crateria_water_speedway")
            ),
            SpeedBooster,
            GravitySuit,
            any(
                LayoutPatches("crateria_left_of_grip"),
                CanEnterHighMorphTunnel
            ),
            any(  # Getting across the Power Grip climb; going down softlocks because of room state nonsense
                CanFly,
                all(
                    NormalLogic,  # Tight jump
                    CanHiGrip
                )
            )
        ),
        all(
            NormalLogic,
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
            all(
                AdvancedLogic,
                CanHiWallJump,
                PowerGrip
            ),
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
        PowerBombCount(2),  # 2 PBs ALWAYS required at minimum, but you may need many more
        any(
            all(
                Bomb,
                any(
                    NormalMode,
                    PowerBombCount(4)  # on Hard a save room is disabled, so you cannot refill PBs, requiring more
                )
            ),
            PowerBombCount(8),
            all(
                NormalMode,
                PowerBombCount(5),
            ),
            all(  # Skips one PB on the slow-crumble morph tunnel
                any(
                    PowerBombCount(7),
                    all(
                        NormalMode,
                        PowerBombCount(4)
                    )
                ),
                any(
                    ScrewAttack,
                    WaveBeam
                ),
                NormalLogic
            ),
            all(  # Skips the Triple Crawling Pirates room and a bomb chain but doesn't skip the crumble tunnel
                any(
                    PowerBombCount(5),  # Saves 2 on Hard
                    all(
                        NormalMode,
                        PowerBombCount(4),  # Only saves 1 on Normal because you can refill
                    )
                ),
                CanFlyWall,
                MissileCount(3),
                Missiles,
                NormalLogic
            ),
            all(  # Skips everything possible, but still only PBs
                CanFlyWall,
                any(
                    ScrewAttack,
                    WaveBeam
                ),
                Missiles,
                PowerBombCount(4),  # technically should be 3 on Normal, but Normal can't have 3 max without having 4
                NormalLogic
            )
        ),
        CanVerticalWall,
        ChozodiaCombat,
    )


#  Potentially useful for closed Chozodia in cases where post-MB you still can't access parts of Chozodia from Crateria
def ruins_test_to_ruins():
    return all(
        ChozoGhostBoss,
        RuinsTestEscape,
        any(
            all(  # Through the lava
                any(
                    CanWallJump,
                    all(
                        GravitySuit,
                        CanFly
                    )
                ),
                any(
                    ScrewAttack,
                    all(
                        NormalLogic,
                        Missiles,
                        any(
                            Bomb,
                            PowerBombCount(2)
                        )
                    )
                ),
                any(
                    GravitySuit,
                    all(
                        Hellrun(249),
                        VariaSuit
                    ),
                    Hellrun(399)
                )
            ),
            all(  # Or going all the way back through the ruins
                NormalLogic,
                any(
                    PowerBombCount(4),
                    all(
                        Bomb,
                        PowerBombCount(2)
                    )
                ),
                CanFlyWall,
                ScrewAttack
            )
        )
    )


def chozo_ruins_to_chozodia_tube():
    return any(
        all(
            NormalLogic,
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
        any(
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
            PowerBombs
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
            NormalLogic,
            CanBallspark
        )
    )


def tube_to_under_tube():
    return any(
        PowerBombCount(3),  # most paths here require breaking a bomb chain on the way here and back
        all(
            Bomb,
            PowerBombs
        )
    )


def chozodia_tube_to_mothership_central():
    return all(
        ChozodiaCombat,
        any(
            CanFly,
            CanHiWallJump,
            all(
                NormalLogic,
                IceBeam
            )
        )
    )


# access to the map station
def mothership_central_to_lower():
    return all(
        any(
            PowerBombCount(2),
            all(
                Bomb,
                PowerBombs
            )
        ),
        any(  # Getting to the save room
            Missiles,
            all(
                any(
                    HiJump,
                    all(
                        NormalLogic,
                        IceBeam
                    )
                ),
                any(
                    PowerGrip,
                    CanWallJump
                )
            ),
            all(
                NormalLogic,
                HiJump,
                IceBeam
            ),
            CanFly
        )
    )


# accessing the missile door just under the Behind Workbot item
def mothership_central_to_upper():
    return all(
        Missiles,
        any(
            Bomb,
            PowerBombCount(2)
        ),
        any(
            all(
                ScrewAttack,
                any(
                    CanWallJump,
                    SpaceJump,
                    all(
                        HiJump,
                        any(
                            PowerGrip,
                            CanIBJ
                        )
                    )
                )
            ),
            all(
                MissileCount(5),
                any(
                    CanFly,
                    CanHiGrip,
                    CanHiWallJump,
                    all(
                        NormalLogic,
                        IceBeam,
                        CanVerticalWall
                    )
                )
            ),
            # the low% way
            all(
                any(
                    MissileCount(4),
                    ScrewAttack
                ),
                any(
                    CanFly,
                    CanHiGrip,
                    CanHiWallJump
                ),
                any(
                    Bomb,
                    PowerBombCount(3)
                ),
                any(
                    ScrewAttack,
                    MissileCount(5),
                    Bomb,
                    PowerBombCount(4)
                )
            )
        )
    )


def mothership_lower_to_upper():
    return all(
        CanBombTunnelBlock,
        any(
            CanFly,
            CanHiGrip,
            CanHiWallJump  # HJWJ required to get from the blue ship to the room under workbot; just WJ doesn't work
        )
    )


# the long way around - in case you don't have enough PBs
def mothership_upper_to_lower():
    return all(
        any(
            CanFlyWall,
            CanHiGrip
        ),
        any(
            all(
                NormalMode,
                MissileCount(2),
                CanBombTunnelBlock
            ),
            all(
                MissileCount(4),
                Bomb  # On Hard, you'd need 2 PBs to go this way, so the more direct central -> lower route is better
            )
        )
    )


# to the room right past Pirate Pitfall Trap
def mothership_upper_to_deep_mothership():
    return any(
        all(
            Missiles,
            any(
                CanFly,
                all(
                    AdvancedLogic,  # very tight midair morph
                    CanHiWallJump
                )
            )
        ),
        # shortcut, going through Pirate Pitfall Trap
        all(
            SuperMissiles,
            PowerBombs,
            any(
                CanFlyWall,
                NormalLogic  # Leave and return to the room after PBing, the bomb blocks never reform
            )
        )
    )


def deep_mothership_to_cockpit():
    return all(
        CanFlyWall,
        any(
            Bomb,
            PowerBombCount(4)
        ),
        ChozodiaCombat
    )


def cockpit_to_original_pb():
    return all(
        any(  # cannot IBJ to escape to cockpit
            CanWallJump,
            HiJump,
            PowerGrip,
            SpaceJump
        ),
        any(
            Bomb,
            PowerBombCount(2)
        ),
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
            all(
                PowerBombs,
                CanVertical
            ),
            CanIBJ,
            PowerGrip,
            all(
                NormalLogic,
                IceBeam
            )
        ),
        any(
            CanBallJump,
            PowerGrip
        ),
        any(
            all(
                PowerBombs,
                any(
                    Bomb,
                    PowerBombCount(2),
                    all(
                        NormalLogic,
                        MissileCount(4)
                    )
                ),
            ),
            all(
                NormalLogic,
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
