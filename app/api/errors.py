from flask import jsonify
from flask import make_response

from app.exceptions import ValidationError
from . import api


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


@api.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
