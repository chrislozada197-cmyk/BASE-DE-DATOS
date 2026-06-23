from flask import Flask, request, render_template
import sqlite3, os, datetime

app = Flask(__name__)
UPLOAD_FOLDER = "archivos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def inicio():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    nombre = file.filename
    tipo = file.filename.split(".")[-1]
    ruta = os.path.join(UPLOAD_FOLDER, nombre)
    file.save(ruta)

    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("documentos.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Documentos (Nombre_Archivo, Tipo_Formato, Ruta_Archivo, Fecha_Subida, Palabras_Clave)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, tipo, ruta, fecha, ""))
    conn.commit()
    conn.close()

    return "Archivo cargado correctamente. <a href='/'>Volver</a>"

@app.route("/buscar", methods=["GET"])
def buscar():
    palabra = request.args.get("q")
    conn = sqlite3.connect("documentos.db")
    cur = conn.cursor()
    cur.execute("SELECT Nombre_Archivo, Ruta_Archivo FROM Documentos WHERE Nombre_Archivo LIKE ?", ('%' + palabra + '%',))
    resultados = cur.fetchall()
    conn.close()

    html = "<h1>Resultados</h1><ul>"
    for nombre, ruta in resultados:
        html += f"<li>{nombre} - <a href='{ruta}' download>Descargar</a></li>"
    html += "</ul><a href='/'>Volver</a>"
    return html

import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)



