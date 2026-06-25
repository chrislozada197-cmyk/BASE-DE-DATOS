from flask import Flask, request, render_template, redirect
import sqlite3, os

app = Flask(__name__)

# Carpeta interna en Render
UPLOAD_FOLDER = "archivos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Inicializar base de datos
def init_db():
    conn = sqlite3.connect("documentos.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Documentos (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT NOT NULL,
        Tipo TEXT NOT NULL,
        Ruta TEXT NOT NULL,
        PalabrasClave TEXT,
        Fecha_Subida TEXT DEFAULT (DATE('now'))
    )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def inicio():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    filename = file.filename
    ruta_local = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    # Palabras clave opcionales desde el formulario
    keywords = request.form.get("keywords", "")

    try:
        file.save(ruta_local)
    except Exception as e:
        return f"Error al guardar el archivo: {str(e)}"

    # Guardar registro en BD con ruta pendiente (OneDrive lo actualizará)
    conn = sqlite3.connect("documentos.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Documentos (Nombre, Tipo, Ruta, PalabrasClave, Fecha_Subida)
        VALUES (?, ?, ?, ?, DATE('now'))
    """, (filename, filename.split(".")[-1], "PENDIENTE", keywords,))
    conn.commit()
    conn.close()

    return f"Archivo '{filename}' cargado correctamente. <a href='/'>Volver</a>"

@app.route("/buscar", methods=["GET"])
def buscar():
    palabra = request.args.get("q")
    conn = sqlite3.connect("documentos.db")
    cur = conn.cursor()
    cur.execute("SELECT ID, Nombre, Ruta FROM Documentos WHERE PalabrasClave LIKE ? OR Nombre LIKE ?", 
                ('%' + palabra + '%', '%' + palabra + '%'))
    resultados = cur.fetchall()
    conn.close()

    html = "<h1>Resultados de búsqueda</h1><ul>"
    for id, nombre, ruta in resultados:
        if ruta != "PENDIENTE":
            html += f"<li>{nombre} - <a href='/download/{id}'>Descargar</a></li>"
        else:
            html += f"<li>{nombre} - (Enlace aún no disponible)</li>"
    html += "</ul><a href='/'>Volver</a>"
    return html

@app.route("/download/<int:id>")
def download_file(id):
    conn = sqlite3.connect("documentos.db")
    cur = conn.cursor()
    cur.execute("SELECT Ruta FROM Documentos WHERE ID=?", (id,))
    resultado = cur.fetchone()
    conn.close()

    if resultado and resultado[0] != "PENDIENTE":
        return redirect(resultado[0])  # redirige al enlace público OneDrive
    else:
        return "El archivo aún no tiene enlace público disponible."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

