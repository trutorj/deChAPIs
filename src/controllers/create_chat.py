from src.app import app
from pymongo import MongoClient
from src.config import DBURL
from bson.json_util import dumps
from flask import request
from src.helpers.errorHandler import errorHandler, Error404, APIError

client = MongoClient(DBURL)
print(f"Connected to {DBURL}")
# Select the collection
db = client.get_default_database()["comments"]

@app.route("/chat/create")
@errorHandler
def createChat():
    chat = request.args.get("n_chat")
    usuarios = (request.args.getlist('u'))

    # Check if chat and user is not in the data base
    # Do a query of the name of the chat. 
    query = list(db.find({"chatname": chat}))
    # Do a query if user exists.
    for e in usuarios:
        #print(e)
        names = list(db.find({"username": e}))
        #print("nombres",len(names))
    
    # Conditions
    if len(query) > 0:
        raise APIError("Chat already exists in the dabatabase. Please, chose another name or add the users to a existing chat.")   
        # Do a query if user exists, if does not, raise an error
    else:
        if len(names) == 0:         
            raise APIError("User doesn't exist. You need to creat it first.")
        else:
            # Extract the id of the users
            usuarios_id = []
            for e in usuarios:
                #print(e)
                id_u = list(db.find({"username":e}, {"_id":1}))
                #print(id_u[0])
                usuarios_id.append(id_u[0]["_id"])
    
            mychat = { "type": "chat", "chatname": chat, "userlist": usuarios_id}
            x = db.insert_one(mychat)    
            return {
                    "status": "New chat created",
                    "dbresponse":dumps(x.inserted_id)}
