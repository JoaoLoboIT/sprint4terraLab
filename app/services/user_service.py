from ..models.User import User
from ..database import db

def criar_usuario(email, senha):
    if User.query.filter_by(email=email).first():
        raise ValueError("Usuário com este email já existe")
    
    novo_usuario = User(email=email, senha=senha)
    db.session.add(novo_usuario)
    db.session.commit()
    return novo_usuario

def listar_usuarios():
    return User.query.all()

def alterar_usuario(email_atual, senha_atual, novo_email=None, nova_senha=None):
    if not email_atual or not senha_atual:
        raise ValueError("Email e senha atual são obrigatórios para fazer alterações.")
        
    usuario = User.query.filter_by(email=email_atual).first()

    if not usuario:
        raise ValueError("Usuário não encontrado")
    if usuario.senha != senha_atual:
        raise PermissionError("Senha atual incorreta.")

    mudancas = {}

    if novo_email and novo_email != usuario.email:
        mudancas['email'] = {'antigo': usuario.email, 'novo': novo_email}
        usuario.email = novo_email

    if nova_senha:
        mudancas['senha'] = {'antiga': usuario.senha, 'nova': nova_senha}
        usuario.senha = nova_senha
    
    if mudancas:
        db.session.commit()
    
    return mudancas

def remover_usuario(user_id=None, email=None):
    if not user_id and not email:
        raise ValueError("É necessário fornecer um ID ou um email para remover o usuário.")

    usuario = None
    if user_id:
        usuario = User.query.get(user_id)
    elif email:
        usuario = User.query.filter_by(email=email).first()

    if not usuario:
        raise ValueError("Usuário não encontrado")

    dados_do_usuario_removido = usuario.to_dict()

    db.session.delete(usuario)
    db.session.commit()

    return dados_do_usuario_removido