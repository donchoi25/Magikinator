from enum import Enum

class Validator():
    def __init__(self):
        return
    
    def validate(self, card, expected_value):
        return False

"""
Default Validator, always returns FALSE
"""
class DefaultValidator(Validator):
    def validate(self, card, expected_value):
        return False

"""
Does the card have color identity value?
"""
class ColorValidator(Validator):
    def validate(self, card, expected_value):
        return str(expected_value.value[0]) in card.colors

"""
Does the card of card type X?
"""
class CardTypeValidator(Validator):
    def validate(self, card, expected_value):
        return expected_value.value in str(card.type_line.lower())

