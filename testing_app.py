from frontend import frontendapi
from globals.constants import cardcsv_dataframe

# Initialize the frontEnd
frontEnd = frontendapi.FrontEnd()
df = cardcsv_dataframe
question_cols = df.columns

def simulateGameForAllCards(print_to_console=False):
    CARD_LIMIT = 100
    index = 0
    failed_cards = {}
    for name, card_row in df.iterrows():
        print('\n')
        print("DOING TEST RUN FOR CARD " + name)

        response = simulateQuestionsForCard(name, card_row)
        success = response[2] == name

        print(f'Test run finished with a {"SUCCESS" if success else "FAILURE"} AFTER {str(len(response[0]))} QUESTIONS')
        print('\n')
        if print_to_console:
            print("MAGIKINATOR GUESSED " + response[2] + " AFTER " + str(len(response[0])) + " TRIES, WHEN WE LOOKED FOR " + name)
            print("HERE ARE THE QUESTIONS WE ASKED: ")
            print(response[0])
            print("HERE ARE THE ANSWERS WE GAVE: ")
            print(response[1])
            print("################################")
        if index >= CARD_LIMIT:
            return
        index += 1

        if not success:
            failed_cards[name] = response
        
    print(str(len(failed_cards.keys)) + " CARDS FAILED!")
    print(failed_cards)

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

# print(cardcsv_dataframe.columns)
# print(cardcsv_dataframe.loc['Fury Sliver'])