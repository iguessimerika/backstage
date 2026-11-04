import db


def create_link(data):
    connection = db.get_connection()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO LINKS (
                TYPE, VALUE, RELATION_TYPE, RELATION_ID
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                data["type"],
                data["value"],
                data["relation_type"],
                data["relation_id"],
            ),
        )

        connection.commit()
        return cursor.lastrowid

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()