from app.models.User import User
from app.models.Ponto import Ponto
from app.database import db

# Testa se a lista de usuários começa vazia
def test_listar_usuarios_vazio(test_client):
    response = test_client.get('/ListarUsuarios')
    assert response.status_code == 200
    assert response.json == []

# Testa a criação de um novo usuário
def test_adicionar_usuario(test_client):
    response = test_client.post('/AdicionarUsuario?email=teste@email.com&senha=123')
    assert response.status_code == 201
    assert response.json['email'] == 'teste@email.com'
    assert 'senha' in response.json # Verifica se a chave 'senha' existe

# Testa se a criação de um usuário duplicado é bloqueada
def test_adicionar_usuario_duplicado(test_client):
    test_client.post('/AdicionarUsuario?email=unico@email.com&senha=123')
    response = test_client.post('/AdicionarUsuario?email=unico@email.com&senha=123')
    assert response.status_code == 409
    assert "Usuário com este email já existe" in response.json['erro']

# Testa a listagem de usuários após a criação
def test_listar_usuarios_com_um_usuario(test_client):
    test_client.post('/AdicionarUsuario?email=teste@email.com&senha=123')
    response = test_client.get('/ListarUsuarios')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['email'] == 'teste@email.com'

# Testa a criação de um ponto, validando a autenticação
def test_adicionar_ponto(test_client):
    test_client.post('/AdicionarUsuario?email=dono.ponto@email.com&senha=abc')
    response = test_client.post('/AdicionarPonto?email=dono.ponto@email.com&senha=abc&latitude=-20&longitude=-45&descricao=Meu Ponto')
    assert response.status_code == 201
    assert response.json['mensagem'] == 'Ponto adicionado com sucesso'
    assert response.json['ponto_criado']['descricao'] == 'Meu Ponto'
    assert response.json['usuario_proprietario']['email'] == 'dono.ponto@email.com'

# Testa a falha ao criar ponto com senha errada
def test_adicionar_ponto_com_senha_errada(test_client):
    test_client.post('/AdicionarUsuario?email=dono.ponto@email.com&senha=abc')
    response = test_client.post('/AdicionarPonto?email=dono.ponto@email.com&senha=senha-errada&latitude=-20&longitude=-45&descricao=Ponto Falho')
    assert response.status_code == 403 # Forbidden
    assert response.json['erro'] == 'Senha incorreta'

# Testa a listagem de todos os pontos
def test_listar_todos_os_pontos(test_client):
    test_client.post('/AdicionarUsuario?email=dono1@email.com&senha=abc')
    test_client.post('/AdicionarUsuario?email=dono2@email.com&senha=def')
    test_client.post('/AdicionarPonto?email=dono1@email.com&senha=abc&latitude=1&longitude=1&descricao=Ponto A')
    test_client.post('/AdicionarPonto?email=dono2@email.com&senha=def&latitude=2&longitude=2&descricao=Ponto B')

    response = test_client.get('/ListarTodosPontos')
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]['descricao'] == 'Ponto A'
    assert response.json[1]['autor']['email'] == 'dono2@email.com'

# Testa a alteração de um usuário
def test_alterar_usuario_sucesso(test_client):
    test_client.post('/AdicionarUsuario?email=original@email.com&senha=123')
    response = test_client.post('/AlterarUsuario?email_atual=original@email.com&senha_atual=123&novo_email=novo@email.com')
    assert response.status_code == 200
    assert response.json['alteracoes']['email']['novo'] == 'novo@email.com'

# Testa a remoção de um usuário
def test_remover_usuario_sucesso(test_client):
    res_user = test_client.post('/AdicionarUsuario?email=usuario.a.remover@email.com&senha=123')
    user_id = res_user.json['id']

    response = test_client.post(f'/RemoverUsuario?id={user_id}')
    assert response.status_code == 200
    assert response.json['usuario_removido']['id'] == user_id