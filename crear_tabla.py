import sqlite3

conn = sqlite3.connect("documentos.db")
cur = conn.cursor()

# Elimina la tabla vieja si existe
cur.execute("""
DROP TABLE IF EXISTS Documentos;
""")

# Crea la tabla con todas las columnas necesarias
cur.execute("""
CREATE TABLE Documentos (
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

print("Tabla Documentos creada/verificada correctamente.")
