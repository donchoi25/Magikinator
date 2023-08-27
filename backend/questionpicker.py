from backend.beyestheoremcalc import BeyesCalcInst
import math
from globals.constants import cardcsv_dataframe, TOTAL_CARDS_FINAL, POSSIBLE_ANSWERS_FINAL, CARD_DATA_FINAL

import multiprocessing.pool as mp
import threading

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
        bestQuestion = ('invalid', 100)
        numQuestionAns = len(questionList)
        with mp.ThreadPool() as q_pool:
            # self, card, numQuestionAns, newQuestion, newAnswer, cache=True
            parameters = [(numQuestionAns, question) for question in self.allQs]
            for result in q_pool.starmap(calculateQuestionEntropy, parameters, chunksize=100):
                if result[1] < bestQuestion[1]:
                    bestQuestion = result
                
        self.allQs.remove(bestQuestion[0])
        return bestQuestion[0]
    
def calculateCardEntropy(card, numQuestionAns, newQuestion, newAnswer):
    return (newAnswer, BeyesCalcInst.calculateCardProb(card, numQuestionAns, newQuestion, newAnswer, False))

def calculateQuestionEntropy(numQuestionAns, question):
    yesCount = cardcsv_dataframe[question + "#YES"]["Sum"] / 100
    noCount = cardcsv_dataframe[question + "#NO"]["Sum"] / 100
    maybeCount = cardcsv_dataframe[question + "#MAYBE"]["Sum"] / 100

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
    
    with mp.ThreadPool() as pool:
        parameters = [(card, numQuestionAns, question, ans) for ans in POSSIBLE_ANSWERS_FINAL for card in CARD_DATA_FINAL]
        for result in pool.starmap(calculateCardEntropy, parameters, chunksize=100):
            entropy_map[result[0]] += -1 * result[1] * math.log(result[1], TOTAL_CARDS_FINAL)
    
    totalEntropy = 0
    #create the weighted sum for entropy
    for key in entropy_map:
        totalEntropy += entropy_map[key] * entropy_weight_map[key]
    
    return (question, totalEntropy)