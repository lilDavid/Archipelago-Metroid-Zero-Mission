from enum import IntEnum
import itertools
import struct
from typing import Callable, Mapping, NamedTuple, Optional, Sequence, Set, Tuple, Union

from . import lz10, rle, iterators
from .data import get_rom_address, get_symbol
from .items import ItemID


ByteString = Union[bytes, bytearray, memoryview]


PALETTE_BYTES = 2 * 16


def decompress_data(rom: bytes, src: Union[str, int]):
    address = get_rom_address(src)
    return bytes(lz10.decompress(memoryview(rom)[address:]))


def write_data(rombuffer: bytearray, data: bytes, dst: Union[str, int]):
    address = get_rom_address(dst)
    rombuffer[address:address + len(data)] = data


def get_tile(tiledata: bytes, x: int, y: int) -> bytes:
    offset = 0x20 * x + 0x400 * y
    return tiledata[offset:offset+0x20]


def get_sprites(tileset: bytes, start_x: int, start_y: int, sprites: int, rows: int = 2):
    return b"".join(get_tile(tileset, 2 * t + x, y)
                    for t in range(sprites)
                    for y in range(start_y, start_y + rows)
                    for x in range(start_x, start_x + 2))


def make_4_frame_animation(data: bytes):
    middle_frame = data[0x80:0x100]
    return data + middle_frame


def extract_chozo_statue_sprite(statue: bytes):
    item = get_sprites(statue, 4, 4, 3)
    return make_4_frame_animation(item)


def extract_unknown_chozo_statue_sprite(statue: bytes, y_offset: int):
    tiles = get_sprites(statue, 4, 4, 2)
    byte_offset = y_offset * 4
    # Move the graphics down by `y_offset` pixels
    shifted = (tiles[byte_offset:0x20] + tiles[0x40:0x40 + byte_offset]
             + tiles[0x20 + byte_offset:0x40] + tiles[0x60:0x60 + byte_offset]
             + tiles[0x40 + byte_offset:0x60] + tiles[0x80:0x80 + byte_offset]
             + tiles[0x60 + byte_offset:0x80] + tiles[0xA0:0xA0 + byte_offset])
    return 4 * shifted


def write_palette_pointer(rombuffer: bytearray, palette_name: str, index: int):
    palette = get_symbol(palette_name)
    write_data(rombuffer,
               palette.to_bytes(4, "little"),
               get_symbol("sItemGfxPointers", 8 * index + 4))  # sItemGfxPointers[index].palette


def add_item_sprites(rom: bytes) -> bytes:
    rombuffer = bytearray(rom)

    # Tanks are already in needed format
    # Plasma Beam, Gravity Suit, and Space Jump are by default custom and already in ROM

    # Long Beam
    long_statue = decompress_data(rom, "sChozoStatueLongBeamGfx")
    long = extract_chozo_statue_sprite(long_statue)
    write_data(rombuffer, long, "sRandoLongBeamGfx")

    # Charge Beam
    charge = decompress_data(rom, "sChargeBeamGfx")
    charge1 = get_sprites(charge, 18, 0, 1)
    charge2 = get_sprites(charge, 20, 0, 1)
    charge3 = bytearray(charge1)
    charge3[0x20:0x40] = get_tile(charge, 22, 0)
    write_data(rombuffer, bytes(charge1 + charge2 + charge3 + charge2), "sRandoChargeBeamGfx")

    # Ice Beam
    ice_statue = decompress_data(rom, "sChozoStatueIceBeamGfx")
    ice = extract_chozo_statue_sprite(ice_statue)
    write_data(rombuffer, ice, "sRandoIceBeamGfx")

    # Wave Beam
    wave_statue = decompress_data(rom, "sChozoStatueWaveBeamGfx")
    wave = extract_chozo_statue_sprite(wave_statue)
    write_data(rombuffer, wave, "sRandoWaveBeamGfx")

    # Bomb
    bomb_statue = decompress_data(rom, "sChozoStatueBombsGfx")
    bomb = extract_chozo_statue_sprite(bomb_statue)
    write_data(rombuffer, bomb, "sRandoBombGfx")

    # Varia Suit
    varia_statue = decompress_data(rom, "sChozoStatueVariaGfx")
    varia = extract_chozo_statue_sprite(varia_statue)
    write_data(rombuffer, varia, "sRandoVariaSuitGfx")

    # Morph Ball
    morph = decompress_data(rom, "sMorphBallGfx")
    morph_core = get_sprites(morph, 0, 0, 3)
    morph_glass = get_sprites(morph, 6, 0, 1)
    morph_composited = bytearray(len(morph_core))
    for t in range(3):
        for y in range(2):
            for i in range(0x40):
                glass_pair = morph_glass[i + 0x40 * y]
                glass_left, glass_right = glass_pair & 0xF, glass_pair >> 4
                ball_pair = morph_core[i + 0x40 * y + 0x80 * t]
                ball_left, ball_right = ball_pair & 0xF, ball_pair >> 4
                if glass_left != 0:
                    ball_left = glass_left
                if glass_right != 0:
                    ball_right = glass_right
                combined = ball_right << 4 | ball_left
                morph_composited[i + 0x40 * y + 0x80 * t] = combined
    write_data(rombuffer, make_4_frame_animation(morph_composited), "sRandoMorphBallGfx")

    # Speed Booster
    speed_statue = decompress_data(rom, "sChozoStatueSpeedboosterGfx")
    speed = extract_chozo_statue_sprite(speed_statue)
    write_data(rombuffer, speed, "sRandoSpeedBoosterGfx")

    # Hi-Jump Boots
    hijump_statue = decompress_data(rom, "sChozoStatueHighJumpGfx")
    hijump = extract_chozo_statue_sprite(hijump_statue)
    write_data(rombuffer, hijump, "sRandoHiJumpGfx")

    # Screw Attack
    screw_statue = decompress_data(rom, "sChozoStatueScrewAttackGfx")
    screw = extract_chozo_statue_sprite(screw_statue)
    write_data(rombuffer, screw, "sRandoScrewAttackGfx")

    # Power Grip
    powergrip = decompress_data(rom, "sPowerGripGfx")
    powergrip = get_sprites(powergrip, 0, 0, 3)
    write_data(rombuffer, make_4_frame_animation(powergrip), "sRandoPowerGripGfx")

    return bytes(rombuffer)


def use_unknown_item_sprites(rom: bytes) -> bytes:
    rombuffer = bytearray(rom)

    # Plasma Beam
    plasma_statue = decompress_data(rom, "sChozoStatuePlasmaBeamGfx")
    plasma = extract_unknown_chozo_statue_sprite(plasma_statue, 4)
    write_data(rombuffer, plasma, "sRandoPlasmaBeamGfx")
    write_palette_pointer(rombuffer, "sChozoStatuePlasmaBeamPal", ItemID.PlasmaBeam)

    # Gravity Suit
    gravity_statue = decompress_data(rom, "sChozoStatueGravitySuitGfx")
    gravity = extract_unknown_chozo_statue_sprite(gravity_statue, 2)
    write_data(rombuffer, gravity, "sRandoGravitySuitGfx")
    write_palette_pointer(rombuffer, "sChozoStatueGravitySuitPal", ItemID.GravitySuit)

    # Space Jump
    space_statue = decompress_data(rom, "sChozoStatueSpaceJumpGfx")
    spacejump = extract_unknown_chozo_statue_sprite(space_statue, 2)
    write_data(rombuffer, spacejump, "sRandoSpaceJumpGfx")
    write_palette_pointer(rombuffer, "sChozoStatueSpaceJumpPal", ItemID.SpaceJump)

    return bytes(rombuffer)


class BackgroundProperties(IntEnum):
    NONE = 0
    RLE_COMPRESSED = 0x10
    LZ77_COMPRESSED = 0x40
    DARK_ROOM = LZ77_COMPRESSED | 5
    STARTS_FROM_BOTTOM = LZ77_COMPRESSED | 6


class BackgroundInfo(NamedTuple):
    rom: memoryview
    properties: BackgroundProperties
    data_ptr: int

    @classmethod
    def from_data(cls, rom: ByteString, prop: int, data_ptr: int):
        return cls(memoryview(rom), BackgroundProperties(prop), data_ptr)

    def rom_address(self):
        return self.data_ptr & (0x8000000 - 1)

    def compressed_data(self):
        return self.rom[self.rom_address():]


class SpriteData(NamedTuple):
    y: int
    x: int
    spriteset_index: int

    @classmethod
    def terminator(cls):
        return cls(255, 255, 255 - 17)

    @classmethod
    def unpack(cls, data: ByteString):
        y, x, i = struct.unpack("<BBB", data)
        return cls(y, x, i - 17)

    @classmethod
    def iter_unpack(cls, data: ByteString):
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
    def from_pointer(cls, rom: ByteString, ptr: int):
        ptr &= (0x8000000 - 1)
        (bg0_prop, bg1_prop, bg2_prop, bg3_prop,
         bg0_ptr, bg1_ptr, bg2_ptr, clipdata_ptr, bg3_ptr,
         default_sprite_ptr
        ) = struct.unpack_from("<xBBBBxxxIIIIIxxxxI", rom, ptr)
        bg0 = BackgroundInfo.from_data(rom, bg0_prop, bg0_ptr)
        bg1 = BackgroundInfo.from_data(rom, bg1_prop, bg1_ptr)
        bg2 = BackgroundInfo.from_data(rom, bg2_prop, bg2_ptr)
        bg3 = BackgroundInfo.from_data(rom, bg3_prop, bg3_ptr)
        clipdata = BackgroundInfo.from_data(rom, BackgroundProperties.RLE_COMPRESSED, clipdata_ptr)
        default_sprites = default_sprite_ptr
        return cls(bg0, bg1, bg2, bg3, clipdata, default_sprites)


class Area(IntEnum):
    BRINSTAR = 0
    KRAID = 1
    NORFAIR = 2
    RIDLEY = 3
    TOURIAN = 4
    CRATERIA = 5
    CHOZODIA = 6


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


class BackgroundTilemap:
    width: int
    height: int
    compression: BackgroundProperties
    bg_size: Optional[int]
    decompressed: bytearray
    max_compressed_size: Optional[int]

    def __init__(self, compressed_data: memoryview, compression: BackgroundProperties, max_compressed_size: Optional[int] = None):
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
    def from_info(cls, info: BackgroundInfo, max_compressed_size: Optional[int] = None):
        return cls(info.compressed_data(), info.properties, max_compressed_size)

    def set(self, x: int, y: int, tile: int, original_tile: Optional[int] = None):
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

    def to_halfword_matrix(self) -> Sequence[Sequence[int]]:
        return tuple(iterators.batched(itertools.chain.from_iterable(struct.iter_unpack("<H", self.decompressed)), self.width))


def print_room_data(room: BackgroundTilemap):
    for row in room.to_halfword_matrix():
        print(*(format(tile, "04x") for tile in row))


def read_u32(rom, addr):
    return int.from_bytes(rom[addr:addr + 4], "little")


def background_extraction_function(rom: ByteString) -> Callable[[int, int], RoomInfo]:
    def get_backgrounds(area, room):
        room_entry_pointer_array_addr = get_rom_address("sAreaRoomEntryPointers")
        room_entry_array_addr = read_u32(rom, (room_entry_pointer_array_addr + 4 * area) & (0x8000000 - 1))
        room_entry_addr = (room_entry_array_addr + 60 * room) & (0x8000000 - 1)
        return RoomInfo.from_pointer(rom, room_entry_addr)
    return get_backgrounds


# Tuples are: Clipdata offset, BG1 offset, tank type
item_clipdata_and_gfx: Mapping[Area, Mapping[int, Sequence[Tuple[Optional[int], Optional[int]]]]] = {
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


def apply_always_background_patches(rom: bytes) -> bytes:
    rombuffer = bytearray(rom)
    get_backgrounds = background_extraction_function(rom)

    # Item graphics and clipdata
    for area, rooms in item_clipdata_and_gfx.items():
        for room, items in rooms.items():
            for i, (clip_offset, bg1_offset) in enumerate(items):
                backgrounds = get_backgrounds(area, room)
                if clip_offset is not None:
                    clipdata = rombuffer[backgrounds.clipdata.rom_address() + clip_offset]
                    behavior = (clipdata - Clipdata.ENERGY_TANK) & 0xF0
                    assert behavior in range(0x00, 0x30, 0x10), f"Expected tank clipdata in {area.name.title()} {room}, found 0x{clipdata:02x}"
                    rombuffer[backgrounds.clipdata.rom_address() + clip_offset] = Clipdata.ENERGY_TANK + i + behavior
                if bg1_offset is not None:
                    rombuffer[backgrounds.bg1.rom_address() + bg1_offset] = 0x49 - i

    # Change the spotlight graphics so it always appears dark
    chozodia_before_map = get_backgrounds(Area.CHOZODIA, 10).bg0
    chozodia_before_map_bg0 = BackgroundTilemap.from_info(chozodia_before_map, 320)
    for y, row in enumerate(chozodia_before_map_bg0.to_halfword_matrix()):
        for x, tile in enumerate(row):
            tile_info = tile & 0x0FFF
            chozodia_before_map_bg0.set(x, y, tile_info | (0 << 12))
    write_data(rombuffer, chozodia_before_map_bg0.to_compressed_data(), chozodia_before_map.data_ptr)
    chozodia_dark_spotlight = get_backgrounds(Area.CHOZODIA, 25).bg0
    chozodia_dark_spotlight_bg0 = BackgroundTilemap.from_info(chozodia_dark_spotlight, 356)
    for y, row in enumerate(chozodia_dark_spotlight_bg0.to_halfword_matrix()):
        for x, tile in enumerate(row):
            tile_info = tile & 0x0FFF
            chozodia_dark_spotlight_bg0.set(x, y, tile_info | (0 << 12))
    write_data(rombuffer, chozodia_dark_spotlight_bg0.to_compressed_data(), chozodia_dark_spotlight.data_ptr)

    return bytes(rombuffer)


compatible_patches = [
    "brinstar_long_beam_hall",
    "brinstar_bridge",
    "crateria_moat",
    "kraid_right_shaft",
    "ridley_ballcannon",
    "norfair_larvae_room",
    "kraid_map_ballcannon"
]

# Patches that require expanded space. These are not backwards compatible, so we keep a list and
# apply only the ones that both the generator and the patcher have.
expansion_required_patches = [
    "brinstar_top",
    "norfair_brinstar_elevator",
    "crateria_water_speedway",
    "crateria_left_of_grip",
    "kraid_speed_jump",
    "norfair_behind_superdoor",
]

layout_patches = [
    *compatible_patches,
    *expansion_required_patches,
]


def apply_layout_patches(rom: bytes, patches: Set[str]) -> bytes:
    rom = memoryview(rom)
    rombuffer = bytearray(rom)
    get_backgrounds = background_extraction_function(rom)

    if "brinstar_long_beam_hall" in patches:
        # Change the three beam blocks to never reform
        long_beam_hall = get_backgrounds(Area.BRINSTAR, 4)
        long_beam_hall_clipdata = BackgroundTilemap.from_info(long_beam_hall.clipdata, 142)
        for x in range(29, 32):
            long_beam_hall_clipdata.set(x, 8, Clipdata.BEAM_BLOCK_NEVER_REFORM, Clipdata.BEAM_BLOCK_NO_REFORM)
        write_data(rombuffer, long_beam_hall_clipdata.to_compressed_data(), long_beam_hall.clipdata.data_ptr)

    if "brinstar_top" in patches:
        # Create a slope instead of a wall to allow leaving Brinstar Ripper Climb room
        brinstar_top = get_backgrounds(Area.BRINSTAR, 29)
        brinstar_top_clipdata = BackgroundTilemap.from_info(brinstar_top.clipdata, 117)
        brinstar_top_bg1 = BackgroundTilemap.from_info(brinstar_top.bg1, 287)
        brinstar_top_clipdata.set(14, 5, Clipdata.STEEP_SLOPE_RISING, Clipdata.AIR)
        brinstar_top_bg1.set(14, 5, 0x009E, 0x0106)
        brinstar_top_bg1.set(14, 6, 0x00AE, 0x0116)
        brinstar_top_clipdata.set(15, 4, Clipdata.STEEP_SLOPE_RISING, Clipdata.SOLID)
        brinstar_top_bg1.set(15, 4, 0x009E, 0x0092)
        brinstar_top_bg1.set(15, 5, 0x00AE, 0x0107)
        brinstar_top_bg1.set(15, 6, 0x005F, 0x0117)
        write_data(rombuffer, brinstar_top_bg1.to_compressed_data(), brinstar_top.bg1.data_ptr)
        write_data(rombuffer, brinstar_top_clipdata.to_compressed_data(), brinstar_top.clipdata.data_ptr)

    if "brinstar_bridge" in patches:
        # Change the bomb block by the Brinstar under-bridge item to never reform
        under_bridge = get_backgrounds(Area.BRINSTAR, 14)
        under_bridge_clipdata = BackgroundTilemap.from_info(under_bridge.clipdata, 287)
        under_bridge_clipdata.set(0xC, 0x17, Clipdata.BOMB_BLOCK_NEVER_REFORM, Clipdata.BOMB_BLOCK_REFORM)
        write_data(rombuffer, under_bridge_clipdata.to_compressed_data(), under_bridge.clipdata.data_ptr)

    if "kraid_speed_jump" in patches:
        # Add a morph tunnel under the item to allow escape without balljumping if the speed blocks
        # were broken in a specific way
        kraid_speed_jump = get_backgrounds(Area.KRAID, 9)
        kraid_speed_jump_clipdata = BackgroundTilemap.from_info(kraid_speed_jump.clipdata, 88)
        kraid_speed_jump_clipdata.set(0x3D, 0x9, Clipdata.AIR, Clipdata.SOLID)
        kraid_speed_jump_clipdata.set(0x3D, 0xA, Clipdata.PITFALL_BLOCK, Clipdata.SOLID)
        for x in range(0x3A, 0x3E):
            kraid_speed_jump_clipdata.set(x, 0xB, Clipdata.AIR, Clipdata.SOLID)
        write_data(rombuffer, kraid_speed_jump_clipdata.to_compressed_data(), kraid_speed_jump.clipdata.data_ptr)

    if "kraid_map_ballcannon" in patches:
        # Converts the speed boost block above the ballcannon to a shot block
        kraid_map_ballcannon = get_backgrounds(Area.KRAID, 13)
        kraid_map_ballcannon_clipdata = BackgroundTilemap.from_info(kraid_map_ballcannon.clipdata, 284)
        kraid_map_ballcannon_clipdata.set(0x9, 0x1B, Clipdata.BEAM_BLOCK_NO_REFORM, Clipdata.SPEED_BOOSTER_BLOCK_NO_REFORM)
        write_data(rombuffer, kraid_map_ballcannon_clipdata.to_compressed_data(), kraid_map_ballcannon.clipdata.data_ptr)

    if "kraid_right_shaft" in patches:
        # Change speed booster blocks in Kraid bottom right shaft to beam blocks, so that Speed Booster or flight
        # are not required to fight Kraid and leave the area
        kraid_right_shaft = get_backgrounds(Area.KRAID, 27)
        kraid_right_shaft_clipdata = BackgroundTilemap.from_info(kraid_right_shaft.clipdata, 520)
        kraid_right_shaft_clipdata.set(0xA, 0x37,
                                       Clipdata.LARGE_BEAM_BLOCK_NW_NO_REFORM, Clipdata.SPEED_BOOSTER_BLOCK_NO_REFORM)
        kraid_right_shaft_clipdata.set(0xB, 0x37,
                                       Clipdata.LARGE_BEAM_BLOCK_NE_NO_REFORM, Clipdata.SPEED_BOOSTER_BLOCK_NO_REFORM)
        kraid_right_shaft_clipdata.set(0xA, 0x38,
                                       Clipdata.LARGE_BEAM_BLOCK_SW_NO_REFORM, Clipdata.SPEED_BOOSTER_BLOCK_NO_REFORM)
        kraid_right_shaft_clipdata.set(0xB, 0x38,
                                       Clipdata.LARGE_BEAM_BLOCK_SE_NO_REFORM, Clipdata.SPEED_BOOSTER_BLOCK_NO_REFORM)
        write_data(rombuffer, kraid_right_shaft_clipdata.to_compressed_data(), kraid_right_shaft.clipdata.data_ptr)

    if "norfair_brinstar_elevator" in patches:
        # Move the elevator to the bottom of the room so that warping out is not required to leave Norfair
        # without having a ton of items guaranteed before going down
        norfair_brinstar_elevator = get_backgrounds(Area.NORFAIR, 0)
        norfair_brinstar_elevator_clipdata = BackgroundTilemap.from_info(norfair_brinstar_elevator.clipdata, 238)
        norfair_brinstar_elevator_bg1 = BackgroundTilemap.from_info(norfair_brinstar_elevator.bg1, 504)
        elevator_tiles = [[0x01D0, 0x01D1, 0x01D2, 0x01D3, 0x01D4],
                          [0x01E0, 0x01E1, 0x01E2, 0x01E3, 0x01E4],
                          [0x0000] * 5]
        ground_tiles = [[0x0000] * 5,
                        [0x009B, 0x006B, 0x009E, 0x009C, 0x009D],
                        [0x00AB, 0x0000, 0x00AE, 0x00AC, 0x00AD]]
        norfair_brinstar_elevator_clipdata.set(9, 16, Clipdata.SOLID, Clipdata.ELEVATOR_UP)
        norfair_brinstar_elevator_clipdata.set(9, 29, Clipdata.ELEVATOR_UP, Clipdata.SOLID)
        for x in (7, 11):
            norfair_brinstar_elevator_clipdata.set(x, 26, Clipdata.AIR, Clipdata.SOLID)
        for y, (elevator_row, ground_row) in enumerate(zip(elevator_tiles, ground_tiles)):
            for x, (elevator_tile, ground_tile) in enumerate(zip(elevator_row, ground_row)):
                norfair_brinstar_elevator_bg1.set(x + 7, y + 15, ground_tile, elevator_tile)
                norfair_brinstar_elevator_bg1.set(x + 7, y + 28, elevator_tile, ground_tile)
        new_sprites = b"".join([
            SpriteData(28, 9, 4).pack(),  # Elevator
            SpriteData(23, 6, 2).pack(),  # Ripper
            SpriteData(23, 12, 2).pack(),  # Ripper
            SpriteData.terminator().pack()
        ])
        write_data(rombuffer, norfair_brinstar_elevator_clipdata.to_compressed_data(), norfair_brinstar_elevator.clipdata.data_ptr)
        write_data(rombuffer, norfair_brinstar_elevator_bg1.to_compressed_data(), norfair_brinstar_elevator.bg1.data_ptr)
        write_data(rombuffer, new_sprites, norfair_brinstar_elevator.default_sprite_data_address)

    if "norfair_larvae_room" in patches:
        # Add beam blocks to the floor to allow escape from under the first larva without balljumping
        norfair_larvae_room = get_backgrounds(Area.NORFAIR, 42)
        norfair_larvae_room_clipdata = BackgroundTilemap.from_info(norfair_larvae_room.clipdata, 187)
        for x in range(6, 8):
            norfair_larvae_room_clipdata.set(x, 8, Clipdata.BEAM_BLOCK_NO_REFORM, Clipdata.VERY_DUSTY_GROUND)
        write_data(rombuffer, norfair_larvae_room_clipdata.to_compressed_data(), norfair_larvae_room.clipdata.data_ptr)

    if "norfair_behind_superdoor" in patches:
        # Add a beam block to allow leaving after collecting the left item without a balljump or Speed Booster
        norfair_behind_super = get_backgrounds(Area.NORFAIR, 32)
        norfair_behind_super_clipdata = BackgroundTilemap.from_info(norfair_behind_super.clipdata, 195)
        norfair_behind_super_clipdata.set(0x24, 0x2, Clipdata.BEAM_BLOCK_NO_REFORM, Clipdata.SOLID)
        write_data(rombuffer, norfair_behind_super_clipdata.to_compressed_data(), norfair_behind_super.clipdata.data_ptr)

    if "ridley_ballcannon" in patches:
        # Change Ridley ballcannon room to allow escape from the bottom without needing the ballcannon
        ridley_ballcannon = get_backgrounds(Area.RIDLEY, 23)
        ridley_ballcannon_clipdata = BackgroundTilemap.from_info(ridley_ballcannon.clipdata, 186)
        ridley_ballcannon_bg1 = BackgroundTilemap.from_info(ridley_ballcannon.bg1, 488)
        for x in range(3, 5):
            ridley_ballcannon_clipdata.set(x, 0xD, Clipdata.AIR, Clipdata.PITFALL_BLOCK)
        ridley_ballcannon_bg1.set(0x3, 0xD, 0x0000, 0x00A6)
        ridley_ballcannon_bg1.set(0x4, 0xD, 0x0000, 0x00A7)
        ridley_ballcannon_clipdata.set(4, 0xF, Clipdata.PITFALL_BLOCK_SLOW, Clipdata.AIR)
        ridley_ballcannon_bg1.set(0x4, 0xF, 0x00B9, 0x0000)
        write_data(rombuffer, ridley_ballcannon_clipdata.to_compressed_data(), ridley_ballcannon.clipdata.data_ptr)
        write_data(rombuffer, ridley_ballcannon_bg1.to_compressed_data(), ridley_ballcannon.bg1.data_ptr)

    if "crateria_moat" in patches:
        # Add beam blocks to escape softlock in the room leading to the Unknown Statue Room
        # Change visual to not leave floating dirt when breaking the blocks
        crateria_near_plasma = get_backgrounds(Area.CRATERIA, 9)
        crateria_near_plasma_clipdata = BackgroundTilemap.from_info(crateria_near_plasma.clipdata, 645)
        crateria_near_plasma_bg1 = BackgroundTilemap.from_info(crateria_near_plasma.bg1, 1539)
        for x in range(9, 12):
            crateria_near_plasma_clipdata.set(x, 39, Clipdata.BEAM_BLOCK_NO_REFORM, Clipdata.SOLID)
        crateria_near_plasma_bg1.set(10, 38, 0x0000, 0x0064)
        crateria_near_plasma_bg1.set(10, 39, 0x0072, 0x0074)
        write_data(rombuffer, crateria_near_plasma_clipdata.to_compressed_data(), crateria_near_plasma.clipdata.data_ptr)
        write_data(rombuffer, crateria_near_plasma_bg1.to_compressed_data(), crateria_near_plasma.bg1.data_ptr)

    if "crateria_water_speedway" in patches:
        # Change speed booster blocks in watery room next to elevator to beam blocks
        # This allows reaching the ship to warp out with no requirements
        # Without this, it is easy to get locked in Crateria early, unable to get back to central Norfair
        # TODO: additionally change the landing site to not require a walljump to reach the ship when this patch is on
        crateria_water_speedway = get_backgrounds(Area.CRATERIA, 11)
        crateria_water_speedway_clipdata = BackgroundTilemap.from_info(crateria_water_speedway.clipdata, 151)
        crateria_water_speedway_clipdata.set(0x11, 0xA,
                                             Clipdata.LARGE_BEAM_BLOCK_NW_NO_REFORM, Clipdata.SPEED_BOOSTER_BLOCK_NO_REFORM)
        crateria_water_speedway_clipdata.set(0x12, 0xA,
                                             Clipdata.LARGE_BEAM_BLOCK_NE_NO_REFORM, Clipdata.SPEED_BOOSTER_BLOCK_NO_REFORM)
        crateria_water_speedway_clipdata.set(0x11, 0xB,
                                             Clipdata.LARGE_BEAM_BLOCK_SW_NO_REFORM, Clipdata.SPEED_BOOSTER_BLOCK_NO_REFORM)
        crateria_water_speedway_clipdata.set(0x12, 0xB,
                                             Clipdata.LARGE_BEAM_BLOCK_SE_NO_REFORM, Clipdata.SPEED_BOOSTER_BLOCK_NO_REFORM)
        crateria_water_speedway_clipdata.set(0x13, 0xB,
                                             Clipdata.BEAM_BLOCK_NO_REFORM,
                                             Clipdata.SPEED_BOOSTER_BLOCK_NO_REFORM)
        write_data(rombuffer, crateria_water_speedway_clipdata.to_compressed_data(),
                   crateria_water_speedway.clipdata.data_ptr)

    if "crateria_left_of_grip" in patches:
        # Change the room left of the Power Grip climb to be escapable with the same requirements as the climb itself
        crateria_left_of_grip = get_backgrounds(Area.CRATERIA, 15)
        crateria_left_of_grip_clipdata = BackgroundTilemap.from_info(crateria_left_of_grip.clipdata, 237)
        crateria_left_of_grip_bg1 = BackgroundTilemap.from_info(crateria_left_of_grip.bg1, 515)
        crateria_left_of_grip_clipdata.set(0x6, 0xD, Clipdata.BEAM_BLOCK_REFORM, Clipdata.SOLID)
        crateria_left_of_grip_clipdata.set(0x7, 0xD, Clipdata.BEAM_BLOCK_REFORM, Clipdata.SOLID)
        crateria_left_of_grip_bg1.set(0x6, 0xD, 0x0130, 0x00A9)
        crateria_left_of_grip_bg1.set(0x7, 0xD, 0x0130, 0x00AA)
        crateria_left_of_grip_bg1.set(0x6, 0xE, 0x00A9, 0x00B9)
        crateria_left_of_grip_bg1.set(0x7, 0xE, 0x00AA, 0x00BA)
        crateria_left_of_grip_bg1.set(0x6, 0xF, 0x00B9, 0x00C9)
        crateria_left_of_grip_bg1.set(0x7, 0xF, 0x00BA, 0x00CA)
        crateria_left_of_grip_bg1.set(0x6, 0x10, 0x00C9, 0x00D9)
        crateria_left_of_grip_bg1.set(0x7, 0x10, 0x00CA, 0x00DA)
        crateria_left_of_grip_bg1.set(0x6, 0x11, 0x00D9, 0x00E9)
        crateria_left_of_grip_bg1.set(0x7, 0x11, 0x00DA, 0x00EA)
        write_data(rombuffer, crateria_left_of_grip_clipdata.to_compressed_data(),
                   crateria_left_of_grip.clipdata.data_ptr)
        write_data(rombuffer, crateria_left_of_grip_bg1.to_compressed_data(), crateria_left_of_grip.bg1.data_ptr)

    return bytes(rombuffer)
