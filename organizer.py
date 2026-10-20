from flask import Blueprint, request, render_template
import db

# Initialisierung des Blueprints für den Organizer-Bereich
# Der erste Parameter ist der Name des Blueprints, der zweite der Import-Name
organizer_bp = Blueprint('organizer', __name__)

# Rendert die HTML Seite
@organizer_bp.route('/', methods=['GET'])
def index():
    return render_template('create-organizer-profil.html')

#Nimmt den HTTP-Post-Request entgegen und speichert diesen in der DB
@organizer_bp.route('/submit_organizer', methods=['POST'])
def submit_organizer():
    company_name = request.form.get('companyName')
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    
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
            INSERT INTO ORGANIZER (USER_ID, NAME, FIRSTNAME, LASTNAME) 
            VALUES (%s, %s, %s, %s)
        """
        insert_tuple = (user_id, company_name, first_name, last_name)
        
        cursor.execute(sql_insert_query, insert_tuple)
        connection.commit() 
        
        return "Veranstalter Profil erfolgreich in der Datenbank angelegt!"
    
    except Exception as e:
        connection.rollback() 
        return f"Fehler bei der Datenbankoperation: {str(e)}", 500
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()