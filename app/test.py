from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Testing creation",
            "completed": False
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"


def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task():
    create = client.post(
        "/tasks",
        json={
            "title": "Get Task",
            "description": "Testing get",
            "completed": False
        }
    )

    task_id = create.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_delete_task():
    create = client.post(
        "/tasks",
        json={
            "title": "Delete Task",
            "description": "Testing delete",
            "completed": False
        }
    )

    task_id = create.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200