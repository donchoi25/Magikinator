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
            "entropyVector": 1,
            "found": False,
            "guessedCard": "Fury Sliver",
            "entropyNumber": 1,
            "bestCardCandidates": ["Fury Sliver", "Fury Sliver", "Fury Sliver", "Fury Sliver", "Fury Sliver"]
        }
        response = jsonify(data)
        return response
    elif request.method == "POST":
        data = request.json
        previous_answers = list(data.get('Answers'))
        previous_questions = list(data.get('Questions'))
        prev_entropy_vector = data.get('Entropy')
        rejected_cards = list(data.get('RejectedCards'))
        if prev_entropy_vector is None:
            prev_entropy_vector = 1
        else:
            prev_entropy_vector = np.array(prev_entropy_vector)

        most_recent_question = previous_questions[-1]
        most_recent_answer = previous_answers[-1]
        guessed_card, cachethisentropy, foundpotentialcard, bestCards, entropyVal, rejectedCards = frontEnd.responseAnswer(previous_questions, most_recent_question, most_recent_answer, prev_entropy_vector, rejected_cards)
        # (maxCard, cardentropy, found_potential_card, maxCards, entropy, rejected_cards)
        
        bestQuestion = frontEnd.askQuestion(previous_questions, cachethisentropy)
        cachethisentropy = json.dumps(cachethisentropy.tolist())
        rejectedCards = json.dumps(rejectedCards)
        foundpotentialcard = json.dumps(bool(foundpotentialcard))
        bestCards = json.dumps(bestCards)

        data = {
            "bestQuestion": bestQuestion,
            "entropyVector": cachethisentropy,
            "found": foundpotentialcard,
            "guessedCard": guessed_card,
            "bestCardCandidates": bestCards,
            "entropyNumber": entropyVal,
            "rejectedCards": rejectedCards
        }
        response = jsonify(data)
        return response

if __name__ == "__main__":
    app.run()