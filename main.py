import artist, os
from flask import Flask, redirect, render_template, request, url_for, session
from database.artist.dbstruct_artist import create_artist_table

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("komponenten-test.html")



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000"))
    )