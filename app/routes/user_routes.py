from flask import Blueprint, render_template, request, redirect, url_for, session
from ..models.User import User
from ..models.Ponto import Ponto
from ..database import db

user = Blueprint('user', __name__)

@user.route('/')
def mostrar_pagina_usuario():
    if 'user_id' in session:
        usuario = User.query.get(session['user_id'])
        return render_template('user.html', usuario=usuario)
    return redirect(url_for('auth.mostrar_pagina_login'))
