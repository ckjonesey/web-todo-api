from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/api/hello")
def hello():
    return jsonify({"message": "Hello from Flask"})

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

if __name__ == "__main__":
    app.run(debug=True)