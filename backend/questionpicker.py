#from data import cards as cardData
#from data import questionbank as questionData
from backend import beyestheoremcalc as beyes
import math
import pandas as pd 

cardcsv_dataframe = pd.read_csv('./data/files/cardsdata_live.csv')

MAYBE_WEIGHT_FINAL = 0.1
#TODO map this to actual value
TOTAL_CARDS_FINAL = 10
POSSIBLE_ANSWERS_FINAL = ["yes", "no", "maybe"]
class QuestionPicker:
    def __init__(self):
        self.beyestheoremcalc = beyes.BeyesTheoremCalc()
        self.cardData = cardcsv_dataframe["name"].tolist()
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
        for question in self.allQs:
            newQuestionList = list(questionList)
            newQuestionList.append(question)
            
            #creating the weights for each answer
            yesCount = cardcsv_dataframe[question + "#YES"].sum() / 100
            noCount = cardcsv_dataframe[question + "#NO"].sum() / 100

            entropy_weight_map = {
                "yes": yesCount / TOTAL_CARDS_FINAL * (1 - MAYBE_WEIGHT_FINAL),
                "no": noCount / TOTAL_CARDS_FINAL * (1 - MAYBE_WEIGHT_FINAL),
                "maybe": MAYBE_WEIGHT_FINAL
            }

            entropy_map = {
                "yes": 0,
                "no": 0,
                "maybe": 0
            }
            
            #calculate the new probabilities for each card if we add the new answer for the current question
            for card in self.cardData:
                for ans in POSSIBLE_ANSWERS_FINAL:
                    newAnsList = list(ansList)
                    newAnsList.append(ans)
                    newProb = self.beyestheoremcalc.calculateCardProb(card, newQuestionList, newAnsList)

                    entropy_map[ans] += -1 * newProb * math.log(newProb, TOTAL_CARDS_FINAL)
            
            totalEntropy = 0
            #create the weighted sum for entropy
            for key in entropy_map:
                totalEntropy += entropy_map[key] * entropy_weight_map[key]
            print((question, totalEntropy))
            #save the question that creates the lowest entropy
            if totalEntropy < bestQuestion[1]:
                bestQuestion = (question, totalEntropy)

        self.allQs.remove(bestQuestion[0])

        return bestQuestion[0]