import typing
from pathlib import Path
from collections import Counter
from typing import Any, ClassVar, Dict, List, Optional

from BaseClasses import Item, ItemClassification, Tutorial
import settings
from worlds.AutoWorld import WebWorld, World

from .client import MZMClient
from .data import data_path
from .items import item_data_table, major_item_data_table, mzm_item_name_groups, MZMItem
from .locations import full_location_table, mzm_location_name_groups
from .options import MZMOptions, MorphBallPlacement, mzm_option_groups
from .regions import create_regions_and_connections
from .rom import MZMProcedurePatch, write_tokens
from .rules import set_rules


class MZMSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Metroid: Zero Mission ROM."""
        description = "Metroid: Zero Mission (U) ROM file"
        copy_to = "Metroid - Zero Mission (USA).gba"
        md5s = [MZMProcedurePatch.hash]

    class RomStart(str):
        """
        Set this to false to never autostart a rom (such as after patching),
        Set it to true to have the operating system default program open the rom
        Alternatively, set it to a path to a program to open the .gba file with
        """
    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: typing.Union[RomStart, bool] = True

class MZMWeb(WebWorld):
    theme = "ice"
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Metroid: Zero Mission for Archipelago on your computer.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["N/A"]
    )

    tutorials = [setup]
    option_groups = mzm_option_groups


class MZMWorld(World):
    """
    Metroid: Zero Mission is a retelling of the first Metroid on NES. Relive Samus' first adventure on planet Zebes with
    new areas, items, enemies, and story! Logic based on Metroid: Zero Mission Randomizer by Biosp4rk and Dragonfangs,
    used with permission.
    """
    game: str = "Metroid Zero Mission"
    options_dataclass = MZMOptions
    options: MZMOptions
    topology_present = True
    settings: ClassVar[MZMSettings]

    web = MZMWeb()

    required_client_version = (0, 5, 0)

    item_name_to_id = {name: data.code for name, data in item_data_table.items()}
    location_name_to_id = {name: data.code for name, data in full_location_table.items()}

    item_name_groups = mzm_item_name_groups
    location_name_groups = mzm_location_name_groups

    junk_fill: List[str]

    def generate_early(self):
        self.junk_fill = list(Counter(self.options.junk_fill_weights).elements())

        # Only this player should have effectively empty locations if they so choose.
        self.options.local_items.value.add("Nothing")

    def create_regions(self) -> None:
        create_regions_and_connections(self)

        self.place_event("Kraid Defeated", "Kraid")
        self.place_event("Ridley Defeated", "Ridley")
        self.place_event("Mother Brain Defeated", "Mother Brain")
        self.place_event("Chozo Ghost Defeated", "Chozo Ghost")
        self.place_event("Mecha Ridley Defeated", "Mecha Ridley")
        self.place_event("Mission Accomplished!", "Chozodia Space Pirate's Ship")

        if self.options.morph_ball == MorphBallPlacement.option_early:
            self.get_location("Brinstar Morph Ball").place_locked_item(self.create_item("Morph Ball"))


    def create_items(self) -> None:
        item_pool: List[MZMItem] = []

        item_pool_size = 100
        if self.options.morph_ball == MorphBallPlacement.option_early:
            item_pool_size -= 1

        for name in major_item_data_table:
            if self.options.morph_ball == MorphBallPlacement.option_early and name == "Morph Ball":
                continue
            item_pool.append(self.create_item(name))
        item_pool.extend(self.create_tanks("Energy Tank", 12))  # All energy tanks
        item_pool.extend(self.create_tanks("Missile Tank", 50, 8))  # First 40/250 missiles
        item_pool.extend(self.create_tanks("Super Missile Tank", 15, 3))  # First 6/30 supers
        item_pool.extend(self.create_tanks("Power Bomb Tank", 9, 2))  # First 4/18 power bombs

        while len(item_pool) < item_pool_size:
            item_pool.append(self.create_filler())

        self.multiworld.itempool += item_pool

    def set_rules(self) -> None:
        set_rules(self, full_location_table)
        self.multiworld.completion_condition[self.player] = lambda state: (
            state.has("Mission Accomplished!", self.player))

    def generate_output(self, output_directory: str):
        output_path = Path(output_directory)

        patch = MZMProcedurePatch()
        patch.write_file("basepatch.bsdiff", data_path("basepatch.bsdiff"))
        write_tokens(self, patch)
        if not self.options.unknown_items_always_usable:
            patch.add_vanilla_unknown_item_sprites()
        if self.options.layout_patches:
            patch.add_layout_patches()

        output_filename = self.multiworld.get_out_file_name_base(self.player)
        patch.write(output_path / f"{output_filename}{patch.patch_file_ending}")

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "goal": self.options.goal.value,
            "unknown_items": self.options.unknown_items_always_usable.value,
            "layout_patches": self.options.layout_patches.value,
            "logic_difficulty": self.options.logic_difficulty.value,
            "ibj_logic": self.options.ibj_in_logic.value,
            "heatruns": self.options.heatruns_lavadives.value,
            "walljump_logic": self.options.walljumps_in_logic.value,
            "tricky_shinesparks": self.options.tricky_shinesparks.value,
            "death_link": self.options.death_link.value,
            "remote_items": self.options.remote_items.value,
            "chozodia_access": self.options.chozodia_access.value,
        }

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(self.junk_fill)

    def create_item(self, name: str, force_classification: Optional[ItemClassification] = None):
        return MZMItem(name,
                       force_classification if force_classification is not None else item_data_table[name].progression,
                       self.item_name_to_id[name],
                       self.player)

    # Overridden so the extra minor items can be forced filler
    def create_filler(self) -> Item:
        return self.create_item(self.get_filler_item_name(), ItemClassification.filler)

    def create_tanks(self, item_name: str, count: int, progression_count: Optional[int] = None):
        if progression_count is None:
            progression_count = count
        for _ in range(progression_count):
            yield self.create_item(item_name)
        for _ in range(count - progression_count):
            yield self.create_item(item_name, ItemClassification.filler)

    def place_event(self, name: str, location_name: Optional[str] = None):
        if location_name is None:
            location_name = name
        item = MZMItem(name, ItemClassification.progression, None, self.player)
        location = self.multiworld.get_location(location_name, self.player)
        assert location.address is None
        location.place_locked_item(item)
        location.show_in_spoiler = True
