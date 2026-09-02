from marshmallow import fields, validate
from app.extensions import ma
from app.models.locacao import Locacao

class LocacaoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Locacao
        load_instance = False

    id = fields.Integer(dump_only=True)
    cliente_id = fields.Integer(required=True)
    filme_id = fields.Integer(required=True)
    data_locacao = fields.DateTime(dump_only=True)
    data_devolucao_prevista = fields.DateTime(required=True)
    data_devolucao = fields.DateTime(allow_none=True)
    valor = fields.Decimal(as_string=True, dump_only=True)
    status = fields.Boolean(dump_only=True)

locacao_schema = LocacaoSchema()
locacoes_schema = LocacaoSchema(many=True)