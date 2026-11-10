import db


def create_links_table():
    connection = None
    cursor = None

    try:
        connection = db.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS LINKS (
                LINKID INT NOT NULL AUTO_INCREMENT,
                TYPE INT NOT NULL,
                VALUE VARCHAR(255) NOT NULL,
                RELATION_TYPE INT NOT NULL,
                RELATION_ID INT NOT NULL,
                PRIMARY KEY (LINKID)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        connection.commit()
        print("Tabelle LINKS ist vorhanden oder existiert bereits.")
        return True

    except Exception as error:
        print(f"Tabelle LINKS konnte nicht erstellt werden: {error}")
        return False

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    create_links_table()