from marshmallow import Schema, fields, validate

not_blank = validate.Length(min=1, error="Field cannot be blank")


class CreateChat(Schema):
    url_pdf = fields.String(required=False, validate=not_blank)
    question = fields.String(required=True, validate=not_blank)
class CreateResume(Schema):
    url_pdf = fields.String(required=False, validate=not_blank)
