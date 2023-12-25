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
import boto3
import operator
from datetime import date
from urllib.request import urlopen
from data.models.cardmodel import CardModel
from scryfallscript import ask_all_questions
import psutil
import math
from collections import Counter

# ====================================================================
#                       DOWNLOADING DATA
# ====================================================================

CARDDATA_JSON_FILENAME = "./data/files/cardsdata.json"
CARDDATA_CSV_FILENAME = "./data/files/cardsdata.csv"
CARDDATA_LIVE_CSV_FILENAME = "./data/files/cardsdata_live.csv"
CARDDATA_IMAGE_LIVE_CSV_FILENAME = "./data/files/cardsdata_images_live.csv"

CORRECT_VALUE = 95
INCORRECT_VALUE = 100 - CORRECT_VALUE
MAYBE_VALUE = 2


SCRYFALL_DEFAULTCARDS_JSON_URL = "https://data.scryfall.io/default-cards/default-cards-20230830090607.json"

CARD_LIMIT = 40000
ROWS_TO_WRITE_AT_A_TIME = 500

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
    list_of_cards = {}
    with open(CARDDATA_JSON_FILENAME, "r") as cd:
        cards_obj_list = json.loads(cd.read())
        for i, card_obj in enumerate(cards_obj_list):
            if i >= CARD_LIMIT:
                break
            if list_of_cards.get(card_obj.get('name')):
                original_card = list_of_cards.get(card_obj.get('name'))
                new_card = Card(card_obj)
                original_card.combine_cards(new_card)
            else:
                list_of_cards[card_obj.get('name')] = Card(card_obj)
        return list_of_cards.values()


def countNumberOfCards():
    list_of_cards = set()
    count = 0
    with open(CARDDATA_JSON_FILENAME, "r") as cd:
        cards_obj_list = json.loads(cd.read())
        for i, card_obj in enumerate(cards_obj_list):
            if card_obj.get('name') not in list_of_cards:
                count += 1
                list_of_cards.add(card_obj.get('name'))
        return len(list_of_cards)

# ====================================================================
#                       DATA FORMATTING CLASSES
# ====================================================================

"""
In memory representation of a card.
"""
class Card:    
    ATTRIBUTES_THAT_VARY_BETWEEN_PRINTINGS = [
        'rarity', #flavor_text
    ]
    
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
        self.colors = [color.lower() for color in card_str.get('colors')] if card_str.get('colors') else []
        self.color_identity = card_str.get('color_identity')
        self.keywords = list(map(lambda keyword: keyword.lower(), card_str.get('keywords')))
        self.legalities = card_str.get('legalities')
        self.image_uris = card_str.get('image_uris').get('normal') if card_str.get('image_uris') else "" 
        self.artist = [card_str.get('artist')]
        self.set = [card_str.get('set')]
        self.flavor_text = [card_str.get('flavor_text')]
        self.produced_mana = list(map(lambda keyword: keyword.lower(), card_str.get('produced_mana') if card_str.get('produced_mana') else []))
        # For rarity specifically, we want to scale the value to the # of cards printed at rare, uncommon, etc...
        self.rarity = Counter({card_str.get('rarity'): 1})

    # meld attributes that vary between printings (rarity)
    def combine_cards(self, other_card):
        for attr in Card.ATTRIBUTES_THAT_VARY_BETWEEN_PRINTINGS:
            self_attr = getattr(self, attr)
            other_attr = getattr(other_card, attr)
            self_attr += other_attr
            # print("CUR CARD: " + self.name + " OTHER CARD: " + other_card.name)
            # print(getattr(self, attr))

    def does_card_match_attribute(self, attribute, expected_value):
        if attribute == "type_line":
            return self.is_card_this_type(expected_value)
        elif attribute == "colors":
            return self.is_card_this_color(expected_value)
        elif attribute == "color_identity":
            return self.is_card_this_color_identity(expected_value)
        elif attribute == "keywords":
            return self.is_card_this_keyword(expected_value)
        elif attribute == "rarity":
            return self.is_card_this_rarity(expected_value)
        elif attribute == "set":
            return self.is_card_this_set(expected_value)
        elif attribute == "produced_mana":
            return self.is_card_produced_mana(expected_value)
        elif attribute == "artist":
            return self.is_card_by_artist(expected_value)
        elif attribute == "flavor_text":
            return self.is_card_flavor_text(expected_value)
        else:
            return False

    def is_card_flavor_text(self):
        return any(self.flavor_text)

    def is_card_this_type(self, suspected_type):
        if not self.type_line:
            return False
        return suspected_type.lower() in self.type_line
    
    def is_card_this_color(self, suspected_color):
        if not self.colors:
            return False
        return suspected_color.lower() in self.colors
    
    def is_card_this_color_identity(self, suspected_color):
        if not self.color_identity:
            return False
        return suspected_color.lower() in self.color_identity
    
    def is_card_this_keyword(self, suspected_keyword):
        if not self.keywords:
            return False
        return suspected_keyword.lower() in self.keywords

    def is_card_this_rarity(self, suspected_rarity):
        if not self.rarity:
            return False
        return suspected_rarity in self.rarity
    
    def is_card_this_set(self, suspected_set):
        if not self.set:
            return False
        return suspected_set in self.set
    
    def is_card_produced_mana(self, suspected_mana):
        if not self.produced_mana:
            return False
        return suspected_mana.lower() in self.produced_mana

    def is_card_by_artist(self, suspected_artist):
        if not suspected_artist:
            return False
        return suspected_artist in self.artist

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

    RELEVANT_ATTRIBUTES = ['id', 'oracle_id', 'name', 
                    'released_at', 'mana_cost', 
                    'cmc', 'type_line', 'oracle_text',
                    'power', 'toughness', 'colors',
                    'color_identity', 'keywords', 
                    'legalities', 'set', 'rarity',
                    'artist', 'flavor_text', 'produced_mana']

### Generate all MATCH QUESTIONS for Card Attributes that can be seen on the card itself.
    MATCH_COLUMNS = ["power", "toughness", "cmc", "mana_cost"]

### Generate All MATCH_AT_LEAST Questions for Card Attributes that need enumeration
    MATCH_AT_LEAST = ["type_line", "color_identity", "keywords", "rarity"]

### Generate All Questions for Card Attributes that vary between printings
    MATCH_COLUMNS_VARY_PRINTINGS = ["rarity"]
    
    def generateMatchQuestionsForCardAttributes(all_cards):
        map_attribute_to_range_arr = {} # column --> set(values)
        for attribute in QuestionBank.MATCH_COLUMNS:
            map_attribute_to_range_arr[attribute] = set()
        for card in all_cards:
            for attribute in QuestionBank.MATCH_COLUMNS:
                attr = getattr(card, attribute)
                if attr:
                    map_attribute_to_range_arr[attribute].add(str(attr))

        default_questions_str = []
        for attribute, unique_values in map_attribute_to_range_arr.items():
            for value in unique_values:
                default_questions_str.append(f'{attribute}@{value}')
        
        return default_questions_str
    
    def generateMatchAtLeastQuestionsForCardAttributes(all_cards):
        map_attribute_to_range_arr = {} # column --> set(values)
        for attribute in QuestionBank.MATCH_AT_LEAST:
            map_attribute_to_range_arr[attribute] = set()
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
                match_at_least_questions_str.append(f'{attribute}@{value}')
        
        return match_at_least_questions_str

    def generateQuestionsForCardAttributes(all_cards):
        map_attribute_to_range_arr = {} # column --> set(values)
        for attribute in QuestionBank.MATCH_COLUMNS:
            map_attribute_to_range_arr[attribute] = set()
        for attribute in QuestionBank.MATCH_AT_LEAST:
            map_attribute_to_range_arr[attribute] = set()
        for card in all_cards:
            for attribute in QuestionBank.MATCH_COLUMNS:
                attr = getattr(card, attribute)
                if attr:
                    map_attribute_to_range_arr[attribute].add(str(attr))
            for attribute in QuestionBank.MATCH_AT_LEAST:
                attribute_value_arr = getattr(card, attribute)
                if not attribute_value_arr:
                    continue
                for attr_val in attribute_value_arr:
                    if attr_val:
                        map_attribute_to_range_arr[attribute].add(attr_val)

        questions_arr = []
        for attribute, unique_values in map_attribute_to_range_arr.items():
            for value in unique_values:
                questions_arr.append(f'{attribute}@{value}')
        
        return questions_arr
    
    def write_cardsdata_live_csv():
        if os.path.exists(CARDDATA_LIVE_CSV_FILENAME):
            os.remove(CARDDATA_LIVE_CSV_FILENAME)
            print("Deleting and recreating " + CARDDATA_LIVE_CSV_FILENAME)
        else:
            print(CARDDATA_LIVE_CSV_FILENAME + " did not exist. Creating it now.")
        all_cards = convertCardDataJsonToCards()
        all_questions = QuestionBank.generateQuestionsForCardAttributes(all_cards)
        question_column_fields = ["Name"]
        for question in all_questions:
            question_column_fields.append(f'{question}#YES')
            question_column_fields.append(f'{question}#NO')
            question_column_fields.append(f'{question}#MAYBE')
        
        print("Generated all questions!")
        scryfall_questions_map = ask_all_questions()
        for scry_q in scryfall_questions_map.keys():
            question_column_fields.append(f'{scry_q}#YES')
            question_column_fields.append(f'{scry_q}#NO')
            question_column_fields.append(f'{scry_q}#MAYBE')
        print("Generated all scryfall questions!")
        
        with open(CARDDATA_LIVE_CSV_FILENAME, 'a', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=question_column_fields)
            writer.writeheader()
            card_rows = []
            for card in all_cards:
                card_row = {}
                card_row["Name"] = card.name
                for question in all_questions:
                    question_attribute, question_expected_value = question.split("@")
                    attr = getattr(card, question_attribute)
                    correct = False
                    if attr:
                        if question_attribute in QuestionBank.MATCH_COLUMNS:
                            correct = str(attr).lower() == str(question_expected_value).lower()
                        elif question_attribute in QuestionBank.MATCH_AT_LEAST:
                            correct = card.does_card_match_attribute(question_attribute, question_expected_value)

                    # For Rarity
                    if question_attribute in Card.ATTRIBUTES_THAT_VARY_BETWEEN_PRINTINGS:
                        scaled_correct_value = int((attr[question_expected_value] / sum(attr.values())) * 100)
                        scaled_incorrect_value = 100 - scaled_correct_value
                        card_row[f'{question}#YES'] = scaled_correct_value if correct else scaled_incorrect_value
                        card_row[f'{question}#NO'] = scaled_incorrect_value if correct else scaled_correct_value
                        card_row[f'{question}#MAYBE'] = MAYBE_VALUE
                    else:
                        card_row[f'{question}#YES'] = CORRECT_VALUE if correct else INCORRECT_VALUE
                        card_row[f'{question}#NO'] = INCORRECT_VALUE if correct else CORRECT_VALUE
                        card_row[f'{question}#MAYBE'] = MAYBE_VALUE

                for question, cards in scryfall_questions_map.items():
                    correct = card.name.lower() in cards

                    card_row[f'{question}#YES'] = CORRECT_VALUE if correct else INCORRECT_VALUE
                    card_row[f'{question}#NO'] = INCORRECT_VALUE if correct else CORRECT_VALUE
                    card_row[f'{question}#MAYBE'] = MAYBE_VALUE

                card_rows.append(card_row)
                if len(card_rows) > ROWS_TO_WRITE_AT_A_TIME:
                    writer.writerows(card_rows)
                    print(f'Wrote {ROWS_TO_WRITE_AT_A_TIME} rows to files/cardsdata_live.csv')
                    card_rows = []

            print("Writing last cards to cardsdata_live.csv")
            writer.writerows(card_rows)
            csvfile.close()

    def upload_cardsdata_live_s3():
        s3 = boto3.resource('s3')
        BUCKET = "magikinator"
        s3.Bucket(BUCKET).upload_file(CARDDATA_LIVE_CSV_FILENAME, 'cardsdata_live.csv')

    def write_cardsimages_live_csv():
        print("Creating List of images for all cards")
        if os.path.exists(CARDDATA_IMAGE_LIVE_CSV_FILENAME):
            os.remove(CARDDATA_IMAGE_LIVE_CSV_FILENAME)
            print("Deleting and recreating " + CARDDATA_IMAGE_LIVE_CSV_FILENAME)
        else:
            print(CARDDATA_IMAGE_LIVE_CSV_FILENAME + " did not exist. Creating it now.")

        all_cards = convertCardDataJsonToCards()
        with open(CARDDATA_IMAGE_LIVE_CSV_FILENAME, 'a', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["Name", "Image_URL"])
            writer.writeheader()
            card_rows = []
            for card in all_cards:
                card_row = {}
                card_row["Name"] = card.name
                card_row["Image_URL"] = card.image_uris
                card_rows.append(card_row)
                if len(card_rows) > ROWS_TO_WRITE_AT_A_TIME:
                    writer.writerows(card_rows)
                    print(f'Wrote {ROWS_TO_WRITE_AT_A_TIME} rows to files/cardsdata_images_live.csv')
                    card_rows = []
            print("Writing last card images to cardsdata_images_live.csv")
            writer.writerows(card_rows)
            csvfile.close()


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

# setup()
QuestionBank.write_cardsdata_live_csv()
# QuestionBank.upload_cardsdata_live_s3()
