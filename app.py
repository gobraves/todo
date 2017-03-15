from flask import Flask, jsonify, make_response, request, abort

# 静态文件的放置路径，可根据实际情况设置，这里设置为默认路径：'./static/'
app = Flask(__name__, static_url_path='')

#模拟json数据
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.route('/')
def root():
    """
    设置根路由
    """

    return app.send_static_file('index.html')


@app.route('/tasks', methods=['GET'])
def getTasks():
    """
    GET方法api
    """
    return jsonify({'tasks': tasks})


@app.route('/addTask', methods=['POST'])
def add_task():
    """
    POST方法API，添加数据项
    """

    if request.json['title'] == "":
        abort(400)
    task = {
        'id' : tasks[len(tasks) - 1]['id'] + 1,
        'title': request.json['title'],
        'description' : request.json.get('description', ''),
        'done' : False
    }
    tasks.append(task)
    return jsonify({'tasks': tasks}), 201


@app.route('/deleteTask/<index>', methods=['DELETE'])
def delete_task(index):
    """
    POST方法API，删除数据项
    """

    task_id = index
    for task in tasks:
        if task['id'] == int(task_id):
            tasks.remove(task)

    return jsonify({'tasks': tasks}), 201


@app.route('/task', methods=['GET', 'PUT'])
def update_task():
    """
    更新数据项
    """
    task_id = request.json['id']
    for task in tasks:
        if task['id'] == task_id:
            task = update_task


@app.errorhandler(404)
def not_found():
    """
    404
    """
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)

