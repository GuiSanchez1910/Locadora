"""Fixtures compartilhadas.

Esta é a justificativa prática da Application Factory: `create_app("testing")`
sobe uma instância isolada, com banco em memória, a cada teste. Sem a factory,
o `app` seria um singleton de módulo e um teste contaminaria o outro.

As fixtures de dados devolvem o JSON da API, não instâncias do ORM. Isso é
proposital: o teste exercita o contrato público e não fica preso à sessão do
SQLAlchemy usada para montar o cenário.
"""

import pytest

from app import create_app
from app.extensions import db as _db


@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def categoria(client) -> dict:
    resposta = client.post("/api/categorias", json={"nome": "Ficção Científica"})
    assert resposta.status_code == 201
    return resposta.get_json()


@pytest.fixture
def filme(client, categoria) -> dict:
    resposta = client.post(
        "/api/filmes",
        json={
            "titulo": "Interestelar",
            "descricao": "Viagem espacial",
            "ano": 2014,
            "duracao": 169,
            "estoque": 3,
            "categoria_id": categoria["id"],
        },
    )
    assert resposta.status_code == 201
    return resposta.get_json()
