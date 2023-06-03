from data import cards as cardData
from data import questionbank as questionData
from backend import beyestheoremcalc as beyes
import math

YES_PROB_FINAL = .4
NO_PROB_FINAL = .4
MAYBE_PROB_FINAL = .2
TOTAL_CARDS_FINAL = cardData.TotalCards
POSSIBLE_ANSWERS_FINAL = ["yes", "no", "maybe"]
ENTROPY_WEIGHT_FINAL = {
    "yes": 0.45,
    "no": 0.45,
    "maybe": 0.10
}
class QuestionPicker:
    def __init__(self):
        self.beyestheoremcalc = beyes.BeyesTheoremCalc()
    def getBestQuestion(self, questionList, ansList):
        bestQuestion = ('invalid',100)
        for question in questionData.QuestionBank:
            newQuestionList = list(questionList)
            newQuestionList.append(question)

            entropy_map = {
                "yes": 0,
                "no": 0,
                "maybe": 0
            }
            for card in cardData.Cards:
                for ans in POSSIBLE_ANSWERS_FINAL:
                    newAnsList = list(ansList)
                    newAnsList.append(ans)
                    newProb = self.beyestheoremcalc.calculateCardProb(card, newAnsList, newQuestionList)

                    entropy_map[ans] += -1 * newProb * math.log(newProb, TOTAL_CARDS_FINAL)

            totalEntropy = 0
            for key in entropy_map:
                totalEntropy += entropy_map[key] * ENTROPY_WEIGHT_FINAL[key]
            print((question, totalEntropy))
            if totalEntropy < bestQuestion[1]:
                bestQuestion = (question, totalEntropy)
        questionData.QuestionBank.remove(bestQuestion[0])
        return bestQuestion[0]