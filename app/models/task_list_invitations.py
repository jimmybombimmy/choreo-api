from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel, Column

from app.enums.model_enums import InvitationStatus
from app.utils.get_datetime_bst import get_datetime_bst


class TaskListInvitation(SQLModel, table=True):
    __tablename__ = "task_list_invitations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    task_list_id: UUID = Field(foreign_key="task_lists.id")
    sender_id: UUID = Field(foreign_key="users.id")
    recipient_id: UUID = Field(foreign_key="users.id")
    status: InvitationStatus = Field(default=InvitationStatus.PENDING)
    created_at: datetime = Field(default_factory=get_datetime_bst)
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True)),
    )
