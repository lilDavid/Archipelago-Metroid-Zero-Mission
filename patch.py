"""
Classes and functions related to creating a ROM patch
"""
from __future__ import annotations

from collections import Counter
import json
import hashlib
import logging
from pathlib import Path
import struct
from typing import TYPE_CHECKING, Any, Sequence, cast

import bsdiff4
from BaseClasses import Item, Location
import Utils
from worlds.Files import APPatchExtension, APProcedurePatch, APTokenMixin, APTokenTypes, InvalidDataError

from . import rom_data
from .data import APWORLD_VERSION, data_path, get_rom_address, get_symbol, symbols_hash
from .items import ItemType, item_data_table, tank_data_table, major_item_data_table
from .item_sprites import Sprite, get_zero_mission_sprite, builtin_sprite_pointers, sprite_imports, unknown_item_alt_sprites
from .locations import full_location_table as location_table
from .options import ChozodiaAccess, DisplayNonLocalItems, Goal
from .text import TERMINATOR_CHAR, Message, make_item_message

if TYPE_CHECKING:
    from . import MZMWorld


MD5_MZMUS = "ebbce58109988b6da61ebb06c7a432d5"
MD5_MZMUS_VC = "e23c14997c2ea4f11e5996908e577125"


class MZMPatchExtensions(APPatchExtension):
    game = "Metroid Zero Mission"

    @staticmethod
    def support_vc(caller: APProcedurePatch, rom: bytes):
        hasher = hashlib.md5()
        hasher.update(rom)
        if hasher.hexdigest() == MD5_MZMUS:
            return rom

        logging.warning("You appear to be using a Virtual Console ROM. "
                        "This is not officially supported and may cause bugs.")
        entry_point = (0xEA00002E).to_bytes(4, 'little')  # b 0x80000C0
        return entry_point + rom[4:]

    @staticmethod
    def apply_basepatch(caller: APProcedurePatch, rom: bytes) -> bytes:
        return bsdiff4.patch(rom, data_path("basepatch.bsdiff"))

    @staticmethod
    def apply_json(caller: APProcedurePatch, rom: bytes, file_name: str) -> bytes:
        return apply_json_data(rom, json.loads(caller.get_file(file_name).decode()))

    @staticmethod
    def add_decompressed_graphics(caller: APProcedurePatch, rom: bytes) -> bytes:
        return rom_data.add_item_sprites(rom)

    @staticmethod
    def apply_background_patches(caller: APProcedurePatch, rom: bytes) -> bytes:
        return rom_data.apply_always_background_patches(rom)

    @staticmethod
    def apply_layout_patches(caller: APProcedurePatch, rom: bytes, patches: Sequence[str]) -> bytes:
        return rom_data.apply_layout_patches(rom, set(patches))


class MZMProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Metroid Zero Mission"
    hash = MD5_MZMUS
    patch_file_ending = ".apmzm"
    result_file_ending = ".gba"

    extra_data_address: int

    def __init__(self, *args, **kwargs):
        super(MZMProcedurePatch, self).__init__(*args, **kwargs)
        self.procedure = [
            ("support_vc", []),
            ("apply_basepatch", []),
            ("apply_json", ["patch.json"]),
            ("add_decompressed_graphics", []),
            ("apply_background_patches", []),
        ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_base_rom_path(), "rb") as stream:
            return stream.read()

    def add_layout_patches(self, selected_patches: Sequence[str]):
        self.procedure.append(("apply_layout_patches", [selected_patches]))


def get_base_rom_path(file_name: str = "") -> Path:
    from . import MZMWorld
    if not file_name:
        file_name = MZMWorld.settings.rom_file

    file_path = Path(file_name)
    if file_path.exists():
        return file_path
    else:
        return Path(Utils.user_path(file_name))


goal_texts = {
    Goal.option_mecha_ridley: "Infiltrate and destroy\nthe Space Pirates' mother ship.",
    Goal.option_bosses: "Exterminate all Metroid\norganisms and defeat Mother Brain.",
}


def get_item_sprite(location: Location, world: MZMWorld) -> str:
    player = world.player
    nonlocal_item_handling = world.options.display_nonlocal_items
    item = location.item

    if location.native_item and (nonlocal_item_handling != DisplayNonLocalItems.option_none or item.player == player):
        other_world = cast("MZMWorld", world.multiworld.worlds[item.player])
        sprite = item_data_table[item.name].sprite
        if (item.name in unknown_item_alt_sprites and other_world.options.fully_powered_suit.use_alt_unknown_sprites()):
            sprite = unknown_item_alt_sprites[item.name]
        return sprite

    if nonlocal_item_handling == DisplayNonLocalItems.option_match_series:
        sprite = get_zero_mission_sprite(item)
        if sprite is not None:
            return sprite

    if item.advancement or item.trap:
        sprite = Sprite.APLogoProgression
    elif item.useful:
        sprite = Sprite.APLogoUseful
    else:
        sprite = Sprite.APLogo
    return sprite


def split_text(text: str):
    lines = [""]
    i = 0
    while i < len(text):
        next_space = text.find(" ", i)
        if next_space == -1:
            next_space = len(text)
        if len(lines[-1]) + next_space - i <= 40:
            lines[-1] = f"{lines[-1]}{text[i:next_space]} "
        else:
            lines[-1] = lines[-1][:-1]
            lines.append(text[i:next_space] + " ")
        i = next_space + 1
    lines[-1] = lines[-1][:-1]
    return lines


def write_json_data(world: MZMWorld, patch: MZMProcedurePatch):
    multiworld = world.multiworld
    player = world.player
    data = {
        "player_number": player,
        "player_name": world.player_name,
        "seed_name": multiworld.seed_name,
    }

    config = {
        "goal": world.options.goal.value,
        "difficulty": world.options.game_difficulty.value,
        "remove_gravity_heat_resistance": True,
        "power_bombs_without_bomb": True,
        "buff_power_bomb_drops": world.options.buff_pb_drops.value,
        "skip_chozodia_stealth": world.options.skip_chozodia_stealth.value,
        "start_with_maps": world.options.start_with_maps.value,
        "skip_tourian_opening_cutscenes": world.options.skip_tourian_opening_cutscenes.value,
        "elevator_speed": world.options.elevator_speed.value,
        "chozodia_requires_mother_brain": world.options.chozodia_access.value == ChozodiaAccess.option_closed
    }
    data["config"] = config

    locations = []
    for location in multiworld.get_locations(player):
        item = location.item
        if item.code is None:
            continue

        sprite = get_item_sprite(location, world)
        if item.player == player:
            item_name = item.name
            message = None
        else:
            item_name = "Nothing"
            message = f"{item.name}\nSent to {multiworld.player_name[item.player]}"

        location_data = location_table[location.name]
        assert location_data.id is not None
        locations.append({
            "id": location_data.id,
            "item": item_name,
            "sprite": sprite,
            "message": message,
        })
    data["locations"] = locations

    precollected_items = Counter(item.name for item in multiworld.precollected_items[player])
    starting_inventory: dict[str, int | bool] = {}
    for item, count in precollected_items.items():
        if item == "Missile Tank":
            starting_inventory[item] = min(count, 999)
        elif item in tank_data_table:
            starting_inventory[item] = min(count, 99)
        elif item in major_item_data_table:
            starting_inventory[item] = count > 0
    data["start_inventory"] = starting_inventory

    text = {"Story": {}}

    world_version = f" / APworld {APWORLD_VERSION}" if APWORLD_VERSION is not None else ""
    text["Story"]["Intro"] = (f"AP {multiworld.seed_name}\n"
                              f"P{player} - {world.player_name}\n"
                              f"Version {Utils.version_tuple.as_simple_string()}{world_version}\n"
                              "\n"
                              f"YOUR MISSION: {goal_texts[world.options.goal.value]}")

    plasma_beam = world.create_item("Plasma Beam")
    if world.options.plasma_beam_hint.value and plasma_beam not in multiworld.precollected_items[player]:
        zss_text = ("With Mother Brain taken down, I needed\n"
                    "to get my suit back in the ruins.\n")
        location = multiworld.find_item(plasma_beam.name, player)
        if location.native_item:
            location_text = location.parent_region.hint_text
        else:
            location_text = f"at {location.name}"
        if location.player != player:
            player_text = f" in {multiworld.player_name[location.player]}'s world"
        else:
            player_text = ""
        lines = split_text(f"Could I find the Plasma Beam {location_text}{player_text}?")
        while len(lines) > 4:
            location_text = location_text[:location_text.rfind(" ")]
            lines = split_text(f"Could I find the Plasma Beam {location_text}{player_text}?")
        if len(lines) < 4:
            zss_text += "\n"
        zss_text += "\n".join(lines)
        text["Story"]["Escape 2"] = zss_text

    data["text"] = text

    patch.write_file("patch.json", json.dumps(data).encode())


RUINS_TEST_LOCATION_ID = 100


GOAL_MAPPING = {
    "vanilla": 0,
    "bosses": 1,
}


DIFFICULTY_MAPPING = {
    "normal": 1,
    "hard": 2,
    "either": 3,
}


TEXT_INDICES = {
    ("Story", "Intro"): 0,
    ("Story", "Escape 1"): 1,
    ("Story", "Escape 2"): 2,
}


PIXEL_SIZE = 4


def apply_json_data(rom: bytes, data: list | dict) -> bytes:
    if type(data) != dict:
        raise InvalidDataError("Invalid JSON provided, expected object")

    local_rom = bytearray(rom)
    def write(address: int, data: bytes):
        assert address <= len(local_rom)
        local_rom[address:address + len(data)] = data

    extra_data_address = get_rom_address("sRandoExtraData")
    def allocate(size: int) -> int:
        nonlocal extra_data_address
        assert size >= 0
        address = extra_data_address
        extra_data_address += size
        return address

    def write_to_arena(data: bytes) -> int:
        address = allocate(len(data))
        write(address, data)
        return address | 0x8000000

    # Config
    config = cast(dict[str, str | int | bool], data["config"])
    goal = config.get("goal", "vanilla")
    seed_info = (
        int(data.get("player_number", 0)),
        cast(str, data.get("player_name", "")).encode("utf-8")[:64],
        cast(str, data.get("seed_name", "")).encode("utf-8")[:64],

        GOAL_MAPPING[goal],
        DIFFICULTY_MAPPING[config.get("difficulty", "either")],
        bool(config.get("remove_gravity_heat_resistance", False)),
        bool(config.get("power_bombs_without_bomb", False)),
        bool(config.get("buff_power_bomb_drops", False)),
        bool(config.get("skip_chozodia_stealth", False)),
        bool(config.get("start_with_maps", False)),
        bool(config.get("skip_tourian_opening_cutscenes", False)),
        2 * PIXEL_SIZE * int(config.get("elevator_speed", 1)),
    )
    write(
        get_rom_address("sRandoSeed"),
        struct.pack("<H64s64s2x9B", *seed_info)
    )

    if goal == "bosses":
        write(
            get_rom_address("sHatchLockEventsChozodia", 8 * 15 + 1),  # sHatchLockEventsChozodia[15].event
            struct.pack("<B", 0x27)  # EVENT_MOTHER_BRAIN_KILLED
        )
        write(
            get_rom_address("sNumberOfHatchLockEventsPerArea", 2 * 6),  # sNumberOfHatchLockEventsPerArea[AREA_CHOZODIA]
            struct.pack("<H", 16)
        )

    if config.get("chozodia_requires_mother_brain", False):
        write(
            get_rom_address("sNumberOfHatchLockEventsPerArea", 2 * 5),
            struct.pack("<H", 4)  # Mother Brain event locks
        )

    # Place items
    message_pointers: dict[tuple[str, str], int] = {}
    def get_message(first_line: str, second_line: str = "") -> int:
        if (first_line, second_line) in message_pointers:
            return message_pointers[(first_line, second_line)]
        message_bytes = make_item_message(first_line, second_line).to_bytes()
        message_ptr = write_to_arena(message_bytes)
        message_pointers[(first_line, second_line)] = message_ptr
        return message_ptr

    file_pointers: dict[str, int] = {}
    def get_file(name: str) -> int:
        if name in file_pointers:
            return file_pointers[name]
        file_bytes = data_path(f"item_sprites/{name}")
        file_ptr = write_to_arena(file_bytes)
        file_pointers[name] = file_ptr
        return file_ptr

    sprite_pointers: dict[str, int] = {**builtin_sprite_pointers}
    def get_sprite(name: str) -> int:
        if name in sprite_pointers:
            return sprite_pointers[name]
        gfx, pal = sprite_imports[name]
        gfx_pointer = gfx if type(gfx) is int else get_file(gfx)
        pal_pointer = pal if type(pal) is int else get_file(pal)
        sprite = struct.pack("<II", gfx_pointer, pal_pointer)
        sprite_ptr = write_to_arena(sprite)
        sprite_pointers[name] = sprite_ptr
        return sprite_ptr

    locations = cast(list[dict[str, Any]], data["locations"])
    for location in locations:
        location_id = cast(int, location["id"])
        item_name = cast(str, location["item"])
        sprite_name = cast(str | None, location.get("sprite"))
        message = cast(str | None, location.get("message"))

        item_data = item_data_table[item_name]
        sprite_pointer = get_sprite(item_data.sprite if sprite_name is None else sprite_name)
        if message is None:
            if type(item_data.message) is int:
                message_pointer = item_data.message
                one_line = True
            else:
                message = cast(str, item_data.message)
        if message is not None:
            message_lines = message.splitlines()
            one_line = len(message_lines) <= 1
            message_pointer = get_message(*message_lines)
        sound = 0x4A if location_id == RUINS_TEST_LOCATION_ID else item_data.sound
        write(
            get_rom_address("sPlacedItems", 16 * location_id),
            struct.pack(
                "<BBHIIHBB",
                item_data.type, False, item_data.bits,
                sprite_pointer,
                message_pointer, sound, item_data.acquisition, one_line
            )
        )

    # Starting inventory
    pickups = [0, 0, 0, 0]
    beams = misc = custom = 0
    start_inventory = cast(dict[str, int | bool], data.get("start_inventory"))
    for item_name, value in start_inventory.items():
        item_data = item_data_table[item_name]
        if value <= 0:
            continue
        if item_data.type == ItemType.BEAM:
            beams |= item_data.bits
        elif item_data.type == ItemType.MAJOR:
            misc |= item_data.bits
        elif item_data.type == ItemType.CUSTOM:
            custom |= item_data.bits
        elif item_data.type <= ItemType.POWER_BOMB_TANK:
            pickups[item_data.type - 1] = value
    write(
        get_rom_address("sRandoStartingInventory"),
        struct.pack("<BxHBBBBB", *pickups, beams, misc, custom)
    )

    # Write text
    text = cast(dict[str, dict[str, str]], data.get("text", {}))
    for group, messages in text.items():
        for name, message in messages.items():
            array_index = TEXT_INDICES[(group, name)]
            encoded_message = Message(message).append(TERMINATOR_CHAR)
            text_address = write_to_arena(encoded_message.to_bytes())
            write(
                get_rom_address(f"sEnglishTextPointers_{group}", 4 * array_index),
                struct.pack("<I", text_address)
            )

    return bytes(local_rom)
