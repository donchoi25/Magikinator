Cards = {
    "Sheoldred, the Apocalypse": {"creature", "black"},
    "Craterhoof Behemoth": {"creature", "green"},
    "Counterspell": {"instant", "blue"},
    "Gamble": {"sorcery", "red"},
    "Swords to Plowshares": {"instant", "white"}
}

CategoryCount = {}

CardProbMap = {}
TotalCards = len(Cards)

def initializeProbMap():
    for key in Cards:
        CardProbMap[key] = 1 / TotalCards

def initializeCategoryCount():
    for key in Cards:
        for category in Cards[key]:
            if category in CategoryCount:
                CategoryCount[category] += 1
            else:
                CategoryCount[category] = 1
def initializeData():
    initializeProbMap()
    initializeCategoryCount()
