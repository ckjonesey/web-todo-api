# web-todo-api
Building on web-todo. This repo is for moving the storage from localstorage to a server and a database
# Web To-Do App

A to-do list with a vanilla JavaScript front end and a Flask + SQLite back end. Tasks can be added, checked off, deleted individually, and cleared in bulk when completed.

**Live demo:** https://web-todo-api.onrender.com

## Features

- Add a task
- Check or uncheck a task (state saves to the server)
- Delete a completed task
- Clear all completed tasks
- Tasks persist in a SQLite database

## Tech Stack

- **Front end:** HTML, CSS, JavaScript (fetch API)
- **Back end:** Python, Flask
- **Database:** SQLite (`sqlite3` standard library)
- **Testing:** pytest
- **Production server:** gunicorn
- **Hosting:** Render

## Project Structure

```
web-todo-api/
├── app.py              # Flask app: routes, database setup
├── test_app.py         # pytest tests for the API
├── requirements.txt    # Python dependencies
├── .gitignore          # Ignores venv, __pycache__, *.db, .DS_Store
└── frontend/
    ├── index.html      # Page markup
    ├── style.css       # Styles
    └── app.js          # Front-end logic, calls the API
```

## API Reference

| Method | Route | Description | Success | Errors |
|--------|-------|-------------|---------|--------|
| GET | `/api/todos` | List all todos | 200 | 500 |
| POST | `/api/todos` | Add a todo. Body: `{"text": "..."}` | 201 | 400 (blank text), 500 |
| PATCH | `/api/todos/<id>` | Update done state. Body: `{"done": true}` | 200 | 400 (invalid body), 404, 500 |
| DELETE | `/api/todos/<id>` | Delete a todo | 200 | 404, 500 |

Each todo is returned as:

```json
{"id": 1, "text": "Buy milk", "done": false}
```

## Getting Started

### Prerequisites

- Python 3.10+
- Git

### Setup

```bash
git clone https://github.com/<your-username>/web-todo-api.git
cd web-todo-api

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Run Locally

```bash
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

> **Note:** On macOS, port 5000 may be taken by AirPlay Receiver. If you get a 403 error, turn off AirPlay Receiver in System Settings, or change the port.

The database file (`todo.db`) is created automatically on first run.

### Run Tests

```bash
pytest -v
```

Tests use a temporary database, so your real `todo.db` is never touched.

## Deployment

The app is deployed on Render as a web service.

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn --bind 0.0.0.0:$PORT app:app`

Render redeploys automatically on each push to the main branch.

> **Note:** The free tier uses ephemeral storage, so `todo.db` may reset on redeploy or restart. The free tier also sleeps after inactivity, so the first request can take a moment.

## What I Learned

- Building a front end that talks to an API with `fetch`
- Designing REST-style routes and returning proper HTTP status codes
- Using parameterized SQL queries to prevent SQL injection
- Writing isolated pytest tests with fixtures
- Separating development (`python app.py`) from production (gunicorn)
- Deploying a Python web app to Render

## Roadmap

- [ ] Rebuild the front end in React using the same API
- [ ] Persist data with a hosted database
- [ ] Add a bulk-delete route for clear-completed

## License

MIT (or your choice)