from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "OK ROOT FUNCIONA"

@app.route("/backup")
def backup():
    return "OK BACKUP FUNCIONA"
``
