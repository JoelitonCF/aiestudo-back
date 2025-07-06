# flask_backend/schemas/simple_ok_schema.py
from marshmallow import Schema, fields


class SimpleOkSchema(Schema):
    ok = fields.Bool(required=True)
