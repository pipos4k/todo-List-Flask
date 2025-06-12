# Todo List Flask API

A simple RESTful API built with Flask and SQLAlchemy to manage a todo list. It supports adding, updating, retrieving, and deleting tasks stored in an SQLite database.

---

## Features

- **GET /tasks** — Retrieve all tasks
- **GET /tasks/<id>** — Retrieve a specific task by ID
- **POST /tasks** — Add a new task (JSON payload)
- **PATCH /tasks/<id>** — Update task details (JSON payload)
- **DELETE /tasks/<id>** — Delete a task by ID

---

## Technologies Used

- Python 3
- Flask
- Flask-Login
- Flask-WTF
- SQLAlchemy (SQLite as database)
- HTML5, CSS3, Bootstrap
- Jinja2 templating engine
---

## Setup and Running

1. Clone the repo:
   ```bash
   git clone https://github.com/pipos4k/todo-List-Flask.git
   cd todo-List-Flask
2. Install dependencies (ideally in a virtual environment):
   ```bash
   pip install -r requirements.txt
3. Run the app:
```bash
  python app.py
```
4. The API will be accessible at http://localhost:5000

## About
This project is inspired by the 100 Days of Code challenge with Angela Yu from Udemy.
It’s a practical exercise in building REST APIs with Flask and SQLAlchemy.
