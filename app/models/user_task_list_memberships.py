from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy import DateTime
from sqlmodel import Field, Column, Relationship, SQLModel, Enum

from app.models.task_lists import TaskLists
from app.utils.get_datetime_bst import get_datetime_bst


class UTLMRoles(Enum):
    VIEWER = "viewer"
    EDITOR = "editor"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"


class UserTaskListLink(SQLModel, table=True):
    __tablename__ = "user_task_list_memberships"

    user_id: UUID = Field(foreign_key="users.id", primary_key=True)
    task_list_id: UUID = Field(foreign_key="task_lists.id", primary_key=True)
    role: UTLMRoles = Field(default=UTLMRoles.VIEWER)
    created_at: datetime = Field(default_factory=get_datetime_bst)
    updated_at: datetime | None = None
