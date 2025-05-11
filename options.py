"""
Option definitions for Metroid: Zero Mission
"""

from schema import And, Schema
from dataclasses import dataclass

from Options import (
    Choice, DeathLink, DefaultOnToggle, OptionDict, OptionGroup, OptionSet, StartInventoryPool, Toggle,
    PerGameCommonOptions, Removed, Visibility
)

from . import rom_data


PIXEL_SIZE = 4


class Goal(Choice):
    """
    What you will be required to do to beat the game.
    Mecha Ridley: Mecha Ridley is always open and can be reached as long as you have the right items.
    Bosses: The door to Mecha Ridley is locked until Kraid, Ridley, Mother Brain, and the Chozo Ghost are defeated.
    """
    display_name = "Goal"
    option_mecha_ridley = 0
    option_bosses = 1
    default = option_bosses


# TODO: test Hard mode logic more
class GameDifficulty(Choice):
    """
    Which in-game difficulty you will play on.
    Normal: Easy and Normal will be available, and Hard will not.
    Hard: Hard will be the only available difficulty.
    Either: All difficulty options will be available.
    Hard has a small effect on logic due to enemy placements. If Either is selected, logic will not require any tricks
    that can't be done on all three difficulties. Either also forces logic to assume Hard Mode tank amounts, which may
    slightly influence item placements.
    """
    display_name = "Game Difficulty"
    option_normal = 1
    option_hard = 2
    option_either = 3
    default = option_either


class ChozodiaAccess(Choice):
    """
    Open: You can access Chozodia at any time by using a Power Bomb to open the doors.
    Closed: You must defeat Mother Brain to access Chozodia.
    """
    display_name = "Chozodia Access"
    option_open = 0
    option_closed = 1
    default = option_open


class UnknownItemsAlwaysUsable(Removed):
    """
    This option has been replaced with Fully Powered Suit.
    """
    display_name = "Unknown Items Always Usable"


class FullyPoweredSuit(Choice):
    """
    How to handle the activation of the unknown items (Plasma Beam, Space Jump, and Gravity Suit).

    Ruins Test: Defeat the Chozo Ruins Test in Chozodia as ZSS to gain the Fully Powered Suit and activate the unknown items, as in the unmodified game
    Shuffled: The Fully Powered Suit is shuffled into the item pool, and the Ruins Test awards a random item
    Start With: Unknown items are activated and usable as soon as they are received, and the Ruins Test awards a random item
    Legacy Always Usable: Unknown items are activated and usable as soon as they are received, and the Ruins Test doesn't have a reward
    """
    display_name = "Fully Powered Suit"
    option_ruins_test = 0
    option_shuffled = 1
    option_start_with = 2
    option_legacy_always_usable = 3
    default = option_start_with

    def use_alt_unknown_sprites(self):
        return self.value <= self.option_shuffled

    def to_slot_data(self):
        return self.option_start_with if self.value == self.option_legacy_always_usable else self.value


class SkipChozodiaStealth(DefaultOnToggle):
    """After escaping Tourian, place Samus in the save room just outside of the Chozo Ghost's room in Chozodia."""
    display_name = "Skip Chozodia Stealth"


class StartWithMaps(DefaultOnToggle):
    """Start the game with all map stations visited."""
    display_name = "Start with Maps"


class BuffPowerBombDrops(Toggle):
    """Make Power Bombs drop from enemies twice as often and give 2 units of ammo."""
    display_name = "Buff Power Bomb Drops"


class PlasmaBeamHint(DefaultOnToggle):
    """Display a hint for the location of the Plasma Beam when you defeat Mother Brain."""
    display_name = "Plasma Beam Hint"


class LogicDifficulty(Choice):
    """
    Determines the difficulty of room traversal and game knowledge required by the game's logic.
    Simple: For beginners to Zero Mission randomizer. Should be comfortable to anyone who has beaten the game. Includes
    mostly routes similar to vanilla or otherwise intuitive to players that have not sequence broken the game.
    Normal: For players with more familiarity with the game. Should be comfortable to anyone who has sequence broken or
    skipped items. Includes developer-intended sequence breaks, unintuitive paths, and some tricks.
    Advanced: For experts who want all their skills challenged. Should be comfortable to MZM Randomizer veterans and
    speedrunners. Includes all tricks, very difficult shinespark chains, crumble jumps, Acid Worm Skip, etc.

    This setting does not affect the difficulty of non-suited runs through heated rooms or acid/lava.
    Specific tricks can be included or excluded in other options.
    """
    display_name = "Logic Difficulty"
    option_simple = 0
    option_normal = 1
    option_advanced = 2


class CombatLogicDifficulty(Choice):
    """
    Determines the difficulty of combat required by the game's logic.
    Relaxed: Requires the player have an ample amount of resources to defeat bosses and traverse areas. Should be
    comfortable to anyone who has beaten the game. Bosses will not be a problem.
    Normal: Requires the player have enough resources to defeat bosses and traverse areas with some wiggle room.
    Bosses may be somewhat challenging.
    Minimal: Requires only the minimum amount of resources to complete the game. You may have to fight bosses like in
    a low% run or find progression items deep in late-game areas with low energy.
    """
    display_name = "Combat Logic Difficulty"
    option_relaxed = 0
    option_normal = 1
    option_minimal = 2


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


# TODO: split into none/comfortable/minimal
class HazardRuns(Toggle):
    """
    Allows for traversing heated rooms and acid/lava dives without the appropriate suit(s) in logic.

    When enabled, logic will ensure you have a reasonable amount of energy before requiring an environmental damage
    run. When disabled, you will not be required to endure any environmental damage before receiving the appropriate
    mitigating suit.
    """
    display_name = "Hazard Runs"


class WallJumps(Choice):
    """
    Determines how wall jumping will be handled:
    - Disabled: Wall jumping will not be possible. All locations can still be reached through other means.
    - Unlockable: A Wall Jump item will be placed into the item pool. Once found, you will be able to wall jump.
    - Enabled, Not Logical: Wall jumping will always be possible, but it will never be required to access any locations.
    - Enabled: Wall jumping will always be possible, and logic may expect using wall jumps to progress where applicable.
    """
    display_name = "Wall Jumps"
    option_disabled = 0
    option_unlockable = 1
    option_enabled_not_logical = 2
    option_enabled = 3
    default = option_enabled


class SpringBall(Toggle):
    """
    Remove Spring Ball functionality from Hi-Jump and shuffle it into the item pool as a separate item.
    """
    display_name = "Spring Ball"


# TODO: turn into a general trick include/exclude option
class TrickyShinesparks(Toggle):
    """
    If enabled, logic will include long, difficult, and/or unintuitive Shinesparks as valid methods of collecting
    items or traversing areas that normally would not require an advanced Shinespark to collect.

    This has no effect on long Shinespark puzzles which are the intended way of collecting an item, such as the long
    Shinespark chain in Chozodia near the Chozo Ghost room.
    """
    display_name = "Tricky Shinesparks"


class LayoutPatches(Choice):
    """
    Slightly modify the layout of some rooms to reduce softlocks.
    NOTE: You can warp to the starting room from any save station or Samus' ship by holding L+R while selecting "No"
    when asked to save.
    """
    display_name = "Layout Patches"
    option_false = 0
    option_true = 1
    option_choice = 2
    default = option_true


class SelectedPatches(OptionSet):
    """
    If Layout Patches is set to Choice, list of layout patches to apply.
    The names of valid layout patches can be found in the compatible_patches and
    expansion_required_patches lists in rom_data here:
    https://github.com/lilDavid/Archipelago-Metroid-Zero-Mission/blob/main/rom_data.py#L486
    Descriptions can be found in the apply_layout_patches function below that.
    """
    display_name = "Selected Layout Patches"
    valid_keys = rom_data.layout_patches


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


class FastItemBanners(DefaultOnToggle):
    """
    Makes the banner that appears when you collect an item much quicker, and makes it play a sound
    related to the item when it appears.
    """
    display_name = "Fast Item Banners"
    visibility = Visibility.none  # This option has no effect, but may be restored in the future


class SkipTourianOpeningCutscenes(DefaultOnToggle):
    """
    Skip the cutscenes that show the Tourian statue's eyes lighting up when you defeat Ridley and Kraid, as well as the
    animation of the statue's mouths opening.
    """
    display_name = "Skip Tourian Opening Sequence"


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


class ElevatorSpeed(Choice):
    """
    Speed up elevators.

    Fast: Double the vanilla speed
    Way Too Fast: Triple the vanilla speed
    """
    display_name = "Elevator Speed"
    option_vanilla = PIXEL_SIZE * 2
    option_fast = option_vanilla * 2
    option_way_too_fast = option_vanilla * 3
    default = option_fast


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


class RemoteItems(DefaultOnToggle):
    """
    Indicates you get items sent from your own world, allowing co-op play of a world.
    When enabled, you will not lose the items you've collected from your own world if you reset or game-over.

    Regardless of this setting, you can still play a single-player game without connecting to a server.
    However, you will not benefit from your items being returned to you when you reload a save.
    """
    display_name = "Remote Items"


mzm_option_groups = [
    OptionGroup("World", [
        ChozodiaAccess,
        UnknownItemsAlwaysUsable,
        LayoutPatches,
        SelectedPatches,
    ]),
    OptionGroup("Item Pool", [
        MorphBallPlacement,
        FullyPoweredSuit,
        WallJumps,
        SpringBall,
        JunkFillWeights,
    ]),
    OptionGroup("Logic", [
        LogicDifficulty,
        CombatLogicDifficulty,
        IBJInLogic,
        HazardRuns,
        TrickyShinesparks
    ]),
    OptionGroup("Quality of Life", [
        SkipChozodiaStealth,
        BuffPowerBombDrops,
        PlasmaBeamHint,
        ElevatorSpeed,
        StartWithMaps,
        FastItemBanners,
        SkipTourianOpeningCutscenes,
    ]),
    OptionGroup("Cosmetic", [
        DisplayNonLocalItems,
    ]),
]


@dataclass
class MZMOptions(PerGameCommonOptions):
    goal: Goal
    game_difficulty: GameDifficulty
    remote_items: RemoteItems
    death_link: DeathLink
    chozodia_access: ChozodiaAccess
    unknown_items_always_usable: UnknownItemsAlwaysUsable
    layout_patches: LayoutPatches
    selected_patches: SelectedPatches
    morph_ball: MorphBallPlacement
    fully_powered_suit: FullyPoweredSuit
    spring_ball: SpringBall
    junk_fill_weights: JunkFillWeights
    logic_difficulty: LogicDifficulty
    combat_logic_difficulty: CombatLogicDifficulty
    ibj_in_logic: IBJInLogic
    hazard_runs: HazardRuns
    walljumps: WallJumps
    tricky_shinesparks: TrickyShinesparks
    skip_chozodia_stealth: SkipChozodiaStealth
    buff_pb_drops: BuffPowerBombDrops
    plasma_beam_hint: PlasmaBeamHint
    elevator_speed: ElevatorSpeed
    start_with_maps: StartWithMaps
    fast_item_banners: FastItemBanners
    skip_tourian_opening_cutscenes: SkipTourianOpeningCutscenes
    display_nonlocal_items: DisplayNonLocalItems
    start_inventory_from_pool: StartInventoryPool
