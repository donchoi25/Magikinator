from backend import beyestheoremcalc as beyes
import math
import pandas as pd 

cardcsv_dataframe = pd.read_csv('./data/files/cardsdata_live.csv')

TOTAL_CARDS_FINAL = len(cardcsv_dataframe.index)
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
            #creating the weights for each answer
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
            
            #calculate the new probabilities for each card if we add the new answer for the current question
            for card in self.cardData:
                for ans in POSSIBLE_ANSWERS_FINAL:
                    newProb = self.beyestheoremcalc.calculateCardProb(card, questionList, ansList, question, ans)

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