import os, user, db, artist
from flask import Flask, redirect, render_template, request, url_for, session
from routes.artist_routes import artist_bp
from routes.organizer_routes import organizer_bp
from routes.explore_routes import explore_bp
from routes.event_routes import event_bp

app = Flask(__name__)
app.secret_key = "supersecretkey"  # wichtig für Sessions
 
@app.route("/test")
def test():
    return render_template("komponenten-test.html")

# -- HEADER --
# Provides each template with the links for dashboard and profile, depending on the profile type of the logged-in user
@app.context_processor
def inject_nav():
    userid = session.get("userid")
    if userid is None:
        return {}

    profile_type = user.dbdata_user.get_profile_type(userid)

    if profile_type == "artist":
        artist_data = artist.get_artist_by_userid(userid)
        return {
            "nav_dashboard_url": url_for("artist.artist_dashboard"),
            "nav_profile_url": url_for("artist.show_artist", artist_id=artist_data.get("ARTISTID"))
        }

    if profile_type == "organizer":
        return {
            "nav_dashboard_url": "#",  # @WIP: organizer dashboard route
            "nav_profile_url": url_for("organizer.view_organizer", organizer_id=artist_data.get("ARTISTID"))
        }

    # No profile created yet
    return {}
 
# -- LOGIN --
@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        db.init_database()
        return render_template("login.html")
    l_user = request.form['login-user']
    l_pass = request.form['login-pass']
    login_check = user.login_user(l_user, l_pass)
    if login_check is True:
        redirect_url = user.get_login_redirect(session.get("userid"))
        return redirect(redirect_url)
 
    return render_template("login.html", error=login_check)
 
# -- REGISTER --
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    l_user = request.form['reg-user'].strip()
    l_email = request.form['reg-email'].strip()
    l_pass = request.form['reg-pass']
    l_confirm = request.form['reg-confirm']
    # Errorhandling from user input
    errors = {}
    if len(l_pass) < 8:
        errors["pass"] = "Das Passwort muss mindestens 8 Zeichen lang sein."
    if l_pass != l_confirm:
        errors["confirm"] = "Die Passwörter stimmen nicht überein."
 
    if errors:
        return render_template("register.html", errors=errors)
    # Create user in database
    user.register_user(l_user, l_email, l_pass)
    return redirect(url_for("profile_choice"))
 
# -- PROFILE CHOICE --
@app.route("/profile-choice")
def profile_choice():
    return render_template("profile-choice.html", name=session.get("username"))
 
 
# -- ARTIST -- 
app.register_blueprint(artist_bp)

# -- ORGANIZER --
# Registrierung des Organizer-Moduls
app.register_blueprint(organizer_bp)

# -- EXPLORE -- 
app.register_blueprint(explore_bp)

# -- EVENT -- 
app.register_blueprint(event_bp)
 
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000"))
        # , debug=True
    )
