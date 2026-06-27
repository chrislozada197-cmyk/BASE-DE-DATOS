@app.route("/backup")
def backup():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM documentos")
        datos = cursor.fetchall()

        conn.close()

        return jsonify({
            "mensaje": "BACKUP FUNCIONA",
            "datos": datos
        })

    except Exception as e:
        return jsonify({"error": str(e)})
