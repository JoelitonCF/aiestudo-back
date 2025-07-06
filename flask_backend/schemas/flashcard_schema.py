from marshmallow import Schema, fields, validate


class FlashcardSchema(Schema):
    usuario_id = fields.Str(required=True)
    disciplina = fields.Str(required=True)
    topico = fields.Str(required=True)
    subtopico = fields.Str(required=True)
    pergunta = fields.Str(required=True, validate=validate.Length(min=1))
    resposta = fields.Str(required=True)
