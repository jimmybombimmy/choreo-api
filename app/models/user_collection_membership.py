from uuid import UUID
from datetime import datetime

from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel, Column

from app.enums.model_enums import MembershipRoles
from app.utils.get_datetime_bst import get_datetime_bst


class UserCollectionMembership(SQLModel, table=True):
    __tablename__ = "user_collection_memberships"

    user_id: UUID = Field(foreign_key="users.id", primary_key=True)
    collection_id: UUID = Field(foreign_key="collection.id", primary_key=True)
    created_at: datetime = Field(default_factory=get_datetime_bst)
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True)),
    )
