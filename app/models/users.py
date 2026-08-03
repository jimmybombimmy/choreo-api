from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy import DateTime
from sqlmodel import Field, Column, Relationship, SQLModel

from app.utils.get_datetime_bst import get_datetime_bst


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(max_length=30)
    email: str = Field(max_length=254)
    password: str = Field(max_length=30)
    created_at: datetime = Field(
        default_factory=get_datetime_bst, sa_column=Column(DateTime(timezone=True))
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True)),
    )
