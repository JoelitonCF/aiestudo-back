from marshmallow import Schema, fields


class PlanoSchema(Schema):
    concurso = fields.Str(required=True)
    cargo = fields.Str(required=True)
    dias = fields.Int(load_default=30, validate=lambda n: n > 0)
