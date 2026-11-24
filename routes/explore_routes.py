from flask import Blueprint, redirect, render_template, url_for


explore_bp = Blueprint("explore", __name__)

@explore_bp.route("/explore", methods=["GET"])
def explore():
    return render_template("explore.html")