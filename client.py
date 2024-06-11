"""
Classes and functions related to interfacing with the BizHawk Client for Metroid: Zero Mission
"""

from __future__ import annotations

import itertools
import struct
from typing import TYPE_CHECKING, Iterator, List

import Utils
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from worlds.mzm.items import AP_MZM_ID_BASE

from .data import encode_str, get_symbol
from .locations import (brinstar_location_table, kraid_location_table, norfair_location_table,
                        ridley_location_table, tourian_location_table, crateria_location_table,
                        chozodia_location_table)

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


def read(address: int, length: int, *, align: int = 1):
    assert address % align == 0, f'address: 0x{address:07x}, align: {align}'
    return (address, length, 'System Bus')

def read8(address: int):
    return read(address, 1)

def read16(address: int):
    return read(address, 2, align=2)

def read32(address: int):
    return read(address, 4, align=4)


def write(address: int, value: bytes, *, align: int = 1):
    assert address % align == 0, f'address: 0x{address:07x}, align: {align}'
    return (address, value, 'System Bus')

def write8(address: int, value: int):
    return write(address, value.to_bytes(1, 'little'))

def write16(address: int, value: int):
    return write(address, value.to_bytes(2, 'little'), align=2)

def write32(address: int, value: int):
    return write(address, value.to_bytes(4, 'little'), align=4)


guard8 = write8
guard16 = write16


def next_int(iterator: Iterator[bytes]) -> int:
    return int.from_bytes(next(iterator), 'little')


# itertools.batched from Python 3.12
# https://docs.python.org/3.11/library/itertools.html#itertools-recipes
def batched(iterable, n):
    if n < 1:
        raise ValueError('n must be at least 1')
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch


def cmd_deathlink(self):
    '''Toggle death link from client. Overrides default setting.'''

    client_handler = self.ctx.client_handler
    client_handler.death_link.client_override = True
    client_handler.death_link.enabled = not client_handler.death_link.enabled
    Utils.async_start(
        self.ctx.update_death_link(client_handler.death_link.enabled),
        name='Update Death Link'
    )


class DeathLinkCtx:
    enabled: bool = False
    client_override: bool = False
    pending: bool = False
    sent_this_death: bool = False

    def __repr__(self):
        return (f'{type(self)} {{ enabled: {self.enabled}, '
                f'client_override: {self.client_override}, '
                f'pending: {self.pending}, '
                f'sent_this_death: {self.sent_this_death} }}')

    def __str__(self):
        return repr(self)


class ZMConstants:
    # Constants
    GM_INGAME = 4
    GM_GAMEOVER = 6
    GM_CHOZODIA_ESCAPE = 7
    SUB_GAME_MODE_PLAYING = 2
    SUB_GAME_MODE_DYING = 5
    AREA_MAX = 7

    # Structs
    Equipment = "<HHBBHHBBBBBBBBBB"

    # Variable addresses
    gMainGameMode = get_symbol("gMainGameMode")
    gGameModeSub1 = get_symbol("gGameModeSub1")
    gPreventMovementTimer = get_symbol("gPreventMovementTimer")
    gEquipment = get_symbol("gEquipment")
    gRandoLocationBitfields = get_symbol("gRandoLocationBitfields")
    gIncomingItemId = get_symbol("gIncomingItemId")
    gMultiworldItemCount = get_symbol("gMultiworldItemCount")
    gMultiworldItemSenderName = get_symbol("gMultiworldItemSenderName")


class MZMClient(BizHawkClient):
    game = "Metroid Zero Mission"
    system = "GBA"
    patch_suffix = ".apmzm"
    local_checked_locations: List[int]
    rom_slot_name: str

    death_link: DeathLinkCtx

    dc_pending: bool

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = []
        self.rom_slot_name = None

    async def validate_rom(self, client_ctx: BizHawkClientContext) -> bool:
        from CommonClient import logger

        bizhawk_ctx = client_ctx.bizhawk_ctx
        try:
            read_result = iter(await bizhawk.read(bizhawk_ctx, [
                read(0x80000A0, 12),
                read(get_symbol("sRandoSeed", 2), 64),
                read(get_symbol("sRandoSeed", 66), 64),
            ]))
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        game_name = next(read_result).decode("ascii")
        slot_name_bytes = next(read_result).rstrip(b'\0')
        seed_name_bytes = next(read_result).rstrip(b'\0')

        if game_name != "ZEROMISSIONE":
            return False

        # Check if we can read the slot name. Doing this here instead of set_auth as a protection against
        # validating a ROM where there's no slot name to read.
        try:
            self.rom_slot_name = slot_name_bytes.decode('utf-8')
        except UnicodeDecodeError:
            logger.info("Could not read slot name from ROM. Are you sure this ROM matches this client version?")
            return False

        client_ctx.game = self.game
        client_ctx.items_handling = 0b001
        client_ctx.want_slot_data = True
        try:
            client_ctx.seed_name = seed_name_bytes.decode('utf-8')
        except UnicodeDecodeError:
            logger.info('Could not determine seed name from ROM. Are you sure this ROM matches this client version?')
            return False

        client_ctx.command_processor.commands['deathlink'] = cmd_deathlink
        self.death_link = DeathLinkCtx()

        self.dc_pending = False

        return True

    async def set_auth(self, client_ctx: BizHawkClientContext) -> None:
        client_ctx.auth = self.rom_slot_name

    @staticmethod
    def is_state_write_safe(main_game_mode: int, game_mode_sub: int):
        if main_game_mode == ZMConstants.GM_GAMEOVER:
            return True
        if main_game_mode == ZMConstants.GM_INGAME:
            return game_mode_sub == ZMConstants.SUB_GAME_MODE_PLAYING
        return False

    @staticmethod
    def is_state_read_safe(main_game_mode: int, game_mode_sub: int):
        if MZMClient.is_state_write_safe(main_game_mode, game_mode_sub):
            return True
        return (main_game_mode, game_mode_sub) == (ZMConstants.GM_INGAME, ZMConstants.SUB_GAME_MODE_DYING)

    async def game_watcher(self, client_ctx: BizHawkClientContext) -> None:
        if self.dc_pending:
            await client_ctx.disconnect()
            return

        bizhawk_ctx = client_ctx.bizhawk_ctx

        try:
            read_result = iter(await bizhawk.read(bizhawk_ctx, [
                read16(ZMConstants.gMainGameMode),
                read16(ZMConstants.gGameModeSub1),
                read16(ZMConstants.gPreventMovementTimer),
                read(ZMConstants.gRandoLocationBitfields, 4 * ZMConstants.AREA_MAX),
                read8(ZMConstants.gMultiworldItemCount)
            ]))
        except bizhawk.RequestFailedError:
            return

        gMainGameMode = next_int(read_result)
        gGameModeSub1 = next_int(read_result)
        gPreventMovementTimer = next_int(read_result)
        gRandoLocationBitfields = struct.unpack(f"<{ZMConstants.AREA_MAX}I", next(read_result))
        gMultiworldItemCount = next_int(read_result)

        gameplay_state = (gMainGameMode, gGameModeSub1)

        if not self.is_state_read_safe(gMainGameMode, gGameModeSub1):
            return

        checked_locations = []
        # events = {flag: False for flag in TRACKER_EVENT_FLAGS}
        game_clear = False

        if gMainGameMode == ZMConstants.GM_INGAME:
            for location_flags, location_table in zip(
                gRandoLocationBitfields,
                (brinstar_location_table, kraid_location_table, norfair_location_table,
                 ridley_location_table, tourian_location_table, crateria_location_table,
                 chozodia_location_table)
            ):
                for location in location_table.values():
                    if location_flags & 1:
                        checked_locations.append(location)
                    location_flags >>= 1

        if self.local_checked_locations != checked_locations:
            self.local_checked_locations = checked_locations
            await client_ctx.send_msgs([{
                "cmd": "LocationChecks",
                "locations": checked_locations
            }])

        # TODO: Game clear

        # TODO: Event flags

        if self.death_link.enabled:
            if (gameplay_state == (ZMConstants.GM_INGAME, ZMConstants.SUB_GAME_MODE_DYING)
                or gMainGameMode == ZMConstants.GM_GAMEOVER):
                self.death_link.pending = False
                if not self.death_link.sent_this_death:
                    self.death_link.sent_this_death = True
                    # TODO: Text for failed Tourian/Chozodia escape
                    await client_ctx.send_death()
            else:
                self.death_link.sent_this_death = False

        if not self.is_state_write_safe(gMainGameMode, gGameModeSub1):
            return

        write_list = []
        guard_list = [
            # Ensure game state hasn't changed
            guard16(ZMConstants.gMainGameMode, gMainGameMode),
            guard16(ZMConstants.gGameModeSub1, gGameModeSub1),
        ]

        if gameplay_state == (ZMConstants.GM_INGAME, ZMConstants.SUB_GAME_MODE_PLAYING):
            if (gPreventMovementTimer != 0):
                return
            guard_list.append(guard16(ZMConstants.gPreventMovementTimer, 0))

        # Receive death link
        if self.death_link.enabled and self.death_link.pending:
            self.death_link.sent_this_death = True
            write_list.append(write8(ZMConstants.gEquipment + 6, 0))  # gEquipment.currentEnergy

        if gMultiworldItemCount < len(client_ctx.items_received):
            next_item = client_ctx.items_received[gMultiworldItemCount]
            next_item_id = next_item.item - AP_MZM_ID_BASE
            print(next_item_id)
            next_item_sender = encode_str(client_ctx.player_names[next_item.player]) + 0xFF00.to_bytes(2, "little")

            write_list += [
                write8(ZMConstants.gIncomingItemId, next_item_id),
                write(ZMConstants.gMultiworldItemSenderName, next_item_sender),
            ]

        try:
            await bizhawk.guarded_write(bizhawk_ctx, write_list, guard_list)
        except bizhawk.RequestFailedError:
            return

    def on_package(self, ctx: BizHawkClientContext, cmd: str, args: dict) -> None:
        if cmd == 'Bounced':
            tags = args.get('tags', [])
            if 'DeathLink' in tags and args['data']['source'] != ctx.auth:
                self.death_link.pending = True
        if cmd == 'RoomInfo':
            if ctx.seed_name and ctx.seed_name != args['seed_name']:
                # CommonClient's on_package displays an error to the user in this case, but connection is not cancelled.
                self.dc_pending = True
