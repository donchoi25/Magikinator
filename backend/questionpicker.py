from backend.beyestheoremcalc import BeyesCalcInst
import math
from globals.constants import cardcsv_dataframe, TOTAL_CARDS_FINAL, POSSIBLE_ANSWERS_FINAL, CARD_DATA_FINAL

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
        for question in self.allQs:
            #creating the weights for each answer
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
            
            #calculate the new probabilities for each card if we add the new answer for the current question
            for card in CARD_DATA_FINAL:
                for ans in POSSIBLE_ANSWERS_FINAL:
                    newProb = BeyesCalcInst.calculateCardProb(card, len(questionList), question, ans, False)

                    entropy_map[ans] += -1 * newProb * math.log(newProb, TOTAL_CARDS_FINAL)
            
            totalEntropy = 0
            #create the weighted sum for entropy
            for key in entropy_map:
                totalEntropy += entropy_map[key] * entropy_weight_map[key]
            #print((question, totalEntropy))
            #save the question that creates the lowest entropy
            if totalEntropy < bestQuestion[1]:
                bestQuestion = (question, totalEntropy)
        self.allQs.remove(bestQuestion[0])

        print("Best question Found")

        return bestQuestion[0]