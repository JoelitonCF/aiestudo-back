from marshmallow import Schema, fields, validate


class QuizStartSchema(Schema):
    usuario_id = fields.String(required=True, validate=validate.Length(
        min=1), description="ID do usuário")
    disciplina = fields.String(required=True, validate=validate.Length(
        min=1), description="Disciplina do quiz")
    subtopico = fields.String(description="Subtópico específico")
    num_questoes = fields.Integer(validate=validate.Range(
        min=1, max=20), description="Número de questões")
    nivel = fields.String(validate=validate.OneOf(
        ["basico", "intermediario", "avancado"]), description="Nível de dificuldade")


class QuizFinishSchema(Schema):
    respostas = fields.Dict(
        required=True, description="Respostas do usuário (chave: índice da questão, valor: resposta)")
