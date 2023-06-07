import pandas as pd
import numpy as np
import json

from questionbank import generate_all_answers, generate_all_possible_questions
from models.questiontypes import QuestionTypes
from models.cardproperties import CardTypes
from models.cardmodel import CardModel

"""
HOW TO: Running this file will generate three files: 
1. cardsdata.json (which is pulled and downloaded directly from scryfall), 
2. cardsdata_csv (a condensed csv of relevant columns of cardsdata.json, defined in CHOSEN_COLUMNS), 
3. cardsdata_live.csv (the productionalized database that maps relevant questions to option choices)

This is the list of every possible key scryfall provides for every card in ./cardsdata.json

(['object', 'id', 'oracle_id', 'multiverse_ids', 'mtgo_id', 'mtgo_foil_id', 'tcgplayer_id', 
'cardmarket_id', 'name', 'lang', 'released_at', 'uri', 'scryfall_uri', 'layout', 'highres_image', 
'image_status', 'image_uris', 'mana_cost', 'cmc', 'type_line', 'oracle_text', 'power', 'toughness', 
'colors', 'color_identity', 'keywords', 'legalities', 'games', 'reserved', 'foil', 'nonfoil', 'finishes', 
'oversized', 'promo', 'reprint', 'variation', 'set_id', 'set', 'set_name', 'set_type', 'set_uri', 
'set_search_uri', 'scryfall_set_uri', 'rulings_uri', 'prints_search_uri', 'collector_number', 
'digital', 'rarity', 'flavor_text', 'card_back_id', 'artist', 'artist_ids', 'illustration_id', 
'border_color', 'frame', 'full_art', 'textless', 'booster', 'story_spotlight', 'edhrec_rank', 
'penny_rank', 'prices', 'related_uris'])
"""

def download_cardsdata_json():
    # TODO: GET request scryfall for bulk data and save it as JSON file
    return

CHOSEN_COLUMNS_FROM_CSV = ['name', 'mana_cost', 'cmc', 'type_line', 'power', 'toughness', 'colors', 'color_identity',
                     'keywords', 'set', 'flavor_text', 'edhrec_rank']

QUESTIONS_TO_COLUMNS_MAP = {
    "colors": QuestionTypes.IS_COLOR,
    "type_line": QuestionTypes.IS_CARD_TYPE
    #TODO: Find a way to move this to the validator instead of mapping this here.
}

"""
Converts JSON file into CSV, only including columns defined in CHOSEN_COLUMNS_FROM_CSV
"""
def create_cardsdata_csv():
    card_dataframe = pd.read_json('./files/cardsdata.json')
    card_dataframe.to_csv('files/cardsdata_csv',
                        columns=CHOSEN_COLUMNS_FROM_CSV,
                        index=False)

create_cardsdata_csv()

"""
Returns range of values for each column in cardsdata_csv.
For each key, return a set of all possible values found in that column.

Note: Make sure that columnData.unique().tolist is used,
      since Pandas is built on Numpy, which is not JSON serializable
"""
def spread_range_per_column():
    range_set_per_key = {}
    cardcsv_dataframe = pd.read_csv('./files/cardsdata_csv')
    for columnName, columnData in cardcsv_dataframe.transpose().iterrows():
        range_set_per_key[columnName] = columnData.unique().tolist()
    return range_set_per_key

"""
Generates a JSON file of range of values, 
found for columns in cardsdata_csv. This will be for 
generating questions in the future.
"""
def create_range_cardsdata_json():
    range_dict = spread_range_per_column()
    with open('./files/cardsdata_range.json', 'w') as fp:
        json.dump(range_dict, fp)

create_range_cardsdata_json()

"""
Takes available questions from questionbank, and K valid answer choices and 
enumerates an csv file with K columns (per answer choice) for each question.

We map each question to a column of the cardscsv_dataframe that can answer it.
Each column has an "95% honest validator" that answers actual True or False,
for whether a card satisfies the question. 
"""
def generate_correct_answers_per_card():
    name_to_card_answer_map = {}
    cardsdata_df = pd.read_csv('./files/cardsdata_csv')
    for _, cardrow in cardsdata_df.iterrows():
        card = CardModel(cardrow)
        card_answers = generate_all_answers(card)
        name_to_card_answer_map[card.name] = card_answers
    return name_to_card_answer_map

def format_csv_from_answers(card_answer_map):
    data = {}
    for card_name, card_answer_map in card_answer_map.items():
        values = card_answer_map.values()
        data[card_name] = values
    category_columns = card_answer_map.keys()
    card_df = pd.DataFrame.from_dict(data, orient='index',
                    columns=category_columns)
    
    card_df.to_csv("files/cardsdata_live.csv",)
    return

ans_dict = generate_correct_answers_per_card()
format_csv_from_answers(ans_dict)

"""
Returns the validator that returns True or False, for whether a card satisfies
a condition from within a column
"""
def return_column_validator():
    return

"""

"""