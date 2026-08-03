from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy import DateTime
from sqlmodel import Field, Column, SQLModel

from app.utils.get_datetime_bst import get_datetime_bst


class TaskTypes(SQLModel, table=True):
    __tablename__ = "task_types"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=30)
    description: str | None = Field(default=None, max_length=140)
    created_at: datetime = Field(
        default_factory=get_datetime_bst, sa_column=Column(DateTime(timezone=True))
    )
    updated_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )
