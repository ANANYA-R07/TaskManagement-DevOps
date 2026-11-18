import os
import sqlite3
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

# Database configuration
DB_PATH = os.environ.get("DB_PATH", "tasks.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    # Create the database directory if needed
    os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)

    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# Initialize database
init_db()


@app.route("/", methods=["GET"])
def welcome():
    return jsonify({
        "message": "Welcome to Task Management REST API",
        "docs": "/api/todos"
    }), 200


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200


# READ all tasks
@app.route("/todos", methods=["GET"])
def get_tasks():
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM tasks ORDER BY id"
        ).fetchall()
        return jsonify({"tasks": [dict(row) for row in rows]}), 200
    finally:
        conn.close()


# CREATE a task
@app.route("/todos", methods=["POST"])
def create_task():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON body is required"}), 400

    title = data.get("title")
    description = data.get("description")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "A valid title is required"}), 400

    if not isinstance(description, str) or not description.strip():
        return jsonify({"error": "A valid description is required"}), 400

    created_at = datetime.now().astimezone().isoformat()

    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO tasks (title, description, created_at) VALUES (?, ?, ?)",
            (title.strip(), description.strip(), created_at)
        )
        conn.commit()

        task = conn.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (cursor.lastrowid,)
        ).fetchone()

        return jsonify({
            "task": dict(task),
            "message": "Task created successfully"
        }), 201
    finally:
        conn.close()


# UPDATE a task
@app.route("/todos/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON body is required"}), 400

    title = data.get("title")
    description = data.get("description")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "A valid title is required"}), 400

    if not isinstance(description, str) or not description.strip():
        return jsonify({"error": "A valid description is required"}), 400

    conn = get_connection()
    try:
        cursor = conn.execute(
            "UPDATE tasks SET title = ?, description = ? WHERE id = ?",
            (title.strip(), description.strip(), task_id)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Task not found"}), 404

        task = conn.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()

        return jsonify({
            "task": dict(task),
            "message": "Task updated successfully"
        }), 200
    finally:
        conn.close()


# DELETE a task
@app.route("/todos/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_connection()
    try:
        cursor = conn.execute(
            "DELETE FROM tasks WHERE id = ?", (task_id,)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Task not found"}), 404

        return jsonify({
            "message": "Task deleted successfully"
        }), 200
    finally:
        conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)