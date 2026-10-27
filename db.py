import os, user, artist
import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host=os.environ["MYSQLHOST"],
        port=int(os.environ["MYSQLPORT"]),
        user=os.environ["MYSQLUSER"],
        password=os.environ["MYSQLPASSWORD"],
        database=os.environ["MYSQLDATABASE"],
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

        print("Datenbank erfolgreich erreicht!")
        return True

    except KeyError as error:
        print(f"Umgebungsvariable fehlt: {error.args[0]}")
        return False

    except (mysql.connector.Error, ValueError) as error:
        print(f"Datenbankverbindung fehlgeschlagen: {error}")
        return False

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

def init_database():
    user.init_user_db()
    artist.init_artist_db()
    
if __name__ == "__main__":
    test_connection()