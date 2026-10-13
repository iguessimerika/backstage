from database.user import dbdata_user, dbstruct_user
from flask import Flask, redirect, session, request, url_for
import utils

def init_user_db():
    dbdata_user.init_user_data()
    dbstruct_user.init_user_struct()

def register_user():
    username = request.form['reg-user']
    email = request.form['reg-email']

    password = request.form['reg-pass']
    password_hash = utils.hash_password(password)

    user_id = dbdata_user.create_user(username, email, password_hash)
    set_session_userid(user_id)

def login_user():
    username_or_email = request.form['login-user']
    password = request.form['login-pass']

    user_id = dbdata_user.get_userid(username_or_email)
    password_hash = dbdata_user.get_password_hash(user_id)

    if utils.check_password(password, password_hash):
        set_session_userid(user_id)
        return True
    else:
        return False

""" Retrieves the appropriate redirect URL based on the user's profile type. """
def get_login_redirect(userid):
    redirect = "profile_choice"
    profile_type = dbdata_user.get_profile_type(userid)

    if profile_type == "artist":
        redirect = "artist_dashboard"
    elif profile_type == "organizer":
        redirect = "organizer_dashboard"

    return redirect

""" Sets the session's user ID. """
def set_session_userid(userid):
    session.userid = userid