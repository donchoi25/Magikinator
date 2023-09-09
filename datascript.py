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
from scryfallscript import ask_all_questions

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
    list_of_cards = {}
    limit = 10
    i = 0
    with open(CARDDATA_JSON_FILENAME, "r") as cd:
        cards_obj_list = json.loads(cd.read())
        for card_obj in cards_obj_list:
            i += 1
            if i > limit:
                break
            # if (card_obj.get('name') == 'Cyclonic Rift' or card_obj.get('name') == 'Mission Briefing'):
            if list_of_cards.get(card_obj.get('name')):
                original_card = list_of_cards.get(card_obj.get('name'))
                new_card = Card(card_obj)
                original_card.combine_cards(new_card)
            else:
                list_of_cards[card_obj.get('name')] = Card(card_obj)
        return list_of_cards.values()

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
    
    ATTRIBUTES_THAT_VARY_BETWEEN_PRINTINGS = [
        'set', 'rarity'
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
        self.colors = card_str.get('colors')
        self.color_identity = card_str.get('color_identity')
        self.keywords = card_str.get('keywords')
        self.legalities = card_str.get('legalities')
        self.produced_mana = card_str.get('produced_mana')
        self.set = [card_str.get('set')]
        self.rarity = [card_str.get('rarity')]
        self.flavor_text = [card_str.get('flavor_text')]

    # meld attributes that vary between printings
    
    def combine_cards(self, other_card):
        for attr in Card.ATTRIBUTES_THAT_VARY_BETWEEN_PRINTINGS:
            self_attr = getattr(self, attr)
            other_attr = getattr(other_card, attr)
            for val in other_attr:
                if val not in self_attr:
                    self_attr.append(val)
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
        elif attribute== "produced_mana":
            return self.is_card_produced_mana(expected_value)
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
    
    def is_card_this_keyword(self, suspected_keyword):
        if not self.keywords:
            return False
        match = suspected_keyword in self.keywords
        # if match:
        #     print("SUSPECTED KEYWORD: " + suspected_keyword)
        #     print(self.keywords)
        return match

    
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
        return suspected_mana in self.produced_mana

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

    MATCH_COLUMNS = ["cmc", "power", "toughness", "mana_cost"]
    # Add colors, but make this only exactly the case

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
    
    def answerDefaultAnswersForCardAttributes(all_cards):
        default_questions = QuestionBank.generateMatchQuestionsForCardAttributes(all_cards)
        question_ans_map = {} # Question (CMC#6) : { Card A : True / False, Card B: True / False, etc }
        for question in default_questions:
            question_ans_map[question] = {}
            question_attribute, question_expected_value = question.split("@")
            for card in all_cards:
                attr = getattr(card, question_attribute)
                if attr:
                    question_ans_map[question][card.name] = str(attr) == str(question_expected_value)
                else:
                    question_ans_map[question][card.name] = False
        return question_ans_map

### Generate All MATCH_AT_LEAST Questions for Card Attributes that need enumeration

    MATCH_AT_LEAST = ["type_line", "color_identity", "keywords", "set", "rarity", "produced_mana"]

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
    
    def answerMatchAtLeastAnswersForCardAttributes(all_cards):
        default_questions = QuestionBank.generateMatchAtLeastQuestionsForCardAttributes(all_cards)
        question_ans_map = {} # Question (CMC#6) : { Card A : True / False, Card B: True / False, etc }
        for question in default_questions:
            question_ans_map[question] = {}
            question_attribute, question_expected_value = question.split("@")
            for card in all_cards:
                match = card.does_card_match_attribute(question_attribute, question_expected_value)
                question_ans_map[question][card.name] = match
                # if match:
                #     print("QUESTION: " + question)
                #     print("ATTRIBUTE: " + str(getattr(card, question_attribute)))
        return question_ans_map
    
    def write_cardsdata_live_csv():
        all_cards = convertCardDataJsonToCards()
        combined_answers = QuestionBank.answerDefaultAnswersForCardAttributes(all_cards)
        match_answers = QuestionBank.answerMatchAtLeastAnswersForCardAttributes(all_cards)
        combined_answers.update(match_answers)

        card_rows = []
        questions = ["Name"]
        for column in combined_answers.keys():
            questions.append(f'{column}#YES')
            questions.append(f'{column}#NO')
            questions.append(f'{column}#MAYBE')

        # SCRYFALL QUESTIONS
        print("ASKING SCRYFALL QUESTIONS")
        scryfall_answers = ask_all_questions()
        print("DONE ASKING SCRYFALL QUESTIONS")
        for scry_q in scryfall_answers.keys():
            questions.append(f'{scry_q}#YES')
            questions.append(f'{scry_q}#NO')
            questions.append(f'{scry_q}#MAYBE')

        for card in all_cards:
            card_row = {}
            card_row["Name"] = card.name
            for question in combined_answers.keys():
                correct = combined_answers[question][card.name]
                
                if question == "set":
                    card_row[f'{question}#YES'] = 95 / len(getattr(card, 'set')) if correct else (100 - (95 / len(getattr(card, 'set'))))
                    card_row[f'{question}#NO'] = (100 - (95 / len(getattr(card, 'set')))) if correct else 95 / len(getattr(card, 'set'))
                    card_row[f'{question}#MAYBE'] = 2
                else:
                    card_row[f'{question}#YES'] = 95 if correct else 5
                    card_row[f'{question}#NO'] = 5 if correct else 95
                    card_row[f'{question}#MAYBE'] = 2

            for question, cards in scryfall_answers.items():
                # print("QUESTION: " + question)
                # print("CARDS: " + str(cards))
                correct = card.name.lower() in cards
                # if correct:
                    # print("CARD NAME: " + card.name + " Question: " + question)
                card_row[f'{question}##YES'] = 95 if correct else 5
                card_row[f'{question}##NO'] = 5 if correct else 95
                card_row[f'{question}##MAYBE'] = 2

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
    # setup()
    # all_cards = convertCardDataJsonToCards()
    # QuestionBank.answerMatchAtLeastAnswersForCardAttributes()
    QuestionBank.write_cardsdata_live_csv()
