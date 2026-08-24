from app.core.db.db import SessionDep
from app.models.task_lists import TaskList


def create_task_list(task_list: TaskList, session: SessionDep) -> TaskList:
    session.add(task_list)
    session.commit()
    session.refresh(task_list)
    return task_list


def delete_user(task_list: TaskList, session: SessionDep):
    session.delete(task_list)
    session.commit()
