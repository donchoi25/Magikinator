import pandas as pd
cardcsv_dataframe = pd.read_csv('./data/files/cardsdata_live.csv')

#TODO: count number of cards
TOTAL_CARDS_FINAL = 10

#how to get specific card:
    #cardcsv_dataframe.loc[cardcsv_dataframe.name=="Swamp", question+"#YES"].values[0]

class BeyesTheoremCalc:
    def calculateCardProb(self, card, questionList, ansList):
        P_card = 1 / TOTAL_CARDS_FINAL
        P_answers_given_card = 1
        P_answers_given_not_card = 1

        for question, answer in zip(questionList, ansList):
            P_answers_given_card *= max(self.calculate_answers_given_card(card, question, answer), 0.01)

            P_answers_given_not_card *= max(self.calculate_answers_given_not_card(card, question, answer), 0.01)

        #Evidence
        P_answers = P_card * P_answers_given_card + (1 - P_card) * P_answers_given_not_card

        #Bayes Theorem
        P_character_given_answers = (P_answers_given_card * P_card) / P_answers

        return P_character_given_answers

    #here, we're essentially taking the average for the answer with the current card excluded
    def calculate_answers_given_not_card(self, card, question, answer):
        #Aggregate percentages from csv file
        numerator = cardcsv_dataframe[question + "#" + answer.upper()].sum() / 100

        #We subtract the value from the numerator
        numerator -= cardcsv_dataframe.loc[cardcsv_dataframe.name==card, question+"#"+answer.upper()].values[0] / 100
        denominator = TOTAL_CARDS_FINAL - 1

        return numerator / denominator

    #this value is a lookup into the table
    def calculate_answers_given_card(self, card, question, answer):
        return cardcsv_dataframe.loc[cardcsv_dataframe.name==card, question+"#"+answer.upper()].values[0] / 100
