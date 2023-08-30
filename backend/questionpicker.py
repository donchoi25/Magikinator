from backend.beyestheoremcalc import BeyesCalcInst
import math
from globals.constants import QUESTION_DATA_FINAL
from globals.constants import TOTAL_CARDS_FINAL
from globals.constants import POSSIBLE_ANSWERS_FINAL
from globals.constants import TOTALS_MAP_FINAL
from globals.constants import COL_NUMPY_DICT_FINAL
import time
import numpy as np

class QuestionPicker:
    def __init__(self):
        #curr len of questions is 1507
        self.allQs = self.qParser()
    def qParser(self):
        qs = QUESTION_DATA_FINAL
        uniQ = set()
        for q in qs:
            #splits by delimiter, then store question into set without "yes, no, maybe"
            splitQ = q.split("#")
            uniQ.add("#".join([splitQ[0], splitQ[1]]))
        return uniQ
    def getBestQuestion(self, questionList, ansList):
        print("Finding best question...")
        bestQuestion = ('invalid', 100)

        prevtime = time.time()
        for question in self.allQs:
            #creating the weights for each answer
            yesCount = TOTALS_MAP_FINAL[question + "#YES"]
            noCount = TOTALS_MAP_FINAL[question + "#NO"]
            maybeCount = TOTALS_MAP_FINAL[question + "#MAYBE"]

            entropy_weight_map = {
                "YES": yesCount / TOTAL_CARDS_FINAL,
                "NO": noCount / TOTAL_CARDS_FINAL,
                "MAYBE": maybeCount / TOTAL_CARDS_FINAL
            }

            entropy_map = {
                "YES": 0,
                "NO": 0,
                "MAYBE": 0
            }
            
            #calculate the new probabilities for each card if we add the new answer for the current question
            for ans in POSSIBLE_ANSWERS_FINAL:
                columnVector = COL_NUMPY_DICT_FINAL[question + "#" + ans]
                newProbVector = BeyesCalcInst.calculateCardProb(len(questionList), question + "#" + ans, columnVector, False)
                entropy_map[ans] = np.sum(-1 * newProbVector * np.emath.logn(TOTAL_CARDS_FINAL, (newProbVector)))
            
            totalEntropy = 0
            #create the weighted sum for entropy
            for key in entropy_map:
                totalEntropy += entropy_map[key] * entropy_weight_map[key]
            #print((question, totalEntropy))
            #save the question that creates the lowest entropy
            if totalEntropy < bestQuestion[1]:
                bestQuestion = (question, totalEntropy)
        print("Time to find question: " + str(time.time() - prevtime))
        self.allQs.remove(bestQuestion[0])

        print("Best question Found")

        return bestQuestion[0]