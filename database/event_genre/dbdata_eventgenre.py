import db
            
""" Inserts a new event-genre relationship into the database. """
def insert_eventgenre(event_id, genre_id):
    connection = db.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO EVENT_GENRE (EVENT_ID, GENRE_ID) VALUES (%s, %s)",
            (event_id, genre_id),
        )
        connection.commit()
        eventgenre_id = cursor.lastrowid
        cursor.close()
        return eventgenre_id
    finally:
        connection.close()
        

def insert_multiple_eventgenres(event_id, genre_ids):
    connection = db.get_connection()
    try:
        cursor = connection.cursor()
        for genre_id in genre_ids:
            cursor.execute(
                "INSERT INTO EVENT_GENRE (EVENT_ID, GENRE_ID) VALUES (%s, %s)",
                (event_id, genre_id),
            )
        connection.commit()
        cursor.close()
    finally:
        connection.close()