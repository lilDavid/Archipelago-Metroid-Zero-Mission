"""
Classes and functions related to creating a ROM patch
"""
from __future__ import annotations

import hashlib
import logging
from pathlib import Path
import struct
from typing import TYPE_CHECKING, Sequence

from BaseClasses import ItemClassification, Location
import Utils
from worlds.Files import APPatchExtension, APProcedurePatch, APTokenMixin, APTokenTypes, InvalidDataError

from . import rom_data
from .data import APWORLD_VERSION, get_rom_address, get_symbol, symbols_hash
from .items import AP_MZM_ID_BASE, ItemID, ItemType, item_data_table
from .nonnative_items import get_zero_mission_sprite
from .options import ChozodiaAccess, DisplayNonLocalItems, Goal
from .text import TERMINATOR_CHAR, Message

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
    def add_decompressed_graphics(caller: APProcedurePatch, rom: bytes):
        return rom_data.add_item_sprites(rom)

    @staticmethod
    def add_unknown_item_graphics(caller: APProcedurePatch, rom: bytes) -> bytes:
        return rom_data.use_unknown_item_sprites(rom)

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

    def __init__(self, *args, **kwargs):
        super(MZMProcedurePatch, self).__init__(*args, **kwargs)
        self.procedure = [
            ("check_symbol_hash", [symbols_hash, APWORLD_VERSION]),
            ("support_vc", []),
            ("apply_bsdiff4", ["basepatch.bsdiff"]),
            ("apply_tokens", ["token_data.bin"]),
            ("add_decompressed_graphics", []),
            ("apply_background_patches", []),
        ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_base_rom_path(), "rb") as stream:
            return stream.read()

    def add_vanilla_unknown_item_sprites(self):
        self.procedure.append(("add_unknown_item_graphics", []))

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

    if item.advancement or item.trap:
        sprite = ItemID.APItemProgression
    elif item.useful:
        sprite = ItemID.APItemUseful
    else:
        sprite = ItemID.APItemFiller
    name = Message(item.name).trim_to_max_width().insert(0, 0x8105)
    pad = ((224 - name.display_width()) // 2) & 0xFF
    name.insert(0, 0x8000 | pad)
    return sprite, name


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
        world.options.unknown_items_always_usable.value,
        True,  # Remove Gravity Suit heat resistance
        True,  # Make Power Bombs usable without Bomb
        world.options.buff_pb_drops.value,
        world.options.skip_chozodia_stealth.value,
        world.options.start_with_maps.value,
        world.options.fast_item_banners.value,
        world.options.skip_tourian_opening_cutscenes.value,
        world.options.elevator_speed.value,
    )
    patch.write_token(
        APTokenTypes.WRITE,
        get_rom_address("sRandoSeed"),
        struct.pack("<H64s64s2x11B", *seed_info)
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
            player_name = Message(multiworld.player_name[item.player])

        for name in (player_name, item_name):
            if name not in names:
                names[name] = next_name_address | 0x8000000
                name.append(TERMINATOR_CHAR)
                name_bytes = name.to_bytes()
                patch.write_token(
                    APTokenTypes.WRITE,
                    next_name_address,
                    name_bytes
                )
                next_name_address += len(name_bytes)

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
