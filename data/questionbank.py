QuestionBank = [
    "black",
    "red",
    "blue",
    "white",
    "green",
    "sorcery",
    "instant",
    "creature"
]

QuestionEntropyMap = {}

def initializeEntropyMap():
    for key in QuestionBank:
        QuestionEntropyMap[key] = 0

def initializeData():
    initializeEntropyMap()