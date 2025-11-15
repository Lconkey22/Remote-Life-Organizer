from fastapi import APIRouter
from ..models.data_models import HomepageData, Task, Event

router = APIRouter()

# Sample in-memory data
tasks = [
    {"id": 1, "title": "Finish assignment", "due_date": "2025-11-15T12:00:00", "completed": False}
]
events = [
    {"id": 1, "name": "Team Meeting", "start_time": "2025-11-14T15:00:00", "end_time": "2025-11-14T16:00:00"}
]

@router.get("/homepage", response_model=HomepageData)
async def get_homepage():
    return {"tasks": tasks, "events": events, "notifications": ["Meeting at 3 PM", "New assignment uploaded"]}

@router.patch("/tasks/{task_id}/complete")
async def complete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return {"message": "Task completed!"}
    return {"error": "Task not found"}
