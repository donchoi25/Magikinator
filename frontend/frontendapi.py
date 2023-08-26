from backend import questionpicker
from backend import answerprocessor

class FrontEnd:
    def __init__(self):
        self.questionPicker = questionpicker.QuestionPicker()
        self.answerProcessor = answerprocessor.AnswerProcessor()
        self.questionList = []
        self.ansList = []

    def askQuestion(self):
        #use entropy calculations to determing best question
        question = self.questionPicker.getBestQuestion(self.questionList, self.ansList)

        #poll answer until we get a valid answer from the user
        answer = ""
        while answer == "":
            answer = input("Is your card a " + question + " card?"+ " Answer yes, no, or maybe: ")
            if answer != "yes" and answer != "no" and answer != "maybe":
                answer = ""
                print("please give a valid answer")

        #determine if answer given gives us enough confidence to give back an answer using beyes theorem
        return self.answerProcessor.processAnswer(self.questionList, self.ansList, question, answer)

    def findAnswer(self):
        #keep asking questions until we get a valid answer back
        finalAns = ""
        while finalAns == "":
            finalAns = self.askQuestion()

        print("Your card is: " + str(finalAns))
        print("end")
