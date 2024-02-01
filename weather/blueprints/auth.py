from flask import Blueprint, render_template, session, redirect, request

from hashlib import sha256

from ..database import Database
from ..utils import set_error

auth = Blueprint("auth", __name__)

@auth.route("/login")
def login():
    return render_template("auth/login.html.j2", title="Login")

@auth.route("/logout")
def logout():
    del session["user"]
    
    return redirect("/")

@auth.route("/api/login", methods=["POST"])
def api_login():
    username = request.form["username"]
    password = request.form["password"]

    user = Database.get_user(username)

    if not user:
        set_error("User not found")
        return redirect("/login")
    
    if user.password != sha256(password.encode('utf-8')).hexdigest():
        set_error("Incorrect password")
        return redirect("/login")
    
    session["user"] = user

    return redirect("/")

@auth.route("/api/register", methods=["POST"])
def api_register():
    username = request.form["username"]
    password = request.form["password"]

    if Database.get_user(username):
        set_error("User already exists")
        return redirect("/login")
    
    Database.create_user(username, sha256(password.encode('utf-8')).hexdigest())

    session["user"] = Database.get_user(username)

    return redirect("/")
    

