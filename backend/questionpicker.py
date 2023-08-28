from backend.beyestheoremcalc import BeyesCalcInst
import math
from globals.constants import cardcsv_dataframe, POSSIBLE_ANSWERS_FINAL

import multiprocessing.pool as mp
import threading
import time

class QuestionPicker:
    def __init__(self):
        #curr len of questions is 1507
        self.allQs = self.qParser()
    def qParser(self):
        qs = list(cardcsv_dataframe.keys())[2:]
        uniQ = set()
        for q in qs:
            #splits by delimiter, then store question into set without "yes, no, maybe"
            splitQ = q.split("#")
            uniQ.add("#".join([splitQ[0], splitQ[1]]))
        return uniQ
    
    def getBestQuestion(self, questionList, ansList):
        print("Finding Best Question...")
        bestQuestion = ('invalid', 100)
        numQuestionAns = len(questionList)
        prevtime = time.time()
        with mp.Pool() as q_pool:
            # self, card, numQuestionAns, newQuestion, newAnswer, cache=True
            parameters = [(cardcsv_dataframe, numQuestionAns, question, BeyesCalcInst.cache_P_answers_given_card, BeyesCalcInst.cache_P_answers_given_not_card) for question in self.allQs ]
            for result in q_pool.starmap(calculateQuestionEntropy, parameters, chunksize=100):
                if result[1] < bestQuestion[1]:
                    bestQuestion = result
        print("Time to find question: " + str(time.time() - prevtime))
        self.allQs.remove(bestQuestion[0])
        return bestQuestion[0]

def calculateQuestionEntropy(datamap, numQuestionAns, question, given_card_cache, given_not_card_cache):
    yesCount = datamap[question + "#YES"]["Sum"] / 100
    noCount = datamap[question + "#NO"]["Sum"] / 100
    maybeCount = datamap[question + "#MAYBE"]["Sum"] / 100

    TOTAL_CARDS_FINAL = len(datamap["Name"])

    entropy_weight_map = {
        "yes": yesCount / TOTAL_CARDS_FINAL,
        "no": noCount / TOTAL_CARDS_FINAL,
        "maybe": maybeCount / TOTAL_CARDS_FINAL
    }

    entropy_map = {
        "yes": 0,
        "no": 0,
        "maybe": 0
    }
    
    CardData = list(datamap["Name"])[0:-1]
     #calculate the new probabilities for each card if we add the new answer for the current question
    for card in CardData:
        for ans in POSSIBLE_ANSWERS_FINAL:
            newProb = BeyesCalcInst.calculateCardProb(card, numQuestionAns, question, ans, \
    datamap, given_card_cache, given_not_card_cache, False)

            entropy_map[ans] += -1 * newProb * math.log(newProb, TOTAL_CARDS_FINAL)
    
    totalEntropy = 0
    #create the weighted sum for entropy
    for key in entropy_map:
        totalEntropy += entropy_map[key] * entropy_weight_map[key]
    
    return (question, totalEntropy)