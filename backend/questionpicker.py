from backend.beyestheoremcalc import BeyesCalcInst
import math
from globals.constants import QUESTION_DATA_FINAL
from globals.constants import TOTAL_CARDS_FINAL
from globals.constants import POSSIBLE_ANSWERS_FINAL
from globals.constants import TOTALS_MAP_FINAL
from globals.constants import cardcsv_dataframe
import time
import numpy as np
import numexpr as ne

class QuestionPicker:
    def __init__(self):
        #curr len of questions is 3900~
        self.allQs = self.qParser()
        # print("NUMBER OF ALL QUESTIONS: " + str(len(self.allQs)))
    def qParser(self):
        qs = QUESTION_DATA_FINAL
        uniQ = set()
        for q in qs:
            #splits by delimiter, then store question into set without "yes, no, maybe"
            splitQ = q.split("#")
            uniQ.add("#".join([splitQ[0]]))
        return uniQ
    def getBestQuestion(self, questionList, cachedEntropyVector=1):
        # TODO: QuestionList, as well as the current entropy values are
        # print("Finding best question...")
        # print("Best questions so far have included: " + str(questionList))
        bestQuestion = ('invalid', float('inf'))
        bestQuestionCandidates = []
        prevtime = time.time()
        for question in self.allQs:
            if question in questionList:
                continue
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
                columnVector = cardcsv_dataframe[question + "#" + ans].to_numpy() / 100
                newProbVector, _ = BeyesCalcInst.calculateCardProb(columnVector, cachedEntropyVector)
                entropy_map[ans] = -1 * np.sum(ne.evaluate("newProbVector * log(newProbVector)"))
                
            totalEntropy = 0
            #create the weighted sum for entropy
            for key in entropy_map:
                totalEntropy += entropy_map[key] * entropy_weight_map[key]
            #print((question, totalEntropy))
            #save the question that creates the lowest entropy
            if totalEntropy < bestQuestion[1]:
                bestQuestionCandidates.append(bestQuestion[0])
                bestQuestion = (question, totalEntropy)
        # print("Time to find question: " + str(time.time() - prevtime))
        # self.allQs.remove(bestQuestion[0])
        # print("Best question Found: " + str(bestQuestion[0]))

        # print(bestQuestionCandidates)
        # print('\n')
        return bestQuestion[0]