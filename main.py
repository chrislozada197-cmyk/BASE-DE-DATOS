from flask import Flask, request, jsonify, send_file, render_template
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
# PAGINA WEB
# ==============================
@app.route("/")
def home():
    return render_template("index.html")


# ==============================
# SUBIR ARCHIVO
# ==============================
@app.route("/subir_archivo", methods=["POST"])
def subir_archivo():
    try:
        archivo = request.files["archivo"]

        nombre = archivo.filename
        contenido = archivo.read()

        contenido_base64 = base64.b64encode(contenido).decode("utf-8")

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO documentos (nombre, contenido) VALUES (?, ?)",
            (nombre, contenido_base64)
        )

        conn.commit()
        conn.close()

        return "✅ Archivo subido correctamente <br><a href='/'>Volver</a>"

    except Exception as e:
        return f"Error: {str(e)}"


# ==============================
# BUSCAR ARCHIVO
# ==============================
@app.route("/buscar")
def buscar():
    try:
        query = request.args.get("q")

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, nombre FROM documentos WHERE nombre LIKE ?",
            ('%' + query + '%',)
        )
        resultados = cursor.fetchall()

        conn.close()

        html = "<h2>Resultados:</h2>"

        for r in resultados:
            html += f"<p>{r[1]} - <a href='/descargar/{r[0]}'>Descargar</a></p>"

        html += "<br><a href='/'>Volver</a>"

        return html

    except Exception as e:
        return f"Error: {str(e)}"


# ==============================
# DESCARGAR ARCHIVO
# ==============================
@app.route("/descargar/<int:id>")
def descargar(id):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("SELECT nombre, contenido FROM documentos WHERE id=?", (id,))
        dato = cursor.fetchone()

        conn.close()

        if not dato:
            return "Archivo no encontrado"

        nombre = dato[0]
        contenido_base64 = dato[1]

        archivo_bytes = base64.b64decode(contenido_base64)

        return send_file(
            BytesIO(archivo_bytes),
            download_name=nombre,
            as_attachment=True
        )

    except Exception as e:
        return f"Error: {str(e)}"


# ==============================
# VER TODO (opcional API)
# ==============================
@app.route("/ver")
def ver():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM documentos")
    datos = cursor.fetchall()

    conn.close()

    return jsonify(datos)


# ==============================
# BACKUP (POWER AUTOMATE)
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
