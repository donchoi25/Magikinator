from backend.beyestheoremcalc import BeyesCalcInst
from globals.constants import CARD_DATA_FINAL
from globals.constants import QUESTION_LIMIT_FINAL
from globals.constants import COL_NUMPY_DICT_FINAL
import numpy as np
class AnswerProcessor:
    def __init__(self):
        self.ansCount = 0
    def processAnswer(self, questionList, ansList, newQuestion, newAnswer):
        print("Processing Answer...")

        columnVector = COL_NUMPY_DICT_FINAL[newQuestion + "#" + newAnswer]
        probVector = BeyesCalcInst.calculateCardProb(len(questionList), newQuestion + "#" + newAnswer, columnVector)

        maxIndex = np.argmax(probVector)

        maxProb = probVector[maxIndex]
        maxCard = CARD_DATA_FINAL[maxIndex]

        questionList.append(newQuestion)
        ansList.append(newAnswer)
        self.ansCount += 1

        print("Answer Processed")

        #return the answer if our certainty is high enough
        #TODO in addition, might need to check entropy so we don't reach a decision to quickly
        if self.ansCount > QUESTION_LIMIT_FINAL:
            return maxCard
        else:
            return ""
