import os, user
from database.links import dbdata_links, dbstruct_links

def init_links_db():
    dbstruct_links.create_links_table()
