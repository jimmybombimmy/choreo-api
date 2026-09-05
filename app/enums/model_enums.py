from enum import Enum


class MembershipRoles(str, Enum):
    VIEWER = "VIEWER"
    USER = "USER"
    EDITOR = "EDITOR"
    ADMIN = "ADMIN"
    OWNER = "OWNER"


class InvitationStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    EXPIRED = "EXPIRED"


class TableList(str, Enum):
    User = "User"
    Collection = "Collection"
    TaskList = "TaskList"
    Task = "Task"
    UserCollectionMembership = "UserCollectionMembership"
    UserTaskListMembership = "UserTaskListMembership"
    CollectionTaskListMembership = "CollectionTaskListMembership"
    CollectionInvitation = "CollectionInvitation"
    TaskListInvitation = "TaskListInvitation"


class TableListDeleteCascade(str, Enum):
    User = "User"
    Collection = "Collection"
    TaskList = "TaskList"
