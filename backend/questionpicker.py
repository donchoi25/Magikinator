from data import cards as cardData
from data import questionbank as questionData
from backend import beyestheoremcalc as beyes
import math

MAYBE_WEIGHT_FINAL = 0.1
TOTAL_CARDS_FINAL = cardData.TotalCards
POSSIBLE_ANSWERS_FINAL = ["yes", "no", "maybe"]
class QuestionPicker:
    def __init__(self):
        self.beyestheoremcalc = beyes.BeyesTheoremCalc()
    def getBestQuestion(self, questionList, ansList):
        bestQuestion = ('invalid',100)
        for question in questionData.QuestionBank:
            newQuestionList = list(questionList)
            newQuestionList.append(question)

            entropy_weight_map = {
                "yes": cardData.CategoryCount[question] / TOTAL_CARDS_FINAL * (1 - MAYBE_WEIGHT_FINAL),
                "no": (TOTAL_CARDS_FINAL - cardData.CategoryCount[question]) / TOTAL_CARDS_FINAL * (1 - MAYBE_WEIGHT_FINAL),
                "maybe": MAYBE_WEIGHT_FINAL
            }

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
                totalEntropy += entropy_map[key] * entropy_weight_map[key]
            print((question, totalEntropy))
            if totalEntropy < bestQuestion[1]:
                bestQuestion = (question, totalEntropy)
        questionData.QuestionBank.remove(bestQuestion[0])
        return bestQuestion[0]
