from flask import Flask, jsonify
import smtplib
from email.message import EmailMessage
import json

app = Flask(__name__)

# CONFIGURACION
EMAIL = "chrislozada197@gmail.com"
APP_PASSWORD = "wnut jysi afxm eeee"


# ROOT
@app.route("/")
def home():
    return jsonify({"mensaje": "NUEVA VERSION FUNCIONANDO ✅"})


# DATA
@app.route("/data")
def data():
    return jsonify({
        "usuarios": [
            {"nombre": "Christian", "edad": 25},
            {"nombre": "Maria", "edad": 22}
        ]
    })


# BACKUP
@app.route("/backup")
def backup():
    try:
        datos = {
            "usuarios": [
                {"nombre": "Christian", "edad": 25},
                {"nombre": "Maria", "edad": 22}
            ]
        }

        # Guardar archivo
        with open("backup.json", "w") as archivo:
            json.dump(datos, archivo)

        # Crear correo
        mensaje = EmailMessage()
        mensaje["Subject"] = "Backup Flask"
        mensaje["From"] = EMAIL
        mensaje["To"] = EMAIL

        # Adjuntar archivo
        with open("backup.json", "rb") as archivo:
            mensaje.add_attachment(
                archivo.read(),
                maintype="application",
                subtype="json",
                filename="backup.json"
            )

        # Enviar correo
        servidor = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        servidor.login(EMAIL, APP_PASSWORD)
        servidor.send_message(mensaje)
        servidor.quit()

        return "✅ BACKUP ENVIADO ✅"

    except Exception as e:
        return f"❌ ERROR: {str(e)}"
``
