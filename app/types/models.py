from typing import TypeAlias, TypeVar


from app.models.collections import Collection
from app.models.tasks import Task
from app.models.task_lists import TaskList
from app.models.users import User
from app.models.user_collection_memberships import UserCollectionMembership
from app.models.user_task_list_memberships import UserTaskListMembership
from app.models.collection_task_list_memberships import CollectionTaskListMembership
from app.models.collection_invitations import CollectionInvitation
from app.models.task_list_invitations import TaskListInvitation

ChoreoModel: TypeAlias = (
    User
    | Collection
    | TaskList
    | Task
    | UserCollectionMembership
    | UserTaskListMembership
    | CollectionInvitation
    | CollectionTaskListMembership
    | TaskListInvitation
)

ChoreoModelTypeVar = TypeVar("ChoreoModelTypeVar", bound=ChoreoModel)


ChoreoModelDeleteCascade = User | Collection | TaskList
