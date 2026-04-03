from flask import Flask, jsonify, request
# Flask - main class
# jsonify - function to convert data to JSON format
# request - object that contains data about the incoming request

app = Flask(__name__)

tasks =[] # list to store tasks in memory

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Task Manager API",
        "endpoints": {
            "GET /health": "Check API health",
            "GET /tasks": "List all tasks",
            "POST /tasks": "Create a task",
            "GET /tasks/<id>": "Get one task",
            "PUT /tasks/<id>": "Update a task",
            "DELETE /tasks/<id>": "Delete a task"
        }
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks}), 200


@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "done": False
    }
    tasks.append(task)
    return jsonify({"task": task}), 201


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    tasks.remove(task)
    return jsonify({"message": "Task deleted"}), 200

if __name__ == '__main__':
    app.run(debug=os.getenv("FLASK_DEBUG", False), port=5000)