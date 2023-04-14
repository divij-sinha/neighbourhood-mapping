from app import app
from app import db
from app.models import Neighborhood
from flask import render_template, redirect, url_for, session
from app.forms import SurveyStart, SurveyDraw, AgreeButton
from wtforms.validators import DataRequired
from utils import get_geojson, get_map_comps, get_neighborhood_list
import uuid
from datetime import datetime, timezone
from geoalchemy2.functions import ST_GeomFromGeoJSON
from geoalchemy2.shape import from_shape
from shapely.geometry import shape

neighborhood_list = get_neighborhood_list()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def start_page():
    agree = AgreeButton()
    if agree.validate_on_submit():
        session["uuid"] = str(uuid.uuid4())
        neighbor = Neighborhood(id_user = session["uuid"], first = "first")
        db.session.add(neighbor)
        db.session.commit()
        return redirect(url_for("survey_form"))
    return render_template("start_page.html", agree=agree)

@app.route("/survey_form", methods=['GET', 'POST'])
def survey_form():
    draw_options = {"polygon":False, "polyline": False, "rectangle": False, "circle": False, "marker": False, "circlemarker": {"radius": 20},}
    header, body_html, script = get_map_comps(loc = (41.8781, -87.6298), zoom = 12, draw_options=draw_options)
    form = SurveyStart()
    
    if form.validate_on_submit():
        parsed_geojson = get_geojson(form.mark_layer.data)
        neighbor = Neighborhood.query.filter_by(id_user = session["uuid"], first = "first").first()
        neighbor.location_geojson = from_shape(shape(parsed_geojson["features"][0]["geometry"]))
        neighbor.neighborhood_name = form.cur_neighborhood.data
        neighbor.rent_own = form.rent_own.data
        neighbor.years_lived = form.years_lived.data
        db.session.commit()
        session["coords"] = parsed_geojson["features"][0]["geometry"]["coordinates"]
        session["neighborhood"] = form.cur_neighborhood.data
        return redirect(url_for("survey_draw", first = "first"))

    return render_template("form_page_start.html",
        form=form,
        neighborhood_list = neighborhood_list,
        header=header,
        body_html=body_html,
        script=script
    )

@app.route("/survey_draw/<first>", methods=['GET', 'POST'])
def survey_draw(first):
    draw_options = {"polyline": False, "rectangle": False, "circle": False, "marker": False, "circlemarker": False}
    header, body_html, script = get_map_comps(loc = session["coords"][::-1], zoom = 13, draw_options=draw_options)
    form = SurveyDraw()
    now = datetime.now(timezone.utc)
    if (form.validate_on_submit() and first == 'first') or form.validate_on_submit(extra_validators={'cur_neighborhood':[DataRequired()]}):
        if form.submit.data:
            return redirect(url_for("thank_page"))
        elif form.draw_another.data:
            parsed_geojson = get_geojson(form.draw_layer.data)
            print(parsed_geojson)
            return redirect(url_for("survey_draw", first = "next"))
    if first == "first":
        form.cur_neighborhood.data = session["neighborhood"]
    else:
        form.cur_neighborhood.data = ""
    return render_template("form_page_draw.html",
        form=form,
        header=header,
        body_html=body_html,
        script=script,
        first=first,
        neighborhood_list = neighborhood_list
    )

@app.route("/thank_you", methods=['GET'])
def thank_page():
    return render_template("thank_page.html")
