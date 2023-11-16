import pymongo as pm
import json

client = pm.MongoClient("mongodb://localhost:27017/")
cardsdb = client["magikinator"]
collection = cardsdb.cards

with open('data/files/cardsdata.json') as file:
    file_data = json.load(file)
    collection.insert_many(file_data)

