from enum import IntEnum
import itertools
import struct
from typing import Optional, Sequence, Union

from . import lz10, rle, iterators
from .data import get_rom_address, get_symbol


def decompress_data(rom: bytes, src: Union[str, int]):
    if isinstance(src, str):
        address = get_rom_address(src)
    else:
        address = src
    return bytes(lz10.decompress(memoryview(rom)[address:]))


def write_data(rombuffer: bytearray, data: bytes, dst: Union[str, int]):
    if isinstance(dst, str):
        address = get_rom_address(dst)
    else:
        address = dst
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
    write_palette_pointer(rombuffer, "sChozoStatuePlasmaBeamPal", 8)

    # Gravity Suit
    gravity_statue = decompress_data(rom, "sChozoStatueGravitySuitGfx")
    gravity = extract_unknown_chozo_statue_sprite(gravity_statue, 2)
    write_data(rombuffer, gravity, "sRandoGravitySuitGfx")
    write_palette_pointer(rombuffer, "sChozoStatueGravitySuitPal", 11)

    # Space Jump
    space_statue = decompress_data(rom, "sChozoStatueSpaceJumpGfx")
    spacejump = extract_unknown_chozo_statue_sprite(space_statue, 2)
    write_data(rombuffer, spacejump, "sRandoSpaceJumpGfx")
    write_palette_pointer(rombuffer, "sChozoStatueSpaceJumpPal", 16)

    return bytes(rombuffer)


class Area(IntEnum):
    BRINSTAR = 0
    KRAID = 1
    NORFAIR = 2
    RIDLEY = 3
    TOURIAN = 4
    CRATERIA = 5
    CHOZODIA = 6


class Clipdata(IntEnum):
    BEAM_BLOCK_NEVER_REFORM = 0x52
    BEAM_BLOCK_NO_REFORM = 0x55


class RoomTilemap:
    width: int
    height: int
    decompressed: bytearray
    max_compressed_size: int

    def __init__(self, compressed_data: memoryview, max_compressed_size: Optional[int] = None):
        self.width = compressed_data[0]
        self.height = compressed_data[1]
        self.decompressed = rle.decompress(compressed_data[2:])
        self.max_compressed_size = max_compressed_size

    def set(self, x: int, y: int, tile: int, original_tile: Optional[int] = None):
        index = (y * self.width + x) * 2
        if original_tile is not None:
            found_tile = int.from_bytes(self.decompressed[index:index + 2], "little")
            if found_tile != original_tile:
                raise ValueError(f"Unexpected tile at ({x}, {y}) (expected {original_tile:04x}, found {found_tile:04x})")
        self.decompressed[index:index + 2] = tile.to_bytes(2, "little")

    def to_compressed_data(self) -> bytes:
        compressed_data = bytes((self.width, self.height)) + rle.compress(self.decompressed)
        if self.max_compressed_size is not None and len(compressed_data) > self.max_compressed_size:
            raise ValueError(f"Compressed size over limit (size: {len(compressed_data)}, limit: {self.max_compressed_size})")
        return compressed_data

    def to_halfword_matrix(self) -> Sequence[Sequence[int]]:
        return tuple(iterators.batched(itertools.chain.from_iterable(struct.iter_unpack("<H", self.decompressed)), self.width))


def print_room_data(room: RoomTilemap):
    print(*room.to_halfword_matrix(), sep="\n")


def apply_layout_patches(rom: bytes) -> bytes:
    rom = memoryview(rom)
    rombuffer = bytearray(rom)

    def read_u32(addr):
        return int.from_bytes(rom[addr:addr + 4], "little")

    def get_bg1_and_clipdata_address(area, room):
        room_entry_pointer_array_addr = get_rom_address("sAreaRoomEntryPointers")
        room_entry_array_addr = read_u32((room_entry_pointer_array_addr + 4 * area) & (0x8000000 - 1))
        room_entry_addr = (room_entry_array_addr + 60 * room) & (0x8000000 - 1)
        bg1_addr = read_u32(room_entry_addr + 12) & (0x8000000 - 1)
        clipdata_addr = read_u32(room_entry_addr + 20) & (0x8000000 - 1)
        return bg1_addr, clipdata_addr

    _, long_beam_hall_clipdata_addr = get_bg1_and_clipdata_address(Area.BRINSTAR, 4)
    long_beam_hall_clipdata = RoomTilemap(rom[long_beam_hall_clipdata_addr:], 142)
    for x in range(29, 32):
        long_beam_hall_clipdata.set(x, 8, Clipdata.BEAM_BLOCK_NEVER_REFORM, Clipdata.BEAM_BLOCK_NO_REFORM)
    write_data(rombuffer, long_beam_hall_clipdata.to_compressed_data(), long_beam_hall_clipdata_addr)

    return bytes(rombuffer)
