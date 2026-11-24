import db
from database.links import dbdata_links


# ==============================================================================
# 1. ORGANIZER ANLEGEN (CREATE)
#    Speichert Stammdaten, Profilbild und Links atomar in einer Transaktion
# ==============================================================================
def create_organizer(user_id, company_name, first_name, last_name, profile_picture_data, form_data):
    """Legt einen neuen Organizer inklusive Links in einer Transaktion an und gibt die neue ID zurück."""
    connection = db.get_connection()
    cursor = None
    try:
        cursor = connection.cursor()

        # Organizer-Datensatz einfügen
        sql_insert_query = """
            INSERT INTO ORGANIZER (USER_ID, NAME, FIRSTNAME, LASTNAME, PROFILPICTURE)
            VALUES (%s, %s, %s, %s, %s)
        """
        insert_tuple = (
            user_id,
            company_name,
            first_name,
            last_name,
            profile_picture_data,
        )
        cursor.execute(sql_insert_query, insert_tuple)
        organizer_id = cursor.lastrowid

        # Zugehörige Links innerhalb derselben Transaktion speichern
        dbdata_links.insert_links(cursor, form_data, organizer_id, 2)
        connection.commit()

        return organizer_id

    except Exception:
        # Bei Fehler alle Änderungen zurückrollen
        connection.rollback()
        raise  # Fehler an die Route weiterreichen
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ==============================================================================
# 2. ORGANIZER-PROFIL LADEN (READ)
#    Lädt Organizer-Stammdaten, zugehörige User-E-Mail und verknüpfte Links
# ==============================================================================
def get_organizer_profile_data(organizer_id):
    """Lädt Organizer-Daten, zugehörige User-E-Mail und Links. Gibt (None, None, None) zurück, falls nicht gefunden."""
    connection = db.get_connection()
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)

        # 1. Organizer-Daten holen
        cursor.execute("SELECT * FROM ORGANIZER WHERE ORGANIZERID = %s", (organizer_id,))
        organizer = cursor.fetchone()

        if not organizer:
            return None, None, None

        # 2. Zugehörige User-E-Mail holen
        cursor.execute("SELECT EMAIL FROM USERS WHERE USERID = %s", (organizer["USER_ID"],))
        user_db = cursor.fetchone()
        user_data = user_db if user_db else {}

        # 3. Verknüpfte Links holen (RELATION_TYPE 2 = Organizer)
        cursor.execute(
            "SELECT TYPE, VALUE FROM LINKS WHERE RELATION_ID = %s AND RELATION_TYPE = 2",
            (organizer_id,),
        )
        links_db = cursor.fetchall()

        return organizer, user_data, links_db

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ==============================================================================
# 3. PROFILBILD LADEN (READ - BLOB)
#    Liest die Binärdaten des gespeicherten Profilbilds aus der Datenbank
# ==============================================================================
def get_organizer_image(organizer_id):
    """Gibt die Binärdaten des Profilbilds zurück oder None, falls kein Bild existiert."""
    connection = db.get_connection()
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT PROFILPICTURE FROM ORGANIZER WHERE ORGANIZERID = %s", (organizer_id,))
        row = cursor.fetchone()

        return row[0] if (row and row[0]) else None

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()