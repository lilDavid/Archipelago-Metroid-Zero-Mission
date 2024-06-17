from BaseClasses import Region
from .logic import MZMLogic as logic
from .locations import (brinstar_location_table, kraid_location_table, norfair_location_table,
                        ridley_location_table, tourian_location_table, crateria_location_table,
                        chozodia_location_table, MZMLocation)


def create_regions(self):
    # create all regions and populate with locations
    menu = Region("Menu", self.player, self.multiworld)
    self.multiworld.regions.append(menu)

    brinstar = Region("Brinstar", self.player, self.multiworld)
    brinstar.add_locations(brinstar_location_table, MZMLocation)
    self.multiworld.regions.append(brinstar)

    kraid = Region("Kraid", self.player, self.multiworld)
    kraid.add_locations(kraid_location_table, MZMLocation)
    self.multiworld.regions.append(kraid)

    norfair = Region("Norfair", self.player, self.multiworld)
    norfair.add_locations(norfair_location_table, MZMLocation)
    self.multiworld.regions.append(norfair)

    ridley = Region("Ridley", self.player, self.multiworld)
    ridley.add_locations(ridley_location_table, MZMLocation)
    self.multiworld.regions.append(ridley)

    tourian = Region("Tourian", self.player, self.multiworld)
    tourian.add_locations(tourian_location_table, MZMLocation)
    self.multiworld.regions.append(tourian)

    crateria = Region("Crateria", self.player, self.multiworld)
    crateria.add_locations(crateria_location_table, MZMLocation)
    self.multiworld.regions.append(crateria)

    chozodia = Region("Chozodia", self.player, self.multiworld)
    chozodia.add_locations(chozodia_location_table, MZMLocation)
    self.multiworld.regions.append(chozodia)

    mission_complete = Region("Mission Complete", self.player, self.multiworld)
    self.multiworld.regions.append(mission_complete)

    menu.connect(brinstar)

    # TODO: finish logic

    brinstar.connect(norfair, "Brinstar-Norfair elevator",
                     lambda state: logic.mzm_can_bomb_block(state, self.player))

    brinstar.connect(kraid, "Brinstar-Kraid elevator",
                     lambda state: logic.mzm_can_bomb_block(state, self.player))

    # this works for now. it's kind of tricky, cause all you need just to get there is PBs and bombs,
    # but to actually do anything (including get to ship) you need IBJ/speed/sj. it's just speed for now.
    # this may not even be necessary because these requirements also cover brinstar -> norfair -> crateria
    brinstar.connect(crateria, "Brinstar-Crateria ball cannon", lambda state: (
            logic.mzm_has_power_bombs(state, self.player)
            and logic.mzm_can_ballcannon(state, self.player)
            and logic.mzm_can_hj_sj_ibj_or_grip(state, self.player)
            and state.has("Speed Booster", self.player)
    ))

    brinstar.connect(tourian, "Brinstar-Tourian elevator", lambda state:
       state.has_all({"EVENT_KRAID_DEFEATED", "EVENT_RIDLEY_DEFEATED"}, self.player))

    norfair.connect(crateria, "Norfair-Crateria elevator",
                    lambda state: logic.mzm_can_long_beam(state, self.player))

    norfair.connect(ridley, "Norfair-Ridley elevator", lambda state: (
        ((logic.mzm_norfair_to_save_behind_hijump(state, self.player)
             and logic.mzm_has_missile_count(state, self.player, 4)
             and state.has_all({"Wave Beam", "Speed Booster"}, self.player)
             )
            or logic.mzm_norfair_shortcut(state, self.player))
        and (logic.mzm_has_missile_count(state, self.player, 6)
             or logic.mzm_has_power_bombs(state, self.player))
    ))

    #tourian.connect(crateria, "Tourian-Crateria Elevator")
    # there's a door lock on the crateria side if you haven't killed Mother Brain
    # in rando. in vanilla it's got a super missile door, weirdly. but the elevator simply
    # doesn't work until after escape i guess. i don't think this is necessary in any case

    crateria.connect(chozodia, "Crateria-Chozodia Upper Door", lambda state: (
            logic.mzm_has_power_bombs(state, self.player)
            and (logic.mzm_can_ibj(state, self.player)
                 or logic.mzm_can_space_jump(state, self.player)
                 or (state.has("Speed Booster", self.player) and logic.mzm_can_walljump(state, self.player)))))

    crateria.connect(chozodia, "Crateria-Chozodia Lower Door", lambda state: (
        logic.mzm_has_power_bombs(state, self.player)))
