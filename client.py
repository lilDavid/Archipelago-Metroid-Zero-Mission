"""
Classes and functions related to interfacing with the BizHawk Client for Metroid: Zero Mission
"""

from __future__ import annotations

import itertools
import struct
from typing import TYPE_CHECKING, Counter, Dict, Iterable, Iterator, List, NamedTuple, Optional, Set, Tuple

from NetUtils import ClientStatus, NetworkItem
import Utils
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from .data import get_symbol
from .items import ItemID, ItemType, item_data_table
from .locations import (brinstar_location_table, kraid_location_table, norfair_location_table,
                        ridley_location_table, tourian_location_table, crateria_location_table,
                        chozodia_location_table)
from .text import LINE_WIDTH, TERMINATOR_CHAR, Message

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


# DEOREM_KILLED and RUINS_TEST_PASSED are out of order to maintain tracker compatibility. DEOREM_KILLED was before any
# of the vanilla events, and RUINS_TEST_PASSED replaces the vanilla FULLY_POWERED_SUIT_OBTAINED.
EVENT_FLAGS = {
    "EVENT_DEOREM_KILLED": 0x4F,
    "EVENT_ACID_WORM_KILLED": 0x1C,
    "EVENT_KRAID_KILLED": 0x1E,
    "EVENT_IMAGO_COCOON_KILLED": 0x22,
    "EVENT_IMAGO_KILLED": 0x23,
    "EVENT_RIDLEY_KILLED": 0x25,
    "EVENT_MOTHER_BRAIN_KILLED": 0x27,
    "EVENT_ESCAPED_ZEBES": 0x41,
    "EVENT_RUINS_TEST_PASSED": 0x50,
    "EVENT_MECHA_RIDLEY_KILLED": 0x4A,
    "EVENT_ESCAPED_CHOZODIA": 0x4B,
}


TRACKER_EVENT_FLAGS = list(EVENT_FLAGS.keys())


def cmd_deathlink(self):
    """Toggle death link from client. Overrides default setting."""

    client_handler = self.ctx.client_handler
    client_handler.death_link.enabled = not client_handler.death_link.enabled
    Utils.async_start(
        self.ctx.update_death_link(client_handler.death_link.enabled),
        name="Update Death Link"
    )


def cmd_kill(self):
    """Receive a death link on command."""
    self.ctx.client_handler.death_link.pending = True


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
    SPOSE_SAVING_LOADING_GAME = 44

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
    gSamusData = get_symbol("gSamusData")
    gEquipment = get_symbol("gEquipment")
    gEventsTriggered = get_symbol("gEventsTriggered")
    gCurrentArea = get_symbol("gCurrentArea")
    gRandoLocationBitfields = get_symbol("gRandoLocationBitfields")
    gIncomingItemId = get_symbol("gIncomingItemId")
    gIncomingItemCount = get_symbol("gIncomingItemCount")
    gMultiworldItemCount = get_symbol("gMultiworldItemCount")
    gMultiworldItemSenderName = get_symbol("gMultiworldItemSenderName")


class QueuedItem(NamedTuple):
    network_items: List[NetworkItem]  # All should be the same item
    index: int  # Position of first instance


class ItemCollection(NamedTuple):
    starting: List[NetworkItem]
    local: List[NetworkItem]
    remote: List[NetworkItem]


class MZMClient(BizHawkClient):
    game = "Metroid Zero Mission"
    system = "GBA"
    patch_suffix = ".apmzm"

    local_checked_locations: Set[int]
    local_set_events: Dict[str, bool]
    local_area: int

    remote_items_acquired: Optional[List[NetworkItem]]
    received_items: ItemCollection
    queued_item: Optional[QueuedItem]

    rom_slot_name: Optional[str]

    death_link: DeathLinkCtx

    dc_pending: bool

    def __init__(self) -> None:
        super().__init__()
        self.remote_items_acquired = None
        self.received_items = ItemCollection([], [], [])
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
        client_ctx.items_handling = 0b111
        client_ctx.want_slot_data = True
        try:
            client_ctx.seed_name = seed_name_bytes.decode("utf-8")
        except UnicodeDecodeError:
            logger.info("Could not determine seed name from ROM. Are you sure this ROM matches this client version?")
            return False

        client_ctx.command_processor.commands["deathlink"] = cmd_deathlink
        # client_ctx.command_processor.commands["kill"] = cmd_kill
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

    async def send_game_state(self, client_ctx: BizHawkClientContext, gameplay_state: Tuple[int, int]):
        bizhawk_ctx = client_ctx.bizhawk_ctx

        try:
            read_result = iter(await bizhawk.read(bizhawk_ctx, [
                read8(ZMConstants.gCurrentArea),
                read(ZMConstants.gEventsTriggered, 4 * 3),
                read(ZMConstants.gRandoLocationBitfields, 4 * ZMConstants.AREA_MAX),
            ]))
        except bizhawk.RequestFailedError:
            return

        gMainGameMode = gameplay_state[0]
        gCurrentArea = next_int(read_result)
        gEventsTriggered = struct.unpack(f"<3I", next(read_result))
        gRandoLocationBitfields = struct.unpack(f"<{ZMConstants.AREA_MAX}I", next(read_result))

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
                        checked_locations.add(location.code)
                    location_flags >>= 1

        for name, number in EVENT_FLAGS.items():
            block = gEventsTriggered[number // 32]
            flag = 1 << (number & 31)
            if block & flag:
                set_events[name] = True

        if self.local_checked_locations != checked_locations:
            self.local_checked_locations = checked_locations
            self.received_items = self.create_collection(client_ctx)
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
            self.local_set_events = set_events
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

        if self.local_area != gCurrentArea and client_ctx.slot is not None:
            self.local_area = gCurrentArea
            await client_ctx.send_msgs([{
                "cmd": "Set",
                "key": f"mzm_area_{client_ctx.team}_{client_ctx.slot}",
                "default": 0,
                "want_reply": False,
                "operations": [{"operation": "replace", "value": gCurrentArea}]
            }])

    async def handle_received_items(self, client_ctx: BizHawkClientContext, received_items: ItemCollection):
        bizhawk_ctx = client_ctx.bizhawk_ctx

        try:
            read_result = iter(await bizhawk.read(bizhawk_ctx, [read8(ZMConstants.gMultiworldItemCount)]))
        except bizhawk.RequestFailedError:
            return

        gMultiworldItemCount = next_int(read_result)

        if (self.remote_items_acquired is None):
            self.remote_items_acquired = list(itertools.islice(received_items.remote, gMultiworldItemCount))

        if self.queued_item is not None and gMultiworldItemCount > self.queued_item.index:
            self.remote_items_acquired.extend(self.queued_item.network_items)
            self.queued_item = None

        if self.queued_item is None and len(self.remote_items_acquired) < len(received_items.remote):
            new_items = Counter(item.item for item in received_items.remote) - Counter(item.item for item in self.remote_items_acquired)
            next_item, next_item_count = next(iter(new_items.items()))
            copies = list(itertools.islice(filter(lambda item: item.item == next_item, reversed(received_items.remote)), next_item_count))
            copies.reverse()
            self.queued_item = QueuedItem(copies, len(self.remote_items_acquired))

        if gMultiworldItemCount > len(received_items.remote):
            self.remote_items_acquired = received_items.remote

    async def update_equipment(self, client_ctx: BizHawkClientContext, gameplay_state: Tuple[int, int], items: Iterable[NetworkItem]):
        bizhawk_ctx = client_ctx.bizhawk_ctx

        try:
            read_result = iter(await bizhawk.read(bizhawk_ctx, [
                read8(ZMConstants.gMultiworldItemCount),
                read8(ZMConstants.gDifficulty),
            ]))
        except bizhawk.RequestFailedError:
            return

        gMainGameMode, gGameModeSub1 = gameplay_state
        gMultiworldItemCount = next_int(read_result)
        gDifficulty = next_int(read_result)

        guard_list = [
            # Ensure game state hasn't changed
            guard16(ZMConstants.gMainGameMode, gMainGameMode),
            guard16(ZMConstants.gGameModeSub1, gGameModeSub1),
        ]
        acquired_items = Counter(item_data_table[client_ctx.item_names.lookup_in_game(item.item)] for item in items)
        try:
            read_result = await bizhawk.guarded_read(
                bizhawk_ctx,
                [read(ZMConstants.gEquipment + 12, 4),
                 read8(ZMConstants.gEquipment + 18)],
                guard_list)
        except bizhawk.RequestFailedError:
            return
        if not read_result:
            return
        current_majors = read_result[0]
        beams, beam_activation, majors, major_activation = current_majors
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
                        guard_list
                    )
                def write_amounts(size, max, current, expect_current=None):
                    return bizhawk.guarded_write(
                        bizhawk_ctx,
                        [write(ZMConstants.gEquipment + max_offset, max.to_bytes(size // 8, 'little')),
                         write(ZMConstants.gEquipment + current_offset, current.to_bytes(size // 8, 'little'))],
                        (guard_list + [guard(ZMConstants.gEquipment + current_offset, expect_current.to_bytes(size // 8, 'little'))])
                            if expect_current is not None else guard_list
                    )
                try:
                    if item.id == ItemID.EnergyTank:
                        read_result = await read_amounts(16)
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
            unknown_items = client_ctx.slot_data["unknown_items_always_usable"] or self.local_set_events["EVENT_RUINS_TEST_PASSED"]
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
                guard_list + [
                    guard(ZMConstants.gEquipment + 12, current_majors),
                    guard8(ZMConstants.gEquipment + 18, current_suit)])
            await bizhawk.guarded_write(
                bizhawk_ctx,
                [write16(ZMConstants.gMultiworldItemCount, len(self.remote_items_acquired))],
                guard_list + [guard16(ZMConstants.gMultiworldItemCount, gMultiworldItemCount)])
        except bizhawk.RequestFailedError:
            return

    async def write_received_item(self, client_ctx: BizHawkClientContext, gameplay_state: Tuple[int, int]):
        bizhawk_ctx = client_ctx.bizhawk_ctx

        try:
            read_result = iter(await bizhawk.read(bizhawk_ctx, [read8(ZMConstants.gMultiworldItemCount)]))
        except bizhawk.RequestFailedError:
            return

        gMainGameMode, gGameModeSub1 = gameplay_state
        gMultiworldItemCount = next_int(read_result)

        guard_list = [
            guard16(ZMConstants.gMainGameMode, gMainGameMode),
            guard16(ZMConstants.gGameModeSub1, gGameModeSub1),
            guard8(ZMConstants.gIncomingItemId, ZMConstants.ITEM_NONE),
            guard16(ZMConstants.gMultiworldItemCount, gMultiworldItemCount),
        ]

        if gMultiworldItemCount > self.queued_item.index:
            return

        next_item = self.queued_item.network_items[0]
        item_data = item_data_table[client_ctx.item_names.lookup_in_game(next_item.item)]
        copies = len(self.queued_item.network_items)
        if next_item.player == client_ctx.slot:
            sender = Message([TERMINATOR_CHAR])
        else:
            sender = (Message(client_ctx.player_names[next_item.player])
                        .trim_to_max_width(LINE_WIDTH - 79)
                        .append(TERMINATOR_CHAR))

        try:
            await bizhawk.guarded_write(
                bizhawk_ctx,
                [write8(ZMConstants.gIncomingItemId, item_data.id),
                 write8(ZMConstants.gIncomingItemCount, copies),
                 write(ZMConstants.gMultiworldItemSenderName, sender.to_bytes())],
                guard_list)
        except bizhawk.RequestFailedError:
            return

    async def game_watcher(self, client_ctx: BizHawkClientContext) -> None:
        if self.dc_pending:
            await client_ctx.disconnect()
            return

        if client_ctx.server is None or client_ctx.server.socket.closed or client_ctx.slot_data is None:
            return

        if self.death_link.update_pending:
            await client_ctx.update_death_link(self.death_link.enabled)
            self.death_link.update_pending = False

        bizhawk_ctx = client_ctx.bizhawk_ctx

        try:
            read_result = iter(await bizhawk.read(bizhawk_ctx, [
                read16(ZMConstants.gMainGameMode),
                read16(ZMConstants.gGameModeSub1),
            ]))
        except bizhawk.RequestFailedError:
            return

        gMainGameMode = next_int(read_result)
        gGameModeSub1 = next_int(read_result)

        gameplay_state = (gMainGameMode, gGameModeSub1)

        if not self.is_state_read_safe(gMainGameMode, gGameModeSub1):
            return

        await self.send_game_state(client_ctx, gameplay_state)

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
                samus_pose = next_int(iter(await bizhawk.read(
                    bizhawk_ctx,
                    [read8(ZMConstants.gSamusData + 0)]  # gSamusData.pose
                )))
                if samus_pose != ZMConstants.SPOSE_SAVING_LOADING_GAME:
                    await bizhawk.guarded_write(
                        bizhawk_ctx,
                        [write16(ZMConstants.gEquipment + 6, 0)],  # gEquipment.currentEnergy
                        guard_list + [guard8(ZMConstants.gSamusData + 0, samus_pose)]  # gSamusData.pose
                    )
            except bizhawk.RequestFailedError:
                return

        received_items = self.received_items
        if not client_ctx.slot_data["remote_items"]:
            remote_items = [item for item in received_items.remote if item.player != client_ctx.slot or item.location <= 0]
            received_items = self.received_items._replace(remote=remote_items)

        await self.handle_received_items(client_ctx, received_items)

        acquired_items = itertools.chain(received_items.starting, received_items.local, self.remote_items_acquired)
        await self.update_equipment(client_ctx, gameplay_state, acquired_items)

        if self.queued_item is not None:
            await self.write_received_item(client_ctx, gameplay_state)

    def create_collection(self, ctx: BizHawkClientContext):
        def is_local(item: NetworkItem):
            return item.player == ctx.slot and item.location in self.local_checked_locations

        starting = itertools.takewhile(lambda item: item.location == -2, ctx.items_received)
        t1, t2 = itertools.tee(itertools.dropwhile(lambda item: item.location == -2, ctx.items_received))
        remote = itertools.filterfalse(is_local, t1)
        local = filter(is_local, t2)
        return ItemCollection(list(starting), list(local), list(remote))

    def on_package(self, ctx: BizHawkClientContext, cmd: str, args: dict) -> None:
        if cmd == "Connected":
            if args["slot_data"].get("death_link"):
                self.death_link.enabled = True
                self.death_link.update_pending = True
        if cmd == "RoomInfo":
            if ctx.seed_name and ctx.seed_name != args["seed_name"]:
                # CommonClient's on_package displays an error to the user in this case, but connection is not cancelled.
                self.dc_pending = True
        if cmd == "ReceivedItems":
            self.received_items = self.create_collection(ctx)
        if cmd == "Bounced":
            tags = args.get("tags", [])
            if "DeathLink" in tags:
                self.death_link.pending = True
