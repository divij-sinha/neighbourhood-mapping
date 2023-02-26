from app import app
from flask import render_template, redirect
from app.forms import SubmitMap
from utils import get_geojson, get_map_comps

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route("/components", methods=['GET', 'POST'])
def components():
    
    header, body_html, script = get_map_comps(loc = (41.8781, -87.6298), zoom = 12)

    form = SubmitMap()
    
    if form.validate_on_submit():
        parsed_geojson = get_geojson(form.cur_layer.data)

    return render_template("form_page.html",
        form=form,
        header=header,
        body_html=body_html,
        script=script,
    )



