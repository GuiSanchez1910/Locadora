from flask import Blueprint, jsonify, request
from app.schemas.locacao_schema import locacao_schema, locacoes_schema
from app.services import locacao_service

locacao_bp = Blueprint("locacoes", __name__)


@locacao_bp.get("")
def listar_locacoes():
    filmes = locacao_service.listar()
    return jsonify(locacao_schema.dump(locacoes)), 200