
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_project():
    response = client.post(
        "/projects",
        json={
            "name": "Test Project",
            "description": "Project created during testing",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Project"
    assert data["description"] == "Project created during testing"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_list_projects():
    response = client.get("/projects")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

