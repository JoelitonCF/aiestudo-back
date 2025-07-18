from marshmallow import Schema, fields, validate


class PlanoSchema(Schema):
    usuario_id = fields.String(required=True, validate=validate.Length(
        min=1), description="ID do usuário")
    concurso = fields.String(required=True, validate=validate.Length(
        min=1), description="Nome do concurso")
    cargo = fields.String(required=True, validate=validate.Length(
        min=1), description="Cargo pretendido")
    tempo_disponivel = fields.Integer(validate=validate.Range(
        min=1, max=24), description="Horas disponíveis por dia")
    data_prova = fields.String(description="Data da prova (YYYY-MM-DD)")
    disciplinas_foco = fields.List(
        fields.String(), description="Lista de disciplinas prioritárias")
