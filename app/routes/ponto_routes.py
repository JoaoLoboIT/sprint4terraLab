from flask import Blueprint, render_template, request, redirect, url_for, session
from ..models.User import User
from ..models.Ponto import Ponto
from ..database import db
from geoalchemy2.elements import WKTElement 

ponto = Blueprint('ponto', __name__)

@ponto.route('/adicionar', methods=['GET', 'POST'])
def adicionar_ponto():
    if 'user_id' not in session:
        return redirect(url_for('auth.mostrar_pagina_login'))

    if request.method == 'POST':
        lat = request.form['latitude']
        lon = request.form['longitude']
        desc = request.form['descricao']

        ponto_geometrico = WKTElement(f'POINT({lon} {lat})', srid=4326)

        novo_ponto = Ponto(
            latitude=lat,
            longitude=lon,
            descricao=desc,
            user_id=session['user_id'],
            geom=ponto_geometrico  
        )
        db.session.add(novo_ponto)
        db.session.commit()
        return redirect(url_for('user.mostrar_pagina_usuario'))

    return render_template('adicionar_ponto.html')

@ponto.route('/meus-pontos')
def ver_meus_pontos():
    if 'user_id' not in session:
        return redirect(url_for('auth.mostrar_pagina_login'))
    
    usuario = User.query.get_or_404(session['user_id'])
    return render_template('listar_pontos.html', usuario=usuario, lista_de_pontos=usuario.pontos)

@ponto.route('/<int:ponto_id>/alterar', methods=['GET', 'POST'])
def alterar_ponto(ponto_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.mostrar_pagina_login'))

    ponto_para_alterar = Ponto.query.get_or_404(ponto_id)
    if ponto_para_alterar.user_id != session['user_id']:
        return "Acesso negado!", 403

    if request.method == 'POST':
        nova_lat = request.form['latitude']
        nova_lon = request.form['longitude']

        ponto_para_alterar.latitude = nova_lat
        ponto_para_alterar.longitude = nova_lon
        ponto_para_alterar.descricao = request.form['descricao']

        ponto_para_alterar.geom = WKTElement(f'POINT({nova_lon} {nova_lat})', srid=4326)
        db.session.commit()
        return redirect(url_for('ponto.ver_meus_pontos'))

    return render_template('alterar_ponto.html', ponto=ponto_para_alterar)

@ponto.route('/<int:ponto_id>/remover', methods=['POST'])
def remover_ponto(ponto_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.mostrar_pagina_login'))

    ponto_para_remover = Ponto.query.get_or_404(ponto_id)
    if ponto_para_remover.user_id != session['user_id']:
        return "Acesso negado!", 403
        
    db.session.delete(ponto_para_remover)
    db.session.commit()
    return redirect(url_for('ponto.ver_meus_pontos'))