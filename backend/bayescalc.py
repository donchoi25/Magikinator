TOTAL_CARDS_NUMBER = 28580

class BayesCalc():
    def __init__(self, cards_data):
        self.cards_data = cards_data
        return
    def calculateAllCardProbabilities(self, questions_so_far, answers_so_far):
        probabilities = []


