from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, SelectField
import pandas as pd

def comm_areas_list():
    df = pd.read_csv("app/data/comm_area_list.csv")
    return df["COMMUNITY"].to_list()

class SubmitMap(FlaskForm):
    cur_neighbourhood = SelectField(choices=comm_areas_list())
    cur_layer = HiddenField("str")
    submit = SubmitField("Submit")