from marshmallow import Schema, fields


class DesafioSchema(Schema):
    usuario = fields.Str(load_default="Aluno")
    disciplina = fields.Str(required=True)
    subtopico = fields.Str(required=True)
    nivel = fields.Str(load_default="TJ-PA")
