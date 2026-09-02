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
    valor = fields.Decimal(as_string=True, required=True, validate=validate.Range(min=0))
    status = fields.String(dump_only=True)
    cliente_nome = fields.Method("get_cliente_nome", dump_only=True)
    filme_titulo = fields.Method("get_filme_titulo", dump_only=True)

    def get_cliente_nome(self, obj):
        return obj.cliente.nome

    def get_filme_titulo(self, obj):
        return obj.filme.titulo

locacao_schema = LocacaoSchema()
locacoes_schema = LocacaoSchema(many=True)