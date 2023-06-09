from backend import databaseparser as dbp, bayescalc as bc
from data import questionbank as qb

class QuestionPick():
    def __init__(self):
        self.ANSWER_CHOICES = qb.AnswerOptions.keys()
        self.database = dbp.DatabaseParser()
        self.NUMBER_TOTAL_CARDS = self.database.get_total_number_of_rows()
        # self.cardsbeyescalc = bc.BayesCalc()
        self.listOfQuestions = self.database.get_list_of_questions()
        self.getBestQuestion([], [])
    def getBestQuestion(self, questions_so_far, ans_so_far):
        bestQuestion = (None, 100)
        for question in self.listOfQuestions:
            print(question)
    

    