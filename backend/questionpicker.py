from backend.beyestheoremcalc import BeyesCalcInst
import math
from globals.constants import cardcsv_dataframe, TOTAL_CARDS_FINAL, POSSIBLE_ANSWERS_FINAL
import multiprocessing.pool as mp
import time

class QuestionPicker:
    def __init__(self):
        self.cardData = cardcsv_dataframe["Name"].tolist()
        self.allQs = self.qParser()
    def qParser(self):
        qs = cardcsv_dataframe.columns.tolist()[2:]
        uniQ = set()
        for q in qs:
            #splits by delimiter, then store question into set without "yes, no, maybe"
            splitQ = q.split("#")
            uniQ.add("#".join([splitQ[0], splitQ[1]]))
        return uniQ
    def getBestQuestion(self, questionList, ansList):
        bestQuestion = ('invalid', 100)
        t0 = time.time()
        with mp.ThreadPool() as q_pool:
            parameters = [(question, questionList, ansList, self.cardData) for question in self.allQs]
            for result in q_pool.starmap(calculateQuestionEntropy, parameters, chunksize=100):
                if result[1] < bestQuestion[1]:
                    bestQuestion = result
        t1 = time.time()
        print(t1 - t0)
        self.allQs.remove(bestQuestion[0])
        return bestQuestion[0]
    
def calculateCardEntropy(card, questionList, ansList, question, ans):
    return (ans, BeyesCalcInst.calculateCardProb(card, questionList, ansList, question, ans))

def calculateQuestionEntropy(question, questionList, ansList, cardData):
    yesCount = cardcsv_dataframe[question + "#YES"].sum() / 100
    noCount = cardcsv_dataframe[question + "#NO"].sum() / 100
    maybeCount = cardcsv_dataframe[question + "#MAYBE"].sum() / 100

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
    
    t0 = time.time()
    with mp.ThreadPool() as pool:
        parameters = [(card, questionList, ansList, question, ans) for ans in POSSIBLE_ANSWERS_FINAL for card in cardData]
        for result in pool.starmap(calculateCardEntropy, parameters, chunksize=100):
            entropy_map[result[0]] += -1 * result[1] * math.log(result[1], TOTAL_CARDS_FINAL)
    t1 = time.time()
    print(t1 - t0)
    
    totalEntropy = 0
    #create the weighted sum for entropy
    for key in entropy_map:
        totalEntropy += entropy_map[key] * entropy_weight_map[key]
    
    return (question, totalEntropy)