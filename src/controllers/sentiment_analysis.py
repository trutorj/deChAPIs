from src.app import app
import pymongo
from pymongo import MongoClient
from src.config import DBURL
from bson.json_util import dumps
from flask import request
from src.helpers.errorHandler import errorHandler, Error404, APIError
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

client = pymongo.MongoClient(DBURL)
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

    # Analize the message and store in a list
    sentiment_list = [SentimentIntensityAnalyzer().polarity_scores(e) for e in lista_msg]

    # Calculate the mean compound of the whole chat
    # Extract the compound component
    compound_list = []
    for e in sentiment_list:
        for k,v in e.items():
            if k == "compound":
                compound_list.append(v)
    # Calculate the mean
    compound_mean = sum(compound_list) / len(compound_list)
    # Classify the value of compound metric 
    sentiment_chat = ""
    if compound_mean >= 0.05:
        sentiment_chat = "Positive"
    elif compound_mean > -0.05 and compound_mean <0.05:
        sentiment_chat = "Neutral"
    else:
        sentiment_chat = "Negative"

    # Create a dictionary to serve each message and its valoration
    results = []
    for i in range(len(lista_msg)):
        results.append({
            "message": lista_msg[i],
            "polarity": sentiment_list[i]
        })
    
    return {
        "Chat overall sentiment": f"The overall sentiment of the chat is {sentiment_chat} with a mean compound of {compound_mean}",
        "Sentiment Analysis Results":results
        }
