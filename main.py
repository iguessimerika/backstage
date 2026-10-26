import os, user
from flask import Flask, redirect, render_template, request, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # wichtig für Sessions

@app.route("/test")
def test():
    return render_template("komponenten-test.html")


@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=['POST'])
def login():
    pass_check = user.login_user()

    if pass_check:
        redirect = user.get_login_redirect(session.userid)
        return render_template(url_for(redirect))


    return render_template("login.html", error=pass_check)

@app.route("/register")
def add_user():
    return render_template("register.html")

@app.route("/register", methods=['POST'])
def register():
    user.register_user()

    return redirect(url_for("profile_choice"))

@app.route("/profile-choice")
def profile_choice():
    return render_template("profile-choice.html", name=session.username)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000"))
    )