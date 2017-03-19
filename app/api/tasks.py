from flask import jsonify, make_response, request, abort
from . import api
from ..models import User, Task

@api.route('/tasks/', methods=['POST'])
def add_task():
    """
    POST方法API，添加数据项
    """

    task =task.from_json(request.json)
    task.username = g.current_user
    db.session.add(task)
    db.commit()
    return jsonify(task.to_json), 201


@api.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(index):
    """
    POST方法API，删除数据项
    """
    

    task_id = index
    for task in tasks:
        if task['id'] == int(task_id):
            tasks.remove(task)

    return jsonify({'tasks': tasks}), 201


@api.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    """
    修改数据项
    """
    task = Task.query.get_or_404(id)
    if g.current_user != task.username:
        return forbidden("Insufficient permissions")
    task.title = request.json.get('title')
    db.session.add(task)
    return jsonify(task.to_json())

@app.errorhandler(404)
def not_found():
    """
    404
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


