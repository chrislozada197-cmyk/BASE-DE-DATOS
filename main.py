from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "FUNCIONA ROOT"

@app.route("/backup")
def backup():
    return "FUNCIONA BACKUP"
``
