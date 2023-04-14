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
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import shape
from datetime import datetime, timezone 

neighborhood_list = get_neighborhood_list()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def start_page():
    agree = AgreeButton()
    if agree.validate_on_submit():
        session["uuid"] = str(uuid.uuid4())
        dt = datetime.now(timezone.utc)
        neighbor = Neighborhood(id_user = session["uuid"], first = "first", neighborhood_time_stamp = dt)
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
        neighbor.neighborhood_time_stamp = datetime.now(timezone.utc)
        db.session.commit()
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
    if first == 'first':
        cur_neighbor = Neighborhood.query.filter_by(id_user = session["uuid"], first = "first").first()
        pt = to_shape(cur_neighbor.location_geojson)
        loc = pt.y, pt.x
    else:
        loc = (41.8781, -87.6298)
    header, body_html, script = get_map_comps(loc = loc, zoom = 13, draw_options=draw_options)
    form = SurveyDraw()
    if (form.validate_on_submit() and first == 'first') or form.validate_on_submit(extra_validators={'cur_neighborhood':[DataRequired()]}):
        parsed_geojson = get_geojson(form.draw_layer.data)
        if first == 'first':
            neighbor = cur_neighbor
            neighbor.neighborhood_geojson = from_shape(shape(parsed_geojson["features"][0]["geometry"]))
            neighbor.neighborhood_time_stamp = datetime.now(timezone.utc)
            db.session.commit()
        else:
            neighbor = Neighborhood(id_user = session["uuid"], first = "next")
            neighbor.neighborhood_name = form.cur_neighborhood.data
            neighbor.neighborhood_geojson = from_shape(shape(parsed_geojson["features"][0]["geometry"]))
            neighbor.neighborhood_time_stamp = datetime.now(timezone.utc)
            db.session.add(neighbor)
            db.session.commit()
        if form.submit.data:
            return redirect(url_for("thank_page"))
        elif form.draw_another.data:
            return redirect(url_for("survey_draw", first = "next"))
    if first == "first":
        form.cur_neighborhood.data = cur_neighbor.neighborhood_name
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
