import pandas as pd
import numpy as np
import json
import csv

from data.questionbank import generate_all_answers, generate_all_possible_questions
from data.models.questiontypes import QuestionTypes
from data.models.cardproperties import CardTypes
from data.models.cardmodel import CardModel

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
    "type_line": QuestionTypes.IS_CARD_TYPE,
    "cmc": QuestionTypes.IS_CMC
    #TODO: Find a way to move this to the validator instead of mapping this here.
}

COLUMNS_TO_CREATE_IS_QUESTIONS = {
    'cmc', 'power', 'toughness', 'colors', 'type_line', 'set'
}


TOTAL_NUMBER_OF_CARDS = 9

"""
Converts JSON file into CSV, only including columns defined in CHOSEN_COLUMNS_FROM_CSV
"""
def create_cardsdata_csv():
    card_dataframe = pd.read_json('./data/files/cardsdata.json')
    card_dataframe.to_csv('./data/files/cardsdata_csv',
                        columns=CHOSEN_COLUMNS_FROM_CSV,
                        index=False)

def generate_all_possible_is_questions_and_flatten(range_dict):
    enumerated_range = {}
    for key, values in range_dict.items():
        all_possible_values = set()
        if key == 'type_line':
            for val in values:
                if isinstance(val, str):
                    delimiters = ["—", "//", " "]
                    for delimiter in delimiters:
                        val = " ".join(val.split(delimiter))
                    
                    for v in val.split():
                        all_possible_values.add(v)
        else:
            all_possible_values = values
        enumerated_range[key] = all_possible_values
    
    flattened_enumerated_range = []
    for col, values_arr in enumerated_range.items():
        for value in values_arr:
            if pd.isna(value):
                continue
            flattened_enumerated_range.append(f'{col}#{value}')
    
    return flattened_enumerated_range

def answer_all_possible_is_questions_for_all_cards(fe_range):
    cardsdata_df = pd.read_csv('./data/files/cardsdata_csv')
    all_cards_answers = [] # {Name, Attributes: ...}
    cur_card = 0
    for _, cardrow in cardsdata_df.iterrows():
        cur_card += 1
        if cur_card > TOTAL_NUMBER_OF_CARDS:
            break
        cards_answers = evaluate_answer_per_question(cardrow, fe_range)
        card_answers_with_answer_choices = {"Name": cardrow["name"]}
        for question, answer in cards_answers.items():
                ### LOGIC FOR WHAT INITIAL VALUES TO ADD
                card_answers_with_answer_choices[f'{question}#YES'] = 95 if answer else 5
                card_answers_with_answer_choices[f'{question}#NO'] = 5 if answer else 95
                card_answers_with_answer_choices[f'{question}#MAYBE'] = 2
        all_cards_answers.append(card_answers_with_answer_choices)
    return all_cards_answers
    
# For each value in the enumerated_range array of questions,
# we'll return True / False in an array. 
# Each card will maintain it's own rows of possible questions: True(s) / False(s)
def evaluate_answer_per_question(card, enumerated_range):
        result_answers_for_card = {}
        for question in enumerated_range:
            column_attribute, attribute_value = question.split("#")
            card_attribute_value = card[column_attribute]
            match = False
            ## If the card attribute has a NaN value, skip this and set to False
            if pd.isna(card_attribute_value):
                result_answers_for_card[question] = False
                continue
            ## Special IS_validation for certain columns
            if column_attribute == "colors":
                match = set(attribute_value).issubset(set(card_attribute_value))
            if column_attribute == "type_line":
                match = attribute_value.lower() in card_attribute_value.lower()
            else:
                match = str(attribute_value) == str(card_attribute_value)
            result_answers_for_card[question] = match
        return result_answers_for_card

def create_cardsdata_live_csv(cards_answers_arr):
    with open('./data/files/cardsdata_live.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=cards_answers_arr[0].keys())
        writer.writeheader()
        writer.writerows(cards_answers_arr)
    # test_cardsdata_live_csv()
    
def print_cardsdata_live_csv():
    cardsdata_df = pd.read_csv('./data/files/cardsdata_live.csv')
    print(cardsdata_df)


"""
Returns range of values for each column in cardsdata_csv.
For each key, return a set of all possible values found in that column.

Note: Make sure that columnData.unique().tolist is used,
      since Pandas is built on Numpy, which is not JSON serializable
"""
def spread_range_per_column():
    range_set_per_key = {}
    cardcsv_dataframe = pd.read_csv('./data/files/cardsdata_csv')
    for columnName, columnData in cardcsv_dataframe.transpose().iterrows():
        if columnName in COLUMNS_TO_CREATE_IS_QUESTIONS:
            range_set_per_key[columnName] = columnData.unique().tolist()
    # This is all the possible columns in our ultimate cardsdata_live.csv
    all_possible_questions = generate_all_possible_is_questions_and_flatten(range_set_per_key)
    cards_answers = answer_all_possible_is_questions_for_all_cards(all_possible_questions)
    create_cardsdata_live_csv(cards_answers)


spread_range_per_column()

"""
Generates a JSON file of range of values, 
found for columns in cardsdata_csv. This will be for 
generating questions in the future.
"""
def create_range_cardsdata_json():
    range_dict = spread_range_per_column()
    with open('./data/files/cardsdata_range.json', 'w') as fp:
        json.dump(range_dict, fp)

"""
Takes available questions from questionbank, and K valid answer choices and 
enumerates an csv file with K columns (per answer choice) for each question.

We map each question to a column of the cardscsv_dataframe that can answer it.
Each column has an "95% honest validator" that answers actual True or False,
for whether a card satisfies the question. 
"""
def generate_correct_answers_per_card():
    name_to_card_answer_map = {}
    cardsdata_df = pd.read_csv('./data/files/cardsdata_csv')
    cur_card = 0
    for _, cardrow in cardsdata_df.iterrows():
        cur_card += 1
        if cur_card > TOTAL_NUMBER_OF_CARDS:
            break
        card = CardModel(cardrow)
        card_answers = generate_all_answers(card)
        name_to_card_answer_map[card.name] = card_answers
    return name_to_card_answer_map

"""
Main function for generating database script.
"""

#TODO: Error handling if necessary files do not exist.
def setup():
    replace = (input("Do you want to recreate all existing data files? y/n")).lower() == "y"
    if replace:
        print("Recreating all files...")
        create_cardsdata_csv()
        print("Created cardsdata_csv successfully")
        create_range_cardsdata_json()
        print("Created range_cardsdata_json successfully")
        # create_cardsdata_live_csv()
        print("Created cardsdata_live_csv successfully")
    else:
        list_of_funcs = {
            "cardsdata.csv": create_cardsdata_csv, 
            "cardsdata_range.json": create_range_cardsdata_json, 
            "cardsdata_live.csv": create_cardsdata_live_csv
        }
        for file_name, func in list_of_funcs.items():
            csv_create = (input(f'Do you want to recreate {file_name}? y/n')).lower() == "y"
            if csv_create:
                print("Recreating cardsdata_csv...")
                func()
            else:
                print(f'Skipping recreating {file_name}...')

# setup()