from .models import questionmodel as qm
from .models import questiontypes as qt
from .models import cardproperties as cp

QuestionMap = {
    # TODO: Pull from cardsdata_range.json and for each column, 
    # generate map between questionType and Type
}

# TODO: Create future nesting for this dict, to support exclusive "is only" questions.
QuestionMap = {
    #TODO: Expand for type of questions
    qt.QuestionTypes.IS_COLOR: list(cp.Colors),
    qt.QuestionTypes.IS_CARD_TYPE: list(cp.CardTypes)
}

AnswerOptions = {
    "YES": True,
    "NO": False,
    "MAYBE": None
}

CorrectnessRatioMap = {
    True: 95,
    False: 3,
    "Default": 2
}

"""
Returns a map of question to TRUE / FALSE for card
"""
def generate_all_answers(card):
    all_questions = generate_all_possible_questions()
    answers = {}
    for column_name_prefix, question_objects in all_questions.items():
        question_type = question_objects[0]
        question_subtype = question_objects[1]

        question_validator = qm.IsQuestion.get_question_validator(question_type)
        actual_value = question_validator.validate(card, question_subtype)
        for option in AnswerOptions:
            answers[column_name_prefix + f'#{option}'] = CorrectnessRatioMap["Default"]
            if option != "MAYBE":
                answers[column_name_prefix + f'#{option}'] = CorrectnessRatioMap[AnswerOptions[option] == actual_value]
    return answers

"""
Returns a list of all possible questions
"""
def generate_all_possible_questions():
    questions_dict = {}
    for question_type, subquestion_list in QuestionMap.items():
        for subquestion in subquestion_list:
            questions_dict[(f'{question_type}#{subquestion}')] = [question_type, subquestion]
    return questions_dict