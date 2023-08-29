from globals.constants import TOTAL_CARDS_FINAL
from globals.constants import TOTAL_PROB_VECTOR_FINAL
import numpy as np
import numexpr as ne

class BeyesTheoremCalc:
    def __init__(self):
        #cache that will store vectors for the following calculations:
            #P_answers_given_card
            #P_answers_given_not_card
        #key will be number of questions and answers we're at so far
        self.cache_P_answers_given_card = {}
        self.cache_P_answers_given_not_card = {}

    #analyze whole matrix of data. Used to calculate entropy. Will not cache
    def MAT_calculateCardProb(self, numQuestionAns, probVector):
        P_card = 1 / TOTAL_CARDS_FINAL
        
        #only look into cache if this is not the first question
        if numQuestionAns > 0:
            cacheResult_P_answers_given_card = self.cache_P_answers_given_card[numQuestionAns]
            cacheResult_P_answers_given_not_card = self.cache_P_answers_given_not_card[numQuestionAns]
            P_answers_given_card =  np.full((probVector.shape[1], TOTAL_CARDS_FINAL), cacheResult_P_answers_given_card).T
            P_answers_given_not_card = np.full((probVector.shape[1], TOTAL_CARDS_FINAL), cacheResult_P_answers_given_not_card).T
        else:
            P_answers_given_card = 1
            P_answers_given_not_card = 1
        #calculate for the new questions and answers
        P_answers_given_card = ne.evaluate("P_answers_given_card * probVector")
        temp = self.MAT_calculate_answers_given_not_card(probVector)
        P_answers_given_not_card = ne.evaluate("P_answers_given_not_card * temp")

        #Evidence
        P_answers = ne.evaluate("P_card * P_answers_given_card + (1 - P_card) * P_answers_given_not_card")

        #Bayes Theorem
        P_character_given_answers = ne.evaluate("(P_answers_given_card * P_card) / P_answers")

        return P_character_given_answers

    #take the average for the answer with the current card excluded
    def MAT_calculate_answers_given_not_card(self, probVector):
        #Aggregate percentages from csv file
        numerator = np.full((len(probVector), len(TOTAL_PROB_VECTOR_FINAL)), TOTAL_PROB_VECTOR_FINAL)
        return ne.evaluate("(numerator - probVector) / (TOTAL_CARDS_FINAL - 1)")

    
    #calculate single prob vector. Used to process answer given. This function will cache
    def COL_calculateCardProb(self, numQuestionAns, probVector, QAPairTotal):
        P_card = 1 / TOTAL_CARDS_FINAL
        
        #only look into cache if this is not the first question
        if numQuestionAns > 0:
            P_answers_given_card = self.cache_P_answers_given_card[numQuestionAns]
            P_answers_given_not_card = self.cache_P_answers_given_not_card[numQuestionAns]
        else:
            P_answers_given_card = 1
            P_answers_given_not_card = 1
        #calculate for the new questions and answers
        P_answers_given_card = P_answers_given_card * probVector
        P_answers_given_not_card = P_answers_given_not_card * self.COL_calculate_answers_given_not_card(probVector, QAPairTotal)

        self.cache_P_answers_given_card[numQuestionAns + 1] = P_answers_given_card
        self.cache_P_answers_given_not_card[numQuestionAns + 1] = P_answers_given_not_card

        #Evidence
        P_answers = P_card * P_answers_given_card + (1 - P_card) * P_answers_given_not_card

        #Bayes Theorem
        P_character_given_answers = (P_answers_given_card * P_card) / P_answers

        return P_character_given_answers

    #take the average for the answer with the current card excluded
    def COL_calculate_answers_given_not_card(self, probVector, QAPairTotal):
        #Aggregate percentages from csv file
        numerator = np.full((len(probVector),), QAPairTotal)

        return (numerator - probVector) / (TOTAL_CARDS_FINAL - 1)

BeyesCalcInst = BeyesTheoremCalc()