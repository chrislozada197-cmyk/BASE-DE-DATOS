import sqlite3

conn = sqlite3.connect("documentos.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS Documentos")

cur.execute("""
    CREATE TABLE Documentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre_Archivo TEXT,
        Tipo_Formato TEXT,
        Ruta_Archivo TEXT,
        Fecha_Subida TEXT,
        Palabras_Clave TEXT
    )
""")

conn.commit()
conn.close()

