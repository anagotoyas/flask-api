from util.utils import validate_schema
from functools import wraps
from flask import jsonify


def request_validator(request, schema):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            result = validate_schema(request.json, schema)
            if result:
                return jsonify({"msg": str(result)}), 400
            return f(*args, **kwargs)

        return decorated_function

    return decorator

def jwt_auth(request):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print(request.headers)
            return f(*args, **kwargs)

        return decorated_function

    return decorator