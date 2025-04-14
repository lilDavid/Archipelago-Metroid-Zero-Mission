from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from BaseClasses import Region, Location, MultiWorld
from .rules import *
from .locations import full_location_table

if TYPE_CHECKING:
    from . import MZMWorld


def create_region(multiworld: MultiWorld, player: int, region_name: str):
    region = Region(region_name, player, multiworld)

    for location_name, location_data in full_location_table.items():
        if location_data.region == region_name:
            location = Location(player, location_name, location_data.code, region)
            location.game = multiworld.game.get(player)
            region.locations.append(location)

    multiworld.regions.append(region)


def connect(multiworld: MultiWorld, player: int, entrance_name: str, source: str, target: str,
            rule: Optional[Requirement] = None):

    source_region = multiworld.get_region(source, player)
    target_region = multiworld.get_region(target, player)
    source_region.connect(target_region, entrance_name, rule)


def create_regions_and_connections(world: MZMWorld):
    player = world.player
    multiworld = world.multiworld

    create_region(multiworld, player, "Menu")
    create_region(multiworld, player, "Brinstar Start")
    create_region(multiworld, player, "Brinstar Main")
    create_region(multiworld, player, "Brinstar Top")
    create_region(multiworld, player, "Brinstar Past Hives")
    create_region(multiworld, player, "Kraid Main")
    create_region(multiworld, player, "Kraid Acid Worm Area")
    create_region(multiworld, player, "Kraid Left Shaft")
    create_region(multiworld, player, "Kraid Bottom")
    create_region(multiworld, player, "Norfair Main")
    create_region(multiworld, player, "Norfair Right Shaft")
    create_region(multiworld, player, "Norfair Upper Right Shaft")
    create_region(multiworld, player, "Norfair Behind Ice Beam")
    create_region(multiworld, player, "Norfair Under Brinstar Elevator")
    create_region(multiworld, player, "Norfair Lower Right Shaft")
    create_region(multiworld, player, "Lower Norfair")
    create_region(multiworld, player, "Norfair Screw Attack Area")
    create_region(multiworld, player, "Norfair Behind Super Door")
    create_region(multiworld, player, "Norfair Bottom")
    create_region(multiworld, player, "Ridley Main")
    create_region(multiworld, player, "Ridley Left Shaft")
    create_region(multiworld, player, "Ridley SW Puzzle")
    create_region(multiworld, player, "Ridley Right Shaft")
    create_region(multiworld, player, "Ridley Speed Puzzles")
    create_region(multiworld, player, "Central Ridley")
    create_region(multiworld, player, "Ridley Room")
    create_region(multiworld, player, "Tourian")
    create_region(multiworld, player, "Crateria")
    create_region(multiworld, player, "Upper Crateria")
    create_region(multiworld, player, "Chozodia Ruins")
    create_region(multiworld, player, "Chozodia Ruins Test Area")
    create_region(multiworld, player, "Chozodia Glass Tube")
    create_region(multiworld, player, "Chozodia Under Tube")
    create_region(multiworld, player, "Chozodia Mothership Central")
    create_region(multiworld, player, "Chozodia Mothership Lower")
    create_region(multiworld, player, "Chozodia Mothership Upper")
    create_region(multiworld, player, "Chozodia Deep Mothership")
    create_region(multiworld, player, "Chozodia Mothership Cockpit")
    create_region(multiworld, player, "Chozodia Original Power Bomb Room")
    create_region(multiworld, player, "Chozodia Mecha Ridley Hallway")
    create_region(multiworld, player, "Mission Accomplished!")

    connect(multiworld, player, "Game Start", "Menu", "Brinstar Start")
    connect(multiworld, player, "Brinstar Start -> Main Shaft", "Brinstar Start", "Brinstar Main", MorphBall.create_rule(world))
    connect(multiworld, player, "Brinstar Main -> Brinstar Top", "Brinstar Main", "Brinstar Top", brinstar_main_to_brinstar_top().create_rule(world))
    connect(multiworld, player, "Brinstar Main -> Past Hives", "Brinstar Main", "Brinstar Past Hives", brinstar_past_hives().create_rule(world))
    connect(multiworld, player, "Brinstar Past Hives -> Top", "Brinstar Past Hives", "Brinstar Top", brinstar_pasthives_to_brinstar_top().create_rule(world))
    connect(multiworld, player, "Brinstar Top -> Past Hives", "Brinstar Top", "Brinstar Past Hives", CanEnterMediumMorphTunnel.create_rule(world))
    connect(multiworld, player, "Brinstar -> Kraid Elevator", "Brinstar Start", "Kraid Main", CanSingleBombBlock.create_rule(world))
    connect(multiworld, player, "Brinstar -> Norfair Elevator", "Brinstar Main", "Norfair Main", CanBombTunnelBlock.create_rule(world))
    connect(multiworld, player, "Brinstar -> Tourian Elevator", "Brinstar Main", "Tourian", all(MorphBall, KraidBoss, RidleyBoss).create_rule(world))
    connect(multiworld, player, "Brinstar -> Crateria Ballcannon", "Brinstar Start", "Upper Crateria", brinstar_crateria_ballcannon().create_rule(world))
    connect(multiworld, player, "Kraid Main -> Acid Worm Area", "Kraid Main", "Kraid Acid Worm Area", kraid_upper_right().create_rule(world))
    connect(multiworld, player, "Kraid Main -> Left Shaft", "Kraid Main", "Kraid Left Shaft", kraid_left_shaft_access().create_rule(world))
    connect(multiworld, player, "Kraid Left Shaft -> Bottom", "Kraid Left Shaft", "Kraid Bottom", kraid_left_shaft_to_bottom().create_rule(world))
    connect(multiworld, player, "Kraid -> Lower Norfair Shortcut", "Kraid Bottom", "Lower Norfair", kraid_bottom_to_lower_norfair().create_rule(world))
    connect(multiworld, player, "Norfair -> Crateria Elevator", "Norfair Main", "Crateria", norfair_main_to_crateria().create_rule(world))
    connect(multiworld, player, "Norfair Elevator -> Right Shaft", "Norfair Main", "Norfair Right Shaft", norfair_right_shaft_access().create_rule(world))
    connect(multiworld, player, "Norfair Right Shaft -> Upper", "Norfair Right Shaft", "Norfair Upper Right Shaft", norfair_upper_right_shaft().create_rule(world))
    connect(multiworld, player, "Norfair Right Shaft -> Under Elevator", "Norfair Right Shaft", "Norfair Under Brinstar Elevator", norfair_shaft_to_under_elevator().create_rule(world))
    connect(multiworld, player, "Norfair Upper Right -> Behind Ice Beam", "Norfair Upper Right Shaft", "Norfair Behind Ice Beam", norfair_behind_ice_beam().create_rule(world))
    connect(multiworld, player, "Norfair Ridley Shortcut", "Norfair Behind Ice Beam", "Norfair Bottom", norfair_behind_ice_to_bottom().create_rule(world))
    connect(multiworld, player, "Norfair Right Shaft -> Lower Shaft", "Norfair Under Brinstar Elevator", "Norfair Lower Right Shaft", norfair_lower_right_shaft().create_rule(world))
    connect(multiworld, player, "Norfair Lower Shaft -> Under Brinstar Elevator", "Norfair Lower Right Shaft", "Norfair Under Brinstar Elevator", norfair_lower_shaft_to_under_elevator().create_rule(world))
    connect(multiworld, player, "Norfair Right Shaft -> Lower Norfair", "Norfair Lower Right Shaft", "Lower Norfair", norfair_lower_right_shaft_to_lower_norfair().create_rule(world))
    connect(multiworld, player, "Lower Norfair -> Screw Attack", "Lower Norfair", "Norfair Screw Attack Area", lower_norfair_to_screwattack().create_rule(world))
    connect(multiworld, player, "Lower Norfair -> Behind Super Missile Door", "Lower Norfair", "Norfair Behind Super Door", lower_norfair_to_spaceboost_room().create_rule(world))
    connect(multiworld, player, "Lower Norfair -> Kraid", "Lower Norfair", "Kraid Bottom", lower_norfair_to_kraid().create_rule(world))
    connect(multiworld, player, "Lower Norfair -> Bottom", "Lower Norfair", "Norfair Bottom", lower_norfair_to_bottom_norfair().create_rule(world))
    connect(multiworld, player, "Lower Norfair -> Lower Right Shaft", "Lower Norfair", "Norfair Lower Right Shaft", lower_norfair_to_lower_right_shaft().create_rule(world))
    connect(multiworld, player, "Norfair Bottom -> Norfair Lower Right Shaft", "Norfair Bottom", "Norfair Lower Right Shaft", bottom_norfair_to_lower_shaft().create_rule(world))
    connect(multiworld, player, "Norfair -> Ridley Elevator", "Norfair Bottom", "Ridley Main", bottom_norfair_to_ridley().create_rule(world))
    connect(multiworld, player, "Norfair Bottom -> Screw Attack", "Norfair Bottom", "Norfair Screw Attack Area", bottom_norfair_to_screw().create_rule(world))
    connect(multiworld, player, "Norfair Screw Attack -> Lower Norfair", "Norfair Screw Attack Area", "Lower Norfair", screw_to_lower_norfair().create_rule(world))
    connect(multiworld, player, "Ridley Elevator -> Left Shaft", "Ridley Main", "Ridley Left Shaft", ridley_main_to_left_shaft().create_rule(world))
    connect(multiworld, player, "Ridley Elevator -> Right Shaft Shortcut", "Ridley Main", "Ridley Right Shaft", ridley_main_to_right_shaft().create_rule(world))
    connect(multiworld, player, "Ridley Left Shaft -> SW Puzzle", "Ridley Left Shaft", "Ridley SW Puzzle", ridley_left_shaft_to_sw_puzzle().create_rule(world))
    connect(multiworld, player, "Ridley Left Shaft -> Right Shaft", "Ridley Left Shaft", "Ridley Right Shaft")
    connect(multiworld, player, "Ridley Right Shaft -> Left Shaft", "Ridley Right Shaft", "Ridley Left Shaft", ridley_right_shaft_to_left_shaft().create_rule(world))
    connect(multiworld, player, "Ridley Right Shaft -> Speed Puzzles", "Ridley Right Shaft", "Ridley Speed Puzzles", ridley_speed_puzzles_access().create_rule(world))
    connect(multiworld, player, "Ridley Right Shaft -> Central", "Ridley Right Shaft", "Central Ridley", ridley_right_shaft_to_central().create_rule(world))
    connect(multiworld, player, "Ridley Right Shaft -> SW Puzzle", "Ridley Right Shaft", "Ridley SW Puzzle", ridley_left_shaft_to_sw_puzzle().create_rule(world))
    connect(multiworld, player, "Ridley Central -> Ridley's Room", "Central Ridley", "Ridley Room", ridley_central_to_ridley_room().create_rule(world))
    connect(multiworld, player, "Tourian Escape -> Chozodia", "Tourian", "Chozodia Ruins Test Area", tourian_to_chozodia().create_rule(world))
    connect(multiworld, player, "Crateria -> Upper", "Crateria", "Upper Crateria", crateria_main_to_crateria_upper().create_rule(world))
    connect(multiworld, player, "Crateria -> Chozodia Lower Door", "Crateria", "Chozodia Under Tube", crateria_to_under_tube().create_rule(world))
    connect(multiworld, player, "Crateria -> Chozodia Upper Door", "Upper Crateria", "Chozodia Ruins", crateria_upper_to_chozo_ruins().create_rule(world))
    connect(multiworld, player, "Chozo Ruins -> Chozo Ruins Test", "Chozodia Ruins", "Chozodia Ruins Test Area", chozo_ruins_to_ruins_test().create_rule(world))
    connect(multiworld, player, "Chozo Ruins Test -> Chozo Ruins", "Chozodia Ruins Test Area", "Chozodia Ruins", ruins_test_to_ruins().create_rule(world))
    connect(multiworld, player, "Chozo Ruins -> Glass Tube", "Chozodia Ruins", "Chozodia Glass Tube", chozo_ruins_to_chozodia_tube().create_rule(world))
    connect(multiworld, player, "Chozodia Under Tube -> Crateria", "Chozodia Under Tube", "Crateria", under_tube_to_crateria().create_rule(world))
    connect(multiworld, player, "Chozodia Under Tube -> Glass Tube", "Chozodia Under Tube", "Chozodia Glass Tube", under_tube_to_tube().create_rule(world))
    connect(multiworld, player, "Chozodia Glass Tube -> Under Tube", "Chozodia Glass Tube", "Chozodia Under Tube", tube_to_under_tube().create_rule(world))
    connect(multiworld, player, "Chozodia Glass Tube -> Chozo Ruins", "Chozodia Glass Tube", "Chozodia Ruins", chozodia_tube_to_chozo_ruins().create_rule(world))
    connect(multiworld, player, "Chozodia Glass Tube -> Mothership Central", "Chozodia Glass Tube", "Chozodia Mothership Central", chozodia_tube_to_mothership_central().create_rule(world))
    connect(multiworld, player, "Chozodia Central Mothership -> Lower Mothership", "Chozodia Mothership Central", "Chozodia Mothership Lower", mothership_central_to_lower().create_rule(world))
    connect(multiworld, player, "Chozodia Central Mothership -> Upper Mothership", "Chozodia Mothership Central", "Chozodia Mothership Upper", mothership_central_to_upper().create_rule(world))
    connect(multiworld, player, "Chozodia Lower Mothership -> Upper Mothership", "Chozodia Mothership Lower", "Chozodia Mothership Upper", mothership_lower_to_upper().create_rule(world))
    connect(multiworld, player, "Chozodia Upper Mothership -> Lower Mothership", "Chozodia Mothership Upper",
            "Chozodia Mothership Lower", mothership_upper_to_lower().create_rule(world))
    connect(multiworld, player, "Chozodia Upper Mothership -> Deep Mothership", "Chozodia Mothership Upper",
            "Chozodia Deep Mothership", mothership_upper_to_deep_mothership().create_rule(world))
    connect(multiworld, player, "Chozodia Deep Mothership -> Cockpit", "Chozodia Deep Mothership",
            "Chozodia Mothership Cockpit", deep_mothership_to_cockpit().create_rule(world))
    connect(multiworld, player, "Chozodia Cockpit -> Original PB", "Chozodia Mothership Cockpit", "Chozodia Original Power Bomb Room", cockpit_to_original_pb().create_rule(world))
    connect(multiworld, player, "Chozodia Cockpit -> Mecha Ridley", "Chozodia Mothership Cockpit", "Chozodia Mecha Ridley Hallway", cockpit_to_mecha_ridley().create_rule(world))
