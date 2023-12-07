from frontend import frontendapi
from globals.constants import cardcsv_dataframe

# Initialize the frontEnd
frontEnd = frontendapi.FrontEnd()
df = cardcsv_dataframe

def testTableForAllCards():
    questions = df.columns
    for index, card_to_search in df.iterrows():
        return
        

testTableForAllCards()

# print(cardcsv_dataframe.columns)
# print(cardcsv_dataframe.loc['Fury Sliver'])