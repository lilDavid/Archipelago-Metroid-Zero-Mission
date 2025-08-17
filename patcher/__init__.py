from __future__ import annotations

import hashlib
import logging
import pkgutil
import struct
from typing import Literal, NotRequired, TypedDict, cast

import bsdiff4

from .backgrounds import patch_chozodia_spotlight, write_item_clipdata_and_gfx
from .constants import RC_COUNT, PIXEL_SIZE, Area, Event, ItemType
from .items import item_data_table
from .layout_patches import apply_layout_patches
from .local_rom import LocalRom, get_rom_address
from .sprites import builtin_sprite_pointers, sprite_imports, write_decompressed_item_sprites
from .text import TERMINATOR_CHAR, Message, make_item_message


MD5_US = "ebbce58109988b6da61ebb06c7a432d5"
MD5_US_VC = "e23c14997c2ea4f11e5996908e577125"


class PatchJson(TypedDict):
    player_name: NotRequired[str]
    seed_name: NotRequired[str]
    config: SeedConfig
    locations: list[Location]
    start_inventory: NotRequired[dict[str, int | bool]]
    text: NotRequired[dict[str, dict[str, str]]]
    layout_patches: NotRequired[list[str] | Literal["all"]]


class SeedConfig(TypedDict):
    goal: NotRequired[Literal["vanilla", "bosses"]]
    difficulty: NotRequired[Literal["normal", "hard", "either"]]
    remove_gravity_heat_resistance: NotRequired[bool]
    power_bombs_without_bomb: NotRequired[bool]
    buff_power_bomb_drops: NotRequired[bool]
    separate_hijump_springball: NotRequired[bool]
    skip_chozodia_stealth: NotRequired[bool]
    chozodia_requires_mother_brain: NotRequired[bool]
    start_with_maps: NotRequired[bool]
    reveal_maps: NotRequired[bool]
    reveal_hidden_blocks: NotRequired[bool]
    skip_tourian_opening_cutscenes: NotRequired[bool]
    elevator_speed: NotRequired[int]


class Location(TypedDict):
    id: int
    item_name: str
    sprite_name: NotRequired[str | None]
    message: NotRequired[str | None]


GOAL_MAPPING = {
    "vanilla": 0,
    "bosses": 1,
}


DIFFICULTY_MAPPING = {
    "normal": 0b01,
    "hard": 0b10,
    "either": 0b11,
}


RUINS_TEST_LOCATION_ID = 100


# TODO: Support overriding more text
TEXT_INDICES = {
    "Story": {
        "Intro": 0,
        "Escape 1": 1,
        "Escape 2": 2,
    }
}


def patch_rom(data: bytes, patch: PatchJson) -> bytes:
    rom = LocalRom(apply_basepatch(data))

    write_seed_config(rom, patch)

    write_decompressed_item_sprites(rom)
    place_items(rom, patch["locations"])
    write_start_inventory(rom, patch.get("start_inventory", {}))

    write_item_clipdata_and_gfx(rom)
    patch_chozodia_spotlight(rom)
    apply_layout_patches(rom, patch.get("layout_patches", []))

    write_text(rom, patch.get("text", {}))

    return rom.to_bytes()


def apply_basepatch(rom: bytes) -> bytes:
    basepatch = pkgutil.get_data(__name__, "data/basepatch.bsdiff")

    hasher = hashlib.md5()
    hasher.update(rom)
    if hasher.hexdigest() == MD5_US:
        return bsdiff4.patch(rom, basepatch)

    logging.warning("You appear to be using a Virtual Console ROM. "
                    "This is not officially supported and may cause bugs.")
    entry_point = (0xEA00002E).to_bytes(4, 'little')  # b 0x80000C0
    return bsdiff4.patch(entry_point + rom[4:], basepatch)


def write_seed_config(rom: LocalRom, patch: PatchJson):
    config = patch["config"]
    seed_info = (
        patch.get("player_name", "").encode("utf-8")[:64],
        patch.get("seed_name", "").encode("utf-8")[:64],

        DIFFICULTY_MAPPING[config.get("difficulty", "either")],
        config.get("remove_gravity_heat_resistance", False),
        config.get("power_bombs_without_bomb", False),
        config.get("buff_power_bomb_drops", False),
        config.get("separate_hijump_springball", False),
        config.get("skip_chozodia_stealth", False),
        config.get("start_with_maps", False),
        config.get("reveal_maps", False),
        config.get("reveal_hidden_blocks", False),
        config.get("skip_tourian_opening_cutscenes", False),
        2 * PIXEL_SIZE * config.get("elevator_speed", 1),
    )
    rom.write(get_rom_address("sRandoSeed"), struct.pack("<64s64s11B", *seed_info))

    if config.get("goal", "vanilla") == "bosses":
        rom.write(
            get_rom_address("sHatchLockEventsChozodia", 8 * 15 + 1),  # sHatchLockEventsChozodia[15].event
            struct.pack("<B", Event.MOTHER_BRAIN_KILLED)
        )
        rom.write(get_rom_address("sNumberOfHatchLockEventsPerArea", 2 * Area.CHOZODIA), struct.pack("<H", 16))

    if config.get("chozodia_requires_mother_brain", False):
        rom.write(get_rom_address("sNumberOfHatchLockEventsPerArea", 2 * Area.TOURIAN), struct.pack("<H", 4))

    if config.get("reveal_maps"):
        rom.write(get_rom_address("sMinimapTilesPal"), pkgutil.get_data(__name__, "data/revealed_map_tile.pal"))


def place_items(rom: LocalRom, locations: list[Location]):
    message_pointers: dict[tuple[str, str], int] = {}
    def get_or_insert_message(first_line: str, second_line: str = "") -> int:
        if (first_line, second_line) in message_pointers:
            return message_pointers[(first_line, second_line)]
        message_bytes = make_item_message(first_line, second_line).to_bytes()
        message_ptr = rom.append(message_bytes)
        message_pointers[(first_line, second_line)] = message_ptr
        return message_ptr

    file_pointers: dict[str, int] = {}
    def get_or_insert_file(name: str) -> int:
        if name in file_pointers:
            return file_pointers[name]
        file_bytes = pkgutil.get_data(__name__, f"data/item_sprites/{name}")
        file_ptr = rom.append(file_bytes)
        file_pointers[name] = file_ptr
        return file_ptr

    sprite_pointers: dict[str, int] = {**builtin_sprite_pointers}
    def get_or_insert_sprite(name: str) -> int:
        if name in sprite_pointers:
            return sprite_pointers[name]
        gfx, pal = sprite_imports[name]
        gfx_pointer = gfx if type(gfx) is int else get_or_insert_file(gfx)
        pal_pointer = pal if type(pal) is int else get_or_insert_file(pal)
        sprite = struct.pack("<II", gfx_pointer, pal_pointer)
        sprite_ptr = rom.append(sprite)
        sprite_pointers[name] = sprite_ptr
        return sprite_ptr

    placed_items: set[int] = set()
    for location in locations:
        location_id = location["id"]
        if location_id >= RC_COUNT or location_id < 0:
            raise ValueError(f"Invalid location ID: {location_id}")
        item_name = location["item"]
        sprite_name = location.get("sprite")
        message = location.get("message")

        item_data = item_data_table[item_name]
        sprite_pointer = get_or_insert_sprite(item_data.sprite if sprite_name is None else sprite_name)
        if message is None:
            if type(item_data.message) is int:
                message_pointer = item_data.message
                one_line = True
            else:
                message = cast(str, item_data.message)
        if message is not None:
            message_lines = message.splitlines()
            one_line = len(message_lines) <= 1
            message_pointer = get_or_insert_message(*message_lines)
        sound = 0x4A if location_id == RUINS_TEST_LOCATION_ID else item_data.sound
        rom.write(
            get_rom_address("sPlacedItems", 16 * location_id),
            struct.pack(
                "<BBHIIHBB",
                item_data.type, False, item_data.bits,
                sprite_pointer,
                message_pointer, sound, item_data.acquisition, one_line
            )
        )
        placed_items.add(location_id)

    for i in range(RC_COUNT):
        if i not in placed_items:
            item_data = item_data_table["Nothing"]
            rom.write(
                get_rom_address("sPlacedItems", 16 * i),
                struct.pack(
                    "<BBHIIHBB",
                    item_data.type, False, item_data.bits,
                    get_or_insert_sprite(item_data.sprite),
                    get_or_insert_message(item_data.message), item_data.sound, item_data.acquisition, True
                )
            )


def write_start_inventory(rom: LocalRom, start_inventory: dict[str, int | bool]):
    pickups = [0, 0, 0, 0]
    beams = misc = custom = 0
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
    rom.write(
        get_rom_address("sRandoStartingInventory"),
        struct.pack("<BxHBBBBB", *pickups, beams, misc, custom)
    )


def write_text(rom: LocalRom, text: dict[str, dict[str, str]]):
    for group, messages in text.items():
        for name, message in messages.items():
            array_index = TEXT_INDICES[group][name]
            encoded_message = Message(message).append(TERMINATOR_CHAR)
            text_address = rom.append(encoded_message.to_bytes())
            rom.write(
                get_rom_address(f"sEnglishTextPointers_{group}", 4 * array_index),
                struct.pack("<I", text_address)
            )
