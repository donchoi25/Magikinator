from backend.beyestheoremcalc import BeyesCalcInst
from globals.constants import CARD_DATA_FINAL
from globals.constants import QUESTION_LIMIT_FINAL
from globals.constants import COL_NUMPY_DICT_FINAL
import numpy as np
import numexpr as ne

class AnswerProcessor:
    def processAnswer(self, questionList, ansList, newQuestion, newAnswer):
        print("Processing Answer...")

        columnVector = COL_NUMPY_DICT_FINAL[newQuestion + "#" + newAnswer]
        probVector = BeyesCalcInst.calculateCardProb(len(questionList), newQuestion + "#" + newAnswer, columnVector)
        entropy = -1 * np.sum(ne.evaluate("probVector * log(probVector)"))

        maxIndex = np.argmax(probVector)

        maxProb = probVector[maxIndex]
        maxCard = CARD_DATA_FINAL[maxIndex]

        questionList.append(newQuestion)
        ansList.append(newAnswer)

        print("Current Entropy: " + str(entropy))
        print("Answer Processed")

        #return the answer if entropy is low enough
        if entropy < 0.01 or len(questionList) >= QUESTION_LIMIT_FINAL:
            return maxCard
        else:
            return ""
