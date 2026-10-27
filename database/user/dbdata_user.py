import db

""" Initializes the user database data. """
def init_user_data():
    pass

""" Creates a new user in the database. """
def create_user(username, email, password_hash):
    connection = db.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO USERS (USERNAME, PASSWORD_HASH, EMAIL) VALUES (%s, %s, %s)",
            (username, password_hash, email),
        )
        connection.commit()
        user_id = cursor.lastrowid
        cursor.close()
        return user_id
    finally:
        connection.close()

""" Retrieves the user ID based on the provided username or email. """
def get_userid(username_or_email):
    connection = db.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT USERID
            FROM USERS
            WHERE USERS.USERNAME = %s OR USERS.EMAIL = %s
            """,
            (username_or_email, username_or_email),
        )
        row = cursor.fetchone()
        cursor.close()
        return row[0] if row else None
    finally:
        connection.close()

""" Retrieves the user ID based on the provided username. """
def get_user_by_id(userid):
    connection = db.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT *
            FROM USERS
            WHERE USERS.USERID = %s
            """,
            (userid,),
        )
        row = cursor.fetchone()
        cursor.close()
        return row[0] if row else None
    finally:
        connection.close()

""" Retrieves the profile type of a user based on their user ID. """
def get_profile_type(userid):
    connection = db.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT
                CASE
                    WHEN ARTIST.USER_ID IS NOT NULL THEN 'artist'
                    WHEN ORGANIZER.USER_ID IS NOT NULL THEN 'organizer'
                    ELSE 'none'
                END
            FROM USERS
            LEFT JOIN ARTIST ON ARTIST.USER_ID = USERS.USERID
            LEFT JOIN ORGANIZER ON ORGANIZER.USER_ID = USERS.USERID
            WHERE USERS.USERID = %s
            """,
            (userid,),
        )
        row = cursor.fetchone()
        cursor.close()
        return row[0] if row else None
    finally:
        connection.close()

""" Retrieves the password hash for a user based on their user ID. """
def get_password_hash(userid):
    connection = db.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT
                USERS.PASSWORD_HASH
            FROM USERS
            WHERE USERS.USERID = %s
            """,
            (userid,),
        )
        row = cursor.fetchone()
        cursor.close()
        return row[0] if row else None
    finally:
        connection.close()

""" Retrieves the username for a user based on their user ID. """
def get_name_by_userid(userid):
    connection = db.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT
                USERS.USERNAME
            FROM USERS
            WHERE USERS.USERID = %s
            """,
            (userid,),
        )
        row = cursor.fetchone()
        cursor.close()
        return row[0] if row else None
    finally:
        connection.close()

if __name__ == "__main__":
    init_user_data()