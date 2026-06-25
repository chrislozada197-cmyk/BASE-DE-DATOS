from flask import Flask, jsonify
import requests
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)

# 🔐 CONFIGURACIÓN
EMAIL = "chrislozada197@gmail.com"
APP_PASSWORD = "wnut jysi afxm eeee"

# IMPORTANTE: usar la misma URL de Render
API_URL = "https://base-de-datos-lyfu.onrender.com"


# ✅ ROOT
@app.route("/")
def home():
    return jsonify({"mensaje": "API funcionando correctamente"})


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
        # 🔹 obtener datos directamente (sin depender de API_URL)
        data = {
            "usuarios": [
                {"nombre": "Christian", "edad": 25},
                {"nombre": "Maria", "edad": 22}
            ]
        }

        filename = "backup.json"
        with open(filename, "w", encoding="utf-8") as f:
            import json
            json.dump(data, f)

        # 🔹 crear correo
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

        # 🔹 enviar correo
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL, APP_PASSWORD)
            smtp.send_message(msg)

        return "✅ Backup enviado correctamente"

    except Exception as e:
        return f"❌ Error: {str(e)}"


# ✅ IMPORTANTE PARA RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
