from flask import Flask
from flask import request
from frontend import frontendapi

app = Flask(__name__)
frontEnd = frontendapi.FrontEnd()

@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/guess', methods = ['GET', 'POST'])
def guess_card():
    if request.method == "GET":
        return "<p>You made a get request to the guess endpoint. Try a post instead.</p>"
    if request.method == "POST":
        data = request.json
        # TODO: First we should get an answer from the player. Everytime we check whether the answer returned by the player gives us 
        # enough confidence to answer them with the card we think they have.
        previous_answers = data.get('Answers')
        previous_questions = data.get('Questions')
        prev_entropy_vector = data.get('Entropy')
        # TODO Process the next question to ask.
        if not prev_entropy_vector:
            prev_entropy_vector = 1
        else:
            prev_entropy_vector = list(prev_entropy_vector)

        # TODO Process their most recent answer.
        if len(previous_answers) > 0:
            most_recent_question = previous_questions[-1]
            most_recent_answer = previous_answers[-1]
            answer = frontEnd.responseAnswer(previous_questions, most_recent_question, most_recent_answer, prev_entropy_vector)
            if answer:
                return f"<p> Your card is {answer} </p>"
        
        bestQuestion, newEntropyVal = frontEnd.askQuestion(previous_questions, prev_entropy_vector)
        return f"<p>{bestQuestion}: {newEntropyVal}</p>"
    
if __name__ == "__main__":
    app.run()