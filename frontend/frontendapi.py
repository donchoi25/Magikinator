from backend import questionpicker
from backend import answerprocessor

class FrontEnd:
    def __init__(self):
        self.questionPicker = questionpicker.QuestionPicker()
        self.answerProcessor = answerprocessor.AnswerProcessor()
        self.questionList = []
        self.ansList = []

    def askQuestion(self):
        question = self.questionPicker.getBestQuestion(self.questionList, self.ansList)

        answer = ""
        while answer == "":
            answer = input("Is your card a " + question + " card?"+ " Answer yes, no, or maybe: ")
            if answer != "yes" and answer != "no" and answer != "maybe":
                answer = ""
                print("please give a valid answer")

        return self.answerProcessor.processAnswer(self.questionList, self.ansList, question, answer)

    def findAnswer(self):
        finalAns = ""
        while finalAns == "":
            finalAns = self.askQuestion()

        print("Your card is: " + str(finalAns))
        print("end")
