from marshmallow import Schema, fields
from .curriculo_list_item_schema import CurriculoItemSchema


class CurriculoListSchema(Schema):
    items = fields.List(fields.Nested(CurriculoItemSchema), required=True)
    nextPageToken = fields.Str(allow_none=True)
