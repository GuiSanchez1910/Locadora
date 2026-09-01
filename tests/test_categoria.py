"""Testes de Categoria.

Os primeiros exercitam a API de ponta a ponta; os dois últimos chamam o service
direto, sem HTTP — que é justamente o que a separação em camadas compra.
"""

import pytest

from app.errors import RecursoNaoEncontrado, RegraDeNegocio
from app.services import categoria_service


def test_listar_vazio(client):
    resposta = client.get("/api/categorias")
    assert resposta.status_code == 200
    assert resposta.get_json() == []


def test_criar_categoria(client):
    resposta = client.post("/api/categorias", json={"nome": "Ação"})
    assert resposta.status_code == 201
    corpo = resposta.get_json()
    assert corpo["nome"] == "Ação"
    assert "id" in corpo


def test_criar_categoria_com_nome_curto_devolve_422(client):
    resposta = client.post("/api/categorias", json={"nome": "X"})
    assert resposta.status_code == 422
    assert "nome" in resposta.get_json()["errors"]


def test_criar_categoria_sem_nome_devolve_422(client):
    resposta = client.post("/api/categorias", json={})
    assert resposta.status_code == 422


def test_nome_duplicado_devolve_409(client, categoria):
    resposta = client.post("/api/categorias", json={"nome": categoria["nome"]})
    assert resposta.status_code == 409


def test_obter_categoria_inexistente_devolve_404(client):
    resposta = client.get("/api/categorias/999")
    assert resposta.status_code == 404
    assert resposta.get_json()["code"] == 404


def test_patch_altera_apenas_o_campo_enviado(client, categoria):
    resposta = client.patch(
        f"/api/categorias/{categoria['id']}", json={"nome": "Aventura"}
    )
    assert resposta.status_code == 200
    assert resposta.get_json()["nome"] == "Aventura"


def test_put_sem_nome_devolve_422(client, categoria):
    resposta = client.put(f"/api/categorias/{categoria['id']}", json={})
    assert resposta.status_code == 422


def test_delete_remove_categoria(client, categoria):
    assert client.delete(f"/api/categorias/{categoria['id']}").status_code == 204
    assert client.get(f"/api/categorias/{categoria['id']}").status_code == 404


# --- Camada de serviço, sem HTTP ---------------------------------------------


def test_service_obter_inexistente_levanta_excecao_de_dominio(app):
    with pytest.raises(RecursoNaoEncontrado):
        categoria_service.obter(999)


def test_service_nome_duplicado_levanta_regra_de_negocio(app):
    categoria_service.criar({"nome": "Drama"})
    with pytest.raises(RegraDeNegocio):
        categoria_service.criar({"nome": "Drama"})
