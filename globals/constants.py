import pandas as pd
from multiprocessing import current_process

cardcsv_dataframe = {}
if current_process().name == 'MainProcess':
    cardcsv_dataframe = pd.read_csv('./data/files/cardsdata_live.csv')

    cardcsv_dataframe.index = cardcsv_dataframe["Name"]

    cardcsv_dataframe.loc["Sum"] = cardcsv_dataframe.sum().transpose()

    cardcsv_dataframe = cardcsv_dataframe.to_dict()

    print("initialization done")

#TOTAL_CARDS_FINAL = len(cardcsv_dataframe["Name"])

POSSIBLE_ANSWERS_FINAL = ["yes", "no", "maybe"]
QUESTION_LIMIT_FINAL = 10

#CARD_DATA_FINAL = list(cardcsv_dataframe["Name"])[0:-1]