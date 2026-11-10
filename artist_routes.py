from flask import Blueprint, redirect, render_template, request, session, url_for
import artist

artist_bp = Blueprint("artist", __name__)


@artist_bp.route("/create_artist", methods=["GET", "POST"])
def create_artist():
    if request.method == "POST":
        artist.create_artist(
            request.form.to_dict(),
            session.get("userid"),
            request.files.get("artist-image"),
        )
        # Nach dem Speichern des Künstlerprofils geht es direkt zum Dashboard
        return redirect(url_for("artist.artist_dashboard"))

    return render_template("create_artist.html")


@artist_bp.route("/artistpicture/<int:artist_id>")
def artist_picture(artist_id):
    return artist.get_artist_picture(artist_id)


@artist_bp.route("/show_artist/<int:artist_id>")
def show_artist(artist_id):
    artist_data = artist.get_artist_by_id(artist_id)

    if artist_data is None:
        return "Artist not found", 404

    return render_template("show_artist.html", artist=artist_data)


@artist_bp.route("/artist_dashboard")
def artist_dashboard():
    # Nur eingeloggte Nutzer
    userid = session.get("userid")
    if userid is None:
        return redirect(url_for("index"))

    # Nur Nutzer mit Künstlerprofil
    artist_data = artist.get_artist_by_userid(userid)
    if artist_data is None:
        return redirect(url_for("profile_choice"))

    completion, next_step = artist.get_profile_progress(artist_data)

    return render_template(
        "artist_dashboard.html",
        name=session.get("username"),
        first_name=artist_data.get("FIRSTNAME") or session.get("username"),
        artist_id=artist_data.get("ARTISTID"),
        completion=completion,
        next_step=next_step,
    )
