"""
Functions used for dictating logic made for making rules in rules.py
"""

from BaseClasses import MultiWorld
from worlds.AutoWorld import LogicMixin
from worlds.mzm import MZMOptions


# TODO: Add missing logic options
# TODO: Fine tune boss logic
# TODO: rewrite without LogixMixin

class MZMLogic(LogicMixin):

    def mzm_options(self, player: int) -> MZMOptions:
        return self.multiworld.worlds[player].options

    def mzm_has_missiles(self, player: int) -> bool:
        return self.has_any({"Missile Tank", "Super Missile Tank"}, player)

    def mzm_has_missile_count(self, player: int, required_missiles: int) -> int:
        # TODO: somehow account for Hard mode
        missilecount = (self.count("Missile Tank", player) * 5) + (self.count("Super Missile Tank", player) * 2)
        return missilecount >= required_missiles

    def mzm_has_super_missiles(self, player: int) -> bool:
        return self.has("Super Missile Tank", player)

    def mzm_has_power_bombs(self, player: int):
        return self.has("Power Bomb Tank", player)

    def mzm_power_bomb_count(self, player: int, required_pbs: int):
        pbcount = 0
        pbcount += (self.count("Power Bomb Tank", player) * 2)
        return pbcount >= required_pbs

    def mzm_can_regular_bomb(self, player: int):
        return self.has_all({"Morph Ball", "Bomb"}, player)

    # this may be different from can_regular_bomb later and also just reads easier in some rules
    def mzm_can_ballcannon(self, player: int):
        return self.has_all({"Morph Ball", "Bomb"}, player)

    def mzm_can_bomb_block(self, player: int) -> bool:
        return (self.has("Morph Ball", player)
                and self.has_any({"Bomb","Power Bomb Tank"}, player))

    # checked for ability to clear blocks that would require long beam to hit
    def mzm_can_long_beam(self, player: int) -> bool:
        return (self.has("Long Beam", player)
                or self.mzm_has_missile_count(player, 3)
                or self.mzm_can_bomb_block(player))

    def mzm_can_hi_jump(self, player: int) -> bool:
        return self.has("Hi-Jump", player) or self.mzm_can_space_jump(player) or self.mzm_can_ibj(player)

    # this particular combination is extremely common
    def mzm_can_hj_sj_ibj_or_grip(self, player: int) -> bool:
        return self.mzm_can_hi_jump(player) or self.has("Power Grip", player)

    def mzm_can_ballspark(self, player: int) -> bool:
        return self.has_all({"Morph Ball", "Hi-Jump", "Speed Booster"}, player)

    def mzm_can_space_jump(self, player: int) -> bool:
        return ((self.has("EVENT_CHOZO_GHOST_DEFEATED", player)
                 or bool(self.mzm_options(player).unknown_items_always_usable.value))
                and self.has("Space Jump", player))

    def mzm_can_traverse_heat(self, player: int) -> bool:
        return self.has("Varia Suit", player) or self.mzm_can_gravity_suit(player)

    # currently used for both heated rooms AND lava dives
    def mzm_hellrun(self, player: int, required_etanks: int) -> bool:
        return (bool(self.mzm_options(player).heatruns_lavadives.value)
                and (self.count("Energy Tank", player) >= required_etanks))

    def mzm_can_gravity_suit(self, player: int) -> bool:
        return ((self.has("EVENT_CHOZO_GHOST_DEFEATED", player)
                 or bool(self.mzm_options(player).unknown_items_always_usable.value))
                and self.has("Gravity Suit", player))

    def mzm_can_ibj(self, player: int) -> bool:
        return bool(self.mzm_options(player).ibj_in_logic.value) and self.mzm_can_regular_bomb(player)

    def mzm_can_walljump(self, player: int) -> bool:
        return bool(self.mzm_options(player).walljumps_in_logic.value)

    def mzm_can_tricky_sparks(self, player: int) -> bool:
        return False and self.has("Speed Booster", player)  # TODO: add option

    def mzm_brinstar_past_hives(self, player: int) -> bool:
        return self.has("Morph Ball", player) and self.mzm_has_missile_count(player, 10)

    # used for the items in this area as well as determining whether the ziplines can be activated
    # it's technically possible to do the climb after ballcannon with just hi-jump using tight morph jumps
    # TODO: add solo hi-jump logic once an option for advanced tricks is added
    def mzm_kraid_upper_right(self, player: int) -> bool:
        return (self.mzm_has_missiles(player)
                and self.mzm_can_ballcannon(player)
                and (self.mzm_can_walljump(player)
                     or self.mzm_can_space_jump(player)
                     or self.has("Power Grip", player))
                ) and (self.mzm_can_ibj(player)
                       or self.has("Power Grip", player)
                       or (self.has("Ice Beam", player) and self.has_any({"Bomb", "Hi-Jump"}, player)))

    # access to lower kraid via left shaft
    # TODO: add logic for acid worm skip
    def mzm_kraid_left_shaft_access(self, player: int) -> bool:
        return (
                (self.mzm_can_ibj(player)
                 or self.has_any({"Power Grip", "Hi-Jump"}, player)
                 )
                and self.mzm_can_bomb_block(player)
                and (self.mzm_can_regular_bomb(player) or self.has("Hi-Jump", player))
                and (self.mzm_kraid_upper_right(player)
                     or self.mzm_can_space_jump(player)
                     or (self.mzm_can_gravity_suit(player)
                         and (self.mzm_can_ibj(player) or self.mzm_can_tricky_sparks(player)))
                     )
        )

    def mzm_norfair_right_shaft_access(self, player: int) -> bool:
        return self.mzm_can_hj_sj_ibj_or_grip(player) or self.has("Speed Booster", player)

    def mzm_norfair_upper_right_shaft(self, player: int) -> bool:
        return (self.mzm_norfair_right_shaft_access(player)
                and (self.mzm_can_hj_sj_ibj_or_grip(player)
                     or self.has("Ice Beam", player)
                     or self.mzm_can_walljump(player))
                )

    # used for one item and the ridley shortcut
    def mzm_norfair_behind_ice_beam(self, player: int) -> bool:
        return (self.mzm_norfair_upper_right_shaft(player)
                and (self.mzm_can_long_beam(player) or self.has("Wave Beam", player))
                and ((self.has("Ice Beam", player) and self.has_any({"Hi-Jump", "Power Grip"},
                                                                    player))  # to get up the rippers
                     or self.mzm_can_ibj(player)
                     or (self.mzm_can_walljump(player) and self.has("Power Grip", player)))
                )

    def mzm_norfair_lower_right_shaft(self, player: int) -> bool:
        return (self.mzm_norfair_right_shaft_access(player)
                and (self.has("Screw Attack", player)
                     or (self.has("Speed Booster", player) and self.mzm_can_ballcannon(player)))
                )

    def mzm_norfair_to_save_behind_hijump(self, player: int) -> bool:
        return (self.mzm_norfair_lower_right_shaft(player)
                and self.mzm_has_missiles(player)
                and self.mzm_can_bomb_block(player)
                and (self.mzm_can_ibj(player)
                     or (self.mzm_has_power_bombs(player) and self.has("Hi-Jump", player))
                     or (self.has("Bomb", player) and self.has_any({"Hi-Jump", "Power Grip"}, player))
                )
                and (self.mzm_can_hj_sj_ibj_or_grip(player) or self.mzm_can_walljump(player)
                     or self.has("Ice Beam", player))
                and (self.mzm_can_traverse_heat(player)
                     or self.mzm_hellrun(player, 6))
                and (self.mzm_can_ibj(player) or self.mzm_can_space_jump(player)
                     or (self.has("Speed Booster", player)
                         and (self.mzm_can_bomb_block(player) or self.has("Screw Attack"), player))
                )
        )

    # TODO: double check this
    def mzm_norfair_shortcut(self, player: int) -> bool:
        return (self.mzm_norfair_behind_ice_beam(player)
                and self.mzm_has_missiles(player)
                and (self.mzm_can_ibj(player)
                     or (self.has("Power Grip", player)
                         and (self.mzm_can_space_jump(player) or self.mzm_can_walljump(player))
                         and self.mzm_can_bomb_block(player)))
                )

    def mzm_norfair_bottom_right_shaft(self, player: int) -> bool:
        return (
                (self.mzm_norfair_to_save_behind_hijump(player)
                 and self.mzm_has_missile_count(player, 4)
                 and self.has_all({"Wave Beam", "Speed Booster"}, player)
                 )
                or (self.mzm_norfair_shortcut(player)))

    def mzm_ridley_left_shaft_access(self, player: int) -> bool:
        return (
                self.mzm_has_super_missiles(player)
                and (self.mzm_can_hj_sj_ibj_or_grip(player) or self.mzm_can_walljump(player)
                     or self.has("Ice Beam", player) or self.mzm_can_bomb_block(player))
                and (self.mzm_can_traverse_heat(player) or self.mzm_hellrun(player, 1))
        )

    # going the "intended" way, to the left of the elevator, down, and back to the right to get to the right shaft
    def mzm_ridley_longway_right_shaft_access(self, player: int) -> bool:
        return (self.mzm_ridley_left_shaft_access(player)
                and (self.has("Power Grip", player)
                     and (self.mzm_can_hj_sj_ibj_or_grip(player) or self.mzm_can_walljump(player)))
                )

    # taking the shortcut, to the right of the elevator and up the hole
    def mzm_ridley_shortcut_right_shaft_access(self, player: int) -> bool:
        return (
                self.mzm_has_missiles(player)
                and (self.mzm_can_ibj(player)
                     or (self.has("Power Grip", player) and self.mzm_has_power_bombs(player)
                         and self.has_any({"Ice Beam", "Hi-Jump"}, player)))
                and (self.mzm_can_bomb_block(player) or self.has("Screw Attack", player))
        )

    # getting into the gap at the start of "ball room" and subsequently into the general area of ridley himself
    def mzm_ridley_central_access(self, player: int) -> bool:
        return (
                (self.mzm_ridley_shortcut_right_shaft_access(player) or self.mzm_ridley_longway_right_shaft_access(
                    player))
                and (self.mzm_can_ibj(player) or self.has_any({"Hi-Jump", "Power Grip"}, player))
        )

    # ice beam makes dealing with the pirates a ton easier. etanks keeps you from needing to go too deep before you have
    # a decent chance to survive. the rest is the strictest requirement to get in and back out of the chozo ghost area
    def mzm_chozodia_ghost_from_upper_crateria_door(self, player: int) -> bool:
        return (
            self.has("Ice Beam", player) and (self.count("Energy Tank", player) >= 4)
            and self.mzm_has_missiles(player)
            and (self.mzm_can_walljump(player) or self.mzm_can_ibj(player)
                 or self.mzm_can_space_jump(player))
            and self.count("Power Bomb Tank", player) >= 2
        )

    def mzm_chozodia_glass_tube_from_crateria_door(self, player: int) -> bool:
        return (
            # from upper door
            (self.has("Ice Beam", player) and (self.count("Energy Tank", player) >= 2)
                and self.mzm_has_missiles(player) and self.has("Power Bomb Tank", player)
                and (self.mzm_can_space_jump(player) or self.mzm_can_ibj(player)))
            # from lower door
            or (self.has("Ice Beam", player) and (self.count("Energy Tank", player) >= 2)
                and (self.mzm_can_ibj(player) or self.mzm_can_space_jump(player) or self.has("Speed Booster", player))
                and self.mzm_has_missile_count(player, 6)
                and self.has("Power Bomb Tank", player)
                )
        )

    # from the ruins to the save station next to the big room with all the tripwires
    def mzm_chozodia_tube_to_mothership_central(self, player: int) -> bool:
        return (self.mzm_chozodia_glass_tube_from_crateria_door(player)
                and self.count("Energy Tank", player) >= 6
                and ((self.has("Hi-Jump", player) and (self.mzm_can_walljump(player) or self.has("Power Grip", player)))
                    or self.mzm_can_ibj(player) or self.mzm_can_space_jump(player)
                )
        )

    def mzm_chozodia_to_cockpit(self, player: int) -> bool:
        return (((self.mzm_can_walljump(player) and self.has("Hi-Jump", player)) or self.mzm_can_ibj(player)
                 or self.mzm_can_space_jump(player))
                and self.count("Energy Tank", player) >= 6
                and self.has("Ice Beam", player)
                and self.mzm_has_missiles(player)
                and (self.has("Bomb", player) or self.count("Power Bomb Tank", player) >= 2))
