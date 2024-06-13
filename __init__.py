from pathlib import Path
from collections import Counter
from typing import Any, Dict, List, Mapping, Optional

from BaseClasses import ItemClassification, Tutorial
import settings
from worlds.AutoWorld import WebWorld, World

from .client import MZMClient
from .items import item_data_table, MZMItem
from .locations import full_location_table
from .options import MZMOptions
from .regions import create_regions
from .rom import LocalRom, MZMDeltaPatch, get_base_rom_path, patch_rom
from .rules import set_rules


class MZMSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        #File name of the Metroid: Zero Mission ROM
        description = "Metroid: Zero Mission (U) ROM file"
        copy_to = "Metroid - Zero Mission (USA).gba"
        md5s = [MZMDeltaPatch.hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class MZMWeb(WebWorld):
    theme = "ice"
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Metroid: Zero Mission for Archipelago on your computer.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["NoiseCrush"]
    )

    tutorials = [setup]


class MZMWorld(World):
    """
    Placeholder Description. Metroid: Zero Mission is a cool game
    """
    game: str = "Metroid Zero Mission"
    options_dataclass = MZMOptions
    options: MZMOptions
    topology_present = True

    web = MZMWeb()

    item_name_to_id = {name: data.code for name, data in item_data_table.items()}
    location_name_to_id = full_location_table

    junk_fill: List[str]

    def generate_early(self):
        self.junk_fill = list(Counter(self.options.junk_fill_weights).elements())

        # Only this player should have effectively empty locations if they so choose.
        self.options.local_items.value.add('Nothing')

    def create_regions(self) -> None:
        create_regions(self)

        self.place_event("Mission Complete", "Chozodia Space Pirate's Ship")

    def create_items(self) -> None:
        item_pool: List[MZMItem] = []

        for name in items.get_major_items():
            item_pool.append(self.create_item(name))
        item_pool.extend(self.create_tanks("Energy Tank", 12))  # All energy tanks
        item_pool.extend(self.create_tanks("Missile Tank", 50, 5))  # First 25/250 missiles
        item_pool.extend(self.create_tanks("Super Missile Tank", 15, 3))  # First 6/30 supers
        item_pool.extend(self.create_tanks("Power Bomb Tank", 9, 2))  # First 4/18 power bombs
        while len(item_pool) < 100:
            item_pool.append(self.create_filler())

        self.multiworld.itempool += item_pool

    def set_rules(self) -> None:
        set_rules(self.multiworld, self.player, full_location_table)
        self.multiworld.completion_condition[self.player] = lambda state: (
            state.has("Mission Complete", self.player))

    def fill_slot_data(self) -> Dict[str, Any]:

        slot_data: Dict[str, Any] = {
            "unknown_items": self.options.unknown_items_always_usable.value,
            "death_link": self.options.death_link.value
        }

        return slot_data

    def generate_output(self, output_directory: str):
        output_path = Path(output_directory)

        try:
            world = self.multiworld
            player = self.player
            rom = LocalRom(get_base_rom_path())
            patch_rom(rom, self)

            rompath = output_path / f'{world.get_out_file_name_base(player)}.gba'
            rom.write_to_file(rompath)
            self.rom_name = rom.name

            patch = MZMDeltaPatch(
                rompath.with_suffix(MZMDeltaPatch.patch_file_ending),
                player = player,
                player_name = world.player_name[player],
                patched_path = rompath
            )
            patch.write()
        finally:
            if rompath.exists():
                rompath.unlink()

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict(
            "unknown_items_always_usable",
            "death_link",
        )

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(self.junk_fill)

    def create_item(self, name: str, force_classification: Optional[ItemClassification] = None):
        return MZMItem(name,
                       force_classification if force_classification is not None else item_data_table[name].progression,
                       self.item_name_to_id[name],
                       self.player)

    def create_tanks(self, item_name: str, count: int, progression_count: int = None):
        if progression_count is None:
            progression_count = count
        for _ in range(progression_count):
            yield self.create_item(item_name, ItemClassification.progression)
        for _ in range(count - progression_count):
            yield self.create_item(item_name)

    def place_event(self, name: str, location_name: Optional[str] = None):
        if location_name is None:
            location_name = name
        item = MZMItem(name, ItemClassification.progression, None, self.player)
        location = self.multiworld.get_location(location_name, self.player)
        assert location.address is None
        location.place_locked_item(item)
        location.show_in_spoiler = False
