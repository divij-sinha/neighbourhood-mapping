from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, SelectField, IntegerField, RadioField
from wtforms.validators import NumberRange
import pandas as pd

def neighborhood_list() -> list:
    df = pd.read_csv("app/data/neighborhoods233.csv")
    return df["name"].to_list()
    
class SurveyStart(FlaskForm): 
    cur_neighbourhood = SelectField("Your neighbourhood", 
                            description = "What is the name of your neighborhood?", 
                            choices=neighborhood_list())
    
    years_lived = IntegerField("Years lived in this neighbourhood",
                            description = "How many years have you lived here?",
                            validators=[NumberRange(0,100)])
    mark_layer = HiddenField("invisible_str_mark")

    submit = SubmitField("Submit")

class SurveyDraw(FlaskForm):
    cur_neighbourhood = SelectField("Neighbourhood", 
                            description = "What is the name of this neighborhood?", 
                            choices=neighborhood_list())
    draw_another = RadioField("Draw another neighbourhood you know?", choices=["Yes","No"])
    draw_layer = HiddenField("invisible_str_draw")
    submit = SubmitField("Submit")

class SurveyDrawFirst(FlaskForm):
    draw_another = RadioField("Draw another neighbourhood you know?", choices=["Yes","No"])
    draw_layer = HiddenField("invisible_str_draw")
    submit = SubmitField("Submit")
