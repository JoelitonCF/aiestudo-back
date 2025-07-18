from marshmallow import Schema, fields, validate


class DesafioSchema(Schema):
    usuario = fields.String(description="Nome do usuário")
    disciplina = fields.String(
        required=True,
        validate=validate.Length(min=1),
        description="Disciplina do desafio",
    )
    subtopico = fields.String(
        required=True,
        validate=validate.Length(min=1),
        description="Subtópico específico",
    )
    nivel = fields.String(
        validate=validate.OneOf(["basico", "intermediario", "avancado"]),
        description="Nível de dificuldade",
    )
