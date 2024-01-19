from backend.beyestheoremcalc import BeyesCalcInst
from globals.constants import CARD_DATA_FINAL
from globals.constants import QUESTION_LIMIT_FINAL
# from globals.constants import COL_NUMPY_DICT_FINAL
# from globals.constants import cardcsv_dataframe
from globals.constants import CARD_DATA_COLUMNS
import numpy as np
import numexpr as ne

class AnswerProcessor:
    def processAnswer(self, questionList, newQuestion, newAnswer, rejected_cards, cachedEntropyValue=1):
        # print("Processing Answer...")

        columnVector = np.array(CARD_DATA_COLUMNS[newQuestion + "#" + newAnswer]) / 100
        # COL_NUMPY_DICT_FINAL[newQuestion + "#" + newAnswer]
        cardprobVector, cardentropy = BeyesCalcInst.calculateCardProb(columnVector, cachedEntropyValue)
        entropy = -1 * np.sum(ne.evaluate("cardprobVector * log(cardprobVector)"))

        maxIndices = np.argpartition(cardprobVector, -1 * max(5, len(rejected_cards) + 1))[-1 * (max(5, len(rejected_cards) + 1)):]
        maxCards = [[CARD_DATA_FINAL[index], cardprobVector[index]] for index in maxIndices]
        maxCards.sort(key=lambda x: -1 * x[1])
        
        maxCard = None
        entropy_difference = 0
        # We are not guessing the card, when the entropy value for our highest card is greater than another candidate by a large 
        # enough factor.
        for i in range(len(maxCards)):
            card = maxCards[i]
            if card[0] not in rejected_cards:
                maxCard = card
                if i + 1 < len(maxCards) - 1:
                    entropy_difference = maxCards[i + 1][1] - maxCard[1]
                    # This is the new threshold for whether we want to take a stab at guessing the card
                break

        maxCards = [card[0] for card in maxCards]
        maxCard = maxCard[0]
        # print("Current suspected card: " + maxCard)
        # questionList.append(newQuestion)
        # print("Current Entropy: " + str(entropy))
        # print("Answer Processed")

        # Return the answer if entropy is low enough
        # Return the answer if the entropy difference between the highest card and the next card has a large enough gap
        # print(entropy_difference)
        found_potential_card = len(questionList) >= QUESTION_LIMIT_FINAL or (entropy_difference != 0 and entropy < 0.001)
        return (maxCard, cardentropy, found_potential_card, maxCards[:5], entropy, rejected_cards)
