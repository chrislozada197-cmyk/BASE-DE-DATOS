from flask import Flask, request, jsonify
import sqlite3
import smtplib
from email.message import EmailMessage
import json

app = Flask(__name__)

# ==============================
# CONFIG
# ==============================
DATABASE = "documentos.db"

EMAIL = "chrislozada197@gmail.com"
APP_PASSWORD = "wnut jysi afxm eeee"


# ==============================
# CREAR TABLA SI NO EXISTE
# ==============================
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            contenido TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()


# ==============================
# RUTA PRINCIPAL
# ==============================
@app.route("/")
def home():
    return jsonify({"mensaje": "API funcionando correctamente"})


# ==============================
# INSERTAR DATOS
# ==============================
@app.route("/insertar", methods=["POST"])
def insertar():
    data = request.json

    nombre = data.get("nombre")
    contenido = data.get("contenido")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO documentos (nombre, contenido) VALUES (?, ?)",
        (nombre, contenido)
    )

    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Datos guardados"})


# ==============================
# VER DATOS
# ==============================
@app.route("/ver", methods=["GET"])
def ver():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM documentos")
    datos = cursor.fetchall()

    conn.close()

    return jsonify(datos)


# ==============================
# BACKUP (ENVÍA EMAIL)
# ==============================
@app.route("/backup")
def backup():
    try:
        # Obtener datos de la DB
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM documentos")
        datos = cursor.fetchall()

        conn.close()

        # Guardar backup JSON
        with open("backup.json", "w") as f:
            json.dump(datos, f)

        # Crear correo
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

        # Enviar correo
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL, APP_PASSWORD)
            smtp.send_message(msg)

        return jsonify({"mensaje": "BACKUP ENVIADO"})

    except Exception as e:
        return jsonify({"error": str(e)})
