from src.app import app
from pymongo import MongoClient
from src.config import DBURL
from bson.json_util import dumps
import re

from src.helpers.errorHandler import errorHandler, Error404

client = MongoClient(DBURL)
print(f"Connected to {DBURL}")
db = client.get_default_database()["users"]


@app.route("/users/<name>")
@errorHandler
def getCompany(name):
    nombreusuario = db.find_one({"username":name},{"_id", "username"})
    
    if not nombreusuario:
        print("ERROR")
        raise Error404("company not found")
    print("OK")
    return dumps(nombreusuario)