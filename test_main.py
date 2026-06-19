from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_create_and_list_todo():
    r = client.post("/todos", json={"title": "Learn DevOps"})
    assert r.status_code == 201
    created = r.json()
    assert created["title"] == "Learn DevOps"
    assert created["done"] is False

    r = client.get("/todos")
    assert any(t["id"] == created["id"] for t in r.json())


def test_get_missing_todo():
    r = client.get("/todos/99999")
    assert r.status_code == 404
