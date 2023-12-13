import requests
from requests.adapters import HTTPAdapter, Retry
from urllib.parse import quote
import math
from common_phrases import COMMON_PHRASES

SCRYFALL_SEARCH_URL = "https://api.scryfall.com/cards/search?q="
TEST_SEARCHES = {
    ###########################################
    # QUESTIONS THAT DO NOT DEPEND ON PRINTINGS
    ###########################################

    # Simple IS questions
    "Is your card a permanent?": "is:permanent",
    "Is your card a spell?": "is:spell",
    "Is your card an artifact?": "t:artifact",
    "Is your card an creature?": "t:creature",
    "Is your card an enchantment?": "t:enchantment",
    "Is your card an instant?": "t:instant",
    "Is your card an land?": "t:land",
    "Is your card an planeswalker?": "t:planeswalker",
    "Is your card an sorcery?": "t:sorcery",
    "Is your card a world enchantment or enchant world?":"t:world",
    "Is your card an aura or enchant creature?": "t:aura",
    "Is your card a saga?": "t:saga",
    "Is your card historic (artifact, legendary creature, saga enchantment)?": "is:historic",
    "Is your card a companion?": "is:companion",
    "Is your card a canopyland?": "is:canopyland",
    "Is your card a checkland?": "is:checkland",
    "Is your card a dual land?": "is:dual",
    "Is your card a fetchland?": "is:fetchland",
    "Is your card a filterland?": "is:filterland",
    "Is your card a gainland?": "is:gainland",
    "Is your card a painland?": "is:painland",
    "Is your card a scryland?": "is:scryland",
    "Is your card a shadowland?": "is:shadowland",
    "Is your card a shockland?": "is:shockland",
    "Is your card a storageland?": "is:storageland",
    "Is your card a creatureland?": "is:creatureland",
    "Is your card a triland?": "is:triland",
    "Is your card a scryland?": "is:scryland",
    "Is your card a battleland?": "is:battleland",
    "Is your card on the reserved list?": "is:reserved",
    "Can your card be in a party? (Rogue, Warrior, Wizard, Cleric, Monk)": "is:party",
    "Can this card be your commander?": "is:commander",
    "Is your card a split card?": "is:split",
    "Can your card flip at any point?": "is:flip",
    "Can your card meld?": "is:meld",
    "Can your card transform?": "is:transform",
    "Can your card level up?": "is:leveler",
    "Does your card meld?": "is:meld",
    "Is your card a modal double-faced card?": "is:mdfc",
    "Is your card a double-faced card?": "is:dfc",
    "Does your card have multiple modes?": "is:modal",
    "Does your card cost or use phyrexian mana?": "is:phyrexian",
    "Is your card a vanilla creature?": "is:vanilla",
    "Is your card a conspiracy?": "t:conspiracy",
    "Does your card have hybrid mana in its mana cost?": "is:hybrid",
    "Does your card have red in its mana cost?": "c:r",
    "Does your card have blue in its mana cost?": "c:u",
    "Does your card have green in its mana cost?": "c:g",
    "Does your card have white in its mana cost?": "c:w",
    "Does your card have black in its mana cost?": "c:b",
    "Is your card colorless? (or has devoid)?": "c:c",
    "Does your card have X in its mana cost?": "m:X",
    "Is your card a token?": "type:token",

    # Questions oracletext
    "Does your card enter the battlefield and make you the monarch?": "o:'you become the monarch'",
    "Does your card have devoid?": "o:devoid",
    "Does your card have madness?": "o:madness",
    "Can your card regenerate itself?": "o:'regenerate ~'",
    "Does your card do something when it dies?": "o:'when ~ dies'",
    "Can your card prevent damage?": "o:prevent",
    "Can you card not be countered?": "o:~ o:'be countered'",
    "Does your card copy something?": "function:copy",
    "Does your card reference its own name in its bottom text?": "o:~",
    "Can your card counter something?": "function:counter",
    "Does your card have players vote?": "o:'player votes'",
    "Does your card have power and toughness equal to the number of (or create a token that does)?": "o:'power and toughness are'",
    "Does your card change the amount of mana generated when tapping permanents?": "++o:'taps a' o:'for mana' o:'add'",
    "Does your card have a triggered ability (has the words 'when', 'whenever', or 'at' in its effect text)?": "o:when or o:'at the'",
    "Does your card have an additional cost, including paying life, sacrificing a creature, discarding a card, etc?": "o:'additional cost'",
    "Does your card do something when itself enters the battlefield or comes into play?:": "o:'enters the battlefield'",
    "Does your card have an effect that triggers when a permanent enters the battlefield under your control?": "o:'enters the battlefield under your control'",
    "Does your card have an effect that triggers when a creature enters the battlefield?": "o:'creature enters the battlefield'",
    "Does your card enter the battlefield tapped?": "o:/~/ o:'enters the battlefield tapped'",
    "Does your card give an anthem to creature you control?":"oracletag:anthem",
    "Does this card remove someone's maximum hand size?": "o:'no maximum hand size'",
    "Can your card have you search your library?": "o:'search your library'",
    'Can your card sacrifice itself?': "o:'sacrifice ~'",
    "Can your card cause someone to discard a card": "o:discard",
    "Can your card create a treasure token?": "o:'treasure token'",
    "Is your card a creature with a power greater than its toughness?": "pow>tou t:creature",
    "Is your card a creature with a power equal to its toughness?": "pow=tou t:creature",
    "Is your card a creature with a power less than its toughness?": "pow<tou t:creature",
    "Does your card involve protection?": "o:'protection'",
    "Does your card involve protection from red?": "o:'protection from red'",
    "Does your card involve protection from blue?": "o:'protection from blue'",
    "Does your card involve protection from green?": "o:'protection from green'",
    "Does your card involve protection from white?": "o:'protection from white'",
    "Does your card involve protection from black?": "o:'protection from black'",
    "Does your card involve protection from multicolored?": "o:'protection from multicolored'",

    # New Questions
    "Is your card an instant that deals damage?": "t:instant o:'deal'",
    "Is your card a sorcery that deals damage?": "t:sorcery o:'deal'",
    "Does your card destroy lands?": "o:'destroy target land' or o:'destroy all lands'", #Ghost Quarters
    "Does your card have an activated ability, or create a token with an activated ability?": "o:':' or o:equip or o:'{X}'",
    "Can your card create an additional combat phase?": "o:'additional combat phase'",

    # Might need to google the card
    "Is your card banned in commander?": "banned:commander",
    "Is your card banned in legacy?": "banned:legacy",

    # Subjective questions
    # "Can your card allow a player to draw a card?": "function:draw",

    # QUESTIONS THAT DEPEND ON PRINTINGS (THESE NEED TO BE REMOVED?)
    # "Does your card have a white border?": "border:white",
    "Does your card contain flavor text?": "ft:' '"
    
    # ### TAGGER QUESTIONS https://scryfall.com/docs/tagger-tags
    # "Does your card have a delayed replacement effect?": "oracletag:delayed-replacement-effect",
    # "Does your card have a delayed triggered ability?": "oracletag:delayed-triggered-ability",
    # "Can your card prevent damage?": "oracletag:damage-prevention",
    # "Does your card have an effect that involves ability-counters?: (Flying Counter, Reach Counter, Trample Counter...etc)": "oracletag:ability-counter",
    # "Does your card have an activated ability, that can be used from the graveyard?": "oracletag:activate-from-graveyard",
    # "Does your card have an activated ability, that can be used from your hand?": "oracletag:activate-from-hand",
    # "Does your card affect dice rolls?": "oracletag:affects-dice-roll",
    # "Does your card have affinity (costs 1 less to cast each ___ permanent you control)?": "oracletag:affinity",
    # "Does your card have affinity for artifacts?": "oracletag:affinity-for-artifacts",
    # "Does your card have affinity for citizens?": "oracletag:affinity-for-citizens",
    # "Does your card have affinity for daleks?": "oracletag:affinity-for-daleks",
    # "Does your card have affinity for enchantments?": "oracletag:affinity-for-enchantments",
    # "Does your card have affinity for equipment?": "oracletag:affinity-for-equipment",
    # "Does your card have affinity for gates?": "oracletag:affinity-for-gates",
    # "Does your card have affinity for knights?": "oracletag:affinity-for-knights",
    # "Does your card have affinity for land types (Domain)?": "oracletag:affinity-for-land-type",
    # "Does your card have affinity for spells in graveyard?": "oracletag:affinity-for-spells",
    # "Does your card have affinity for spirits?": "oracletag:affinity-for-spirits",
    # "Does your card not untap during your untap step?": "oracletag:doesn-t-untap",
    # "Does your card affect all players equally?": "oracletag:symmetrical",
    # "Does your card double counters on creatures?": "oracletag:counter-doubler",
    # "Does your card double counters on creatures, and other permanents?": "oracletag:counter-doubler o:creature",
    # "Does your card create an alternative win-condition?": "oracletag:alternate-win-condition",
    # "Does your card have an anthem effect?": "oracletag:anthem",
    # "Does your card have a daybound or nightbound effect?": "o:daybound",
    # "Does your card have an attack trigger?": "oracletag:attack-trigger",
    # "Does your card enter the battlefield as a copy of a permanent?": "o:'enter the battlefield as a copy'",
    # "Does your card care about basic lands?": "oracletag:cares-about-basic-land",
    # "Is your card castable from exile?": "oracletag:castable-from-exile",
    # "Can your card be cast from the graveyard?": "oracletag:cast-from-graveyard",
    # "Does your card let you play cards from the top of your library?": "oracletag:cast-from-top",
    # "Does your card have a casting restriction?": "oracletag:casting-restriction",
    # "Does your card have a cast trigger?": "oracletag:cast-trigger",

    # ### TAGGER ART QUESTIONS
    # "Does your card art include acid of any kind?": "art:acid",
    # "Does your card art include any acrobatics?": "art:acrobat",
    # "Does your card art include anybody with their arms crossed?": "art:arms-crossed",
    # "Does your card art include an angel?": "art:angel",
    # "Does your card art include an arrow?": "art:arrow",
    # "Does your card art include an axe?": "art:axe",
    # "Does your card art include Liliana the PlanesWalker?": "art:liliana"
}
def get_top_phrases():
    TOP_PHRASE_LIMIT = 50
    i = 0
    for phrase_and_count in COMMON_PHRASES:
        if i > TOP_PHRASE_LIMIT:
            break
        phrase_arr, count = phrase_and_count
        phrase = " ".join(phrase_arr)
        print(phrase)
        i += 1

s = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
s.mount("https://", HTTPAdapter(max_retries=retries))

def make_page_request(URL, question=""):
    r = s.get(url=URL)
    cardslist = []
    r_js = r.json()
    data = r_js.get('data')
    if not data:
        print(question)
        print("Failed to make a page request when asking " + question + ". Skipping this question.")
        return (cardslist, None)
    for card in data:
        cardslist.append(card.get('name').lower())
    next_page_url = r_js.get('next_page')
    return (cardslist, next_page_url)

def ask_question(q):
    all_cards_data = []
    first_page_url = f'{SCRYFALL_SEARCH_URL}' + quote(q)
    page_result, next_page_url = make_page_request(first_page_url, q)
    i = 1

    while next_page_url:
        if page_result:
            all_cards_data.extend(page_result)
        page_result, next_page_url = make_page_request(next_page_url, q)
        i += 1

    if page_result:
        all_cards_data.extend(page_result)

    return all_cards_data

def ask_all_questions():
    questions_cards_map = {}
    for question_text, question in TEST_SEARCHES.items():
        cards_returned = ask_question(question)
        # print("Answered with " + str(len(cards_returned)) + " cards returned.")
        questions_cards_map[question_text] = cards_returned
    return questions_cards_map