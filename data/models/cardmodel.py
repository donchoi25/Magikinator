class CardModel():
    def __init__(self, cardrow):
        for key, value in cardrow.items():
            setattr(self, key, str(value))
    """
    self.name, self.mana_cost, self.cmc, self.type_line,...
    """
    
