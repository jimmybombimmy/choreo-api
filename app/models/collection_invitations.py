from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel, Column

from app.enums.model_enums import InvitationStatus
from app.utils.get_datetime_uk import get_datetime_uk


class CollectionInvitation(SQLModel, table=True):
    __tablename__ = "collection_invitations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    collection_id: UUID = Field(foreign_key="collections.id", ondelete="CASCADE")
    sender_id: UUID = Field(foreign_key="users.id", ondelete="CASCADE")
    recipient_id: UUID = Field(foreign_key="users.id", ondelete="CASCADE")
    status: InvitationStatus = Field(default=InvitationStatus.PENDING)
    created_at: datetime = Field(default_factory=get_datetime_uk)
    updated_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )
