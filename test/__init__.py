from test.bases import WorldTestBase
from test.general import setup_solo_multiworld
from worlds import AutoWorldRegister


class MZMTestBase(WorldTestBase):
    game = "Metroid Zero Mission"

    def test_always_accessible(self) -> None:
        self.assertTrue(self.can_reach_location("Brinstar Morph Ball"))
