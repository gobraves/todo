from flask import g, jsonify, request, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from .errors import unauthorized, forbidden
from . import api
from ..models import User

@api.before_request
def before_request():
    path = request.path
    print(path)
    # bypass token url path
    if not (path.startswith(api.url_prefix)
            and not path.startswith(
                url_for("%s.%s" % (api.name, "get_token")))):
        return None
    token = request.headers['Authorization']
    if not token:
        return forbidden("Request without a token")
    user = User.verify_auth_token(token)
    if not user:
        return forbidden("Unconfirmed account" + path)

    g.current_user = user
    g.token_used = True


@api.route('/token', methods=['POST'])
def get_token():
    username = request.json["username"]
    password = request.json["password"]
    user = User.query.filter_by(username=username).first()
    if not user:
        return unauthorized('User ' + username + ' doesn\'t exist.')
    if not user.verify_password(password):
        return unauthorized('Invalid credentials')
    # return user and token as json
    userData = {
        "id": user.id,
        "username": user.username,
        "token": user.generate_auth_token().decode()
    }
    return jsonify(userData)
