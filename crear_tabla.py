import sqlite3

conn = sqlite3.connect("documentos.db")
cur = conn.cursor()

cur.execute("""
DROP TABLE IF EXISTS Documentos;
""")

cur.execute("""
CREATE TABLE Documentos (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    Tipo TEXT NOT NULL,
    Ruta TEXT NOT NULL,
    PalabrasClave TEXT
)
""")

conn.commit()
conn.close()

print("Tabla Documentos creada/verificada correctamente.")
