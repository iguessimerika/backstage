from io import BytesIO
from flask import abort, send_file
from database.links import dbdata_links
import db



def create_artist(data, user_id, picture=None,):
    connection = db.get_connection()
    cursor = None

    try:

        picture_data = picture.read() or None            
        cursor = connection.cursor()
        cursor.execute(
                    """
                    INSERT INTO ARTIST (
                        ARTISTNAME, FIRSTNAME, LASTNAME,
                        LOCATION, BIO, USER_ID, PICTURE
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        data["artistname"],
                        data["firstname"],
                        data["lastname"],
                        data["location"],
                        data.get("bio", ""),
                        user_id,
                        picture_data,
                    ),
                )
        artist_id = cursor.lastrowid
        dbdata_links.insert_artist_links(cursor, data, artist_id, 1) # relation_type 1 for artist
        connection.commit()
        return artist_id;

    

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

def get_picture(artist_id):
    connection = db.get_connection()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT PICTURE FROM ARTIST WHERE ARTISTID = %s",
            (artist_id,),
        )
        row = cursor.fetchone()
        return row[0] if row else None

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def get_artist_by_id(artist_id):
    connection = db.get_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                ARTISTID,
                USER_ID,
                ARTISTNAME,
                FIRSTNAME,
                LASTNAME,
                LOCATION,
                BIO,
                GENRE_ID,
                SUBGENRE_ID,
                PICTURE
            FROM ARTIST
            WHERE ARTISTID = %s
            """,
            (artist_id,),
        )
        artist_data = cursor.fetchone()
        if artist_data is None:
            return None;
        artist_data["links"] = dbdata_links.get_links_byRelationType(artist_id, cursor, dbdata_links.ARTIST_RELATION_TYPE)
        return artist_data

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def get_artist_by_userid(user_id):
    connection = db.get_connection()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT ARTISTID FROM ARTIST WHERE USER_ID = %s",
            (user_id,),
        )
        row = cursor.fetchone()

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

    if row is None:
        return None

    # Vorhandene Funktion wiederverwenden, damit auch die Links mitkommen
    return get_artist_by_id(row[0])


def artist_picture(artist_id):
    picture = get_picture(artist_id)

    if not picture:
        abort(404)

    mimetype = (
        "image/png"
        if picture.startswith(b"\x89PNG\r\n\x1a\n")
        else "image/jpeg"
    )

    return send_file(
        BytesIO(picture),
        mimetype=mimetype,
    )