from typing import List

from sqlmodel import Field, SQLModel

from .users import User


class LocalSeedCollection(SQLModel):
    users: List[User] = Field(default_factory=list)
