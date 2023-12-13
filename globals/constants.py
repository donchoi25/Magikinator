import pandas as pd
import boto3
import botocore

# BUCKET_NAME = 'magikinator'
# KEY = 'cardsdata_live.csv'
# PATH_TO_DOWNLOAD_TO = 'data/files/cardsdata_live.csv'

# try:
#     s3 = boto3.resource('s3')
#     s3.Bucket(BUCKET_NAME).download_file(KEY, PATH_TO_DOWNLOAD_TO)
# except botocore.exceptions.ClientError as e:
#     if e.response['Error']['Code'] == "404":
#         print("The object does not exist.")
#     else:
#         raise

cardcsv_dataframe = pd.read_csv('./data/files/cardsdata_live.csv')
cardcsv_dataframe.index = cardcsv_dataframe["Name"]
cardcsv_dataframe = cardcsv_dataframe.iloc[: , 1:]

TOTAL_CARDS_FINAL = len(cardcsv_dataframe.index)

TOTALS_MAP_FINAL = {ele:sum / 100 for ele, sum in zip(cardcsv_dataframe.columns, cardcsv_dataframe.sum().transpose().tolist())}
# for elem, sum in zip(cardcsv_dataframe.columns, cardcsv_dataframe.sum().transpose().tolist()):
#     print(elem, sum)
# print(TOTALS_MAP_FINAL)

# Column of question
COL_NUMPY_DICT_FINAL = {ques:cardcsv_dataframe[ques].to_numpy() / 100 for ques in cardcsv_dataframe.columns}

CARD_DATA_FINAL = list(cardcsv_dataframe.index)

POSSIBLE_ANSWERS_FINAL = ["YES", "NO", "MAYBE"]
QUESTION_LIMIT_FINAL = float('inf')
QUESTION_DATA_FINAL = cardcsv_dataframe.columns

print("initialization done")