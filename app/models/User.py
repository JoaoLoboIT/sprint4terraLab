from ..database import db  

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(80), nullable=False)
    pontos = db.relationship('Ponto', backref='autor', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "senha": self.senha
        }