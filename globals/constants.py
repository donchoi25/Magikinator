import pandas as pd

cardcsv_dataframe = pd.read_csv('./data/files/cardsdata_live.csv', engine="pyarrow")
cardcsv_dataframe.index = cardcsv_dataframe["Name"]
cardcsv_dataframe = cardcsv_dataframe.iloc[: , 1:]

TOTAL_CARDS_FINAL = len(cardcsv_dataframe.index)

TOTALS_MAP_FINAL = {ele:sum / 100 for ele, sum in zip(cardcsv_dataframe.columns, cardcsv_dataframe.sum().transpose().tolist())}

COL_NUMPY_DICT_FINAL = {ques:cardcsv_dataframe[ques].to_numpy() / 100 for ques in cardcsv_dataframe.columns}

CARD_DATA_FINAL = list(cardcsv_dataframe.index)

POSSIBLE_ANSWERS_FINAL = ["YES", "NO", "MAYBE"]
QUESTION_LIMIT_FINAL = 10
QUESTION_DATA_FINAL = cardcsv_dataframe.columns

print("initialization done")