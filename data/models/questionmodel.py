from . import validator as val
from . import questiontypes as qt

class QuestionModel():
    def __init__(self, parameters):
        self.parameters = parameters
        return
    
    def get_question_validator(questionType, validAnswers):
        return val.DefaultValidator()
    
    def toString():
        return 

    
class IsQuestion(QuestionModel):
    def get_question_validator(questionType):
        if questionType == qt.QuestionTypes.IS_COLOR:
            return val.ColorValidator()
        if questionType == qt.QuestionTypes.IS_CARD_TYPE:
            return val.CardTypeValidator()
        #TODO: Add a new validator for each column in cardsdata_csv
        return val.DefaultValidator()
    
#TODO: Implementing IsOnly Questions
# like, is a card only a creature, 
# and not also an enchantment.