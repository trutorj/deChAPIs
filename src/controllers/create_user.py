from src.app import app
import pymongo
from pymongo import MongoClient
from src.config import DBURL
from bson.json_util import dumps
from src.helpers.errorHandler import errorHandler, Error404, APIError

client = pymongo.MongoClient(DBURL)
print(f"Connected to {DBURL}")
# Select the collection
db = client.get_default_database()["comments"]


@app.route("/users/create/<username>")
@errorHandler
def insertUsername(username):
    # Check that username is not in the db
    # Do a query of the name
    query = list(db.find({"username":f"{username}"}))
    if len(query) > 0:
        print("Error")
        raise APIError("Username exists in the dabatabase. Choose another one")   
    else:
        myuser = {"username": f"{username}"}
        x = db.insert_one(myuser)    
        return {
            "status": "New user created",
            "dbresponse":dumps(x.inserted_id)}
    
