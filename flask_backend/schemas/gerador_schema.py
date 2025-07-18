from marshmallow import Schema, fields, validate


class GeradorSchema(Schema):
    tipo = fields.String(
        required=True,
        validate=validate.OneOf(
            ["resumo", "questoes", "plano_aula", "exercicios"]),
        description="Tipo de conteúdo a ser gerado"
    )
    disciplina = fields.String(
        required=True,
        validate=validate.Length(min=1),
        description="Disciplina do conteúdo"
    )
    topico = fields.String(
        required=True,
        validate=validate.Length(min=1),
        description="Tópico específico"
    )
    nivel = fields.String(
        validate=validate.OneOf(["basico", "intermediario", "avancado"]),
        description="Nível de dificuldade"
    )
    formato = fields.String(
        validate=validate.OneOf(["texto", "markdown", "html"]),
        description="Formato de saída"
    )
    num_questoes = fields.Integer(
        validate=validate.Range(min=1, max=20),
        description="Número de questões (para tipo 'questoes')"
    )
