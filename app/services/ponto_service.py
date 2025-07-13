from ..models.User import User
from ..models.Ponto import Ponto
from ..database import db
from geoalchemy2.elements import WKTElement

def criar_ponto(email_usuario, senha_usuario, lat, lon, desc):
    if not email_usuario or not senha_usuario:
        raise ValueError("Email e senha são obrigatórios para criar um ponto.")

    usuario = User.query.filter_by(email=email_usuario).first()
    
    if not usuario:
        raise ValueError("Usuário não encontrado")
    if usuario.senha != senha_usuario:
        raise PermissionError("Senha incorreta")

    ponto_geom = WKTElement(f'POINT({lon} {lat})', srid=4326)
    novo_ponto = Ponto(
        latitude=lat,
        longitude=lon,
        descricao=desc,
        user_id=usuario.id,
        geom=ponto_geom
    )
    db.session.add(novo_ponto)
    db.session.commit()
    
    return novo_ponto, usuario

def listar_pontos_de_usuario(email):
    usuario = User.query.filter_by(email=email).first()
    if not usuario:
        raise ValueError("Usuário não encontrado")
    return usuario.pontos

def alterar_ponto(ponto_id, email_usuario, novos_dados):
    ponto = Ponto.query.get(ponto_id)
    if not ponto:
        raise ValueError("Ponto não encontrado")
    
    if ponto.autor.email != email_usuario:
        raise PermissionError("Acesso negado. O ponto não pertence a este usuário.")

    nova_lat = novos_dados.get('latitude', ponto.latitude)
    nova_lon = novos_dados.get('longitude', ponto.longitude)
    
    ponto.descricao = novos_dados.get('descricao', ponto.descricao)
    ponto.geom = WKTElement(f'POINT({nova_lon} {nova_lat})', srid=4326)
    
    db.session.commit()
    return ponto

def remover_ponto(ponto_id, email_usuario):
    ponto = Ponto.query.get(ponto_id)
    if not ponto:
        raise ValueError("Ponto não encontrado")

    if ponto.autor.email != email_usuario:
        raise PermissionError("Acesso negado. O ponto não pertence a este usuário.")
    
    db.session.delete(ponto)
    db.session.commit()