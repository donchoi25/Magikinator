import pandas as pd
from backend import beyestheoremcalc as beyes

cardcsv_dataframe = pd.read_csv('./data/files/cardsdata_live.csv')

QUESTION_LIMIT_FINAL = 10

class AnswerProcessor:
    def __init__(self):
        self.beyestheoremcalc = beyes.BeyesTheoremCalc()
        self.cardData = cardcsv_dataframe["name"].tolist()
        self.ansCount = 0
    def processAnswer(self, questionList, ansList):
        bestAns = ("Invalid", 0)
        for card in self.cardData:
            currProb = self.beyestheoremcalc.calculateCardProb(card, questionList, ansList)

            print((card, currProb))

            if currProb > bestAns[1]:
                bestAns = (card, currProb)

        self.ansCount += 1

        if bestAns[1] > 0.75 or self.ansCount > QUESTION_LIMIT_FINAL:
            return bestAns[0]
        else:
            return ""
