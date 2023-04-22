from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, RadioField, StringField, DecimalField
from wtforms.validators import NumberRange, DataRequired, ValidationError, Optional
from utils import get_geojson

def validator_geo_json(form, field):
    parsed_geojson = get_geojson(field.data)
    if len(parsed_geojson["features"]) != 1:
        raise ValidationError()
    
class SurveyStart(FlaskForm): 
    cur_neighborhood = StringField("What is the name of your neighborhood?", 
                            description="Choose from the list, or type your own!",
                            validators=[DataRequired()])
    years_lived = DecimalField("How many years have you lived here?",
                            description="How many years have you lived here?",
                            default=0.0,places=1,
                            validators=[NumberRange(0,100)])
    rent_own = RadioField("Do you rent or own your current residence?", 
                          choices=[("rent","Rent"),("own","Own"),("other","Other Arrangements")], 
                          validators=[Optional()])
    mark_layer = HiddenField("invisible_str_mark",validators=[DataRequired(),validator_geo_json])

    submit = SubmitField("Next!")

class SurveyDraw(FlaskForm):
    cur_neighborhood = StringField("What is the name of this neighborhood?", 
                            description="Choose from the list, or type your own!")
    draw_layer = HiddenField("invisible_str_draw",validators=[DataRequired(),validator_geo_json])
    submit = SubmitField("I'm done!")
    draw_another = SubmitField("I want to draw the boundary of another neighborhood")

class AgreeButton(FlaskForm):
    agree = SubmitField("Yes, I agree to participate")