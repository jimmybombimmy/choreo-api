from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy import DateTime
from sqlmodel import Field, Column, SQLModel

from app.utils.get_datetime_bst import get_datetime_bst


class TaskList(SQLModel, table=True):
    __tablename__ = "task_lists"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=30)
    collection_id: UUID = Field(foreign_key="collections.id")
    created_at: datetime = Field(
        default_factory=get_datetime_bst, sa_column=Column(DateTime(timezone=True))
    )
    last_completed_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )
    updated_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )
    locked: bool = False
