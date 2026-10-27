from database.user import dbdata_user, dbstruct_user
from flask import Flask, redirect, session, request, url_for
import utils

def init_user_db():
    dbdata_user.init_user_data()
    dbstruct_user.init_user_struct()

def register_user(username, email, password):
    password_hash = utils.hash_password(password)

    userid = dbdata_user.create_user(username, email, password_hash)
    set_session_user(userid)

def login_user(username_or_email, password):
    userid = dbdata_user.get_userid(username_or_email)
    
    if userid is None:
        return "no-user"
    
    password_hash = dbdata_user.get_password_hash(userid)

    if utils.check_password(password, password_hash):
        set_session_user(userid)
        return True
    else:
        return "wrong-password"

""" Retrieves the appropriate redirect URL based on the user's profile type. """
def get_login_redirect(userid):
    redirect = "profile_choice"
    profile_type = dbdata_user.get_profile_type(userid)

    if profile_type == "artist":
        redirect = "artist_dashboard"
    elif profile_type == "organizer":
        redirect = "organizer_dashboard"
    
    return url_for(redirect)

""" Sets the session's user ID. """
def set_session_user(userid):
    session["userid"] = userid
    username = dbdata_user.get_name_by_userid(userid)
    session["username"] = username