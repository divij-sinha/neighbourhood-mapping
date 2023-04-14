from app import db

class Neighborhood(db.Model):
    id_key = db.Column(db.String(64), primary_key = True)
    id_user = db.Column(db.String(64))
    neighborhood_name = db.Column(db.String(200))
    location_geojson = db.Column(db.String(1000))
    neighborhood_geojson = db.Column(db.String(1000))