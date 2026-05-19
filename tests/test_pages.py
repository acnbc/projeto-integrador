def test_pagina_login(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Entrar" in response.text or "login" in response.text.lower()


def test_raiz_redireciona_login(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "/login"
