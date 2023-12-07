from frontend import frontendapi
from tabulate import tabulate
from globals.constants import cardcsv_dataframe as df
import os.path

# Files to save test data to
TEST_CARDS_PATH = "./data/files/test/simulate_game_allcards.txt"
LAST_CARD_PATH = "./data/files/test/last_card.txt"

# Testing parameters
CARD_LIMIT = 10
HOW_OFTEN_TO_SAVE = 4

# Initialize the frontEnd
frontEnd = frontendapi.FrontEnd()
question_cols = df.columns

def simulateGameForAllCards(print_to_console=False):
    index = 0
    failed_cards = {}
    continuing_card = None
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
    with open(TEST_CARDS_PATH, 'a') as file:
        for name, card_row in df.iterrows():
            if continuing_card != None and skip_to_continue:
                if name.lower() == continuing_card.lower():
                    skip_to_continue = False
                    index += 1
                continue
            
            response = simulateQuestionsForCard(name, card_row)
            success = response[2] == name

            print(f"Test #{str(index)} for {name} {'SUCCEEDED' if success else 'FAILED'} after {str(len(response[0]))} questions.\n")
            if print_to_console:
                print(f"Questions | Answers\n")
                print(tabulate(zip(response[0], response[1])))

            file.write('\n')
            file.write(f"Test #{str(index)} for {name} {'SUCCEEDED' if success else 'FAILED'} after {str(len(response[0]))} questions.\n")
            file.write(f"Questions | Answers\n")
            file.write(tabulate(zip(response[0], response[1])))
            file.write('\n')

            index += 1
            if index % HOW_OFTEN_TO_SAVE == 0:
                with open(LAST_CARD_PATH, "w") as f:
                    f.seek(0, 0)
                    f.write(name)
                    print("Saved progress up to " + name)
                    f.close()
            
            if index >= CARD_LIMIT:
                break

        file.close()

    # if not success:
    #     failed_cards[name] = response
        
    # print(str(len(failed_cards.keys)) + " CARDS FAILED!")
    # print(failed_cards)

def simulateQuestionsForCard(card_name, card_data):
    MAX_QUESTIONS_TO_ASK = 40
    questions_asked = []
    answers_given = []
    response = (None, 1, None)
    while response[0] != card_name and len(questions_asked) < MAX_QUESTIONS_TO_ASK:
        bestQuestion = frontEnd.askQuestion(questions_asked, 1)
        answer = getAnswerForCard(card_data, bestQuestion)
        response = frontEnd.responseAnswer(questions_asked, bestQuestion, answer, response[1])
        questions_asked.append(bestQuestion)
        answers_given.append(answer)
    return (questions_asked, answers_given, response[0])

def getAnswerForCard(card_data, question):
    ANSWERS = ["YES", "NO", "MAYBE"]
    best_answer = None
    best_answer_val = float("-inf")
    for answer in ANSWERS:
        answer_val = card_data[question + "#" + answer]
        if answer_val > best_answer_val:
            best_answer = answer
            best_answer_val = answer_val
    return best_answer
        
simulateGameForAllCards()