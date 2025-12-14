"""Event CRUD API routes."""

from __future__ import annotations

# pylint: disable=too-many-arguments,too-many-positional-arguments

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from backend.dependencies import get_store
from backend.models.data_models import EventCreate, EventRead, EventUpdate
from backend.store.memory_store import InMemoryStore

router = APIRouter(prefix="/events", tags=["Events"])

DEFAULT_LIMIT = 100

@router.get("/", response_model=List[EventRead])
def list_events(
    type_: Optional[str] = Query(default=None, alias="type"),
    completed: Optional[bool] = None,
    start_after: Optional[datetime] = None,
    start_before: Optional[datetime] = None,
    limit: int = Query(default=DEFAULT_LIMIT, ge=0, le=1000),
    offset: int = Query(default=0, ge=0),
    store: InMemoryStore = Depends(get_store),
) -> List[EventRead]:
    """List events with optional filters."""

    return store.list_events(
        type_=type_,
        completed=completed,
        start_after=start_after,
        start_before=start_before,
        limit=limit,
        offset=offset,
    )


@router.post("/", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(
    payload: EventCreate,
    store: InMemoryStore = Depends(get_store),
) -> EventRead:
    """Create an event."""

    return store.create_event(payload)


@router.get("/{event_id}", response_model=EventRead)
def get_event(
    event_id: int,
    store: InMemoryStore = Depends(get_store),
) -> EventRead:
    """Fetch a single event by id."""

    event = store.get_event(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.patch("/{event_id}", response_model=EventRead)
def update_event(
    event_id: int,
    payload: EventUpdate,
    store: InMemoryStore = Depends(get_store),
) -> EventRead:
    """Partially update an event by id."""

    try:
        updated = store.update_event(event_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    if updated is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return updated


@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    store: InMemoryStore = Depends(get_store),
) -> dict:
    """Delete an event by id."""

    deleted = store.delete_event(event_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"deleted": True}
