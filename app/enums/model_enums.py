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
