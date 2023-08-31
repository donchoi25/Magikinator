from .models import cardproperties as cp

QuestionMap = {
    # TODO: Pull from cardsdata_range.json and for each column, 
    # generate map between questionType and Type
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