# Magikinator

Magic card predicting app that wil attempt to determine what card you're thinking about by asking yes or no questions. 

Uses Bayes' theorem to determine the probability that the card is the answer based on previous answers to questions given.

Next best question is picked based on which question will decrease the entropy the most on average.


How to download cardsdata.json:
Go and download https://data.scryfall.io/default-cards/default-cards-20230607210803.json. Put it in the data/files folder.