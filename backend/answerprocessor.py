from backend.beyestheoremcalc import BeyesCalcInst
from globals.constants import CARD_DATA_FINAL
from globals.constants import QUESTION_LIMIT_FINAL
from globals.constants import COL_NUMPY_DICT_FINAL
import numpy as np
import numexpr as ne

class AnswerProcessor:
    def processAnswer(self, questionList, newQuestion, newAnswer, cachedEntropyVal):
        print("Processing Answer...")

        columnVector = COL_NUMPY_DICT_FINAL[newQuestion + "#" + newAnswer]
        cardprobVector, cardentropy = BeyesCalcInst.calculateCardProb(len(questionList), columnVector)
        entropy = -1 * np.sum(ne.evaluate("probVector * log(probVector)"))

        maxIndex = np.argmax(cardprobVector)

        # maxProb = probVector[maxIndex]
        maxCard = CARD_DATA_FINAL[maxIndex]
        print("Current suspected card: " + maxCard)

        questionList.append(newQuestion)

        print("Current Entropy: " + str(entropy))
        print("Answer Processed")

        #return the answer if entropy is low enough
        if len(questionList) >= QUESTION_LIMIT_FINAL:
            return maxCard
        else:
            return None
