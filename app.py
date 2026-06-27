from flask import Flask, jsonify
import smtplib
from email.message import EmailMessage
import json

app = Flask(__name__)

# CONFIGURACIÓN (usa tu Gmail y App Password)
EMAIL = "chrislozada197@gmail.com"
APP_PASSWORD = "wnut jysi afxm eeee"


# ✅ RUTA PRINCIPAL
@app.route("/")
def home():
    return jsonify({"mensaje": "VERSION FUNCIONANDO"})


# ✅ RUTA BACKUP
@app.route("/backup")
def backup():
    try:
        # Datos a respaldar
        datos = {
            "usuarios": [
                {"nombre": "Christian", "edad": 25},
                {"nombre": "Maria", "edad": 22}
            ]
        }

        # Crear archivo JSON
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

        return "BACKUP ENVIADO"

    except Exception as e:
        return f"ERROR: {str(e)}"
