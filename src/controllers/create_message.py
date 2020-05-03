from src.app import app
from pymongo import MongoClient
from src.config import DBURL
from bson.json_util import dumps
from flask import request
from src.helpers.errorHandler import errorHandler, Error404, APIError

client = MongoClient(DBURL)
print(f"Connected to {DBURL}")
db = client.get_default_database()["comments"]

@app.route("/chat/<chat_name>/addmessage")
@errorHandler
def createMessage(chat_name):
    usuario = request.args.get("u")
    mensaje = request.args.get("msg")
    # Extract the id of the chat from chat name
    id_chat = list(db.find({"chatname":chat_name}, {"_id":1}))
    print((id_chat))
    
    # Extract the id of the users
    id_u = list(db.find({"username":usuario}, {"_id":1}))
    print((id_u))
    
    # Create the document and fill it
    mymessage = { 
        "type": "message",
        "chat_id": id_chat[0]["_id"],
        "user_id": id_u[0]["_id"],
        "text": mensaje
    }

    # Insert the document in the database
    x = db.insert_one(mymessage)    
    return {
            "status": "New message created",
            "dbresponse":dumps(x.inserted_id)}
    