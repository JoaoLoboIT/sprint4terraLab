from flask import Blueprint, render_template, request, redirect, url_for, session
from ..models.User import User
from ..models.Ponto import Ponto
from ..database import db

user = Blueprint('user', __name__)

@user.route('/')
def mostrar_pagina_usuario():
    if 'user_id' not in session:
        return redirect(url_for('auth.mostrar_pagina_login'))
    
    usuario = User.query.get_or_404(session['user_id'])
    return render_template('user.html', usuario=usuario)

@user.route('/alterar-login', methods=['GET', 'POST'])
def alterar_login():
    if 'user_id' not in session:
        return redirect(url_for('auth.mostrar_pagina_login'))
    
    usuario = User.query.get_or_404(session['user_id'])
    if request.method == 'POST':
        usuario.email = request.form['email']
        nova_senha = request.form['senha']
        if nova_senha:
            usuario.senha = nova_senha
        db.session.commit()
        return redirect(url_for('user.mostrar_pagina_usuario'))
    
    return render_template('alterar_login.html', usuario=usuario)

@user.route('/remover', methods=['POST'])
def remover_usuario():
    if 'user_id' not in session:
        return redirect(url_for('auth.mostrar_pagina_login'))
    
    usuario = User.query.get_or_404(session['user_id'])
    Ponto.query.filter_by(user_id=usuario.id).delete()
    db.session.delete(usuario)
    db.session.commit()
    session.clear()
    return redirect(url_for('auth.mostrar_pagina_login'))