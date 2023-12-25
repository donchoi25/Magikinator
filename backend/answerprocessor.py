from backend.beyestheoremcalc import BeyesCalcInst
from globals.constants import CARD_DATA_FINAL
from globals.constants import QUESTION_LIMIT_FINAL
# from globals.constants import COL_NUMPY_DICT_FINAL
from globals.constants import cardcsv_dataframe
import numpy as np
import numexpr as ne

class AnswerProcessor:
    def processAnswer(self, questionList, newQuestion, newAnswer, rejected_cards, cachedEntropyValue=1):
        # print("Processing Answer...")

        columnVector = cardcsv_dataframe[newQuestion + "#" + newAnswer].to_numpy() / 100
        # COL_NUMPY_DICT_FINAL[newQuestion + "#" + newAnswer]
        cardprobVector, cardentropy = BeyesCalcInst.calculateCardProb(columnVector, cachedEntropyValue)
        entropy = -1 * np.sum(ne.evaluate("cardprobVector * log(cardprobVector)"))

        maxIndex = np.argmax(cardprobVector)
        maxCard = CARD_DATA_FINAL[maxIndex]
        while maxCard in rejected_cards:
            cardprobVector = np.delete(cardprobVector, maxIndex)
            maxIndex = np.argmax(cardprobVector)
            maxCard = CARD_DATA_FINAL[maxIndex]

        maxIndices = np.argpartition(cardprobVector, -5)[-5:]
        # maxProb = probVector[maxIndex]
        maxCards = [CARD_DATA_FINAL[index] for index in maxIndices]
        # print("Current suspected card: " + maxCard)

        # questionList.append(newQuestion)

        # print("Current Entropy: " + str(entropy))
        # print("Answer Processed")

        #return the answer if entropy is low enough
        found_potential_card = len(questionList) >= QUESTION_LIMIT_FINAL
        return (maxCard, cardentropy, found_potential_card, maxCards, entropy, rejected_cards)
