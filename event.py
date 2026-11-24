from database.event_genre import dbdata_eventgenre, dbstruct_eventgenre

def init_event_dbs():
    dbstruct_eventgenre.create_eventgenre_table()