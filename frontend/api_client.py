"""Frontend HTTP client helpers for calling the backend API."""

import httpx
API_BASE_URL = "http://127.0.0.1:8000"

async def get_homepage():
    """Fetch homepage aggregation data from the backend."""
    async with httpx.AsyncClient(base_url=API_BASE_URL) as client:
        r = await client.get("/homepage")
        r.raise_for_status()
        return r.json()

async def complete_task(task_id: int):
    """Mark a task as completed in the backend."""
    async with httpx.AsyncClient(base_url=API_BASE_URL) as client:
        r = await client.patch(f"/tasks{task_id}/complete")
        r.raise_for_status()
        return r.json()
