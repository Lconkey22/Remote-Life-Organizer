from __future__ import annotations

from datetime import date, datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from backend.dependencies import get_store
from backend.main import app
from backend.store.memory_store import InMemoryStore


@pytest.fixture()
def client() -> TestClient:
    store = InMemoryStore()

    def _override_store() -> InMemoryStore:
        return store

    app.dependency_overrides[get_store] = _override_store
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_tasks_crud_and_complete(client: TestClient) -> None:
    due = (datetime.now() + timedelta(days=1)).isoformat()
    create_resp = client.post("/tasks/", json={"title": "Test task", "due_date": due})
    assert create_resp.status_code == 201
    task = create_resp.json()
    assert task["id"] == 1
    assert task["completed"] is False

    get_resp = client.get("/tasks/1")
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "Test task"

    patch_resp = client.patch("/tasks/1", json={"title": "Updated"})
    assert patch_resp.status_code == 200
    assert patch_resp.json()["title"] == "Updated"

    complete_resp = client.patch("/tasks/1/complete")
    assert complete_resp.status_code == 200
    assert complete_resp.json()["completed"] is True

    list_resp = client.get("/tasks/?completed=true")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    delete_resp = client.delete("/tasks/1")
    assert delete_resp.status_code == 200
    assert delete_resp.json() == {"deleted": True}

    missing_resp = client.get("/tasks/1")
    assert missing_resp.status_code == 404


def test_events_crud_and_validation(client: TestClient) -> None:
    start = datetime.now() + timedelta(hours=1)
    end = start + timedelta(hours=2)
    create_resp = client.post(
        "/events/",
        json={
            "name": "Meeting",
            "type": "Work",
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
        },
    )
    assert create_resp.status_code == 201
    event = create_resp.json()
    assert event["id"] == 1

    list_resp = client.get("/events/?type=Work")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    bad_create = client.post(
        "/events/",
        json={
            "name": "Bad",
            "type": "Work",
            "start_time": end.isoformat(),
            "end_time": start.isoformat(),
        },
    )
    assert bad_create.status_code == 422

    bad_patch = client.patch("/events/1", json={"end_time": (start - timedelta(hours=1)).isoformat()})
    assert bad_patch.status_code == 422

    delete_resp = client.delete("/events/1")
    assert delete_resp.status_code == 200


def test_homework_crud(client: TestClient) -> None:
    create_resp = client.post(
        "/homework/",
        json={
            "course": "Math",
            "due_date": date.today().isoformat(),
            "description": "Problem set",
        },
    )
    assert create_resp.status_code == 201
    hw = create_resp.json()
    assert hw["id"] == 1
    assert hw["completed"] is False

    patch_resp = client.patch("/homework/1", json={"completed": True})
    assert patch_resp.status_code == 200
    assert patch_resp.json()["completed"] is True

    list_resp = client.get("/homework/?completed=true")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    delete_resp = client.delete("/homework/1")
    assert delete_resp.status_code == 200
    assert client.get("/homework/1").status_code == 404


def test_time_entries_crud_and_validation(client: TestClient) -> None:
    start = datetime.now() - timedelta(hours=2)
    end = datetime.now() - timedelta(hours=1)
    create_resp = client.post(
        "/time-entries/",
        json={"type": "Work", "start_time": start.isoformat(), "end_time": end.isoformat(), "note": "Deep work"},
    )
    assert create_resp.status_code == 201
    entry = create_resp.json()
    assert entry["id"] == 1

    get_resp = client.get("/time-entries/1")
    assert get_resp.status_code == 200
    assert get_resp.json()["note"] == "Deep work"

    bad_patch = client.patch("/time-entries/1", json={"end_time": (start - timedelta(hours=1)).isoformat()})
    assert bad_patch.status_code == 422

    delete_resp = client.delete("/time-entries/1")
    assert delete_resp.status_code == 200


def test_homepage_aggregates_from_store(client: TestClient) -> None:
    now = datetime.now()
    client.post("/tasks/", json={"title": "Soon", "due_date": (now + timedelta(days=1)).isoformat()})
    client.post(
        "/events/",
        json={
            "name": "Soon Event",
            "type": "Work",
            "start_time": (now + timedelta(hours=1)).isoformat(),
            "end_time": (now + timedelta(hours=2)).isoformat(),
        },
    )

    resp = client.get("/homepage?days=7&tasks_limit=10&events_limit=10")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["tasks"]) == 1
    assert len(data["events"]) == 1
    assert len(data["notifications"]) >= 1

