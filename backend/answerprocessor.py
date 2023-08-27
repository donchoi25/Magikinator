from backend.beyestheoremcalc import BeyesCalcInst
from globals.constants import cardcsv_dataframe, QUESTION_LIMIT_FINAL

import multiprocessing.pool as mp
import time

class AnswerProcessor:
    def __init__(self):
        self.cardData = cardcsv_dataframe["Name"].tolist()
        self.ansCount = 0
    def processAnswer(self, questionList, ansList, newQuestion, newAnswer):
        bestAns = ("Invalid", 0)

        time.time()
        with mp.ThreadPool() as pool:
            parameters = [(card, questionList, ansList, newQuestion, newAnswer) for card in self.cardData]
            for result in pool.starmap(calculateCardProbability, parameters, chunksize=100):
                if result[1] > bestAns[1]:
                    bestAns = result
        time.time()
                    
        # #go through every card and calculate its probability
        # for card in self.cardData:
        #     currProb = BeyesCalcInst.calculateCardProb(card, questionList, ansList, newQuestion, newAnswer)

        #     if currProb > bestAns[1]:
        #         bestAns = (card, currProb)

        questionList.append(newQuestion)
        ansList.append(newAnswer)
        self.ansCount += 1

        #return the answer if our certainty is high enough
        #TODO in addition, might need to check entropy so we don't reach a decision to quickly
        if bestAns[1] > 0.75 or self.ansCount > QUESTION_LIMIT_FINAL:
            return bestAns[0]
        else:
            return ""

def calculateCardProbability(card, questionList, ansList, newQuestion, newAnswer):
    return (card, BeyesCalcInst.calculateCardProb(card, questionList, ansList, newQuestion, newAnswer))