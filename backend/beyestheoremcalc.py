from data import cards as data
TOTAL_CARDS_FINAL = data.TotalCards

class BeyesTheoremCalc:
    def calculateCardProb(self, card, ansList, questionList):
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

    def calculate_answers_given_not_card(self, card, question, answer):
        numerator = data.CategoryCount[question] if answer == 'yes' else TOTAL_CARDS_FINAL - data.CategoryCount[question]
        denominator = TOTAL_CARDS_FINAL
        if (question in data.Cards[card] and answer == 'yes') or (question not in data.Cards[card] and answer == 'no'):
            numerator -= 1
            denominator -= 1
        else:
            denominator -= 1

        return numerator / denominator

    def calculate_answers_given_card(self, card, question, answer):
        if card in data.Cards:
            if (question in data.Cards[card] and answer == 'yes') or (question not in data.Cards[card] and answer == 'no'):
                return 1
            elif answer == 'maybe':
                return 0.5
            else:
                return 0
        else:
            print('Card not in database')
            return 0
