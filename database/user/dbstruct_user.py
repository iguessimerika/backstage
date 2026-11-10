import db

def create_users_table():
    connection = db.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS USERS (
                USERID INT NOT NULL AUTO_INCREMENT,
                USERNAME VARCHAR(50) NOT NULL,
                PASSWORD_HASH VARCHAR(255) NOT NULL,
                EMAIL VARCHAR(50) NOT NULL,
                PRIMARY KEY (USERID)
            )
        """)
        connection.commit()
        cursor.close()
        print("Tabelle 'USERS' erfolgreich erstellt oder existiert bereits.")
    finally:
        connection.close()

""" Initializes the user database structure. """
def init_user_struct():
    create_users_table()

if __name__ == "__main__":
    init_user_struct()