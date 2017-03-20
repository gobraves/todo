from flask import g, jsonify, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_httpauth import HTTPBasicAuth
from .errors import unauthorized, forbidden
from . import api
from ..models import User

auth = HTTPBasicAuth()


@auth.verify_password()
def verify_password(username_or_token, password):
    if username_or_token == '':
        return False;
    if password == '':
        g.current_user = User.verify_auth_token(username_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(username_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@api.before_request
@auth.login_required()
def before_request():
    url = request.url
    if url == "/users":
        return "log in"
    token = request.headers['Authorization']

    if not token:
        return forbidden("Unconfirmed account")
    s = Serializer(api.config['SECRET_KEY'])
    data = s.load(token)
    user = User.query.filter_by(data.get('id'))
    if not user:
        return forbidden("Unconfirmed account")
    g.current_user = user
    g.token_used = True


@api.route('/token')
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration': 3600})