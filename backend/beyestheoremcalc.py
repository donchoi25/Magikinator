from globals.constants import cardcsv_dataframe, TOTAL_CARDS_FINAL, totals_map
import numpy as np

#how to get specific card:
    #cardcsv_dataframe.at["Swamp", question+"#YES"].values[0]

class BeyesTheoremCalc:
    def __init__(self):
        #cache that will store vectors for the following calculations:
            #P_answers_given_card
            #P_answers_given_not_card
        #key will be number of questions and answers we're at so far
        self.cache_P_answers_given_card = {}
        self.cache_P_answers_given_not_card = {}
    #probVector will be a numpy array. This vector represents a column for a question, answer pair
    def calculateCardProb(self, numQuestionAns, questionans, probVector, cache=True):
        P_card = 1 / TOTAL_CARDS_FINAL
        
        #only look into cache if this is not the first question
        if numQuestionAns > 0:
            P_answers_given_card = self.cache_P_answers_given_card[numQuestionAns]
            P_answers_given_not_card = self.cache_P_answers_given_not_card[numQuestionAns]
        else:
            #these will be numpy arrays
            P_answers_given_card = np.ones(len(probVector),)
            P_answers_given_not_card = np.ones(len(probVector),)
        #calculate for the new questions and answers
        P_answers_given_card = P_answers_given_card * probVector
        P_answers_given_not_card = P_answers_given_not_card * self.calculate_answers_given_not_card(questionans, probVector)

        #save cacheable answers
        if cache:
            self.cache_P_answers_given_card[numQuestionAns + 1] = P_answers_given_card
            self.cache_P_answers_given_not_card[numQuestionAns + 1] = P_answers_given_not_card

        #Evidence
        P_answers = P_card * P_answers_given_card + (1 - P_card) * P_answers_given_not_card

        #Bayes Theorem
        P_character_given_answers = (P_answers_given_card * P_card) / P_answers

        return P_character_given_answers

    #take the average for the answer with the current card excluded
    def calculate_answers_given_not_card(self, questionans, probVector):
        #Aggregate percentages from csv file
        numerator = np.full((len(probVector),), totals_map[questionans])

        #We subtract the value from the numerator
        numerator = numerator - probVector
        denominator = np.full((len(probVector),), TOTAL_CARDS_FINAL - 1)

        return numerator / denominator

BeyesCalcInst = BeyesTheoremCalc()