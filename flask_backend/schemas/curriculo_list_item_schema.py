# flask_backend/schemas/curriculo_list_item_schema.py
from marshmallow import Schema, fields


class CurriculoItemSchema(Schema):
    id = fields.Str(required=True)
    concurso = fields.Str(required=True)
    cargo = fields.Str(required=True)
