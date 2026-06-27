from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)

# ==============================
# CONFIG
# ==============================
DATABASE = "documentos.db"


# ==============================
# CREAR TABLA
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
# HOME
# ==============================
@app.route("/")
def home():
    return jsonify({"mensaje": "API funcionando correctamente"})


# ==============================
# INSERTAR
# ==============================
@app.route("/insertar", methods=["POST"])
def insertar():
    try:
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

    except Exception as e:
        return jsonify({"error": str(e)})


# ==============================
# VER DATOS
# ==============================
@app.route("/ver")
def ver():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM documentos")
        datos = cursor.fetchall()

        conn.close()

        return jsonify(datos)

    except Exception as e:
        return jsonify({"error": str(e)})


# ==============================
# BACKUP (ESTABLE)
# ==============================
@app.route("/backup")
def backup():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM documentos")
        datos = cursor.fetchall()

        conn.close()

        datos_json = []
        for fila in datos:
            datos_json.append({
                "id": fila[0],
                "nombre": fila[1],
                "contenido": fila[2]
            })

        return jsonify({
            "mensaje": "BACKUP OK",
            "data": datos_json
        })

    except Exception as e:
        return jsonify({"error": str(e)})
