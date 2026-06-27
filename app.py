from flask import Flask, jsonify
import smtplib
from email.message import EmailMessage
import json

app = Flask(__name__)

EMAIL = "chrislozada197@gmail.com"
APP_PASSWORD = "wnut jysi afxm eeee"


@app.route("/")
def home():
    return jsonify({"mensaje": "VERSION FUNCIONANDO"})


@app.route("/backup")
def backup():
    try:
        datos = {
            "usuarios": [
                {"nombre": "Christian", "edad": 25},
                {"nombre": "Maria", "edad": 22}
            ]
        }

        with open("backup.json", "w") as archivo:
            json.dump(datos, archivo)

        mensaje = EmailMessage()
        mensaje["Subject"] = "Backup Flask"
        mensaje["From"] = EMAIL
        mensaje["To"] = EMAIL

        with open("backup.json", "rb") as archivo:
            mensaje.add_attachment(
                archivo.read(),
                maintype="application",
                subtype="json",
                filename="backup.json"
            )

        servidor = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        servidor.login(EMAIL, APP_PASSWORD)
        servidor.send_message(mensaje)
        servidor.quit()

        return "BACKUP ENVIADO"

    except Exception as e:
        return str(e)
