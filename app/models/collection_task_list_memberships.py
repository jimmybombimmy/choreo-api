from uuid import UUID
from datetime import datetime

from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel, Column

from app.utils.get_datetime_uk import get_datetime_uk


class CollectionTaskListMembership(SQLModel, table=True):
    __tablename__ = "collection_task_list_memberships"

    collection_id: UUID = Field(foreign_key="collections.id", primary_key=True)
    task_list_id: UUID = Field(foreign_key="task_lists.id", primary_key=True)
    created_at: datetime = Field(default_factory=get_datetime_uk)
    updated_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )
