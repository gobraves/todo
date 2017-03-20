from flask import jsonify, request, g
from . import api
from ..models import Task
from .. import db
from .errors import forbidden


@api.route('/tasks/', methods=['POST'])
def add_task():
    """
    add task
    """

    task = Task.from_json(request.json)
    if task.username != g.current_user:
        db.session.add(task)
        db.commit()
    return jsonify(task.to_json), 201


@api.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    delete task
    """
    task = Task.query.get_or_404(task_id)
    if g.current_user != task.username:
        return forbidden("Insufficient permissions")
    db.session.delete(task)
    db.session.commit()
    return 201


@api.route('/tasks/<int:id>', methods=['PUT'])
def update_task(task_id):
    """
    modify task
    """
    task = Task.query.get_or_404(task_id)
    if g.current_user != task.username:
        return forbidden("Insufficient permissions")
    task.title = request.json.get('title')
    db.session.add(task)
    return jsonify(task.to_json())





