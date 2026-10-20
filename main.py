import artist, os
from flask import Flask, redirect, render_template, request, url_for, session
from database.artist.dbstruct_artist import create_artist_table

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("komponenten-test.html")


@app.route("/create_artist", methods=["GET", "POST"])
def create_artist():
    if request.method == "POST":
        artist.create_artist(request.form.to_dict(), 
                             request.files.get("artist-image"))
        return redirect(url_for("create_artist"))

    return render_template("create_artist.html")


@app.route("/artist/<int:artist_id>/picture")
def artist_picture(artist_id):
    return artist.artist_picture(artist_id)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000"))
    )