from app.core.db import SessionDep
from app.models.task_list_invitations import TaskListInvitation


def create_task_list_invitation(
    task_list_invitation: TaskListInvitation, session: SessionDep
) -> TaskListInvitation:
    session.add(task_list_invitation)
    session.commit()
    session.refresh(task_list_invitation)
    return task_list_invitation


def delete_user(task_list_invitation: TaskListInvitation, session: SessionDep):
    session.delete(task_list_invitation)
    session.commit()
