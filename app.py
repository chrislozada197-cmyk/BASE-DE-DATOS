from flask import Flask, request, render_template, send_from_directory
import sqlite3, os

app = Flask(__name__)

# Carpeta interna en Render (compatible con cualquier archivo)
UPLOAD_FOLDER = "archivos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # crea la carpeta si no existe
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Inicializar base de datos automáticamente al arrancar
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

# Ejecutar inicialización al inicio
init_db()

@app.route("/")
def inicio():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]

    # Mantener el nombre original del archivo (con espacios y caracteres especiales)
    filename = file.filename  

    # Ruta completa en carpeta interna
    ruta = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    try:
        file.save(ruta)
    except Exception as e:
        return f"Error al guardar el archivo: {str(e)}"

    # Guardar en la base de datos
    conn = sqlite3.connect("documentos.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Documentos (Nombre, Tipo, Ruta, PalabrasClave, Fecha_Subida)
        VALUES (?, ?, ?, ?, DATE('now'))
    """, (filename, filename.split(".")[-1], ruta, "",))
    conn.commit()
    conn.close()

    return f"Archivo '{filename}' cargado y registrado correctamente. <a href='/'>Volver</a>"

@app.route("/buscar", methods=["GET"])
def buscar():
    palabra = request.args.get("q")
    conn = sqlite3.connect("documentos.db")
    cur = conn.cursor()
    # Buscar tanto en PalabrasClave como en Nombre
    cur.execute("SELECT Nombre, Ruta FROM Documentos WHERE PalabrasClave LIKE ? OR Nombre LIKE ?", 
                ('%' + palabra + '%', '%' + palabra + '%'))
    resultados = cur.fetchall()
    conn.close()

    html = "<h1>Resultados de búsqueda</h1><ul>"
    for nombre, ruta in resultados:
        if os.path.exists(ruta):
            # Enlace de descarga válido
            html += f"<li>{nombre} - <a href='/download/{nombre}'>Descargar</a></li>"
        else:
            html += f"<li>{nombre} - (Archivo no encontrado)</li>"
    html += "</ul><a href='/'>Volver</a>"
    return html

# Nueva ruta para servir descargas (acepta nombres con espacios y caracteres)
@app.route("/download/<path:filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

