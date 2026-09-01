from marshmallow import fields, validate
from app.extensions import ma
from app.models.categoria import Categoria


class CategoriaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Categoria
        load_instance = False

    id = fields.Integer(dump_only=True)

    nome = fields.String(required=True, validate=validate.Length(min=2, max=100))


categoria_schema = CategoriaSchema()
categorias_schema = CategoriaSchema(many=True)