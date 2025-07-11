from flask import Blueprint, render_template, request, redirect, url_for, session
from ..models.User import User
from ..models.Ponto import Ponto
from ..database import db

ponto = Blueprint('ponto', __name__)

@ponto.route('/adicionar', methods=['GET', 'POST'])
def adicionar_ponto():
    if 'user_id' not in session:
        return redirect(url_for('auth.mostrar_pagina_login'))

    if request.method == 'POST':
        user_id_logado = session['user_id']
        novo_ponto = Ponto(...)
        db.session.add(novo_ponto)
        db.session.commit()
        return redirect(url_for('user.mostrar_pagina_usuario'))

    return render_template('adicionar_ponto.html')
