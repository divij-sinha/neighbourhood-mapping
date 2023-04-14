from app import app
from flask import render_template, redirect, url_for, session
from app.forms import SurveyStart, SurveyDraw, AgreeButton
from wtforms.validators import DataRequired
from utils import get_geojson, get_map_comps, get_neighborhood_list
import uuid

neighborhood_list = get_neighborhood_list()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def start_page():
    agree = AgreeButton()
    if agree.validate_on_submit():
        session["uuid"] = uuid.uuid4()
        return redirect(url_for("survey_form"))
    return render_template("start_page.html", agree=agree)

@app.route("/survey_form", methods=['GET', 'POST'])
def survey_form():
    draw_options = {"polygon":False, "polyline": False, "rectangle": False, "circle": False, "marker": False, "circlemarker": {"radius": 20},}
    header, body_html, script = get_map_comps(loc = (41.8781, -87.6298), zoom = 12, draw_options=draw_options)
    form = SurveyStart()
    
    if form.validate_on_submit():
        parsed_geojson = get_geojson(form.mark_layer.data)
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
