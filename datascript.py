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

CARDDATA_JSON_FILENAME = "./data/files/cardsdata.json"
CARDDATA_CSV_FILENAME = "./data/files/cardsdata.csv"

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
        self.type_line = Card.enumerate_all_types(card_str.get('type_line'))
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

    def does_card_match_attribute(self, attribute, expected_value):
        if attribute == "type_line":
            return self.is_card_this_type(expected_value)
        elif attribute == "colors":
            return self.is_card_this_color(expected_value)
        elif attribute == "color_identity":
            return self.is_card_this_color_identity(expected_value)
        else:
            return False

    def is_card_this_type(self, suspected_type):
        if not self.type_line:
            return False
        return suspected_type in self.type_line
    
    def is_card_this_color(self, suspected_color):
        if not self.colors:
            return False
        return suspected_color in self.colors
    
    def is_card_this_color_identity(self, suspected_color):
        if not self.color_identity:
            return False
        return suspected_color in self.color_identity

    irrelevant_types = [
        "and", "or", "and/or", "of"
        # Go through and eliminate types that are articles
    ]

    def enumerate_all_types(types_str):
        if not types_str:
            return ""
        all_types_arr = []
        characters_to_remove = ['/', '\u2014']
        for char in characters_to_remove:
            types_str = types_str.replace(char, "")
        for type in types_str.split(" "):
            if type not in Card.irrelevant_types:
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
        default_questions = QuestionBank.generateMatchQuestionsForCardAttributes()
        all_cards = convertCardDataJsonToCards()
        question_ans_map = {} # Question (CMC#6) : { Card A : True / False, Card B: True / False, etc }
        for question in default_questions:
            question_ans_map[question] = {}
            question_attribute, question_expected_value = question.split("#")
            for card in all_cards:
                question_ans_map[question][card.name] = getattr(card, question_attribute) == question_expected_value
        return question_ans_map

### Generate All MATCH_AT_LEAST Questions for Card Attributes that need enumeration

    MATCH_AT_LEAST = ["type_line", "color_identity", "keywords"]

    def generateMatchAtLeastQuestionsForCardAttributes():
        map_attribute_to_range_arr = {} # column --> set(values)
        for attribute in QuestionBank.MATCH_AT_LEAST:
            map_attribute_to_range_arr[attribute] = set()
        all_cards = convertCardDataJsonToCards()
        for card in all_cards:
            for attribute in QuestionBank.MATCH_AT_LEAST:
                attribute_value_arr = getattr(card, attribute)
                if not attribute_value_arr:
                    continue
                for attr_val in attribute_value_arr:
                    if attr_val:
                        map_attribute_to_range_arr[attribute].add(attr_val)

        match_at_least_questions_str = []
        for attribute, unique_values in map_attribute_to_range_arr.items():
            for value in unique_values:
                match_at_least_questions_str.append(f'{attribute}#{value}')
        
        return match_at_least_questions_str
    
    def answerMatchAtLeastAnswersForCardAttributes():
        default_questions = QuestionBank.generateMatchAtLeastQuestionsForCardAttributes()
        all_cards = convertCardDataJsonToCards()
        question_ans_map = {} # Question (CMC#6) : { Card A : True / False, Card B: True / False, etc }
        for question in default_questions:
            question_ans_map[question] = {}
            question_attribute, question_expected_value = question.split("#")
            for card in all_cards:
                match = card.does_card_match_attribute(question_attribute, question_expected_value)
                question_ans_map[question][card.name] = match
                # if match:
                #     print("QUESTION: " + question)
                #     print("ATTRIBUTE: " + str(getattr(card, question_attribute)))
        return question_ans_map
    
    def write_cardsdata_live_csv():
        combined_answers = QuestionBank.answerDefaultAnswersForCardAttributes()
        match_answers = QuestionBank.answerMatchAtLeastAnswersForCardAttributes()
        all_cards = convertCardDataJsonToCards()
        combined_answers.update(match_answers)

        card_rows = []
        questions = ["Name"]
        for column in combined_answers.keys():
            questions.append(f'{column}#YES')
            questions.append(f'{column}#NO')
            questions.append(f'{column}#MAYBE')

        for card in all_cards:
            card_row = {}
            for question in combined_answers.keys():
                card_row["Name"] = card.name
                correct = combined_answers[question][card.name]
                
                card_row[f'{question}#YES'] = 95 if correct else 5
                card_row[f'{question}#NO'] = 5 if correct else 95
                card_row[f'{question}#MAYBE'] = 2

            card_rows.append(card_row)
        
        with open('./data/files/cardsdata_live.csv', 'w', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=questions)
            writer.writeheader()
            writer.writerows(card_rows)

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
    setup()
    # all_cards = convertCardDataJsonToCards()
    # QuestionBank.answerMatchAtLeastAnswersForCardAttributes()
    QuestionBank.write_cardsdata_live_csv()
