from marshmallow import fields, validate
from app.extensions import ma
from app.models.filme import Filme


class FilmeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Filme
        load_instance = False

    id = fields.Integer(dump_only=True)
    titulo = fields.String(required=True, validate=validate.Length(min=2, max=150))
    descricao = fields.String(
        load_default=None, allow_none=True, validate=validate.Length(max=500)
    )
    ano = fields.Integer(load_default=None, allow_none=True)
    duracao = fields.Integer(load_default=None, allow_none=True)
    estoque = fields.Integer(load_default=0, validate=validate.Range(min=0))
    disponivel = fields.Boolean(dump_only=True)
    categoria_id = fields.Integer(required=True)


filme_schema = FilmeSchema()
filmes_schema = FilmeSchema(many=True)
