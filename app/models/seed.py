from typing import List

from sqlmodel import Field, SQLModel

from app.models.collections import Collection

from .users import User


class LocalSeedCollection(SQLModel):
    users: List[User] = Field(default_factory=list)
    collections: List[Collection] = Field(default_factory=list)
