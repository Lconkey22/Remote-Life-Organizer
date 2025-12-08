from fastapi import APIRouter
from backend.models.data_models import Task

router = APIRouter(prefix="/tasks", tags=["Tasks"])

fake_tasks = [
    Task(id=1, title="Finish CIS module", due_date="2025-02-10", completed=False),
    Task(id=2, title="Follow up on discussion post", due_date="2025-02-10", completed=False)
]

@router.get("/")
def get_tasks():
    return fake_tasks

@router.post("/")
def create_task(task: Task):
    fake_tasks.append(task)
    return {"message": "Task added", "task": task}
