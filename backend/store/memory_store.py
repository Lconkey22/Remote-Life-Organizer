"""Thread-safe in-memory store for API resources.

This is the single source of truth for Tasks, Events, Homework, and Time Entries
while we are in the in-memory phase.
"""

from __future__ import annotations

# pylint: disable=missing-function-docstring,too-many-instance-attributes,too-many-public-methods,too-many-arguments

from dataclasses import dataclass
from datetime import date, datetime
from threading import Lock
from typing import Dict, List, Optional

from backend.models.data_models import (
    EventCreate,
    EventRead,
    EventUpdate,
    HomeworkCreate,
    HomeworkRead,
    HomeworkUpdate,
    TaskCreate,
    TaskRead,
    TaskUpdate,
    TimeEntryCreate,
    TimeEntryRead,
    TimeEntryUpdate,
)


def _paginate(items: List, limit: int, offset: int) -> List:
    """Return a paginated slice of a list."""

    offset = max(offset, 0)
    limit = max(limit, 0)
    return items[offset : offset + limit]


@dataclass(frozen=True)
class _IdSequence:
    start: int = 1


class InMemoryStore:
    """In-memory repository for all domain resources."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._task_id_seq = _IdSequence()
        self._event_id_seq = _IdSequence()
        self._homework_id_seq = _IdSequence()
        self._time_entry_id_seq = _IdSequence()
        self.reset()

    def reset(self) -> None:
        """Reset all resources (intended for tests/dev)."""
        with self._lock:
            self._next_task_id = self._task_id_seq.start
            self._next_event_id = self._event_id_seq.start
            self._next_homework_id = self._homework_id_seq.start
            self._next_time_entry_id = self._time_entry_id_seq.start
            self._tasks_by_id: Dict[int, TaskRead] = {}
            self._events_by_id: Dict[int, EventRead] = {}
            self._homework_by_id: Dict[int, HomeworkRead] = {}
            self._time_entries_by_id: Dict[int, TimeEntryRead] = {}

    # ---- Tasks ----
    def list_tasks(
        self,
        *,
        completed: Optional[bool] = None,
        due_before: Optional[datetime] = None,
        due_after: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[TaskRead]:
        tasks = list(self._tasks_by_id.values())
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        if due_before is not None:
            tasks = [t for t in tasks if t.due_date <= due_before]
        if due_after is not None:
            tasks = [t for t in tasks if t.due_date >= due_after]
        tasks.sort(key=lambda t: (t.due_date, t.id))
        return _paginate(tasks, limit=limit, offset=offset)

    def get_task(self, task_id: int) -> Optional[TaskRead]:
        return self._tasks_by_id.get(task_id)

    def create_task(self, payload: TaskCreate) -> TaskRead:
        with self._lock:
            task = TaskRead(id=self._next_task_id, **payload.model_dump())
            self._tasks_by_id[task.id] = task
            self._next_task_id += 1
            return task

    def update_task(self, task_id: int, payload: TaskUpdate) -> Optional[TaskRead]:
        with self._lock:
            existing = self._tasks_by_id.get(task_id)
            if existing is None:
                return None
            updated = existing.model_copy(update=payload.model_dump(exclude_unset=True))
            self._tasks_by_id[task_id] = updated
            return updated

    def delete_task(self, task_id: int) -> bool:
        with self._lock:
            return self._tasks_by_id.pop(task_id, None) is not None

    # ---- Events ----
    def list_events(
        self,
        *,
        type_: Optional[str] = None,
        completed: Optional[bool] = None,
        start_after: Optional[datetime] = None,
        start_before: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[EventRead]:
        events = list(self._events_by_id.values())
        if type_ is not None:
            events = [e for e in events if e.type == type_]
        if completed is not None:
            events = [e for e in events if e.completed == completed]
        if start_after is not None:
            events = [e for e in events if e.start_time >= start_after]
        if start_before is not None:
            events = [e for e in events if e.start_time <= start_before]
        events.sort(key=lambda e: (e.start_time, e.id))
        return _paginate(events, limit=limit, offset=offset)

    def get_event(self, event_id: int) -> Optional[EventRead]:
        return self._events_by_id.get(event_id)

    def create_event(self, payload: EventCreate) -> EventRead:
        with self._lock:
            event = EventRead(id=self._next_event_id, **payload.model_dump())
            self._events_by_id[event.id] = event
            self._next_event_id += 1
            return event

    def update_event(self, event_id: int, payload: EventUpdate) -> Optional[EventRead]:
        with self._lock:
            existing = self._events_by_id.get(event_id)
            if existing is None:
                return None
            updated = existing.model_copy(update=payload.model_dump(exclude_unset=True))
            if updated.end_time <= updated.start_time:
                raise ValueError("end_time must be after start_time")
            self._events_by_id[event_id] = updated
            return updated

    def delete_event(self, event_id: int) -> bool:
        with self._lock:
            return self._events_by_id.pop(event_id, None) is not None

    # ---- Homework ----
    def list_homework(
        self,
        *,
        course: Optional[str] = None,
        due_before: Optional[date] = None,
        due_after: Optional[date] = None,
        completed: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[HomeworkRead]:
        items = list(self._homework_by_id.values())
        if course is not None:
            items = [h for h in items if h.course == course]
        if completed is not None:
            items = [h for h in items if h.completed == completed]
        if due_before is not None:
            items = [h for h in items if h.due_date <= due_before]
        if due_after is not None:
            items = [h for h in items if h.due_date >= due_after]
        items.sort(key=lambda h: (h.due_date, h.id))
        return _paginate(items, limit=limit, offset=offset)

    def get_homework(self, homework_id: int) -> Optional[HomeworkRead]:
        return self._homework_by_id.get(homework_id)

    def create_homework(self, payload: HomeworkCreate) -> HomeworkRead:
        with self._lock:
            hw = HomeworkRead(id=self._next_homework_id, **payload.model_dump())
            self._homework_by_id[hw.id] = hw
            self._next_homework_id += 1
            return hw

    def update_homework(
        self, homework_id: int, payload: HomeworkUpdate
    ) -> Optional[HomeworkRead]:
        with self._lock:
            existing = self._homework_by_id.get(homework_id)
            if existing is None:
                return None
            updated = existing.model_copy(update=payload.model_dump(exclude_unset=True))
            self._homework_by_id[homework_id] = updated
            return updated

    def delete_homework(self, homework_id: int) -> bool:
        with self._lock:
            return self._homework_by_id.pop(homework_id, None) is not None

    # ---- Time Entries ----
    def list_time_entries(
        self,
        *,
        type_: Optional[str] = None,
        start_after: Optional[datetime] = None,
        start_before: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[TimeEntryRead]:
        entries = list(self._time_entries_by_id.values())
        if type_ is not None:
            entries = [e for e in entries if e.type == type_]
        if start_after is not None:
            entries = [e for e in entries if e.start_time >= start_after]
        if start_before is not None:
            entries = [e for e in entries if e.start_time <= start_before]
        entries.sort(key=lambda e: (e.start_time, e.id))
        return _paginate(entries, limit=limit, offset=offset)

    def get_time_entry(self, entry_id: int) -> Optional[TimeEntryRead]:
        return self._time_entries_by_id.get(entry_id)

    def create_time_entry(self, payload: TimeEntryCreate) -> TimeEntryRead:
        with self._lock:
            entry = TimeEntryRead(id=self._next_time_entry_id, **payload.model_dump())
            self._time_entries_by_id[entry.id] = entry
            self._next_time_entry_id += 1
            return entry

    def update_time_entry(
        self, entry_id: int, payload: TimeEntryUpdate
    ) -> Optional[TimeEntryRead]:
        with self._lock:
            existing = self._time_entries_by_id.get(entry_id)
            if existing is None:
                return None
            updated = existing.model_copy(update=payload.model_dump(exclude_unset=True))
            if updated.end_time <= updated.start_time:
                raise ValueError("end_time must be after start_time")
            self._time_entries_by_id[entry_id] = updated
            return updated

    def delete_time_entry(self, entry_id: int) -> bool:
        with self._lock:
            return self._time_entries_by_id.pop(entry_id, None) is not None
