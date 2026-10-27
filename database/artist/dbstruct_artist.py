import db


def create_artist_table():
    connection = None
    cursor = None

    try:
        connection = db.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ARTIST (
                ARTISTID INT NOT NULL AUTO_INCREMENT,
                USER_ID INT NOT NULL,
                ARTISTNAME VARCHAR(50) NOT NULL,
                FIRSTNAME VARCHAR(50) NOT NULL,
                LASTNAME VARCHAR(50) NOT NULL,
                LOCATION VARCHAR(50),
                BIO VARCHAR(500),
                GENRE_ID INT,
                SUBGENRE_ID INT,
                PICTURE MEDIUMBLOB,

                PRIMARY KEY (ARTISTID)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        connection.commit()
        print("Tabelle ARTIST ist vorhanden.")
        return True

    except Exception as error:
        print(f"Tabelle ARTIST konnte nicht erstellt werden: {error}")
        return False

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    create_artist_table()