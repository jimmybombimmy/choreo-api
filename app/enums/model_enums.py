from sqlmodel import Enum


class MembershipRoles(Enum):
    VIEWER = "viewer"
    EDITOR = "editor"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"


class InvitationStatus(Enum):
    PENDING = ("PENDING",)
    ACCEPTED = ("ACCEPTED",)
    DECLINED = ("DECLINED",)
    EXPIRED = ("EXPIRED",)
