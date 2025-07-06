from marshmallow import Schema, fields, validate


class CurriculoSchema(Schema):
    concurso = fields.Str(required=True)
    cargo = fields.Str(required=True)
    # Se você tiver outros campos obrigatórios no body, adicione aqui...
