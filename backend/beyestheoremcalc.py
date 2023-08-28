from globals.constants import cardcsv_dataframe
from multiprocessing import Process, current_process, parent_process

#how to get specific card:
    #cardcsv_dataframe.at["Swamp", question+"#YES"].values[0]

class BeyesTheoremCalc:
    def __init__(self):
        #calculations cache
        self.cache_P_answers_given_card = {}
        self.cache_P_answers_given_not_card = {}
    def calculateCardProb(self, card, numQuestionAns, newQuestion, newAnswer, datamap = {}, cache_given_card = {}, cache_given_not_card = {}, cache=True):
        if current_process().name == 'MainProcess':
            P_card = 1 / len(cardcsv_dataframe["Name"])

            P_answers_given_card = 1
            P_answers_given_not_card = 1
            #only look into cache if this is not the first question
            if numQuestionAns > 0:
                P_answers_given_card = self.cache_P_answers_given_card[(card, numQuestionAns)]
                P_answers_given_not_card = self.cache_P_answers_given_not_card[(card, numQuestionAns)]

            #calculate for the new questions and answers
            P_answers_given_card *= self.calculate_answers_given_card(card, newQuestion, newAnswer, datamap)
            P_answers_given_not_card *= self.calculate_answers_given_not_card(card, newQuestion, newAnswer, datamap)

            #save cacheable answers
            if cache:
                self.cache_P_answers_given_card[(card, numQuestionAns + 1)] = P_answers_given_card
                self.cache_P_answers_given_not_card[(card, numQuestionAns + 1)] = P_answers_given_not_card

            #Evidence
            P_answers = P_card * P_answers_given_card + (1 - P_card) * P_answers_given_not_card

            #Bayes Theorem
            P_character_given_answers = (P_answers_given_card * P_card) / P_answers

            return P_character_given_answers
        else:
            P_card = 1 / len(datamap["Name"])

            P_answers_given_card = 1
            P_answers_given_not_card = 1
            #only look into cache if this is not the first question
            if numQuestionAns > 0:
                P_answers_given_card = cache_given_card[(card, numQuestionAns)]
                P_answers_given_not_card = cache_given_not_card[(card, numQuestionAns)]

            #calculate for the new questions and answers
            P_answers_given_card *= self.calculate_answers_given_card(card, newQuestion, newAnswer, datamap)
            P_answers_given_not_card *= self.calculate_answers_given_not_card(card, newQuestion, newAnswer, datamap)

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
    def calculate_answers_given_not_card(self, card, question, answer, datamap = {}):
        if current_process().name == 'MainProcess':
            #Aggregate percentages from csv file
            numerator = cardcsv_dataframe[question + "#" + answer.upper()]["Sum"] / 100

            #We subtract the value from the numerator
            numerator -= cardcsv_dataframe[question+"#"+answer.upper()][card] / 100

            denominator = len(cardcsv_dataframe["Name"]) - 1
        else:
            #Aggregate percentages from csv file
            numerator = datamap[question + "#" + answer.upper()]["Sum"] / 100

            #We subtract the value from the numerator
            numerator -= datamap[question+"#"+answer.upper()][card] / 100

            denominator = len(datamap["Name"]) - 1

        return numerator / denominator

    #this value is a lookup into the table
    def calculate_answers_given_card(self, card, question, answer, datamap = {}):
        if current_process().name == 'MainProcess':
            return cardcsv_dataframe[question+"#"+answer.upper()][card] / 100
        else:
            return datamap[question+"#"+answer.upper()][card] / 100

BeyesCalcInst = BeyesTheoremCalc()