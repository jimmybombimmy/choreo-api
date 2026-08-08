from uuid import UUID
from datetime import datetime

from sqlmodel import Field, SQLModel, Enum

from app.utils.get_datetime_bst import get_datetime_bst


class UTLMRoles(Enum):
    VIEWER = "viewer"
    EDITOR = "editor"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"


class UserTaskListMembership(SQLModel, table=True):
    __tablename__ = "user_task_list_memberships"

    user_id: UUID = Field(foreign_key="users.id", primary_key=True)
    task_list_id: UUID = Field(foreign_key="task_lists.id", primary_key=True)
    role: UTLMRoles = Field(default=UTLMRoles.VIEWER)
    created_at: datetime = Field(default_factory=get_datetime_bst)
    updated_at: datetime | None = None
