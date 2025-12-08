from fastapi import APIRouter

router = APIRouter(prefix="/events", tags=["Events"])

fake_events = [
    {"id": 1, "name": "Zoom meeting with professor", "type": "Homework", "date": "2025-02-10"},
    {"id": 2, "name": "Work shift",  "type": "Work", "date": "2025-02-12"}
]

@router.get("/")
def get_events():
    return fake_events
