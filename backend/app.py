from flask import Flask, jsonify, request
import os
import mysql.connector

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "mahasan")
DB_PASSWORD = os.getenv("DB_PASSWORD", "mahasandatabase")
DB_NAME = os.getenv("DB_NAME", "shoppingdb")

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.route("/api/plans", methods=["GET"])
def get_plans():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM shopping_plans")
    plans = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(plans=plans)

@app.route("/api/plans", methods=["POST"])
def create_plan():
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"error": "name is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO shopping_plans (name) VALUES (%s)", (name,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Plan created successfully"}), 201

@app.route("/api/plans/<int:plan_id>/tasks", methods=["GET"])
def get_tasks(plan_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM tasks WHERE plan_id = %s", (plan_id,))
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(tasks=tasks)

@app.route("/api/plans/<int:plan_id>/tasks", methods=["POST"])
def create_task(plan_id):
    data = request.get_json()
    title = data.get("title")
    if not title:
        return jsonify({"error": "title is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title, plan_id) VALUES (%s, %s)", (title, plan_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Task created successfully"}), 201

@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    completed = data.get("completed")
    if completed is None:
        return jsonify({"error": "completed is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET completed = %s WHERE id = %s", (completed, task_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Task updated successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)