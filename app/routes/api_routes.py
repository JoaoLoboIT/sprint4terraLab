from flask import Blueprint, request, jsonify
from ..models.User import User
from ..models.Ponto import Ponto
from ..database import db
from geoalchemy2.elements import WKTElement

api = Blueprint('api', __name__)

# --- ROTAS DE USUÁRIO ---

# Adicionar um novo usuário 
@api.route('/AdicionarUsuario', methods=['POST'])
def adicionar_usuario_api():
    email = request.args.get('email')
    senha = request.args.get('senha') 

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400 # 

    if User.query.filter_by(email=email).first():
        return jsonify({"erro": "Usuário com este email já existe"}), 409

    novo_usuario = User(email=email, senha=senha) 
    db.session.add(novo_usuario)
    db.session.commit()
    
    return jsonify({"mensagem": "Usuário criado com sucesso", "id": novo_usuario.id}), 201

# Listar todos os usuários
@api.route('/ListarUsuarios', methods=['GET'])
def listar_usuarios_api():
    usuarios = User.query.all()
    lista_de_usuarios = [{"id": u.id, "email": u.email} for u in usuarios]
    return jsonify(lista_de_usuarios), 200

# Alterar email ou senha de um usuário
@api.route('/AlterarUsuario', methods=['POST'])
def alterar_usuario_api():
    email_atual = request.args.get('email_atual')
    if not email_atual:
        return jsonify({"erro": "O parâmetro 'email_atual' é obrigatório"}), 400

    usuario = User.query.filter_by(email=email_atual).first()
    if not usuario:
        return jsonify({"erro": "Usuário a ser alterado não encontrado"}), 404

    novo_email = request.args.get('novo_email')
    nova_senha = request.args.get('nova_senha')

    if novo_email:
        usuario.email = novo_email
    if nova_senha:
        usuario.senha = nova_senha
    
    db.session.commit()
    return jsonify({"mensagem": "Usuário atualizado com sucesso"}), 200

# Remover um usuário e todos os seus pontos
@api.route('/RemoverUsuario', methods=['POST'])
def remover_usuario_api():
    email = request.args.get('email')
    usuario = User.query.filter_by(email=email).first()

    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    Ponto.query.filter_by(user_id=usuario.id).delete()
    db.session.delete(usuario)
    db.session.commit()
    
    return jsonify({"mensagem": "Usuário e seus pontos foram removidos com sucesso"}), 200


# --- ROTAS DE PONTO ---

# Adicionar um novo ponto geográfico para um usuário
@api.route('/AdicionarPonto', methods=['POST'])
def adicionar_ponto_api():
    email = request.args.get('email')
    lat = request.args.get('latitude')
    lon = request.args.get('longitude')
    desc = request.args.get('descricao', "")

    if not all([email, lat, lon]):
        return jsonify({"erro": "Parâmetros 'email', 'latitude' e 'longitude' são obrigatórios"}), 400

    usuario = User.query.filter_by(email=email).first()
    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    ponto_geom = WKTElement(f'POINT({lon} {lat})', srid=4326)
    novo_ponto = Ponto(latitude=lat, longitude=lon, descricao=desc, user_id=usuario.id, geom=ponto_geom)
    db.session.add(novo_ponto)
    db.session.commit()

    return jsonify({"mensagem": "Ponto adicionado com sucesso", "ponto_id": novo_ponto.id}), 201

# Listar todos os pontos de um usuário específico
@api.route('/ListarPontos', methods=['GET'])
def listar_pontos_api():
    email = request.args.get('email')
    if not email:
        return jsonify({"erro": "Parâmetro 'email' é obrigatório"}), 400

    usuario = User.query.filter_by(email=email).first()
    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    pontos_lista = [{"id": p.id, "latitude": p.latitude, "longitude": p.longitude, "descricao": p.descricao} for p in usuario.pontos]
    return jsonify(pontos_lista), 200

# Alterar os dados de um ponto existente
@api.route('/AlterarPonto', methods=['POST'])
def alterar_ponto_api():
    ponto_id = request.args.get('id')
    email_usuario = request.args.get('user')

    if not ponto_id or not email_usuario:
        return jsonify({"erro": "Parâmetros 'id' (do ponto) e 'user' (email do usuário) são obrigatórios"}), 400

    ponto = Ponto.query.get(ponto_id)
    if not ponto:
        return jsonify({"erro": "Ponto não encontrado"}), 404
        
    if ponto.autor.email != email_usuario:
        return jsonify({"erro": "Acesso negado. O ponto não pertence a este usuário."}), 403

    ponto.latitude = request.args.get('latitude', ponto.latitude)
    ponto.longitude = request.args.get('longitude', ponto.longitude)
    ponto.descricao = request.args.get('descricao', ponto.descricao)
    ponto.geom = WKTElement(f'POINT({ponto.longitude} {ponto.latitude})', srid=4326)

    db.session.commit()
    return jsonify({"mensagem": "Ponto atualizado com sucesso"}), 200

# Remover um ponto específico
@api.route('/RemoverPonto', methods=['POST'])
def remover_ponto_api():
    ponto_id = request.args.get('id')
    email_usuario = request.args.get('user')

    if not ponto_id or not email_usuario:
        return jsonify({"erro": "Parâmetros 'id' (do ponto) e 'user' (email do usuário) são obrigatórios"}), 400

    ponto = Ponto.query.get(ponto_id)
    if not ponto:
        return jsonify({"erro": "Ponto não encontrado"}), 404

    if ponto.autor.email != email_usuario:
        return jsonify({"erro": "Acesso negado. O ponto não pertence a este usuário."}), 403

    db.session.delete(ponto)
    db.session.commit()
    
    return jsonify({"mensagem": "Ponto removido com sucesso"}), 200