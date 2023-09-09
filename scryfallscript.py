import requests
import math

SCRYFALL_SEARCH_URL = "https://api.scryfall.com/cards/search?q="
TEST_SEARCHES = {
    "Is your card a permanent?": "is:permanent",
    "Can this card be your commander?": "is:commander",
    "Does your card have more than one face?": "is:split",\
    "Does your card deal with counters of any kind?": "o:counters",
    "Does your card do something when it enters the battlefield or comes into play?:": "o:'enters the battlefield'",
    "Is your card a creature that deals with drawing cards?": "o:draw t:creature",
    "Does your card enchant creatures?": "o:'enchant creature'"
}

s = requests.Session()

def make_page_request(URL):
    r = s.get(url=URL)
    cardslist = []
    r_js = r.json()
    data = r_js.get('data')
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


ask_all_questions()