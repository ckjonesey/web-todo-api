from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

#@app.route("/api/hello")
#def hello():
    #return jsonify({"message": "Hello from Flask"})

connection = sqlite3.connect('todo.db')
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    done BOOLEAN NOT NULL CHECK (done IN (0, 1))
)''')

connection.commit()
connection.close()

@app.route("/api/todos")
def get_todos():
    connection = sqlite3.connect('todo.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM todos")
    rows = cursor.fetchall()
    connection.close()

    todos = []
    for row in rows:
        todos.append({
            "id": row[0],
            "text": row[1],
            "done": bool(row[2])
        })
    return jsonify(todos)

@app.route("/api/todos", methods=["POST"])
def post_todo():
    data = request.get_json()
    if not data or "text" not in data or not data["text"].strip():
        return jsonify({"error": "Invalid request"}), 400

    text = data["text"].strip()
    connection = sqlite3.connect('todo.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO todos (text, done) VALUES (?, 0)", (text,))
    connection.commit()
    new_id = cursor.lastrowid
    connection.close()

    return jsonify({"id": new_id, "text": text, "done": False}), 201


if __name__ == "__main__":
    app.run(debug=True)