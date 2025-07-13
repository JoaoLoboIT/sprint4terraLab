from flask import Flask
from .database import db

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'postgre'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:postgre@localhost:5432/sprint4'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .routes.api_routes import api
    app.register_blueprint(api, url_prefix='/')

    with app.app_context():
        db.create_all()

    return app  