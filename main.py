from flask import Flask, request, jsonify, send_file
import sqlite3
import json
import base64
from io import BytesIO

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
# INSERTAR TEXTO
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
# SUBIR ARCHIVO REAL
# ==============================
@app.route("/subir_archivo", methods=["POST"])
def subir_archivo():
    try:
        archivo = request.files["archivo"]

        nombre = archivo.filename
        contenido = archivo.read()

        # Convertir archivo a base64
        contenido_base64 = base64.b64encode(contenido).decode("utf-8")

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO documentos (nombre, contenido) VALUES (?, ?)",
            (nombre, contenido_base64)
        )

        conn.commit()
        conn.close()

        return jsonify({"mensaje": "Archivo guardado correctamente"})

    except Exception as e:
        return jsonify({"error": str(e)})


# ==============================
# DESCARGAR ARCHIVO REAL
# ==============================
@app.route("/descargar/<int:id>")
def descargar(id):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("SELECT nombre, contenido FROM documentos WHERE id=?", (id,))
        dato = cursor.fetchone()

        conn.close()

        if dato is None:
            return jsonify({"error": "Archivo no encontrado"})

        nombre = dato[0]
        contenido_base64 = dato[1]

        # Decodificar archivo
        archivo_bytes = base64.b64decode(contenido_base64)

        return send_file(
            BytesIO(archivo_bytes),
            download_name=nombre,
            as_attachment=True
        )

    except Exception as e:
        return jsonify({"error": str(e)})


# ==============================
# BACKUP (PARA POWER AUTOMATE)
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
