from enum import Enum

class QuestionTypes(Enum):
    IS_COLOR = "color"
    IS_CMC = "cmc"
    IS_COLOR_IDENTITY = "color_identity"
    IS_CARD_TYPE = "card_type"
    IS_MANA_COST = "mana_cost"
    IS_CREATURE_TYPE = "creature_type"
    HAS_KEYWORDS = "keywords"