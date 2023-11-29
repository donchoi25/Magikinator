# Magikinator

Magic card predicting app that wil attempt to determine what card you're thinking about by asking yes or no questions. 

Uses Bayes' theorem to determine the probability that the card is the answer based on previous answers to questions given.

Next best question is picked based on which question will decrease the entropy the most on average.

To setup the backend: 

1. Run the Datascript.py file in order to generate the necessary CSV file for the backend.
   Call 'python datascript.py' (This can take about 10 - 15 minutes)

2. Once the data/files/cardsdata_live.csv file has been successfully generated from Step 1, begin the 
   service on port 5000, by cd'ing to the root directory and running the command 
   'python -m flask run --debug -p 5000'

3. The backend service should successfully be running on Port 5000. 

4. Clone the Magikinator Frontend Application from https://github.com/danieljaeim/magikinator-frontend

5. Setup the Frontend application by going into the root director of magikinator-frontend. 
    Run 'npm install' if this is the first time running the frontend
    Then run 'npm run dev', and this should allow you to run a local version of the frontend application.

