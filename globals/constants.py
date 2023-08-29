import pandas as pd
import numpy as np

cardcsv_dataframe = pd.read_csv('./data/files/cardsdata_live.csv', engine="pyarrow")
cardcsv_dataframe.index = cardcsv_dataframe["Name"]
cardcsv_dataframe = cardcsv_dataframe.iloc[: , 1:]

TOTAL_CARDS_FINAL = len(cardcsv_dataframe.index)

TOTAL_PROB_VECTOR_FINAL = np.array([sum / 100 for sum in cardcsv_dataframe.sum().transpose().tolist()])

DATA_NUMPY_FINAL = cardcsv_dataframe.to_numpy()

print("initialization done")

POSSIBLE_ANSWERS_FINAL = ["YES", "NO", "MAYBE"]
QUESTION_LIMIT_FINAL = 20

CARD_DATA_FINAL = list(cardcsv_dataframe.index)
QUESTION_DATA_FINAL = list(cardcsv_dataframe.keys())

ENTROPY_WEIGHT_VECTOR_FINAL = [TOTAL_PROB_VECTOR_FINAL[i] / TOTAL_CARDS_FINAL for i in range(len(QUESTION_DATA_FINAL))]