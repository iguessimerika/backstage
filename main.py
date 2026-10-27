import os, user
from flask import Flask, redirect, render_template, request, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # wichtig für Sessions

@app.route("/test")
def test():
    return render_template("komponenten-test.html")


# -- LOGIN --
@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
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


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000"))
        # , debug=True
    )