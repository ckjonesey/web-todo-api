# Import Flask: the web framework that handles incoming requests.
# jsonify turns Python data into a JSON response; request reads data sent by the client.
from flask import Flask, jsonify, request
# Import sqlite3: Python's built-in library for talking to SQLite databases.
import sqlite3

# Create the Flask application object. __name__ tells Flask where this file lives.
app = Flask(__name__)

# The following block is a route that's currently turned off.
# A route connects a URL to a function. This one would answer /api/hello.
#@app.route("/api/hello")
# Function that runs when /api/hello is requested. It returns a JSON message.
#def hello():
    # Build a JSON response with one key, "message".
    #return jsonify({"message": "Hello from Flask"})

# Open a connection to the database file todo.db. If the file doesn't exist, SQLite creates it.
connection = sqlite3.connect('todo.db')
# A cursor is the object that runs SQL statements on that connection.
cursor = connection.cursor()

# Run a SQL statement that creates the todos table only if it doesn't already exist.
# The triple quotes let the SQL span several lines.
# Each task's unique number. INTEGER PRIMARY KEY makes it the row's identifier,
# and AUTOINCREMENT gives each new row a number one higher than the last.
# text holds the task's text, stored as a string.
# done records whether the task is finished, stored as 0 (not done) or 1 (done).
# NOT NULL means the column can't be empty, and CHECK limits it to 0 or 1.
cursor.execute('''CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    done BOOLEAN NOT NULL CHECK (done IN (0, 1))
)''')

# Save the table creation to the database file.
connection.commit()
# Close the connection, since this setup code is finished with it.
connection.close()

# Register get_todos to handle GET requests to /api/todos.
@app.route("/api/todos")
# Function that returns every task as JSON.
def get_todos():
    # Open a new connection, because each route runs separately and needs its own.
    connection = sqlite3.connect('todo.db')
    # Create a cursor for running SQL on this connection.
    cursor = connection.cursor()
    # Ask the database for every column of every row in the todos table.
    cursor.execute("SELECT * FROM todos")
    # Pull all the results into a list of tuples, such as (1, "Buy milk", 0).
    rows = cursor.fetchall()
    # Close the connection now that we have the data.
    connection.close()

    # Start an empty list that will hold the tasks as dictionaries.
    todos = []
    # Go through each row the database returned.
    for row in rows:
        # Turn the tuple into a dictionary with named keys the front end can read.
        todos.append({
            # Position 0 in the tuple is the id.
            "id": row[0],
            # Position 1 is the text.
            "text": row[1],
            # Position 2 is the done value, 0 or 1. bool() converts it to True or False.
            "done": bool(row[2])
        })
    # Convert the list into a JSON response and send it back.
    return jsonify(todos)

# Register post_todo to handle POST requests to /api/todos.
@app.route("/api/todos", methods=["POST"])
# Function that adds a new task.
def post_todo():
    # Read the JSON body the client sent. Returns a dictionary, or None if it isn't valid JSON.
    data = request.get_json()
    # If there's no data, no "text" key, or the text is blank after trimming spaces,
    # send an error message with status code 400 (bad request) and stop here.
    if not data or "text" not in data or not data["text"].strip():
        return jsonify({"error": "Invalid request"}), 400

    # Take the text from the request and remove spaces at both ends.
    text = data["text"].strip()
    # Open a new connection for this request.
    connection = sqlite3.connect('todo.db')
    # Create a cursor for running SQL on it.
    cursor = connection.cursor()
    # Insert a new row. The ? is a placeholder that gets the text value safely,
    # which prevents SQL injection. The 0 means the new task starts as not done.
    cursor.execute("INSERT INTO todos (text, done) VALUES (?, 0)", (text,))
    # Save the new row to the database file.
    connection.commit()
    # Read the id SQLite assigned to the row we just inserted.
    new_id = cursor.lastrowid
    # Close the connection.
    connection.close()

    # Send back the new task with status 201 (created).
    return jsonify({"id": new_id, "text": text, "done": False}), 201

@app.route("/api/todos/<int:todo_id>", methods=["PATCH"])
def patch_todo(todo_id):
    # Read the JSON body the client sent.
    data = request.get_json()
    # If there's no data or no "done" key, send an error message.
    if not data or "done" not in data:
        return jsonify({"error": "Invalid request"}), 400

    # Open a new connection for this request.
    connection = sqlite3.connect('todo.db')
    # Create a cursor for running SQL on it.
    cursor = connection.cursor()
    # Update the done value for the specified task.
    cursor.execute("UPDATE todos SET done = ? WHERE id = ?", (int(data["done"]), todo_id))
    if cursor.rowcount == 0:
        # If no rows were updated, the task didn't exist.
        connection.close()
        return jsonify({"error": "Task not found"}), 404
    # Save the changes to the database file.
    connection.commit()
    # Close the connection.
    connection.close()

    # Send back a success message.
    return jsonify({"message": "Task updated successfully"}), 200

@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    # Open a new connection for this request.
    connection = sqlite3.connect('todo.db')
    # Create a cursor for running SQL on it.
    cursor = connection.cursor()
    # Delete the specified task from the database.
    cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    if cursor.rowcount == 0:
        # If no rows were deleted, the task didn't exist.
        connection.close()
        return jsonify({"error": "Task not found"}), 404
    # Save the changes to the database file.
    connection.commit()
    # Close the connection.
    connection.close()

    # Send back a success message.
    return jsonify({"message": "Task deleted successfully"}), 200

# Run this block only when the file is started directly (python app.py),
# not when another file imports it.
if __name__ == "__main__":
    # Start the development server. debug=True reloads it when you save and shows error pages.
    app.run(debug=True)