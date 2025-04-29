from enum import IntEnum
from typing import Mapping

from BaseClasses import Item

from .data import get_symbol


class Sprite(IntEnum):
    EnergyTank = get_symbol("sRandoEnergyTankSprite")
    MissileTank = get_symbol("sRandoMissileTankSprite")
    SuperMissileTank = get_symbol("sRandoSuperMissileTankSprite")
    PowerBombTank = get_symbol("sRandoPowerBombTankSprite")
    LongBeam = get_symbol("sRandoLongBeamSprite")
    ChargeBeam = get_symbol("sRandoChargeBeamSprite")
    IceBeam = get_symbol("sRandoIceBeamSprite")
    WaveBeam = get_symbol("sRandoWaveBeamSprite")
    UnknownPlasmaBeam = get_symbol("sRandoUnknownPlasmaBeamSprite")
    PlasmaBeam = get_symbol("sRandoPlasmaBeamSprite")
    Bomb = get_symbol("sRandoBombSprite")
    VariaSuit = get_symbol("sRandoVariaSuitSprite")
    UnknownGravitySuit = get_symbol("sRandoUnknownGravitySuitSprite")
    GravitySuit = get_symbol("sRandoGravitySuitSprite")
    MorphBall = get_symbol("sRandoMorphBallSprite")
    SpeedBooster = get_symbol("sRandoSpeedBoosterSprite")
    HiJump = get_symbol("sRandoHiJumpSprite")
    ScrewAttack = get_symbol("sRandoScrewAttackSprite")
    UnknownSpaceJump = get_symbol("sRandoUnknownSpaceJumpSprite")
    SpaceJump = get_symbol("sRandoSpaceJumpSprite")
    PowerGrip = get_symbol("sRandoPowerGripSprite")
    Nothing = get_symbol("sRandoNothingSprite")
    APLogo = get_symbol("sRandoAPLogoSprite")
    APLogoProgression = get_symbol("sRandoAPLogoProgressionSprite")
    APLogoUseful = get_symbol("sRandoAPLogoUsefulSprite")
    SpazerBeam = get_symbol("sRandoSpazerBeamSprite")
    GrappleBeam = get_symbol("sRandoGrappleBeamSprite")
    SpringBall = get_symbol("sRandoSpringBallSprite")
    XRayScope = get_symbol("sRandoXRayScopeSprite")
    ReserveTank = get_symbol("sRandoReserveTankSprite")
    WallJump = get_symbol("sRandoWallJumpSprite")
    PowerBeam = get_symbol("sRandoPowerBeamSprite")
    SpiderBall = get_symbol("sRandoSpiderBallSprite")


unknown_item_alt_sprites: Mapping[str, int] = {
    "Plasma Beam": Sprite.UnknownPlasmaBeam,
    "Space Jump": Sprite.UnknownSpaceJump,
    "Gravity Suit": Sprite.UnknownGravitySuit,
}


compatible_games: Mapping[str, Mapping[str, int]] = {
    "Super Metroid": {
        "Energy Tank": Sprite.EnergyTank,
        "Missile": Sprite.MissileTank,
        "Super Missile": Sprite.SuperMissileTank,
        "Power Bomb": Sprite.PowerBombTank,
        "Bomb": Sprite.Bomb,
        "Charge Beam": Sprite.ChargeBeam,
        "Ice Beam": Sprite.IceBeam,
        "Hi-Jump Boots": Sprite.HiJump,
        "Speed Booster": Sprite.SpeedBooster,
        "Wave Beam": Sprite.WaveBeam,
        "Spazer Beam": Sprite.SpazerBeam,
        "Spring Ball": Sprite.SpringBall,
        "Varia Suit": Sprite.VariaSuit,
        "Plasma Beam": Sprite.PlasmaBeam,
        "Grappling Beam": Sprite.GrappleBeam,
        "Morph Ball": Sprite.MorphBall,
        "Reserve Tank": Sprite.ReserveTank,
        "Gravity Suit": Sprite.GravitySuit,
        "X-Ray Scope": Sprite.XRayScope,
        "Space Jump": Sprite.SpaceJump,
        "Screw Attack": Sprite.ScrewAttack,
    },
    "SMZ3": {
        "Missile": Sprite.MissileTank,
        "Super": Sprite.SuperMissileTank,
        "PowerBomb": Sprite.PowerBombTank,
        "Grapple": Sprite.GrappleBeam,
        "XRay": Sprite.XRayScope,
        "ETank": Sprite.EnergyTank,
        "ReserveTank": Sprite.ReserveTank,
        "Charge": Sprite.ChargeBeam,
        "Ice": Sprite.IceBeam,
        "Wave": Sprite.WaveBeam,
        "Spazer": Sprite.SpazerBeam,
        "Plasma": Sprite.PlasmaBeam,
        "Varia": Sprite.VariaSuit,
        "Gravity": Sprite.GravitySuit,
        "Morph": Sprite.MorphBall,
        "Bombs": Sprite.Bomb,
        "SpringBall": Sprite.SpringBall,
        "ScrewAttack": Sprite.ScrewAttack,
        "HiJump": Sprite.HiJump,
        "SpaceJump": Sprite.SpaceJump,
        "SpeedBooster": Sprite.SpeedBooster,
        # "CardCrateriaL1":
        # "CardCrateriaL2":
        # "CardCrateriaBoss":
        # "CardBrinstarL1":
        # "CardBrinstarL2":
        # "CardBrinstarBoss":
        # "CardNorfairL1":
        # "CardNorfairL2":
        # "CardNorfairBoss":
        # "CardMaridiaL1":
        # "CardMaridiaL2":
        # "CardMaridiaBoss":
        # "CardWreckedShipL1":
        # "CardWreckedShipBoss":
        # "CardLowerNorfairL1":
        # "CardLowerNorfairBoss":
    },
    "Metroid Prime": {
        "Power Beam": Sprite.PowerBeam,
        "Ice Beam": Sprite.IceBeam,
        "Wave Beam": Sprite.WaveBeam,
        "Plasma Beam": Sprite.PlasmaBeam,
        "Missile Expansion": Sprite.MissileTank,
        # "Scan Visor":
        "Morph Ball Bomb": Sprite.Bomb,
        "Power Bomb Expansion": Sprite.PowerBombTank,
        # "Flamethrower":
        # "Thermal Visor":
        "Charge Beam": Sprite.ChargeBeam,
        # "Super Missile":
        "Grapple Beam": Sprite.GrappleBeam,
        # "X-Ray Visor":
        # "Ice Spreader":
        "Space Jump Boots": Sprite.SpaceJump,
        "Morph Ball": Sprite.MorphBall,
        # "Boost Ball":
        "Spider Ball": Sprite.SpiderBall,
        "Gravity Suit": Sprite.GravitySuit,
        "Varia Suit": Sprite.VariaSuit,
        # "Phazon Suit":
        "Energy Tank": Sprite.EnergyTank,
        # "Wavebuster":
        # "Missile Launcher":
        # "Power Bomb (Main)":
        "Progressive Power Beam": Sprite.PowerBeam,
        "Progressive Ice Beam": Sprite.IceBeam,
        "Progressive Wave Beam": Sprite.WaveBeam,
        "Progressive Plasma Beam": Sprite.PlasmaBeam,
    },
    "Super Metroid Map Rando": {
        "ETank": Sprite.EnergyTank,
        "Missile": Sprite.MissileTank,
        "Super": Sprite.SuperMissileTank,
        "PowerBomb": Sprite.PowerBombTank,
        "Bombs": Sprite.Bomb,
        "Charge": Sprite.ChargeBeam,
        "Ice": Sprite.IceBeam,
        "HiJump": Sprite.HiJump,
        "SpeedBooster": Sprite.SpeedBooster,
        "Wave": Sprite.WaveBeam,
        "Spazer": Sprite.SpazerBeam,
        "SpringBall": Sprite.SpringBall,
        "Varia": Sprite.VariaSuit,
        "Gravity": Sprite.GravitySuit,
        "XRayScope": Sprite.XRayScope,
        "Plasma": Sprite.PlasmaBeam,
        "Grapple": Sprite.GrappleBeam,
        "SpaceJump": Sprite.SpaceJump,
        "ScrewAttack": Sprite.ScrewAttack,
        "Morph": Sprite.MorphBall,
        "ReserveTank": Sprite.ReserveTank,
        "WallJump": Sprite.WallJump,
    },
}


def get_zero_mission_sprite(item: Item) -> int | None:
    if item.game not in compatible_games:
        return None

    return compatible_games[item.game].get(item.name)
