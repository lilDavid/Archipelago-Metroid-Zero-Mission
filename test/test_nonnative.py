from typing import Type
from test.bases import TestBase
from worlds.AutoWorld import World
from ..nonnative_items import compatible_games

class MZMTestNonNativeItems(TestBase):
    """Ensures that the names of compatible games and items are spelled correctly"""

    def _test_item_compatibility(self, cls: Type[World]):
        self.assertTrue(cls.game in compatible_games, f"Metroid: Zero Mission does not display items from {cls.game}")
        for item_name in compatible_games[cls.game]:
            with self.subTest(item_name):
                self.assertTrue(item_name in cls.item_names, f"{item_name} is not a valid item for {cls.game}")

    def test_sm_item_compatibility(self):
        try:
            from worlds.sm import SMWorld
        except ImportError:
            return
        self._test_item_compatibility(SMWorld)

    def test_smz3_item_compatibility(self):
        try:
            from worlds.smz3 import SMZ3World
        except ImportError:
            return
        self._test_item_compatibility(SMZ3World)
