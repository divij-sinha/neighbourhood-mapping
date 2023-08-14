from app import db
from geoalchemy2 import Geometry


class Location(db.Model):
    user_id = db.Column(db.String(36), primary_key=True)
    geometry = db.Column(Geometry("POINT"))
    time_stamp = db.Column(db.DateTime(timezone=True))
    name = db.Column(db.String(200))
    rent_own = db.Column(db.String(5))
    years_lived = db.Column(db.Float())
    neighborhoods = db.relationship(
        "Neighborhood", backref="neighborhoods", lazy="subquery"
    )


class Neighborhood(db.Model):
    neighborhood_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey("location.user_id"))
    name = db.Column(db.String(200))
    geometry = db.Column(Geometry("POLYGON"))
    time_stamp = db.Column(db.DateTime(timezone=True))
    user_relationship = db.Column(db.String(10))


class Respondent(db.Model):
    user_id = db.Column(
        db.String(36), db.ForeignKey("location.user_id"), primary_key=True
    )
    gender = db.Column(db.String(10))
    age = db.Column(db.String(5))
    ethnicity = db.Column(db.String(20))
    soc_cohes_neighborhood_knit = db.Column(db.String(10))
    soc_cohes_neighborhood_value = db.Column(db.String(10))
    soc_cohes_neighborhood_talk = db.Column(db.String(10))
    soc_cohes_neighborhood_belong = db.Column(db.String(10))
