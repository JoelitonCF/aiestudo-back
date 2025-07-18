from marshmallow import Schema, fields, validate


class UserCreateSchema(Schema):
    user_id = fields.Str(required=True)
    nome = fields.Str(required=True)


class UserSchema(Schema):
    nome = fields.String(required=True, validate=validate.Length(
        min=2, max=100), description="Nome completo do usuário")
    email = fields.Email(required=True, description="Email do usuário")
    concurso_foco = fields.String(description="Concurso de foco do usuário")
    cargo_foco = fields.String(description="Cargo de foco do usuário")


class UserActivitySchema(Schema):
    tipo = fields.String(required=True, validate=validate.OneOf(
        ["estudo", "quiz", "flashcard", "desafio"]), description="Tipo de atividade")
    dados = fields.Dict(
        required=True, description="Dados específicos da atividade")
    duracao = fields.Integer(validate=validate.Range(
        min=1), description="Duração da atividade em minutos")
