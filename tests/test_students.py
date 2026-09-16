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
