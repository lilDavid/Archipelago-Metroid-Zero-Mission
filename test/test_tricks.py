from .bases import MZMTestBase
from ..options import LogicDifficulty


class MZMTestTricks(MZMTestBase):

    options = {
        "logic_difficulty": LogicDifficulty.option_normal,
        "ibj_in_logic": 0,
        "tricks_allowed": {"Brinstar Ceiling E-Tank Tricky Spark"},
        "tricks_denied": {"Varia Area Access Enemy Freeze"},
    }

    def test_trick_only_accessible(self):
        self.assertFalse(self.can_reach_location("Brinstar Ceiling E-Tank"))
        self.collect_by_name("Morph Ball")
        self.collect_by_name("Speed Booster")
        self.collect_by_name("Bomb")
        self.collect_by_name("Varia Suit")
        self.collect_by_name("Power Grip")
        self.collect_by_name("Ice Beam")
        self.assertTrue(self.can_reach_location("Brinstar Ceiling E-Tank"))
        self.assertFalse(self.can_reach_location("Brinstar Acid Near Varia"))
