from src.app import app
from pymongo import MongoClient
from src.config import DBURL
from bson.json_util import dumps
import re

from src.helpers.errorHandler import errorHandler, Error404

client = MongoClient(DBURL)
print(f"Connected to {DBURL}")
db = client.get_default_database()["companies"]


@app.route("/company/<name>")
@errorHandler
def getCompany(name):
    namereg = re.compile(f"^{name}", re.IGNORECASE)
    company = db.find_one({"name":namereg},{"_id":0, "name":1, "home_url":1, "email_address":1})
    print(namereg)
    if not company:
        print("ERROR")
        raise Error404("company not found")
    print("OK")
    return dumps(company)