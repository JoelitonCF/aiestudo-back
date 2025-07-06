# flask_backend/schemas/flashcard_review_schema.py
from marshmallow import Schema, fields


class FlashcardReviewSchema(Schema):
    acerto = fields.Bool(required=True)

# flask_backend/schemas/simple_ok_schema.py


class SimpleOkSchema(Schema):
    ok = fields.Bool()
