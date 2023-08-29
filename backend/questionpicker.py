from backend.beyestheoremcalc import BeyesCalcInst
import math
from globals.constants import DATA_NUMPY_FINAL
from globals.constants import TOTAL_CARDS_FINAL
from globals.constants import POSSIBLE_ANSWERS_FINAL
from globals.constants import CARD_DATA_FINAL
from globals.constants import TOTAL_PROB_VECTOR_FINAL
from globals.constants import ENTROPY_WEIGHT_VECTOR_FINAL
from globals.constants import QUESTION_DATA_FINAL
from globals.constants import cardcsv_dataframe
import time
import numpy as np

class QuestionPicker:
    def __init__(self):
        #curr len of questions is 1507
        self.uniQs = self.qParser()
    def qParser(self):
        qs = QUESTION_DATA_FINAL
        uniQSet = set()
        uniQ = []
        for q in qs:
            #splits by delimiter, then store question into set without "yes, no, maybe"
            splitQ = q.split("#")
            justQ = "#".join([splitQ[0], splitQ[1]])
            if justQ not in uniQSet:
                uniQ.append(justQ)
                uniQSet.add(justQ)
        return uniQ
    def getBestQuestion(self, questionList, ansList):
        print("Finding best question...")
        prevtime = time.time()

        #calculate the new probabilities for each card if we add the new answer for all questions
        matrixVector = DATA_NUMPY_FINAL / 100
        newProbVector = BeyesCalcInst.MAT_calculateCardProb(len(questionList), matrixVector)
        entropyVector = np.sum(-1 * newProbVector * np.emath.logn(TOTAL_CARDS_FINAL, (newProbVector)), axis=0)

        entropyVector = entropyVector * ENTROPY_WEIGHT_VECTOR_FINAL

        entropyVector = np.add.reduceat(entropyVector, np.arange(0, len(entropyVector), 3))

        
        maxIndex = np.argmin(entropyVector)

        bestQuestion = self.uniQs[maxIndex]
        print("Time to find question: " + str(time.time() - prevtime))


        #TODO need a clean way to remove questions from consideration in data
        #self.uniQs.remove(bestQuestion[0])

        print("Best question Found")

        return bestQuestion