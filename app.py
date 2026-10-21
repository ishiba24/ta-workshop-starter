from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

ALLOWED_PRIORITIES = {"Low", "Medium", "High"}
DEFAULT_PRIORITY = "Medium"

tasks = [
    {"id": 1, "title": "Project-1 Report", "priority": DEFAULT_PRIORITY},
    {"id": 2, "title": "Project-2 MMFs", "priority": DEFAULT_PRIORITY}
]
next_id = 3


@app.route('/')
def index():
    """Render the task tracker page."""
    return render_template('index.html')


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Return all tasks with a priority value."""
    serialized_tasks = [
        {**task, "priority": task.get("priority", DEFAULT_PRIORITY)}
        for task in tasks
    ]
    return jsonify(serialized_tasks)


@app.route('/api/tasks', methods=['POST'])
def add_task():
    """Create a task with a validated priority."""
    global next_id
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data.get('title'):
        return jsonify({"error": "Title is required"}), 400

    submitted_priority = data.get("priority", DEFAULT_PRIORITY)
    if isinstance(submitted_priority, str):
        normalized_priority = submitted_priority.strip().capitalize()
    else:
        normalized_priority = submitted_priority

    if normalized_priority not in ALLOWED_PRIORITIES:
        return jsonify({
            "error": "Priority must be Low, Medium, or High"
        }), 400

    new_task = {
        "id": next_id,
        "title": data['title'],
        "priority": normalized_priority
    }
    tasks.append(new_task)
    next_id += 1

    return jsonify(new_task), 201


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task by its identifier."""
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({"result": "success"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
