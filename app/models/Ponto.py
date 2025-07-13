from ..database import db
from geoalchemy2 import Geometry

class Ponto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    geom = db.Column(Geometry(geometry_type='POINT', srid=4326))

    def to_dict(self):
        return {
            "id": self.id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "descricao": self.descricao,
            "user_id": self.user_id
        }