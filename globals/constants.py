import pandas as pd

cardcsv_dataframe = pd.read_csv('./data/files/cardsdata_live.csv')

TOTAL_CARDS_FINAL = len(cardcsv_dataframe.index)
POSSIBLE_ANSWERS_FINAL = ["yes", "no", "maybe"]
QUESTION_LIMIT_FINAL = 10