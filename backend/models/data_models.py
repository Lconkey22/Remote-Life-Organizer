from pydantic import BaseModel
from datetime import datetime
from typing import List

class Task(BaseModel):
    id: int
    title: str
    due_date: datetime
    completed: bool

class Event(BaseModel):
    id: int
    name: str
    start_time: datetime
    end_time: datetime

class HomepageData(BaseModel):
    tasks: List[Task]
    events: List[Event]
    notifications: List[str]

