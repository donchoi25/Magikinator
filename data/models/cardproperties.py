from enum import Enum

#TODO: We'll need to actually generate these card properties from the range of possible answers per column

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

# # Possible CMC values
# class CMC(Enum):
#     "1": 1
#     2: 2
#     3: 3
#     4: 4
#     5: 5
#     6: 6
#     7: 7
#     8: 8
#     9: 9
#     10: 10
#     11: 11
#     12: 12
#     13: 13
#     14: 14
#     15: 15
#     16: 16
#     1000000: 1000000
