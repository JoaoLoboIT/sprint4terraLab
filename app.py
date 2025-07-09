from flask import Flask, render_template, request, redirect, url_for, session
import os 
from database import db
from entities.User import User
from entities.Ponto import Ponto

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
SUA_SENHA_POSTGRES = 'postgre'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{SUA_SENHA_POSTGRES}@localhost:5432/sprint4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def mostrar_pagina_login():
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def receber_dados_login():
    email = request.form['email']
    senha = request.form['senha'] 

    usuario_existente = User.query.filter_by(email=email).first()

    if usuario_existente is None:
        novo_usuario = User(email=email, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect(url_for('mostrar_pagina_usuario', email=email, senha=senha))
    else:
        if senha == usuario_existente.senha:
            return redirect(url_for('mostrar_pagina_usuario', email=email, senha=senha))
        else:
            return "<h1>Senha incorreta!</h1><a href='/'>Tente novamente</a>"
  
@app.route("/user")
def mostrar_pagina_usuario():
    email = request.args.get('email')
    senha = request.args.get('senha')
    if email and senha:
        return render_template('user.html', email=email, senha=senha)
    else:
        return "Usuário não encontrado", 404
    
@app.route('/logout', methods=['POST'])
def logout():
    return render_template('login.html')

@app.route('/adicionar_ponto', methods=['POST'])
def adicionar_ponto():
    if 'user_id' not in session:
        return redirect(url_for('mostrar_pagina_login'))

    lat = request.form['latitude']
    lon = request.form['longitude']
    desc = request.form['descricao']
    
    user_id_logado = session['user_id']

    novo_ponto = Ponto(latitude=lat, longitude=lon, descricao=desc, user_id=user_id_logado)

    db.session.add(novo_ponto)
    db.session.commit()

    return redirect(url_for('mostrar_pagina_usuario'))