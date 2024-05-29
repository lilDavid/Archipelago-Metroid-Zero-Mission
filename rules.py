"""
Logic rule definitions for Metroid: Zero Mission
"""

from worlds.generic.Rules import add_rule, set_rule
from .logic import MZMLogic as logic
from BaseClasses import MultiWorld


# TODO: eventually take options as parameters and use that to determine rules

def set_rules(multiworld: MultiWorld, player, locations):
    # starting with most restrictive "newbie" logic -- no IBJs or walljumps
    # should long beam be counted as required? currently assuming no
    # should speed booster shortcut missile require speed? would a newbie know to go in backwards?
    brinstar_access_rules = {
        "Brinstar Morph Ball Cannon": lambda state: logic.mzm_has_bombs(state, multiworld, player),
        "Brinstar Long Beam": lambda state: state.has("Morph Ball", player),
        "Brinstar Ceiling E-Tank":
            lambda state: (logic.mzm_can_hi_jump(state, multiworld, player)
                           or logic.mzm_can_space_jump(state, multiworld, player)
                           or state.has("Speed Booster", player)),
        "Brinstar Missile Above Super":
            lambda state: (logic.mzm_can_bomb_any(state, multiworld, player)
                           and (logic.mzm_can_space_jump(state, multiworld, player)
                                or state.has("Ice Beam", player)
                                or (logic.mzm_can_hi_jump(state, multiworld, player)
                                    and state.has("Power Grip", player)
                                    )
                                )
                           ),
        "Brinstar Super Missile": lambda state: (state.has("Speed Booster", player)),
        "Brinstar Top Missile":
            lambda state: (state.has("Power Grip", player)
                           and (state.has("Ice Beam", player)
                                or logic.mzm_can_space_jump(state, multiworld, player))
                           ),
        "Brinstar Speed Booster Shortcut Missile": lambda state: (logic.mzm_can_bomb_any(state, multiworld, player)),
        "Brinstar Varia Suit":
            lambda state: (logic.mzm_can_bomb_any(state, multiworld, player)
                           and state.has("Power Grip", player)
                           and logic.mzm_can_hi_jump(state, multiworld, player)),
        "Brinstar Worm drop":
            lambda state: (state.has("Morph Ball", player)
                           and logic.mzm_has_missiles(state, multiworld, player)),
        "Brinstar Varia E-Tank":
            lambda state: (logic.mzm_can_bomb_any(state, multiworld, player)
                           and state.has("Power Grip", player)
                           and logic.mzm_can_hi_jump(state, multiworld, player)
                           and logic.mzm_etank_count(state, multiworld, player) >= 1),
        "Brinstar First Missile": lambda state: state.has("Morph Ball", player),
        "Brinstar Hive Missile":
            lambda state: (state.has("Morph Ball", player)
                           and logic.mzm_has_missile_count(state, multiworld, player) >= 10),
        "Brinstar Under Bridge":
            lambda state: (logic.mzm_can_bomb_any(state, multiworld, player)
                           and logic.mzm_has_missiles(state, multiworld, player)),
        "Brinstar Post-Hive Missile":
            lambda state: (state.has("Morph Ball", player)
                           and logic.mzm_has_missile_count(state, multiworld, player) >= 10),
        "Brinstar Upper Pillar Missile": lambda state: logic.mzm_can_bomb_any(state, multiworld, player),
        "Brinstar Missile Behind Bombs":
            lambda state: (state.has("Morph Ball", player)
                           and logic.mzm_has_missile_count(state, multiworld, player) >= 10),
        "Brinstar Bomb":
            lambda state: (state.has("Morph Ball", player)
                           and logic.mzm_has_missile_count(state, multiworld, player) >= 10),
        "Brinstar Post-Hive E-Tank":
            lambda state: (state.has("Morph Ball", player)
                           and logic.mzm_has_missile_count(state, multiworld, player) >= 10)
    }

    kraid_access_rules = {
    }

    norfair_access_rules = {}

    ridley_access_rules = {}

    #TODO: also require Mother Brain defeated
    tourian_access_rules = {
        "Tourian Left of Mother Brain": lambda state: (state.has("Speed Booster", player)
                                                       and logic.mzm_can_space_jump(state, multiworld, player)),
        "Tourian Under Mother Brain ": lambda state: (logic.mzm_has_super_missiles(state, multiworld, player))
    }

    crateria_access_rules = {
        "Crateria Power Bomb": lambda state: (logic.mzm_has_power_bombs(state, multiworld, player)
                                              and logic.mzm_can_space_jump(state, multiworld, player)
                                              and state.has("Speed Booster", player))
    }

    chozodia_access_rules = {}

    access_rules = {
        **brinstar_access_rules,
        **kraid_access_rules,
        **norfair_access_rules,
        **ridley_access_rules,
        **tourian_access_rules,
        **crateria_access_rules,
        **chozodia_access_rules
    }

    for i in locations:
        location = multiworld.get_location(i, player)
        try:
            add_rule(location, access_rules[i])
        except KeyError:
            continue