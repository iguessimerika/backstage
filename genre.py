from database.genre import dbstruct_genre, dbdata_genre

def init_genre_db():
    dbstruct_genre.create_genre_table();
    dbdata_genre.insert_genres();



