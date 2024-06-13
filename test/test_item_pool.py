from collections import Counter

from worlds.mzm.test import MZMTestBase


class MZMTestItemPool(MZMTestBase):
    options = {
        "junk_fill_weights": { "Nothing": 1, "Missile Tank": 0, "Super Missile Tank": 0, "Power Bomb Tank": 0 },
    }

    def setUp(self):
        super().setUp()
        self.item_counts = Counter(item.name for item in self.multiworld.itempool)

    def test_item_pool_covers_all_locations(self):
        """Ensure junk fill is not normally required."""
        self.assertNotIn("Nothing", self.item_counts, "Item pool required junk fill")

    def test_default_fill_matches_vanilla(self):
        """Ensure that the maximum capacities are the same as vanilla."""

        with self.subTest("Maximum energy"):
            self.assertEqual(1299, 99 + 100 * self.item_counts["Energy Tank"])
        with self.subTest("Maximum Missile ammo"):
            self.assertEqual(250, 5 * self.item_counts["Missile Tank"])
        with self.subTest("Maximum Super Missile ammo"):
            self.assertEqual(30, 2 * self.item_counts["Super Missile Tank"])
        with self.subTest("Maximum Power Bombs"):
            self.assertEqual(18, 2 * self.item_counts["Power Bomb Tank"])
