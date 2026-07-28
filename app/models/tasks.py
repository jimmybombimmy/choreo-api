from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy import DateTime
from sqlmodel import Field, Column, SQLModel

from app.utils.get_datetime_bst import get_datetime_bst


class Tasks(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=30)
    task_list_id: UUID = Field(foreign_key="task_lists.id")
    created_at: datetime = Field(
        default_factory=get_datetime_bst, sa_column=Column(DateTime(timezone=True))
    )
    last_completed_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )
    updated_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )
    completed: bool = False
    locked: bool = False
    parent_task_id: UUID | None = Field(default=None, foreign_key="tasks.id")
