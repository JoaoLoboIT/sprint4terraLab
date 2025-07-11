from flask import Flask
import os
from .database import db

def create_app():
    app = Flask(__name__)

    # Configuração do banco de dados e chave secreta
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SECRET_KEY'] = 'postgre'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:postgre@localhost:5432/sprint4'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Importa e registra os Blueprints (nossas rotas)
    from .routes.auth_routes import auth
    from .routes.user_routes import user
    from .routes.ponto_routes import ponto

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(ponto, url_prefix='/ponto')

    # Cria as tabelas do banco de dados, se não existirem
    with app.app_context():
        db.create_all()

    return app