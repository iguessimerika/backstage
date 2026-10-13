import os
import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        connection_timeout=10
    )


def test_connection():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()

        print(" Datenbank erfolgreich erreicht!")
        return True

    except (mysql.connector.Error, ValueError) as error:
        print(f" Datenbankverbindung fehlgeschlagen: {error}")
        return False

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    test_connection()