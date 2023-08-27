import pandas as pd

cardcsv_dataframe = pd.read_csv('./data/files/cardsdata_live.csv')

TOTAL_CARDS_FINAL = len(cardcsv_dataframe.index)

cardcsv_dataframe.index = cardcsv_dataframe["Name"]

cardcsv_dataframe.loc["Sum"] = cardcsv_dataframe.sum().transpose()

cardcsv_dataframe = cardcsv_dataframe.to_dict()

print("initialization done")

POSSIBLE_ANSWERS_FINAL = ["yes", "no", "maybe"]
QUESTION_LIMIT_FINAL = 10

CARD_DATA_FINAL = list(cardcsv_dataframe["Name"])[0:-1]