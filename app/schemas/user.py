"""
A user schema will live here.
Database representation and API representation often shouldn't be the same thing.
"""

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class UserOut(BaseModel):
    id: UUID
    username: str
    email: str
    password: str
    created_at: datetime
    updated_at: datetime | None
