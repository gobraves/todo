from flask import jsonify, make_response, request, abort
from . import api
from ..models import User, Task

@api.route('/')
def root():
    """
    设置根路由
    """

    return app.send_static_file('index.html')

@api.route('/users/<int:id>')
def get_user(id)
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())

@api.route('/users/<int:id>/tasks', methods=['GET'])
def getTasks(id):
    """
    GET方法api
    """
    user = User.query.get_or_404(id)
    tasks = user.tasks
    return jsonify({
        'tasks': [task.to_json() for task in tasks]
    })



