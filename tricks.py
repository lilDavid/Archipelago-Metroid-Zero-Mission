"""
Logic rules for hazard runs and tricks
"""

from .logic import *

# Normal logic default tricks
# TODO

# Advanced logic default tricks
# TODO

# Cursed tricks - Off by default, opt-in only
# TODO

# Hazard runs
BrinstarAcidNearVariaAcidDiveNormal = all(
    NormalHazardRuns,
    Energy(199)
)

BrinstarAcidNearVariaAcidDiveMinimal = all(
    MinimalHazardRuns,
    Energy(149)
)

NorfairAboveIceHellrunNormal = all(
    NormalHazardRuns,
    Energy(199)
)

NorfairAboveIceHellrunMinimal = all(
    MinimalHazardRuns,
    any(
        Energy(149),
        ScrewAttack
    )
)

NorfairUnderElevatorHellrunNormal = all(  # Note that this area is inaccessible without either Screw or Speed
    NormalHazardRuns,
    any(
        all(
            ScrewAttack,
            Energy(399)
        ),
        all(
            SpeedBooster,
            Energy(199)
        ),
        all(
            ScrewAttack,
            SpaceJump,
            Energy(299)
        )
    )
)

NorfairUnderElevatorHellrunMinimal = all(
    MinimalHazardRuns,  #TODO: In theory Hard mode can allow these to be done with less by farming in Bomb Trap room, but I'm not sure I want that on by default
    any(
        all(
            ScrewAttack,
            Energy(299),
        ),
        all(
            SpeedBooster,
            Energy(149)
        ),
        all(
            ScrewAttack,
            SpaceJump,
            Energy(249)
        )
    )
)

NorfairRightShaftToLowerHellrunNormal = all(
    NormalHazardRuns,
    any(
        Energy(449),
        all(
            any(
                CanHorizontalIBJ,
                all(
                    GravitySuit,
                    CanIBJ
                ),
            ),
            Energy(399)
        ),
        all(
            SpeedBooster,
            PowerBombs,
            Energy(349)
        ),
        all(
            SpaceJump,
            Energy(249)
        )
    )
)

NorfairRightShaftToLowerHellrunMinimal = all(  # TODO some of these can probably go lower if done by a better player
    MinimalHazardRuns,
    any(
        Energy(299),
        all(
            any(
                PowerGrip,
                CanWallJump
            ),
            SpeedBooster,
            PowerBombs,
            Energy(249)
        ),
        all(
            SpaceJump,
            Energy(199)
        )
    )
)

NorfairLavaDiveNormal = all(
    NormalHazardRuns,
    any(
        all(
            PowerGrip,
            Energy(799)
        ),
        all(
            CanHiWallJump,
            Energy(949)  # Much harder to execute well without grip, even if similar when done optimally
        ),
        all(
            VariaSuit,
            PowerGrip,
            Energy(499)
        ),
        all(
            VariaSuit,
            CanHiWallJump,
            Energy(599)
        )
    )
)

NorfairLavaDiveMinimal = all(
    MinimalHazardRuns,
    any(  # Both Grip and HiWJs are about as fast optimally
        Energy(599),  # This could maybe go down 50, but I can't do it, you need to be SO clean
        all(
            VariaSuit,
            Energy(349)
        )
    )
)

NorfairWaveHellrunLeftNormal = all(
    NormalHazardRuns,
    Energy(199)
)

NorfairWaveHellrunLeftMinimal = all(
    MinimalHazardRuns,
    Energy(149)
)

NorfairWaveHellrunRightNormal = all(
    NormalHazardRuns,
    Energy(299)
)

NorfairWaveHellrunRightMinimal = all(
    MinimalHazardRuns,
    any(
        Energy(249),
        all(
            any(
                MissileCount(4),
                ScrewAttack
            ),
            Energy(199)
        )
    )
)

LowerNorfairToRightShaftHellrunNormal = all(
    NormalHazardRuns,
    any(
        all(
            CanHorizontalIBJ,
            Energy(399)
        ),
        all(
            any(
                PowerGrip,
                HiJump,
                SpaceJump,
                CanWallJump,
                all(
                    CanIBJ,
                    any(
                        IceBeam,
                        GravitySuit
                    )
                )
            ),
            Energy(299)
        )
    )
)

LowerNorfairToRightShaftHellrunMinimal = all(
    MinimalHazardRuns,
    any(
        all(
            any(
                HiJump,
                SpaceJump
            ),
            Energy(149)
        ),
        all(
            any(
                PowerGrip,
                CanWallJump
            ),
            Energy(199)
        ),
        all(
            CanIBJ,
            IceBeam,
            Energy(249)
        ),
        all(
            any(
                CanHorizontalIBJ,
                all(
                    CanIBJ,
                    GravitySuit
                )
            ),
            Energy(299)
        )
    )
)

RidleyHellrunNormal = all(
    NormalHazardRuns,
    any(
        MissileCount(6),
        PlasmaBeam,
        Energy(199)
    )
)

RidleyHellrunMinimal = all(
    MinimalHazardRuns,
    any(
        NormalMode,  # Just tank hits
        Energy(149),
        MissileCount(6),
        PlasmaBeam
    )
)

ChozodiaEscapeLavaDiveNormal = all(
    NormalHazardRuns,
    any(
        Energy(399),
        all(
            VariaSuit,
            Energy(249)
        )
    )
)

ChozodiaEscapeLavaDiveMinimal = all(
    MinimalHazardRuns,
    any(
        Energy(299),
        all(
            VariaSuit,
            Energy(199)
        )
    )
)

ChozodiaItemLavaDiveNormal = all(
    NormalHazardRuns,
    PowerGrip,
    CanSpringBall,
    any(
        Energy(649),
        all(
            VariaSuit,
            Energy(399)
        )
    )
)

ChozodiaItemLavaDiveMinimal = all(
    MinimalHazardRuns,
    PowerGrip,
    CanSpringBall,
    any(
        Energy(499),
        all(
            VariaSuit,
            Energy(299)
        )
    )
)
