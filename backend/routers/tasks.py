"""Task CRUD API routes."""

from __future__ import annotations

# pylint: disable=too-many-arguments,too-many-positional-arguments

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from backend.dependencies import get_store
from backend.models.data_models import TaskCreate, TaskRead, TaskUpdate
from backend.store.memory_store import InMemoryStore

router = APIRouter(prefix="/tasks", tags=["Tasks"])

DEFAULT_LIMIT = 100

@router.get("/", response_model=List[TaskRead])
def list_tasks(
    completed: Optional[bool] = None,
    due_before: Optional[datetime] = None,
    due_after: Optional[datetime] = None,
    limit: int = Query(default=DEFAULT_LIMIT, ge=0, le=1000),
    offset: int = Query(default=0, ge=0),
    store: InMemoryStore = Depends(get_store),
) -> List[TaskRead]:
    """List tasks with optional filters."""

    return store.list_tasks(
        completed=completed,
        due_before=due_before,
        due_after=due_after,
        limit=limit,
        offset=offset,
    )

@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    store: InMemoryStore = Depends(get_store),
) -> TaskRead:
    """Create a task."""

    return store.create_task(payload)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    store: InMemoryStore = Depends(get_store),
) -> TaskRead:
    """Fetch a single task by id."""

    task = store.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    store: InMemoryStore = Depends(get_store),
) -> TaskRead:
    """Partially update a task by id."""

    updated = store.update_task(task_id, payload)
    if updated is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    store: InMemoryStore = Depends(get_store),
) -> dict:
    """Delete a task by id."""

    deleted = store.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"deleted": True}


@router.patch("/{task_id}/complete", response_model=TaskRead)
def complete_task(
    task_id: int,
    store: InMemoryStore = Depends(get_store),
) -> TaskRead:
    """Mark a task completed."""

    updated = store.update_task(task_id, TaskUpdate(completed=True))
    if updated is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated
