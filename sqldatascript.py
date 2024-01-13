import psycopg2 as psy
import psycopg2.extras
import psycopg2.sql as sql
from psycopg2 import Error
import os.path
from urllib.request import urlopen
import json
import csv
from scryfallscript import ask_all_questions

CARDDATA_JSON_FILENAME = "./data/files/cardsdata.json"
SCRYFALL_DEFAULTCARDS_JSON_URL = "https://data.scryfall.io/default-cards/default-cards-20230830090607.json"
CARDSDATA_LIVE_FILENAME = "./data/files/cardsdata_live.csv"

def create_connection(database_name=""):
    try:
        conn = psy.connect(
            host="127.0.0.1",
            user="postgres",
            password="master123",
            database=database_name
        )

        conn.autocommit = True
        return conn
    except(Exception, Error) as error:
        print("Error while creating connection to PostgreSQL: ", error)

def login_user_create_database():
    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE magikinator")
    except(Exception, psy.errors.DuplicateDatabase) as error:
        print(error)
    finally:
        if conn:
            cursor.close()
            conn.close()
    

def create_table():
    commands = (
        """
        DROP TABLE IF EXISTS Cards;
        """,
        """
        CREATE TABLE IF NOT EXISTS Cards (
            name TEXT PRIMARY KEY,
            released_at TEXT,
            mana_cost TEXT,
            cmc TEXT,
            type_line TEXT,
            oracle_text TEXT,
            power TEXT,
            toughness TEXT,
            colors TEXT,
            color_identity TEXT,
            flavor_text TEXT,
            keywords TEXT,
            set TEXT,
            rarity TEXT,
            artist TEXT
        )
        """,
    )
    conn = None
    try:
        conn = create_connection("magikinator")
        cursor = conn.cursor()
        for command in commands:
            cursor.execute(command)
        print("Successfully created tables Cards and Questions")
        conn.commit()
    except (Exception, psy.errors.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            cursor.close()
            conn.close()

class CardModel:
    RELEVANT_ATTRIBUTES = ['name', 'released_at', 'mana_cost', 
                        'cmc', 'type_line', 'oracle_text',
                        'power', 'toughness', 'colors', 
                        'color_identity', 'keywords', 
                        'set', 'rarity', 'artist', 'flavor_text']

    ATTRIBUTE_TYPING_MAP = {
        "name": str,
        "released_at": str,
        "mana_cost": str,
        "cmc": str,
        "type_line": str,
        "oracle_text": str,
        "power": str,
        "toughness": str,
        "colors": str,
        "color_identity": str,
        "keywords": str,
        "set": str,
        "rarity": str,
        "artist": str,
        "flavor_text": str
    }
    
    def printRelevantAttributes():
        return ", ".join(CardModel.RELEVANT_ATTRIBUTES)

    def getRelevantAttributes(self):
        return ", ".join(["%s" for attr in CardModel.RELEVANT_ATTRIBUTES])
            
    def getSelfAttributesValues(self):
        return [getattr(self, attr) for attr in CardModel.RELEVANT_ATTRIBUTES]
    
    ATTRIBUTES_THAT_VARY_BETWEEN_PRINTINGS = [
        'set', 'rarity'
    ]
    
    def __init__(self, card_str):
        self.id = card_str.get('id')
        self.oracle_id = card_str.get('oracle_id')
        self.name = card_str.get('name')
        self.released_at = card_str.get('released_at')
        self.mana_cost = str(card_str.get('mana_cost'))
        self.cmc = str(card_str.get('cmc'))
        self.type_line = CardModel.enumerate_all_types(card_str.get('type_line'))
        self.oracle_text = card_str.get('oracle_text')
        self.power = str(card_str.get('power'))
        self.toughness = str(card_str.get('toughness'))
        self.colors = card_str.get('colors')
        self.color_identity = card_str.get('color_identity')
        self.keywords = card_str.get('keywords')
        self.produced_mana = card_str.get('produced_mana')
        self.artist = [card_str.get('artist')]
        self.set = [card_str.get('set')]
        self.rarity = [card_str.get('rarity')]
        self.flavor_text = [card_str.get('flavor_text')]

# meld attributes that vary between printings
    
    def combine_cards(self, other_card):
        for attr in CardModel.ATTRIBUTES_THAT_VARY_BETWEEN_PRINTINGS:
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
        elif attribute == "produced_mana":
            return self.is_card_produced_mana(expected_value)
        elif attribute == "artist":
            return self.is_card_by_artist(expected_value)
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
            if type not in CardModel.irrelevant_types:
                all_types_arr.append(type)
        return "_".join(all_types_arr)

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
    all_cards_combined = {}
    combined = 0
    for card_data_json in data_json:
        cardModel = CardModel(card_data_json)
        if all_cards_combined.get(cardModel.name):
            all_cards_combined.get(cardModel.name).combine_cards(cardModel)
            combined += 1
        else:
            all_cards_combined[cardModel.name] = cardModel
    
    print("FINISHED Combining Card Models")
    for card in all_cards_combined.values():
        insert_card_sql(card)
    
    print("Added all cards into postgres table")

def insert_card_sql(cardModel):
    INSERT_COMMAND = f"""
    INSERT INTO cards ({CardModel.printRelevantAttributes()}) VALUES ({cardModel.getRelevantAttributes()})"""
    conn = None
    try:
        conn = create_connection("magikinator")
        cursor = conn.cursor()
        cursor.execute(INSERT_COMMAND, cardModel.getSelfAttributesValues())
        conn.commit()
    except (Exception, psy.errors.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            cursor.close()
            conn.close()

def fetch_all_cards():
    FETCH_COMMAND = f"""
    SELECT * FROM Cards"""
    conn = None
    data_records = None
    dict_data_records = []
    cur = None
    try:
        conn = create_connection("magikinator")
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(FETCH_COMMAND)
        data_records = cur.fetchall()
        for row in data_records:
            dict_data_records.append(dict(row))
        print("Data has been fetched successfully from Cards Table")
        conn.commit()
    except (Exception, psy.errors.DatabaseError) as error:
        print(error)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    
    return dict_data_records

def fetch_all_cards_as_cardobjects():
    all_cards = fetch_all_cards()
    card_objects = []
    for card in all_cards:
        card_objects.append(CardModel(card))
    print("Fetched :" + str(len(card_objects)) + " cards as card objects.")
    return card_objects



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

### Generate All MATCH_AT_LEAST Questions for Card Attributes that need enumeration
    MATCH_AT_LEAST = ["type_line", "color_identity", "keywords", "set", "rarity", "produced_mana", "artist"]
    
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
    
    def answerQuestionsForCardAttributes():
        all_cards = fetch_all_cards_as_cardobjects() #TODO
        print("Finished fetching all cards as data objects.")
        all_questions = QuestionBank.generateQuestionsForCardAttributes(all_cards)
        print("Finished generating all possible questions for all cards.")

        # TODO: Create table to hold cardsdata_live

        card_rows = []
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
        print("Generated all Scryfall questions!")

        question_column_fields
        index = 0
        for card in all_cards:
            print(index)
            index += 1
            card_row = {}
            card_row["Name"] = card.name
            for question in all_questions:
                question_attribute, question_expected_value = question.split("@")
                attr = getattr(card, question_attribute)
                correct = False
                if attr:
                    if question_attribute in QuestionBank.MATCH_COLUMNS:
                        correct = str(attr) == str(question_expected_value)
                    elif question_attribute in QuestionBank.MATCH_AT_LEAST:
                        correct = card.does_card_match_attribute(question_attribute, question_expected_value)
                
                if question == "set" or question == "rarity":
                    card_row[f'{question}#YES'] = 95 / len(getattr(card, question)) if correct else (100 - (95 / len(getattr(card, question))))
                    card_row[f'{question}#NO'] = (100 - (95 / len(getattr(card, question)))) if correct else 95 / len(getattr(card, question))
                    card_row[f'{question}#MAYBE'] = 2

                else:
                    card_row[f'{question}#YES'] = 95 if correct else 5
                    card_row[f'{question}#NO'] = 5 if correct else 95
                    card_row[f'{question}#MAYBE'] = 2
            
            for question, cards in scryfall_questions_map.items():
                correct = card.name.lower() in cards

                card_row[f'{question}#YES'] = 95 if correct else 5
                card_row[f'{question}#NO'] = 5 if correct else 95
                card_row[f'{question}#MAYBE'] = 2
            
            # Write card-question row direction in PSQL right here

            card_rows.append(card_row)
        
        with open('./data/files/cardsdata_live.csv', 'w', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=question_column_fields)
            writer.writeheader()
            writer.writerows(card_rows)
    
    def create_cardsdatalive_table():
        all_cards = fetch_all_cards_as_cardobjects() #TODO
        print("Finished fetching all cards as data objects.")
        all_questions = QuestionBank.generateQuestionsForCardAttributes(all_cards)
        print("Finished generating all possible questions for all cards.")
        question_column_fields = ["Name"]
        for question in all_questions:
            question_column_fields.append(f'{question}#YES')
            question_column_fields.append(f'{question}#NO')
            question_column_fields.append(f'{question}#MAYBE')
        
        # print("Generated all questions!")
        # scryfall_questions_map = ask_all_questions()
        # for scry_q in scryfall_questions_map.keys():
        #     question_column_fields.append(f'{scry_q}#YES')
        #     question_column_fields.append(f'{scry_q}#NO')
        #     question_column_fields.append(f'{scry_q}#MAYBE')
        # print("Generated all Scryfall questions!")

        fields = []
        for col in question_column_fields:
            fields.append( sql.SQL(" {} {} ").format( sql.Identifier(col), sql.SQL("TEXT")))
        query = sql.SQL( "CREATE TABLE IF NOT EXISTS CardsLive( {columns} );" ).format(
            columns=sql.SQL(', ').join(fields))
        commands = (
            f"""
            DROP TABLE IF EXISTS CardsLive;
            """,
            query
        )

        conn = None
        try:
            print("Creating connection to Magikinator database.")
            conn = create_connection("magikinator")
            cursor = conn.cursor()
            for command in commands:
                cursor.execute(command)
            conn.commit()
        except (Exception, psy.errors.DatabaseError) as error:
            print(error)
        finally:
            if conn:
                cursor.close()
                conn.close()



# login_user_create_database()
# create_table()
# downloadDefaultCardDataFromScryfall()
# fetch_all_cards()
# convert_cards_into_card_objects()
# QuestionBank.answerQuestionsForCardAttributes()
QuestionBank.create_cardsdatalive_table()