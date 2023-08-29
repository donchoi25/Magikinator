from backend.beyestheoremcalc import BeyesCalcInst
import math
from globals.constants import cardcsv_dataframe, TOTAL_CARDS_FINAL, POSSIBLE_ANSWERS_FINAL, CARD_DATA_FINAL, totals_map
import time
import numpy as np

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
        print("Finding best question...")
        bestQuestion = ('invalid', 100)

        prevtime = time.time()
        for question in self.allQs:
            #creating the weights for each answer
            yesCount = totals_map[question + "#YES"] / 100
            noCount = totals_map[question + "#NO"] / 100
            maybeCount = totals_map[question + "#MAYBE"] / 100

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
                columnVector = np.array(list(cardcsv_dataframe[question + "#" + ans].values())) / 100
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