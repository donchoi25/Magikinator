from data import cards as data
from backend import beyestheoremcalc as beyes
from data import questionbank as questionData

class AnswerProcessor:
    def __init__(self):
        self.beyestheoremcalc = beyes.BeyesTheoremCalc()
    def processAnswer(self, questionList, ansList):
        bestAns = ("Invalid", 0)
        for card in data.Cards:
            currProb = self.beyestheoremcalc.calculateCardProb(card, ansList, questionList)

            print((card, currProb))

            if currProb > bestAns[1]:
                bestAns = (card, currProb)

        if bestAns[1] > 0.9 or len(questionData.QuestionBank) == 0:
            return bestAns[0]
        else:
            return ""