from flask import Flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from frontend import frontendapi
import json
import numpy as np

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
frontEnd = frontendapi.FrontEnd()

@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/guess', methods = ["GET", "POST"])
@cross_origin(origin='*', headers='Content-Type')
def guess_card():
    if request.method == "GET":
        bestQuestion = frontEnd.askQuestion([], 1)
        data = {
            "bestQuestion": bestQuestion,
            "entropyValue": 1,
            "found": False,
            "guessedCard": ""
        }
        response = jsonify(data)
        return response
    elif request.method == "POST":
        data = request.json
        # TODO: First we should get an answer from the player. Everytime we check whether the answer returned by the player gives us 
        # enough confidence to answer them with the card we think they have.
        previous_answers = list(data.get('Answers'))
        previous_questions = list(data.get('Questions'))
        prev_entropy_vector = data.get('Entropy')
        # print(previous_answers)
        # print(previous_questions)
        # print(type(prev_entropy_vector))
        # TODO Process the next question to ask.
        if prev_entropy_vector is None:
            print("FIRST QUESTION SO PREV_ENTROPY_VECTOR IS DEFAULTED TO 1")
            prev_entropy_vector = 1
        else:
            prev_entropy_vector = np.array(prev_entropy_vector)

        # TODO Process their most recent answer.
        most_recent_question = previous_questions[-1]
        most_recent_answer = previous_answers[-1]
        guessed_card, cachethisentropy, foundpotentialcard = frontEnd.responseAnswer(previous_questions, most_recent_question, most_recent_answer, prev_entropy_vector)
        
        bestQuestion = frontEnd.askQuestion(previous_questions, cachethisentropy)
        cachethisentropy = json.dumps(cachethisentropy.tolist())
        foundpotentialcard = json.dumps(bool(foundpotentialcard))

        data = {
            "bestQuestion": bestQuestion,
            "entropyValue": cachethisentropy,
            "found": foundpotentialcard,
            "guessedCard": guessed_card
        }
        response = jsonify(data)
        return response

if __name__ == "__main__":
    app.run()