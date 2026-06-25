from flask import Flask, jsonify
import requests
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# 🔐 CONFIGURA ESTO
EMAIL = "chrislozada197@gmail.com"
APP_PASSWORD = "wnut jysi afxm eeee"   # ⚠️ App Password de Gmail

# ✅ URL CORRECTA DE TU APP EN RENDER
API_URL = "https://base-de-datos-lyfu.onrender.com"


# ✅ ENDPOINT PRINCIPAL
@app.route("/")
def home():
    return jsonify({
        "mensaje": "API funcionando correctamente"
    })


# ✅ ENDPOINT DE DATOS
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
        # 🔹 Obtener datos
        response = requests.get(API_URL + "/data")
        data = response.text

        # 🔹 Guardar archivo
        filename = "backup.json"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(data)

        # 🔹 Crear correo
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

        return "✅ Backup enviado correctamente"

    except Exception as e:
        return f"❌ Error en backup: {str(e)}"


# ✅ ENDPOINT DE BACKUP
@app.route("/backup")
def backup():
    return enviar_backup()


if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)

