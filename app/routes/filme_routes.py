from flask import Blueprint, jsonify, request
from app.schemas.filme_schema import filme_schema, filmes_schema
from app.services import filme_service

filme_bp = Blueprint("filmes", __name__)


@filme_bp.get("")
def listar_filmes():
    filmes = filme_service.listar()
    return jsonify(filmes_schema.dump(filmes)), 200


@filme_bp.get("/<int:filme_id>")
def obter_filme(filme_id: int):
    filme = filme_service.obter(filme_id)
    return jsonify(filme_schema.dump(filme)), 200


@filme_bp.post("")
def criar_filme():
    dados = filme_schema.load(request.get_json())
    filme = filme_service.criar(dados)
    return jsonify(filme_schema.dump(filme)), 201


@filme_bp.put("/<int:filme_id>")
def substituir_filme(filme_id: int):
    dados = filme_schema.load(request.get_json(), partial=False)
    filme = filme_service.atualizar(filme_id, dados)
    return jsonify(filme_schema.dump(filme)), 200


@filme_bp.patch("/<int:filme_id>")
def atualizar_filme(filme_id: int):
    dados = filme_schema.load(request.get_json(), partial=True)
    filme = filme_service.atualizar(filme_id, dados)
    return jsonify(filme_schema.dump(filme)), 200


@filme_bp.delete("/<int:filme_id>")
def remover_filme(filme_id: int):
    filme_service.remover(filme_id)
    return "", 204


@filme_bp.post("/<int:filme_id>/alugar")
def alugar_filme(filme_id: int):
    filme = filme_service.alugar(filme_id)
    return jsonify(filme_schema.dump(filme)), 200


@filme_bp.post("/<int:filme_id>/devolver")
def devolver_filme(filme_id: int):
    filme = filme_service.devolver(filme_id)
    return jsonify(filme_schema.dump(filme)), 200
