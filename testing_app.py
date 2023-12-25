from frontend import frontendapi
from tabulate import tabulate
from globals.constants import cardcsv_dataframe as df
import os.path

# Files to save test data to
TEST_CARDS_PATH = "./data/files/test/simulate_game_allcards.txt"
LAST_CARD_PATH = "./data/files/test/last_card.txt"
QUESTIONS_PATH = "./data/files/questions_analysis.txt"
FAILED_PATH = "./data/files/failed_cards.txt"

# Testing parameters
CARD_LIMIT_PER_RUN = float('inf')
HOW_OFTEN_TO_SAVE = 4
MAX_QUESTIONS_TO_ASK = 50
# Saving Progress (Optional)
SPECIFIC_CARD_TO_START_FROM = None

# Initialize the frontEnd
frontEnd = frontendapi.FrontEnd()
question_cols = df.columns

def simulateGameForAllCards(print_to_console=False):
    index = 0
    failed_cards = {}
    continuing_card = SPECIFIC_CARD_TO_START_FROM
    # This gets the first line of the test file, which tracks the last card we ran the test on.
    if os.path.exists(LAST_CARD_PATH):
        with open(LAST_CARD_PATH, 'r') as file:
            try:
                firstline = file.readline().strip('\n')
                if not df.loc[firstline].empty:
                    print("Continuing test from card: " + firstline)
                    continuing_card = firstline
            except KeyError as e:
                print(f"We did not find a card with the name {str(e)} to continue from. \n Starting test from scratch.")
            file.close()
    else:
        with open(LAST_CARD_PATH, "w") as file:
            file.write("Fury Sliver")
            file.close()
        print("Creating a new last_card.txt file.")

    # If we have a valid card to continue from, we'll iterate to that card before continuing our tests.

    skip_to_continue = True
    
    # We append a delimiter here, in order to parse through the text file later for analysis
    delimiter_list = ['@'] * MAX_QUESTIONS_TO_ASK
    with open(TEST_CARDS_PATH, 'a') as file:
        for name, card_row in df.iterrows():
            if continuing_card != None and skip_to_continue:
                if name.lower() == continuing_card.lower():
                    skip_to_continue = False
                    index += 1
                else:
                    index += 1    
                    continue
            
            response = simulateQuestionsForCard(name, card_row)
            success = response[0] == name
            minor_success = len(response[5]) > 0

            print(f"Test #{str(index)} for {name} {'SUCCEEDED' if success else 'FAILED'} after {str(len(response[1]))} questions.\n")
            if not success and minor_success:
                print(f"Minor Success, as {name} was found in top cards in rounds {', '.join(minor_success)}.\n")
            if print_to_console:
                print(f"Question | Answer | Cards Guessed | Best Cards Guessed \n")
                print(tabulate(zip(response[1], response[2], response[3], response[4])))

            file.write('\n')
            file.write(f"Test #{str(index)} for {name} {'SUCCEEDED' if success else 'FAILED'} after {str(len(response[1]))} questions.\n")
            if not success and minor_success:
                file.write(f"Minor Success, as {name} was found in top cards in rounds {', '.join(minor_success)}.\n")
            file.write(f"Question | Answer | Cards Guessed | Best Cards Guessed \n")
            file.write(tabulate(zip(response[1], response[2], response[3], response[4])))
            file.write('\n')

            if not success:
                with open(FAILED_PATH, 'a') as f:
                    f.write(f"{name} | {response[3][-1]}\n")
                    f.close()

            index += 1
            if index % HOW_OFTEN_TO_SAVE == 0:
                with open(LAST_CARD_PATH, "w") as f:
                    f.seek(0, 0)
                    f.write(name)
                    print("Saved progress up to " + name)
                    f.close()
            
            if index >= CARD_LIMIT_PER_RUN:
                break

        file.close()

def simulateQuestionsForCard(card_name, card_data):
    questions_asked = []
    answers_given = []
    cards_guessed = []
    best_cards_guessed = []
    cached_entropy_vector = 1
    was_seen = []
    response = (None, cached_entropy_vector, None)
    while response[0] != card_name and len(questions_asked) < MAX_QUESTIONS_TO_ASK:
        bestQuestion = frontEnd.askQuestion(questions_asked, cached_entropy_vector)
        answer = getAnswerForCard(card_data, bestQuestion)
        response = frontEnd.responseAnswer(questions_asked, bestQuestion, answer, cached_entropy_vector, [])
        cached_entropy_vector = response[1]
        questions_asked.append(bestQuestion)
        answers_given.append(answer)
        cards_guessed.append(response[0])
        best_cards_guessed.append(response[3])
        if card_name in best_cards_guessed:
            was_seen.append(len(questions_asked))
    return (response[0], questions_asked, answers_given, cards_guessed, best_cards_guessed, was_seen)

def getAnswerForCard(card_data, question):
    ANSWERS = ["YES", "NO", "MAYBE"]
    best_answer = None
    best_answer_val = float("-inf")
    for answer in ANSWERS:
        answer_val = card_data[question + "#" + answer]
        if answer_val >= best_answer_val:
            best_answer = answer
            best_answer_val = answer_val
    return best_answer

def get_most_common_questions():
    return
        
simulateGameForAllCards()