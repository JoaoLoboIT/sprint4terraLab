from flask import Flask
import os
from .database import db

def create_app():
    app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SECRET_KEY'] = 'postgre'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:postgre@localhost:5432/sprint4'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .routes.auth_routes import auth
    from .routes.user_routes import user
    from .routes.ponto_routes import ponto
    from .routes.api_routes import api

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(ponto, url_prefix='/ponto')
    app.register_blueprint(api, url_prefix='/')

    with app.app_context():
        db.create_all()

    return app