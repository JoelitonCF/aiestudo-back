from marshmallow import Schema, fields


class QuizStartSchema(Schema):
    usuario_id = fields.Str(required=True)
    questoes = fields.List(fields.Dict(), required=True)


class QuizFinishSchema(Schema):
    respostas = fields.Dict(required=True)
