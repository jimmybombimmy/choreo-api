from app.core.db import SessionDep
from app.models.user_task_list_memberships import UserTaskListMembership


def create_user_task_list_membership(
    user_task_list_membership: UserTaskListMembership, session: SessionDep
) -> UserTaskListMembership:
    session.add(user_task_list_membership)
    session.commit()
    session.refresh(user_task_list_membership)
    return user_task_list_membership


def delete_user(user_task_list_membership: UserTaskListMembership, session: SessionDep):
    session.delete(user_task_list_membership)
    session.commit()
