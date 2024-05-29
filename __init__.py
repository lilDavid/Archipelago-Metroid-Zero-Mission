from typing import Any, Dict, List

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World

#from .client import MZMClient
from .items import item_data_table, MZMItem
from .locations import full_location_table
from .options import MZMOptions
from .regions import create_regions
from .rom import MZMDeltaPatch
from .rules import set_rules

"""
class MZMSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        #File name of the Metroid: Zero Mission ROM
        description = "Metroid: Zero Mission (U) ROM file"
        copy_to = "Metroid - Zero Mission (USA).gba"
        md5s = [MZMDeltaPatch.hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)
"""


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

    data_version = 0
    web = MZMWeb()

    item_name_to_id = {name: data.code for name, data in item_data_table.items()}
    location_name_to_id = full_location_table

    def create_item(self, name: str):
        return MZMItem(name, item_data_table[name].progression, self.item_name_to_id[name], self.player)

    def create_regions(self) -> None:
        create_regions(self)

    def create_items(self) -> None:
        item_pool: List[MZMItem] = []
        for name, item in item_data_table.items():
            item_pool.append(self.create_item(name))

        for item in range(0, 11):
            item_pool.append(self.create_item("Energy Tank"))  # add all the etanks

        for item in range(0, 14):
            item_pool.append(self.create_item("Super Missile Tank"))  # add all the supers

        for item in range(0, 9):
            item_pool.append(self.create_item("Power Bomb Tank"))  # add all the power bombs

        while len(item_pool) < 100:
            item_pool.append(self.create_item("Missile Tank"))  # fill the rest with missiles

        self.multiworld.itempool += item_pool

    def set_rules(self) -> None:
        set_rules(self.multiworld, self.player, full_location_table)
        self.multiworld.completion_condition[self.player] = lambda state: (
            state.can_reach("Mission Complete", "Region", self.player))

    def fill_slot_data(self) -> Dict[str, Any]:

        slot_data: Dict[str, Any] = {
            "unknown_items": self.options.unknown_items_always_usable.value,
            "death_link": self.options.death_link.value
        }

        return slot_data
