from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, SelectField, RadioField, StringField, DecimalField
from wtforms.validators import NumberRange, DataRequired, InputRequired
import pandas as pd

def neighborhood_list() -> list:
    df = pd.read_csv("app/data/neighborhoods233.csv")
    return df["name"].to_list()
    
class SurveyStart(FlaskForm): 
    cur_neighbourhood = StringField("What is the name of your neighborhood?", 
                            description="What is the name of your neighborhood?",
                            validators=[DataRequired()])
    years_lived = DecimalField("How many years have you lived here?",
                            description="How many years have you lived here?",
                            default=0,places=1,
                            validators=[NumberRange(0,100),DataRequired()])
    rent_own = RadioField("Do you rent or own your current residence?", choices=["Rent","Own"], validators=[DataRequired()])
    mark_layer = HiddenField("invisible_str_mark",validators=[DataRequired()])

    submit = SubmitField("Submit")

class SurveyDraw(FlaskForm):
    cur_neighbourhood = SelectField("Neighbourhood", 
                            description = "What is the name of this neighborhood?", 
                            choices=neighborhood_list())
    draw_another = RadioField("Draw another neighbourhood you know?", choices=["Yes","No"],validators=[InputRequired()])
    draw_layer = HiddenField("invisible_str_draw")
    submit = SubmitField("Submit")

class SurveyDrawFirst(FlaskForm):
    draw_another = RadioField("Draw another neighbourhood you know?", choices=["Yes","No"])
    draw_layer = HiddenField("invisible_str_draw")
    submit = SubmitField("Submit")

class AgreeButton(FlaskForm):
    agree = SubmitField("I Agree")