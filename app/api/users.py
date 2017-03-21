from flask import jsonify, request
from . import api
from ..models import User
from .errors import forbidden


@api.route('/users')
@api.route('/users/<int:id>')
def get_user(user_id):
    if not user_id:
        user_id = g.current_user.id
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
