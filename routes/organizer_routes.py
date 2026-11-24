from flask import Blueprint, render_template, request, redirect, url_for, session, send_file
from database.links import dbdata_links
import db
import io

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

            return redirect(url_for('organizer.view_organizer', organizer_id=organizer_id))

        except Exception as e:  # noqa: BLE001
            connection.rollback()
            return f"Fehler bei der Datenbankoperation: {e!s}", 500

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

# --- NEUE ROUTEN FÜR DIE ANZEIGE DES PROFILS ---

@organizer_bp.route("/organizer/<int:organizer_id>")
def view_organizer(organizer_id):
    connection = db.get_connection()
    cursor = None
    try:
        # Dictionary-Cursor verwenden, um über Spaltennamen (Keys) auf Daten zuzugreifen
        cursor = connection.cursor(dictionary=True) 
        
        # 1. Organizer-Daten holen
        cursor.execute("SELECT * FROM ORGANIZER WHERE ORGANIZERID = %s", (organizer_id,))
        organizer = cursor.fetchone()
        
        if not organizer:
            return "Veranstalter nicht gefunden", 404
            
        # 2. User-Daten holen (z. B. für Kontakt-E-Mail)
        cursor.execute("SELECT EMAIL FROM USERS WHERE USERID = %s", (organizer['USER_ID'],))
        user_db = cursor.fetchone()
        user_data = user_db if user_db else {}
        
        # 3. Links holen (RELATION_TYPE 2)
        cursor.execute("SELECT TYPE, VALUE FROM LINKS WHERE RELATION_ID = %s AND RELATION_TYPE = 2", (organizer_id,))
        links_db = cursor.fetchall()
        
        # Links formatieren
        type_mapping = {1: "Website", 2: "Instagram", 3: "Weitere"}
        links = []
        for link in links_db:
            links.append({
                "type_name": type_mapping.get(link['TYPE'], "Link"),
                "value": link['VALUE']
            })

        # 4. Prüfen, ob ein Bild in der DB liegt und die URL generieren
        if organizer.get('PROFILPICTURE'):
            organizer['profile_picture'] = url_for('organizer.get_image', organizer_id=organizer_id)
        else:
            organizer['profile_picture'] = None

        # Hier wird die HTML-Datei aufgerufen, die wir am Anfang erstellt haben
        return render_template("show_organizer.html", organizer=organizer, user=user_data, links=links)

    except Exception as e:
        return f"Fehler beim Laden des Profils: {str(e)}", 500
    finally:
        if cursor: cursor.close()
        if connection: connection.close()


@organizer_bp.route("/organizer_image/<int:organizer_id>")
def get_image(organizer_id):
    connection = db.get_connection()
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT PROFILPICTURE FROM ORGANIZER WHERE ORGANIZERID = %s", (organizer_id,))
        row = cursor.fetchone()
        
        if row and row[0]:
            return send_file(io.BytesIO(row[0]), mimetype='image/jpeg') 
        
        return "Kein Bild gefunden", 404
    finally:
        if cursor: cursor.close()
        if connection: connection.close()
