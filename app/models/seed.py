from typing import List

from sqlmodel import Field, SQLModel

from .users import User
from .collections import Collection
from .task_lists import TaskList
from .tasks import Task
from .user_collection_memberships import UserCollectionMembership
from .user_task_list_memberships import UserTaskListMembership
from .collection_task_list_memberships import CollectionTaskListMembership
from .collection_invitations import CollectionInvitation
from .task_list_invitations import TaskListInvitation


class LocalSeedCollection(SQLModel):
    users: List[User] = Field(default_factory=list)
    collections: List[Collection] = Field(default_factory=list)
    task_lists: List[TaskList] = Field(default_factory=list)
    tasks: List[Task] = Field(default_factory=list)
    user_collection_memberships: List[UserCollectionMembership] = Field(
        default_factory=list
    )
    user_task_list_memberships: List[UserTaskListMembership] = Field(
        default_factory=list
    )
    collection_task_list_memberships: List[CollectionTaskListMembership] = Field(
        default_factory=list
    )
    collection_invitations: list[CollectionInvitation] = Field(default_factory=list)
    task_list_invitations: list[TaskListInvitation] = Field(default_factory=list)
