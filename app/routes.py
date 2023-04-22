from app import app, db
from app.models import Neighborhood, Location
from app.forms import SurveyStart, SurveyDraw, AgreeButton
from flask import render_template, redirect, url_for, session
from wtforms.validators import DataRequired
from utils import get_geojson, get_map_comps, get_neighborhood_list
from datetime import datetime, timezone
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import shape
import uuid

neighborhood_list = get_neighborhood_list()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def start_page():
    agree = AgreeButton()
    if agree.validate_on_submit():
        session["uuid"] = str(uuid.uuid4())
        location = Location(user_id = session["uuid"], time_stamp = datetime.now(timezone.utc))
        db.session.add(location)
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
        location = Location.query.filter_by(user_id = session["uuid"]).first()
        location.geometry = from_shape(shape(parsed_geojson["features"][0]["geometry"]))
        location.name = form.cur_neighborhood.data
        location.rent_own = form.rent_own.data
        location.years_lived = form.years_lived.data
        location.time_stamp = datetime.now(timezone.utc)
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
        location = Location.query.filter_by(user_id = session["uuid"]).first()
        pt = to_shape(location.geometry)
        loc = pt.y, pt.x
    else:
        loc = (41.8781, -87.6298)
    header, body_html, script = get_map_comps(loc = loc, zoom = 13, draw_options=draw_options)
    form = SurveyDraw()
    if (form.validate_on_submit() and first == 'first') or form.validate_on_submit(extra_validators={'cur_neighborhood':[DataRequired()]}):
        parsed_geojson = get_geojson(form.draw_layer.data)
        if first == 'first':
            neighborhood = Neighborhood(
                user_id = session["uuid"],
                name = location.name,
                geometry = from_shape(shape(parsed_geojson["features"][0]["geometry"])),
                user_relationship = "cur_live",
                time_stamp = datetime.now(timezone.utc)
            )
            db.session.add(neighborhood)
            db.session.commit()
        else:
            neighborhood = Neighborhood(
                user_id = session["uuid"],
                name = form.cur_neighborhood.data,
                geometry = from_shape(shape(parsed_geojson["features"][0]["geometry"])),
                user_relationship = form.user_relationship.data,
                time_stamp = datetime.now(timezone.utc)
            )
            db.session.add(neighborhood)
            db.session.commit()
        if form.submit.data:
            return redirect(url_for("thank_page"))
        elif form.draw_another.data:
            return redirect(url_for("survey_draw", first = "next"))
    if first == "first":
        form.cur_neighborhood.data = location.name
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
