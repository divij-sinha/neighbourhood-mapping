from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, SelectField, RadioField, StringField, DecimalField
from wtforms.validators import NumberRange, DataRequired, InputRequired, ValidationError
from utils import get_geojson

def validator_geo_json(form, field):
    parsed_geojson = get_geojson(field.data)
    if len(parsed_geojson["features"]) != 1:
        raise ValidationError()
    
class SurveyStart(FlaskForm): 
    cur_neighborhood = StringField("What is the name of your neighborhood?", 
                            description="What is the name of your neighborhood?",
                            validators=[DataRequired()])
    years_lived = DecimalField("How many years have you lived here?",
                            description="How many years have you lived here?",
                            default=0.0,places=1,
                            validators=[NumberRange(0,100),DataRequired()])
    rent_own = RadioField("Do you rent or own your current residence?", choices=["Rent","Own"], validators=[DataRequired()])
    mark_layer = HiddenField("invisible_str_mark",validators=[DataRequired(),validator_geo_json])

    submit = SubmitField("Next!")

class SurveyDraw(FlaskForm):
    cur_neighborhood = StringField("What is the name of your neighborhood?", 
                            description="What is the name of your neighborhood?")
    draw_layer = HiddenField("invisible_str_draw",validators=[DataRequired(),validator_geo_json])
    submit = SubmitField("Submit and Finish!")
    draw_another = SubmitField("Draw Another Neighborhood?")

class AgreeButton(FlaskForm):
    agree = SubmitField("I Agree")