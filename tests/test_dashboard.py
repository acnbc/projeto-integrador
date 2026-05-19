def test_dashboard_stats_coordenador(client, admin_headers):
    response = client.get("/api/dashboard/stats", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert "tempo_medio_resposta_dias" in data
    assert "total_pareceres_com_resposta" in data
    assert "distribuicao_por_setor" in data
    assert isinstance(data["distribuicao_por_setor"], list)


def test_dashboard_stats_aluno_negado(client, aluno_headers):
    response = client.get("/api/dashboard/stats", headers=aluno_headers)
    assert response.status_code == 403
