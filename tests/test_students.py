from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def test_get_all_students():
    with TestClient(app) as client:
        response = client.get("/students")

    assert response.status_code == 200
    assert len(response.json()) >= 3


def test_get_student_by_id():
    with TestClient(app) as client:
        response = client.get("/students/20260001")

    assert response.status_code == 200
    data = response.json()
    assert data["student_id"] == "20260001"
    assert data["name"] == "Alice Zhang"


def test_get_nonexistent_student():
    with TestClient(app) as client:
        response = client.get("/students/99999999")

    assert response.status_code == 404


def test_create_student():
    unique_id = uuid4().hex[:8]
    payload = {
        "student_id": f"2027{unique_id}",
        "name": "David Chen",
        "email": f"david.{unique_id}@example.com",
        "major": "Software Engineering",
        "grade": 2027,
    }

    with TestClient(app) as client:
        response = client.post("/students", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["student_id"] == payload["student_id"]
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert "id" in data
    assert "created_at" in data


def test_create_student_duplicate_student_id():
    payload = {
        "student_id": "20260001",
        "name": "Duplicate Student ID",
        "email": f"duplicate.id.{uuid4().hex[:8]}@example.com",
        "major": "Computer Science",
        "grade": 2026,
    }

    with TestClient(app) as client:
        response = client.post("/students", json=payload)

    assert response.status_code == 409
    assert response.json()["detail"] == "Student ID already exists"


def test_create_student_duplicate_email():
    payload = {
        "student_id": f"2028{uuid4().hex[:8]}",
        "name": "Duplicate Email",
        "email": "alice@example.com",
        "major": "Computer Science",
        "grade": 2028,
    }

    with TestClient(app) as client:
        response = client.post("/students", json=payload)

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already exists"


def test_create_student_empty_student_id():
    payload = {
        "student_id": "   ",
        "name": "Empty Student ID",
        "email": f"empty.id.{uuid4().hex[:8]}@example.com",
        "major": "Software Engineering",
        "grade": 2027,
    }

    with TestClient(app) as client:
        response = client.post("/students", json=payload)

    assert response.status_code == 422


def test_create_student_empty_email():
    payload = {
        "student_id": f"2029{uuid4().hex[:8]}",
        "name": "Empty Email",
        "email": "   ",
        "major": "Software Engineering",
        "grade": 2029,
    }

    with TestClient(app) as client:
        response = client.post("/students", json=payload)

    assert response.status_code == 422
