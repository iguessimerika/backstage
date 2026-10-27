import os, user
from database.artist import dbdata_artist, dbstruct_artist

def create_artist(data, user_id, picture=None):
    # Call the function from dbdata_artist to create the artist in the database
    artist_id = dbdata_artist.create_artist(data, user_id, picture)
    return artist_id

def get_artist_picture(artist_id):
    # Call the function from dbdata_artist to retrieve the artist's picture
    picture_data = dbdata_artist.get_picture(artist_id)
    return picture_data

def init_artist_db():
    dbstruct_artist.create_artist_table()

