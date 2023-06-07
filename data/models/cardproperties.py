from enum import Enum

class Colors(Enum):
    WHITE = "W"
    BLUE = "U"
    BLACK = "B"
    RED = "R"
    GREEN = "G"

# Types pulled from MTG Wiki
class CardTypes(Enum):
    ARTIFACT = "artifact"
    BATTLE = "battle"
    CONSPIRACY = "conspiracy"
    CREATURE = "creature"
    DUNGEON = "dungeon"
    ENCHANTMENT = "enchantment"
    INSTANT = "instant"
    LAND = "land"
    PHENOMENON = "phenomenon"
    PLANE = "plane"
    PLANESWALKER = "planeswalker"
    SCHEME = "scheme"
    SORCERY = "sorcery"
    TRIBAL = "tribal"
    VANGUARD = "vanguard"
