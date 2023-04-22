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
    user_relationship = RadioField("What is your relationship with this neighborhood?", 
                                   validators=[Optional()],
                                   default = "default",
                                   choices=[("past_live","I used to live here"),
                                            ("rel_live","Someone I know lives here"),
                                            ("work", "I work/worked here"),
                                            ("visit", "I like to vist here"),
                                            ("other","Other Arrangements")])
    submit = SubmitField("I'm done!")
    draw_another = SubmitField("I want to draw the boundary of another neighborhood")

class SurveyDemo(FlaskForm):
    gender = RadioField("What gender do you identify as?",
                        validators=[Optional()],
                        default = "default",
                        choices=[("man","Man"),("woman","Woman"),("nonbin","Non-Binary"),("other", "Other")])
    age = RadioField("What age group do you fall in?",
                        validators=[Optional()],
                        default = "default",
                        choices=[("1825","18-25"),("2635","26-35"),("3645","36-45"),("4660", "46-60"),("6080", "60-80"),("80", "80+")])
    ethnicity = RadioField("What race or ethnic group do you most closely identify with?",
                        validators=[Optional()],
                        default = "default",
                        choices = [("tbd","tbd")],
                        )
    submit = SubmitField("I'm done!")
    
class AgreeButton(FlaskForm):
    agree = SubmitField("Yes, I agree to participate")