def test_listar_tipos_alta(client, admin_headers):
    response = client.get("/api/tipo-alta", headers=admin_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_criar_tipo_alta(client, admin_headers):
    payload = {"alta": "Alta programada (teste)"}
    response = client.post("/api/tipo-alta", json=payload, headers=admin_headers)
    assert response.status_code == 201
    assert response.json()["alta"] == payload["alta"]
