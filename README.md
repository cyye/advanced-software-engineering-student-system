# Student Management System

## Project Purpose

This repository is a small backend project for a graduate Advanced Software Engineering course.

It demonstrates a simplified student information management system and is intentionally designed to be easy to read in a classroom setting. The project has enough structure for repository understanding, file search, planning, code modification, testing, and repair, while avoiding unnecessary framework complexity.

## Current Features

- List all students
- Get student by student ID
- Store student data in SQLite
- Initialize sample data when the database is empty
- Provide automated tests with pytest and FastAPI TestClient

## Project Structure

```text
student-system/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   └── services.py
├── tests/
│   ├── __init__.py
│   └── test_students.py
├── requirements.txt
├── README.md
├── AGENTS.md
├── .gitignore
└── agent-development-log.md
```

- `app/main.py`: creates the FastAPI application, defines HTTP APIs, and handles HTTP errors.
- `app/models.py`: defines the SQLAlchemy `Student` database model.
- `app/schemas.py`: defines Pydantic response schemas used by the API.
- `app/database.py`: configures SQLite, SQLAlchemy sessions, database initialization, and sample data.
- `app/services.py`: contains student-related business logic.
- `tests/`: contains pytest tests for the current API behavior.

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

Start the FastAPI application:

```bash
uvicorn app.main:app --reload
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

## Test

Run the test suite:

```bash
pytest -v
```

## Current Limitations

The current version does NOT support student registration.

It also does not include authentication, authorization, student login, course management, grade management, update APIs, or delete APIs.
