from src.app import app
import pymongo
from pymongo import MongoClient
from src.config import DBURL
from bson.json_util import dumps
from flask import request
from src.helpers.errorHandler import errorHandler, Error404, APIError

client = pymongo.MongoClient(DBURL)
print(f"Connected to {DBURL}")
# Select the collection
db = client.get_default_database()["comments"]

@app.route("/chat/<chat_name>/list")
@errorHandler
def extractList(chat_name):
    # Check if chat is in the data base
    # Do a query of the name of the chat. 
    query = list(db.find({"chatname": chat_name})) 
    #print(query)
    if len(query) == 0:
        raise APIError("Chat doesn't exists in the dabatabase. Please, chose another name or create the chat.") 
    else: 
        # Extract the id of the chat from chat name
        id_chat = list(db.find({"chatname":chat_name}, {"_id":1}))[0]
        #print(id_chat[0]["_id"])
        #id_chat["_id"]
    
        # Lok for all the messages in that chat
        messages = list(db.find({"$and":[{"type": "message"},{"chat_id":id_chat["_id"]}]}))
        total = len(messages)
        #print(messages)
        lista_msg = [e["text"] for e in messages]
     
        return {
            "status":f"{total} messages found in the chat",
            "list":lista_msg
            }

    