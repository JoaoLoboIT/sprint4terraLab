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

def listar_pontos_de_usuario(user_id=None, email=None):
    if not user_id and not email:
        raise ValueError("É necessário fornecer um ID ou um email de usuário.")

    usuario = None
    if user_id:
        usuario = User.query.get(user_id)
    elif email:
        usuario = User.query.filter_by(email=email).first()

    if not usuario:
        raise ValueError("Usuário não encontrado")
        
    return usuario.pontos

def alterar_ponto(ponto_id, email_usuario, senha_usuario, novos_dados):
    if not ponto_id or not email_usuario or not senha_usuario:
        raise ValueError("ID do ponto, email e senha do usuário são obrigatórios.")

    ponto = Ponto.query.get(ponto_id)
    if not ponto:
        raise ValueError("Ponto não encontrado")

    if ponto.autor.email != email_usuario:
        raise PermissionError("Acesso negado. O ponto não pertence a este usuário.")

    if ponto.autor.senha != senha_usuario:
        raise PermissionError("Senha incorreta.")

    mudancas = {}
    
    nova_lat = novos_dados.get('latitude')
    nova_lon = novos_dados.get('longitude')
    nova_desc = novos_dados.get('descricao')

    if nova_lat is not None and float(nova_lat) != ponto.latitude:
        mudancas['latitude'] = {'antiga': ponto.latitude, 'nova': float(nova_lat)}
        ponto.latitude = float(nova_lat)

    if nova_lon is not None and float(nova_lon) != ponto.longitude:
        mudancas['longitude'] = {'antiga': ponto.longitude, 'nova': float(nova_lon)}
        ponto.longitude = float(nova_lon)

    if nova_desc is not None and nova_desc != ponto.descricao:
        mudancas['descricao'] = {'antiga': ponto.descricao, 'nova': nova_desc}
        ponto.descricao = nova_desc
    
    if mudancas:
        ponto.geom = WKTElement(f'POINT({ponto.longitude} {ponto.latitude})', srid=4326)
        db.session.commit()
    
    return mudancas

def remover_ponto(ponto_id, email_usuario, senha_usuario):
    if not ponto_id or not email_usuario or not senha_usuario:
        raise ValueError("ID do ponto, email e senha são obrigatórios.")

    ponto = Ponto.query.get(ponto_id)
    if not ponto:
        raise ValueError("Ponto não encontrado")

    if ponto.autor.email != email_usuario:
        raise PermissionError("Acesso negado. O ponto não pertence a este usuário.")

    if ponto.autor.senha != senha_usuario:
        raise PermissionError("Senha incorreta.")
    
    dados_ponto = ponto.to_dict()
    dados_autor = ponto.autor.to_dict()

    db.session.delete(ponto)
    db.session.commit()

    return dados_ponto, dados_autor

def listar_todos_os_pontos():
    return Ponto.query.all()