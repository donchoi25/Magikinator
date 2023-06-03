from frontend import frontendapi
from data import datainit
def run_program():
    # Use a breakpoint in the code line below to debug your script.
    datainit.initializeData()
    frontEnd = frontendapi.FrontEnd()
    frontEnd.findAnswer()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_program()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
