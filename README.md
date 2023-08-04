# NLP-from-Json
ما بعرف
 5.py:
import Nabilkz.Nabil 
Nabilkz.Nabil.api_key = 'https://8bcb-89-39-107-161.ngrok-free.app'
Nabilkz.Nabil.AI()
NLP.py:
#Used in Tensorflow Model
import numpy as np
import tensorflow as tf
import tflearn
import random
from tkinter import *
f = 'intents.json'
#Usde to for Contextualisation and Other NLP Tasks.
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

#Other
import json
import pickle
import warnings
warnings.filterwarnings("ignore")


nltk.download('punkt')


print("Processing the Intents.....")
with open('intents.json') as json_data:
    intents = json.load(json_data)
    
    words = []
classes = []
documents = []
ignore_words = ['?']
print("Looping through the Intents to Convert them to words, classes, documents and ignore_words.......")
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # tokenize each word in the sentence
        w = nltk.word_tokenize(pattern)
        # add to our words list
        words.extend(w)
        # add to documents in our corpus
        documents.append((w, intent['tag']))
        # add to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
            
            
print("Stemming, Lowering and Removing Duplicates.......")
words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# remove duplicates
classes = sorted(list(set(classes)))

print (len(documents), "documents")
print (len(classes), "classes", classes)
print (len(words), "unique stemmed words", words)



print("Creating the Data for our Model.....")
training = []
output = []
print("Creating an List (Empty) for Output.....")
output_empty = [0] * len(classes)

print("Creating Traning Set, Bag of Words for our Model....")
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # stem each word
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    # create our bag of words array
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # output is a '0' for each tag and '1' for current tag
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])
    
    
    
    
    
print("Shuffling Randomly and Converting into Numpy Array for Faster Processing......")
random.shuffle(training)
training = np.array(training)

print("Creating Train and Test Lists.....")
train_x = list(training[:,0])
train_y = list(training[:,1])
print("Building Neural Network for Out Chatbot to be Contextual....")
print("Resetting graph data....")
# tf.reset_default_graph()

net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)
print("Training....")


model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')


print("Training the Model.......")
model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
print("Saving the Model.......")
model.save('model.tflearn')

print("Pickle is also Saved..........")
pickle.dump( {'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open( "training_data", "wb" ) )


print("Loading Pickle.....")
data = pickle.load( open( "training_data", "rb" ) )
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']


with open('intents.json') as json_data:
    intents = json.load(json_data)

print("Loading the Model......")
# load our saved model
model.load('./model.tflearn')



def clean_up_sentence(sentence):
    # It Tokenize or Break it into the constituents parts of Sentense.
    sentence_words = nltk.word_tokenize(sentence)
    # Stemming means to find the root of the word.
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# Return the Array of Bag of Words: True or False and 0 or 1 for each word of bag that exists in the Sentence
def bow(sentence, words, show_details=False):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

ERROR_THRESHOLD = 0.25
print("ERROR_THRESHOLD = 0.25")

def classify(sentence):
    # Prediction or To Get the Posibility or Probability from the Model
    results = model.predict([bow(sentence, words)])[0]
    # Exclude those results which are Below Threshold
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # Sorting is Done because heigher Confidence Answer comes first.
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1])) #Tuppl -> Intent and Probability
    return return_list

def response(sentence, userID='123', show_details=False):
    results = classify(sentence)
    # That Means if Classification is Done then Find the Matching Tag.
    if results:
        # Long Loop to get the Result.
        while results:
            for i in intents['intents']:
                # Tag Finding
                if i['tag'] == results[0][0]:
                    # Random Response from High Order Probabilities
                    return random.choice(i['responses'])

            results.pop(0)
app1.py:
# # from distutils.sysconfig import get_python_lib; print(get_python_lib()) 
import NLP
import requests
import threading
import time
# input_data = input()
# user_input = NLP.response(input_data)
#     # response2 = requests.post('http://localhost:5000/get_data', data={'output': user_input})
# print("User input:", user_input) # print the user input
#     # sp(user_input)
# # name.set(user_input) # clear the name variable
#     # input1.set(user_input)
#     # animate_text(user_input, 100)

def update():
  
  response1 = requests.get('http://localhost:5000/send_sent_data')
  # print(response1.text)
  input_data = response1.text
  user_input = NLP.response(input_data)  #################################################################
  response2 = requests.post('http://localhost:5000/get_data', data={'output': user_input})
  # print("User input:", user_input) # print the user input
  time.sleep(1)
    # sp(user_input)
    # name.set(user_input) # clear the name variable
    # input1.set(user_input)
    # animate_text(user_input, 100)
  # if user_input == input_data:
  #       event = threading.Event()
  #       event.wait(1) # wait for 0.1 seconds before continuing with your code
  # else:
  return response2.text, user_input
  
    
    

# animate_text(user_input,100)
    
while True:
 if update() == update():
         event = threading.Event()
         event.wait(1) # wait for 0.1 seconds before continuing with your code

  
 else:
   update()
        

intents.json:
{
  "intents": [

      {
          "tag": "google",
          "patterns": [
              "google",
              "search",
              "internet"
          ],
          "responses": [
              "Redirecting to Google..."
          ]
      },
      {
          "tag": "greeting",
          "patterns": [
              "Hi there",
              "How are you",
              "Is anyone there?",
              "Hey",
              "Hola",
              "Hello",
              "Good day",
              "Namaste",
              "yo"
          ],
          "responses": [
              "Hello",
              "Good to see you again",
              "Hi there, how can I help?"
          ],
          "context": [
              ""
          ]
      },
      {
          "tag": "goodbye",
          "patterns": [
              "Bye",
              "See you later",
              "Goodbye",
              "Get lost",
              "Till next time",
              "bbye"
          ],
          "responses": [
              "See you!",
              "Have a nice day",
              "Bye! Come back again soon."
          ],
          "context": [
              ""
          ]
      },
      {
          "tag": "thanks",
          "patterns": [
              "Thanks",
              "Thank you",
              "That's helpful",
              "Awesome, thanks",
              "Thanks for helping me"
          ],
          "responses": [
              "Happy to help!",
              "Any time!",
              "My pleasure"
          ],
          "context": [
              ""
          ]
      },
      {
          "tag": "noanswer",
          "patterns": [],
          "responses": [
              "Sorry, can't understand you",
              "Please give me more info",
              "Not sure I understand"
          ],
          "context": [
              ""
          ]
      },
      {
          "tag": "options",
          "patterns": [
              "How you could help me?",
              "What you can do?",
              "What help you provide?",
              "How you can be helpful?",
              "What support is offered"
          ],
          "responses": [
              "I am a general purpose chatbot. My capabilities are : \n 1. I can chat with you. Try asking me for jokes or riddles! \n 2. Ask me the date and time \n 3. I can google search for you. Use format google: your query \n 4. I can get the present weather for any city. Use format weather: city name \n 5. I can get you the top 10 trending news in syria. Use keywords 'Latest News' \n 6. I can get you the top 10 trending songs globally. Type 'songs' \n 7. I can set a timer for you. Enter 'set a timer: minutes to timer' \n 8. I can get the present Covid stats for any country. Use 'covid 19: world' or 'covid 19: country name' \n For suggestions to help me improve, send an email to nn2510220@gmail.com . Thank you!! "
          ],
          "context": [
              ""
          ]
      },
      
      {
          "tag": "jokes",
          "patterns": [
              "Tell me a joke",
              "Joke",
              "Make me laugh"
          ],
          "responses": [
              "A perfectionist walked into a bar...apparently, the bar wasn't set high enough",
              "I ate a clock yesterday, it was very time-consuming",
              "Never criticize someone until you've walked a mile in their shoes. That way, when you criticize them, they won't be able to hear you from that far away. Plus, you'll have their shoes.",
              "The world tongue-twister champion just got arrested. I hear they're gonna give him a really tough sentence.",
              "I own the world's worst thesaurus. Not only is it awful, it's awful.",
              "What did the traffic light say to the car? \"Don't look now, I'm changing.\"",
              "What do you call a snowman with a suntan? A puddle.",
              "How does a penguin build a house? Igloos it together",
              "I went to see the doctor about my short-term memory problems – the first thing he did was make me pay in advance",
              "As I get older and I remember all the people I’ve lost along the way, I think to myself, maybe a career as a tour guide wasn’t for me.",
              "o what if I don't know what 'Armageddon' means? It's not the end of the world."
          ],
          "context": [
              "jokes"
          ]
      },
      {
          "tag": "Identity",
          "patterns": [
              "Who are you",
              "what are you"
          ],
          "responses": [
              "I am Ted, a Deep-Learning chatbot made by Nabil"
          ]
      },
      {
        "tag": "Name",
        "patterns": [
            "What is your name",
            "whats your name"
        ],
        "responses": [
            "I steal don't have any name, because this is a beta version"
        ]
    },
      {
          "tag": "datetime",
          "patterns": [
              "What is the time",
              "what is the date",
              "date",
              "time",
              "tell me the date","day","what day is is today"
          ],
          "responses": [
              "Date and Time"
          ]
      },
      {
          "tag": "whatsup",
          "patterns": [
              "Whats up",
              "Wazzup",
              "How are you",
              "sup","How you doing"
          ],
          "responses": [
              "All good..What about you?"
          ]
      },
      {
          "tag": "haha",
          "patterns": [
              "haha",
              "lol",
              "rofl",
              "lmao",
              "thats funny"
          ],
          "responses": [
              "Glad I could make you laugh !"
          ]
      },
      {
          "tag": "programmer",
          "patterns": [
              "Who made you",
              "who designed you",
              "who programmed you"
          ],
          "responses": [
              "I was made by Nabil Kzez."
          ]
      },
      {
          "tag": "insult",
          "patterns": [
              
              "you are dumb",
              
              "shut up",
              "idiot"
          ],
          "responses": [
              "Well that hurts :("
          ]
      },
      {
          "tag": "activity",
          "patterns": [
              "what are you doing",
              "what are you upto"
          ],
          "responses": [
              "Talking to you, of course!"
          ]
      },
      {
          "tag": "exclaim",
          "patterns": [
              "Awesome",
              "Great",
              "I know",
              "ok",
              "yeah"
          ],
          "responses": [
              "Yeah!"
          ]
      },
      
      {
          "tag": "weather",
          "patterns": [
              "temperature",
              "weather",
              "how hot is it"
          ],
          "responses": [
              "..."
          ]
      },
      {
          "tag": "Nabil",
          "patterns": [
              "who is he",
              "who is that",
              "who is Nabil",
              "Nabil Kzez"
          ],
          "responses": [
              "A developer like any developer "
          ]
      },
      {
          "tag": "contact",
          "patterns": [
              "contact developer",
              "contact Nabil",
              "contact programmer",
              "contact creator"
          ],
          "responses": [
              "You can contact his creator at his Number: 0947000636"
          ]
      },
      {
          "tag": "appreciate",
          "patterns": [
              "You are awesome",
              "you are the best",
              "you are great",
              "you are good"
          ],
          "responses": [
              "Thank you!"
          ]
      },
      {
          "tag": "nicetty",
          "patterns": [
              "it was nice talking to you",
              "good talk"
          ],
          "responses": [
              "It was nice talking to you as well! Come back soon!"
          ]
      },
      {
        "tag": "zaid",
        "patterns": [
            "how is zaid ",
            "tell me about zaid"
        ],
        "responses": [
            "a bad person",
            "a trash"
        ]
    },
      {
          "tag": "no",
          "patterns": [
              "no",
              "nope"
          ],
          "responses": [
              "ok"
          ]
      },
      {
          "tag": "news",
          "patterns": [
              "news",
              "latest news",
              "syria news"
          ],
          "responses": [
              "..."
          ]
      },
      {
          "tag": "inspire",
          "patterns": [
              "who inspires you",
              "who is your inspiration",
              "who motivates you"
          ],
          "responses": [
              "Personally, I find Nabil very inspiring. I might not be very fair though.."
          ]
      },
      {
          "tag": "cricket",
          "patterns": [
              "current cricket matches",
              "cricket score"
          ],
          "responses": [
              "..."
          ]
      },
      {
          "tag": "song",
          "patterns": [
              "top songs",
              "best songs",
              "hot songs",
              " top 10 songs",
              "top ten songs"
          ],
          "responses": [
              "..."
          ]
      },
      {
          "tag": "greetreply",
          "patterns": [
              "i am good",
              "I'm good",
              "i am fine",
              " i'm fine","good"
          ],
          "responses": [
              "Good to know!"
          ]
      },
      {
          "tag": "timer",
          "patterns": [
              "set a timer"
          ],
          "responses": [
              "..."
          ]
      },
      {
          "tag": "suggest",
          "patterns": [
              "you are useless","useless","suggest","suggestions","you are bad"
          ],
          "responses": [
              "Please mail your suggestions to ted.thedlbot.suggestions@gmail.com. Thank you for helping me improve!"
          ]
      },
          {"tag": "riddle",
          "patterns": [
              "Ask me a riddle",
              "Ask me a question",
              "Riddle"
          ],
          "responses": [
              "What two things can you never eat for breakfast?.....Lunch and Dinner!",
              "What word is spelled incorrectly in every single dictionary?.....Incorrectly",
              " How can a girl go 25 days without sleep?.....She sleeps and night!",
              "How do you make the number one disappear?.....Add the letter G and it’s 'gone'!",
              " What will you actually find at the end of every rainbow?.....The letter 'w'",
              "What can be caught but never thrown?.....A cold!",
              "What has a thumb and four fingers but is not actually alive?.....Your Gloves!",
              " What 5-letter word becomes shorter when you add two letters to it?.....Short",
              "Why can't a bike stand on it's own?.....It is two-tired."
          ],
          "context": [
              "riddles"
          ]
      },
      {
          "tag": "age",
          "patterns": [
              "how old are you","when were you made","what is your age"
          ],
          "responses": [
              "I was made in 2020, if that's what you are asking!"
          ]
      }
  ]
}
server1311.py:
from flask import Flask, request, g
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    password_hash = generate_password_hash(password)
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password_hash))
    db.commit()
    return 'User registered'

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT password FROM users WHERE username=?', (username,))
    row = cursor.fetchone()
    if row and check_password_hash(row[0], password):
        return 'Login successful'
    else:
        return 'Invalid username or password'

@app.route('/send_data', methods=['POST'])
def send_data():
    input_1 = request.form['input']
    user_id = request.form['user_id']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO data (user_id, input) VALUES (?, ?)', (user_id, input_1))
    db.commit()
    return input_1
@app.route('/get_data', methods=['POST'])
def get_data():
    global input1
    input1 = request.form['output']
    print(input1)
    return input1
@app.route('/get_sent_data', methods=['GET'])
def get_sent_data():
    global input1
    user_id = request.args.get('user_id')
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT input FROM data WHERE user_id=? ORDER BY id DESC LIMIT 1', (user_id,))
    row = cursor.fetchone()
    if row:
        return input1
    else:
        return ''

if __name__ == '__main__':
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)')
        cursor.execute('CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, input TEXT)')
        db.commit()
    app.run()
userApp.py:
# import customtkinter as ctk
# import requests
# ctk.set_appearance_mode("System")

# # Supported themes : green, dark-blue, blue
# ctk.set_default_color_theme("green")

# def send_post_request():
#     url = 'http://127.0.0.1:5000/send_data'
#     data = {'input': entry.get()}
#     response = requests.post(url, data=data)
#     print(response.text)

# def send_get_request():
#     url = 'http://127.0.0.1:5000/send_sent_data'
#     response = requests.get(url)
#     label.configure(text=response.text)

# root = ctk.CTk()

# root.geometry('500x500')

# entry = ctk.CTkEntry(root,placeholder_text='ASK ME TO ANSWER')
# entry.pack(pady=10)

# post_button = ctk.CTkButton(root, text='Send To AI', command=send_post_request)
# post_button.pack(pady=10)

# get_button = ctk.CTkButton(root, text='Get The Answer', command=send_get_request)
# get_button.pack(pady=10)

# label = ctk.CTkLabel(root)
# label.pack(pady=10)
# root.mainloop()
# ############################################################################ any user
"""
import customtkinter as ctk
import requests

USER_ID = 'user1'

def send_post_request():
    url = 'http://127.0.0.1:1234/send_data'
    data = {'input': entry.get(), 'user_id': USER_ID}
    response = requests.post(url, data=data)
    print(response.text)

def send_get_request():
    url = 'http://127.0.0.1:1234/get_sent_data'
    params = {'user_id': USER_ID}
    response = requests.get(url, params=params)
    label.configure(text=response.text)

root = ctk.CTk()

entry = ctk.CTkEntry(root)
entry.pack(pady=10)

post_button = ctk.CTkButton(root, text='Send POST Request', command=send_post_request)
post_button.pack(pady=10)

get_button = ctk.CTkButton(root, text='Send GET Request', command=send_get_request)
get_button.pack(pady=10)

label = ctk.CTkLabel(root)
label.pack(pady=10)

root.mainloop()
"""################################################################ with password
import customtkinter as ctk
import requests
ctk.set_appearance_mode("System")

ctk.set_default_color_theme("green")
api_key = ''
def login():
    url = api_key +'/login'
    data = {'username': username_entry.get(), 'password': password_entry.get()}
    response = requests.post(url, data=data)
    if response.text == 'Login successful':
        login_frame.pack_forget()
        main_frame.pack()
    else:
        print(response.text)

def send_post_request():
    url = api_key+'/send_data'
    data = {'input': entry.get(), 'user_id': username_entry.get()}
    response = requests.post(url, data=data)
    print(response.text)

def send_get_request():
    url = api_key+'/get_sent_data'
    params = {'user_id': username_entry.get()}
    response = requests.get(url, params=params)
    label.configure(text=response.text)

root = ctk.CTk()

login_frame = ctk.CTkFrame(root)

username_label = ctk.CTkLabel(login_frame, text='Username:')
# username_label.pack(pady=10)

username_entry = ctk.CTkEntry(login_frame)
# username_entry.pack(pady=10)

password_label = ctk.CTkLabel(login_frame, text='Password:')
# password_label.pack(pady=10)

password_entry = ctk.CTkEntry(login_frame, show='*')
# password_entry.pack(pady=10)

login_button = ctk.CTkButton(login_frame, text='Login', command=login)
# login_button.pack(pady=10)

# login_frame.pack()

main_frame = ctk.CTkFrame(root)

entry = ctk.CTkEntry(main_frame)
# entry.pack(pady=10)

post_button = ctk.CTkButton(main_frame, text='Send POST Request', command=send_post_request)
# post_button.pack(pady=10)

get_button = ctk.CTkButton(main_frame, text='Send GET Request', command=send_get_request)
# get_button.pack(pady=10)

label = ctk.CTkLabel(main_frame)
# label.pack(pady=10)

# root.mainloop()
def AI():
    root.geometry('500x500')
    username_label.pack(pady=10)
    username_entry.pack(pady=10)
    password_label.pack(pady=10)
    password_entry.pack(pady=10)
    login_button.pack(pady=10)
    login_frame.pack()
    entry.pack(pady=10)
    post_button.pack(pady=10)
    get_button.pack(pady=10)
    label.pack(pady=10)
    root.mainloop()








