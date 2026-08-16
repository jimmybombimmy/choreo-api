from uuid import UUID
from datetime import datetime

from sqlalchemy import DateTime, Enum as SQLEnum
from sqlmodel import Field, SQLModel, Column

from app.enums.model_enums import MembershipRoles
from app.utils.get_datetime_bst import get_datetime_bst


class UserTaskListMembership(SQLModel, table=True):
    __tablename__ = "user_task_list_memberships"

    user_id: UUID = Field(foreign_key="users.id", primary_key=True)
    task_list_id: UUID = Field(foreign_key="task_lists.id", primary_key=True)
    role: MembershipRoles = Field(
        default=MembershipRoles.VIEWER,
        sa_column=Column(
            SQLEnum(
                MembershipRoles,
                name="membership_roles",
                create_type=False,
            ),
            nullable=False,
            server_default="VIEWER",
        ),
    )
    created_at: datetime = Field(default_factory=get_datetime_bst)
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True)),
    )
