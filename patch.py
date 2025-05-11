"""
Classes and functions related to creating a ROM patch
"""
from __future__ import annotations

import json
import hashlib
import logging
from pathlib import Path
import struct
from typing import TYPE_CHECKING, Any, Sequence, cast

from BaseClasses import Location
import Utils
from worlds.Files import APPatchExtension, APProcedurePatch, APTokenMixin, APTokenTypes, InvalidDataError

from . import rom_data
from .data import APWORLD_VERSION, data_path, get_rom_address, get_symbol, symbols_hash
from .items import ItemType, item_data_table
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
    def check_symbol_hash(caller: APProcedurePatch, rom: bytes, hash: str, *args):
        if hash == symbols_hash:
            return rom
        if len(args) == 0:
            raise InvalidDataError("Memory addresses don't match. This patch was generated with an older version of "
                                   "the apworld.")

        expected_version = args[0]
        if APWORLD_VERSION is None:
            if expected_version is None:
                error_msg = "This patch was generated with a different base patch."
            else:
                error_msg = (f"This patch was generated with version {expected_version}, "
                             "which has a different base patch.")
        else:
            if expected_version is None:
                error_msg = ("This patch was likely generated using the source code, "
                             f"and you are using version {APWORLD_VERSION}.")
            else:
                error_msg = (f"This patch was generated with version {expected_version}, "
                             f"and you are using version {APWORLD_VERSION}.")
        raise InvalidDataError(f"Memory addresses don't match. {error_msg}")

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
    def apply_json(caller: APProcedurePatch, rom: bytes, file_name: str):
        return apply_json_data(rom, json.loads(caller.get_file("patch.json").decode()))

    @staticmethod
    def add_decompressed_graphics(caller: APProcedurePatch, rom: bytes):
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
            ("check_symbol_hash", [symbols_hash, APWORLD_VERSION]),
            ("support_vc", []),
            ("apply_bsdiff4", ["basepatch.bsdiff"]),
            ("apply_tokens", ["token_data.bin"]),
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


def write_tokens(world: MZMWorld, patch: MZMProcedurePatch):
    multiworld = world.multiworld
    player = world.player

    # Basic information about the seed
    seed_info = (
        player,
        world.player_name.encode("utf-8")[:64],
        multiworld.seed_name.encode("utf-8")[:64],

        world.options.goal.value,
        world.options.game_difficulty.value,
        True,  # Remove Gravity Suit heat resistance
        True,  # Make Power Bombs usable without Bomb
        world.options.buff_pb_drops.value,
        world.options.skip_chozodia_stealth.value,
        world.options.start_with_maps.value,
        world.options.skip_tourian_opening_cutscenes.value,
        world.options.elevator_speed.value,
    )
    patch.write_token(
        APTokenTypes.WRITE,
        get_rom_address("sRandoSeed"),
        struct.pack("<H64s64s2x9B", *seed_info)
    )

    # Set goal
    if world.options.goal.value != Goal.option_mecha_ridley:
        patch.write_token(
            APTokenTypes.WRITE,
            get_rom_address("sHatchLockEventsChozodia", 8 * 15 + 1),  # sHatchLockEventsChozodia[15].event
            (0x27).to_bytes(1, 'little'),  # EVENT_MOTHER_BRAIN_KILLED
        )
        patch.write_token(
            APTokenTypes.WRITE,
            get_rom_address("sNumberOfHatchLockEventsPerArea", 2 * 6),  # sNumberOfHatchLockEventsPerArea[AREA_CHOZODIA]
            (16).to_bytes(2, 'little')
        )

    # Create starting inventory
    pickups = [0, 0, 0, 0]
    beams = misc = custom = 0
    for item in multiworld.precollected_items[player]:
        data = item_data_table[item.name]
        if data.type == ItemType.BEAM:
            beams |= data.bits
        elif data.type == ItemType.MAJOR:
            misc |= data.bits
        elif data.type == ItemType.CUSTOM:
            custom |= data.bits
        elif (data.type == ItemType.MISSILE_TANK and pickups[1] < 999 or pickups[data.type - 1] < 99):
            pickups[data.type - 1] += 1
    patch.write_token(
        APTokenTypes.WRITE,
        get_rom_address("sRandoStartingInventory"),
        struct.pack("<BxHBBBBB", *pickups, beams, misc, custom)
    )

    if world.options.chozodia_access == ChozodiaAccess.option_closed:
        patch.write_token(
            APTokenTypes.WRITE,
            get_rom_address("sNumberOfHatchLockEventsPerArea", 2 * 5),
            struct.pack("<H", 4)  # Acknowledge Mother Brain event locks
        )

    # Write new intro text
    world_version = f" / APworld {APWORLD_VERSION}" if APWORLD_VERSION is not None else ""
    intro_text = (f"AP {multiworld.seed_name}\n"
                  f"P{player} - {world.player_name}\n"
                  f"Version {Utils.version_tuple.as_simple_string()}{world_version}\n"
                  "\n"
                  f"YOUR MISSION: {goal_texts[world.options.goal.value]}")
    encoded_intro = Message(intro_text).append(TERMINATOR_CHAR)
    assert len(encoded_intro) <= 235  # Original intro text is 235 characters
    patch.write_token(
        APTokenTypes.WRITE,
        get_rom_address("sEnglishText_Story_PlanetZebes"),
        encoded_intro.to_bytes()
    )

    # Write new ZSS text
    zss_text = ("With Mother Brain taken down, I needed\n"
                "to get my suit back in the ruins.\n")
    plasma_beam = world.create_item("Plasma Beam")
    if world.options.plasma_beam_hint.value and plasma_beam not in multiworld.precollected_items[player]:
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
    else:
        zss_text += "\nCould I survive long enough to escape?"
    encoded_zss_text = Message(zss_text).append(TERMINATOR_CHAR)
    assert len(encoded_zss_text) < 339
    patch.write_token(
        APTokenTypes.WRITE,
        get_rom_address("sEnglishText_Story_TheTiming"),
        encoded_zss_text.to_bytes()
    )
    patch.write_token(
        APTokenTypes.WRITE,
        get_rom_address("sEnglishTextPointers_Story", 4 * 2),  # Could I survive...?
        get_symbol("sEnglishText_Story_TheTiming").to_bytes(4, "little")
    )

    patch.write_file("token_data.bin", patch.get_token_binary())

def write_json_data(world: MZMWorld, patch: MZMProcedurePatch):
    multiworld = world.multiworld
    player = world.player

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

    patch.write_file(
        "patch.json",
        json.dumps({
            "locations": locations,
        }).encode()
    )


RUINS_TEST_LOCATION_ID = 100


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

    return bytes(local_rom)
