from flask import Blueprint, render_template, request, redirect, url_for, session
from ..models.User import User
from ..database import db

auth = Blueprint('auth', __name__)

@auth.route('/')
def mostrar_pagina_login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def receber_dados_login():
    email = request.form['email']
    senha = request.form['senha']
    usuario_existente = User.query.filter_by(email=email).first()

    if usuario_existente:
        if senha == usuario_existente.senha:
            session['user_id'] = usuario_existente.id
            return redirect(url_for('user.mostrar_pagina_usuario'))
        else:
            return "<h1>Senha incorreta!</h1><a href=\"{{ url_for('auth.mostrar_pagina_login') }}\">Tente novamente</a>"
    else:
        novo_usuario = User(email=email, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()
        session['user_id'] = novo_usuario.id
        return redirect(url_for('user.mostrar_pagina_usuario'))

@auth.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.mostrar_pagina_login'))