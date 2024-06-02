"""
Classes and functions related to creating a ROM patch
"""
from __future__ import annotations

import bsdiff4
import hashlib
from pathlib import Path
import struct
from typing import TYPE_CHECKING, Iterable, Union

import Utils
from worlds.Files import APDeltaPatch

from .data import data_path, encode_str, get_rom_symbol
from .items import AP_MZM_ID_BASE

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

        location_id = location.address - AP_MZM_ID_BASE
        if location.native_item:
            item_id = item.code - AP_MZM_ID_BASE
            item_name = None
        else:
            item_id = 21 + item.classification.as_flag().bit_length()
            item_name = item.name
        if item.player == player:
            player_name = None
        else:
            player_name = multiworld.player_name[item.player]

        for name in (player_name, item_name):
            if name not in names:
                names[name] = next_name_address
                encoded = encode_str(name[:32]) + 0xFF00.to_bytes(2, "little")
                rom.write_bytes(next_name_address, encoded)
                next_name_address += len(encoded)

        placement = names[player_name], names[item_name], item_id
        address = get_rom_symbol("sPlacedItems", 12 * location_id)
        rom.write_bytes(address, struct.pack("<IIB", *placement))
