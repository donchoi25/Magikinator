import pandas as pd

PATH_TO_DATABASE_CSV = "data/files/cardsdata_live.csv"

class DatabaseParser():
    def __init__(self):
        self.data = pd.read_csv(PATH_TO_DATABASE_CSV)
    
    def get_total_number_of_rows(self):
        return self.data.shape[0]
    
    def get_list_of_questions(self):
        return self.data.columns