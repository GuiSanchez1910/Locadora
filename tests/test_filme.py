"""Testes de Filme."""

import pytest

from app.errors import RecursoNaoEncontrado, ReferenciaInvalida, RegraDeNegocio
from app.services import filme_service


def test_criar_filme(client, categoria):
    resposta = client.post(
        "/api/filmes",
        json={
            "titulo": "Matrix",
            "descricao": "Ficção científica",
            "ano": 1999,
            "duracao": 136,
            "estoque": 5,
            "categoria_id": categoria["id"],
        },
    )
    assert resposta.status_code == 201
    corpo = resposta.get_json()
    assert corpo["titulo"] == "Matrix"
    assert corpo["estoque"] == 5
    assert corpo["disponivel"] is True
    assert corpo["categoria_id"] == categoria["id"]


def test_estoque_ausente_assume_zero(client, categoria):
    resposta = client.post(
        "/api/filmes",
        json={"titulo": "Blade Runner", "categoria_id": categoria["id"]},
    )
    assert resposta.status_code == 201
    corpo = resposta.get_json()
    assert corpo["estoque"] == 0
    assert corpo["disponivel"] is False


def test_criar_filme_sem_titulo_devolve_422(client, categoria):
    resposta = client.post(
        "/api/filmes",
        json={"estoque": 1, "categoria_id": categoria["id"]},
    )
    assert resposta.status_code == 422
    assert "titulo" in resposta.get_json()["errors"]


def test_estoque_negativo_devolve_422(client, categoria):
    resposta = client.post(
        "/api/filmes",
        json={
            "titulo": "Matrix",
            "estoque": -1,
            "categoria_id": categoria["id"],
        },
    )
    assert resposta.status_code == 422
    assert "estoque" in resposta.get_json()["errors"]


def test_categoria_inexistente_devolve_422(client):
    resposta = client.post(
        "/api/filmes",
        json={"titulo": "Matrix", "estoque": 1, "categoria_id": 999},
    )
    assert resposta.status_code == 422
    assert "999" in resposta.get_json()["description"]


def test_patch_preserva_os_campos_nao_enviados(client, filme):
    resposta = client.patch(f"/api/filmes/{filme['id']}", json={"ano": 2015})
    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert corpo["ano"] == 2015
    assert corpo["titulo"] == "Interestelar"
    assert corpo["estoque"] == 3
    assert corpo["disponivel"] is True


def test_put_sem_estoque_zera_o_estoque(client, filme):
    resposta = client.put(
        f"/api/filmes/{filme['id']}",
        json={
            "titulo": "Interestelar",
            "categoria_id": filme["categoria_id"],
        },
    )
    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert corpo["estoque"] == 0
    assert corpo["disponivel"] is False


def test_mover_para_categoria_inexistente_nao_altera_o_filme(client, filme):
    resposta = client.patch(
        f"/api/filmes/{filme['id']}", json={"categoria_id": 999}
    )
    assert resposta.status_code == 422
    atual = client.get(f"/api/filmes/{filme['id']}").get_json()
    assert atual["categoria_id"] == filme["categoria_id"]


def test_delete_filme(client, filme):
    assert client.delete(f"/api/filmes/{filme['id']}").status_code == 204
    assert client.get(f"/api/filmes/{filme['id']}").status_code == 404


def test_alugar_reduz_estoque(client, filme):
    resposta = client.post(f"/api/filmes/{filme['id']}/alugar")
    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert corpo["estoque"] == 2
    assert corpo["disponivel"] is True


def test_alugar_filme_sem_estoque_devolve_409(client, categoria):
    criado = client.post(
        "/api/filmes",
        json={"titulo": "Esgotado", "estoque": 0, "categoria_id": categoria["id"]},
    ).get_json()
    resposta = client.post(f"/api/filmes/{criado['id']}/alugar")
    assert resposta.status_code == 409


def test_devolver_aumenta_estoque(client, filme):
    client.post(f"/api/filmes/{filme['id']}/alugar")
    resposta = client.post(f"/api/filmes/{filme['id']}/devolver")
    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert corpo["estoque"] == 3
    assert corpo["disponivel"] is True


def test_alugar_ultimo_exemplar_marca_indisponivel(client, categoria):
    criado = client.post(
        "/api/filmes",
        json={"titulo": "Último", "estoque": 1, "categoria_id": categoria["id"]},
    ).get_json()
    resposta = client.post(f"/api/filmes/{criado['id']}/alugar")
    corpo = resposta.get_json()
    assert corpo["estoque"] == 0
    assert corpo["disponivel"] is False


# --- Camada de serviço, sem HTTP ---------------------------------------------


def test_service_obter_inexistente_levanta_excecao_de_dominio(app):
    with pytest.raises(RecursoNaoEncontrado):
        filme_service.obter(999)


def test_service_categoria_inexistente_levanta_referencia_invalida(app):
    with pytest.raises(ReferenciaInvalida):
        filme_service.criar({"titulo": "Matrix", "estoque": 1, "categoria_id": 999})


def test_service_alugar_indisponivel_levanta_regra_de_negocio(app, categoria):
    filme = filme_service.criar(
        {"titulo": "Esgotado", "estoque": 0, "categoria_id": categoria["id"]}
    )
    with pytest.raises(RegraDeNegocio):
        filme_service.alugar(filme.id)
