from backend import questionpicker, questionpick
from backend import answerprocessor

class FrontEnd:
    def __init__(self):
        self.questionPicker = questionpick.QuestionPick()
        self.answerProcessor = answerprocessor.AnswerProcessor()
        self.questionList = []
        self.ansList = []

    def askQuestion(self):
        #TODO: modify this so that we always ask the best question
        question = self.questionPicker.getBestQuestion(self.questionList, self.ansList)

        # answer = ""
        # while answer == "":
        #     answer = input("Is your card a " + question + " card?"+ " Answer yes, no, or maybe: ")
        #     if answer != "yes" and answer != "no" and answer != "maybe":
        #         answer = ""
        #         print("please give a valid answer")

        # self.ansList.append(answer)
        # self.questionList.append(question)

        # return self.answerProcessor.processAnswer(self.questionList, self.ansList)
        return question

    def findAnswer(self):
        finalAns = ""
        while finalAns == "":
            finalAns = self.askQuestion()
            break

        print("Your card is: " + str(finalAns))
