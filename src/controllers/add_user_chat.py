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

@app.route("/chat/<chat_id>/adduser")
@errorHandler
def addUserChat(chat_id):
    usuarios = (request.args.getlist('u'))
    # Extract the id of the users
    usuarios_id = []
    for e in usuarios:
        print(e)
        id_u = list(db.find({"username":e}, {"_id":1}))
        print(id_u[0])
        usuarios_id.append(id_u[0]["_id"])
    
    x = db.update_one({"chatname": chat_id}, {"$push": {"userlist": {"$each": usuarios_id } } })
    return {
        "status": f"Added user {usuarios} to the chat {chat_id}"
        }


    