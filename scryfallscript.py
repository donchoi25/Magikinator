import requests
import math
from common_phrases import COMMON_PHRASES

SCRYFALL_SEARCH_URL = "https://api.scryfall.com/cards/search?q="
TEST_SEARCHES = {
    "Is your card a permanent?": "is:permanent",
    "Can this card be your commander?": "is:commander",
    "Does your card have more than one face?": "is:split",\
    "Does your card deal with counters of any kind?": "o:counters",
    "Does your card do something when it enters the battlefield or comes into play?:": "o:'enters the battlefield'",
    "Does your card enchant creatures?": "o:'enchant creature'",
    "Does your card tap or untap target permanent?": "o:'tap target permanent'",
    "Does your card have an additional cost, including paying life, sacrificing a creature, discarding a card, etc?": "o:'additional cost'",
    "Does your card have a triggered ability?": 'o:whenever',
    "Does your card meld?": "is:meld",
    "Is your card a vanilla creature?": "is:vanilla",
    "Is your card an alchemy card?": "st:alchemy",
    "Is your card banned in commander?": "banned:legacy",
    "Is your card on the reserved list?": "is:reserved",
    "Does your card have a white border?": "border:white",
    "Is your card used as removal?": "function:removal",
    "Can your card draw you a card?": "function:draw",
    "Can you card have you or an opponent discard cards?": "function:discard",
    "Can you card counter something?": "function:counter",
    "Does your card cost or require phyrexian mana?": "is:phyrexian",
    "Does your card contain flavor text?": "ft:' '",
    "Does your card trigger an effect at the beginning of a phase?": "o:'at the beginning'",
    "Does your card trigger an effect at the beginning of your upkeep?": "o:'at the beginning of your upkeep'",
    "Does your card create an effect that lasts 'until end of turn'?": "o:'until end of turn'",
    "Does your card put a +1/+1 counter on a permanent?": "o:'put a +1\/+1 counter'",
    "Does your card target a creature you control?": "o:'target creature you control'",
    "Does your card trigger when combat damage is dealt?": "o:'deals combat damage'",
    "Does your card trigger when combat damage is dealt specifically to a player?": "o:'deals combat damage to a player'",
    "Does your card stop itself or other creatures from being blocked?": "o:'can\'t be blocked'",
    "Does your card have an effect that deals exactly 1 damage?": "o:'deals 1 damage'",
    "Does your card have an effect that deals exactly 2 damage?": "o:'deals 2 damage'",
    "Does your card have an effect that deals exactly 3 damage?": "o:'deals 3 damage'",
    "Does your card have an effect that deals exactly 4 damage?": "o:'deals 4 damage'",
    "Does your card have an effect that deals exactly 5 damage?": "o:'deals 5 damage'",
    "Does your card have an effect that deals exactly 5 damage?": "o:'deals 5 damage'",
    "Does your card have an effect that deals exactly 6 damage?": "o:'deals 6 damage'",
    "Does your card have an effect that deals exactly 7 damage?": "o:'deals 7 damage'",
    "Does your card have an effect that deals exactly 8 damage?": "o:'deals 8 damage'",
    "Does your card have an effect that deals exactly X damage?": "o:'deals X damage'",
    "Does your card have an effect that triggers when a permanent enters the battlefield under your control?": "o:'enters the battlefield under your control'",
    "Does your card have an effect that triggers when a creature enters the battlefield?": "o:'creature enters the battlefield'",
    "Does your card reference its own name in its bottom text?": "o:/~/",
    "Does your card enter the battlefield tapped?": "o:/~/ o:'enters the battlefield tapped'",
    "Does your card give an effect to creatures you control?": "o:'creatures you control'",
    "Does your card have an effect that you can only activate as a sorcery?": "o:'activate only as a sorcery'",
    "Does your card have an effect that involves the top card of your library?": "o:'top card of your library'",
    "Does your card have an effect that involves one or more cards from the top of your library?": "o:'cards of your library'",
    "Does your card prevent damage?": "o:prevent o:damage",
    "Does your card trigger an effect at the beginning of the next end step?": "o:'beginning of the next end step'"
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

# get_top_phrases()

s = requests.Session()

def make_page_request(URL):
    r = s.get(url=URL)
    cardslist = []
    r_js = r.json()
    data = r_js.get('data')
    if not data:
        print("Failed to make a page request to " + URL + ". Skipping this question.")
        return (cardslist, None)
    for card in data:
        cardslist.append(card.get('name').lower())
    next_page_url = r_js.get('next_page')
    return (cardslist, next_page_url)

def ask_question(q):
    all_cards_data = []
    first_page_url = f'{SCRYFALL_SEARCH_URL}' + q
    page_result, next_page_url = make_page_request(first_page_url)
    i = 1

    while next_page_url:
        # if not i % 5:
            # print("On page: " + str(i))
        if page_result:
            all_cards_data.extend(page_result)
        page_result, next_page_url = make_page_request(next_page_url)
        i += 1

    if page_result:
        all_cards_data.extend(page_result)

    return all_cards_data

def ask_all_questions():
    questions_cards_map = {}
    for question_text, question in TEST_SEARCHES.items():
        question_text = "_".join(question_text.split(" "))
        # print(f'Asking the question: "{text}"...')
        cards_returned = ask_question(question)
        # print("Answered with " + str(len(cards_returned)) + " cards returned.")
        questions_cards_map[question_text] = cards_returned

    return questions_cards_map


# ask_all_questions()