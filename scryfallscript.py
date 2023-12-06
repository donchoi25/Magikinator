import requests
from requests.adapters import HTTPAdapter, Retry
from urllib.parse import quote
import math
from common_phrases import COMMON_PHRASES

SCRYFALL_SEARCH_URL = "https://api.scryfall.com/cards/search?q="
TEST_SEARCHES = {
    "Is your card a permanent?": "is:permanent",
    "Can this card be your commander?": "is:commander",
    "Is your card a split card?": "is:split",
    "Can your card flip at any point?": "is:flip",
    "Can your card meld?": "is:meld",
    "Can your card transform?": "is:transform",
    "Can your card level up?": "is:leveler",
    "Is your card a double-faced card?": "is:dfc",
    "Is your card a vanilla creature? (It has no effects)": "is:vanilla",
    "Does your card deal with counters of any kind?": "o:counters",
    "Does your card do something when it enters the battlefield or comes into play?:": "o:'enters the battlefield'",
    "Does your card enchant creatures?": "o:'enchant creature'",
    "Does your card tap or untap target permanent?": "o:'tap target permanent'",
    "Does your card have an additional cost, including paying life, sacrificing a creature, discarding a card, etc?": "o:'additional cost'",
    "Does your card have a triggered ability (has the word 'whenever' in its effect text)?": 'o:whenever',
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
    "Does your card put a +1/+1 counter on a permanent?": "o:'put a +1/+1 counter'",
    "Does your card target a creature you control?": "o:'target creature you control'",
    "Does your card trigger when combat damage is dealt?": "o:'deals combat damage'",
    "Does your card trigger when combat damage is dealt specifically to a player?": "o:'deals combat damage to a player'",
    "Does your card stop itself or other creatures from being blocked?": "o:'be blocked'",
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
    "Does your card trigger an effect at the beginning of the next end step?": "o:'beginning of the next end step'",
    "Does your card copy a spell or permanent?": "function:copy",
    "Does your card stop itself or spells from being countered": "o:'be countered'",
    "Does your card exile a target?": "o:'exile target'",
    "Is your card a land?": "t:land",
    "Is your card banned in commander?": "banned:commander",
    "Does this card change your maximum hand size?": "o:'maximum hand size'",
    "Is your card a conspiracy?": "t:conspiracy",
    "Can your card foretell?": "o:'foretell'",
    "Can your card 'search your library'?": "o:'search your library'",
    'Can your card sacrifice itself?': "o:'sacrifice /~/'",
    "Does your card have an activated ability that requires sacrificing a creature?": "o:'sacrifice a creature:'",
    "Does your card cause you or an opponent to discard a card": "o:discard",
    "Can your card create a treasure token?": "o:'create a treasure token'",
    "Is your card a token?": "type:token",
    "Does your card amass?": "o:amass",
    "Does your card cost 1 colorless mana less to cast, if something is true?": "o:'less to cast for each'",
    "Does your card double the number of tokens or counters that would be created?": "o:'twice that many'",
    "Is your card a creature with a power greater than its toughness?": "'pow>tou t:creature'",
    "Is your card a creature with a power equal to its toughness?": "'pow=tou t:creature'",
    "Is your card a creature with a power less than its toughness?": "'pow<tou t:creature'",

    ### TAGGER QUESTIONS https://scryfall.com/docs/tagger-tags
    "Does your card have a delayed replacement effect?": "oracletag:delayed-replacement-effect",
    "Does your card have a delayed triggered ability?": "oracletag:delayed-triggered-ability",
    "Can your card prevent damage?": "oracletag:damage-prevention",
    "Does your card have an effect that involves ability-counters?: (Flying Counter, Reach Counter, Trample Counter...etc)": "oracletag:ability-counter",
    "Does your card have an activated ability?": "oracletag:activated-ability",
    "Does your card have an activated ability, that can be used from the graveyard?": "oracletag:activate-from-graveyard",
    "Does your card have an activated ability, that can be used from your hand?": "oracletag:activate-from-hand",
    "Does your card affect dice rolls?": "oracletag:affects-dice-roll",
    "Does your card have affinity (costs 1 less to cast each ___ permanent you control)?": "oracletag:affinity",
    "Does your card have affinity for artifacts?": "oracletag:affinity-for-artifacts",
    "Does your card have affinity for citizens?": "oracletag:affinity-for-citizens",
    "Does your card have affinity for daleks?": "oracletag:affinity-for-daleks",
    "Does your card have affinity for enchantments?": "oracletag:affinity-for-enchantments",
    "Does your card have affinity for equipment?": "oracletag:affinity-for-equipment",
    "Does your card have affinity for gates?": "oracletag:affinity-for-gates",
    "Does your card have affinity for knights?": "oracletag:affinity-for-knights",
    "Does your card have affinity for land types (Domain)?": "oracletag:affinity-for-land-type",
    "Does your card have affinity for spells in graveyard?": "oracletag:affinity-for-spells",
    "Does your card have affinity for spirits?": "oracletag:affinity-for-spirits",
    "Does your card not untap during your untap step?": "oracletag:doesn-t-untap",
    "Does your card affect all players equally?": "oracletag:symmetrical",
    "Does your card double counters on creatures?": "oracletag:counter-doubler",
    "Does your card double counters on creatures, and other permanents?": "oracletag:counter-double o:'creature'",
    "Does your card create an alternative win-condition?": "oracletag:alternate-win-condition",
    "Does your card have an anthem effect?": "oracletag:anthem",
    "Does your card have a daybound or nightbound effect?": "o:daybound",
    "Does your card have an attack trigger?": "oracletag:attack-trigger",
    "Does your card enter the battlefield as a copy of a permanent?": "o:'enter the battlefield as a copy'",
    "Does your card care about basic lands?": "oracletag:cares-about-basic-land",
    "Is your card castable from exile?": "oracletag:castable-from-exile",
    "Can your card be cast from the graveyard?": "oracletag:cast-from-graveyard",
    "Does your card let you play cards from the top of your library?": "oracletag:cast-from-top",
    "Does your card have a casting restriction?": "oracletag:casting-restriction",
    "Does your card have a cast trigger?": "oracletag:cast-trigger",

    ### TAGGER ART QUESTIONS
    "Does your card art include acid of any kind?": "art:acid",
    "Does your card art include any acrobatics?": "art:acrobat",
    "Does your card art include anybody with their arms crossed?": "art:arms-crossed",
    "Does your card art include an angel?": "art:angel",
    "Does your card art include an arrow?": "art:arrow",
    "Does your card art include an axe?": "art:axe",
    
    


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
retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
s.mount("https://", HTTPAdapter(max_retries=retries))

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
    first_page_url = f'{SCRYFALL_SEARCH_URL}' + quote(q)
    page_result, next_page_url = make_page_request(first_page_url)
    i = 1

    while next_page_url:
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
        print(f'Asking Scryfall the question: "{question_text}"...')
        cards_returned = ask_question(question)
        # print("Answered with " + str(len(cards_returned)) + " cards returned.")
        questions_cards_map[question_text] = cards_returned

    return questions_cards_map


# ask_all_questions()