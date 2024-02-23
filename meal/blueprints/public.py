from flask import Blueprint, render_template, jsonify, request, session

public = Blueprint("public")

@public.route("/")
def index(): 
    return render_template("index.html.j2")

