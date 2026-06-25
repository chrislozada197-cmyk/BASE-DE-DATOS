from flask import Flask, jsonify
import requests
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)

# 🔐 CONFIGURA ESTO
EMAIL = "tuemail@gmail.com"
APP_PASSWORD = "tu_app_password"   # ⚠️ NO tu contraseña normal

# 🔹 URL de tu propia API (ajústala si es necesario)
API_URL = "https://base-de-datos.onrender.com"  


# ✅ ENDPOINT PRINCIPAL (el que ya tienes)
@app.route("/")
def home():
    return jsonify({
        "mensaje": "API funcionando correctamente"
    })


# ✅ EJEMPLO DE DATOS (ajústalo a tu endpoint real)
@app.route("/data")
def get_data():
    data = {
        "usuarios": [
            {"nombre": "Christian", "edad": 25},
            {"nombre": "Maria", "edad": 22}
        ]
    }
    return jsonify(data)


# ✅ FUNCIÓN PARA ENVIAR BACKUP
def enviar_backup():
    try:
        # 🔹 1. Obtener datos de tu API
        response = requests.get(API_URL + "/data")
        data = response.text

        # 🔹 2. Guardar archivo temporal
        filename = "backup.json"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(data)

        # 🔹 3. Crear correo
        msg = EmailMessage()
        msg['Subject'] = 'Backup Flask'
        msg['From'] = EMAIL
        msg['To'] = EMAIL

        with open(filename, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype='application',
                subtype='json',
                filename=filename
            )

        # 🔹 4. Enviar correo
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL, APP_PASSWORD)
            smtp.send_message(msg)

        return "✅ Backup enviado correctamente"

    except Exception as e:
        return f"❌ Error en backup: {str(e)}"


# ✅ ENDPOINT PARA ACTIVAR BACKUP
@app.route("/backup")
def backup():
    return enviar_backup()


if __name__ == "__main__":
    app.run(debug=True)

