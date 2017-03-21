from flask import jsonify, request, g, current_app
from . import api
from ..models import Task
from .. import db
from .errors import forbidden, bad_request

def get_tasks():
    user = g.current_user
    #user = User.query.get_or_404()
    tasks = user.tasks
    return jsonify({
        'tasks': [task.to_json() for task in tasks]
    })

def add_task():
    """
    add task
    """
    task = Task.from_json(request.json)
    if not task.title:
        return bad_request("Title required.")
    db.session.add(task)
    db.session.flush()
    task_map = task.to_json()
    db.session.commit()
    return jsonify(task_map), 201

@api.route('/tasks', methods=['GET', 'POST'])
def task():
    if request.method == 'GET':
        return get_tasks()
    else:
        return add_task()

@api.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    delete task
    """
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"status": "ok"}), 201

@api.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify(task.to_json())

@api.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    """
    modify task
    """
    task = Task.query.get_or_404(id)
    t = Task.from_json(request.json)
    task.title = t.title
    task.done = t.done
    db.session.add(task)
    db.session.commit()
    current_app.logger.warning(task.to_json())
    return jsonify(task.to_json())
