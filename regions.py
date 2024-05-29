from BaseClasses import Region
from .logic import MZMLogic as logic
from .locations import (brinstar_location_table, kraid_location_table, norfair_location_table,
                        ridley_location_table, tourian_location_table, crateria_location_table,
                        chozodia_location_table, MZMLocation)


def create_regions(self): # TODO: later take "difficulty/tricks required" as a parameter?
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

    #TODO: finish logic

    brinstar.connect(norfair, "Brinstar-Norfair elevator", lambda state: (
        logic.mzm_can_bomb_any(state, self.multiworld, self.player)
    )
    ) #TODO in trickless, require can long beam as well if it's decided the shortcut is a "trick"

    brinstar.connect(kraid, "Brinstar-Kraid elevator", lambda state: (
        logic.mzm_can_bomb_any(state, self.multiworld, self.player))
    )

    # this works for now. it's kind of tricky, cause all you need just to get there is PBs and bombs,
    # but to actually do anything (including get to ship) you need IBJ/speed/sj. it's just speed for now.
    brinstar.connect(crateria, "Brinstar-Crateria ball cannon", lambda state: (
        logic.mzm_has_power_bombs(state, self.multiworld, self.player)
        and logic.mzm_has_bombs(state, self.multiworld, self.player)
        and state.has("Speed Booster", self.player)
    ))

    #brinstar.connect(tourian, "Brinstar-Tourian elevator", lambda state: (Ridley_defeated and Kraid_defeated)

    norfair.connect(crateria, "Norfair-Crateria elevator")
    norfair.connect(ridley, "Norfair-Ridley elevator", lambda state: (
        state.has("Speed Booster", self.player)
        and logic.mzm_has_missiles(state, self.multiworld, self.player)
    ))  # yes this is actually all you need in least-restrictive logic

    # norfair.connect(ridley, "Norfair-Ridley Imago path") # TODO: confirm if unnecessary

    tourian.connect(crateria, "Tourian-Crateria Elevator")
    # there's a door lock on the crateria side if you haven't killed Mother Brain
    # in rando. in vanilla it's got a super missile door, weirdly. but the elevator simply
    # doesn't work until after escape i guess.

    # currently assumes IBJ
    crateria.connect(chozodia, "Crateria-Chozodia Upper Door", lambda state: (
        logic.mzm_has_power_bombs(state, self.multiworld, self.player)
        and (logic.mzm_has_bombs(state, self.multiworld, self.player)
             or logic.mzm_can_space_jump(state, self.multiworld, self.player))
    ))

    crateria.connect(chozodia, "Crateria-Chozodia Lower Door", lambda state: (
        logic.mzm_has_power_bombs(state, self.multiworld, self.player)
    ))

    chozodia.connect(mission_complete, "Mission Complete")