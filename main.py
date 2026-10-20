import os
from flask import Flask, render_template
from organizer import organizer_bp

# Wird zur Initalisierung der Datenbank gebraucht
#from database.organizer.dbstruct_organizer import init_organizer_struct

app = Flask(__name__)

# Registrierung des Organizer-Moduls
app.register_blueprint(organizer_bp)


if __name__ == "__main__":

    # Initalisierung der Datenbank
    #init_organizer_struct()

    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000"))
    )