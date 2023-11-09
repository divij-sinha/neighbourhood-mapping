from app import app, db
from app.models import Neighborhood, Location, Respondent, Feedback
from app.forms import (
    SurveyStart,
    SurveyDraw,
    AgreeButton,
    SurveyDemo,
    SurveyFeedback,
    validator_geo_json,
    DataRequired,
)
from flask import render_template, redirect, url_for, session, request
from utils import get_geojson, get_map_comps, get_neighborhood_list
from datetime import datetime, timezone
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import shape
import uuid
from flask_babel import Babel


def get_locale():
    if "locale" in session.keys():
        locale = session["locale"]
    else:
        locale = request.accept_languages.best_match(["en", "es", "zh", "pl"])
    return locale


babel = Babel(app, locale_selector=get_locale)


neighborhood_list = get_neighborhood_list()


@app.route("/locale/<locale>", methods=["GET"])
def set_locale(locale):
    session["locale"] = locale
    return redirect(url_for("start_page"))


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def start_page():
    agree = AgreeButton()
    if agree.validate_on_submit():
        session["uuid"] = str(uuid.uuid4())
        location = Location(
            user_id=session["uuid"], time_stamp=datetime.now(timezone.utc)
        )
        db.session.add(location)
        db.session.commit()
        return redirect(url_for("survey_form"))
    return render_template("start_page.html", agree=agree)


@app.route("/survey_form", methods=["GET", "POST"])
def survey_form():
    try:
        draw_options = {
            "polygon": False,
            "polyline": False,
            "rectangle": False,
            "circle": False,
            "marker": False,
            "circlemarker": {"radius": 20},
        }
        header, body_html, script = get_map_comps(
            loc=(41.8781, -87.6298), zoom=12, draw_options=draw_options
        )
        form = SurveyStart()

        if form.validate_on_submit():
            parsed_geojson = get_geojson(form.mark_layer.data)
            location = Location.query.filter_by(user_id=session["uuid"]).first()
            location.geometry = from_shape(
                shape(parsed_geojson["features"][0]["geometry"])
            )
            location.time_stamp = datetime.now(timezone.utc)
            db.session.commit()
            return redirect(url_for("survey_draw", first="first"))

        return render_template(
            "form_page_start.html",
            form=form,
            neighborhood_list=neighborhood_list,
            header=header,
            body_html=body_html,
            script=script,
        )
    except:
        redirect(url_for("start_page"))


@app.route("/survey_draw/<first>", methods=["GET", "POST"])
def survey_draw(first):
    try:
        draw_options = {
            "polyline": False,
            "rectangle": False,
            "circle": False,
            "marker": False,
            "circlemarker": False,
        }
        if first == "first":
            location = Location.query.filter_by(user_id=session["uuid"]).first()
            pt = to_shape(location.geometry)
            loc = pt.y, pt.x
        else:
            loc = (41.8781, -87.6298)
        header, body_html, script = get_map_comps(
            loc=loc, zoom=13, draw_options=draw_options
        )
        form = SurveyDraw()
        if (form.validate_on_submit() and first == "next") or (
            form.validate_on_submit(
                extra_validators={"draw_layer": [DataRequired(), validator_geo_json]}
            )
            and first == "first"
        ):
            parsed_geojson = get_geojson(form.draw_layer.data)
            try:
                geometry = from_shape(shape(parsed_geojson["features"][0]["geometry"]))
            except:
                geometry = None
            neighborhood = Neighborhood(
                user_id=session["uuid"],
                geometry=geometry,
                time_stamp=datetime.now(timezone.utc),
                name=form.cur_neighborhood.data,
            )
            if first == "first":
                neighborhood.user_relationship = ["cur_live"]
                # neighborhood.name = location.name
            else:
                neighborhood.user_relationship = form.user_relationship.data
                # neighborhood.name = form.cur_neighborhood.data
            db.session.add(neighborhood)
            db.session.commit()
            if form.submit.data:
                return redirect(url_for("survey_demo"))
            elif form.draw_another.data:
                return redirect(url_for("survey_draw", first="next"))
        # if first == "first":
        #     form.cur_neighborhood.data = location.name
        # else:
        # form.cur_neighborhood.data = ""
        return render_template(
            "form_page_draw.html",
            form=form,
            header=header,
            body_html=body_html,
            script=script,
            first=first,
            neighborhood_list=neighborhood_list,
        )
    except:
        redirect(url_for("start_page"))


@app.route("/survey_demo", methods=["GET", "POST"])
def survey_demo():
    try:
        form = SurveyDemo()
        if form.validate_on_submit():
            resp = Respondent.query.get(session["uuid"])
            if not resp:
                resp = Respondent()
                db.session.add(resp)

            resp.user_id = session["uuid"]
            resp.rent_own = form.rent_own.data
            resp.years_lived_chicago = form.years_lived_chicago.data
            resp.years_lived = form.years_lived.data
            resp.age = form.age.data
            resp.gender = form.gender.data
            resp.ethnicity = form.ethnicity.data
            resp.soc_cohes_neighborhood_knit = form.soc_cohes_neighborhood_knit.data
            resp.soc_cohes_neighborhood_value = form.soc_cohes_neighborhood_value.data
            resp.soc_cohes_neighborhood_talk = form.soc_cohes_neighborhood_talk.data
            resp.soc_cohes_neighborhood_belong = form.soc_cohes_neighborhood_belong.data
            db.session.commit()

            return redirect(url_for("thank_page", feedback_page="feedback"))

        return render_template("form_page_demo.html", form=form)
    except:
        redirect(url_for("start_page"))


@app.route("/thank_you/<feedback_page>", methods=["GET", "POST"])
def thank_page(feedback_page):
    try:
        form = SurveyFeedback()
        if form.validate_on_submit():
            feedback = Feedback(
                user_id=session["uuid"],
                feedback=form.feedback.data,
                email=form.email.data,
            )
            db.session.add(feedback)
            db.session.commit()
            return redirect(url_for("thank_page", feedback_page="thank_you"))
        return render_template(
            "thank_page.html", form=form, feedback_page=feedback_page
        )
    except:
        redirect(url_for("start_page"))
