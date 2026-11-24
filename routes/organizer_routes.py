import io
from flask import Blueprint, render_template, request, redirect, url_for, send_file
from database.organizer import dbdata_organizer

# Blueprint-Initialisierung für alle Organizer-Routen
organizer_bp = Blueprint("organizer", __name__)


# ==============================================================================
# 1. FORMULAR ANZEIGEN (GET /create_organizer)
#    Rendert die HTML-Seite zum Erstellen eines neuen Organizer-Profils
# ==============================================================================
@organizer_bp.route("/create_organizer", methods=["GET"])
def index():
    return render_template("create-organizer-profil.html")


# ==============================================================================
# 2. FORMULAR VERARBEITEN & SPEICHERN (POST /submit_organizer)
#    Liest Formulardaten und Profilbild aus, validiert Pflichtfelder,
#    speichert den Organizer in der DB und leitet auf das Profil weiter
# ==============================================================================
@organizer_bp.route("/submit_organizer", methods=["POST"])
def submit_organizer():
    # Formulardaten auslesen
    company_name = request.form.get("companyName")
    first_name = request.form.get("firstName")
    last_name = request.form.get("lastName")
    data = request.form.to_dict()

    # Profilbild als Binärdaten auslesen (falls hochgeladen)
    profile_picture_file = request.files.get("profilePicture")
    profile_picture_data = None
    if profile_picture_file and profile_picture_file.filename != "":
        profile_picture_data = profile_picture_file.read()

    # Serverseitige Validierung
    if not company_name or not first_name or not last_name:
        return "Fehler: Bitte alle Pflichtfelder ausfüllen.", 400

    # Aktuell als statischer Dummy (später z. B. aus session)
    user_id = 1

    # In Datenbank speichern und auf die Profilansicht weiterleiten
    try:
        organizer_id = dbdata_organizer.create_organizer(
            user_id=user_id,
            company_name=company_name,
            first_name=first_name,
            last_name=last_name,
            profile_picture_data=profile_picture_data,
            form_data=data,
        )
        return redirect(url_for("organizer.view_organizer", organizer_id=organizer_id))

    except Exception as e:
        return f"Fehler bei der Datenbankoperation: {e!s}", 500


# ==============================================================================
# 3. ORGANIZER-PROFIL ANZEIGEN (GET /organizer/<organizer_id>)
#    Lädt Stammdaten, User-E-Mail und Links aus der DB, bereitet sie für
#    das Template auf und rendert die Profilseite
# ==============================================================================
@organizer_bp.route("/organizer/<int:organizer_id>")
def view_organizer(organizer_id):
    try:
        organizer, user_data, links_db = dbdata_organizer.get_organizer_profile_data(organizer_id)

        if not organizer:
            return "Veranstalter nicht gefunden", 404

        # Link-Typen für die Anzeige im Frontend mappen
        type_mapping = {1: "Website", 2: "Instagram", 3: "Weitere"}
        links = [
            {
                "type_name": type_mapping.get(link["TYPE"], "Link"),
                "value": link["VALUE"],
            }
            for link in links_db
        ]

        # Bild-URL für das <img>-Tag generieren, falls ein Bild in der DB liegt
        if organizer.get("PROFILPICTURE"):
            organizer["profile_picture"] = url_for("organizer.get_image", organizer_id=organizer_id)
        else:
            organizer["profile_picture"] = None

        return render_template("show_organizer.html", organizer=organizer, user=user_data, links=links)

    except Exception as e:
        return f"Fehler beim Laden des Profils: {e!s}", 500


# ==============================================================================
# 4. PROFILBILD AUSLIEFERN (GET /organizer_image/<organizer_id>)
#    Lädt die gespeicherten Bild-Binärdaten aus der DB und sendet sie
#    als HTTP-Bildantwort (JPEG) an den Browser
# ==============================================================================
@organizer_bp.route("/organizer_image/<int:organizer_id>")
def get_image(organizer_id):
    try:
        image_data = dbdata_organizer.get_organizer_image(organizer_id)

        if image_data:
            return send_file(io.BytesIO(image_data), mimetype="image/jpeg")

        return "Kein Bild gefunden", 404
    except Exception as e:
        return f"Fehler beim Laden des Bildes: {e!s}", 500