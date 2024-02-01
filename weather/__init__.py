import os
from weather import geo, net, database

from flask import Flask, render_template, session

app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="")

# This limits the worker pool size to 1, but this is stateless, therefore easier.
app.secret_key = os.urandom(32)

with app.app_context():
    from .blueprints import public
    app.register_blueprint(public.public)

    from .blueprints import admin
    app.register_blueprint(admin.admin, url_prefix="/admin")

    from .blueprints import auth
    app.register_blueprint(auth.auth)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html.j2", title="404"), 404

@app.context_processor
def handle_context():
    if "error" in session:
        error = session["error"]
        del session["error"]
        return dict(os=os, error=error)

    return dict(os=os)

def setup():
    # run pre run setup
    net.Net.verify_cache()
    database.Database.connect("localhost", 3306, "root", "", "jbradford")

setup()