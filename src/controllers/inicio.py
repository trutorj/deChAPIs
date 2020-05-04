from src.app import app
from flask import render_template

@app.route("/")
def inicio():
    return render_template('miweb.html')