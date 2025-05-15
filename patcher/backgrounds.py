from enum import IntEnum
import itertools
import struct
from typing import NamedTuple

from . import iterators, lz10, rle
from .constants import Area
from .local_rom import ROM_START, LocalRom, get_rom_address


class Clipdata(IntEnum):
    AIR = 0x00
    SOLID = 0x10
    STEEP_SLOPE_RISING = 0x11  # Positive gradient, like /
    ELEVATOR_UP = 0x29
    VERY_DUSTY_GROUND = 0x2D
    BEAM_BLOCK_NEVER_REFORM = 0x52
    LARGE_BEAM_BLOCK_NW_NO_REFORM = 0x53
    LARGE_BEAM_BLOCK_NE_NO_REFORM = 0x54
    BEAM_BLOCK_NO_REFORM = 0x55
    PITFALL_BLOCK = 0x56
    BOMB_BLOCK_NEVER_REFORM = 0x57
    SPEED_BOOSTER_BLOCK_NO_REFORM = 0x5A
    ENERGY_TANK = 0x5C
    MISSILE_TANK = 0x5D
    BEAM_BLOCK_REFORM = 0x62
    LARGE_BEAM_BLOCK_SW_NO_REFORM = 0x63
    LARGE_BEAM_BLOCK_SE_NO_REFORM = 0x64
    PITFALL_BLOCK_SLOW = 0x66
    BOMB_BLOCK_REFORM = 0x67
    SPEED_BOOSTER_BLOCK_REFORM = 0x6A
    SCREW_ATTACK_BLOCK_NO_REFORM = 0x6B
    HIDDEN_ENERGY_TANK = 0x6C
    UNDERWATER_ENERGY_TANK = 0x7C


class BackgroundProperties(IntEnum):
    NONE = 0
    RLE_COMPRESSED = 0x10
    LZ77_COMPRESSED = 0x40
    DARK_ROOM = LZ77_COMPRESSED | 5
    STARTS_FROM_BOTTOM = LZ77_COMPRESSED | 6


class BackgroundInfo(NamedTuple):
    rom: LocalRom
    properties: BackgroundProperties
    data_ptr: int

    @classmethod
    def from_data(cls, rom: LocalRom, prop: int, data_ptr: int):
        return cls(rom, BackgroundProperties(prop), data_ptr)

    def rom_address(self):
        return self.data_ptr & (ROM_START - 1)

    def compressed_data(self):
        return self.rom.view(self.rom_address())


class SpriteData(NamedTuple):
    y: int
    x: int
    spriteset_index: int

    @classmethod
    def terminator(cls):
        return cls(255, 255, 255 - 17)

    @classmethod
    def unpack(cls, data: bytes):
        y, x, i = struct.unpack("<BBB", data)
        return cls(y, x, i - 17)

    @classmethod
    def iter_unpack(cls, data: bytes):
        for i in itertools.count(0, 3):
            packed = data[i:i + 3]
            self = cls.unpack(packed)
            yield self
            if self == cls.terminator():
                return

    def pack(self):
        return struct.pack("<BBB", self.y, self.x, 17 + self.spriteset_index)


class RoomInfo(NamedTuple):
    bg0: BackgroundInfo
    bg1: BackgroundInfo
    bg2: BackgroundInfo
    bg3: BackgroundInfo
    clipdata: BackgroundInfo
    default_sprite_data_address: int

    @classmethod
    def from_pointer(cls, rom: LocalRom, ptr: int):
        ptr &= (ROM_START - 1)
        (bg0_prop, bg1_prop, bg2_prop, bg3_prop,
         bg0_ptr, bg1_ptr, bg2_ptr, clipdata_ptr, bg3_ptr,
         default_sprite_ptr
        ) = rom.read(ptr, "<xBBBBxxxIIIIIxxxxI")
        bg0 = BackgroundInfo.from_data(rom, bg0_prop, bg0_ptr)
        bg1 = BackgroundInfo.from_data(rom, bg1_prop, bg1_ptr)
        bg2 = BackgroundInfo.from_data(rom, bg2_prop, bg2_ptr)
        bg3 = BackgroundInfo.from_data(rom, bg3_prop, bg3_ptr)
        clipdata = BackgroundInfo.from_data(rom, BackgroundProperties.RLE_COMPRESSED, clipdata_ptr)
        default_sprites = default_sprite_ptr
        return cls(bg0, bg1, bg2, bg3, clipdata, default_sprites)


class BackgroundTilemap:
    width: int
    height: int
    compression: BackgroundProperties
    bg_size: int | None
    decompressed: bytearray
    max_compressed_size: int | None

    def __init__(self, compressed_data: memoryview, compression: BackgroundProperties, max_compressed_size: int | None = None):
        if compression & BackgroundProperties.RLE_COMPRESSED:
            self.width = compressed_data[0]
            self.height = compressed_data[1]
            self.compression = BackgroundProperties.RLE_COMPRESSED
            self.decompressed = rle.decompress(compressed_data[2:])
        elif compression & BackgroundProperties.LZ77_COMPRESSED:
            self.bg_size = compressed_data[0]
            self.width = self.height = 256 // 8
            if self.bg_size & 1:
                self.width *= 2
            if self.bg_size & 2:
                self.height *= 2
            self.compression = BackgroundProperties.LZ77_COMPRESSED
            self.decompressed = lz10.decompress(compressed_data[4:])
        else:
            raise ValueError(f"Invalid background properties: {compression:02x}")
        self.max_compressed_size = max_compressed_size

    @classmethod
    def from_info(cls, info: BackgroundInfo, max_compressed_size: int | None = None):
        return cls(info.compressed_data(), info.properties, max_compressed_size)

    def set(self, x: int, y: int, tile: int, original_tile: int | None = None):
        index = (y * self.width + x) * 2
        if original_tile is not None:
            found_tile = int.from_bytes(self.decompressed[index:index + 2], "little")
            if found_tile != original_tile:
                raise ValueError(f"Unexpected tile at ({x}, {y}) (expected {original_tile:04x}, found {found_tile:04x})")
        self.decompressed[index:index + 2] = tile.to_bytes(2, "little")

    def to_compressed_data(self) -> bytes:
        if self.compression == BackgroundProperties.RLE_COMPRESSED:
            compressed_data = bytes((self.width, self.height)) + rle.compress(self.decompressed)
        if self.compression == BackgroundProperties.LZ77_COMPRESSED:
            compressed_data = self.bg_size.to_bytes(4, "little") + lz10.compress(self.decompressed)
        if self.max_compressed_size is not None and len(compressed_data) > self.max_compressed_size:
            raise ValueError(f"Compressed size over limit (size: {len(compressed_data)}, limit: {self.max_compressed_size})")
        return compressed_data

    def to_halfword_matrix(self) -> list[list[int]]:
        return tuple(iterators.batched(itertools.chain.from_iterable(struct.iter_unpack("<H", self.decompressed)), self.width))


# Tuples are: Clipdata offset, BG1 offset
item_clipdata_and_gfx: dict[Area, dict[int, list[tuple[int | None, int | None]]]] = {
    Area.BRINSTAR: {
        1: [(0x26, 0x54)],
        2: [(0xE, None)],
        12: [(0x34, 0x154)],
        14: [(0x97, 0x122)],
        15: [(0x1E, 0x9E)],
        19: [(0xE6, None), (0x68, 0x134)],
        21: [(0x35, 0x110)],
        23: [(0x10B, 0x220)],
        25: [(0x1A, 0x44)],
        29: [(0x30, 0x63)],
        40: [(0x17, 0x36)],
        41: [(0x5E, 0x10D), (0x9B, 0x184)],
    },
    Area.KRAID: {
        1: [(0x1B, 0xC5)],
        2: [(0x10F, 0x1E3)],
        4: [(0x21, 0x5A)],
        7: [(0x69, 0x166)],
        8: [(0x17E, 0x3A8)],
        9: [(0x3D, 0xCC)],
        10: [(0x69, 0xA2)],
        17: [(0x14, None)],
        21: [(0x16, 0x78)],
        26: [(0x33, 0x6C)],
        38: [(0xC, 0x35)],
    },
    Area.NORFAIR: {
        1: [(0x85, 0x154)],
        3: [(0x46, 0xB7)],
        4: [(0xC1, 0x16C)],
        5: [(0x3E6, 0x6B7), (0x5D4, 0x9AF)],
        10: [(0x34, 0x60)],
        17: [(0x17, 0x53)],
        28: [(0x3C, None), (0x55, 0xA7)],
        32: [(0x4f, 0xC2), (0x30, 0x8D)],
        37: [(0x10, None)],
        38: [(0x29, 0x87)],
        42: [(0x26, None)],
        46: [(0x25, None)],
        47: [(0x11, None)],
        55: [(0x6F, 0xF6), (0xD6, 0x1D9)]
    },
    Area.RIDLEY: {
        4: [(0x2B, 0x4C)],
        6: [(0x111, 0x1BC)],
        9: [(0x23, 0x2F)],
        10: [(0x86, 0x18C), (0x35, None)],
        13: [(0x3D, 0x78)],
        14: [(0x7C, 0x10C)],
        16: [(0x3A, 0xB8)],
        17: [(0x13C, None)],
        18: [(0x66, 0x21E)],
        19: [(0x9C, 0x14C)],
        22: [(0x16, None), (0x58, 0xC1)],
        23: [(0x8, 0x2D), (0x7B, 0xC9)],
        29: [(0xA, 0x2E), (0x118, 0x198)],
        30: [(0x103, 0x152)],
        31: [(0x30, 0x96)],
    },
    Area.TOURIAN: {
        7: [(0x24, 0x48)],
        8: [(0x27A, None)],
    },
    Area.CRATERIA: {
        0: [(None, 0x1AC)],
        5: [(0xD5, 0x1AC)],
        7: [(0x1C8, None)],
        9: [(0x3D, 0x92), (0x1CA, 0x3B4)],
        14: [(0x46, 0xC0)],
    },
    Area.CHOZODIA: {
        10: [(0x8, None)],
        14: [(0x10, 0x43)],
        24: [(0x55, 0x9E)],
        26: [(0x14, 0x4B)],
        34: [(0x3C, None)],
        41: [(None, 0x2EE), (None, 0x4BC)],
        47: [(0x45, 0xB1)],
        49: [(0x17, 0x52)],
        54: [(0xE4, 0x295)],
        65: [(0x6, None)],
        66: [(0x18, None)],
        71: [(0xA9, 0x1C7)],
        73: [(0x3B, None)],
        78: [(0x47, 0xBC)],
        87: [(0x2B, None)],
        89: [(0x7C, None)],
        90: [(0x107, 0x307), (0x1E2, 0x4D5)],
        95: [(0x12, 0x3A)],
    },
}


def get_backgrounds(rom: LocalRom, area: Area, room: int) -> RoomInfo:
    room_entry_pointer_array_addr = get_rom_address("sAreaRoomEntryPointers")
    room_entry_array_addr = rom.read((room_entry_pointer_array_addr + 4 * area) & (ROM_START - 1), "<I")[0]
    room_entry_addr = (room_entry_array_addr + 60 * room) & (ROM_START - 1)
    return RoomInfo.from_pointer(rom, room_entry_addr)


def write_item_clipdata_and_gfx(rom: LocalRom):
    for area, rooms in item_clipdata_and_gfx.items():
        for room, items in rooms.items():
            for i, (clip_offset, bg1_offset) in enumerate(items):
                backgrounds = get_backgrounds(rom, area, room)
                if clip_offset is not None:
                    clipdata = rom.read(backgrounds.clipdata.rom_address() + clip_offset, "<B")[0]
                    behavior = (clipdata - Clipdata.ENERGY_TANK) & 0xF0
                    assert behavior in range(0x00, 0x30, 0x10), f"Expected tank clipdata in {area.name.title()} {room} at offset 0x{clip_offset:x}, found 0x{clipdata:02x}"
                    rom.write(backgrounds.clipdata.rom_address() + clip_offset, struct.pack("<B", Clipdata.ENERGY_TANK + i + behavior))
                if bg1_offset is not None:
                    rom.write(backgrounds.bg1.rom_address() + bg1_offset, struct.pack("<B", 0x49 - i))


def patch_chozodia_spotlight(rom: LocalRom):
    chozodia_before_map = get_backgrounds(rom, Area.CHOZODIA, 10).bg0
    chozodia_before_map_bg0 = BackgroundTilemap.from_info(chozodia_before_map, 320)
    for y, row in enumerate(chozodia_before_map_bg0.to_halfword_matrix()):
        for x, tile in enumerate(row):
            tile_info = tile & 0x0FFF
            chozodia_before_map_bg0.set(x, y, tile_info | (0 << 12))
    rom.write(chozodia_before_map.rom_address(), chozodia_before_map_bg0.to_compressed_data())
    chozodia_dark_spotlight = get_backgrounds(rom, Area.CHOZODIA, 25).bg0
    chozodia_dark_spotlight_bg0 = BackgroundTilemap.from_info(chozodia_dark_spotlight, 356)
    for y, row in enumerate(chozodia_dark_spotlight_bg0.to_halfword_matrix()):
        for x, tile in enumerate(row):
            tile_info = tile & 0x0FFF
            chozodia_dark_spotlight_bg0.set(x, y, tile_info | (0 << 12))
    rom.write(chozodia_dark_spotlight.rom_address(), chozodia_dark_spotlight_bg0.to_compressed_data())
