from tests.conftest import TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD


def test_login_sucesso(client):
    response = client.post(
        "/api/usuario/token",
        data={"username": TEST_ADMIN_EMAIL, "password": TEST_ADMIN_PASSWORD},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 20


def test_login_senha_invalida(client):
    response = client.post(
        "/api/usuario/token",
        data={"username": TEST_ADMIN_EMAIL, "password": "senha-errada"},
    )
    assert response.status_code == 401


def test_me_autenticado(client, admin_headers):
    response = client.get("/api/usuario/me", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["email"] == TEST_ADMIN_EMAIL


def test_me_sem_token(client):
    response = client.get("/api/usuario/me")
    assert response.status_code == 401


def test_usuarios_requer_coordenador(client, aluno_headers):
    response = client.get("/api/usuario", headers=aluno_headers)
    assert response.status_code == 403
