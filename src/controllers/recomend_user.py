from src.app import app
import pymongo
from pymongo import MongoClient
from src.config import DBURL
from bson.json_util import dumps
from flask import request
from src.helpers.errorHandler import errorHandler, Error404, APIError
from src.controllers.recomendator import dic_rec

client = pymongo.MongoClient(DBURL)
print(f"Connected to {DBURL}")
# Select the collection
db = client.get_default_database()["comments"]

@app.route("/user/<user_id>/recommend")
@errorHandler
def recomendUser(user_id):    
    # Extract the id of the user from chat name
    u_id = list(db.find({"username": user_id}, {"_id":1}))
    # Check the user exists
    if len(u_id) == 0:
        raise APIError("Username doesn't exists in the dabatabase. Choose another one")   
    else:    
        # Look for the id in the dict, and then in the db to extract the name    
        rec_name = db.find_one({"_id":dic_rec[(u_id[0]["_id"])]})["username"]
        #print(rec_name)
     
        return {
             "status":"Todo OK, José Luís",
            "recommended user": rec_name
        }

    