from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    HiddenField,
    RadioField,
    StringField,
    DecimalField,
    TextAreaField,
    SelectMultipleField,
)
from wtforms import widgets
from wtforms.validators import NumberRange, DataRequired, ValidationError, Optional
from utils import get_geojson
from flask_babel import lazy_gettext


def validator_geo_json(form, field):
    parsed_geojson = get_geojson(field.data)
    if len(parsed_geojson["features"]) != 1:
        raise ValidationError("Please fill in the requirement!")


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """

    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SurveyStart(FlaskForm):
    # cur_neighborhood = StringField(
    #     "What is the name of your neighborhood?",
    #     description="Choose from the list, or type your own!",
    #     validators=[DataRequired()],
    # )
    # years_lived = DecimalField(
    #     "How many years in total have you lived here?",
    #     description="How many years in total have you lived here?",
    #     default=0.0,
    #     places=1,
    #     validators=[NumberRange(0, 100)],
    # )
    # rent_own = RadioField(
    #     "Do you rent or own your current residence?",
    #     choices=[
    #         ("rent", "I rent it"),
    #         ("own", "I own it"),
    #         ("other", "Other arrangement"),
    #     ],
    #     validators=[Optional()],
    # )
    mark_layer = HiddenField(
        "invisible_str_mark", validators=[DataRequired(), validator_geo_json]
    )

    submit = SubmitField(lazy_gettext("Next!"))


class SurveyDraw(FlaskForm):
    cur_neighborhood = StringField(
        "",
        description=lazy_gettext("Choose from the list, or type your own!"),
        validators=[Optional()]
    )
    draw_layer = HiddenField(
        "invisible_str_draw", validators=[]
    )
    user_relationship = MultiCheckboxField(
        lazy_gettext("How do you know this neighborhood? (Select all that apply)"),
        validators=[Optional()],
        default="default",
        choices=[
            ("past_live", lazy_gettext("I used to live here")),
            # ("rel_live", "Someone I know lives here"),
            ("work", lazy_gettext("I work/worked here")),
            ("school", lazy_gettext("I go/went to school here")),
            ("visit", lazy_gettext("I visit/visited friends here")),
            ("shop", lazy_gettext("I shop/shopped here")),
            ("other", lazy_gettext("Other")),
        ],
    )
    submit = SubmitField(lazy_gettext("I'm done!"))
    draw_another = SubmitField(lazy_gettext("I want to draw the boundary of another neighborhood"))


class SurveyDemo(FlaskForm):
    years_lived = DecimalField(
        lazy_gettext("How many years in total have you lived in your current neighborhood?"),
        description=lazy_gettext("How many years in total have you lived in your current neighborhood?"),
        default=0.0,
        places=1,
        validators=[Optional(), NumberRange(0, 100)],
    )
    years_lived_chicago = DecimalField(
        lazy_gettext("How many years in total have you lived in the city of Chicago?"),
        description=lazy_gettext("How many years in total have you lived in the city of Chicago?"),
        default=0.0,
        places=1,
        validators=[Optional(), NumberRange(0, 100)],
    )
    rent_own = RadioField(
        lazy_gettext("Do you rent or own your current residence?"),
        choices=[
            ("rent", lazy_gettext("I rent it")),
            ("own", lazy_gettext("I own it")),
            ("other", lazy_gettext("Other arrangement")),
        ],
        validators=[Optional()],
    )
    gender = RadioField(
        lazy_gettext("What gender do you identify as?"),
        validators=[Optional()],
        default="none",
        choices=[
            ("man", lazy_gettext("Man")),
            ("woman", lazy_gettext("Woman")),
            ("nonbin", lazy_gettext("Non-Binary")),
            ("other", lazy_gettext("Other")),
        ],
    )
    age = RadioField(
        lazy_gettext("What is your age?"),
        validators=[Optional()],
        default="none",
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
    ethnicity = MultiCheckboxField(
        lazy_gettext("How would you identify your racial/ethnic background? (Select all that apply)"),
        validators=[Optional()],
        default="none",
        choices=[
            ("black_afamer", lazy_gettext("Black / African American")),
            ("hisp_latino", lazy_gettext("Hispanic / Latino")),
            ("white", lazy_gettext("White")),
            ("amer_ind_alaska", lazy_gettext("American Indian or Alaska Native")),
            ("haw_pac_isl", lazy_gettext("Native Hawaiian or Pacific Islander")),
            ("mid_east_nor_afr", lazy_gettext("Middle Eastern / North African")),
            ("asian", lazy_gettext("Asian")),
            ("multi_racial", lazy_gettext("Multi-racial / Two or more races")),
            ("other", lazy_gettext("Other")),
        ],
    )
    soc_cohes_neighborhood_knit = RadioField(
        lazy_gettext("I live in a close-knit neighborhood"),
        validators=[Optional()],
        default="none",
        choices=[
            ("strong_dis", lazy_gettext("Strong disagree")),
            ("somew_dis", lazy_gettext("Somewhat disagree")),
            ("neither", lazy_gettext("Neither agree nor disagree")),
            ("somew_agr", lazy_gettext("Somewhat agree")),
            ("strong_agr", lazy_gettext("Strong agree")),
        ],
    )
    soc_cohes_neighborhood_value = RadioField(
        lazy_gettext("People in my neighborhood share the same values"),
        validators=[Optional()],
        default="none",
        choices=[
            ("strong_dis", lazy_gettext("Strong disagree")),
            ("somew_dis", lazy_gettext("Somewhat disagree")),
            ("neither", lazy_gettext("Neither agree nor disagree")),
            ("somew_agr", lazy_gettext("Somewhat agree")),
            ("strong_agr", lazy_gettext("Strong agree")),
        ],
    )
    soc_cohes_neighborhood_talk = RadioField(
        lazy_gettext("I regularly stop and talk with people in my neighborhood"),
        validators=[Optional()],
        default="none",
        choices=[
            ("strong_dis", lazy_gettext("Strong disagree")),
            ("somew_dis", lazy_gettext("Somewhat disagree")),
            ("neither", lazy_gettext("Neither agree nor disagree")),
            ("somew_agr", lazy_gettext("Somewhat agree")),
            ("strong_agr", lazy_gettext("Strong agree")),
        ],
    )
    soc_cohes_neighborhood_belong = RadioField(
        lazy_gettext("I feel like I belong in my neighborhood"),
        validators=[Optional()],
        default="none",
        choices=[
            ("strong_dis", lazy_gettext("Strong disagree")),
            ("somew_dis", lazy_gettext("Somewhat disagree")),
            ("neither", lazy_gettext("Neither agree nor disagree")),
            ("somew_agr", lazy_gettext("Somewhat agree")),
            ("strong_agr", lazy_gettext("Strong agree")),
        ],
    )
    submit = SubmitField(lazy_gettext("I'm done!"))
    submit_giftcard = SubmitField(lazy_gettext("Enter to win $50 gift card"))


class SurveyFeedback(FlaskForm):
    feedback = TextAreaField(
        label=lazy_gettext("Write feedback here!"),
        validators=[Optional()],
        description=lazy_gettext("Write feedback here!"),
    )
    email = StringField(
        label=lazy_gettext("Enter email here!"),
        validators=[Optional()],
        description=lazy_gettext("Enter email here!"),
    )
    agree = SubmitField(lazy_gettext("I'm done!"))


class AgreeButton(FlaskForm):
    agree = SubmitField(lazy_gettext("Start survey!"))
