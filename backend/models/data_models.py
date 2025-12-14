"""Pydantic schemas for the Remote Life Organizer API.

These models are used for request validation and consistent responses.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field, model_validator


class TaskBase(BaseModel):
    """Shared task fields used in requests/responses."""

    title: str = Field(min_length=1)
    due_date: datetime
    completed: bool = False


class TaskCreate(TaskBase):
    """Request body for creating a task."""


class TaskUpdate(BaseModel):
    """Request body for partially updating a task."""

    title: Optional[str] = Field(default=None, min_length=1)
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None


class TaskRead(TaskBase):
    """Task representation returned by the API."""

    id: int


class EventBase(BaseModel):
    """Shared event fields used in requests/responses."""

    name: str = Field(min_length=1)
    type: str = Field(min_length=1)
    start_time: datetime
    end_time: datetime

    @model_validator(mode="after")
    def validate_time_order(self) -> "EventBase":
        """Ensure the event's end_time is after start_time."""

        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class EventCreate(EventBase):
    """Request body for creating an event."""


class EventUpdate(BaseModel):
    """Request body for partially updating an event."""

    name: Optional[str] = Field(default=None, min_length=1)
    type: Optional[str] = Field(default=None, min_length=1)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    @model_validator(mode="after")
    def validate_time_order_if_provided(self) -> "EventUpdate":
        """Ensure end_time is after start_time when both are provided."""

        if self.start_time is not None and self.end_time is not None:
            if self.end_time <= self.start_time:
                raise ValueError("end_time must be after start_time")
        return self


class EventRead(EventBase):
    """Event representation returned by the API."""

    id: int


class HomeworkBase(BaseModel):
    """Shared homework fields used in requests/responses."""

    course: str = Field(min_length=1)
    due_date: date
    description: str = Field(min_length=1)
    completed: bool = False


class HomeworkCreate(HomeworkBase):
    """Request body for creating a homework item."""


class HomeworkUpdate(BaseModel):
    """Request body for partially updating a homework item."""

    course: Optional[str] = Field(default=None, min_length=1)
    due_date: Optional[date] = None
    description: Optional[str] = Field(default=None, min_length=1)
    completed: Optional[bool] = None


class HomeworkRead(HomeworkBase):
    """Homework representation returned by the API."""

    id: int


class TimeEntryBase(BaseModel):
    """Shared time entry fields used in requests/responses."""

    type: str = Field(min_length=1)
    start_time: datetime
    end_time: datetime
    note: Optional[str] = None

    @model_validator(mode="after")
    def validate_time_order(self) -> "TimeEntryBase":
        """Ensure the entry's end_time is after start_time."""

        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class TimeEntryCreate(TimeEntryBase):
    """Request body for creating a time entry."""


class TimeEntryUpdate(BaseModel):
    """Request body for partially updating a time entry."""

    type: Optional[str] = Field(default=None, min_length=1)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    note: Optional[str] = None

    @model_validator(mode="after")
    def validate_time_order_if_provided(self) -> "TimeEntryUpdate":
        """Ensure end_time is after start_time when both are provided."""

        if self.start_time is not None and self.end_time is not None:
            if self.end_time <= self.start_time:
                raise ValueError("end_time must be after start_time")
        return self


class TimeEntryRead(TimeEntryBase):
    """Time entry representation returned by the API."""

    id: int


class HomepageData(BaseModel):
    """Aggregate dashboard data returned by `GET /homepage`."""

    tasks: List[TaskRead]
    events: List[EventRead]
    notifications: List[str]
