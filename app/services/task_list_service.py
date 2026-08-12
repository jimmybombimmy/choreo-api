from app.core.db import SessionDep
from app.models.task_lists import TaskList


def create_task_list(task_list: TaskList, session: SessionDep) -> TaskList:
    session.add(task_list)
    session.commit()
    session.refresh(task_list)
    return task_list


def get_current_task_list(user_id: TaskList, session: SessionDep):
    task_list = session.get(TaskList, user_id)
    print(f"task_list {task_list}")
    return task_list


def delete_user(task_list: TaskList, session: SessionDep):
    session.delete(task_list)
    session.commit()
