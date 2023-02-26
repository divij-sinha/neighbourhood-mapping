from app import app
from flask import render_template, redirect, url_for
from app.forms import SurveyStart, SurveyDraw, SurveyDrawFirst
from utils import get_geojson, get_map_comps

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route("/survey_form", methods=['GET', 'POST'])
def survey_form():
    draw_options = {"polygon":False, "polyline": False, "rectangle": False, "circle": False, "marker": False, "circlemarker": {"radius": 20},}
    header, body_html, script = get_map_comps(loc = (41.8781, -87.6298), zoom = 12, draw_options=draw_options)
    form = SurveyStart()

    if form.validate_on_submit():
        print("HERE!")
        parsed_geojson = get_geojson(form.mark_layer.data)
        print(parsed_geojson)
        return redirect(url_for("survey_draw"), True)
    
    if form.is_submitted:
        print(form.cur_neighbourhood.data)
        print(form.years_lived.data)
        print(form.mark_layer.data)

    return render_template("form_page_start.html",
        form=form,
        header=header,
        body_html=body_html,
        script=script,
    )

@app.route("/survey_draw", methods=['GET', 'POST'])
def survey_draw(first_time: bool = True):
    draw_options = {"polyline": False, "rectangle": False, "circle": False, "marker": False, "circlemarker": False}
    header, body_html, script = get_map_comps(loc = (41.8781, -87.6298), zoom = 12, draw_options=draw_options)
    if first_time:
        form = SurveyDrawFirst()
    else:
        form = SurveyDraw()
    if form.validate_on_submit():
        if form.draw_another.data == "Yes":
            parsed_geojson = get_geojson(form.draw_layer.data)
            print(parsed_geojson)
            return redirect(url_for("survey_draw", False))
        else:
            pass

    return render_template("form_page_draw.html",
        form=form,
        header=header,
        body_html=body_html,
        script=script,
    )