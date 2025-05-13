from typing import Callable, Iterable, Literal

from .constants import Area
from .backgrounds import BackgroundTilemap, Clipdata, SpriteData, get_backgrounds
from .local_rom import LocalRom, get_rom_address


def brinstar_long_beam_hall(rom: LocalRom):
    # Change the three beam blocks to never reform
    long_beam_hall = get_backgrounds(rom, Area.BRINSTAR, 4)
    long_beam_hall_clipdata = BackgroundTilemap.from_info(long_beam_hall.clipdata, 142)
    for x in range(29, 32):
        long_beam_hall_clipdata.set(x, 8, Clipdata.BEAM_BLOCK_NEVER_REFORM, Clipdata.BEAM_BLOCK_NO_REFORM)
    rom.write(long_beam_hall.clipdata.rom_address(), long_beam_hall_clipdata.to_compressed_data())


def brinstar_top(rom: LocalRom):
    # Create a slope instead of a wall to allow leaving Brinstar Ripper Climb room
    brinstar_top = get_backgrounds(rom, Area.BRINSTAR, 29)
    brinstar_top_clipdata = BackgroundTilemap.from_info(brinstar_top.clipdata, 117)
    brinstar_top_bg1 = BackgroundTilemap.from_info(brinstar_top.bg1, 287)
    brinstar_top_clipdata.set(14, 5, Clipdata.STEEP_SLOPE_RISING, Clipdata.AIR)
    brinstar_top_bg1.set(14, 5, 0x009E, 0x0106)
    brinstar_top_bg1.set(14, 6, 0x00AE, 0x0116)
    brinstar_top_clipdata.set(15, 4, Clipdata.STEEP_SLOPE_RISING, Clipdata.SOLID)
    brinstar_top_bg1.set(15, 4, 0x009E, 0x0092)
    brinstar_top_bg1.set(15, 5, 0x00AE, 0x0107)
    brinstar_top_bg1.set(15, 6, 0x005F, 0x0117)
    rom.write(brinstar_top.bg1.rom_address(), brinstar_top_bg1.to_compressed_data())
    rom.write(brinstar_top.clipdata.rom_address(), brinstar_top_clipdata.to_compressed_data())


def brinstar_bridge(rom: LocalRom):
    # Change the bomb block by the Brinstar under-bridge item to never reform
    under_bridge = get_backgrounds(rom, Area.BRINSTAR, 14)
    under_bridge_clipdata = BackgroundTilemap.from_info(under_bridge.clipdata, 287)
    under_bridge_clipdata.set(0xC, 0x17, Clipdata.BOMB_BLOCK_NEVER_REFORM, Clipdata.BOMB_BLOCK_REFORM)
    rom.write(under_bridge.clipdata.rom_address(), under_bridge_clipdata.to_compressed_data())


def kraid_speed_jump(rom: LocalRom):
    # Add a morph tunnel under the item to allow escape without balljumping if the speed blocks
    # were broken in a specific way
    kraid_speed_jump = get_backgrounds(rom, Area.KRAID, 9)
    kraid_speed_jump_clipdata = BackgroundTilemap.from_info(kraid_speed_jump.clipdata, 88)
    kraid_speed_jump_clipdata.set(0x3D, 0x9, Clipdata.AIR, Clipdata.SOLID)
    kraid_speed_jump_clipdata.set(0x3D, 0xA, Clipdata.PITFALL_BLOCK, Clipdata.SOLID)
    for x in range(0x3A, 0x3E):
        kraid_speed_jump_clipdata.set(x, 0xB, Clipdata.AIR, Clipdata.SOLID)
    rom.write(kraid_speed_jump.clipdata.rom_address(), kraid_speed_jump_clipdata.to_compressed_data())


def kraid_map_ballcannon(rom: LocalRom):
    # Converts the speed boost block above the ballcannon to a shot block
    kraid_map_ballcannon = get_backgrounds(rom, Area.KRAID, 13)
    kraid_map_ballcannon_clipdata = BackgroundTilemap.from_info(kraid_map_ballcannon.clipdata, 284)
    kraid_map_ballcannon_clipdata.set(0x9, 0x1B, Clipdata.BEAM_BLOCK_NO_REFORM, Clipdata.SPEED_BOOSTER_BLOCK_NO_REFORM)
    rom.write(kraid_map_ballcannon.clipdata.rom_address(), kraid_map_ballcannon_clipdata.to_compressed_data())


def kraid_right_shaft(rom: LocalRom):
    # Change speed booster blocks in Kraid bottom right shaft to beam blocks, so that Speed Booster or flight
    # are not required to fight Kraid and leave the area
    kraid_right_shaft = get_backgrounds(rom, Area.KRAID, 27)
    kraid_right_shaft_clipdata = BackgroundTilemap.from_info(kraid_right_shaft.clipdata, 520)
    kraid_right_shaft_clipdata.set(0xA, 0x37,
                                   Clipdata.LARGE_BEAM_BLOCK_NW_NO_REFORM, Clipdata.SPEED_BOOSTER_BLOCK_NO_REFORM)
    kraid_right_shaft_clipdata.set(0xB, 0x37,
                                   Clipdata.LARGE_BEAM_BLOCK_NE_NO_REFORM, Clipdata.SPEED_BOOSTER_BLOCK_NO_REFORM)
    kraid_right_shaft_clipdata.set(0xA, 0x38,
                                   Clipdata.LARGE_BEAM_BLOCK_SW_NO_REFORM, Clipdata.SPEED_BOOSTER_BLOCK_NO_REFORM)
    kraid_right_shaft_clipdata.set(0xB, 0x38,
                                   Clipdata.LARGE_BEAM_BLOCK_SE_NO_REFORM, Clipdata.SPEED_BOOSTER_BLOCK_NO_REFORM)
    rom.write(kraid_right_shaft.clipdata.rom_address(), kraid_right_shaft_clipdata.to_compressed_data())


def norfair_brinstar_elevator(rom: LocalRom):
    # Move the elevator to the bottom of the room so that warping out is not required to leave Norfair
    # without having a ton of items guaranteed before going down
    norfair_brinstar_elevator = get_backgrounds(rom, Area.NORFAIR, 0)
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
    rom.write(norfair_brinstar_elevator.clipdata.rom_address(), norfair_brinstar_elevator_clipdata.to_compressed_data())
    rom.write(norfair_brinstar_elevator.bg1.rom_address(), norfair_brinstar_elevator_bg1.to_compressed_data())
    rom.write(get_rom_address(norfair_brinstar_elevator.default_sprite_data_address), new_sprites)


def norfair_larvae_room(rom: LocalRom):
    # Add beam blocks to the floor to allow escape from under the first larva without balljumping
    norfair_larvae_room = get_backgrounds(rom, Area.NORFAIR, 42)
    norfair_larvae_room_clipdata = BackgroundTilemap.from_info(norfair_larvae_room.clipdata, 187)
    for x in range(6, 8):
        norfair_larvae_room_clipdata.set(x, 8, Clipdata.BEAM_BLOCK_NO_REFORM, Clipdata.VERY_DUSTY_GROUND)
    rom.write(norfair_larvae_room.clipdata.rom_address(), norfair_larvae_room_clipdata.to_compressed_data())


def norfair_behind_superdoor(rom: LocalRom):
    # Add a beam block to allow leaving after collecting the left item without a balljump or Speed Booster
    norfair_behind_super = get_backgrounds(rom, Area.NORFAIR, 32)
    norfair_behind_super_clipdata = BackgroundTilemap.from_info(norfair_behind_super.clipdata, 195)
    norfair_behind_super_clipdata.set(0x24, 0x2, Clipdata.BEAM_BLOCK_NO_REFORM, Clipdata.SOLID)
    rom.write(norfair_behind_super.clipdata.rom_address(), norfair_behind_super_clipdata.to_compressed_data())


def ridley_ballcannon(rom: LocalRom):
    # Change Ridley ballcannon room to allow escape from the bottom without needing the ballcannon
    ridley_ballcannon = get_backgrounds(rom, Area.RIDLEY, 23)
    ridley_ballcannon_clipdata = BackgroundTilemap.from_info(ridley_ballcannon.clipdata, 186)
    ridley_ballcannon_bg1 = BackgroundTilemap.from_info(ridley_ballcannon.bg1, 488)
    for x in range(3, 5):
        ridley_ballcannon_clipdata.set(x, 0xD, Clipdata.AIR, Clipdata.PITFALL_BLOCK)
    ridley_ballcannon_bg1.set(0x3, 0xD, 0x0000, 0x00A6)
    ridley_ballcannon_bg1.set(0x4, 0xD, 0x0000, 0x00A7)
    ridley_ballcannon_clipdata.set(4, 0xF, Clipdata.PITFALL_BLOCK_SLOW, Clipdata.AIR)
    ridley_ballcannon_bg1.set(0x4, 0xF, 0x00B9, 0x0000)
    rom.write(ridley_ballcannon.clipdata.rom_address(), ridley_ballcannon_clipdata.to_compressed_data())
    rom.write(ridley_ballcannon.bg1.rom_address(), ridley_ballcannon_bg1.to_compressed_data())


def crateria_moat(rom: LocalRom):
    # Add beam blocks to escape softlock in the room leading to the Unknown Statue Room
    # Change visual to not leave floating dirt when breaking the blocks
    crateria_near_plasma = get_backgrounds(rom, Area.CRATERIA, 9)
    crateria_near_plasma_clipdata = BackgroundTilemap.from_info(crateria_near_plasma.clipdata, 645)
    crateria_near_plasma_bg1 = BackgroundTilemap.from_info(crateria_near_plasma.bg1, 1539)
    for x in range(9, 12):
        crateria_near_plasma_clipdata.set(x, 39, Clipdata.BEAM_BLOCK_NO_REFORM, Clipdata.SOLID)
    crateria_near_plasma_bg1.set(10, 38, 0x0000, 0x0064)
    crateria_near_plasma_bg1.set(10, 39, 0x0072, 0x0074)
    rom.write(crateria_near_plasma.clipdata.rom_address(), crateria_near_plasma_clipdata.to_compressed_data())
    rom.write(crateria_near_plasma.bg1.rom_address(), crateria_near_plasma_bg1.to_compressed_data())


def crateria_water_speedway(rom: LocalRom):
    # Change speed booster blocks in watery room next to elevator to beam blocks
    # This allows reaching the ship to warp out with no requirements
    # Without this, it is easy to get locked in Crateria early, unable to get back to central Norfair
    # TODO: additionally change the landing site to not require a walljump to reach the ship when this patch is on
    crateria_water_speedway = get_backgrounds(rom, Area.CRATERIA, 11)
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
    rom.write(crateria_water_speedway.clipdata.rom_address(), crateria_water_speedway_clipdata.to_compressed_data())


def crateria_left_of_grip(rom: LocalRom):
    # Change the room left of the Power Grip climb to be escapable with the same requirements as the climb itself
    crateria_left_of_grip = get_backgrounds(rom, Area.CRATERIA, 15)
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
    rom.write(crateria_left_of_grip.clipdata.rom_address(), crateria_left_of_grip_clipdata.to_compressed_data())
    rom.write(crateria_left_of_grip.bg1.rom_address(), crateria_left_of_grip_bg1.to_compressed_data())


LAYOUT_PATCH_MAPPING: dict[str, Callable[[LocalRom], None]] = {
    "brinstar_long_beam_hall": brinstar_long_beam_hall,
    "brinstar_top": brinstar_top,
    "brinstar_bridge": brinstar_bridge,
    "kraid_speed_jump": kraid_speed_jump,
    "kraid_map_ballcannon": kraid_map_ballcannon,
    "kraid_right_shaft": kraid_right_shaft,
    "norfair_brinstar_elevator": norfair_brinstar_elevator,
    "norfair_larvae_room": norfair_larvae_room,
    "norfair_behind_superdoor": norfair_behind_superdoor,
    "ridley_ballcannon": ridley_ballcannon,
    "crateria_moat": crateria_moat,
    "crateria_water_speedway": crateria_water_speedway,
    "crateria_left_of_grip": crateria_left_of_grip,
}


def apply_layout_patches(rom: LocalRom, patches: Iterable[str] | Literal["all"]):
    if patches == "all":
        patches = LAYOUT_PATCH_MAPPING.keys()

    for patch in patches:
        LAYOUT_PATCH_MAPPING[patch](rom)
