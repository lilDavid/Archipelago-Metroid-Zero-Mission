"""
Option definitions for Metroid: Zero Mission
"""

from schema import And, Schema
from dataclasses import dataclass

from Options import (
    Choice, DeathLink, DefaultOnToggle, OptionDict, OptionGroup, StartInventoryPool, Toggle,
    PerGameCommonOptions, Visibility
)


class ChozodiaAccess(Choice):
    """
    Open: You can access Chozodia at any time by using a Power Bomb to open the doors.
    Closed: You must defeat Mother Brain to access Chozodia.
    """
    display_name = "Chozodia Access"
    option_open = 0
    option_closed = 1
    default = option_open


class UnknownItemsAlwaysUsable(DefaultOnToggle):
    """
    Unknown Items (Plasma Beam, Space Jump, and Gravity Suit) are activated and usable as soon as
    they are received.

    When this option is disabled, the player will need to defeat the Chozo Ghost in Chozodia as ZSS in order
    to unlock Samus' fully-powered suit, after which they may then use the Plasma Beam, Space Jump,
    and Gravity Suit, as in the unmodified game.
    """
    display_name = "Unknown Items Always Usable"


class SkipChozodiaStealth(DefaultOnToggle):
    """After escaping Tourian, place Samus in the save room just outside of the Chozo Ghost's room in Chozodia."""
    display_name = "Skip Chozodia Stealth"


class LogicDifficulty(Choice):
    """
    Determines the general difficulty of the game's logic. On advanced difficulty, more niche techniques and game
    knowledge may be required to collect items or progress, and you may be required to complete areas or bosses
    with fewer resources. Examples of "tricks" this may put in logic include entering invisible tunnels, jump extends,
    and Acid Worm skip.

    Other specific tricks (such as difficult Shinesparks and horizontal IBJ) have individual difficulty settings that
    this does not affect.
    """
    display_name = "Logic Difficulty"
    option_normal = 0
    option_advanced = 1


class IBJInLogic(Choice):
    """
    Allows for using IBJ (infinite bomb jumping) in logic.

    Enabling this option may require you to traverse long vertical and/or horizontal distances using only bombs.

    If disabled, this option does not disable performing IBJ, but it will never be logically required.
    """
    display_name = "IBJ In Logic"
    option_none = 0
    option_vertical_only = 1
    option_horizontal_and_vertical = 2


# TODO: split into none/simple/advanced
class HeatRunsAndLavaDives(Toggle):
    """
    Allows for traversing heated rooms and acid/lava dives without the appropriate suit(s) in logic.

    When enabled, logic will ensure you have a reasonable amount of energy before requiring an environmental damage
    run. When disabled, you will not be required to endure any environmental damage before receiving the appropriate
    mitigating suit.
    """
    display_name = "Heat Runs/Lava Dives"


class WalljumpsInLogic(DefaultOnToggle):
    """
    Allows for using walljumps in logic. You may be required to walljump instead of using items such as Hi-Jump or
    Power Grip in order to logically progress, where possible.

    Disabling this option will not remove the ability to walljump, but it will never be logically required.
    """
    display_name = "Wall Jumps In Logic"


class TrickyShinesparks(Toggle):
    """
    If enabled, logic will include long, difficult, and/or unintuitive Shinesparks as valid methods of collecting
    items or traversing areas that normally would not require an advanced Shinespark to collect.

    This has no effect on long Shinespark puzzles which are the intended way of collecting an item, such as the long
    Shinespark chain in Chozodia near the Chozo Ghost room.
    """
    display_name = "Tricky Shinesparks"


class LayoutPatches(DefaultOnToggle):
    """
    Slightly modify the layout of some rooms to reduce softlocks.
    NOTE: You can warp to the starting room from any save station or Samus' ship by holding L+R while selecting "No"
    when asked to save.
    """
    display_name = "Layout Patches"


class MorphBallPlacement(Choice):
    """
    Influences where the Morph Ball will be placed.
    Normal: Shuffled into the pool with no special treatment.
    Early: Forced to be local in an early location.
    """
    display_name = "Morph Ball Placement"
    option_normal = 0
    option_early = 1
    default = option_early


class DisplayNonLocalItems(Choice):
    """
    How to display items that will be sent to other players.

    Match Series: Items from Super Metroid and SMZ3 display as their counterpart in Zero Mission.
    Match Game: Items for other Zero Mission worlds appear as the item that will be sent.
    None: All items for other players appear as Archipelago logos.
    """
    display_name = "Display Other Players' Items"
    option_none = 0
    option_match_game = 1
    option_match_series = 2
    default = option_match_series


class JunkFillWeights(OptionDict):
    """
    Specify the distribution of extra capacity expansions that should be used to fill vacancies in the pool.
    This option only has any effect if there are unfilled locations, e.g. when some items are removed.
    """
    display_name = "Junk Fill Weights"
    visibility = Visibility.template | Visibility.complex_ui | Visibility.spoiler
    schema = Schema({item_name: And(int, lambda n: n >= 0) for item_name in (
        "Missile Tank", "Super Missile Tank", "Power Bomb Tank", "Nothing"
    )})
    default = {
        "Missile Tank": 1,
        "Super Missile Tank": 0,
        "Power Bomb Tank": 0,
        "Nothing": 0,
    }


mzm_option_groups = [
    OptionGroup("World", [
        ChozodiaAccess,
        SkipChozodiaStealth,
        UnknownItemsAlwaysUsable,
        LayoutPatches,
        MorphBallPlacement,  # TODO: Shuffle settings group?
    ]),
    OptionGroup("Logic", [
        LogicDifficulty,
        IBJInLogic,
        HeatRunsAndLavaDives,
        WalljumpsInLogic,
        TrickyShinesparks
    ]),
    OptionGroup("Cosmetic", [
        DisplayNonLocalItems,
    ]),
    OptionGroup("Item & Location Options", [
        JunkFillWeights,
    ]),
]


@dataclass
class MZMOptions(PerGameCommonOptions):
    death_link: DeathLink
    chozodia_access: ChozodiaAccess
    skip_chozodia_stealth: SkipChozodiaStealth
    unknown_items_always_usable: UnknownItemsAlwaysUsable
    layout_patches: LayoutPatches
    morph_ball: MorphBallPlacement
    logic_difficulty: LogicDifficulty
    ibj_in_logic: IBJInLogic
    heatruns_lavadives: HeatRunsAndLavaDives
    walljumps_in_logic: WalljumpsInLogic
    tricky_shinesparks: TrickyShinesparks
    display_nonlocal_items: DisplayNonLocalItems
    start_inventory_from_pool: StartInventoryPool
    junk_fill_weights: JunkFillWeights
