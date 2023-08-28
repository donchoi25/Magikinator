from backend.beyestheoremcalc import BeyesCalcInst
from globals.constants import cardcsv_dataframe, QUESTION_LIMIT_FINAL

class AnswerProcessor:
    def __init__(self):
        self.ansCount = 0
    def processAnswer(self, questionList, ansList, newQuestion, newAnswer):
        print("Processing Answer...")
        bestAns = ("Invalid", 0)

        cardData = list(cardcsv_dataframe["Name"])[0:-1]
        #go through every card and calculate its probability
        for card in cardData:
            currProb = BeyesCalcInst.calculateCardProb(card, len(questionList), newQuestion, newAnswer)

            #print((card, currProb))

            if currProb > bestAns[1]:
                bestAns = (card, currProb)

        questionList.append(newQuestion)
        ansList.append(newAnswer)
        self.ansCount += 1

        print("Answer Processed")

        #return the answer if our certainty is high enough
        #TODO in addition, might need to check entropy so we don't reach a decision to quickly
        if bestAns[1] > 0.75 or self.ansCount > QUESTION_LIMIT_FINAL:
            return bestAns[0]
        else:
            return ""
