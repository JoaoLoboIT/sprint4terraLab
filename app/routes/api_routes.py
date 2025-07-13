from flask import Blueprint, request, jsonify
from ..services import user_service, ponto_service

api = Blueprint('api', __name__)

# Adiciona um novo usuário
@api.route('/AdicionarUsuario', methods=['POST'])
def adicionar_usuario_api():
    try:
        email = request.args.get('email')
        senha = request.args.get('senha') 
        usuario = user_service.criar_usuario(email, senha)
        return jsonify(usuario.to_dict()), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 409

# Lista todos os usuários
@api.route('/ListarUsuarios', methods=['GET'])
def listar_usuarios_api():
    usuarios = user_service.listar_usuarios()
    return jsonify([u.to_dict() for u in usuarios]), 200

# Altera um usuário
@api.route('/AlterarUsuario', methods=['POST'])
def alterar_usuario_api():
    try:
        email_atual = request.args.get('email_atual')
        senha_atual = request.args.get('senha_atual')
        novo_email = request.args.get('novo_email')
        nova_senha = request.args.get('nova_senha')
        
        alteracoes_feitas = user_service.alterar_usuario(
            email_atual=email_atual,
            senha_atual=senha_atual,
            novo_email=novo_email,
            nova_senha=nova_senha
        )
        
        if alteracoes_feitas:
            return jsonify({
                "mensagem": "Usuário atualizado com sucesso",
                "alteracoes": alteracoes_feitas
            }), 200
        else:
            return jsonify({"mensagem": "Nenhum dado novo foi fornecido para alteração."}), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
    except PermissionError as e:
        return jsonify({"erro": str(e)}), 403

# Remove um usuário
@api.route('/RemoverUsuario', methods=['POST'])
def remover_usuario_api():
    try:
        user_id = request.args.get('id')
        email = request.args.get('email')
        
        usuario_removido_info = user_service.remover_usuario(user_id=user_id, email=email)
        
        return jsonify({
            "mensagem": "Usuário removido com sucesso",
            "usuario_removido": usuario_removido_info
        }), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404

# Adiciona um novo ponto
@api.route('/AdicionarPonto', methods=['POST'])
def adicionar_ponto_api():
    try:
        email = request.args.get('email')
        senha = request.args.get('senha')
        lat = request.args.get('latitude')
        lon = request.args.get('longitude')
        desc = request.args.get('descricao', "")
        
        novo_ponto, usuario_do_ponto = ponto_service.criar_ponto(email, senha, lat, lon, desc)
        
        return jsonify({
            "mensagem": "Ponto adicionado com sucesso",
            "ponto_criado": novo_ponto.to_dict(),
            "usuario_proprietario": usuario_do_ponto.to_dict()
        }), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
    except PermissionError as e:
        return jsonify({"erro": str(e)}), 403

# Lista os pontos de um usuário
@api.route('/ListarPontos', methods=['GET'])
def listar_pontos_api():
    try:
        email = request.args.get('email')
        pontos = ponto_service.listar_pontos_de_usuario(email)
        return jsonify([{"id": p.id, "latitude": p.latitude, "longitude": p.longitude, "descricao": p.descricao} for p in pontos]), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404

# Altera um ponto
@api.route('/AlterarPonto', methods=['POST'])
def alterar_ponto_api():
    try:
        ponto_id = request.args.get('id')
        email_usuario = request.args.get('user')
        novos_dados = {
            'latitude': request.args.get('latitude'),
            'longitude': request.args.get('longitude'),
            'descricao': request.args.get('descricao')
        }
        # Filtra para não enviar chaves com valor None
        novos_dados = {k: v for k, v in novos_dados.items() if v is not None}
        ponto_service.alterar_ponto(ponto_id, email_usuario, novos_dados)
        return jsonify({"mensagem": "Ponto atualizado com sucesso"}), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
    except PermissionError as e:
        return jsonify({"erro": str(e)}), 403

# Remove um ponto
@api.route('/RemoverPonto', methods=['POST'])
def remover_ponto_api():
    try:
        ponto_id = request.args.get('id')
        email_usuario = request.args.get('user')
        ponto_service.remover_ponto(ponto_id, email_usuario)
        return jsonify({"mensagem": "Ponto removido com sucesso"}), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
    except PermissionError as e:
        return jsonify({"erro": str(e)}), 403