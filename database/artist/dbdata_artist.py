from os import abort
from io import BytesIO
from flask import abort, send_file
from flask import send_file

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

        connection.commit()
        return cursor.lastrowid

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