"""
Classes and functions related to interfacing with the BizHawk Client for Metroid: Zero Mission
"""

from __future__ import annotations

import asyncio
import itertools
import struct
from typing import TYPE_CHECKING, Counter, Dict, Iterable, Iterator, List, NamedTuple, Optional, Set

from NetUtils import ClientStatus, NetworkItem
import Utils
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from .data import encode_str, get_symbol
from .items import AP_MZM_ID_BASE, ItemID, ItemType, item_data_table
from .locations import (brinstar_location_table, kraid_location_table, norfair_location_table,
                        ridley_location_table, tourian_location_table, crateria_location_table,
                        chozodia_location_table)

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


def read(address: int, length: int, *, align: int = 1):
    assert address % align == 0, f"address: 0x{address:07x}, align: {align}"
    return (address, length, "System Bus")

def read8(address: int):
    return read(address, 1)

def read16(address: int):
    return read(address, 2, align=2)

def read32(address: int):
    return read(address, 4, align=4)


def write(address: int, value: bytes, *, align: int = 1):
    assert address % align == 0, f"address: 0x{address:07x}, align: {align}"
    return (address, value, "System Bus")

def write8(address: int, value: int):
    return write(address, value.to_bytes(1, "little"))

def write16(address: int, value: int):
    return write(address, value.to_bytes(2, "little"), align=2)

def write32(address: int, value: int):
    return write(address, value.to_bytes(4, "little"), align=4)


guard = write
guard8 = write8
guard16 = write16


def get_int(b: bytes) -> int:
    return int.from_bytes(b, "little")


def next_int(iterator: Iterator[bytes]) -> int:
    return get_int(next(iterator))


# itertools.batched from Python 3.12
# https://docs.python.org/3.11/library/itertools.html#itertools-recipes
def batched(iterable, n):
    if n < 1:
        raise ValueError("n must be at least 1")
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch


# Potential future use to properly identify Deorem kill
DEOREM_FLAGS = {
        "EVENT_DEOREM_ENCOUNTERED_AT_FIRST_LOCATION_OR_KILLED": 0x19,
        "EVENT_DEOREM_ENCOUNTERED_AT_SECOND_LOCATION_OR_KILLED": 0x1A,
        "EVENT_DEOREM_KILLED_AT_SECOND_LOCATION": 0x1B,
}

EVENT_FLAGS = {
    "EVENT_ACID_WORM_KILLED": 0x1C,
    "EVENT_KRAID_KILLED": 0x1E,
    "EVENT_IMAGO_COCOON_KILLED": 0x22,
    "EVENT_IMAGO_KILLED": 0x23,
    "EVENT_RIDLEY_KILLED": 0x25,
    "EVENT_MOTHER_BRAIN_KILLED": 0x27,
    "EVENT_ESCAPED_ZEBES": 0x41,
    "EVENT_FULLY_POWERED_SUIT_OBTAINED": 0x43,
    "EVENT_MECHA_RIDLEY_KILLED": 0x4A,
    "EVENT_ESCAPED_CHOZODIA": 0x4B,
}


TRACKER_EVENT_FLAGS = [
    "EVENT_DEOREM_KILLED",
    *EVENT_FLAGS.keys(),
]


TERMINATOR_CHAR = 0xFF00.to_bytes(2, "little")


def cmd_deathlink(self):
    """Toggle death link from client. Overrides default setting."""

    client_handler = self.ctx.client_handler
    client_handler.death_link.enabled = not client_handler.death_link.enabled
    Utils.async_start(
        self.ctx.update_death_link(client_handler.death_link.enabled),
        name="Update Death Link"
    )


class DeathLinkCtx:
    enabled: bool = False
    update_pending = False
    pending: bool = False
    sent_this_death: bool = False

    def __repr__(self):
        return (f"{type(self)} {{ enabled: {self.enabled}, "
                f"update_pending: {self.update_pending}, "
                f"pending: {self.pending}, "
                f"sent_this_death: {self.sent_this_death} }}")

    def __str__(self):
        return repr(self)


class TankList(NamedTuple):
    energy: int
    missile: int
    super_missile: int
    power_bomb: int


class ZMConstants:
    # Constants
    GM_INGAME = 4
    GM_GAMEOVER = 6
    GM_CHOZODIA_ESCAPE = 7
    GM_CREDITS = 8
    SUB_GAME_MODE_PLAYING = 2
    SUB_GAME_MODE_DYING = 5
    AREA_MAX = 7
    ITEM_NONE = 0xFF
    SUIT_FULLY_POWERED = 1
    SUIT_SUITLESS = 2

    # Structs
    Equipment = "<HHBBHHBBBBBBBBBB"

    # Statics
    sStartingHealthAmmo = TankList(99, 0, 0, 0)
    sTankIncreaseAmount = [
        TankList(100, 5, 2, 2),
        TankList(100, 5, 2, 2),
        TankList(50, 2, 1, 1),
    ]

    # Variable addresses
    gMainGameMode = get_symbol("gMainGameMode")
    gGameModeSub1 = get_symbol("gGameModeSub1")
    gPreventMovementTimer = get_symbol("gPreventMovementTimer")
    gDifficulty = get_symbol("gDifficulty")
    gEquipment = get_symbol("gEquipment")
    gEventsTriggered = get_symbol("gEventsTriggered")
    gCurrentArea = get_symbol("gCurrentArea")
    gRandoLocationBitfields = get_symbol("gRandoLocationBitfields")
    gIncomingItemId = get_symbol("gIncomingItemId")
    gMultiworldItemCount = get_symbol("gMultiworldItemCount")
    gMultiworldItemSenderName = get_symbol("gMultiworldItemSenderName")


class QueuedItem(NamedTuple):
    network_item: NetworkItem
    index: int  # Position of first instance


class MZMClient(BizHawkClient):
    game = "Metroid Zero Mission"
    system = "GBA"
    patch_suffix = ".apmzm"

    local_items_acquired: Optional[List[NetworkItem]]
    local_checked_locations: Set[int]
    local_set_events: Dict[str, bool]
    local_area: int

    queued_item: Optional[QueuedItem]

    rom_slot_name: Optional[str]

    death_link: DeathLinkCtx

    dc_pending: bool

    def __init__(self) -> None:
        super().__init__()
        self.local_items_acquired = None
        self.local_checked_locations = set()
        self.local_set_events = {flag: False for flag in TRACKER_EVENT_FLAGS}
        self.local_area = 0
        self.queued_item = None
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
        slot_name_bytes = next(read_result).rstrip(b"\0")
        seed_name_bytes = next(read_result).rstrip(b"\0")

        if game_name != "ZEROMISSIONE":
            return False

        # Check if we can read the slot name. Doing this here instead of set_auth as a protection against
        # validating a ROM where there's no slot name to read.
        try:
            self.rom_slot_name = slot_name_bytes.decode("utf-8")
        except UnicodeDecodeError:
            logger.info("Could not read slot name from ROM. Are you sure this ROM matches this client version?")
            return False

        client_ctx.game = self.game
        client_ctx.items_handling = 0b000
        client_ctx.want_slot_data = True
        try:
            client_ctx.seed_name = seed_name_bytes.decode("utf-8")
        except UnicodeDecodeError:
            logger.info("Could not determine seed name from ROM. Are you sure this ROM matches this client version?")
            return False

        client_ctx.command_processor.commands["deathlink"] = cmd_deathlink
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
        if main_game_mode in (ZMConstants.GM_CHOZODIA_ESCAPE, ZMConstants.GM_CREDITS):
            return True
        return (main_game_mode, game_mode_sub) == (ZMConstants.GM_INGAME, ZMConstants.SUB_GAME_MODE_DYING)

    async def game_watcher(self, client_ctx: BizHawkClientContext) -> None:
        if self.dc_pending:
            await client_ctx.disconnect()
            return

        if client_ctx.server is None or client_ctx.server.socket.closed or client_ctx.slot_data is None:
            return

        if not client_ctx.items_handling:
            client_ctx.items_handling = 0b111 if client_ctx.slot_data["remote_items"] else 0b001
            await client_ctx.send_msgs([{
                "cmd": "ConnectUpdate",
                "items_handling": client_ctx.items_handling
            }])

            # Need to make sure items handling updates and we get the correct list of received items before continuing.
            await asyncio.sleep(0.75)
            return

        if self.death_link.update_pending:
            await client_ctx.update_death_link(self.death_link.enabled)
            self.death_link.update_pending = False

        bizhawk_ctx = client_ctx.bizhawk_ctx

        try:
            read_result = iter(await bizhawk.read(bizhawk_ctx, [
                read16(ZMConstants.gMainGameMode),
                read16(ZMConstants.gGameModeSub1),
                read8(ZMConstants.gCurrentArea),
                read(ZMConstants.gEventsTriggered, 4 * 3),
                read(ZMConstants.gRandoLocationBitfields, 4 * ZMConstants.AREA_MAX),
                read8(ZMConstants.gMultiworldItemCount),
                read8(ZMConstants.gDifficulty),
            ]))
        except bizhawk.RequestFailedError:
            return

        gMainGameMode = next_int(read_result)
        gGameModeSub1 = next_int(read_result)
        gCurrentArea = next_int(read_result)
        gEventsTriggered = struct.unpack(f"<3I", next(read_result))
        gRandoLocationBitfields = struct.unpack(f"<{ZMConstants.AREA_MAX}I", next(read_result))
        gMultiworldItemCount = next_int(read_result)
        gDifficulty = next_int(read_result)

        gameplay_state = (gMainGameMode, gGameModeSub1)

        if not self.is_state_read_safe(gMainGameMode, gGameModeSub1):
            return

        checked_locations = set()
        set_events = {flag: False for flag in TRACKER_EVENT_FLAGS}

        if gMainGameMode == ZMConstants.GM_INGAME:
            for location_flags, location_table in zip(
                gRandoLocationBitfields,
                (brinstar_location_table, kraid_location_table, norfair_location_table,
                 ridley_location_table, tourian_location_table, crateria_location_table,
                 chozodia_location_table)
            ):
                for location in location_table.values():
                    if location_flags & 1:
                        checked_locations.add(location)
                    location_flags >>= 1

        # Deorem flags are in a weird arrangement, but he also drops Charge Beam so whatever just look for that check
        if not self.local_set_events["EVENT_DEOREM_KILLED"] and brinstar_location_table["Brinstar Worm drop"] in checked_locations:
            set_events["EVENT_DEOREM_KILLED"] = True

        for name, number in EVENT_FLAGS.items():
            block = gEventsTriggered[number // 32]
            flag = 1 << (number & 31)
            if block & flag:
                set_events[name] = True

        if self.local_checked_locations != checked_locations:
            self.local_checked_locations = checked_locations
            await client_ctx.send_msgs([{
                "cmd": "LocationChecks",
                "locations": list(checked_locations)
            }])

        if ((set_events["EVENT_ESCAPED_CHOZODIA"] or gMainGameMode in (ZMConstants.GM_CHOZODIA_ESCAPE, ZMConstants.GM_CREDITS))
            and not client_ctx.finished_game):
            await client_ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])

        if self.local_set_events != set_events and client_ctx.slot is not None:
            event_bitfield = 0
            for i, flag in enumerate(TRACKER_EVENT_FLAGS):
                if set_events[flag]:
                    event_bitfield |= 1 << i
            await client_ctx.send_msgs([{
                "cmd": "Set",
                "key": f"mzm_events_{client_ctx.team}_{client_ctx.slot}",
                "default": 0,
                "want_reply": False,
                "operations": [{"operation": "or", "value": event_bitfield}]
            }])
            self.local_set_events = set_events

        if self.local_area != gCurrentArea and client_ctx.slot is not None:
            await client_ctx.send_msgs([{
                "cmd": "Set",
                "key": f"mzm_area_{client_ctx.team}_{client_ctx.slot}",
                "default": 0,
                "want_reply": False,
                "operations": [{"operation": "replace", "value": gCurrentArea}]
            }])

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

        guard_list = [
            # Ensure game state hasn't changed
            guard16(ZMConstants.gMainGameMode, gMainGameMode),
            guard16(ZMConstants.gGameModeSub1, gGameModeSub1),
        ]

        # Receive death link
        if self.death_link.enabled and self.death_link.pending:
            self.death_link.sent_this_death = True
            try:
                await bizhawk.guarded_write(bizhawk_ctx, [write8(ZMConstants.gEquipment + 6, 0)], guard_list)
            except bizhawk.RequestFailedError:
                return

        def get_remote_items(item_list: Iterable[NetworkItem]):
            return filter(lambda item: item.player != client_ctx.slot or item.location not in self.local_checked_locations,
                          itertools.dropwhile(lambda item: item.location == -2, item_list))

        if (self.local_items_acquired is None):
            remote_item_count = 0
            self.local_items_acquired = []
            for item in client_ctx.items_received:
                if (item.location == -2 or
                    (item.player == client_ctx.slot and item.location in self.local_checked_locations)):
                    self.local_items_acquired.append(item)
                elif remote_item_count < gMultiworldItemCount:
                    self.local_items_acquired.append(item)
                    remote_item_count += 1

        remote_items_found = list(get_remote_items(client_ctx.items_received))

        if self.queued_item is not None and gMultiworldItemCount > self.queued_item.index:
            self.local_items_acquired.append(self.queued_item.network_item)
            self.queued_item = None

        local_multiworld_item_count = sum(1 for _ in get_remote_items(self.local_items_acquired))
        if self.queued_item is None and local_multiworld_item_count < len(remote_items_found):
            item = remote_items_found[local_multiworld_item_count]
            self.queued_item = QueuedItem(item, local_multiworld_item_count)

        if gMultiworldItemCount > len(remote_items_found):
            self.local_items_acquired = client_ctx.items_received
            local_multiworld_item_count = sum(1 for _ in get_remote_items(self.local_items_acquired))

        # Update items if nonlocal
        if client_ctx.items_handling & 0b110:
            acquired_items = Counter(item_data_table[client_ctx.item_names.lookup_in_game(item.item)]
                                     for item in self.local_items_acquired)
            item_guard_list = guard_list + [guard8(ZMConstants.gPreventMovementTimer, 0)]
            try:
                read_result = await bizhawk.guarded_read(
                    bizhawk_ctx,
                    [read(ZMConstants.gEquipment + 12, 4),
                     read8(ZMConstants.gEquipment + 18)],
                    item_guard_list)
            except bizhawk.RequestFailedError:
                return
            if not read_result:
                return
            beams, beam_activation, majors, major_activation = read_result[0]
            beam_deactivation = beams ^ beam_activation
            major_deactivation = majors ^ major_activation
            beams = majors = 0
            current_suit = new_suit = read_result[1][0]
            if current_suit == ZMConstants.SUIT_SUITLESS:
                return
            for item, count in acquired_items.items():
                if item.type == ItemType.tank:
                    max_offset, current_offset = ((0, 6), (2, 8), (4, 10), (5, 11))[item.id]
                    new_capacity = ZMConstants.sStartingHealthAmmo[item.id] + count * ZMConstants.sTankIncreaseAmount[gDifficulty][item.id]
                    def read_amounts(size):
                        return bizhawk.guarded_read(
                            bizhawk_ctx,
                            [read(ZMConstants.gEquipment + max_offset, size // 8),
                             read(ZMConstants.gEquipment + current_offset, size // 8)],
                            item_guard_list
                        )
                    def write_amounts(size, max, current, expect_current=None):
                        return bizhawk.guarded_write(
                            bizhawk_ctx,
                            [write(ZMConstants.gEquipment + max_offset, max.to_bytes(size // 8, 'little')),
                             write(ZMConstants.gEquipment + current_offset, current.to_bytes(size // 8, 'little'))],
                            (item_guard_list + [guard(ZMConstants.gEquipment + current_offset, expect_current.to_bytes(size // 8, 'little'))])
                                if expect_current is not None else item_guard_list
                        )
                    try:
                        if item.id == ItemID.EnergyTank:
                            read_result = await read_amounts(size)
                            if read_result is None:
                                continue
                            capacity, current = map(get_int, read_result)
                            if new_capacity > capacity:
                                await write_amounts(16, new_capacity, new_capacity)
                        else:
                            size = 16 if item.id == ItemID.MissileTank else 8
                            read_result = await read_amounts(size)
                            if read_result is None:
                                continue
                            capacity, current = map(get_int, read_result)
                            consumed = capacity - current
                            await write_amounts(size, new_capacity, max(new_capacity - consumed, 0), current)
                    except bizhawk.RequestFailedError:
                        return
                unknown_items = client_ctx.slot_data["unknown_items"] or self.local_set_events["EVENT_FULLY_POWERED_SUIT_OBTAINED"]
                if item.type == ItemType.beam:
                    beams |= item.bits
                    if item.id != ItemID.PlasmaBeam or unknown_items:
                        beam_activation |= item.bits
                if item.type == ItemType.major:
                    majors |= item.bits
                    if item.id not in (ItemID.SpaceJump, ItemID.GravitySuit) or unknown_items:
                        major_activation |= item.bits
                    if item.id in (ItemID.VariaSuit, ItemID.GravitySuit) and unknown_items:
                        new_suit = ZMConstants.SUIT_FULLY_POWERED
            major_activation &= ~major_deactivation & 0xFF
            beam_activation &= ~beam_deactivation & 0xFF
            try:
                await bizhawk.guarded_write(
                    bizhawk_ctx,
                    [write(ZMConstants.gEquipment + 12, bytes((beams, beam_activation, majors, major_activation))),
                     write8(ZMConstants.gEquipment + 18, new_suit)],
                    item_guard_list + [guard(ZMConstants.gEquipment + 18, current_suit)])
                await bizhawk.guarded_write(
                    bizhawk_ctx,
                    [write16(ZMConstants.gMultiworldItemCount, local_multiworld_item_count)],
                    item_guard_list + [guard16(ZMConstants.gMultiworldItemCount, gMultiworldItemCount)])
            except bizhawk.RequestFailedError:
                return

        if self.queued_item is not None and gMultiworldItemCount <= self.queued_item.index:
            next_item = self.queued_item.network_item
            item_data = item_data_table[client_ctx.item_names.lookup_in_game(next_item.item)]
            if next_item.player == client_ctx.slot:
                sender = TERMINATOR_CHAR
            else:
                sender = encode_str(client_ctx.player_names[next_item.player]) + TERMINATOR_CHAR

            try:
                await bizhawk.guarded_write(
                    bizhawk_ctx,
                    [write8(ZMConstants.gIncomingItemId, item_data.id),
                     write(ZMConstants.gMultiworldItemSenderName, sender)],
                    guard_list + [guard8(ZMConstants.gIncomingItemId, ZMConstants.ITEM_NONE),
                                  guard16(ZMConstants.gMultiworldItemCount, gMultiworldItemCount)])
            except bizhawk.RequestFailedError:
                return

    def on_package(self, ctx: BizHawkClientContext, cmd: str, args: dict) -> None:
        if cmd == "Connected":
            if args["slot_data"].get("death_link"):
                self.death_link.enabled = True
                self.death_link.update_pending = True
        if cmd == "RoomInfo":
            if ctx.seed_name and ctx.seed_name != args["seed_name"]:
                # CommonClient's on_package displays an error to the user in this case, but connection is not cancelled.
                self.dc_pending = True
        if cmd == "Bounced":
            tags = args.get("tags", [])
            if "DeathLink" in tags and args["data"]["source"] != ctx.auth:
                self.death_link.pending = True
