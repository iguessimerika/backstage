import os
from flask import Flask, render_template
from organizer import organizer_bp

app = Flask(__name__)

# Registrierung des Organizer-Moduls
app.register_blueprint(organizer_bp)

@app.route("/")
def index():
    return render_template("komponenten-test.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000"))
    )