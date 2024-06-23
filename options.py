from schema import And, Schema

"""
Option definitions for Metroid: Zero Mission
"""
from Options import Choice, DeathLink, DefaultOnToggle, OptionDict, StartInventoryPool, Toggle, PerGameCommonOptions, Visibility
from dataclasses import dataclass


class UnknownItemsAlwaysUsable(DefaultOnToggle):
    """
    Unknown Items (Plasma Beam, Space Jump, and Gravity Suit) are activated and usable as soon as
    they are received.

    When this option is disabled, the player will need to defeat the Chozo Ghost in Chozodia in order
    to unlock Samus' fully-powered suit, after which they may then use the Plasma Beam, Space Jump,
    and Gravity Suit, as in the original game.
    """
    display_name = "Unknown Items Always Usable"


class SkipChozodiaStealth(DefaultOnToggle):
    """When escaping Tourian, place Samus in the save room just outside of the Chozo Ghost's room in Chozodia."""
    display_name = "Skip Chozodia Stealth"

class IBJInLogic(Toggle):
    """
    Allows for using IBJ (infinite bomb jumping) in logic.

    This option may require you to traverse long vertical or horizontal distances using only bombs.

    If disabled, this option does not disable performing IBJ, but it will never be logically required.
    """
    display_name = "IBJ In Logic"

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
    Allows for using walljumps in logic. As the game does not teach nor require walljumping to complete the game
    while acquiring all items, all items will be accessible using other means regardless of this setting.

    Disabling this option will not remove the ability to walljump, but it will never be logically required.
    """
    display_name = "Wall Jumps In Logic"

class DisplayNonLocalItems(Choice):
    """
    How to display items that will be sent to other players.

    Match Series: Items from Super Metroid and SMZ3 display as their counterpart in Zero Mission
    Match Game: Items for other Zero Mission worlds appear as the item that will be sent
    None: All items for other players appear as AP logos
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

@dataclass
class MZMOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    skip_chozodia_stealth: SkipChozodiaStealth
    unknown_items_always_usable: UnknownItemsAlwaysUsable
    ibj_in_logic: IBJInLogic
    heatruns_lavadives: HeatRunsAndLavaDives
    walljumps_in_logic: WalljumpsInLogic
    display_nonlocal_items: DisplayNonLocalItems
    death_link: DeathLink
    junk_fill_weights: JunkFillWeights
