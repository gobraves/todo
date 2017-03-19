from flask import jsonify
from . import api
from ..models import User


@api.route('/')
def root():
    """
    设置根路由
    """

    return api.send_static_file('index.html')


@api.route('/users/<int:id>')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_json())


@api.route('/users/<int:id>/tasks', methods=['GET'])
def get_tasks(user_id):
    """
    GET方法api
    """
    user = User.query.get_or_404(user_id)
    tasks = user.tasks
    return jsonify({
        'tasks': [task.to_json() for task in tasks]
    })



