"""
Classes and functions related to interfacing with the BizHawk Client for Metroid: Zero Mission
"""
from typing import TYPE_CHECKING, List

from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import (BizHawkClientContext)

"""
class MZMClient(BizHawkClient):
    game = "Metroid Zero Mission"
    system = "GBA"
    patch_suffix = ".apmzm"
    local_checked_locations: List[int]
    rom_slot_name: str

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = []
        self.rom_slot_name = None

    async def validate_rom(self, client_ctx: BizHawkClientContext) -> bool:
        
        haven't actually tested this yet but it looks like the right place
        TODO: understand what's up with the PlayerName/slot_name stuff
        I assume the slot name gets patched into the ROM somewhere, should probably look there
        
        try:
            read_result = iter(await bizhawk.read(client_ctx.bizhawk_ctx, [
                read(0xA0, 16),
                read(get_symbol("PlayerName"), 64)
            ]))
        except RequestFailedError:
            return False  # Should verify on the next pass

        game_name = next(read_result).decode("ascii")
        slot_name_bytes = bytes(filter(None, next(read_result)))

        if game_name not in ("ZEROMISSIONBMXE"):
            return False
        
        # Check if we can read the slot name. Doing this here instead of set_auth as a protection against
        # validating a ROM where there's no slot name to read.
        try:
            self.rom_slot_name = slot_name_bytes.decode('utf-8')
        except UnicodeDecodeError:
            logger.info("Could not read slot name from ROM. Are you sure this ROM matches this client version?")
            return False
        """"""
        return True

    async def set_auth(self, client_ctx: BizHawkClientContext) -> None:
        client_ctx.auth = self.rom_slot_name

    async def game_watcher(self, client_ctx: BizHawkClientContext) -> None:
        variable = 0
    # items: check if not in main menu or game over screen, otherwise any time should be fine
    # death link: additionally check if not in door transition eventually (it works otherwise but is jank)

    #def on_package(self, ctx: BizHawkClientContext, cmd: str, args: dict) -> None:
"""
