from flask import Blueprint, render_template, request
from database.links import dbdata_links
import db

# Initialisierung des Blueprints für den Organizer-Bereich
# Der erste Parameter ist der Name des Blueprints, der zweite der Import-Name
organizer_bp = Blueprint("organizer", __name__)


# Rendert die HTML Seite
@organizer_bp.route("/create_organizer", methods=["GET"])
def index():
    return render_template("create-organizer-profil.html")


# Nimmt den HTTP-Post-Request entgegen und speichert diesen in der DB
@organizer_bp.route("/submit_organizer", methods=["POST","GET"])
def submit_organizer():
    if request.method == "POST":
        company_name = request.form.get("companyName")
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        data = request.form.to_dict()

        # Profilbild auslesen
        profile_picture_file = request.files.get("profilePicture")
        profile_picture_data = None
        if profile_picture_file and profile_picture_file.filename != "":
            profile_picture_data = profile_picture_file.read()  # Liest die Binärdaten

        # Serverseitige Validierung
        if not company_name or not first_name or not last_name:
            return "Fehler: Bitte alle Pflichtfelder ausfüllen.", 400

        # Festlegen der USER_ID (Aktuell als statischer Dummy, da in DB NOT NULL)
        user_id = 1

        connection = db.get_connection()
        cursor = None
        try:
            cursor = connection.cursor()

            # Schutz gegen SQL Angriffe
            sql_insert_query = """
                INSERT INTO ORGANIZER (USER_ID, NAME, FIRSTNAME, LASTNAME, PROFILPICTURE) 
                VALUES (%s, %s, %s, %s,%s)
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
            dbdata_links.insert_links(cursor, data, organizer_id, 2)
            connection.commit()

            return "Veranstalter Profil erfolgreich in der Datenbank angelegt!"

        except Exception as e:  # noqa: BLE001
            connection.rollback()
            return f"Fehler bei der Datenbankoperation: {e!s}", 500

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
