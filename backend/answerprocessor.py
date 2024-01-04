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

        maxIndices = np.argpartition(cardprobVector, -1 * max(5, len(rejected_cards) + 1))[-1 * (max(5, len(rejected_cards) + 1)):]
        maxCards = [[CARD_DATA_FINAL[index], cardprobVector[index]] for index in maxIndices]
        maxCards.sort(key=lambda x: -1 * x[1])
        maxCards = [card[0] for card in maxCards]
        
        maxCard = None
        for card in maxCards:
            if card not in rejected_cards:
                maxCard = card
                break

        # print("Current suspected card: " + maxCard)
        # questionList.append(newQuestion)
        # print("Current Entropy: " + str(entropy))
        # print("Answer Processed")

        # Return the answer if entropy is low enough
        # Return the answer if the entropy difference between the highest card and the next card has a large enough gap
        
        found_potential_card = len(questionList) >= QUESTION_LIMIT_FINAL
        return (maxCard, cardentropy, found_potential_card, maxCards[:5], entropy, rejected_cards)
