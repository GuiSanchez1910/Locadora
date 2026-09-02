from flask import Blueprint, jsonify, request
from app.schemas.locacao_schema import locacao_schema, locacoes_schema
from app.services import locacao_service

locacao_bp = Blueprint("locacoes", __name__)


@locacao_bp.get("")
def listar_locacoes():
    locacoes = locacao_service.listar()
    return jsonify(locacoes_schema.dump(locacoes)), 200

@locacao_bp.get("/<int:locacao_id>")
def obter_locacao(locacao_id: int):
    locacao = locacao_service.obter(locacao_id)
    return jsonify(locacao_schema.dump(locacao)), 200

@locacao_bp.post("")
def criar_locacao():
    dados = locacao_schema.load(request.get_json())
    locacao = locacao_service.criar(dados)
    return jsonify(locacao_schema.dump(locacao)), 201

@locacao_bp.put("/<int:locacao_id>")
def substituir_locacao(locacao_id: int):
    dados = locacao_schema.load(request.get_json(), partial=False)
    locacao = locacao_service.atualizar(locacao_id, dados)
    return jsonify(locacao_schema.dump(locacao)), 200

@locacao_bp.patch("/<int:locacao_id>")
def atualizar_locacao(locacao_id: int):
    dados = locacao_schema.load(request.get_json(), partial=True)
    locacao = locacao_service.atualizar(locacao_id, dados)
    return jsonify(locacao_schema.dump(locacao)), 200

@locacao_bp.delete("/<int:locacao_id>")
def remover_locacao(locacao_id: int):
    locacao_service.remover(locacao_id)
    return "", 204

@locacao_bp.post("/<int:locacao_id>/devolver")
def devolver_locacao(locacao_id: int):
    locacao = locacao_service.devolver(locacao_id)
    return jsonify(locacao_schema.dump(locacao)), 200