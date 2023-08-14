from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, RadioField, StringField, DecimalField
from wtforms.validators import NumberRange, DataRequired, ValidationError, Optional
from utils import get_geojson


def validator_geo_json(form, field):
    parsed_geojson = get_geojson(field.data)
    if len(parsed_geojson["features"]) != 1:
        raise ValidationError()


class SurveyStart(FlaskForm):
    cur_neighborhood = StringField(
        "What is the name of your neighborhood?",
        description="Choose from the list, or type your own!",
        validators=[DataRequired()],
    )
    years_lived = DecimalField(
        "How many years in total have you lived here?",
        description="How many years in total have you lived here?",
        default=0.0,
        places=1,
        validators=[NumberRange(0, 100)],
    )
    rent_own = RadioField(
        "Do you rent or own your current residence?",
        choices=[
            ("rent", "I rent it"),
            ("own", "I own it"),
            ("other", "Other arrangement"),
        ],
        validators=[Optional()],
    )
    mark_layer = HiddenField(
        "invisible_str_mark", validators=[DataRequired(), validator_geo_json]
    )

    submit = SubmitField("Next!")


class SurveyDraw(FlaskForm):
    cur_neighborhood = StringField(
        "What is the name of this neighborhood?",
        description="Choose from the list, or type your own!",
    )
    draw_layer = HiddenField(
        "invisible_str_draw", validators=[DataRequired(), validator_geo_json]
    )
    user_relationship = RadioField(
        "How do you know this neighborhood?",
        validators=[Optional()],
        default="default",
        choices=[
            ("past_live", "I used to live here"),
            # ("rel_live", "Someone I know lives here"),
            ("work", "I work/worked here"),
            ("school", "I go/went to school here"),
            ("visit", "I visit/visited friends here"),
            ("shop", "I shop/shopped here"),
            ("other", "Other Arrangements"),
        ],
    )
    submit = SubmitField("I'm done!")
    draw_another = SubmitField("I want to draw the boundary of another neighborhood")


class SurveyDemo(FlaskForm):
    gender = RadioField(
        "What gender do you identify as?",
        validators=[Optional()],
        default="default",
        choices=[
            ("man", "Man"),
            ("woman", "Woman"),
            ("nonbin", "Non-Binary"),
            ("other", "Other"),
        ],
    )
    age = RadioField(
        "What age group do you fall in?",
        validators=[Optional()],
        default="default",
        choices=[
            ("1824", "18-24"),
            ("2534", "25-34"),
            ("3544", "35-44"),
            ("4554", "45-54"),
            ("5564", "55-64"),
            ("6574", "65-74"),
            ("75", "75+"),
        ],
    )
    ethnicity = RadioField(
        "How would you identify your racial/ethnic background?",
        validators=[Optional()],
        default="default",
        choices=[
            ("black_afamer", "Black / African American"),
            ("hisp_latino", "Hispanic / Latino"),
            ("white", "White"),
            ("amer_ind_alaska", "American Indian or Alaska Native"),
            ("haw_pac_isl", "Native Hawaiian or Pacific Islander"),
            ("mid_east_nor_afr", "Middle Eastern / North African"),
            ("asian", "Asian"),
            ("multi_racial", "Multi-racial / Two or more races"),
            ("other", "Other"),
        ],
    )
    submit = SubmitField("I'm done!")


class AgreeButton(FlaskForm):
    agree = SubmitField("Yes, I agree to participate")
