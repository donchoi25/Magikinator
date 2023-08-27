from backend.beyestheoremcalc import BeyesCalcInst
from globals.constants import cardcsv_dataframe, QUESTION_LIMIT_FINAL, CARD_DATA_FINAL

class AnswerProcessor:
    def __init__(self):
        self.ansCount = 0
    def processAnswer(self, questionList, ansList, newQuestion, newAnswer):
        bestAns = ("Invalid", 0)

        #go through every card and calculate its probability
        for card in CARD_DATA_FINAL:
            currProb = BeyesCalcInst.calculateCardProb(card, questionList, ansList, newQuestion, newAnswer)

            #print((card, currProb))

            if currProb > bestAns[1]:
                bestAns = (card, currProb)

        questionList.append(newQuestion)
        ansList.append(newAnswer)
        self.ansCount += 1

        #return the answer if our certainty is high enough
        #TODO in addition, might need to check entropy so we don't reach a decision to quickly
        if bestAns[1] > 0.75 or self.ansCount > QUESTION_LIMIT_FINAL:
            return bestAns[0]
        else:
            return ""
