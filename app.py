from flask import Flask, jsonify
from flask import Flask, jsonify
import smtplib
from email.message import EmailMessage
import json

app = Flask(__name__)

# 🔐 CONFIGURACIÓN
EMAIL = "chrislozada197@gmail.com"
APP_PASSWORD = "wnut jysi afxm eeee"


# ✅ ROOT
@app.route("/")
def home():
    return jsonify({"mensaje": "NUEVA VERSION FUNCIONANDO ✅"})


# ✅ DATA
@app.route("/data")
def data():
    return jsonify({
        "usuarios": [
            {"nombre": "Christian", "edad": 25},
            {"nombre": "Maria", "edad": 22}
        ]
    })


# ✅ BACKUP
@app.route("/backup")
def backup():
    try:
        data = {
            "usuarios": [
                {"nombre": "Christian", "edad": 25},
                {"nombre": "Maria", "edad": 22}
            ]
        }

        # 🔹 guardar archivo
        with open("backup.json", "w") as f:
            json.dump(data, f)

        # 🔹 crear correo
        msg = EmailMessage()
        msg['Subject'] = 'Backup Flask'
        msg['From'] = EMAIL
        msg['To'] = EMAIL

        with open("backup.json", "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype='application',
                subtype='json',
                filename="backup.json"
            )

        # 🔹 enviar correo
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL, APP_PASSWORD)
            smtp.send_message(msg)

        return "✅ BACKUP ENVIADO ✅"

    except Exception as e:
        return f"❌ ERROR: {str(e)}"

``
