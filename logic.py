"""
Functions used for dictating logic made for making rules in rules.py
"""

from BaseClasses import MultiWorld
from worlds.AutoWorld import LogicMixin


# TODO: Eventually add "Samus Strength" parameters used for boss logic
# TODO: do i need to use a LogicMixin for this?

class MZMLogic(LogicMixin):

    def mzm_etank_count(self, world: MultiWorld, player: int) -> int:
        return self.count("Energy Tank", player)

    def mzm_has_missiles(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({"Missile", "Missile Tank", "Super Missile", "Super Missile Tank"}, player)

    def mzm_has_missile_count(self, world: MultiWorld, player: int) -> int:
        count = 0
        if self.has("Missile", player):
            count = 5
        count += self.count("Missile Expansion", player) * 5
        return count

    def mzm_has_super_missiles(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({"Super Missile", "Super Missile Tank"}, player)

    def mzm_has_power_bombs(self, world: MultiWorld, player: int):
        return self.has_any({"Power Bomb", "Power Bomb Tank"}, player)

    def mzm_has_bombs(self, world: MultiWorld, player: int):
        return self.has_all({"Morph Ball", "Bomb"}, player)

    def mzm_can_bomb_any(self, world: MultiWorld, player: int) -> bool:
        return (self.has("Morph Ball", player)
                and self.has_any({"Bomb", "Power Bomb", "Power Bomb Tank"}, player))
    # NOTE: PBs do NOT activate bomb cannons in vanilla. there is a patch for that, but idk if i like it

    # if PB jumping disabled
    #def mzm_can_bomb_jump(self, world: MultiWorld, player: int) -> bool:
    #    return (self.mzm_has_morph(self, world, player) and self.has("Bomb", player))

    # checked for ability to clear blocks that would require long beam to hit
    def mzm_can_long_beam(self, world: MultiWorld, player: int) -> bool:
        return (self.has_any({"Long Beam", "Missile", "Missile Tank",
                             "Super Missile", "Super Missile Tank"}, player)
                or self.mzm_can_bomb_any(world, player))
    # TODO: double check missiles/supers/bomb/PB also count as long beam for everything logical

    def mzm_can_hi_jump(self, world: MultiWorld, player: int) -> bool:
        return self.has("Hi-Jump Boots", player) or self.mzm_can_space_jump(world, player)
        # and suit state 1
    # or bombs and ibj enabled

    def mzm_can_space_jump(self, world: MultiWorld, player: int) -> bool:
        return self.has("Space Jump", player)  # and samus suit state is 1

    def mzm_can_traverse_heat(self, world: MultiWorld, player: int) -> bool:
        # TODO add logic for samus suit state here
        # TODO double check gravity by itself stops heat, i know it stops acid damage
        return self.has_any({"Varia Suit", "Gravity Suit"}, player)

    def mzm_has_gravity_suit(self, world: MultiWorld, player: int) -> bool:
        return self.has("Gravity Suit", player)  # and samus suit state is 1
