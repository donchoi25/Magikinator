from backend.beyestheoremcalc import BeyesCalcInst
from globals.constants import CARD_DATA_FINAL
from globals.constants import QUESTION_LIMIT_FINAL
from globals.constants import COL_NUMPY_DICT_FINAL
import numpy as np
import numexpr as ne

class AnswerProcessor:
    def processAnswer(self, questionList, newQuestion, newAnswer, cachedEntropyValue=1):
        print("Processing Answer...")

        columnVector = COL_NUMPY_DICT_FINAL[newQuestion + "#" + newAnswer]
        cardprobVector, cardentropy = BeyesCalcInst.calculateCardProb(columnVector, cachedEntropyValue)
        entropy = -1 * np.sum(ne.evaluate("cardprobVector * log(cardprobVector)"))

        maxIndex = np.argmax(cardprobVector)

        # maxProb = probVector[maxIndex]
        maxCard = CARD_DATA_FINAL[maxIndex]
        print("Current suspected card: " + maxCard)

        questionList.append(newQuestion)

        print("Current Entropy: " + str(entropy))
        print("Answer Processed")

        #return the answer if entropy is low enough
        found_potential_card = len(questionList) >= QUESTION_LIMIT_FINAL or entropy < 0.01
        return (maxCard, cardentropy, found_potential_card)
