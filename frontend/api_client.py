"""Frontend HTTP client helpers for calling the backend API."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

import httpx

API_BASE_URL = "http://127.0.0.1:8000"


def _maybe_iso(value: Optional[datetime]) -> Optional[str]:
    if value is None:
        return None
    return value.isoformat()


async def get_homepage() -> dict[str, Any]:
    """Fetch homepage aggregation data from the backend."""
    async with httpx.AsyncClient(base_url=API_BASE_URL) as client:
        r = await client.get("/homepage")
        r.raise_for_status()
        return r.json()


async def complete_task(task_id: int) -> dict[str, Any]:
    """Mark a task as completed in the backend."""
    async with httpx.AsyncClient(base_url=API_BASE_URL) as client:
        r = await client.patch(f"/tasks/{task_id}/complete")
        r.raise_for_status()
        return r.json()


async def get_events(
    *,
    type_: Optional[str] = None,
    start_after: Optional[datetime] = None,
    start_before: Optional[datetime] = None,
    limit: int = 100,
    offset: int = 0,
) -> list[dict[str, Any]]:
    """Fetch events from the backend with optional filters."""

    params: dict[str, Any] = {"limit": limit, "offset": offset}
    if type_ is not None:
        params["type"] = type_
    if start_after is not None:
        params["start_after"] = _maybe_iso(start_after)
    if start_before is not None:
        params["start_before"] = _maybe_iso(start_before)

    async with httpx.AsyncClient(base_url=API_BASE_URL) as client:
        r = await client.get("/events/", params=params)
        r.raise_for_status()
        return r.json()


async def create_event(
    *,
    name: str,
    type_: str,
    start_time: datetime,
    end_time: datetime,
) -> dict[str, Any]:
    """Create an event in the backend."""

    payload = {
        "name": name,
        "type": type_,
        "start_time": _maybe_iso(start_time),
        "end_time": _maybe_iso(end_time),
    }
    async with httpx.AsyncClient(base_url=API_BASE_URL) as client:
        r = await client.post("/events/", json=payload)
        r.raise_for_status()
        return r.json()


async def get_time_entries(
    *,
    type_: Optional[str] = None,
    start_after: Optional[datetime] = None,
    start_before: Optional[datetime] = None,
    limit: int = 100,
    offset: int = 0,
) -> list[dict[str, Any]]:
    """Fetch time entries from the backend with optional filters."""

    params: dict[str, Any] = {"limit": limit, "offset": offset}
    if type_ is not None:
        params["type"] = type_
    if start_after is not None:
        params["start_after"] = _maybe_iso(start_after)
    if start_before is not None:
        params["start_before"] = _maybe_iso(start_before)

    async with httpx.AsyncClient(base_url=API_BASE_URL) as client:
        r = await client.get("/time-entries/", params=params)
        r.raise_for_status()
        return r.json()
