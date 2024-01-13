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
cardcsv_dataframe = cardcsv_dataframe.astype(int) #reduces memory load by converting datatype of column values into int.

TOTAL_CARDS_FINAL = len(cardcsv_dataframe.index)
TOTALS_MAP_FINAL = {ele:sum / 100 for ele, sum in zip(cardcsv_dataframe.columns, cardcsv_dataframe.sum().transpose().tolist())}
CARD_DATA_FINAL = list(cardcsv_dataframe.index)

# # import os, psutil; print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
POSSIBLE_ANSWERS_FINAL = ["YES", "NO", "MAYBE"]
QUESTION_LIMIT_FINAL = float('inf')
QUESTION_DATA_FINAL = cardcsv_dataframe.columns
print("initialization done")