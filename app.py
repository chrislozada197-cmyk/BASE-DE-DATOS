from flask import Flask, jsonify
import smtplib
from email.message import EmailMessage
import json
import os

app = Flask(__name__)

# 🔐 CONFIGURACIÓN
EMAIL = "chrislozada197@gmail.com"
APP_PASSWORD = "wnut jysi afxm eeee"


# ✅ ROOT (CAMBIO PARA VERIFICAR DEPLOY)
@app.route("/")
def home():
    return jsonify({
        "mensaje": "NUEVA VERSION FUNCIONANDO ✅"
    })


# ✅ ENDPOINT DE DATOS
@app.route("/data")
def data():
    return jsonify({
        "usuarios": [
            {"nombre": "Christian", "edad": 25},
            {"nombre": "Maria", "edad": 22}
        ]
    })


# ✅ ENDPOINT BACKUP (TODO AQUÍ)
@app.route("/backup")
def backup():
    try:
        # 🔹 Crear datos manualmente
        data = {
            "usuarios": [
                {"nombre": "Christian", "edad": 25},
                {"nombre": "Maria", "edad": 22}
            ]
        }

        filename = "backup.json"

        # 🔹 Guardar archivo
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f)

        # 🔹 Crear email
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

        # 🔹 Enviar correo
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL, APP_PASSWORD)
            smtp.send_message(msg)

        return "✅ BACKUP ENVIADO ✅"

    except Exception as e:
        return f"❌ ERROR: {str(e)}"


# ✅ IMPORTANTE PARA RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
``
