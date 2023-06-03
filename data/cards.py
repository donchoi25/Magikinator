Cards = {
    "Sheoldred, the Apocalypse": {"creature", "black"},
    "Sheoldred, the Apocalypse1": {"creature", "black"},
    "Sheoldred, the Apocalypse2": {"creature", "black"},
    "Craterhoof Behemoth": {"creature", "green"},
    "Craterhoof Behemoth1": {"creature", "green"},
    "Craterhoof Behemoth2": {"creature", "green"},
    "Craterhoof Behemoth3": {"creature", "green"},
    "Counterspell": {"instant", "blue"},
    "Counterspell1": {"instant", "blue"},
    "Counterspell2": {"instant", "blue"},
    "Counterspell3": {"instant", "blue"},
    "Gamble": {"sorcery", "red"},
    "Gamble1": {"sorcery", "red"},
    "Swords to Plowshares": {"instant", "white"},
    "Swords to Plowshares1": {"instant", "white"},
    "Swords to Plowshares2": {"instant", "white"},
    "Swords to Plowshares3": {"instant", "white"},
    "Swords to Plowshares4": {"instant", "white"},
    "Swords to Plowshares5": {"instant", "white"},
    "Swords to Plowshares6": {"instant", "white"},
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