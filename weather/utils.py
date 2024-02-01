from flask import session

def set_error(error: str):
    session["error"] = error