from typing import Mapping

from BaseClasses import Item

from .items import ItemID


compatible_games: Mapping[str, Mapping[str, int]] = {
    "Super Metroid": {
        "Energy Tank": ItemID.EnergyTank,
        "Missile": ItemID.MissileTank,
        "Super Missile": ItemID.SuperMissileTank,
        "Power Bomb": ItemID.PowerBombTank,
        "Bomb": ItemID.Bomb,
        "Charge Beam": ItemID.ChargeBeam,
        "Ice Beam": ItemID.IceBeam,
        "Hi-Jump Boots": ItemID.HiJump,
        "Speed Booster": ItemID.SpeedBooster,
        "Wave Beam": ItemID.WaveBeam,
        # "Spazer Beam":
        # "Spring Ball":
        "Varia Suit": ItemID.VariaSuit,
        "Plasma Beam": ItemID.PlasmaBeam,
        # "Grappling Beam":
        "Morph Ball": ItemID.MorphBall,
        # "Reserve Tank":
        "Gravity Suit": ItemID.GravitySuit,
        # "X-Ray Scope":
        "Space Jump": ItemID.SpaceJump,
        "Screw Attack": ItemID.ScrewAttack,
    },
    "SMZ3": {
        "Missile": ItemID.MissileTank,
        "Super": ItemID.SuperMissileTank,
        "PowerBomb": ItemID.PowerBombTank,
        # "Grapple":
        # "XRay":
        "ETank": ItemID.EnergyTank,
        # "ReserveTank":
        "Charge": ItemID.ChargeBeam,
        "Ice": ItemID.IceBeam,
        "Wave": ItemID.WaveBeam,
        # "Spazer":
        "Plasma": ItemID.PlasmaBeam,
        "Varia": ItemID.VariaSuit,
        "Gravity": ItemID.GravitySuit,
        "Morph": ItemID.MorphBall,
        "Bombs": ItemID.Bomb,
        # "SpringBall":
        "ScrewAttack": ItemID.ScrewAttack,
        "HiJump": ItemID.HiJump,
        "SpaceJump": ItemID.SpaceJump,
        "SpeedBooster": ItemID.SpeedBooster,
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
        # "Power Beam":
        "Ice Beam": ItemID.IceBeam,
        "Wave Beam": ItemID.WaveBeam,
        "Plasma Beam": ItemID.PlasmaBeam,
        "Missile Expansion": ItemID.MissileTank,
        # "Scan Visor":
        "Morph Ball Bomb": ItemID.Bomb,
        "Power Bomb Expansion": ItemID.PowerBombTank,
        # "Flamethrower":
        # "Thermal Visor":
        "Charge Beam": ItemID.ChargeBeam,
        # "Super Missile":
        # "Grapple Beam":
        # "X-Ray Visor":
        # "Ice Spreader":
        # "Space Jump Boots":
        "Morph Ball": ItemID.MorphBall,
        # "Combat Visor":
        # "Boost Ball":
        # "Spider Ball":
        # "Power Suit":
        "Gravity Suit": ItemID.GravitySuit,
        "Varia Suit": ItemID.VariaSuit,
        # "Phazon Suit":
        "Energy Tank": ItemID.EnergyTank,
        # "Wavebuster":
        # "Missile Launcher":
        # "Power Bomb (Main)":
        # "Progressive Power Beam":
        "Progressive Ice Beam": ItemID.IceBeam,
        "Progressive Wave Beam": ItemID.WaveBeam,
        "Progressive Plasma Beam": ItemID.PlasmaBeam,
    },
    "Super Metroid Map Rando": {
        "ETank": ItemID.EnergyTank,
        "Missile": ItemID.MissileTank,
        "Super": ItemID.SuperMissileTank,
        "PowerBomb": ItemID.PowerBombTank,
        "Bombs": ItemID.Bomb,
        "Charge": ItemID.ChargeBeam,
        "Ice": ItemID.IceBeam,
        "HiJump": ItemID.HiJump,
        "SpeedBooster": ItemID.SpeedBooster,
        "Wave": ItemID.WaveBeam,
        # "Spazer":
        # "SpringBall":
        "Varia": ItemID.VariaSuit,
        "Gravity": ItemID.GravitySuit,
        # "XRayScope":
        "Plasma": ItemID.PlasmaBeam,
        # "Grapple":
        "SpaceJump": ItemID.SpaceJump,
        "ScrewAttack": ItemID.ScrewAttack,
        "Morph": ItemID.MorphBall,
        # "ReserveTank":
        # "WallJump":
    },
}


def get_zero_mission_sprite(item: Item):
    if item.game not in compatible_games:
        return None

    return compatible_games[item.game].get(item.name)
