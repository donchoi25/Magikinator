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

    # IS QUERIES
    "Is your card a permanent?": "is:permanent",
    "Is your card a spell?": "is:spell",
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
    "Is your card a bondland?": "is:bondland",
    "Is your card a tronland?": "is:tron",
    "Is your card a fastland?": "is:fastland",
    "Is your card on the reserved list?": "is:reserved",
    "Is your card a split card?": "is:split",
    "Can your card be in a party? (Rogue, Warrior, Wizard, Cleric, Monk)": "is:party",
    "Can your card be your commander?": "is:commander",
    "Can your card flip?": "is:flip",
    "Can your card meld?": "is:meld",
    "Can your card transform?": "is:transform",
    "Can your card level up?": "is:leveler",
    "Is your card a modal-double-faced card?": "is:mdfc",
    "Is your card a double-faced card?": "is:dfc",
    "Does your card have multiple modes?": "is:modal",
    "Is your card a vanilla creature with no effects?": "is:vanilla",
    "Does your card have hybrid mana cost?": "is:hybrid",
    
    # TYPE QUERIES
    "Is your card an artifact?": "t:artifact",
    "Is your card an creature?": "t:creature",
    "Is your card an enchantment?": "t:enchantment",
    "Is your card an instant?": "t:instant",
    "Is your card an land?": "t:land",
    "Is your card an planeswalker?": "t:planeswalker",
    "Is your card an sorcery?": "t:sorcery",
    "Is your card a token?": "t:token",
    "Is your card a world enchantment or enchant world?":"t:world",
    "Is your card an aura or enchant creature?": "t:aura",
    "Is your card a saga?": "t:saga",
    "Is your card a vanguard?": "t:vanguard",
    "Is your card a plane card?": "t:plane",
    "Is your card a conspiracy?": "t:conspiracy",
    "Is your card an instant that deals damage?": "t:instant o:'deal'",
    "Is your card a sorcery that deals damage?": "t:sorcery o:'deal'",
    "Is your card an emblem?": "t:emblem",
    "Is your card an equipment that gives equipped creature first strike?": "t:equipment o:'first strike'",
    "Is your card an equipment that gives equipped creature trample?": "t:equipment o:'trample'",
    "Is your card an equipment that gives equipped creature haste?": "t:equipment o:'haste'",
    "Is your card an equipment that gives equipped creature flying?": "t:equipment o:'flying'",
    "Is your card an equipment that gives equipped creature vigilance?": "t:equipment o:'vigilance'",
    "Is your card an equipment that gives equipped creature indestructible?": "t:equipment o:'indestructible'",
    "Is your card an equipment that gives equipped creature lifelink?": "t:equipment o:'lifelink'",
    "Is your card an equipment that gives equipped creature double strike?": "t:equipment o:'double strike'",
    "Is your card an equipment that gives equipped creature hexproof?": "t:equipment o:'hexproof'",
    "Is your card an equipment that gives equipped creature shroud?": "t:equipment o:'shroud'",
    "Is your card a phenomenon?": "t:phenomenon",
    "Is your card an eldrazi?": "o:eldrazi or t:eldrazi",
    "Is your card phyrexian?": "o:phyrexian or t:phyrexian or is:phyrexian",
    
    # Color QUERIES
    "Is your card red?": "c:r",
    "Is your card blue?": "c:u",
    "Is your card green?": "c:g",
    "Is your card white": "c:w",
    "Is your card black": "c:b",
    "Is your card colorless?": "c:c",
    "Is your card multicolored?": "c:m",
    
    # Color Identity QUERIES
    "Is your card's color identity red?": "id:r -id:c",
    "Is your card's color identity blue?": "id:u -id:c",
    "Is your card's color identity green?": "id:g -id:c",
    "Is your card's color identity white?": "id:w -id:c",
    "Is your card's color identity black?": "id:b -id:c",
    "Is your card's color identity colorless?": "id:c",
    
    # Mana Cost QUERIES
    "Does your card have X mana cost?": "m:X",
    "Does your card use phyrexian mana?": "is:phyrexian",
    
    # Function QUERIES
    "Can your card draw cards?": "function:draw",
    "Can your card copy?": "function:copy",
    "Can your card counter spells or abilities?": "function:counter",
    "Can your card make someone discard?": "function:discard",
    "Is your card a wrath?": "function:wrath",
    
    # Oracletext QUERIES
    "Does your card make you the monarch?": "o:'you become the monarch'",
    "Does your card regenerate itself?": "o:'regenerate ~'",
    "Does your card trigger when it dies?": "o:'when ~ dies'",
    "Does your card prevent anything?": "o:prevent",
    "Is your card uncounterable?": "o:~ o:'be countered'",
    "Does your card mention itself in its bottom text?": "o:~",
    "Does your card involve voting?": "o:'player votes'",
    "Is your card's power and toughness based on the number of something": "o:power o:toughness o:equal",
    "Does your card increase the mana produced by permanents?": "++o:'taps a' o:'for mana' o:'add'",
    "Does your card have a triggered ability (contains 'when'/'whenever'/'at' in its effect)?": "o:when or o:'at the'",
    "Does your card have an additional cost?": "o:'additional cost'",
    "Does your card have an enters the battlefield trigger?": "(o:enters o:the o:battlefield) and -(o:'may have ~')",
    "Does your card have an enters the battlefield trigger for only permanents you control?": "(o:enters o:the o:battlefield) and -(o:'may have ~') and (o:under o:your o:control)",
    "Does your card enter the battlefield tapped?": "o:'~ enters the battlefield tapped'",
    "Is your card an anthem?": "oracletag:anthem",
    "Does your card remove maximum hand size?": "o:no o:maximum o:hand o:size",
    "Does your card search your library?": "o:search o:your o:library",
    "Can your card sacrifice itself?": "o:'sacrifice ~'",
    "Does your card have power greater than toughness?": "pow>tou t:creature",
    "Does your card have power equal to its toughness?": "pow=tou t:creature",
    "Does your card have power less than its toughness?": "pow<tou t:creature",
    "Does your card have or grant protection from red?": "keyword:protection (o:'from red' or o:everything) ",
    "Does your card have or grant protection from blue?": "keyword:protection (o:'from blue' or o:everything) ",
    "Does your card have or grant protection from green?": "keyword:protection (o:'from green' or o:everything) ",
    "Does your card have or grant protection from white?": "keyword:protection (o:'from white' or o:everything) ",
    "Does your card have or grant protection from black?": "keyword:protection (o:'from black' or o:everything) ",
    "Does your card have or grant protection from instants?": "keyword:protection (o:'from instants' or o:everything) ",
    "Does your card have or grant protection from creatures?": "keyword:protection (o:'from creatures' or o:everything)",
    "Does your card have or grant protection from multicolored?": "keyword:protection (o:'from multicolored' or o:everything) ",
    "Does your card have an effect that lasts until end of turn?": "o:until o:end o:of o:turn",
    "Does your card grant reach?": "o:'gains reach'",
    "Does your card grant lifelink?": "o:'gains lifelink'",
    "Does your card grant vigilance?": "o:'gains vigilance'",
    "Does your card grant flying?": "o:'gains flying'",
    "Does your card grant hexproof?": "o:'gains hexproof'",
    "Does your card grant indestructible?": "o:'gains indestructible'",
    "Does your card grant first strike?": "o:'gains first strike'",
    "Does your card grant trample?": "o:'gains trample'",
    "Does your card grant haste?": "o:'gains haste'",
    "Does your card grant shroud?": "o:'gains shroud'",
    "Does your card grant double strike?": "o:'gains double strike'",
    "Does your card target creatures?": 'o:target o:creature',
    "Does your card increase the power/toughness of creatures you control?": "o:creatures o:'you control get'",
    "Does your card counter noncreature spells?": "o:counter o:target o:'noncreature spell'",
    "Does your card counter creature spells?": "o:counter o:target o:'creature spell'",
    "Does your card place counters on permanents?": "o:put o:counter o:on",
    "Does your card only enchant creatures you control?": "o:'enchant ' o:creature o:'you control'",
    "Does your card have an alternate win condition?": "o:'you win the game'",
    "Does your card use infect or poison counters?": "o:poison o:counter or keyword:infect",
    "Does your card gain you life?": "o:'you gain life' o:lifelink",
    "Does your card return things to hand?": "o:'return target' o:hand",
    "Does your card return things to library?": "o:'return target' o:library",
    "Does your card care about same names?": "o:'same name'",
    "Does your card  activate by sacrificing something?": "o:sacrifice o:':'",
    "Does your card target multiple players?": "o:different o:players",
    "Does your card only activate if something is true?": "o:'activate only'",
    "Does your card have a you-may ability?": "o:'you may'",
    "Does your card prevent damage from white sources?": "o:prevent o:damage o:'white source'",
    "Does your card prevent damage from blue sources?": "o:prevent o:damage o:'blue source'",
    "Does your card prevent damage from black sources?": "o:prevent o:damage o:'black source'",
    "Does your card prevent damage from red sources?": "o:prevent o:damage o:'red source'",
    "Does your card prevent damage from green sources?": "o:prevent o:damage o:'green source'",
    "Does your card make things lose all abilities?": "o:'loses all abilities'",
    "Does your card produce mana only for certain abilities?": "o:'spend this mana only' o:activate",
    "Does your card destroy lands?": "o:'destroy target land' or o:'destroy all lands'", #Ghost Quarters
    "Does your card have an activated ability?": "o:':' or o:equip or o:'{X}'",
    "Can your card create additional combat phases?": "o:additional o:combat o:phase",
    "Does your card enchant creatures to grant vigilance?": "o:'enchanted creature' o:vigilance",
    "Does your card enchant creatures to grant first strike?": "o:'enchanted creature' o:'first strike'",
    "Does your card enchant creatures to grant trample?": "o:'enchanted creature' o:'trample'",
    "Does your card enchant creatures to grant haste?": "o:'enchanted creature' o:'haste'",
    "Does your card enchant creatures to grant flying?": "o:'enchanted creature' o:'flying'",
    "Does your card enchant creatures to grant vigilance?": "o:'enchanted creature' o:'vigilance'",
    "Does your card enchant creatures to grant indestructible?": "o:'enchanted creature' o:'indestructible'",
    "Does your card enchant creatures to grant lifelink?": "o:'enchanted creature' o:'lifelink'",
    "Does your card enchant creatures to grant double strike?": "o:'enchanted creature' o:'double strike'",
    "Does your card enchant creatures to grant hexproof?": "o:'enchanted creature' o:'hexproof'",
    "Does your card enchant creatures to grant shroud?": "o:'enchanted creature' o:'shroud'",
    "Does your card care about players casting red spells?": "o:'casts a red spell'",
    "Does your card care about players casting blue spells?": "o:'casts a blue spell'",
    "Does your card care about players casting green spells?": "o:'casts a green spell'",
    "Does your card care about players casting black spells?": "o:'casts a black spell'",
    "Does your card care about players casting white spells?": "o:'casts a white spell'",
    "Does your card enchant creatures?": "o:'enchant creature'",
    "Does your card enchant permanents?": "o:'enchant permanent'",
    "Does your card enchant instants?": "o:'enchant instant'",
    "Can your card distribute counters onto creatures?": "o:'distribute'",
    "Can you card return permanents or spells from the graveyard?": "o:return o:graveyard",
    "Does your card sacrifice itself and let you draw a card?": "o:'sacrifice ~' and o:'draw a card'",
    "Can you card let you draw two cards at once?": "o:'draw two cards'",
    "Can you card let you draw three cards at once?": "o:'draw three cards'",
    "Can you card let you draw four cards at once?": "o:'draw four cards'",
    "Can you card let you draw five cards at once?": "o:'draw five cards'",
    "Does your card affect how creature can or cannot be regenerated?": "o:'regenerated'",
    "Does your card have a targetted exile effect?": "o:'exile target'",
    "Does your card create Food Tokens?": "o:'create' o:'food'",
    "Does your card create Treasure Tokens?": "o:'create' o:'treasure'",
    "Does your card create Blood Tokens?": "o:'create' o:'blood'",
    "Does your card create tokens of any kind?": "o:create o:token",
    "Is your card an Attraction?": "o:attraction",
    "Does your card care about dice rolls?": "oracletag:dice-roll",
    "Is your card removal?": "oracletag:removal",
    "Does your card have an effect that cares about black creatures?": "o:'black creatures'",
    "Does your card have an effect that cares red creatures?": "o:'red creatures'",
    "Does your card have an effect that cares white creatures?": "o:'white creatures'",
    "Does your card have an effect that cares green creatures?": "o:'green creatures'",
    "Does your card have an effect that cares blue creatures?": "o:'blue creatures'",
    "Does your card generate mana that can only be used for certain types of spells?": "o:'spend this mana only'",
    "Does your card generate mana for only multicolored spells?": "o:'spend this mana only' o:'multicolored spell'",
    "Does your card generate mana for only creature spells?": "o:'spend this mana only' o:'creature spell'",
    "Does your card generate mana for only artifact spells?": "o:'spend this mana only' o:'artifact spell'",
    "Does your card generate mana for only enchantment spells?": "o:'spend this mana only' o:'enchantment spell'",
    "Does your card generate mana for only instant or sorcery spells?": "o:'spend this mana only' o:'instant or sorcery spell'",
    "Does your card reduce the cost of playing spells, or playing itself?": "o:cost o:'less to cast'",
    "Does your card increase the cost of playing spells, or playing itself?": "o:cost o:'more to cast'",
    "Does your card affect your opponent's hand?": "o:'opponent\'s hand' or o:'their hand'",
    "Does your card reveal your opponent's entire hand?": "o:'target player reveals their hand'",
    "Does your card have an effect that places cards into piles?": "o:piles",
    "Does your card have a tap ability?": "o:'{T}'",
    "Does your card deal damage that you can divide among targets?": "o:deal o:damage o:divided",
    "Does your card have a fling effect (sacrifice a creature, damage a target based on sacrificed creatures power/toughness)?": "oracletag:fling",
    "Does your card have an ability that targets creatures?": "o:target o:creature",
    "Does your card have an ability that targets artifacts?": "o:target o:artifact",
    "Does your card have an ability that targets enchantments?": "o:target o:enchantment",
    "Does your card have an ability that targets planeswalkers?": "o:target o:planeswalker",
    "Does your card have an ability that targets instants?": "o:target o:instant",
    "Does your card have an ability that targets sorceries?": "o:target o:sorcery",
    "Does your card have an ability that targets equipment?": "o:target o:equipment",
    
    # Oracletag QUERIES
    "Does your card allow you to impulse draw (exile top card of library and cast this turn)?": "oracletag:impulsive-draw",
    
    # Art QUERIES
    "Does your card have art of a monkey, gorilla, or ape?": "art:monkey or art:gorilla or art:ape",
    "Does your card have a devil, demon, or vampire in the art?": "art:devil or art:demon or art:vampire",
    "Does your card have a goblin, orc, or ogre in its art?": "art:goblin or art:orc or art:ogre",
    "Does your card have a horse in the art?": "art:horse",
    "Does your card art include acid of any kind?": "art:acid",
    "Does your card art include any acrobatics?": "art:acrobat",
    "Does your card art include anybody with their arms crossed?": "art:arms-crossed",
    "Does your card art include an angel?": "art:angel",
    "Does your card art include an arrow?": "art:arrow",
    "Does your card art include an axe?": "art:axe",
    "Does your card art include Liliana the PlanesWalker?": "art:liliana",
    "Does your card art feature Elspeth the PlanesWalker?": "art:elspeth",

    # Banned QUERIES
    "Is your card banned in commander?": "banned:commander",
    "Is your card banned in legacy?": "banned:legacy",

    # Border QUERIES
    "Does your card have a white border?": "border:white",
    "Does your card have a silver border?": "border:silver",
    
    # Flavor Text QUERIES
    "Does your card contain flavor text?": "ft:' '",
    "Does your card have flavor text, that is in quotations?": "has:flavor and ft:'\"'",

    # Keyword QUERIES
    "Does your card proliferate?": "keyword:proliferate", #Karn's Bastion
    "Does your card have the keyword domain?": "keyword:domain",
    "Does your card have storm?": "keyword:storm",
    "Is your card an arcane spell?": "t:arcane",
    "Does your card have madness?": 'keyword:madness',
    "Does your card have a myr in the art?": "art:myr",
    "Is your card a battle?": "type:battle",
    "Does your card have an effect that buffs power or toughness, through effects or counters?": "o:'+'",
    "Does your card allow you to search your library for a card?": "function:tutor",
    "Does your card have devoid?": "keyword:devoid",
    "Does your card have madness?": "keyword:madness",
    "Does your card have protection from something?": "keyword:protection",
    "Does your card have the keyword landfall?": "keyword:landfall",
    
    # Oracletag QUERIES
    "Does your card use energy counters?": "fulloracle:'Energy counter'",
    "Does your card have a delayed replacement effect?": "oracletag:delayed-replacement-effect",
    "Does your card have a delayed triggered ability?": "oracletag:delayed-triggered-ability",
    "Can your card prevent damage?": "oracletag:damage-prevention",
    "Does your card have an effect that involves ability-counters?: (Flying Counter, Reach Counter, Trample Counter...etc)": "oracletag:ability-counter",
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
    "Does your card double counters on creatures, and other permanents?": "oracletag:counter-doubler o:creature",
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
    "Does your card care about monarchs?": "oracletag:monarch",
    
    # Set QUERIES
    "Is your card from an un-set?": "set:und OR set:ust OR set:unh OR set:ugl OR set:unf",
    # ### TAGGER ART QUESTIONS
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