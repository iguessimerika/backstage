import os

from flask import Flask, jsonify
from db import get_connection

app = Flask(__name__)


@app.get("/")
def index():
    return "Backstage läuft! Datenbank testen: /db-test"


@app.get("/db-test")
def db_test():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        return jsonify(db_connected=result[0] == 1)

    except Exception:
        app.logger.exception("Datenbankverbindung fehlgeschlagen")
        return jsonify(db_connected=False), 500

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000"))
    )