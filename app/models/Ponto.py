from ..database import db
from geoalchemy2 import Geometry
from sqlalchemy.ext.hybrid import hybrid_property

class Ponto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    geom = db.Column(Geometry(geometry_type='POINT', srid=4326))

    @hybrid_property
    def latitude(self):
        if self.geom is not None:
            return self.geom.y

    @hybrid_property
    def longitude(self):
        if self.geom is not None:
            return self.geom.x

    def to_dict(self):
        return {
            "id": self.id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "descricao": self.descricao,
            "user_id": self.user_id
        }