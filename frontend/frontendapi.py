from backend import questionpicker
from backend import answerprocessor

class FrontEnd:
    def __init__(self):
        self.questionPicker = questionpicker.QuestionPicker()
        self.answerProcessor = answerprocessor.AnswerProcessor()

    def askQuestion(self, questionList=[], entropyVector=1):
        #use entropy calculations to determining best question
        question = self.questionPicker.getBestQuestion(questionList, entropyVector)
        return question

    def responseAnswer(self, questionList, question, answer, cachedEntropyVal):
        return self.answerProcessor.processAnswer(questionList, question, answer.upper(), cachedEntropyVal)
