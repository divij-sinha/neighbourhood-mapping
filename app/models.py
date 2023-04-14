from app import db
from geoalchemy2 import Geometry

class Neighborhood(db.Model):
    id_key = db.Column(db.Integer, primary_key = True)
    id_user = db.Column(db.String(64))
    neighborhood_name = db.Column(db.String(200))
    location_geojson = db.Column(Geometry('POINT'))
    neighborhood_geojson = db.Column(Geometry('POLYGON'))
    ### change name
    neighborhood_time_stamp = db.Column(db.DateTime(timezone=True))
    rent_own = db.Column(db.String(10))
    years_lived = db.Column(db.Float())
    first = db.Column(db.String(10))