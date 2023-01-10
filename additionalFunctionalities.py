import warnings
import wikipedia
import datetime
from PyDictionary import PyDictionary

dictionary = PyDictionary()
warnings.filterwarnings('ignore')


def dic(dicSearch):
    try:
        dicResults = dictionary.meaning(dicSearch)
        results = dicResults.items()
        return results
    except EOFError as e:
        error = "Sorry, i quite can't  get the meaning of " + dicSearch + " right now."
        return error


def dateTime():
    current_time = datetime.datetime.now().strftime('%I:%M %p')
    return current_time


def wiki(wikiSearch):
    try:
        searchResults = wikipedia.summary(wikiSearch, sentences=2)
        return searchResults
    except EOFError as e:
        error = "Sorry, i can't quite get to wikipedia right now."
        return error


def makeNote(myBotName):
    note = input(myBotName + " Said : \n  What do want to note down? :")
    if note != "":
        done = False
        while not done:
            with open("notes" + '.txt', 'a') as w:
                w.write("\n" + note)
                done = True
                print(myBotName + " Said : \n I have created the note")


def getNote():
    with open("notes" + '.txt', 'r') as w:
        return w.read()