"""
Logic rule definitions for Metroid: Zero Mission.

Logic based on MZM Randomizer, by Biospark and dragonfangs.
"""

from worlds.generic.Rules import add_rule, set_rule
from .logic import MZMLogic as logic
from BaseClasses import MultiWorld


# Logic pass 1. Probably scuffed in edge cases but it seems to work.
def set_rules(multiworld: MultiWorld, player, locations):
    brinstar_access_rules = {
        "Brinstar Morph Ball Cannon": lambda state: logic.mzm_can_regular_bomb(state, player),
        "Brinstar Long Beam": lambda state: state.has("Morph Ball", player) and logic.mzm_can_long_beam(state, player),
        "Brinstar Ceiling E-Tank":
            lambda state: (state.has("Ice Beam", player) and state.has("EVENT_RIDLEY_DEFEATED", player)) or
                          logic.mzm_can_space_jump(state, player)
                          or logic.mzm_can_ibj(state, player),
        "Brinstar Missile Above Super":
            lambda state: (logic.mzm_can_bomb_block(state, player)
                           and (logic.mzm_can_space_jump(state, player)
                                or state.has("Ice Beam", player)
                                or state.has_all({"Hi-Jump", "Power Grip"}, player)
                                or logic.mzm_can_ibj(state, player)
                                or logic.mzm_can_walljump(state, player)
                                )
                           ),
        "Brinstar Super Missile": lambda state: logic.mzm_can_ballspark(state, player),
        "Brinstar Top Missile":
            lambda state: (state.has_all({"Morph Ball", "Power Grip"}, player)
                           and (state.has("Ice Beam", player)
                                or logic.mzm_can_space_jump(state, player)
                                or logic.mzm_can_walljump(state, player))
                           )
                          or logic.mzm_can_ibj(state, player),  # needs a rewrite
        "Brinstar Speed Booster Shortcut Missile":
            lambda state: (logic.mzm_can_bomb_block(state, player)
                           and logic.mzm_can_ballspark(state, player)
                           and (logic.mzm_can_walljump(state, player) or logic.mzm_can_hj_sj_ibj_or_grip(state, player))
                           ),
        "Brinstar Varia Suit":
            lambda state: (logic.mzm_can_ibj(state, player)
                           or logic.mzm_can_space_jump(state, player)
                           or state.has_all({"Power Grip", "Hi-Jump"}, player))
                          and (logic.mzm_can_regular_bomb(state, player)
                               or state.has_all({"Morph Ball", "Hi-Jump"}, player))
                          and ((logic.mzm_can_ibj(state, player)
                                or state.has("Power Grip", player)
                                or (state.has("Hi-Jump", player)
                                    and (logic.mzm_can_walljump(state, player)
                                         or logic.mzm_can_gravity_suit(state, player))
                                    )
                                )
                               and logic.mzm_can_bomb_block(state, player)
                               ),
        "Brinstar Worm drop":
            lambda state: (state.has("Morph Ball", player)
                           and logic.mzm_has_missiles(state, player)),
        "Brinstar Acid near Varia":
            lambda state: ((logic.mzm_can_ibj(state, player)
                            or logic.mzm_can_space_jump(state, player)
                            or state.has_all({"Power Grip", "Hi-Jump"}, player))
                           and (logic.mzm_can_regular_bomb(state, player)
                                or state.has_all({"Morph Ball", "Hi-Jump"}, player))
                           and (logic.mzm_can_long_beam(state, player)
                                and (logic.mzm_hellrun(state, player, 2)
                                     or state.has("Varia Suit", player)
                                     or logic.mzm_can_gravity_suit(state, player)
                                     )
                                )
                           ),
        "Brinstar First Missile": lambda state: state.has("Morph Ball", player),
        "Brinstar Behind Hive":
            lambda state: (state.has("Morph Ball", player)
                           and logic.mzm_has_missile_count(state, player, 5)),
        "Brinstar Under Bridge":
            lambda state: (logic.mzm_has_missiles(state, player)
                           and logic.mzm_can_bomb_block(state, player)),
        "Brinstar Post-Hive Missile": lambda state: logic.mzm_brinstar_past_hives(state, player),
        "Brinstar Upper Pillar Missile": lambda state: logic.mzm_can_bomb_block(state, player),
        "Brinstar Behind Bombs":
            lambda state: (logic.mzm_brinstar_past_hives(state, player)
                           and (state.has("Bomb", player)
                                or (logic.mzm_has_power_bombs(state, player) and state.has("Hi-Jump", player)))
                           ),
        "Brinstar Bomb":
            lambda state: logic.mzm_brinstar_past_hives(state, player),
        "Brinstar Post-Hive E-Tank":
            lambda state: logic.mzm_brinstar_past_hives(state, player)
    }

    # TODO: add norfair-kraid backdoor logic
    kraid_access_rules = {
        "Kraid Giant Hoppers Missile": lambda state: (
                logic.mzm_kraid_left_shaft_access(state, player)
                and (logic.mzm_can_ibj(state, player)
                     or state.has_all({"Morph Ball", "Power Grip"}, player))
        ),
        "Kraid Save Room Missile": lambda state: logic.mzm_can_bomb_block(state, player),
        "Kraid Crumble Block Missile": lambda state: (
                logic.mzm_kraid_upper_right(state, player)
                and state.has("Morph Ball", player)
                and state.has_any({"Bomb", "Hi-Jump"}, player)
        ),
        "Kraid Quad Ball Cannon Room": lambda state: (  # there are trickier ways to add later
                logic.mzm_kraid_left_shaft_access(state, player)
                and logic.mzm_kraid_upper_right(state, player)
                and logic.mzm_has_missiles(state, player)
        ),
        "Kraid Space Jump/Unknown Item 2": lambda state: (
                logic.mzm_kraid_left_shaft_access(state, player)
                and (state.has("Bomb", player) or logic.mzm_power_bomb_count(state, player, 2))
                and (state.has_any({"Power Grip", "Hi-Jump"}, player)
                     or logic.mzm_can_ibj(state, player)
                     )
                and logic.mzm_has_missiles(state, player)  # to get out
        ),
        "Kraid Acid Ballspark": lambda state: (
                (logic.mzm_can_ibj(state, player)
                 or state.has_any({"Power Grip", "Hi-Jump"}, player))
                and logic.mzm_can_bomb_block(state, player)
                and (logic.mzm_can_regular_bomb(state, player) or state.has("Hi-Jump", player))
                and (logic.mzm_can_gravity_suit(state, player)
                     and logic.mzm_can_ballspark(state, player))
        ),
        "Kraid Speed Booster": lambda state: state.can_reach("Kraid Defeated", "Location", player),
        "Kraid Worm Missile": lambda state: (
                logic.mzm_kraid_upper_right(state, player)
                and logic.mzm_has_missile_count(state, player, 30)
                and logic.mzm_can_bomb_block(state, player)
                and (logic.mzm_can_hj_sj_ibj_or_grip(state, player) or logic.mzm_can_walljump(state, player))
        ),
        "Kraid Pillar Missile": lambda state: logic.mzm_has_missiles(state, player),
        "Kraid Acid Fall": lambda state: (
                state.can_reach("Kraid Space Jump/Unknown Item 2", "Location", player)
                and state.has("Morph Ball", player)
                and (state.count("Energy Tank", player) >= 1)
        ),
        "Kraid Worm E-Tank": lambda state: logic.mzm_kraid_upper_right(state, player),
        "Kraid Speed Jump": lambda state: (logic.mzm_has_missiles(state, player)
                                           and state.has("Speed Booster", player)),
        "Kraid Upper Right Morph Ball Cannon": lambda state: logic.mzm_has_missiles(state, player)
                                                             and logic.mzm_can_ballcannon(state, player),
        "Kraid Defeated": lambda state: (
                state.can_reach("Kraid Space Jump/Unknown Item 2", "Location", player)
                and logic.mzm_has_missile_count(state, player, 30)
                and (state.count("Energy Tank", player) >= 1)
                and (state.has_all({"Hi-Jump", "Power Grip"}, player)
                     or state.has("Speed Booster", player)
                     or logic.mzm_can_ibj(state, player)
                     or logic.mzm_can_walljump(state, player))
        )
    }

    norfair_access_rules = {
        "Norfair Lava Power Bomb": lambda state: (
                logic.mzm_norfair_to_save_behind_hijump(state, player)
                and logic.mzm_has_missile_count(state, player, 5)
                and logic.mzm_can_gravity_suit(state, player)
                and (logic.mzm_can_space_jump(state, player) or logic.mzm_can_ibj(state, player))
        ),
        "Norfair Lava Missile": lambda state: (
                logic.mzm_norfair_to_save_behind_hijump(state, player)
                and logic.mzm_has_missile_count(state, player, 3)
                and (logic.mzm_can_bomb_block(state, player) or state.has("Wave Beam", player))
                and (logic.mzm_can_gravity_suit(state, player)
                     or (state.has("Varia Suit", player) and logic.mzm_hellrun(state, player, 5))
                     or logic.mzm_hellrun(state, player, 9))
                and (logic.mzm_can_ibj(state, player) or logic.mzm_can_space_jump(state, player)
                     or logic.mzm_can_walljump(state, player) or state.has_any({"Hi-Jump", "Power Grip"}, player))
        ),
        "Norfair Screw Attack": lambda state: (  # there's an obnoxious enemy freeze you can do here too but ehhh
                logic.mzm_norfair_to_save_behind_hijump(state, player)
                and (logic.mzm_can_tricky_sparks(state, player)
                     or (state.has("Screw Attack", player)
                         and (logic.mzm_can_space_jump(state, player)
                              or logic.mzm_can_walljump(state, player)))
                     or (logic.mzm_has_missile_count(state, player, 5)
                         and (logic.mzm_can_walljump(state, player)
                              or logic.mzm_can_ibj(state, player)
                              or logic.mzm_can_space_jump(state, player))
                         )
                     )
                and (logic.mzm_can_hj_sj_ibj_or_grip(state, player) or state.has("Ice Beam", player))
        ),
        "Norfair Screw Attack Missile": lambda state: (
                logic.mzm_norfair_to_save_behind_hijump(state, player)
                and state.has("Screw Attack", player)
                and (logic.mzm_can_tricky_sparks(state, player)
                     or logic.mzm_can_space_jump(state, player)
                     or logic.mzm_can_walljump(state, player)
                     or (logic.mzm_has_missile_count(state, player, 5)
                         and logic.mzm_can_ibj(state, player)))
                and (logic.mzm_can_hj_sj_ibj_or_grip(state, player) or state.has("Ice Beam", player))
        ),
        "Norfair Power Grip Missile": lambda state: (
                logic.mzm_can_ibj(state, player)
                or (state.has("Power Grip", player)
                    or state.has_all({"Hi-Jump", "Ice Beam"}, player))
        ),
        "Norfair Under Crateria Elevator": lambda state: (
                (logic.mzm_can_long_beam(state, player)
                 or logic.mzm_can_ballspark(state, player)
                 )
                and (state.has("Power Grip", player) or logic.mzm_can_ibj(state, player))
        ),
        "Norfair Wave Beam": lambda state: (
                logic.mzm_norfair_to_save_behind_hijump(state, player)
                and logic.mzm_has_missile_count(state, player, 4)),
        "Norfair Bomb Trap": lambda state: (
                logic.mzm_norfair_lower_right_shaft(state, player)
                and logic.mzm_has_super_missiles(state, player)
                and (logic.mzm_can_traverse_heat(state, player)
                     or logic.mzm_hellrun(state, player, 4)
                     or (state.has("Speed Booster", player)
                         and logic.mzm_hellrun(state, player, 1))
                     )
                and (state.has_all({"Morph Ball", "Bomb"}, player)
                     or (logic.mzm_can_space_jump(state, player)
                         and logic.mzm_has_power_bombs(state, player))
                     )
        ),
        "Norfair Bottom Heated Room First": lambda state: logic.mzm_norfair_to_save_behind_hijump(state, player),
        "Norfair Bottom Heated Room Second": lambda state: logic.mzm_norfair_to_save_behind_hijump(state, player),
        "Norfair Heated Room Under Brinstar Elevator": lambda state: (
                logic.mzm_norfair_lower_right_shaft(state, player)
                and logic.mzm_has_super_missiles(state, player)
                and (logic.mzm_can_traverse_heat(state, player)
                     or logic.mzm_hellrun(state, player, 4)
                     or (state.has("Speed Booster", player) and logic.mzm_hellrun(state, player, 1))
                     )
        ),
        "Norfair Space Boost Missile": lambda state: (  # TODO may need to rename, and double check this later
                logic.mzm_norfair_to_save_behind_hijump(state, player)
                and logic.mzm_has_super_missiles(state, player)
                and (state.has("Speed Booster", player)
                     or (logic.mzm_can_bomb_block(state, player)
                         or (state.has_all({"Long Beam", "Wave Beam"}, player))
                         and (state.has("Power Grip", player)
                              or (logic.mzm_can_gravity_suit(state, player) and state.has("Hi-Jump", player)))
                         )
                     )
                and (logic.mzm_can_hj_sj_ibj_or_grip(state, player) or logic.mzm_can_walljump(state, player))
                and ((logic.mzm_can_ibj(state, player) and logic.mzm_can_gravity_suit(state, player))
                     or (logic.mzm_can_space_jump(state, player) and state.has("Power Grip", player))
                     or (state.has("Ice Beam", player) and (state.has_any({"Power Grip", "Hi-Jump", "Bomb"}, player)))
                     )
        ),
        "Norfair Space Boost Super Missile": lambda state: (  # TODO may need to rename, and double check this later
                logic.mzm_norfair_to_save_behind_hijump(state, player)
                and logic.mzm_has_super_missiles(state, player)
                and (state.has("Speed Booster", player)
                     or (logic.mzm_can_bomb_block(state, player)
                         or (state.has_all({"Long Beam", "Wave Beam"}, player))
                         and (state.has("Power Grip", player)
                              or (logic.mzm_can_gravity_suit(state, player) and state.has("Hi-Jump", player)))
                         )
                     )
                and (logic.mzm_can_hj_sj_ibj_or_grip(state, player) or logic.mzm_can_walljump(state, player))
                and (logic.mzm_can_ibj(state, player) or logic.mzm_can_space_jump(state, player)
                     or state.has_all({"Ice Beam", "Hi-Jump"}, player)
                     or (logic.mzm_can_gravity_suit(state, player) and logic.mzm_can_walljump(state, player)
                         and state.has("Hi-Jump", player)))
        ),
        "Norfair Ice Beam": lambda state: (logic.mzm_norfair_upper_right_shaft(state, player)),
        "Norfair Heated Room above Ice Beam": lambda state: (
                logic.mzm_norfair_upper_right_shaft(state, player)
                and (logic.mzm_can_traverse_heat(state, player) or logic.mzm_hellrun(state, player, 1))
        ),
        "Norfair Hi-Jump":
            lambda state: logic.mzm_norfair_lower_right_shaft(state, player) and logic.mzm_has_missiles(state, player),
        "Norfair Big Room": lambda state: (  # there's also a way to do this with hi-jump, grip, a walljump, and a jump extend
                state.has("Speed Booster", player)
                or (logic.mzm_norfair_right_shaft_access(state, player)
                    and (logic.mzm_can_ibj(state, player)
                         or logic.mzm_can_space_jump(state, player)
                         or (state.has("Ice Beam", player)
                             and (state.has_any({"Hi-Jump", "Power Grip"}, player)
                                  or logic.mzm_can_walljump(state, player))
                             )
                         )
                    )
        ),
        "Norfair Behind Top Chozo Statue": lambda state: logic.mzm_norfair_behind_ice_beam(state, player),
        "Norfair Larva Ceiling E-tank": lambda state: (
                logic.mzm_norfair_to_save_behind_hijump(state, player)
                and logic.mzm_has_missile_count(state, player, 4)
                and state.has_all({"Wave Beam", "Speed Booster"}, player)
        ),
        "Norfair Right Shaft Lower": lambda state: (
                logic.mzm_norfair_lower_right_shaft(state, player)
                and (logic.mzm_can_ibj(state, player)
                     or (state.has("Power Grip", player)
                         and (logic.mzm_can_hi_jump(state, player) or logic.mzm_can_walljump(state, player))))
        ),
        "Norfair Right Shaft Bottom": lambda state: (
                logic.mzm_norfair_bottom_right_shaft(state, player)
                and (logic.mzm_can_hj_sj_ibj_or_grip(state, player) or logic.mzm_can_walljump(state, player)
                     or state.has("Ice Beam", player))
        )
    }

    ridley_access_rules = {
        "Ridley Southwest Puzzle Top": lambda state: (
                (logic.mzm_ridley_longway_right_shaft_access(state, player)
                 or logic.mzm_ridley_shortcut_right_shaft_access(state, player))
                and state.has("Speed Booster", player)
                and (state.has("Power Grip", player) or logic.mzm_can_space_jump(state, player))
                and (state.has("Power Grip", player) or logic.mzm_has_power_bombs(state, player)
                     or state.has_all({"Long Beam", "Wave Beam"}, player))
                and (logic.mzm_has_missile_count(state, player, 5)
                     and (logic.mzm_can_walljump(state, player) or logic.mzm_can_space_jump(state, player)
                          or logic.mzm_can_space_jump(state, player) or state.has("Power Grip"), player))
        ),
        "Ridley Southwest Puzzle Bottom": lambda state: (
                (logic.mzm_ridley_longway_right_shaft_access(state, player)
                 or logic.mzm_ridley_shortcut_right_shaft_access(state, player))
                and state.has("Speed Booster", player)
                and (state.has("Power Grip", player) or logic.mzm_can_space_jump(state, player))
                and (state.has("Power Grip", player) or logic.mzm_has_power_bombs(state, player)
                     or state.has_all({"Long Beam", "Wave Beam"}, player))
        ),
        "Ridley West Pillar":
            lambda state: logic.mzm_ridley_longway_right_shaft_access(state, player),
        "Ridley E-Tank behind Gravity":
            lambda state: state.can_reach("Ridley Gravity Suit/Unknown Item 3", "Location", player),
        "Ridley Gravity Suit/Unknown Item 3": lambda state: (
                logic.mzm_ridley_central_access(state, player)
                and logic.mzm_has_missile_count(state, player, 40)
                and (state.count("Energy Tank", player) >= 3)
                and ((state.has("Ice Beam", player) and state.has_any({"Hi-Jump", "Power Grip"}, player))
                     or logic.mzm_can_ibj(state, player) or logic.mzm_can_space_jump(state, player))),
        "Ridley Fake Floor E-Tank":
            lambda state: (logic.mzm_ridley_left_shaft_access(state, player)
                           and (logic.mzm_can_hj_sj_ibj_or_grip(state, player) or logic.mzm_can_walljump(state, player))
                           and logic.mzm_can_bomb_block(state, player)),
        "Ridley Upper Ball Cannon Puzzle": lambda state: (
                logic.mzm_ridley_central_access(state, player)
                and logic.mzm_can_ballcannon(state, player)
                and ((logic.mzm_can_walljump(state, player) and state.has("Power Grip", player))
                     or state.has("Hi-Jump", player) or logic.mzm_can_ibj(state, player))
        ),
        "Ridley Lower Ball Cannon Puzzle": lambda state: (
                logic.mzm_ridley_central_access(state, player)
                and logic.mzm_can_ballcannon(state, player)
                and (state.has_any({"Hi-Jump", "Bomb"}, player) or logic.mzm_can_walljump(state, player)
                     or logic.mzm_can_space_jump(state, player))
        ),
        "Ridley Imago Super Missile": lambda state: (
                (logic.mzm_can_hj_sj_ibj_or_grip(state, player) or logic.mzm_can_walljump(state, player))
                and (logic.mzm_has_missile_count(state, player, 20) or state.has("Charge Beam", player))
        ),
        "Ridley After Sidehopper Hall Upper": lambda state: logic.mzm_ridley_central_access(state, player),
        "Ridley After Sidehopper Hall Lower": lambda state: logic.mzm_ridley_central_access(state, player),
        "Ridley Long Hall": lambda state: (
                logic.mzm_ridley_longway_right_shaft_access(state, player)
                or logic.mzm_ridley_shortcut_right_shaft_access(state, player)
        ),
        "Ridley Center Pillar Missile": lambda state: logic.mzm_ridley_central_access(state, player),
        "Ridley Ball Room Missile": lambda state: logic.mzm_ridley_central_access(state, player),
        "Ridley Ball Room Super": lambda state: (
                logic.mzm_ridley_central_access(state, player) and logic.mzm_has_super_missiles(state, player)
                and (logic.mzm_can_ibj(state, player) or logic.mzm_can_walljump(state, player)
                     or logic.mzm_can_space_jump(state, player) or state.has_all({"Hi-Jump", "Power Grip"}, player))
        ),
        "Ridley Fake Lava Missile": lambda state: (
                logic.mzm_ridley_central_access(state, player)
                and (state.has("Wave Beam", player) or logic.mzm_can_bomb_block(state, player))
                and logic.mzm_can_ibj(state, player) or state.has("Power Grip", player)),
        "Ridley Owl E-Tank": lambda state: logic.mzm_ridley_central_access(state, player),
        "Ridley Northeast Corner Missile": lambda state: (
                logic.mzm_has_missiles(state, player)
                and (logic.mzm_can_ibj(state, player)
                     or (state.has("Power Grip", player) and logic.mzm_has_power_bombs(state, player)
                         and state.has_any({"Ice Beam", "Hi-Jump"}, player)))
                and (logic.mzm_can_bomb_block(state, player) or state.has("Screw Attack", player))
        ),
        "Ridley Bomb Puzzle": lambda state: (
                (logic.mzm_ridley_longway_right_shaft_access(state, player)
                 or logic.mzm_ridley_shortcut_right_shaft_access(state, player))
                and state.has_all({"Speed Booster", "Bomb", "Power Grip"}, player)
        ),
        "Ridley Speed Jump": lambda state: (
                (logic.mzm_ridley_longway_right_shaft_access(state, player)
                 or logic.mzm_ridley_shortcut_right_shaft_access(state, player))
                and state.has_all({"Wave Beam", "Speed Booster"}, player)
        ),
        "Ridley Defeated": lambda state: state.can_reach("Ridley Gravity Suit/Unknown Item 3", "Location", player)
    }

    tourian_access_rules = {
        "Tourian Left of Mother Brain": lambda state: (
                state.has_all({"EVENT_CHOZO_GHOST_DEFEATED", "Speed Booster"}, player)
                and logic.mzm_can_space_jump(state, player)),
        "Tourian Under Mother Brain ": lambda state: (state.has("EVENT_MOTHER_BRAIN_DEFEATED", player)
                                                      and logic.mzm_has_super_missiles(state, player)),
        "Mother Brain Defeated": lambda state: (
                state.has("Ice Beam", player)
                and (logic.mzm_can_space_jump(state, player) or logic.mzm_can_ibj(state, player)
                     or state.has_all({"Hi-Jump", "Power Grip", "Speed Booster"}, player))
                and logic.mzm_can_bomb_block(state, player)
                and logic.mzm_has_missile_count(state, player, 40)
                and (state.count("Energy Tank", player) >= 4)
        )
    }

    crateria_access_rules = {
        "Crateria Landing Site Ballspark": lambda state: (logic.mzm_has_power_bombs(state, player)
                                                          and logic.mzm_can_ballspark(state, player)),
        "Crateria Power Grip": lambda state: (
                state.has_any({"Bomb", "Hi-Jump"}, player) and logic.mzm_can_hj_sj_ibj_or_grip(state, player)),
        "Crateria Statue Water":
            lambda state: state.can_reach("Crateria Plasma Beam/Unknown Item 1", "Location", player),
        "Crateria Plasma Beam/Unknown Item 1": lambda state: state.has_any({"Bomb", "Hi-Jump"}, player),
        "Crateria East Ballspark": lambda state: (
                logic.mzm_can_ballspark(state, player)
                and (logic.mzm_can_space_jump(state, player) or logic.mzm_can_walljump(state, player))
        ),
        "Crateria Northeast Corner": lambda state: (
                state.has("Speed Booster", player)
                and (logic.mzm_can_space_jump(state, player) or logic.mzm_can_walljump(state, player)
                     or logic.mzm_can_tricky_sparks(state, player))
        )
    }

    chozodia_access_rules = {
        "Chozodia Upper Crateria Door": lambda state: (
                logic.mzm_has_missiles(state, player)
                and (logic.mzm_can_walljump(state, player) or logic.mzm_can_ibj(state, player)
                     or logic.mzm_can_space_jump(state, player))
        ),
        "Chozodia Bomb Maze": lambda state: (
                (logic.mzm_can_ibj(state, player) or logic.mzm_can_ballspark(state, player)
                 or (state.has("Power Grip", player)
                     and (logic.mzm_can_walljump(state, player) or logic.mzm_can_space_jump(state, player))))
                and (state.has("Bomb", player) or state.count("Power Bomb Tank", player) >= 3)
                and (state.has("Bomb", player) or state.has("Hi-Jump", player))
                and (state.has("Hi-Jump", player) or logic.mzm_can_ibj(state, player)
                     or (state.has("Power Grip", player) and logic.mzm_can_walljump(state, player)))
        ),
        "Chozodia Zoomer Maze": lambda state: (
                (logic.mzm_can_ibj(state, player) or logic.mzm_can_ballspark(state, player)
                 or (state.has("Power Grip", player)
                     and (logic.mzm_can_walljump(state, player) or logic.mzm_can_space_jump(state, player))))
                and (logic.mzm_can_ibj(state, player)
                     or (state.has("Hi-Jump", player) and state.has_any({"Speed Booster", "Power Grip"}, player)))
        ),
        "Chozodia Ruins Near Upper Crateria Door": lambda state: (
                logic.mzm_has_missiles(state, player)
                and (logic.mzm_can_walljump(state, player) or logic.mzm_can_ibj(state, player)
                     or logic.mzm_can_space_jump(state, player))
                and state.has("Power Bomb Tank", player)
        ),
        "Chozodia Chozo Ghost Area Morph Tunnel Above Water": lambda state: ( # The room leading to this item is inaccessible until the Chozo Ghost is defeated
                state.has("EVENT_CHOZO_GHOST_DEFEATED", player) and state.has_any({"Hi-Jump", "Bomb"}, player)
        ),
        "Chozodia Chozo Ghost Area Underwater": lambda state: ( # This item does not really exist until the Chozo Ghost is defeated
                state.has("EVENT_CHOZO_GHOST_DEFEATED", player)
                and logic.mzm_can_gravity_suit(state, player) and state.has("Speed Booster", player)
        ),
        "Chozodia Under Chozo Ghost Area Water": lambda state: (
                logic.mzm_chozodia_ghost_from_upper_crateria_door(state, player)
                or state.has("EVENT_MOTHER_BRAIN_DEFEATED", player)),
        "Chozodia Glass Tube E-Tank": lambda state: (
                (logic.mzm_can_ibj(state, player) or logic.mzm_can_ballspark(state, player)
                 or (state.has("Power Grip", player)
                     and (logic.mzm_can_walljump(state, player) or logic.mzm_can_space_jump(state, player))))
                and logic.mzm_has_missile_count(state, player, 6)
                and state.has("Speed Booster", player)
        ),
        "Chozodia Lava Super": lambda state: ( # This room is inaccessible until the Chozo Ghost is defeated
                state.has("EVENT_CHOZO_GHOST_DEFEATED", player)
                and ((logic.mzm_can_gravity_suit(state, player)
                      and ((state.has("Power Grip", player) and state.has_any({"Hi-Jump", "Bomb"}, player))
                           or logic.mzm_can_ibj(state, player)))
                     or (state.has_all({"Hi-Jump", "Power Grip"}, player)
                         and (state.has("Varia Suit", player)
                              or logic.mzm_hellrun(state, player, 6))))
                and (logic.mzm_can_walljump(state, player)
                     or (logic.mzm_can_gravity_suit(state, player)
                         and (logic.mzm_can_ibj(state, player) or logic.mzm_can_space_jump(state, player))))
        ),
        "Chozodia Original Power Bomb": lambda state: logic.mzm_chozodia_to_cockpit(state, player),
        "Chozodia Next to Original Power Bomb": lambda state: (
                logic.mzm_chozodia_to_cockpit(state, player)
                and state.has("Power Bomb Tank", player)
                and (logic.mzm_can_space_jump(state, player) or logic.mzm_can_ibj(state, player))
        ),
        "Chozodia Glass Tube Power Bomb": lambda state: logic.mzm_chozodia_glass_tube_from_crateria_door(state, player),
        "Chozodia Chozo Ghost Area Long Shinespark": lambda state: ( # The room leading to this item is inaccessible until the Chozo Ghost is defeated
                state.has_all({"EVENT_CHOZO_GHOST_DEFEATED", "Speed Booster"}, player)
                and logic.mzm_can_gravity_suit(state, player)
        ),
        "Chozodia Shortcut Super": lambda state: (  # you can also do this with screw and not need ibj/wj/sj but that's for advanced logic later
                (logic.mzm_chozodia_tube_to_mothership_central(state, player)
                 or state.has("Chozo Ghost Defeated", player))
                and state.has_any({"Super Missile Tank", "Power Bomb Tank"}, player)
                and (logic.mzm_can_ibj(state, player) or logic.mzm_can_walljump(state, player)
                     or logic.mzm_can_space_jump(state, player))
        ),
        "Chozodia Workbot Super": lambda state: (
                (logic.mzm_chozodia_tube_to_mothership_central(state, player)
                 or state.has("Chozo Ghost Defeated", player))
                and logic.mzm_has_missile_count(state, player, 5)
        ),
        "Chozodia Mothership Ceiling Near ZSS Start":
            lambda state: logic.mzm_chozodia_tube_to_mothership_central(state, player)
                          or state.has_all({"Chozo Ghost Defeated", "Power Bomb"}, player),
        "Chozodia Under Mecha Ridley Hallway": lambda state: (  # you can also get here without PBs but we'll save that for advanced logic later
                logic.mzm_chozodia_to_cockpit(state, player)
                and (state.has("Power Grip", player) or logic.mzm_can_ibj(state, player))
                and state.has_all({"Power Bomb Tank", "Speed Booster"}, player)
        ),
        "Chozodia Southeast Corner In Hull":
            lambda state: logic.mzm_chozodia_tube_to_mothership_central(state, player)
                          or state.has_all({"Chozo Ghost Defeated", "Power Bomb"}, player),
        "Chozo Ghost Defeated": lambda state: state.can_reach("Mother Brain Defeated", "Location", player),
        "Chozodia Space Pirate's Ship": lambda state: (
                logic.mzm_chozodia_to_cockpit(state, player)
                and logic.mzm_has_missile_count(state, player, 40)
                and state.has_all({"Power Bomb Tank", "Plasma Beam"}, player)
        )
    }

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
