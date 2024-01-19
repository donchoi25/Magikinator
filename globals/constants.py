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

# can we store this in a postgresql database
CHUNKSIZE=500
TOTAL_CARDS_FINAL = 0
TOTALS_MAP_FINAL = {}
CARD_DATA_COLUMNS = {}
CARD_DATA_FINAL = []
POSSIBLE_ANSWERS_FINAL = ["YES", "NO", "MAYBE"]
QUESTION_LIMIT_FINAL = float('inf')
QUESTION_DATA_FINAL = None
with pd.read_csv('./data/files/cardsdata_live.csv', chunksize=CHUNKSIZE) as reader:
    for chunk in reader:
        CARD_DATA_FINAL += list(chunk['Name'])
        chunk = chunk.iloc[: , 1:]
        QUESTION_DATA_FINAL = chunk.columns
        TOTAL_CARDS_FINAL += len(chunk)
        for col in chunk:
            if not TOTALS_MAP_FINAL.get(col):
                TOTALS_MAP_FINAL[col] = int(chunk[col].sum()) / 100
            else:
                TOTALS_MAP_FINAL[col] += int(chunk[col].sum()) / 100
            
            chunkvalues = chunk[col].values.tolist()
            if not CARD_DATA_COLUMNS.get(col):
                CARD_DATA_COLUMNS[col] = chunkvalues
            else:
                CARD_DATA_COLUMNS[col] += chunkvalues

# print(TOTALS_MAP_FINAL)
# print(QUESTION_COLUMNS)
# print(CARD_DATA_FINAL)
# print(list(CARD_DATA_COLUMNS.values())[0])

# cardcsv_dataframe = pd.read_csv('./data/files/cardsdata_live.csv')
# cardcsv_dataframe.index = cardcsv_dataframe["Name"]
# cardcsv_dataframe = cardcsv_dataframe.iloc[: , 1:]
# cardcsv_dataframe = cardcsv_dataframe.astype(int) #reduces memory load by converting datatype of column values into int.

# TOTAL_CARDS_FINAL = len(cardcsv_dataframe.index)
# Total number of YES/NO/MAYBE for each question
# TOTALS_MAP_FINAL = {ele:sum / 100 for ele, sum in zip(cardcsv_dataframe.columns, cardcsv_dataframe.sum().transpose().tolist())}

import os, psutil; print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
# print("initialization done")
