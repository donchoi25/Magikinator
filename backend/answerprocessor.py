from backend.beyestheoremcalc import BeyesCalcInst
from globals.constants import cardcsv_dataframe
from globals.constants import QUESTION_LIMIT_FINAL
from globals.constants import CARD_DATA_FINAL
from globals.constants import QUESTION_DATA_FINAL
from globals.constants import TOTAL_PROB_VECTOR_FINAL
from globals.constants import DATA_NUMPY_FINAL
import numpy as np
class AnswerProcessor:
    def __init__(self):
        self.ansCount = 0
    def processAnswer(self, questionList, ansList, newQuestion, newAnswer):
        print("Processing Answer...")

        #find the column index, then return that as the column vector
        #TODO possibly remove this linear search for index
        colIndex = QUESTION_DATA_FINAL.index(newQuestion + "#" + newAnswer)

        columnVector = DATA_NUMPY_FINAL[:, colIndex] / 100

        #finding questionans total value
        QAPairTotal = TOTAL_PROB_VECTOR_FINAL[colIndex]

        #calculating probability for this question#ans pair
        probVector = BeyesCalcInst.COL_calculateCardProb(len(questionList), columnVector, QAPairTotal)

        maxIndex = np.argmax(probVector)

        maxProb = probVector[maxIndex]
        maxCard = CARD_DATA_FINAL[maxIndex]

        questionList.append(newQuestion)
        ansList.append(newAnswer)
        self.ansCount += 1

        print("Answer Processed")

        #return the answer if our certainty is high enough
        #TODO in addition, might need to check entropy so we don't reach a decision to quickly
        if maxProb > 0.9 or self.ansCount > QUESTION_LIMIT_FINAL:
            return maxCard
        else:
            return ""
