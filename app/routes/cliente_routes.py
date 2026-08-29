from flask import Blueprint, jsonify, request

from app.schemas.cliente_schema import cliente_schema, clientes_schema
from app.services import cliente_service


cliente_bp = Blueprint("clientes", __name__)


@cliente_bp.get("")
def listar_clientes():
    clientes = cliente_service.listar()
    return jsonify(clientes_schema.dump(clientes)), 200


@cliente_bp.get("/<int:cliente_id>")
def obter_cliente(cliente_id: int):
    cliente = cliente_service.obter(cliente_id)
    return jsonify(cliente_schema.dump(cliente)), 200


@cliente_bp.post("")
def criar_cliente():
    dados = cliente_schema.load(request.get_json())
    cliente = cliente_service.criar(dados)
    return jsonify(cliente_schema.dump(cliente)), 201


@cliente_bp.put("/<int:cliente_id>")
def substituir_cliente(cliente_id: int):
    dados = cliente_schema.load(request.get_json(), partial=False)
    cliente = cliente_service.atualizar(cliente_id, dados)
    return jsonify(cliente_schema.dump(cliente)), 200


@cliente_bp.patch("/<int:cliente_id>")
def atualizar_cliente(cliente_id: int):
    dados = cliente_schema.load(request.get_json(), partial=True)
    cliente = cliente_service.atualizar(cliente_id, dados)
    return jsonify(cliente_schema.dump(cliente)), 200


@cliente_bp.delete("/<int:cliente_id>")
def remover_cliente(cliente_id: int):
    cliente_service.remover(cliente_id)
    return jsonify({"message": "Cliente removido com sucesso."}), 200