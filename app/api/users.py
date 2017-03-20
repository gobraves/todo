from flask import jsonify, request
from . import api
from ..models import User
from .authentication import verify_password
from .errors import forbidden

@api.route('/')
def root():
    """
    set route
    """

    return api.send_static_file('index.html')


@api.route('/users', methods=['POST'])
def log_in():
    username = request.json.get("username")
    passwd = request.json.get("password")
    if not verify_password(username_or_token=username, password=passwd):
        return forbidden("Unconfirmed account")
    user = User.query.get_or_404(username)
    return jsonify(user.to_json())


@api.route('/users/<int:id>')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_json())


@api.route('/users/<int:id>/tasks', methods=['GET'])
def get_tasks(user_id):
    """
    get tasks
    """
    user = User.query.get_or_404(user_id)
    tasks = user.tasks
    return jsonify({
        'tasks': [task.to_json() for task in tasks]
    })



