"""Homepage aggregation routes."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends, Query

from backend.dependencies import get_store
from backend.models.data_models import HomepageData
from backend.store.memory_store import InMemoryStore

router = APIRouter()

def _build_notifications(tasks, events) -> List[str]:
    """Create a small list of human-readable dashboard notifications."""

    notifications: List[str] = []
    for task in tasks:
        notifications.append(f"Task due {task.due_date.isoformat()}: {task.title}")
    for event in events:
        notifications.append(
            f"Upcoming {event.type} event at {event.start_time.isoformat()}: {event.name}"
        )
    return notifications[:10]


@router.get("/homepage", response_model=HomepageData)
async def get_homepage(
    days: int = Query(default=7, ge=0, le=365),
    tasks_limit: int = Query(default=10, ge=0, le=100),
    events_limit: int = Query(default=10, ge=0, le=100),
    store: InMemoryStore = Depends(get_store),
) -> HomepageData:
    """Return dashboard data scoped to the next N days."""

    now = datetime.now()
    horizon = now + timedelta(days=days)

    tasks = store.list_tasks(
        completed=False, due_before=horizon, limit=tasks_limit, offset=0
    )
    events = store.list_events(
        start_after=now, start_before=horizon, limit=events_limit, offset=0
    )
    notifications = _build_notifications(tasks, events)
    return HomepageData(tasks=tasks, events=events, notifications=notifications)
