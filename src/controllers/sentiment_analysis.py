from src.app import app
from pymongo import MongoClient
from src.config import DBURL
from bson.json_util import dumps
from flask import request
from src.helpers.errorHandler import errorHandler, Error404, APIError
from nltk.sentiment.vader import SentimentIntensityAnalyzer

client = MongoClient(DBURL)
print(f"Connected to {DBURL}")
# Select the collection
db = client.get_default_database()["comments"]

@app.route("/chat/<chat_name>/sentiment")
@errorHandler
def extracSentiments(chat_name):
    # Extract the id of the chat from chat name
    id_chat = list(db.find({"chatname":chat_name}, {"_id":1}))[0]
    #print(id_chat[0]["_id"])
    id_chat["_id"]
    
    # Lok for all the messages in that chat
    messages = list(db.find({"$and":[{"type": "message"},{"chat_id":id_chat["_id"]}]}))
    #print(messages)
    lista_msg = [e["text"] for e in messages]

    # Analize each message and store its score in a dictionary. Append them in a list
    results = []
    for i in range(len(lista_msg)):
        results.append({
            "message": lista_msg[i],
            "polarity": SentimentIntensityAnalyzer().polarity_scores(lista_msg[i])
        })


     
    return {
        "Sentiment Analysis Results":results
        }

    