from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# In-memory list of tasks (no database)
tasks = []

@app.route('/', methods=['GET'])
def welcome():
    """Home endpoint - returns a welcome message."""
    return jsonify({
        "message": "Welcome to Task Management REST API",
        "docs": "/api/todos"
    }), 200

@app.route('/todos', methods=['GET'])
def get_tasks():
    """Retrieve all tasks."""
    return jsonify({"tasks": tasks}), 200

@app.route('/todos', methods=['POST'])
def create_task():
    """Create a new task.
    
    Expected JSON body: { "title": str, "description": str }
    Returns: 201 Created with the new task details.
    """
    data = request.get_json(silent=True)
    if not data or 'title' not in data or 'description' not in data:
        return jsonify({"error": "Title and description are required fields"}), 400
    task = {
        "id": len(tasks) + 1,
        "title": data['title'],
        "description": data['description'],
        "created_at": datetime.now().isoformat(),
    }
    tasks.append(task)
    return jsonify({"task": task, "message": "Task created successfully"}), 201

@app.route('/health', methods=['GET'])
def health_check():
    """Health-check endpoint - returns status of the service."""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    # Run on all interfaces, port 5000
    app.run(host='0.0.0.0', port=5000)
