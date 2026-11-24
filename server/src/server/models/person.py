from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class Status(StrEnum):
    CREATED = "Created"
    CONTACTED = "Contacted"
    ACTIVE = "Active"
    CLOSED = "Closed"


class Person(BaseModel):
    id: int | None = None
    created_at: datetime | None = None
    name: str
    email: str | None = None
    title: str
    company: str
    status: Status = Status.CREATED


class SaveResult(BaseModel):
    saved: bool
    reason: str | None = None
    person: Person
