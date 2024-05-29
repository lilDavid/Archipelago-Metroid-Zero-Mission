"""
Option definitions for Metroid: Zero Mission
"""
from Options import DeathLink, DefaultOnToggle, Toggle, PerGameCommonOptions
from dataclasses import dataclass

"""
- copy options from MZMR, add others such as disable IBJs/progressive bombs (so you eventually can),
  power bomb jumping, and probably add some others as decided on by input in game-suggestions.
  might need some tweaks to vanilla/some tricks/everything "difficulties"
- for starters i'm just going to stick to Unknowns activation, a simple one-byte change.
- next one to add would be forcing vanilla Morph, which should be the default. however, it is useful to
  leave out for now for testing generation.
"""


class UnknownItemsAlwaysUsable(DefaultOnToggle):
    """
    Unknown Items (Plasma Beam, Space Jump, and Gravity Suit) are activated and usable as soon as
    they are received.

    When this option is disabled, the player will need to defeat the Chozo Ghost in Chozodia in order
    to unlock Samus' fully-powered suit, after which they may then use the Plasma Beam, Space Jump,
    and Gravity Suit, as in vanilla.
    """
    display_name = "UnknownItemsAlwaysUsable"


@dataclass
class MZMOptions(PerGameCommonOptions):
    unknown_items_always_usable: UnknownItemsAlwaysUsable
    death_link: DeathLink
