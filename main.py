ffrom flask import Flask, jsonify
import smtplib
from email.message import EmailMessage
import json

app = Flask(__name__)

# ✅ CONFIGURA TU CORREO
EMAIL = "chrislozada197@gmail.com"
APP_PASSWORD = "wnut jysi afxm eeee"


# ✅ RUTA PRINCIPAL (NO CAMBIAR)
@app.route("/")
def home():
    return jsonify({"mensaje": "VERSION FUNCIONANDO"})


# ✅ RUTA BACKUP
@app.route("/backup")
def backup():
    try:
        # 🔹 datos de prueba (puedes cambiar luego por tu BD)
        datos = {
            "backup": "funcionando correctamente"
        }

        # 🔹 guardar archivo
        with open("backup.json", "w") as f:
            json.dump(datos, f)

        # 🔹 crear correo
        msg = EmailMessage()
        msg["Subject"] = "Backup Flask"
        msg["From"] = EMAIL
        msg["To"] = EMAIL

        # 🔹 adjuntar archivo
        with open("backup.json", "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="json",
                filename="backup.json"
            )

        # 🔹 enviar correo
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL, APP_PASSWORD)
            smtp.send_message(msg)

        return "BACKUP OK"

    except Exception as e:
        return "ERROR: " + str(e)
``
