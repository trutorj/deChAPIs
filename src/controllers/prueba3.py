from src.app import app
from pymongo import MongoClient
from src.config import DBURL
from bson.json_util import dumps
import re
from src.helpers.errorHandler import errorHandler, Error404, APIError

client = MongoClient(DBURL)
print(f"Connected to {DBURL}")
db = client.get_default_database()["users"]


@app.route("/chat/create")
@errorHandler
def insertUsername(usuarios, nombrechat):
    # Convertir los nombres de usuarios a sus id
    usuarios_id = []
    for e in usuarios:
        id_u = list(db.find({"username":f"{e}"}, {"_id":1}))
        usuarios_id.append(id_u[0])

    mychat = { "type": "chat", "chatname": f"{nombrechat}", "userlist": usuarios_id}
    x = db.insert_one(mychat)    
    return dumps(x.inserted_id)
