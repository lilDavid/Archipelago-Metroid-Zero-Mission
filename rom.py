"""
Classes and functions related to creating a ROM patch
"""
from __future__ import annotations

import bsdiff4
import hashlib
from pathlib import Path
import struct
from typing import TYPE_CHECKING, Iterable, Union

from BaseClasses import Location
import Utils
from worlds import sm
from worlds.smz3.TotalSMZ3.Item import ItemType as SMZ3Item, items_start_id as smz3_items_start_id
from worlds.Files import APDeltaPatch

from .data import data_path, encode_str, get_rom_symbol, get_width_of_encoded_string
from .items import AP_MZM_ID_BASE
from .options import DisplayNonLocalItems

if TYPE_CHECKING:
    from . import MZMWorld


MD5_MZMUS = "ebbce58109988b6da61ebb06c7a432d5"


class MZMDeltaPatch(APDeltaPatch):
    game = "Metroid Zero Mission"
    hash = MD5_MZMUS
    patch_file_ending = ".apmzm"
    result_file_ending = ".gba"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_path = get_base_rom_path(file_name)
        base_rom_bytes = bytes(open(file_path, "rb").read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() != MD5_MZMUS:
            raise Exception("Supplied base ROM does not match the US version of "
                            "Metroid Zero Mission. Please provide the correct "
                            "ROM version")

        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> Path:
    options = Utils.get_options()
    if not file_name:
        file_name = options["mzm_options"]["rom_file"]

    file_path = Path(file_name)
    if file_path.exists():
        return file_path
    else:
        return Path(Utils.user_path(file_name))


class LocalRom:
    def __init__(self, file: Path, name=None, hash=None):
        self.name = name
        self.hash = hash

        with open(file, "rb") as rom_file:
            rom_bytes = rom_file.read()
        patch_bytes = data_path("basepatch.bsdiff")
        self.buffer = bytearray(bsdiff4.patch(rom_bytes, patch_bytes))

    def get_address(self, address: Union[int, str]):
        if isinstance(address, str):
            address = get_rom_symbol(address)
        return address & (0x8000000 - 1)

    def read_byte(self, address: Union[int, str]):
        return self.buffer[self.get_address(address)]

    def read_bytes(self, address: Union[int, str], length: int, align: int = 1):
        address = self.get_address(address)
        if address % align != 0:
            raise ValueError(f"Misaligned address {address:06x} for alignment {align}")
        return self.buffer[address:address + length]

    def read_int(self, address: Union[int, str], size: int, align: int = 1):
        value = self.read_bytes(address, size, align)
        return int.from_bytes(value, "little")

    def read_halfword(self, address: Union[int, str]):
        return self.read_int(address, 2, 2)

    def read_word(self, address: Union[int, str]):
        return self.read_int(address, 4, 4)

    def write_byte(self, address: Union[int, str], value: int):
        self.buffer[self.get_address(address)] = value

    def write_bytes(self, address: Union[int, str], values: Iterable[int], align: int = 1):
        address = self.get_address(address)
        if address % align != 0:
            raise ValueError(f"Misaligned address {address:06x} for alignment {align}")
        self.buffer[address:address + len(values)] = values

    def write_int(self, address: Union[int, str], value: int, size: int, align: int = 1):
        self.write_bytes(address, value.to_bytes(size, "little"), align)

    def write_halfword(self, address: Union[int, str], value: int):
        self.write_int(self, address, value, 2, 2)

    def write_word(self, address: Union[int, str], value: int):
        self.write_int(self, address, value, 4, 4)

    def write_to_file(self, file: Path):
        with open(file, "wb") as stream:
            stream.write(self.buffer)


sm_id_to_mzm_id = {
    0: 0,  # Energy Tank
    1: 1,  # Missile Tank
    2: 2,  # Super Missile Tank
    3: 3,  # Power Bomb Tank
    4: 9,  # Bomb
    5: 5,  # Charge Beam
    6: 6,  # Ice Beam
    7: 14,  # Hi-Jump Boots
    8: 13,  # Speed Booster
    9: 7,  # Wave Beam
    # 10:  # Spazer Beam
    # 11:  # Spring Ball
    12: 10,  # Varia Suit
    15: 8,  # Plasma Beam
    # 16:  # Grapple Beam
    19: 12,  # Morph Ball
    # 20:  # Reserve Tank
    13: 11,  # Gravity Suit
    # 14:  # X-Ray Scope
    17: 16,  # Space Jump
    18: 15,  # Screw Attack
}

smz3_id_to_mzm_id = {
    SMZ3Item.Missile.value: 1,
    SMZ3Item.Super.value: 2,
    SMZ3Item.PowerBomb.value: 3,
    # SMZ3Item.Grapple.value:
    # SMZ3Item.XRay.value:
    SMZ3Item.ETank.value: 0,
    # SMZ3Item.ReserveTank:
    SMZ3Item.Charge.value: 5,
    SMZ3Item.Ice.value: 6,
    SMZ3Item.Wave.value: 7,
    # SMZ3Item.Spazer.value:
    SMZ3Item.Plasma.value: 8,
    SMZ3Item.Varia.value: 10,
    SMZ3Item.Gravity.value: 11,
    SMZ3Item.Morph.value: 12,
    SMZ3Item.Bombs.value: 9,
    # SMZ3Item.SpringBall.value:
    SMZ3Item.ScrewAttack.value: 15,
    SMZ3Item.HiJump.value: 14,
    SMZ3Item.SpaceJump.value: 16,
    SMZ3Item.SpeedBooster.value: 13,
}


def get_item_sprite_and_name(location: Location, world: MZMWorld):
    player = world.player
    nonlocal_item_handling = world.options.display_nonlocal_items
    item = location.item

    if location.native_item and (nonlocal_item_handling != DisplayNonLocalItems.option_none or item.player == player):
        sprite = item.code - AP_MZM_ID_BASE
        return sprite, None

    if nonlocal_item_handling == DisplayNonLocalItems.option_match_series:
        if item.game == "Super Metroid" and item.code - sm.items_start_id in sm_id_to_mzm_id:
            sprite = sm_id_to_mzm_id[item.code - sm.items_start_id]
            return sprite, None

        if item.game == "SMZ3" and item.code - smz3_items_start_id in smz3_id_to_mzm_id:
            sprite = smz3_id_to_mzm_id[item.code - smz3_items_start_id]
            return sprite, None

    sprite = 21 + item.classification.as_flag().bit_length()
    name = encode_str(item.name[:32])
    pad = ((224 - get_width_of_encoded_string(name)) // 2) & 0xFF
    name = struct.pack("<HH", 0x8000 | pad, 0x8105) + name
    return sprite, name


def patch_rom(rom: LocalRom, world: MZMWorld):
    multiworld = world.multiworld
    player = world.player

    # Basic information about the seed
    seed_info = (
        player,
        multiworld.player_name[player].encode("utf-8")[:64],
        multiworld.seed_name.encode("utf-8")[:64],

        world.options.unknown_items_always_usable.value,
    )
    rom.write_bytes("sRandoSeed", struct.pack("<H64s64s2xB", *seed_info))

    # Place items
    next_name_address = get_rom_symbol("sRandoItemAndPlayerNames")
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
                names[name] = next_name_address
                terminated = name + 0xFF00.to_bytes(2, "little")
                rom.write_bytes(next_name_address, terminated)
                next_name_address += len(terminated)

        location_id = location.address - AP_MZM_ID_BASE
        placement = names[player_name], names[item_name], item_id
        address = get_rom_symbol("sPlacedItems", 12 * location_id)
        rom.write_bytes(address, struct.pack("<IIB", *placement))
