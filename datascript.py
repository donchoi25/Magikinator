""" Updated Data Formatting and Question Creation Process: 

Two ways we ingest data: 
1. Locally we have a cardsdata.csv that we download from ScryFall with bulk card-data. 
   These serve as the card objects we'll compare against our questions. 
2. We fetch information from the mtg-sdk API https://docs.magicthegathering.io/ to generate
   questions, and answer these questions for each card. 
"""
import pandas as pd
import numpy as np
import json
import os.path
import csv
import operator
from datetime import date
from urllib.request import urlopen
from data.models.cardmodel import CardModel

# ====================================================================
#                       DOWNLOADING DATA
# ====================================================================

CARDDATA_JSON_FILENAME = "./data/files/cardsdata_test.json"
CARDDATA_CSV_FILENAME = "./data/files/cardsdata_test.csv"

SCRYFALL_DEFAULTCARDS_JSON_URL = "https://data.scryfall.io/default-cards/default-cards-20230830090607.json"

"""
Downloading Scryfall JSON into <CARDDATAJSON_FILENAME>
"""
def downloadDefaultCardDataFromScryfall():
    check_file = os.path.isfile(CARDDATA_JSON_FILENAME)
    if check_file:
        if not input("Are you sure you want to recreate the CARDSDATA_JSON from Scryfall? It already exists at: \n" +
               CARDDATA_JSON_FILENAME + "?: y/n ").lower() == "y":
            return
    url_response = urlopen(SCRYFALL_DEFAULTCARDS_JSON_URL)
    data = url_response.read()
    encoding = url_response.info().get_content_charset('utf-8')
    data_json = json.loads(data.decode(encoding))
    with open(CARDDATA_JSON_FILENAME, "w") as outfile:
        json.dump(data_json, outfile, indent=4)


"""
Runtime Operation to convert cardsdata.json (Scryfall) into Card Class objects
"""
def convertCardDataJsonToCards():
    list_of_cards = []
    with open(CARDDATA_JSON_FILENAME, "r") as cd:
        cards_obj_list = json.loads(cd.read())
        for card_obj in cards_obj_list:
            list_of_cards.append(Card(card_obj))
        return list_of_cards

# ====================================================================
#                       DATA FORMATTING CLASSES
# ====================================================================

"""
In memory representation of a card.
"""
class Card:
    RELEVANT_ATTRIBUTES = ['id', 'oracle_id', 'name', 
                        'released_at', 'mana_cost', 
                        'cmc', 'type_line', 'oracle_text',
                        'power', 'toughness', 'colors', 
                        'color_identity', 'keywords', 
                        'legalities', 'set', 'rarity',
                        'flavor_text']
    
    def __init__(self, card_str):
        self.id = card_str.get('id')
        self.oracle_id = card_str.get('oracle_id')
        self.name = card_str.get('name')
        self.released_at = card_str.get('released_at')
        self.mana_cost = card_str.get('mana_cost')
        self.cmc = card_str.get('cmc')
        self.type_line = card_str.get('type_line')
        self.oracle_text = card_str.get('oracle_text')
        self.power = card_str.get('power')
        self.toughness = card_str.get('toughness')
        self.colors = card_str.get('colors')
        self.color_identity = card_str.get('color_identity')
        self.keywords = card_str.get('keywords')
        self.legalities = card_str.get('legalities')
        self.set = card_str.get('set')
        self.rarity = card_str.get('rarity')
        self.flavor_text = card_str.get('flavor_text')

    def is_card_this_type(self, suspected_type):
        return suspected_type.lower() in self.type_line
    
    def is_card_this_color(self, suspected_color):
        return suspected_color in self.color_identity
    
    # Returns flat array of enumerated types
    def enumerate_attributes(self, attribute):
        if attribute == "type_line":
            return self.enumerate_all_types()
        else:
            return getattr(self, attribute)

    def enumerate_all_types(self):
        if not self.type_line:
            return []
        all_types_arr = []
        characters_to_remove = ['/', '\u2014']
        types_str = self.type_line
        for char in characters_to_remove:
            types_str = types_str.replace(char, "")
        for type in types_str.split(" "):
            all_types_arr.append(type)
        return all_types_arr

"""
Class for gathering possible questions. 
"""
class QuestionBank:

    def __init__(self):
        return
    
    """
    Generates all basic questions that can be observed on card,
    via range of possible values per attribute, based on attributes below.
    Omits columns that need additional parsing, or meta-information.
    """

    SCRYFALL_QUERYABLE_QUESTIONS_QUERY_MAP = {

    }

### Generate all MATCH QUESTIONS for Card Attributes that can be seen on the card itself.

    MATCH_COLUMNS = ["cmc", "power", "toughness",
                    "set", "rarity"]

    def generateMatchQuestionsForCardAttributes():
        map_attribute_to_range_arr = {} # column --> set(values)
        for attribute in QuestionBank.MATCH_COLUMNS:
            map_attribute_to_range_arr[attribute] = set()

        all_cards = convertCardDataJsonToCards()
        for card in all_cards:
            for attribute in QuestionBank.MATCH_COLUMNS:
                map_attribute_to_range_arr[attribute].add(str(getattr(card, attribute)))

        default_questions_str = []
        for attribute, unique_values in map_attribute_to_range_arr.items():
            for value in unique_values:
                default_questions_str.append(f'{attribute}#{value}')
        
        return default_questions_str
    
    def answerDefaultAnswersForCardAttributes():
        default_questions = QuestionBank.generateDefaultQuestionsForCardAttributes()
        all_cards = convertCardDataJsonToCards()
        question_ans_map = {} # Question (CMC#6) : { Card A : True / False, Card B: True / False, etc }
        for question in default_questions:
            question_ans_map[question] = {}
            question_attribute, question_expected_value = question.split("#")
            for card in all_cards:
                question_ans_map[question][card.name] = getattr(card, question_attribute) == question_expected_value
        return question_ans_map

### Generate All MATCH_AT_LEAST Questions for Card Attributes that need enumeration

    MATCH_AT_LEAST = ["type_line", "colors", "color_identity"]

    def generateMatchAtLeastQuestionsForCardAttributes():
        map_attribute_to_range_arr = {} # column --> set(values)
        for attribute in QuestionBank.MATCH_AT_LEAST:
            map_attribute_to_range_arr[attribute] = set()
        all_cards = convertCardDataJsonToCards()
        for card in all_cards:
            for attribute in QuestionBank.MATCH_AT_LEAST:
                attribute_value_arr = card.enumerate_attributes(attribute)
                if not attribute_value_arr:
                    continue
                for attr_val in attribute_value_arr:
                    if attr_val:
                        map_attribute_to_range_arr[attribute].add(attr_val)
        # print(map_attribute_to_range_arr)

        #         if value_set:
        #             value_set.add(str(getattr(card, attribute)))
        #         else:
        #             map_attribute_to_range_arr[attribute] = set()
        #             map_attribute_to_range_arr[attribute].add(str(getattr(card, attribute)))

        # match_at_least_questions_str = []
        # for attribute, unique_values in map_attribute_to_range_arr.items():
        #     for value in unique_values:
        #         default_questions_str.append(f'{attribute}#{value}')
        
        # return default_questions_str

# ====================================================================
#                   DATA FORMATTING AND WRITING
# ====================================================================

# ====================================================================
#                       RUNNING THIS SCRIPT
# ====================================================================

def setup():
    list_of_funcs = {
        "Redownloading Cardsdata.JSON from Scryfall": downloadDefaultCardDataFromScryfall
    }
    for file_operation, func in list_of_funcs.items():
        perform_op = (input(f'Do you want to begin {file_operation}? y/n: ')).lower() == "y"
        if perform_op:
            print(f'{file_operation}')
            func()
        else:
            print(f'SKIPPING {file_operation}...')

if __name__ == "__main__":
    # setup()
    # convertCardDataJsonToCards()
    QuestionBank.generateMatchAtLeastQuestionsForCardAttributes()