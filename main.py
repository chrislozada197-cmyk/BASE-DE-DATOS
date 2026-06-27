from flask import Flask, jsonify
import smtplib
from email.message import EmailMessage
import json

app = Flask(__name__)

EMAIL = "chrislozada197@gmail.com"
APP_PASSWORD = "wnut jysi afxm eeee"


@app.route("/")
def home():
    return "ARCHIVO CORRECTO CON BACKUP"



@app.route("/backup")
def backup():
    try:
        # datos simples
        datos = {"mensaje": "backup funcionando"}

        # guardar archivo
        with open("backup.json", "w") as f:
            json.dump(datos, f)

        # email
        msg = EmailMessage()
        msg["Subject"] = "Backup Flask"
        msg["From"] = EMAIL
        msg["To"] = EMAIL

        with open("backup.json", "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="json",
                filename="backup.json"
            )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL, APP_PASSWORD)
            smtp.send_message(msg)

        return "BACKUP ENVIADO OK"

    except Exception as e:
        return "ERROR: " + str(e)
