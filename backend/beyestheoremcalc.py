from globals.constants import cardcsv_dataframe, TOTAL_CARDS_FINAL
#from numba import jit

#how to get specific card:
    #cardcsv_dataframe.at["Swamp", question+"#YES"].values[0]

class BeyesTheoremCalc:
    def __init__(self):
        #calculations cache
        self.cache_P_answers_given_card = {}
        self.cache_P_answers_given_not_card = {}
    def calculateCardProb(self, card, numQuestionAns, newQuestion, newAnswer, cache=True):
        P_card = 1 / TOTAL_CARDS_FINAL

        P_answers_given_card = 1
        P_answers_given_not_card = 1
        #only look into cache if this is not the first question
        if numQuestionAns > 0:
            P_answers_given_card = self.cache_P_answers_given_card[(card, numQuestionAns)]
            P_answers_given_not_card = self.cache_P_answers_given_not_card[(card, numQuestionAns)]

        #calculate for the new questions and answers
        P_answers_given_card *= self.calculate_answers_given_card(card, newQuestion, newAnswer)
        P_answers_given_not_card *= self.calculate_answers_given_not_card(card, newQuestion, newAnswer)

        #save cacheable answers
        if cache:
            self.cache_P_answers_given_card[(card, numQuestionAns + 1)] = P_answers_given_card
            self.cache_P_answers_given_not_card[(card, numQuestionAns + 1)] = P_answers_given_not_card

        #Evidence
        P_answers = P_card * P_answers_given_card + (1 - P_card) * P_answers_given_not_card

        #Bayes Theorem
        P_character_given_answers = (P_answers_given_card * P_card) / P_answers

        return P_character_given_answers

    #take the average for the answer with the current card excluded
    def calculate_answers_given_not_card(self, card, question, answer):
        #Aggregate percentages from csv file
        numerator = cardcsv_dataframe[question + "#" + answer.upper()]["Sum"] / 100

        #We subtract the value from the numerator
        numerator -= cardcsv_dataframe[question+"#"+answer.upper()][card] / 100
        denominator = TOTAL_CARDS_FINAL - 1

        return numerator / denominator

    #this value is a lookup into the table
    def calculate_answers_given_card(self, card, question, answer):
        return cardcsv_dataframe[question+"#"+answer.upper()][card] / 100

BeyesCalcInst = BeyesTheoremCalc()