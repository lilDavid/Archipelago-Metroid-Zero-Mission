from enum import StrEnum
from typing import Mapping

from BaseClasses import Item

from .data import get_symbol


class Sprite(StrEnum):
    EnergyTank = "Energy Tank"
    MissileTank = "Missile Tank"
    SuperMissileTank = "Super Missile Tank"
    PowerBombTank = "Power Bomb Tank"
    LongBeam = "Long Beam"
    ChargeBeam = "Charge Beam"
    IceBeam = "Ice Beam"
    WaveBeam = "Wave Beam"
    UnknownPlasmaBeam = "Unknown Plasma Beam"
    PlasmaBeam = "Plasma Beam"
    Bomb = "Bomb"
    VariaSuit = "Varia Suit"
    UnknownGravitySuit = "Unknown Gravity Suit"
    GravitySuit = "Gravity Suit"
    MorphBall = "Morph Ball"
    SpeedBooster = "Speed Booster"
    HiJump = "Hi-Jump"
    ScrewAttack = "Screw Attack"
    UnknownSpaceJump = "Unknown Space Jump"
    SpaceJump = "Space Jump"
    PowerGrip = "Power Grip"
    Nothing = "Nothing"
    APLogo = "AP Logo"
    APLogoProgression = "AP Progression"
    APLogoUseful = "AP Useful"
    SpazerBeam = "Spazer Beam"
    GrappleBeam = "Grapple Beam"
    SpringBall = "Spring Ball"
    XRayScope = "X-Ray Scope"
    ReserveTank = "Reserve Tank"
    WallJump = "Wall Jump"
    PowerBeam = "Power Beam"
    SpiderBall = "Spider Ball"


builtin_sprite_pointers: Mapping[Sprite, int] = {
    Sprite.EnergyTank: get_symbol("sRandoEnergyTankSprite"),
    Sprite.MissileTank: get_symbol("sRandoMissileTankSprite"),
    Sprite.SuperMissileTank: get_symbol("sRandoSuperMissileTankSprite"),
    Sprite.PowerBombTank: get_symbol("sRandoPowerBombTankSprite"),
    Sprite.LongBeam: get_symbol("sRandoLongBeamSprite"),
    Sprite.ChargeBeam: get_symbol("sRandoChargeBeamSprite"),
    Sprite.IceBeam: get_symbol("sRandoIceBeamSprite"),
    Sprite.WaveBeam: get_symbol("sRandoWaveBeamSprite"),
    Sprite.UnknownPlasmaBeam: get_symbol("sRandoUnknownPlasmaBeamSprite"),
    Sprite.PlasmaBeam: get_symbol("sRandoPlasmaBeamSprite"),
    Sprite.Bomb: get_symbol("sRandoBombSprite"),
    Sprite.VariaSuit: get_symbol("sRandoVariaSuitSprite"),
    Sprite.UnknownGravitySuit: get_symbol("sRandoUnknownGravitySuitSprite"),
    Sprite.GravitySuit: get_symbol("sRandoGravitySuitSprite"),
    Sprite.MorphBall: get_symbol("sRandoMorphBallSprite"),
    Sprite.SpeedBooster: get_symbol("sRandoSpeedBoosterSprite"),
    Sprite.HiJump: get_symbol("sRandoHiJumpSprite"),
    Sprite.ScrewAttack: get_symbol("sRandoScrewAttackSprite"),
    Sprite.UnknownSpaceJump: get_symbol("sRandoUnknownSpaceJumpSprite"),
    Sprite.SpaceJump: get_symbol("sRandoSpaceJumpSprite"),
    Sprite.PowerGrip: get_symbol("sRandoPowerGripSprite"),
    Sprite.Nothing: get_symbol("sRandoNothingSprite"),
}


# TODO: Edited vanilla sprites could/should be diffed, segmented, or something
# Plasma Beam also
sprite_imports: Mapping[Sprite, tuple[str | int, str | int]] = {
    Sprite.APLogo: ("ap_logo.gfx", "ap_logo.pal"),
    Sprite.APLogoProgression: ("ap_logo_progression.gfx", "ap_logo.pal"),
    Sprite.APLogoUseful: ("ap_logo_useful.gfx", "ap_logo.pal"),
    Sprite.SpazerBeam: ("spazer_beam.gfx", "spazer_beam.pal"),
    Sprite.GrappleBeam: ("grapple_beam.gfx", "grapple_beam.pal"),
    Sprite.SpringBall: ("spring_ball.gfx", "spring_ball.pal"),
    Sprite.XRayScope: ("xray_scope.gfx", "xray_scope.pal"),
    Sprite.ReserveTank: ("reserve_tank.gfx", get_symbol("sCommonTilesPal")),
    Sprite.WallJump: (get_symbol("sRandoHiJumpGfx"), "wall_jump.pal"),  # Will be moved back into patch when added as full item
    Sprite.PowerBeam: ("power_beam.gfx", "power_beam.pal"),
    Sprite.SpiderBall: ("spider_ball.gfx", "spider_ball.pal"),
}


unknown_item_alt_sprites: Mapping[str, str] = {
    "Plasma Beam": Sprite.UnknownPlasmaBeam,
    "Space Jump": Sprite.UnknownSpaceJump,
    "Gravity Suit": Sprite.UnknownGravitySuit,
}


compatible_games: Mapping[str, Mapping[str, str]] = {
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


def get_zero_mission_sprite(item: Item) -> str | None:
    if item.game not in compatible_games:
        return None

    return compatible_games[item.game].get(item.name)
