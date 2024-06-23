"""
Classes and functions related to creating a ROM patch
"""
from __future__ import annotations

from pathlib import Path
import struct
from typing import TYPE_CHECKING

from BaseClasses import Location
import Utils
from worlds.Files import APPatchExtension, APProcedurePatch, APTokenMixin, APTokenTypes

from . import rom_data
from .data import encode_str, get_symbol, get_width_of_encoded_string
from .items import AP_MZM_ID_BASE, ItemType, item_data_table
from .nonnative_items import get_zero_mission_sprite
from .options import DisplayNonLocalItems

if TYPE_CHECKING:
    from . import MZMWorld


MD5_MZMUS = "ebbce58109988b6da61ebb06c7a432d5"


def get_rom_address(name, offset=0):
    address = get_symbol(name, offset)
    if not address & 0x8000000:
        raise ValueError(f"{name}+{offset} is not in ROM (address: {address:07x})")
    return address & 0x8000000 - 1


class MZMPatchExtensions(APPatchExtension):
    game = "Metroid Zero Mission"

    @staticmethod
    def add_decompressed_graphics(caller: APProcedurePatch, rom: bytes) -> bytes:
        return rom_data.add_item_sprites(rom)


class MZMProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Metroid Zero Mission"
    hash = MD5_MZMUS
    patch_file_ending = ".apmzm"
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["basepatch.bsdiff"]),
        ("apply_tokens", ["token_data.bin"]),
        ("add_decompressed_graphics", []),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_base_rom_path(), "rb") as stream:
            return stream.read()


def get_base_rom_path(file_name: str = "") -> Path:
    options = Utils.get_options()
    if not file_name:
        file_name = options["mzm_options"]["rom_file"]

    file_path = Path(file_name)
    if file_path.exists():
        return file_path
    else:
        return Path(Utils.user_path(file_name))


def get_item_sprite_and_name(location: Location, world: MZMWorld):
    player = world.player
    nonlocal_item_handling = world.options.display_nonlocal_items
    item = location.item

    if location.native_item and (nonlocal_item_handling != DisplayNonLocalItems.option_none or item.player == player):
        sprite = item.code - AP_MZM_ID_BASE
        return sprite, None

    if nonlocal_item_handling == DisplayNonLocalItems.option_match_series:
        sprite = get_zero_mission_sprite(item)
        if sprite is not None:
            return sprite, None

    sprite = 21 + item.classification.as_flag().bit_length()
    name = encode_str(item.name[:32])
    pad = ((224 - get_width_of_encoded_string(name)) // 2) & 0xFF
    name = struct.pack("<HH", 0x8000 | pad, 0x8105) + name
    return sprite, name


def write_tokens(world: MZMWorld, patch: MZMProcedurePatch):
    multiworld = world.multiworld
    player = world.player

    # Basic information about the seed
    seed_info = (
        player,
        multiworld.player_name[player].encode("utf-8")[:64],
        multiworld.seed_name.encode("utf-8")[:64],

        world.options.unknown_items_always_usable.value,
        world.options.skip_chozodia_stealth.value,
    )
    patch.write_token(
        APTokenTypes.WRITE,
        get_rom_address("sRandoSeed"),
        struct.pack("<H64s64s2xBB", *seed_info)
    )

    # Place items
    next_name_address = get_rom_address("sRandoItemAndPlayerNames")
    names = {None: 0}
    for location in multiworld.get_locations(player):
        item = location.item
        if item.code is None or location.address is None:
            continue

        item_id, item_name = get_item_sprite_and_name(location, world)
        if item.player == player:
            player_name = None
        else:
            player_name = encode_str(multiworld.player_name[item.player])

        for name in (player_name, item_name):
            if name not in names:
                names[name] = next_name_address | 0x8000000
                terminated = name + 0xFF00.to_bytes(2, "little")
                patch.write_token(
                    APTokenTypes.WRITE,
                    next_name_address,
                    terminated
                )
                next_name_address += len(terminated)

        location_id = location.address - AP_MZM_ID_BASE
        placement = names[player_name], names[item_name], item_id
        patch.write_token(
            APTokenTypes.WRITE,
            get_rom_address("sPlacedItems", 12 * location_id),
            struct.pack("<IIB", *placement),
        )

    # Create starting inventory
    pickups = [0, 0, 0, 0]
    beams = misc = 0
    for item in multiworld.precollected_items[player]:
        data = item_data_table[item.name]
        if data.type == ItemType.beam:
            beams |= data.bits
        if data.type == ItemType.major:
            misc |= data.bits
        if data.type == ItemType.tank and (
            data.id == 1 and pickups[1] < 999
            or pickups[data.id] < 99
        ):
            pickups[data.id] += 1
    patch.write_token(
        APTokenTypes.WRITE,
        get_rom_address("sRandoStartingInventory"),
        struct.pack("<BxHBBBB", *pickups, beams, misc)
    )

    patch.write_file("token_data.bin", patch.get_token_binary())
