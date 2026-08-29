from marshmallow import fields, validate

from app.extensions import ma
from app.models.cliente import Cliente

class ClienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente
        load_instance = False

    id = fields.Integer(dump_only=True)
    nome = fields.String(required=True, validate=validate.Length(min=2, max=100))
    cpf = fields.String(required=True, validate=validate.Length(min=11, max=11))
    email = fields.Email(required=True)
    telefone = fields.String(required=True, validate=validate.Length(min=8, max=20))

cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)