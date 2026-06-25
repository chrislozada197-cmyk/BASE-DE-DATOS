import sqlite3

conn = sqlite3.connect("documentos.db")
cur = conn.cursor()

cur.execute("PRAGMA table_info(Documentos)")
columnas = cur.fetchall()

print("Columnas de la tabla Documentos:")
for col in columnas:
    print(col)

conn.close()
