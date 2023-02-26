from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, SelectField, IntegerRangeField, RadioField
from wtforms.validators import NumberRange
import pandas as pd

def comm_areas_list() -> list:
    df = pd.read_csv("app/data/comm_area_list.csv")
    return df["COMMUNITY"].to_list()
    
class SurveyStart(FlaskForm): 
    cur_neighbourhood = SelectField("Your neighbourhood", 
                            description = "What is the name of your neighborhood?", 
                            choices=comm_areas_list())
    
    years_lived = IntegerRangeField("Years lived in this neighbourhood",
                            description = "How many years have you lived here?",
                            validators=[NumberRange(0,100)])
    mark_layer = HiddenField("invisible_str_mark")

    submit = SubmitField("Submit")

class SurveyDraw(FlaskForm):
    cur_neighbourhood = SelectField("Neighbourhood", 
                            description = "What is the name of this neighborhood?", 
                            choices=comm_areas_list())
    draw_another = RadioField("Draw another neighbourhood you know?", choices=["Yes","No"])
    draw_layer = HiddenField("invisible_str_draw")
    submit = SubmitField("Submit")

class SurveyDrawFirst(FlaskForm):
    draw_another = RadioField("Draw another neighbourhood you know?", choices=["Yes","No"])
    draw_layer = HiddenField("invisible_str_draw")
    submit = SubmitField("Submit")
