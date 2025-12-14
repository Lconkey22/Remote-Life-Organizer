"""Time entry CRUD API routes."""

from __future__ import annotations

# pylint: disable=too-many-arguments,too-many-positional-arguments,duplicate-code

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from backend.dependencies import get_store
from backend.models.data_models import TimeEntryCreate, TimeEntryRead, TimeEntryUpdate
from backend.store.memory_store import InMemoryStore

router = APIRouter(prefix="/time-entries", tags=["Time Entries"])

DEFAULT_LIMIT = 100


@router.get("/", response_model=List[TimeEntryRead])
def list_time_entries(
    type_: Optional[str] = Query(default=None, alias="type"),
    start_after: Optional[datetime] = None,
    start_before: Optional[datetime] = None,
    limit: int = Query(default=DEFAULT_LIMIT, ge=0, le=1000),
    offset: int = Query(default=0, ge=0),
    store: InMemoryStore = Depends(get_store),
) -> List[TimeEntryRead]:
    """List time entries with optional filters."""

    return store.list_time_entries(
        type_=type_,
        start_after=start_after,
        start_before=start_before,
        limit=limit,
        offset=offset,
    )


@router.post("/", response_model=TimeEntryRead, status_code=status.HTTP_201_CREATED)
def create_time_entry(
    payload: TimeEntryCreate,
    store: InMemoryStore = Depends(get_store),
) -> TimeEntryRead:
    """Create a time entry."""

    return store.create_time_entry(payload)


@router.get("/{entry_id}", response_model=TimeEntryRead)
def get_time_entry(
    entry_id: int,
    store: InMemoryStore = Depends(get_store),
) -> TimeEntryRead:
    """Fetch a time entry by id."""

    entry = store.get_time_entry(entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Time entry not found")
    return entry


@router.patch("/{entry_id}", response_model=TimeEntryRead)
def update_time_entry(
    entry_id: int,
    payload: TimeEntryUpdate,
    store: InMemoryStore = Depends(get_store),
) -> TimeEntryRead:
    """Partially update a time entry by id."""

    try:
        updated = store.update_time_entry(entry_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    if updated is None:
        raise HTTPException(status_code=404, detail="Time entry not found")
    return updated


@router.delete("/{entry_id}")
def delete_time_entry(
    entry_id: int,
    store: InMemoryStore = Depends(get_store),
) -> dict:
    """Delete a time entry by id."""

    deleted = store.delete_time_entry(entry_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Time entry not found")
    return {"deleted": True}
