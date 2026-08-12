from typing import List

from sqlmodel import Field, SQLModel

from .users import User
from .collections import Collection
from .task_lists import TaskList
from .tasks import Task


class LocalSeedCollection(SQLModel):
    users: List[User] = Field(default_factory=list)
    collections: List[Collection] = Field(default_factory=list)
    task_lists: List[TaskList] = Field(default_factory=list)
    tasks: List[Task] = Field(default_factory=list)
