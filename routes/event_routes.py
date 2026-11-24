from flask import Blueprint, render_template


event_bp = Blueprint("event", __name__)

@event_bp.route("/create_event", methods=["GET", "POST"])
def create_event():
    return render_template("create_event.html")