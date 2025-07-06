from marshmallow import Schema, fields


class UserCreateSchema(Schema):
    user_id = fields.Str(required=True)
    nome = fields.Str(required=True)


class UserActivitySchema(Schema):
    xp = fields.Int(required=True)
