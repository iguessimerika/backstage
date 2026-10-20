import db
 
def create_organizers_table():
    connection = db.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ORGANIZER (
                ORGANIZERID INT NOT NULL AUTO_INCREMENT,
                USER_ID INT NOT NULL,
                NAME VARCHAR(50) NOT NULL,
                FIRSTNAME VARCHAR(50) NOT NULL,
                LASTNAME VARCHAR(50) NOT NULL,
                PROFILPICTURE MEDIUMBLOB,
                PRIMARY KEY (ORGANIZERID)
            )
        """)
        connection.commit()
        cursor.close()
        print("Tabelle 'ORGANIZER' erfolgreich erstellt oder existiert bereits.")
    finally:
        connection.close()
 
""" Initializes the organizer database structure. """
def init_organizer_struct():
    create_organizers_table()
 
if __name__ == "__main__":
    init_organizer_struct()