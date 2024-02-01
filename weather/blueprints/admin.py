from flask import blueprints, render_template, request, jsonify, session, redirect

from ..database import Database
from ..utils import set_error

admin = blueprints.Blueprint("admin", __name__)

@admin.before_request
def check_auth():
    if not "user" in session:
        return redirect("/login")

    if not session["user"]['admin']:
        return redirect("/")

@admin.route('/')
def index():
    return redirect("/admin/dashboard")

@admin.route('/dashboard')
def dashboard():
    return render_template("admin/dashboard.html.j2", title="Dashboard", triggers=Database.get_triggers() or [], articles=Database.get_articles() or [])

@admin.route('/upload', methods=['POST'])
def upload_article():
    title = request.form['title']
    search_keys = request.form['tags']
    content = request.form['content']

    if not title or not search_keys or not content:
        set_error("Missing fields")
        return redirect("/admin")

    Database.create_article(title, search_keys, content)

    article = Database.get_article_by_title(title)

    return redirect(f"/article/{article.article_id}")

@admin.route('/add_trigger', methods=['POST'])
def add_trigger():
    lhs = request.form['lhs']
    rhs = request.form['rhs']
    logic = request.form['logic']
    article_id = request.form['article_id']

    if not lhs or not rhs or not logic or not article_id:
        return redirect("/admin")
    
    article = Database.get_article(article_id)

    if not article:
        set_error("Article not found")
        return redirect("/admin")

    Database.create_trigger(lhs, rhs, logic, article_id)

    return redirect("/admin/dashboard")

@admin.route('/delete_trigger', methods=['POST'])
def delete_trigger():
    trigger_id = request.form['trigger_id']

    if not trigger_id:
        return redirect("/admin")

    Database.delete_trigger(trigger_id)

    return redirect("/admin/dashboard")

@admin.route('/delete_article', methods=['POST'])
def delete_article():
    article_id = request.form['article_id']

    if not article_id:
        return redirect("/admin")

    Database.delete_article(article_id)

    return redirect("/admin/dashboard")