from marshmallow import Schema, fields


class IdSchema(Schema):
    id = fields.Str()
