"""Homework CRUD API routes."""

from __future__ import annotations

# pylint: disable=too-many-arguments,too-many-positional-arguments

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from backend.dependencies import get_store
from backend.models.data_models import HomeworkCreate, HomeworkRead, HomeworkUpdate
from backend.store.memory_store import InMemoryStore

router = APIRouter(prefix="/homework", tags=["Homework"])

DEFAULT_LIMIT = 100


@router.get("/", response_model=List[HomeworkRead])
def list_homework(
    course: Optional[str] = None,
    due_before: Optional[date] = None,
    due_after: Optional[date] = None,
    completed: Optional[bool] = None,
    limit: int = Query(default=DEFAULT_LIMIT, ge=0, le=1000),
    offset: int = Query(default=0, ge=0),
    store: InMemoryStore = Depends(get_store),
) -> List[HomeworkRead]:
    """List homework items with optional filters."""

    return store.list_homework(
        course=course,
        due_before=due_before,
        due_after=due_after,
        completed=completed,
        limit=limit,
        offset=offset,
    )


@router.post("/", response_model=HomeworkRead, status_code=status.HTTP_201_CREATED)
def create_homework(
    payload: HomeworkCreate,
    store: InMemoryStore = Depends(get_store),
) -> HomeworkRead:
    """Create a homework item."""

    return store.create_homework(payload)


@router.get("/{homework_id}", response_model=HomeworkRead)
def get_homework(
    homework_id: int,
    store: InMemoryStore = Depends(get_store),
) -> HomeworkRead:
    """Fetch a homework item by id."""

    item = store.get_homework(homework_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Homework not found")
    return item


@router.patch("/{homework_id}", response_model=HomeworkRead)
def update_homework(
    homework_id: int,
    payload: HomeworkUpdate,
    store: InMemoryStore = Depends(get_store),
) -> HomeworkRead:
    """Partially update a homework item by id."""

    updated = store.update_homework(homework_id, payload)
    if updated is None:
        raise HTTPException(status_code=404, detail="Homework not found")
    return updated


@router.delete("/{homework_id}")
def delete_homework(
    homework_id: int,
    store: InMemoryStore = Depends(get_store),
) -> dict:
    """Delete a homework item by id."""

    deleted = store.delete_homework(homework_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Homework not found")
    return {"deleted": True}
