import pytest
import app as todo_app

@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(todo_app, "DB_PATH", str(tmp_path / "test.db"))
    todo_app.init_db()
    todo_app.app.config["TESTING"] = True
    with todo_app.app.test_client() as client:
        yield client

def test_add_then_list(client):
    # Add a new task.
    response = client.post("/api/todos", json={"text": "Test task"})
    assert response.status_code == 201

    response = client.get("/api/todos")
    assert len(response.get_json()) == 1

def test_blank_text(client):
    response = client.post("/api/todos", json={"text": "   "})
    assert response.status_code == 400

def test_patch_todo(client):
    # Add a new task.
    response = client.post("/api/todos", json={"text": "Test task"})
    assert response.status_code == 201
    todo_id = response.get_json()["id"]

    # Mark the task as done.
    response = client.patch(f"/api/todos/{todo_id}", json={"done": True})
    assert response.status_code == 200

    # Verify that the task is marked as done.
    response = client.get("/api/todos")
    todos = response.get_json()
    assert len(todos) == 1
    assert todos[0]["done"] is True

def test_patch_nonexistent_todo(client):
    response = client.patch("/api/todos/999", json={"done": True})
    assert response.status_code == 404

def test_patch_invalid_request(client):
    # Add a new task.
    response = client.post("/api/todos", json={"text": "Test task"})
    assert response.status_code == 201
    todo_id = response.get_json()["id"]

    # Try to patch without "done" key.
    response = client.patch(f"/api/todos/{todo_id}", json={})
    assert response.status_code == 400

def test_delete_missing_todo(client):
    response = client.delete("/api/todos/999")
    assert response.status_code == 404

def test_delete_todo(client):
    # Add a new task.
    response = client.post("/api/todos", json={"text": "Test task"})
    assert response.status_code == 201
    todo_id = response.get_json()["id"]

    # Delete the task.
    response = client.delete(f"/api/todos/{todo_id}")
    assert response.status_code == 200

    # Verify that the task is deleted.
    response = client.get("/api/todos")
    todos = response.get_json()
    assert len(todos) == 0