from globals.constants import TOTAL_CARDS_FINAL
from globals.constants import TOTALS_MAP_FINAL
import numpy as np

class BeyesTheoremCalc:
    def __init__(self):
        #cache that will store most recent Vector for calculating P_answers_given_card
        self.cache_P_answers_given_card = None
    #probVector will be a numpy array. This vector represents a column for a question, answer pair
    def calculateCardProb(self, numQuestionAns, questionans, probVector, cache=True):
        #It could be (# of times card was picked / total # of games)
        P_card = 1 / TOTAL_CARDS_FINAL
        
        #only look into cache if this is not the first question
        if numQuestionAns > 0:
            P_answers_given_card = self.cache_P_answers_given_card
        else:
            P_answers_given_card = 1
        #calculate for the new questions and answers
        P_answers_given_card = P_answers_given_card * probVector

        #save cacheable answers
        if cache:
            self.cache_P_answers_given_card = P_answers_given_card

        #Bayes Theorem simplified. No need to calculate Evidence
        P_character_given_answers = (P_answers_given_card * P_card)

        return P_character_given_answers

    #take the average for the answer with the current card excluded
    def calculate_answers_given_not_card(self, questionans, probVector):
        #Aggregate percentages from csv file
        numerator = np.full((len(probVector),), TOTALS_MAP_FINAL[questionans])

        #We subtract the value from the numerator
        numerator = numerator - probVector
        denominator = np.full((len(probVector),), TOTAL_CARDS_FINAL - 1)

        return numerator / denominator

BeyesCalcInst = BeyesTheoremCalc()