import tflearn
import random
import json
import numpy as np
import pickle
import nltk
from additionalFunctionalities import wiki, getNote, makeNote, dic, dateTime
from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
from keras.models import Sequential
from nltk.stem.lancaster import LancasterStemmer
from starlette.responses import RedirectResponse

classifier = Sequential()
stemmer = LancasterStemmer()
nltk.download('punkt')

with open('Intent.json') as file:
    data = json.load(file)

with open("data.pickle", "rb") as f:
    words, labels, training, output = pickle.load(f)

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net, tensorboard_verbose=0)

model.load("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return np.array(bag)


def chatBot(inputUser):
    idk = ["Sorry I didn't understand you correctly.I'm still learning. could you ask another question?", "I may "
                                                                                                          "misinterpret things from time to time This time i don't seem to understand you",
           "I don't quite understand what you just said could you please ask another question?"]
    modelResults = model.predict([bag_of_words(inputUser, words)])[0]
    modelResultsIndex = np.argmax(modelResults)
    tag = labels[modelResultsIndex]

    if modelResults[modelResultsIndex] > 0.94:
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
                reply = random.choice(responses)
                return reply
    else:
        return random.choice(idk)


app = FastAPI(title='Companion chat-bot system')

origins = [
    'http://localhost:3000', 'https://pisciumweb.web.app'
    ]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],)

with open('bot.txt', 'r') as bn:
    myBotName = bn.read()


@app.get("/", include_in_schema=False)
def home():
    return RedirectResponse(url="/docs")


@app.get("/chat")
def chat(userInput: str, myUsername: str):
    if 'time' in userInput.lower():
        return 'The current time is ' + dateTime()

    elif 'wiki' in userInput.lower():
        return wiki(userInput.lower().replace('wiki', ''))

    elif 'meaning' in userInput.lower():
        dit = userInput.lower().replace('meaning', '')
        results = dic(dit)
        for key, value in results:
            return key, " : ", value

    elif 'get my note' in userInput.lower():
        getNote()

    else:
        res = chatBot(userInput.lower())
        if 'human' in res:
            return res.replace('human', myUsername)

        elif 'bName' in res:
            return res.replace('bName', myBotName)

        else:
            return res
