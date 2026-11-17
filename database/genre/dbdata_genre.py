import db

def insert_genres():
    genres = [
        "Rock", "Ambient", "Classical", "Country", "EDM",
        "Disco", "Dnb", "Folk", "Hiphop/Rap", "Indie",
        "Jazz/Blues", "Metal", "Pop", "Rnb/Soul", "Cover"
    ]

    connection = None
    cursor = None

    try:
        connection = db.get_connection()
        cursor = connection.cursor()

        cursor.executemany(
            "INSERT INTO GENRE (`VALUE`) VALUES (%s)",
            [(genre,) for genre in genres]
        )

        connection.commit()
        return True

    except Exception as error:
        if connection is not None:
            connection.rollback()

        print(f"Fehler beim Speichern der Genres: {error}")
        return False

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

def get_genres():
    connection = None
    cursor = None

    try:
        connection = db.get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT ID, `VALUE` FROM GENRE ORDER BY `VALUE`")
        return cursor.fetchall()

    except Exception as error:
        print(f"Fehler beim Laden der Genres: {error}")
        raise

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()