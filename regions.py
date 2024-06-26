from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region

from .logic import MZMLogic as logic
from .locations import (brinstar_location_table, kraid_location_table, norfair_location_table,
                        ridley_location_table, tourian_location_table, crateria_location_table,
                        chozodia_location_table, MZMLocation)

if TYPE_CHECKING:
    from . import MZMWorld


def create_regions(world: MZMWorld):
    # create all regions and populate with locations
    menu = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu)

    brinstar = Region("Brinstar", world.player, world.multiworld)
    brinstar.add_locations(brinstar_location_table, MZMLocation)
    world.multiworld.regions.append(brinstar)

    kraid = Region("Kraid", world.player, world.multiworld)
    kraid.add_locations(kraid_location_table, MZMLocation)
    world.multiworld.regions.append(kraid)

    norfair = Region("Norfair", world.player, world.multiworld)
    norfair.add_locations(norfair_location_table, MZMLocation)
    world.multiworld.regions.append(norfair)

    ridley = Region("Ridley", world.player, world.multiworld)
    ridley.add_locations(ridley_location_table, MZMLocation)
    world.multiworld.regions.append(ridley)

    tourian = Region("Tourian", world.player, world.multiworld)
    tourian.add_locations(tourian_location_table, MZMLocation)
    world.multiworld.regions.append(tourian)

    crateria = Region("Crateria", world.player, world.multiworld)
    crateria.add_locations(crateria_location_table, MZMLocation)
    world.multiworld.regions.append(crateria)

    chozodia = Region("Chozodia", world.player, world.multiworld)
    chozodia.add_locations(chozodia_location_table, MZMLocation)
    world.multiworld.regions.append(chozodia)

    mission_complete = Region("Mission Complete", world.player, world.multiworld)
    world.multiworld.regions.append(mission_complete)

    menu.connect(brinstar)

    # TODO: finish logic

    brinstar.connect(norfair, "Brinstar-Norfair elevator",
                     lambda state: logic.mzm_can_bomb_block(state, world.player))

    brinstar.connect(kraid, "Brinstar-Kraid elevator",
                     lambda state: logic.mzm_can_bomb_block(state, world.player))

    # this works for now. it's kind of tricky, cause all you need just to get there is PBs and bombs,
    # but to actually do anything (including get to ship) you need IBJ/speed/sj. it's just speed for now.
    # this may not even be necessary because these requirements also cover brinstar -> norfair -> crateria
    brinstar.connect(crateria, "Brinstar-Crateria ball cannon", lambda state: (
            logic.mzm_has_power_bombs(state, world.player)
            and logic.mzm_can_ballcannon(state, world.player)
            and logic.mzm_can_hj_sj_ibj_or_grip(state, world.player)
            and state.has("Speed Booster", world.player)
    ))

    brinstar.connect(tourian, "Brinstar-Tourian elevator", lambda state:
       state.has_all({"EVENT_KRAID_DEFEATED", "EVENT_RIDLEY_DEFEATED"}, world.player))

    norfair.connect(crateria, "Norfair-Crateria elevator",
                    lambda state: logic.mzm_can_long_beam(state, world.player))

    norfair.connect(ridley, "Norfair-Ridley elevator", lambda state: (
        ((logic.mzm_norfair_to_save_behind_hijump(state, world.player)
             and logic.mzm_has_missile_count(state, world.player, 4)
             and state.has_all({"Wave Beam", "Speed Booster"}, world.player)
             )
            or logic.mzm_norfair_shortcut(state, world.player))
        and (logic.mzm_has_missile_count(state, world.player, 6)
             or logic.mzm_has_power_bombs(state, world.player))
    ))

    #tourian.connect(crateria, "Tourian-Crateria Elevator")
    # there's a door lock on the crateria side if you haven't killed Mother Brain
    # in rando. in vanilla it's got a super missile door, weirdly. but the elevator simply
    # doesn't work until after escape i guess. i don't think this is necessary in any case

    crateria.connect(chozodia, "Crateria-Chozodia Upper Door", lambda state: (
            logic.mzm_has_power_bombs(state, world.player)
            and (logic.mzm_can_ibj(state, world.player)
                 or logic.mzm_can_space_jump(state, world.player)
                 or (state.has("Speed Booster", world.player) and logic.mzm_can_walljump(state, world.player)))
            and (state.has("EVENT_MOTHER_BRAIN_DEFEATED", world.player) or not world.options.chozodia_access.value)))

    crateria.connect(chozodia, "Crateria-Chozodia Lower Door", lambda state: (
        logic.mzm_has_power_bombs(state, world.player)
        and (state.has("EVENT_MOTHER_BRAIN_DEFEATED", world.player) or not world.options.chozodia_access.value)))
