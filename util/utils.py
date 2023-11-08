def validate_schema(body, Schema):
    schema = Schema()
    result = schema.validate(body)
    return result
