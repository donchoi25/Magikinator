import psycopg2 as psy
from psycopg2 import Error
import os.path
from urllib.request import urlopen
import json

CARDDATA_JSON_FILENAME = "./data/files/cardsdata.json"
SCRYFALL_DEFAULTCARDS_JSON_URL = "https://data.scryfall.io/default-cards/default-cards-20230830090607.json"


def create_connection(database_name=""):
    try:
        conn = psy.connect(
            host="127.0.0.1",
            user="postgres",
            password="master123",
            database=database_name
        )

        cursor = conn.cursor()
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
            conn.close()
    

def create_table():
    commands = (
        """
        DROP TABLE IF EXISTS Cards;
        """,
        """
        CREATE TABLE IF NOT EXISTS Cards (
            name SERIAL PRIMARY KEY,
            released_at TEXT,
            mana_cost TEXT,
            cmc TEXT,
            type_line TEXT,
            oracle_text TEXT,
            power TEXT,
            toughness TEXT,
            colors TEXT,
            color_identity TEXT,
            keywords TEXT[],
            legalities TEXT[],
            set TEXT[],
            rarity TEXT[],
            artist TEXT[],
            flavor_text TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Questions (
            question SERIAL PRIMARY KEY
        )
        """
    )
    conn = None
    try:
        conn = create_connection("magikinator")
        cursor = conn.cursor()
        for command in commands:
            cursor.execute(command)
        print("Successfully created tables Cards and Questions")
        cursor.close()
        conn.commit()
    except (Exception, psy.errors.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            conn.close()

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
    for card_data_json in data_json:
        print(card_data_json.get("name"))
        insert_card_sql(card_data_json)
        break
        

def insert_card_sql(card):
    COMMAND = f"""
    INSERT INTO Cards (name, released_at, mana_cost, cmc, type_line, \
        oracle_text, power, toughness, colors, color_identity, keywords, \
        legalities, set, rarity, artist, flavor_text) \
    VALUES ({card.get("name")}, {card.get("released_at")}, {card.get("mana_cost")}, {card.get("cmc")}, \
        {card.get("type_line")}, {card.get("oracle_text")}, {card.get("power")}, {card.get("toughness")}, \
            {card.get("colors")}, {card.get("color_identity")}, {card.get("keywords")}, {card.get("legalities")}, \
                {card.get("set")}, {card.get("rarity")}, {card.get("artist")}, {card.get("flavor_text")})
    """
    conn = None
    try:
        conn = create_connection("magikinator")
        cursor = conn.cursor()
        cursor.execute(COMMAND)
        cursor.close()
        conn.commit()
    except (Exception, psy.errors.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            conn.close()


login_user_create_database()
create_table()
downloadDefaultCardDataFromScryfall()