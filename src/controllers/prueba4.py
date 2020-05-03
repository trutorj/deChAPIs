from src.app import app
from pymongo import MongoClient
from src.config import DBURL
from bson.json_util import dumps
from flask import request
from src.helpers.errorHandler import errorHandler, Error404, APIError

client = MongoClient(DBURL)
print(f"Connected to {DBURL}")
db = client.get_default_database()["users"]


@app.route("/prueba")
@errorHandler
def hello():
    u = str(request.args.getlist('u'))
    return {
            "saludo": f"Hola {u}"
        }