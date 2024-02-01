from flask import blueprints, render_template, request, session, redirect

from markdown import markdown

from ..geo import Weather, GeoToolkit
from ..database import Database

public = blueprints.Blueprint("public", __name__)

@public.route('/')
@public.route('/index')
def index():
    lat, lon = request.args.get("lat"), request.args.get("lon")
    weather = None 
    recommended_articles = []

    if lat and lon:
        weather = Weather(float(lat), float(lon))

        # evaulate triggers
        triggers = Database.get_triggers()

        for trigger in triggers:
            lhs = trigger.lhs.replace("%temp%", str(weather.get_current_temp()))
            rhs = trigger.rhs.replace("%temp%", str(weather.get_current_temp()))

            if eval(lhs + trigger.logic + rhs):
                recommended_articles.append(Database.get_article(trigger.article_id))

    return render_template("index.html.j2", title="Landing", recent_articles=session.get("recent_articles", [])[:3], weather=weather, recommended_articles=recommended_articles)


@public.route('/get_weather', methods=['POST'])
def get_weather():
    geo_toolkit: GeoToolkit = GeoToolkit()
    lat, lon = geo_toolkit.fetch_lat_lon(request.form['location'])
    return redirect(f"/?lat={lat}&lon={lon}")

@public.route("/article/<id>")
def article(id: int):
    article = Database.get_article(id)

    if not article:
        return render_template("404.html.j2", title="404")
    
    if "recent_articles" not in session:
        session["recent_articles"] = [article]
    else:
        if article in session["recent_articles"]:
            session["recent_articles"].remove(article)
        session["recent_articles"].insert(0, article)

    return render_template("article.html.j2", title=article.title, content=markdown(article.content))

@public.route("/articles")
def articles():
    return render_template("articles.html.j2", title="Articles", articles=Database.get_articles() or [])