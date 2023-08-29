from backend.beyestheoremcalc import BeyesCalcInst
from globals.constants import cardcsv_dataframe, QUESTION_LIMIT_FINAL, CARD_DATA_FINAL
import numpy as np
class AnswerProcessor:
    def __init__(self):
        self.ansCount = 0
    def processAnswer(self, questionList, ansList, newQuestion, newAnswer):
        print("Processing Answer...")

        columnVector = np.array(list(cardcsv_dataframe[newQuestion + "#" + newAnswer].values())) / 100
        probVector = BeyesCalcInst.calculateCardProb(len(questionList), newQuestion + "#" + newAnswer, columnVector)

        maxIndex = np.argmax(probVector)

        maxProb = probVector[maxIndex]
        maxCard = list(cardcsv_dataframe[newQuestion + "#" + newAnswer].keys())[maxIndex]

        questionList.append(newQuestion)
        ansList.append(newAnswer)
        self.ansCount += 1

        print("Answer Processed")

        #return the answer if our certainty is high enough
        #TODO in addition, might need to check entropy so we don't reach a decision to quickly
        if maxProb > 0.8 or self.ansCount > QUESTION_LIMIT_FINAL:
            return maxCard
        else:
            return ""
