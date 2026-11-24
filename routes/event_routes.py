from flask import Blueprint, redirect, url_for


event_bp = Blueprint("event", __name__)

@event_bp.route("/create_event", methods=["GET", "POST"])
def create_event():
    return redirect(url_for("create_event"))